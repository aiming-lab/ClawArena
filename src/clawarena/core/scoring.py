"""Scoring pipeline — score infer results against ground truth."""

from __future__ import annotations

import json
from pathlib import Path

from clawarena.core.io import load_json, write_json
from clawarena.core.types import TestContext
from clawarena.qtypes.registry import get_qtype


def run_scoring(
    infer_dir: Path,
    out_dir: Path | None = None,
) -> None:
    """Score all infer_result.json files under infer_dir."""
    infer_files = sorted(infer_dir.rglob("infer_result.json"))
    if not infer_files:
        print(f"[warn] No infer_result.json found under {infer_dir}")
        return

    scored = 0
    for infer_path in infer_files:
        try:
            result = load_json(infer_path)
        except Exception:
            print(f"  [fail] cannot read {infer_path}")
            continue

        meta = result.get("meta", {})
        test_id = meta.get("test_id", "unknown")
        round_id = meta.get("round_id", "unknown")
        question_type = meta.get("question_type", "multi_choice")

        # Load round record from questions.json
        eval_path_rel = meta.get("eval_question_path", "")
        round_record = _find_round_record(infer_path, eval_path_rel, round_id)

        answer_text = result.get("answer", {}).get("text", "")

        ctx = TestContext(framework=meta.get("framework", ""), test_id=test_id)

        try:
            qtype = get_qtype(question_type)
            scored_result = qtype.score(answer_text, round_record or {}, ctx, infer_result=result)
        except ValueError:
            scored_result = {
                "extracted_answer": None, "correct_answer": None,
                "score": 0.0, "metrics": {},
            }

        scoring_data = {
            "meta": {
                "framework": meta.get("framework", ""),
                "test_id": test_id,
                "round_id": round_id,
                "question_type": question_type,
            },
            **scored_result,
        }

        if out_dir:
            scoring_path = out_dir / infer_path.relative_to(infer_dir).parent / "scoring.json"
        else:
            scoring_path = infer_path.parent / "scoring.json"

        write_json(scoring_path, scoring_data)
        _print_score(scoring_data)
        scored += 1

    print(f"\nScoring complete: {scored}/{len(infer_files)} processed.")


def _find_round_record(
    infer_path: Path, eval_path: str, round_id: str,
) -> dict | None:
    """Locate the round record from questions.json using eval_question_path."""
    if not eval_path:
        return None
    p = Path(eval_path)
    # Absolute path: use directly (written by infer pipeline)
    if p.is_absolute():
        if not p.exists():
            return None
        try:
            q_data = load_json(p)
            for rnd in q_data.get("rounds", []):
                if rnd.get("id") == round_id:
                    return rnd
        except Exception:
            pass
        return None
    # Legacy relative path: walk up ancestor directories to locate the file
    for ancestor in [infer_path.parent, *infer_path.parents]:
        candidate = ancestor / p
        if candidate.exists():
            try:
                q_data = load_json(candidate)
                for rnd in q_data.get("rounds", []):
                    if rnd.get("id") == round_id:
                        return rnd
            except Exception:
                pass
    return None


def _print_score(scoring: dict) -> None:
    meta = scoring.get("meta", {})
    s = scoring.get("score", 0)
    qtype = meta.get("question_type", "multi_choice")
    tid = meta.get("test_id", "?")
    rid = meta.get("round_id", "?")
    mark = "\u2713" if s else "\u2717"
    if qtype == "exec_check":
        passed = scoring.get("metrics", {}).get("passed", False)
        print(f"  [{mark}] {tid}/{rid}: exec_check={'pass' if passed else 'fail'} -> {s}")
    else:
        ex = ",".join(scoring.get("extracted_answer") or ["?"])
        cor = ",".join(scoring.get("correct_answer") or ["?"])
        print(f"  [{mark}] {tid}/{rid}: {ex} vs {cor} -> {s}")
