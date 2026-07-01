"""Collect benchmark stats from tests.json + manifest + eval data."""

from __future__ import annotations

from pathlib import Path

from clawarena.core.io import load_json, load_tests_config
from clawarena.qtypes.registry import get_qtype
from clawarena.stats.base import (
    BenchmarkStats, FileFact, FrameworkLayout, RoundFact, ScenarioStats,
    SessionFact, UpdateFact, WorkspaceFact,
)
from clawarena.stats.registry import get_layout
from clawarena.stats.session_parser import count_session_tokens
from clawarena.stats.tokenizer import TokenCounter


# ---------------------------------------------------------------------------
# Round-level collection
# ---------------------------------------------------------------------------

def _collect_round_text_tokens(
    rnd: dict, counter: TokenCounter, rtype: str,
) -> tuple[int, int, int, bool]:
    """Return (q_tokens, fb_tokens, pref_tokens, has_pref) for one round."""
    try:
        qtype = get_qtype(rtype)
        q_text = qtype.format_query(rnd, {})
    except Exception:
        q_text = rnd.get("question", "")
    q_tokens = counter.count(q_text)

    fb = rnd.get("feedback", {})
    fb_chunks: list[str] = []
    if isinstance(fb, dict):
        for v in fb.values():
            if isinstance(v, str):
                fb_chunks.append(v)
            elif isinstance(v, dict):
                fb_chunks.extend(vv for vv in v.values() if isinstance(vv, str))
    fb_tokens = counter.count("\n".join(fb_chunks))

    pref = rnd.get("pref")
    has_pref = isinstance(pref, dict)
    pref_tokens = 0
    if has_pref:
        chunks: list[str] = []
        cmd = pref.get("command")
        if isinstance(cmd, str):
            chunks.append(cmd)
        pfb = pref.get("feedback")
        if isinstance(pfb, dict):
            chunks.extend(v for v in pfb.values() if isinstance(v, str))
        rules = pref.get("rules")
        if isinstance(rules, list):
            for rule in rules:
                if isinstance(rule, str):
                    chunks.append(rule)
                elif isinstance(rule, dict):
                    chunks.extend(v for v in rule.values() if isinstance(v, str))
        pref_tokens = counter.count("\n".join(chunks))

    return q_tokens, fb_tokens, pref_tokens, has_pref


def _round_facts(
    scenario: str, rounds: list[dict], counter: TokenCounter,
) -> list[RoundFact]:
    out: list[RoundFact] = []
    for rnd in rounds:
        rid = rnd.get("id", "?")
        rtype = rnd.get("type", "multi_choice")
        q, fb, pref, has_pref = _collect_round_text_tokens(rnd, counter, rtype)
        has_updates = bool(rnd.get("update_ids"))

        mc_options = mc_answers = None
        ec_has_expect_exit = ec_has_expect_stdout = False
        ec_is_regex = ec_has_timeout = False
        ec_timeout: float | None = None

        ev = rnd.get("eval")
        if isinstance(ev, dict):
            if rtype == "multi_choice":
                opts = ev.get("options")
                if isinstance(opts, dict):
                    mc_options = len(opts)
                ans = ev.get("answer")
                if isinstance(ans, list):
                    mc_answers = len(ans)
                elif ans is not None:
                    mc_answers = 1
            elif rtype == "exec_check":
                ec_has_expect_exit = "expect_exit" in ev
                es = ev.get("expect_stdout")
                ec_has_expect_stdout = isinstance(es, str) and len(es) > 0
                ec_is_regex = bool(ev.get("expect_stdout_regex"))
                t = ev.get("timeout")
                if isinstance(t, (int, float)):
                    ec_has_timeout = True
                    ec_timeout = float(t)

        out.append(RoundFact(
            scenario=scenario, round_id=rid, type=rtype,
            has_pref=has_pref, has_updates=has_updates,
            q_tokens=q, fb_tokens=fb, pref_tokens=pref,
            mc_options=mc_options, mc_answers=mc_answers,
            ec_has_expect_exit=ec_has_expect_exit,
            ec_has_expect_stdout=ec_has_expect_stdout,
            ec_is_regex=ec_is_regex,
            ec_has_timeout=ec_has_timeout,
            ec_timeout=ec_timeout,
        ))
    return out


# ---------------------------------------------------------------------------
# Update / session / workspace collection
# ---------------------------------------------------------------------------

def _update_facts(
    scenario: str, manifest: dict, manifest_dir: Path,
    counter: TokenCounter, session_update_types: set[str],
    session_parser,
) -> list[UpdateFact]:
    out: list[UpdateFact] = []
    upd_map = manifest.get("updates", {}).get(scenario, {})
    for uid, umeta in upd_map.items():
        raw_type = umeta.get("type", "workspace")
        is_session = raw_type in session_update_types
        utype = "session" if is_session else raw_type
        udir = manifest_dir / umeta.get("dir", "")
        files: list[FileFact] = []
        for item in umeta.get("files", []):
            if isinstance(item, str):
                name, action = item, ""
            elif isinstance(item, dict):
                name = item.get("name", "")
                action = item.get("action", "")
            else:
                continue
            if not name:
                continue
            fpath = udir / name
            # Session-typed updates that ship as jsonl transcripts are
            # counted through the framework parser so that their token
            # budget reflects the prompt payload rather than raw JSON
            # bytes. Markdown session patches are counted verbatim.
            if (
                is_session
                and session_parser is not None
                and fpath.suffix.lower() == ".jsonl"
            ):
                tokens = count_session_tokens(fpath, session_parser, counter)
            else:
                tokens = counter.count_file(fpath)
            files.append(FileFact(name=name, action=action, tokens=tokens))
        out.append(UpdateFact(scenario=scenario, uid=uid, type=utype, files=files))
    return out


def _count_session_file(
    path: Path, parser, counter: TokenCounter,
) -> int:
    """Count a session file's tokens, routing jsonl through ``parser``
    when one is provided and the file exists."""
    if path is None or not path.exists():
        return 0
    if parser is not None and path.suffix.lower() == ".jsonl":
        return count_session_tokens(path, parser, counter)
    return counter.count_file(path)


def _session_facts(
    scenario: str, agent_info: dict, manifest_dir: Path,
    counter: TokenCounter, layout: FrameworkLayout,
) -> list[SessionFact]:
    out: list[SessionFact] = []
    main = layout.main_session_path(agent_info, manifest_dir, scenario)
    if main is not None:
        out.append(SessionFact(
            scenario=scenario, kind="main",
            tokens=_count_session_file(
                main, layout.main_session_parser, counter,
            ),
        ))
    hist_parser = layout.history_session_parser
    for hp in layout.history_session_paths(agent_info, manifest_dir, scenario):
        out.append(SessionFact(
            scenario=scenario, kind="history",
            tokens=_count_session_file(hp, hist_parser, counter),
        ))
    return out


def _workspace_fact(
    scenario: str, agent_info: dict, manifest_dir: Path,
    counter: TokenCounter, excludes: set[str],
) -> WorkspaceFact:
    rel = agent_info.get("workspace", "")
    if not rel:
        return WorkspaceFact(scenario=scenario, tokens=0)
    ws = manifest_dir / rel
    if not ws.exists():
        return WorkspaceFact(scenario=scenario, tokens=0)
    total = 0
    file_count = 0
    for f in ws.rglob("*"):
        if not f.is_file():
            continue
        try:
            parts = f.relative_to(ws).parts
        except ValueError:
            continue
        if parts and parts[0] in excludes:
            continue
        total += counter.count_file(f)
        file_count += 1
    return WorkspaceFact(scenario=scenario, tokens=total, files=file_count)


# ---------------------------------------------------------------------------
# Top-level
# ---------------------------------------------------------------------------

def collect_benchmark(
    tests_json_path: Path, framework: str, counter: TokenCounter,
) -> BenchmarkStats:
    """Collect a full BenchmarkStats for one framework."""
    cfg = load_tests_config(tests_json_path)
    base_dir = tests_json_path.parent
    manifest_rel = cfg["frameworks"][framework]["manifest"]
    manifest_path = base_dir / manifest_rel
    manifest = load_json(manifest_path)
    manifest_dir = manifest_path.parent
    eval_dir = base_dir / cfg.get("eval_dir", "eval")

    layout = get_layout(framework)

    bench = BenchmarkStats(
        name=cfg.get("name", tests_json_path.stem),
        framework=framework,
        tokenizer=counter.name,
    )

    for test in cfg.get("tests", []):
        sid = test["id"]
        eval_name = test.get("eval", sid)
        scenario = ScenarioStats(id=sid, desc=test.get("desc", ""))

        agent_info = manifest.get("agents", {}).get(sid, {})
        scenario.sessions = _session_facts(
            sid, agent_info, manifest_dir, counter, layout,
        )
        scenario.workspace = _workspace_fact(
            sid, agent_info, manifest_dir, counter, layout.workspace_excludes,
        )

        q_path = eval_dir / eval_name / "questions.json"
        if q_path.exists():
            try:
                q_data = load_json(q_path)
                rounds = q_data.get("rounds", [])
                scenario.rounds = _round_facts(sid, rounds, counter)
            except Exception:
                pass

        scenario.updates = _update_facts(
            sid, manifest, manifest_dir, counter,
            layout.session_update_types,
            layout.history_session_parser,
        )
        bench.scenarios.append(scenario)

    return bench
