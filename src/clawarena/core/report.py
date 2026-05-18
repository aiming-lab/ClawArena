"""Report generation — aggregate scoring results.

Headline metrics
----------------
- TCR (Task Completion Rate): per-round score mean.
- SC  (Success Cohesion):     (S - k) / (N - 1) over success run-lengths;
                              high when successes coalesce into long runs.
- FD  (Failure Dispersion):   1 - (S_fail - k_fail) / (N - 1);
                              high when failures stay scattered (or absent).
- Robustness = SC * FD.       Multiplicative streak health, range [0, 1].
- CRS = (TCR + Robustness) / 2.

Round order is taken from the eval directory's `questions.json` so streak
metrics reflect the true round sequence rather than filesystem order.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from clawarena.core.io import load_json, load_tests_config, write_json


# ---------------------------------------------------------------------------
# Streak / coherence kernel
# ---------------------------------------------------------------------------

def _runs(rounds: list[dict], success: bool, threshold: float) -> list[int]:
    lengths: list[int] = []
    cur = 0
    for r in rounds:
        is_success = r.get("score", 0.0) >= threshold
        match = is_success if success else (not is_success)
        if match:
            cur += 1
        else:
            if cur > 0:
                lengths.append(cur)
            cur = 0
    if cur > 0:
        lengths.append(cur)
    return lengths


def _coherence(lengths: list[int], n: int) -> float:
    s = sum(lengths)
    k = len(lengths)
    if n <= 1 or k == 0:
        return 0.0
    return (s - k) / (n - 1)


def _streak_metrics(rounds: list[dict], threshold: float = 1.0) -> dict:
    n = len(rounds)
    L = _runs(rounds, success=True, threshold=threshold)
    Lf = _runs(rounds, success=False, threshold=threshold)
    sc = _coherence(L, n)
    fd = 1.0 - _coherence(Lf, n)
    return {
        "sc": round(sc, 4),
        "fd": round(fd, 4),
        "streak_lengths": L,
        "num_streaks": len(L),
        "max_streak_length": max(L) if L else 0,
        "failure_streak_lengths": Lf,
        "num_failure_streaks": len(Lf),
        "max_failure_streak_length": max(Lf) if Lf else 0,
    }


def _robustness(sc: float, fd: float) -> float:
    """Robustness = SC * FD. Range [0, 1]."""
    return round(sc * fd, 4)


def _composite_reliability(tcr: float, sc: float, fd: float) -> float:
    """CRS = (TCR + Robustness) / 2 = (TCR + SC * FD) / 2. Range [0, 1]."""
    return round((tcr + sc * fd) / 2, 4)


def _safe_mean(xs: list[float]) -> float:
    xs = [x for x in xs if x is not None]
    return round(sum(xs) / len(xs), 4) if xs else 0.0


# ---------------------------------------------------------------------------
# Round-order resolution from tests.json + questions.json
# ---------------------------------------------------------------------------

def _build_round_order(tests_json: Path) -> dict[str, list[str]]:
    """Map test_id -> ordered list of round_ids, sourced from questions.json."""
    cfg = load_tests_config(tests_json)
    base_dir = tests_json.parent
    eval_dir = base_dir / cfg.get("eval_dir", "eval")
    order: dict[str, list[str]] = {}
    for test in cfg.get("tests", []):
        tid = test["id"]
        eval_name = test.get("eval", tid)
        q_path = eval_dir / eval_name / "questions.json"
        if not q_path.exists():
            continue
        try:
            q = load_json(q_path)
        except Exception:
            continue
        order[tid] = [r["id"] for r in q.get("rounds", []) if "id" in r]
    return order


# ---------------------------------------------------------------------------
# Token / timing extraction (unchanged)
# ---------------------------------------------------------------------------

def _empty_tokens() -> dict:
    return {"input": 0, "output": 0, "cache_read": 0, "total_input": 0}


def _extract_agent_tokens(infer_result: dict) -> dict:
    tokens = _empty_tokens()
    llm_log = infer_result.get("llm_log")
    if not isinstance(llm_log, dict):
        return tokens
    messages = llm_log.get("messages", [])
    for msg in messages:
        if msg.get("role") == "assistant":
            usage = msg.get("usage", {})
            tokens["input"] += usage.get("input", 0)
            tokens["output"] += usage.get("output", 0)
            tokens["cache_read"] += usage.get("cacheRead", 0)
    tokens["total_input"] = tokens["input"] + tokens["cache_read"]
    return tokens


# ---------------------------------------------------------------------------
# Main entry
# ---------------------------------------------------------------------------

def generate_report(score_dir: Path, out_dir: Path, tests_json: Path) -> None:
    """Generate report.json and report.md from scoring results.

    Round order is read from tests_json -> eval_dir/<sid>/questions.json so
    streak metrics (SC / FD / Robustness / CRS) reflect the true sequence.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    scoring_files = sorted(score_dir.rglob("scoring.json"))
    if not scoring_files:
        print(f"[warn] No scoring.json found under {score_dir}")
        return

    round_order = _build_round_order(tests_json)

    # Phase 1: collect raw round data per test (keyed by round_id for re-ordering).
    by_test: dict[str, dict] = {}

    for sp in scoring_files:
        try:
            scoring = load_json(sp)
        except Exception:
            continue

        meta = scoring.get("meta", {})
        test_id = meta.get("test_id", "unknown")
        round_id = meta.get("round_id", sp.parent.name)
        score = scoring.get("score", 0)

        bucket = by_test.setdefault(test_id, {
            "rounds_by_id": {}, "total_tokens": 0, "total_duration_ms": 0,
        })

        infer_path = sp.parent / "infer_result.json"
        if not infer_path.exists():
            parts = sp.parts
            if "scoring" in parts:
                idx = parts.index("scoring")
                infer_path = Path(
                    *parts[:idx], "infer", *parts[idx + 1:]
                ).with_name("infer_result.json")
        tokens = 0
        duration_ms = 0
        if infer_path.exists():
            try:
                ir = load_json(infer_path)
                agent_tok = _extract_agent_tokens(ir)
                tokens = agent_tok.get("total_input", 0) + agent_tok.get("output", 0)
                duration_ms = ir.get("timing", {}).get("duration_ms", 0)
            except Exception:
                pass

        bucket["rounds_by_id"][round_id] = {
            "round_id": round_id,
            "type": meta.get("question_type", "multi_choice"),
            "score": score,
            "tokens": tokens,
            "duration_ms": duration_ms,
        }
        bucket["total_tokens"] += tokens
        bucket["total_duration_ms"] += duration_ms

    # Phase 2: order rounds, compute per-test metrics.
    total_rounds = 0
    total_tokens = 0
    total_duration = 0
    by_test_list: list[dict] = []
    by_type: dict[str, dict] = {}

    for test_id in sorted(by_test):
        td = by_test[test_id]
        rounds_by_id: dict[str, dict] = td["rounds_by_id"]

        canonical = round_order.get(test_id, [])
        if canonical:
            ordered: list[dict] = [rounds_by_id[rid] for rid in canonical if rid in rounds_by_id]
            # Append any stragglers not declared in questions.json (sorted for determinism).
            extras = sorted(set(rounds_by_id) - set(canonical))
            ordered.extend(rounds_by_id[rid] for rid in extras)
        else:
            ordered = [rounds_by_id[rid] for rid in sorted(rounds_by_id)]

        n = len(ordered)
        tcr = round(sum(r["score"] for r in ordered) / n, 4) if n else 0.0

        sk = _streak_metrics(ordered)
        rob = _robustness(sk["sc"], sk["fd"])
        crs = _composite_reliability(tcr, sk["sc"], sk["fd"])

        by_test_list.append({
            "test_id": test_id,
            "rounds": n,
            "task_completion_rate": tcr,
            "composite_reliability_score": crs,
            "robustness": rob,
            "sc": sk["sc"],
            "fd": sk["fd"],
            "streak_lengths": sk["streak_lengths"],
            "num_streaks": sk["num_streaks"],
            "max_streak_length": sk["max_streak_length"],
            "failure_streak_lengths": sk["failure_streak_lengths"],
            "num_failure_streaks": sk["num_failure_streaks"],
            "max_failure_streak_length": sk["max_failure_streak_length"],
            "tokens": td["total_tokens"],
            "duration_ms": td["total_duration_ms"],
            "rounds_detail": ordered,
        })

        total_rounds += n
        total_tokens += td["total_tokens"]
        total_duration += td["total_duration_ms"]

        for r in ordered:
            rtype = r["type"]
            slot = by_type.setdefault(rtype, {"count": 0, "total_score": 0.0})
            slot["count"] += 1
            slot["total_score"] += r["score"]

    # Aggregate-of-tests for headline (mean over tests, not over rounds).
    tcr_avg = _safe_mean([t["task_completion_rate"] for t in by_test_list])
    sc_avg = _safe_mean([t["sc"] for t in by_test_list])
    fd_avg = _safe_mean([t["fd"] for t in by_test_list])
    rob_avg = _safe_mean([t["robustness"] for t in by_test_list])
    crs_summary = _composite_reliability(tcr_avg, sc_avg, fd_avg)

    framework = ""
    if scoring_files:
        try:
            first = load_json(scoring_files[0])
            framework = first.get("meta", {}).get("framework", "")
        except Exception:
            pass

    # experiment_id: dir two levels above scoring/ (e.g. results/<EXP>/<framework>/scoring)
    # falls back to <framework> if the path is too shallow (e.g. test fixtures).
    try:
        experiment_id = score_dir.resolve().parents[1].name or framework
    except IndexError:
        experiment_id = framework

    report = {
        "experiment_id": experiment_id,
        "framework": framework,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total_tests": len(by_test_list),
            "total_rounds": total_rounds,
            "task_completion_rate": tcr_avg,
            "composite_reliability_score": crs_summary,
            "robustness": rob_avg,
            "avg_sc": sc_avg,
            "avg_fd": fd_avg,
            "total_tokens": total_tokens,
            "total_duration_ms": total_duration,
        },
        "by_test": by_test_list,
        "by_type": {
            k: {"count": v["count"], "task_completion_rate": round(v["total_score"] / v["count"], 4)}
            for k, v in by_type.items()
        },
    }

    write_json(out_dir / "report.json", report)
    md = _render_markdown(report)
    (out_dir / "report.md").write_text(md, encoding="utf-8")
    print(f"Report written to {out_dir}")
    print(md)


def _render_markdown(report: dict) -> str:
    s = report["summary"]
    lines = [
        f"# Benchmark Report — {report.get('framework', '')}",
        "",
        "## Summary",
        "",
        f"- **Tests**: {s['total_tests']}",
        f"- **Rounds**: {s['total_rounds']}",
        f"- **CRS** (Composite Reliability Score): {s['composite_reliability_score']:.2%}  "
        f"_= (TCR + SC · FD) / 2_",
        f"- **TCR** (Task Completion Rate): {s['task_completion_rate']:.2%}",
        f"- **Robustness**: {s['robustness']:.2%}  _= SC · FD_",
        f"- **SC** (Success Cohesion): {s['avg_sc']:.2%}",
        f"- **FD** (Failure Dispersion): {s['avg_fd']:.2%}",
        f"- **Total Tokens**: {s['total_tokens']:,}",
        "",
        "## By Test",
        "",
        "| Test | Rounds | **CRS** | TCR | Robustness | SC | FD | Tokens |",
        "|------|--------|---------|-----|-----------|----|----|--------|",
    ]
    for t in report["by_test"]:
        lines.append(
            f"| {t['test_id']} | {t['rounds']} "
            f"| **{t['composite_reliability_score']:.2%}** "
            f"| {t['task_completion_rate']:.2%} "
            f"| {t['robustness']:.2%} "
            f"| {t['sc']:.2%} "
            f"| {t['fd']:.2%} "
            f"| {t['tokens']:,} |"
        )
    lines += ["", "## By Type", ""]
    for k, v in report.get("by_type", {}).items():
        lines.append(f"- **{k}**: {v['count']} rounds, TCR {v['task_completion_rate']:.2%}")
    lines += [
        "",
        "## Notes",
        "",
        "- **CRS** = (TCR + SC · FD) / 2. Range [0, 1]. TCR (correctness) and "
        "Robustness (streak health) carry equal weight.",
        "- **SC** = (S − k) / (N − 1) over success run-lengths; L=[N]→1, "
        "L=[1,1,…]→0, empty L→0.",
        "- **FD** = 1 − (S_fail − k_fail) / (N − 1) over failure run-lengths; "
        "no failures → 1, full failure cascade → 0.",
        "- **Robustness** = SC · FD. Multiplicative: either axis collapsing "
        "tanks the score.",
    ]
    return "\n".join(lines) + "\n"
