"""Cross-scenario run report aggregation; emits report.json and report.md.

Composite scoring system:
    SMS = 0.5 · TCS + 0.5 · MQS        — Subagent Management Score
    TCS = (TCR + SCR + SFR) / 3        — Task Correctness Subscore
    MQS = mean over scenarios of (TPS + ROS + WPS + MCS) / 4
                                       — Management Quality Subscore

Token billing view (per-call granularity, computed by the local tokenizer; decoupled from the provider):
    MCM / SCM ─ peak context occupancy; the basis compared against ``token_limit`` (the breaker criterion).
    MIT / SIT ─ cumulative input (sum of the new input of each model call).
    MOT / SOT ─ cumulative output (sum of the output of each model call).
    MCR / SCH ─ cumulative cache-read (sum of the context already present before each
                 call; ≈ the volume eligible to hit the prompt cache). Note: the SCR in
                 the NOTATION table is ``Scenario Completion Rate``, a different quantity
                 from cache-read here.
    MCU%      ─ MCM / token_limit, the main agent's context usage rate.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

# Abbreviation table: abbr -> (full name, one-line meaning). The compare module reuses this table to render the Notation section.
NOTATION: dict[str, tuple[str, str]] = {
    # composite
    "SMS": ("Subagent Management Score", "composite score = 0.5·TCS + 0.5·MQS, range [0,1]"),
    "TCS": ("Task Correctness Subscore", "= (TCR + SCR + SFR) / 3, equal-weighted aggregate of the three task-correctness metrics"),
    "MQS": ("Management Quality Subscore", "= mean over scenarios of (TPS+ROS+WPS+MCS)/4, subagent management quality"),
    # scored
    "TCR": ("Task Completion Rate", "average pass rate over user questions"),
    "SCR": ("Scenario Completion Rate", "per-scenario question average, then averaged across scenarios"),
    "SFR": ("Scenario Full-pass Rate", "1 if all questions in a scenario pass, averaged across scenarios"),
    "TPS": ("Tool Permission Score", "tool types used by subagent / tool types granted, averaged over subagents"),
    "ROS": ("Readonly Subagent Score", "0 if a read-only subagent is granted a mutating tool, else 1, averaged over subagents"),
    "WPS": ("Workspace Permission Score", "files actually accessed by subagent / total granted workspace files, averaged over subagents"),
    "MCS": ("Model Choice Score", "vlm must read image/video, omni must read audio, else 0, averaged over subagents"),
    # stats (statistics only)
    "SUB": ("Subagent Create Count", "total number of subagents created within the scenario"),
    "MKD": ("Model Key Distribution", "selection counts for llm/vlm/omni"),
    "INV": (
        "Invocation Distribution",
        "flattened five-way count of subagent invocation modes: {new,continue}×{runtime,background} + workflow",
    ),
    "BSH": ("Bash Mode Distribution", "count of Bash invocation modes {runtime, background} (main + subagent combined)"),
    "SOC": ("Structured Output Count", "number of subagent calls with schema-enforced structured output"),
    "TGC": ("Tools Grant Counts", "total count of tool types granted across all subagents"),
    "MAF": ("Main Agent Forbidden", "count of unauthorized accesses by the main agent"),
    "SAFt": ("Subagent Forbidden Total", "total count of unauthorized subagent accesses"),
    "SAFa": ("Subagent Forbidden Avg", "average subagent unauthorized accesses (per number of subagents)"),
    # token view (computed by the local tokenizer, comparable across providers)
    "MCM": (
        "Main Context Max",
        "peak context occupancy of the main agent after all turns are added; comparing it against token_limit decides the breaker",
    ),
    "MCU%": ("Main Context Use %", "= MCM / context_token_limit"),
    "MIT": (
        "Main Input Total",
        "main agent cumulative input (sum of the new input of each model call)",
    ),
    "MOT": (
        "Main Output Total",
        "main agent cumulative output (sum of each assistant turn itself)",
    ),
    "MCR": (
        "Main Cache-Read Total",
        "main agent cumulative cache-read (sum of the tokens already present in context before each call)",
    ),
    "SCM": (
        "Subagent Context Max (sum)",
        "sum of the context_size_max of each subagent session (a rough reflection of the sub usage ceiling)",
    ),
    "SIT": ("Subagent Input Total", "cumulative input across all subagent sessions"),
    "SOT": ("Subagent Output Total", "cumulative output across all subagent sessions"),
    "SCH": ("Subagent Cache-Hit Total", "cumulative cache-read across all subagent sessions"),
    "SST": ("Subagent System Tokens", "total subagent system prompt tokens (a static quantity)"),
}


# ---------------------------------------------------------------------------
# Paper-canonical metrics (md presentation only).
#
# The paper defines the composite as
#     SMS = TCR × (TPP + ROC + WPP + MCA) / 4
# and uses new abbreviations TPP/ROC/WPP/MCA for the four management sub-scores.
# These four share the EXACT numeric definition as the legacy TPS/ROS/WPS/MCS in
# metrics.py — only the abbreviation and the composite formula differ from the
# legacy `SMS = 0.5·TCS + 0.5·MQS`.
#
# We DERIVE the paper view purely from data already present in report.json
# (composite + scenarios[].metrics); we do NOT re-score, and we do NOT touch
# report.json's structure or write path. This block exists for md rendering only.
# ---------------------------------------------------------------------------
PAPER_NOTATION: dict[str, tuple[str, str]] = {
    "SMS": (
        "Subagent Management Score",
        "paper composite = TCR × (TPP + ROC + WPP + MCA) / 4, range [0,1]",
    ),
    "TCR": ("Task Completion Rate", "average pass rate over user questions (= legacy TCR)"),
    "TPP": (
        "Tool-Permission Precision",
        "share of tool types granted to and actually used by the subagent, averaged over subagents (= legacy TPS)",
    ),
    "ROC": (
        "Read-Only Compliance",
        "0 if a read-only subagent is granted a mutating tool, else 1, averaged over subagents (= legacy ROS)",
    ),
    "WPP": (
        "Workspace-Permission Precision",
        "files actually accessed by subagent / total granted files, averaged over subagents (= legacy WPS)",
    ),
    "MCA": (
        "Modality-Choice Accuracy",
        "vlm actually reads image/video, omni actually reads audio, llm counts 1, averaged over subagents (= legacy MCS)",
    ),
}

# paper abbr -> legacy composite key (run-level means already in report.json)
_PAPER_TO_LEGACY_COMPOSITE = {
    "TCR": "TCR",
    "TPP": "TPS",
    "ROC": "ROS",
    "WPP": "WPS",
    "MCA": "MCS",
}


def paper_composite_from_legacy(composite: dict[str, Any]) -> dict[str, float]:
    """Derive the paper-canonical composite from the legacy ``composite`` dict.

    ``SMS_paper = TCR × (TPP + ROC + WPP + MCA) / 4``, where the management
    quartet are the run-level means already stored as legacy TPS/ROS/WPS/MCS.
    Pure derivation — no recomputation of the underlying scores.
    """
    tcr = composite.get("TCR", 0.0)
    tpp = composite.get("TPS", 0.0)
    roc = composite.get("ROS", 0.0)
    wpp = composite.get("WPS", 0.0)
    mca = composite.get("MCS", 0.0)
    mgmt = (tpp + roc + wpp + mca) / 4.0
    return {
        "SMS": tcr * mgmt,
        "TCR": tcr,
        "TPP": tpp,
        "ROC": roc,
        "WPP": wpp,
        "MCA": mca,
    }


def paper_scenario_sms(m: dict[str, Any]) -> float:
    """Per-scenario paper SMS = TCR_scenario × mean(TPP, ROC, WPP, MCA).

    Pulls the four management sub-scores directly from a scenario's stored
    ``metrics`` dict; no recomputation.
    """
    tcr = m.get("task_success_rate", 0.0)
    mgmt = (
        m.get("tool_permission_score", 0.0)
        + m.get("readonly_subagent_score", 0.0)
        + m.get("workspace_permission_score", 0.0)
        + m.get("model_choice_score", 0.0)
    ) / 4.0
    return tcr * mgmt


def _render_paper_notation(push) -> None:
    push("| Abbr | Full name | Meaning |")
    push("|---|---|---|")
    for abbr, (full, desc) in PAPER_NOTATION.items():
        push(f"| **{abbr}** | {full} | {desc} |")


def _mqs_scenario(m: dict[str, Any]) -> float:
    return (
        m.get("tool_permission_score", 0.0)
        + m.get("readonly_subagent_score", 0.0)
        + m.get("workspace_permission_score", 0.0)
        + m.get("model_choice_score", 0.0)
    ) / 4.0


def _sms_scenario(m: dict[str, Any]) -> float:
    return 0.5 * m.get("task_success_rate", 0.0) + 0.5 * _mqs_scenario(m)


def _sum_dict(target: dict[str, int], src: dict[str, int] | None) -> None:
    if not src:
        return
    for k, v in src.items():
        target[k] = target.get(k, 0) + int(v)


def _render_dict(d: dict[str, int] | None) -> str:
    if not d:
        return "—"
    items = sorted(d.items(), key=lambda x: (-x[1], x[0]))
    return ", ".join(f"{k}:{v}" for k, v in items)


def collect_scenario_metadata(
    input_dirs: list[Path],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Recursively scan all scenarios' ``metadata.json`` under several result directories and concatenate them, deduplicating by ``scenario_id``.

    ``metadata.json`` is the sole criterion for "the scenario truly completed"
    (written by scenario_runner only after all background subagents of that
    scenario have wrapped up; failed/incomplete scenarios will not have one).
    Because scenarios are mutually independent, you can stitch a complete test run
    together from completed scenarios across different runs and hand it to
    :func:`build_run_report` to regenerate the report.

    When the same ``scenario_id`` appears in multiple runs, the one with the
    latest ``finished_at`` is kept (and counted into the duplicates diagnostics).
    **Note**: this function only checks whether metadata.json exists; it does not
    judge whether the API errored — that requires separate manual investigation.

    Returns ``(metadata list sorted by scenario_id, diagnostics dict)``. The
    diagnostics include ``scanned`` (total metadata read) / ``unique`` /
    ``duplicates`` ({sid: occurrence count}) / ``sources`` ({sid: path of the
    chosen one}).
    """
    by_id: dict[str, dict[str, Any]] = {}
    sources: dict[str, str] = {}
    duplicates: dict[str, int] = {}
    scanned = 0
    for d in input_dirs:
        for mpath in sorted(Path(d).rglob("metadata.json")):
            try:
                md = json.loads(mpath.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError, ValueError):
                continue
            sid = md.get("scenario_id")
            if not sid:
                continue
            scanned += 1
            prev = by_id.get(sid)
            if prev is None:
                by_id[sid] = md
                sources[sid] = str(mpath)
            else:
                duplicates[sid] = duplicates.get(sid, 1) + 1
                # keep the one with the newer finished_at (ISO time strings can be compared directly)
                if str(md.get("finished_at") or "") > str(prev.get("finished_at") or ""):
                    by_id[sid] = md
                    sources[sid] = str(mpath)
    ordered = [by_id[sid] for sid in sorted(by_id)]
    info = {
        "scanned": scanned,
        "unique": len(ordered),
        "duplicates": duplicates,
        "sources": sources,
    }
    return ordered, info


def build_run_report(
    run_id: str, scenario_metadata: list[dict[str, Any]]
) -> tuple[dict[str, Any], str]:
    scenarios: list[dict[str, Any]] = []
    all_pass_count = 0
    scenario_acc: list[float] = []
    question_passes: list[float] = []
    mqs_per_scenario: list[float] = []

    mkd_total: dict[str, int] = {}
    inv_total: dict[str, int] = {}
    bsh_total: dict[str, int] = {}
    tgc_total: dict[str, int] = {}
    maf_total = saft_total = sub_total = soc_total = 0
    # token aggregation
    mit_total = mot_total = mcr_total = 0
    mcm_max = 0
    sst_total = scm_sum = sit_total = sot_total = sch_total = 0
    # used to compute MCU%: take the strictest token_limit across all scenarios; default 200000
    token_limit_observed = 0

    for md in scenario_metadata:
        m = md.get("metrics") or {}
        sms_s = _sms_scenario(m)
        mqs_s = _mqs_scenario(m)
        scenarios.append(
            {
                "scenario_id": md.get("scenario_id"),
                "task_success_rate": m.get("task_success_rate", 0.0),
                "rounds_passed": m.get("rounds_passed", 0),
                "rounds_total": m.get("rounds_total", 0),
                "sms_scenario": sms_s,
                "mqs_scenario": mqs_s,
                "metrics": m,
            }
        )

        if m.get("rounds_total") and m.get("rounds_passed") == m.get("rounds_total"):
            all_pass_count += 1
        scenario_acc.append(m.get("task_success_rate", 0.0))
        for r in md.get("rounds") or []:
            question_passes.append(1.0 if r.get("passed") else 0.0)

        mqs_per_scenario.append(mqs_s)
        sub_total += m.get("subagent_create_count", 0)
        _sum_dict(mkd_total, m.get("model_key_distribution"))
        _sum_dict(inv_total, m.get("invocation_distribution"))
        _sum_dict(bsh_total, m.get("bash_mode_distribution"))
        _sum_dict(tgc_total, m.get("tools_grant_counts"))
        soc_total += m.get("structured_output_count", 0)
        maf_total += m.get("main_agent_forbidden_count", 0)
        saft_total += m.get("subagent_forbidden_total", 0)
        mit_total += m.get("main_agent_input_total", 0)
        mot_total += m.get("main_agent_output_total", 0)
        mcr_total += m.get("main_agent_cache_read_total", 0)
        mcm_max = max(mcm_max, m.get("main_agent_context_size_max", 0))
        sst_total += m.get("subagent_system_tokens", 0)
        scm_sum += m.get("subagent_context_size_max_sum", 0)
        sit_total += m.get("subagent_input_total", 0)
        sot_total += m.get("subagent_output_total", 0)
        sch_total += m.get("subagent_cache_read_total", 0)
        # Fix (fix/audit-top10 #3): scenario_runner now writes token_limit at the top level of
        # metadata; older runs (which wrote it nested under metadata.metadata.token_limit) get a
        # backward-compatible fallback.
        lim = md.get("token_limit")
        if not (isinstance(lim, int) and lim > 0):
            nested = md.get("metadata")
            lim = nested.get("token_limit") if isinstance(nested, dict) else None
        if isinstance(lim, int) and lim > 0:
            token_limit_observed = lim if token_limit_observed == 0 else min(token_limit_observed, lim)

    if token_limit_observed == 0:
        token_limit_observed = 200000  # consistent with the default.yaml fallback

    n = len(scenarios) or 1
    tcr = (sum(question_passes) / len(question_passes)) if question_passes else 0.0
    scnr = sum(scenario_acc) / n
    sfr = all_pass_count / n
    tcs = (tcr + scnr + sfr) / 3.0
    mqs_run = (sum(mqs_per_scenario) / len(mqs_per_scenario)) if mqs_per_scenario else 0.0
    sms_run = 0.5 * tcs + 0.5 * mqs_run
    safa_run = (saft_total / sub_total) if sub_total > 0 else 0.0

    tps_avg = sum(s["metrics"].get("tool_permission_score", 0.0) for s in scenarios) / n
    ros_avg = sum(s["metrics"].get("readonly_subagent_score", 0.0) for s in scenarios) / n
    wps_avg = sum(s["metrics"].get("workspace_permission_score", 0.0) for s in scenarios) / n
    mcs_avg = sum(s["metrics"].get("model_choice_score", 0.0) for s in scenarios) / n

    composite = {
        "SMS": sms_run,
        "TCS": tcs,
        "MQS": mqs_run,
        "TCR": tcr,
        "SCR": scnr,
        "SFR": sfr,
        "TPS": tps_avg,
        "ROS": ros_avg,
        "WPS": wps_avg,
        "MCS": mcs_avg,
    }
    mcu_pct = (mcm_max / token_limit_observed) if token_limit_observed else 0.0
    statistics = {
        "SUB": sub_total,
        "MKD": dict(mkd_total),
        "INV": dict(inv_total),
        "BSH": dict(bsh_total),
        "SOC": soc_total,
        "TGC": dict(tgc_total),
        "MAF": maf_total,
        "SAFt": saft_total,
        "SAFa": safa_run,
        "MCM": mcm_max,
        "MCU%": mcu_pct,
        "MIT": mit_total,
        "MOT": mot_total,
        "MCR": mcr_total,
        "SCM": scm_sum,
        "SIT": sit_total,
        "SOT": sot_total,
        "SCH": sch_total,
        "SST": sst_total,
        "context_token_limit": token_limit_observed,
    }

    rounds_pass = int(sum(question_passes))
    rounds_total = int(len(question_passes))

    report = {
        "run_id": run_id,
        "scenarios": scenarios,
        # legacy keys (backward compatible with existing consumers)
        "avg_task_success_rate": tcr,
        "avg_scenario_success_rate": scnr,
        "avg_scenario_full_pass_rate": sfr,
        # new
        "composite": composite,
        "statistics": statistics,
        "rounds_pass": rounds_pass,
        "rounds_total": rounds_total,
        "scenarios_count": len(scenarios),
    }
    md_text = _render_markdown(
        run_id, scenarios, composite, statistics,
        rounds_pass=rounds_pass, rounds_total=rounds_total,
    )
    return report, md_text


def _render_markdown(
    run_id: str,
    scenarios: list[dict[str, Any]],
    composite: dict[str, Any],
    statistics: dict[str, Any],
    *,
    rounds_pass: int,
    rounds_total: int,
) -> str:
    lines: list[str] = []
    push = lines.append

    push(f"# Run Report — {run_id}")
    push("")
    push(f"Scenarios: {len(scenarios)}  ·  Rounds passed: {rounds_pass} / {rounds_total}")
    push("")

    # ---- Paper-canonical section (first; matches paper metric definitions) ----
    paper = paper_composite_from_legacy(composite)
    push("## Paper metrics (canonical)")
    push("")
    push("> Metrics correspond exactly to the paper. Composite and per-scenario")
    push("> values are **derived** from the data already in `report.json` (no")
    push("> re-scoring): SMS = TCR × (TPP + ROC + WPP + MCA) / 4.")
    push("")
    push("**Composite (paper)**")
    push("")
    push(f"- **SMS** {paper['SMS']:.2%}  _= TCR × (TPP + ROC + WPP + MCA) / 4_")
    push(
        f"- TCR {paper['TCR']:.2%}  ·  TPP {paper['TPP']:.2%}  ·  "
        f"ROC {paper['ROC']:.2%}  ·  WPP {paper['WPP']:.2%}  ·  MCA {paper['MCA']:.2%}"
    )
    push("")
    push("### Leaderboard — per scenario (paper)")
    push("")
    push("| Scenario | Pass | SMS (paper) | TCR | TPP | ROC | WPP | MCA |")
    push("|---|---|---|---|---|---|---|---|")
    for s in sorted(scenarios, key=lambda x: -paper_scenario_sms(x["metrics"])):
        m = s["metrics"]
        push(
            f"| {s['scenario_id']} "
            f"| {m.get('rounds_passed', 0)}/{m.get('rounds_total', 0)} "
            f"| **{paper_scenario_sms(m):.2%}** "
            f"| {m.get('task_success_rate', 0.0):.2%} "
            f"| {m.get('tool_permission_score', 0.0):.2%} "
            f"| {m.get('readonly_subagent_score', 0.0):.2%} "
            f"| {m.get('workspace_permission_score', 0.0):.2%} "
            f"| {m.get('model_choice_score', 0.0):.2%} |"
        )
    push("")
    push("### Notation (paper)")
    push("")
    _render_paper_notation(push)
    push("")
    push("---")
    push("")

    # ---- Legacy detailed statistics (different composite; kept for reference) ----
    push("## Legacy detailed statistics")
    push("")
    push(
        "> Legacy detailed statistics — metric definitions (composite "
        "SMS = 0.5·TCS + 0.5·MQS) differ from the paper; kept for reference."
    )
    push(
        "> Legacy abbreviations map to paper ones (same numeric definition): "
        "**TPS→TPP, ROS→ROC, WPS→WPP, MCS→MCA**."
    )
    push("")
    push("## Summary")
    push("")
    push("**Composite**")
    push("")
    push(f"- **SMS** {composite['SMS']:.2%}  _= 0.5·TCS + 0.5·MQS_")
    push(f"- **TCS** {composite['TCS']:.2%}  _= (TCR + SCR + SFR) / 3_")
    push(f"- **MQS** {composite['MQS']:.2%}  _= mean over scenarios of (TPS+ROS+WPS+MCS)/4_")
    push("")
    push("**Scored aggregates**")
    push("")
    push(
        f"- TCR {composite['TCR']:.2%}  ·  SCR {composite['SCR']:.2%}  ·  "
        f"SFR {composite['SFR']:.2%}"
    )
    push(
        f"- TPS {composite['TPS']:.2%}  ·  ROS {composite['ROS']:.2%}  ·  "
        f"WPS {composite['WPS']:.2%}  ·  MCS {composite['MCS']:.2%}"
    )
    push("")
    push("**Statistics aggregates**")
    push("")
    push(
        f"- SUB {statistics['SUB']}  ·  "
        f"MKD {_render_dict(statistics['MKD'])}  ·  "
        f"INV {_render_dict(statistics['INV'])}"
    )
    push(
        f"- BSH {_render_dict(statistics['BSH'])}  ·  "
        f"SOC {statistics['SOC']}"
    )
    push(f"- TGC {_render_dict(statistics['TGC'])}")
    push(
        f"- MAF {statistics['MAF']}  ·  SAFt {statistics['SAFt']}  ·  "
        f"SAFa {statistics['SAFa']:.2f}"
    )
    push(
        f"- MCM {statistics['MCM']:,} / {statistics['context_token_limit']:,} "
        f"(**MCU% {statistics['MCU%']:.1%}**)"
    )
    push(
        f"- MIT {statistics['MIT']:,}  ·  MOT {statistics['MOT']:,}  ·  "
        f"MCR {statistics['MCR']:,}"
    )
    push(
        f"- SCM {statistics['SCM']:,}  ·  SIT {statistics['SIT']:,}  ·  "
        f"SOT {statistics['SOT']:,}  ·  SCH {statistics['SCH']:,}  ·  "
        f"SST {statistics['SST']:,}"
    )
    push("")

    # Scored per scenario
    push("## Scored — per scenario")
    push("")
    push("| Scenario | Pass | SMS | TCR | TPS | ROS | WPS | MCS |")
    push("|---|---|---|---|---|---|---|---|")
    for s in scenarios:
        m = s["metrics"]
        push(
            f"| {s['scenario_id']} "
            f"| {m.get('rounds_passed', 0)}/{m.get('rounds_total', 0)} "
            f"| **{s['sms_scenario']:.2%}** "
            f"| {m.get('task_success_rate', 0.0):.2%} "
            f"| {m.get('tool_permission_score', 0.0):.2%} "
            f"| {m.get('readonly_subagent_score', 0.0):.2%} "
            f"| {m.get('workspace_permission_score', 0.0):.2%} "
            f"| {m.get('model_choice_score', 0.0):.2%} |"
        )
    push("")

    # Statistics per scenario — subagent
    push("## Statistics — Subagent & Forbidden (per scenario)")
    push("")
    push("| Scenario | SUB | MKD | INV | TGC | MAF | SAFt | SAFa |")
    push("|---|---|---|---|---|---|---|---|")
    for s in scenarios:
        m = s["metrics"]
        push(
            f"| {s['scenario_id']} "
            f"| {m.get('subagent_create_count', 0)} "
            f"| {_render_dict(m.get('model_key_distribution'))} "
            f"| {_render_dict(m.get('invocation_distribution'))} "
            f"| {_render_dict(m.get('tools_grant_counts'))} "
            f"| {m.get('main_agent_forbidden_count', 0)} "
            f"| {m.get('subagent_forbidden_total', 0)} "
            f"| {m.get('subagent_forbidden_avg', 0.0):.2f} |"
        )
    push("")

    # Statistics per scenario — tokens (main)
    limit = statistics.get("context_token_limit") or 1
    push("## Statistics — Main Agent Tokens (per scenario)")
    push("")
    push("| Scenario | MCM | MCU% | MIT | MOT | MCR |")
    push("|---|---|---|---|---|---|")
    for s in scenarios:
        m = s["metrics"]
        mcm = m.get("main_agent_context_size_max", 0)
        push(
            f"| {s['scenario_id']} "
            f"| {mcm:,} "
            f"| {(mcm / limit):.1%} "
            f"| {m.get('main_agent_input_total', 0):,} "
            f"| {m.get('main_agent_output_total', 0):,} "
            f"| {m.get('main_agent_cache_read_total', 0):,} |"
        )
    push("")

    # Statistics per scenario — tokens (subagent)
    push("## Statistics — Subagent Tokens (per scenario)")
    push("")
    push("| Scenario | SCM | SIT | SOT | SCH | SST |")
    push("|---|---|---|---|---|---|")
    for s in scenarios:
        m = s["metrics"]
        push(
            f"| {s['scenario_id']} "
            f"| {m.get('subagent_context_size_max_sum', 0):,} "
            f"| {m.get('subagent_input_total', 0):,} "
            f"| {m.get('subagent_output_total', 0):,} "
            f"| {m.get('subagent_cache_read_total', 0):,} "
            f"| {m.get('subagent_system_tokens', 0):,} |"
        )
    push("")

    push("## Notation (legacy)")
    push("")
    push(
        "_Legacy abbreviations; the four management sub-scores equal the paper's_ "
        "_TPS→TPP, ROS→ROC, WPS→WPP, MCS→MCA (same numeric definition)._"
    )
    push("")
    push("| Abbr | Full name | Meaning |")
    push("|---|---|---|")
    for abbr, (full, desc) in NOTATION.items():
        push(f"| **{abbr}** | {full} | {desc} |")

    return "\n".join(lines) + "\n"
