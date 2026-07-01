"""Cross-run comparison: takes multiple report.json files and emits comparison.json + comparison.md.

The output is structurally consistent with report.md: a scored table and a
statistics-only table + a Notation section.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .report import (
    NOTATION,
    _render_dict,
    _render_paper_notation,
    paper_composite_from_legacy,
    paper_scenario_sms,
)


def _label(report: dict[str, Any], idx: int) -> str:
    return report.get("run_id") or f"run_{idx}"


def build_comparison(
    report_paths: list[Path],
) -> tuple[dict[str, Any], str]:
    if len(report_paths) < 2:
        raise ValueError("at least 2 report.json paths required for comparison")

    raw_reports: list[dict[str, Any]] = []
    for p in report_paths:
        with open(p, "r", encoding="utf-8") as f:
            raw_reports.append(json.load(f))

    # Fix (fix/audit-top10 W2 F3 / v1#9): previously label=run_id, so with duplicate
    # run_ids the `label_to_report = {lab: r ...}` dict comprehension let the later one
    # overwrite the earlier; the earlier report's per-scenario data vanished from the
    # mapping; summary_rows still zipped out two rows with the same name, and the pivot
    # table's two columns pointed at the same data with no warning at all. Here we detect
    # duplicate labels and append `#idx` to disambiguate, then warn.
    raw_labels = [_label(r, i) for i, r in enumerate(raw_reports)]
    seen_count: dict[str, int] = {}
    labels: list[str] = []
    for lab in raw_labels:
        seen_count[lab] = seen_count.get(lab, 0) + 1
        if seen_count[lab] == 1 and raw_labels.count(lab) == 1:
            labels.append(lab)
        else:
            labels.append(f"{lab}#{seen_count[lab]}")
    if any(c > 1 for c in seen_count.values()):
        import sys
        dupes = [k for k, c in seen_count.items() if c > 1]
        print(f"[compare.py] WARN: duplicate run_id(s) {dupes}; suffixed with #N to disambiguate.",
              file=sys.stderr)

    summary_rows: list[dict[str, Any]] = []
    for r, lab in zip(raw_reports, labels):
        summary_rows.append(
            {
                "label": lab,
                "composite": r.get("composite", {}),
                "statistics": r.get("statistics", {}),
                "rounds_pass": r.get("rounds_pass", 0),
                "rounds_total": r.get("rounds_total", 0),
                "scenarios_count": r.get("scenarios_count", len(r.get("scenarios", []))),
            }
        )

    # sort by SMS descending
    summary_rows.sort(key=lambda x: -x["composite"].get("SMS", 0.0))
    ordered_labels = [r["label"] for r in summary_rows]
    label_to_report = {lab: r for lab, r in zip(labels, raw_reports)}

    # per-scenario pivot: rows=scenario_id, columns=run label
    seen: set[str] = set()
    all_sids: list[str] = []
    for r in raw_reports:
        for s in r.get("scenarios", []):
            sid = s.get("scenario_id")
            if sid and sid not in seen:
                seen.add(sid)
                all_sids.append(sid)

    by_scenario: list[dict[str, Any]] = []
    for sid in all_sids:
        per_exp: dict[str, dict[str, Any]] = {}
        for lab in ordered_labels:
            r = label_to_report[lab]
            for s in r.get("scenarios", []):
                if s.get("scenario_id") == sid:
                    per_exp[lab] = {
                        "sms": s.get("sms_scenario", 0.0),
                        "metrics": s.get("metrics", {}),
                    }
                    break
        by_scenario.append({"scenario_id": sid, "per_experiment": per_exp})

    comparison = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "labels": ordered_labels,
        "summary": summary_rows,
        "by_scenario": by_scenario,
    }
    md_text = _render_comparison_md(comparison)
    return comparison, md_text


def _render_comparison_md(c: dict[str, Any]) -> str:
    labels: list[str] = c["labels"]
    summary: list[dict[str, Any]] = c["summary"]

    lines: list[str] = []
    push = lines.append

    push("# Run Comparison")
    push("")
    push(f"_Generated at {c['generated_at']}_  ·  Runs sorted by **SMS** (descending).")
    push("")

    # ---- Paper-canonical leaderboard (first; matches paper metric definitions) ----
    push("## Paper metrics (canonical)")
    push("")
    push("> Metrics correspond exactly to the paper. Values are **derived** from")
    push("> each `report.json` (no re-scoring): SMS = TCR × (TPP + ROC + WPP + MCA) / 4.")
    push("")
    push("### Leaderboard — by run (paper)")
    push("")
    paper_rows = [
        {"label": row["label"], "paper": paper_composite_from_legacy(row.get("composite", {})),
         "rounds_pass": row["rounds_pass"], "rounds_total": row["rounds_total"]}
        for row in summary
    ]
    paper_rows.sort(key=lambda x: -x["paper"]["SMS"])
    push("| Run | **SMS** | TCR | TPP | ROC | WPP | MCA | Pass |")
    push("|---|---|---|---|---|---|---|---|")
    for pr in paper_rows:
        p = pr["paper"]
        push(
            f"| {pr['label']} "
            f"| **{p['SMS']:.2%}** "
            f"| {p['TCR']:.2%} "
            f"| {p['TPP']:.2%} "
            f"| {p['ROC']:.2%} "
            f"| {p['WPP']:.2%} "
            f"| {p['MCA']:.2%} "
            f"| {pr['rounds_pass']}/{pr['rounds_total']} |"
        )
    push("")
    push("### SMS (paper) — per scenario × run")
    push("")
    push("| Scenario | " + " | ".join(labels) + " |")
    push("|---|" + "|".join("---" for _ in labels) + "|")
    for row in c["by_scenario"]:
        cells: list[str] = []
        for lab in labels:
            entry = row["per_experiment"].get(lab)
            cells.append(f"{paper_scenario_sms(entry['metrics']):.2%}" if entry else "—")
        push(f"| {row['scenario_id']} | " + " | ".join(cells) + " |")
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

    # Scored — by run
    push("## Composite & Scored — by run")
    push("")
    push("| Run | **SMS** | TCS | MQS | TCR | SCR | SFR | TPS | ROS | WPS | MCS | Pass |")
    push("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for row in summary:
        comp = row["composite"]
        push(
            f"| {row['label']} "
            f"| **{comp.get('SMS', 0.0):.2%}** "
            f"| {comp.get('TCS', 0.0):.2%} "
            f"| {comp.get('MQS', 0.0):.2%} "
            f"| {comp.get('TCR', 0.0):.2%} "
            f"| {comp.get('SCR', 0.0):.2%} "
            f"| {comp.get('SFR', 0.0):.2%} "
            f"| {comp.get('TPS', 0.0):.2%} "
            f"| {comp.get('ROS', 0.0):.2%} "
            f"| {comp.get('WPS', 0.0):.2%} "
            f"| {comp.get('MCS', 0.0):.2%} "
            f"| {row['rounds_pass']}/{row['rounds_total']} |"
        )
    push("")

    # Statistics — by run (subagent / forbidden)
    push("## Statistics — Subagent & Forbidden — by run")
    push("")
    push("| Run | SUB | MKD | INV | TGC | MAF | SAFt | SAFa |")
    push("|---|---|---|---|---|---|---|---|")
    for row in summary:
        s = row["statistics"]
        push(
            f"| {row['label']} "
            f"| {s.get('SUB', 0)} "
            f"| {_render_dict(s.get('MKD'))} "
            f"| {_render_dict(s.get('INV'))} "
            f"| {_render_dict(s.get('TGC'))} "
            f"| {s.get('MAF', 0)} "
            f"| {s.get('SAFt', 0)} "
            f"| {s.get('SAFa', 0.0):.2f} |"
        )
    push("")

    # Statistics — tokens — by run (main agent)
    push("## Statistics — Main Agent Tokens — by run")
    push("")
    push("| Run | MCM | MCU% | MIT | MOT | MCR |")
    push("|---|---|---|---|---|---|")
    for row in summary:
        s = row["statistics"]
        push(
            f"| {row['label']} "
            f"| {s.get('MCM', 0):,} "
            f"| {s.get('MCU%', 0.0):.1%} "
            f"| {s.get('MIT', 0):,} "
            f"| {s.get('MOT', 0):,} "
            f"| {s.get('MCR', 0):,} |"
        )
    push("")

    # Statistics — tokens — by run (subagent)
    push("## Statistics — Subagent Tokens — by run")
    push("")
    push("| Run | SCM | SIT | SOT | SCH | SST |")
    push("|---|---|---|---|---|---|")
    for row in summary:
        s = row["statistics"]
        push(
            f"| {row['label']} "
            f"| {s.get('SCM', 0):,} "
            f"| {s.get('SIT', 0):,} "
            f"| {s.get('SOT', 0):,} "
            f"| {s.get('SCH', 0):,} "
            f"| {s.get('SST', 0):,} |"
        )
    push("")

    # Per-scenario SMS pivot
    push("## SMS — per scenario × run")
    push("")
    push("| Scenario | " + " | ".join(labels) + " |")
    push("|---|" + "|".join("---" for _ in labels) + "|")
    for row in c["by_scenario"]:
        cells: list[str] = []
        for lab in labels:
            entry = row["per_experiment"].get(lab)
            cells.append(f"{entry['sms']:.2%}" if entry else "—")
        push(f"| {row['scenario_id']} | " + " | ".join(cells) + " |")
    push("")

    # Notation reuses report.NOTATION
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
