"""Tests for report generation."""

import json
from pathlib import Path

from clawarena.core.report import generate_report


def _write_scoring(score_dir: Path, test_id: str, round_id: str,
                   score: float, qtype: str = "multi_choice") -> None:
    d = score_dir / test_id / round_id
    d.mkdir(parents=True, exist_ok=True)
    scoring = {
        "meta": {
            "framework": "openclaw",
            "test_id": test_id,
            "round_id": round_id,
            "question_type": qtype,
        },
        "extracted_answer": ["A"],
        "correct_answer": ["A"],
        "score": score,
        "metrics": {"exact_match": 1.0 if score == 1.0 else 0.0},
    }
    (d / "scoring.json").write_text(json.dumps(scoring))
    infer = {
        "timing": {"duration_ms": 1000},
        "llm_log": {"messages": [
            {"role": "assistant", "usage": {"input": 100, "output": 50, "cacheRead": 10}},
        ]},
    }
    (d / "infer_result.json").write_text(json.dumps(infer))


def _write_tests_config(root: Path, tests: list[tuple[str, list[str]]]) -> Path:
    """Create tests.json + eval/<sid>/questions.json fixtures.

    `tests` is a list of (test_id, [round_id, ...]) — the round_id order is
    used as the canonical sequence for streak metrics.
    """
    eval_dir = root / "eval"
    for tid, round_ids in tests:
        d = eval_dir / tid
        d.mkdir(parents=True, exist_ok=True)
        rounds = [{"id": rid, "type": "multi_choice"} for rid in round_ids]
        (d / "questions.json").write_text(json.dumps({"id": tid, "rounds": rounds}))
    cfg = {
        "name": "test-bench",
        "eval_dir": "eval",
        "frameworks": {"openclaw": {"manifest": "openclaw/manifest.json"}},
        "tests": [{"id": tid, "eval": tid} for tid, _ in tests],
    }
    tests_json = root / "tests.json"
    tests_json.write_text(json.dumps(cfg))
    return tests_json


def test_report_generation(tmp_path):
    tests_json = _write_tests_config(tmp_path, [("t1", ["r1"])])
    score_dir = tmp_path / "scores"
    _write_scoring(score_dir, "t1", "r1", 1.0)

    out_dir = tmp_path / "report"
    generate_report(score_dir, out_dir, tests_json)

    assert (out_dir / "report.json").exists()
    assert (out_dir / "report.md").exists()

    report = json.loads((out_dir / "report.json").read_text())
    s = report["summary"]
    assert s["total_tests"] == 1
    assert s["total_rounds"] == 1
    assert s["task_completion_rate"] == 1.0
    assert "avg_score" not in s
    # N=1 is degenerate for the (S-k)/(N-1) kernel: SC clamps to 0.0.
    # FD = 1 - 0 = 1.0 (no failure runs). Robustness = 0; CRS = (1.0 + 0)/2.
    assert s["avg_sc"] == 0.0
    assert s["avg_fd"] == 1.0
    assert s["robustness"] == 0.0
    assert s["composite_reliability_score"] == 0.5


def test_report_streak_metrics_use_questions_order(tmp_path):
    # Canonical order [r1..r5] but filesystem-sorted order would be different.
    tests_json = _write_tests_config(tmp_path, [("t1", ["r1", "r2", "r3", "r4", "r5"])])
    score_dir = tmp_path / "scores"
    # Trajectory: 1, 1, 0, 1, 1 -> success runs [2, 2], failure runs [1].
    # SC = (4-2)/(5-1) = 0.5; CFR = (1-1)/(5-1) = 0 → FD = 1.
    # Robustness = 0.5; CRS = (0.8 + 0.5)/2 = 0.65.
    for rid, sc in zip(["r1", "r2", "r3", "r4", "r5"], [1.0, 1.0, 0.0, 1.0, 1.0]):
        _write_scoring(score_dir, "t1", rid, sc)

    out_dir = tmp_path / "report"
    generate_report(score_dir, out_dir, tests_json)

    report = json.loads((out_dir / "report.json").read_text())
    t = report["by_test"][0]
    assert t["task_completion_rate"] == 0.8
    assert t["sc"] == 0.5
    assert t["fd"] == 1.0
    assert t["robustness"] == 0.5
    assert t["composite_reliability_score"] == 0.65
    assert t["streak_lengths"] == [2, 2]
    assert t["failure_streak_lengths"] == [1]
    assert [r["round_id"] for r in t["rounds_detail"]] == ["r1", "r2", "r3", "r4", "r5"]


def test_report_multiple_tests(tmp_path):
    tests_json = _write_tests_config(tmp_path, [
        ("t1", ["r1", "r2"]),
        ("t2", ["r1"]),
    ])
    score_dir = tmp_path / "scores"
    _write_scoring(score_dir, "t1", "r1", 1.0)
    _write_scoring(score_dir, "t1", "r2", 0.5)
    _write_scoring(score_dir, "t2", "r1", 0.0)

    out_dir = tmp_path / "report"
    generate_report(score_dir, out_dir, tests_json)
    report = json.loads((out_dir / "report.json").read_text())
    assert report["summary"]["total_rounds"] == 3
    assert len(report["by_test"]) == 2


def test_report_reads_infer_from_parallel_infer_tree(tmp_path):
    tests_json = _write_tests_config(tmp_path, [("t1", ["r1"])])
    score_dir = tmp_path / "openclaw" / "scoring"
    infer_dir = tmp_path / "openclaw" / "infer"
    score_round = score_dir / "t1" / "r1"
    infer_round = infer_dir / "t1" / "r1"
    score_round.mkdir(parents=True)
    infer_round.mkdir(parents=True)

    scoring = {
        "meta": {
            "framework": "openclaw", "test_id": "t1", "round_id": "r1",
            "question_type": "multi_choice",
        },
        "score": 1.0,
        "metrics": {"exact_match": 1.0},
    }
    (score_round / "scoring.json").write_text(json.dumps(scoring))
    infer = {
        "timing": {"duration_ms": 2345},
        "llm_log": {"messages": [
            {"role": "assistant", "usage": {"input": 10, "output": 5, "cacheRead": 1}},
        ]},
    }
    (infer_round / "infer_result.json").write_text(json.dumps(infer))

    out_dir = tmp_path / "report"
    generate_report(score_dir, out_dir, tests_json)
    report = json.loads((out_dir / "report.json").read_text())
    assert report["summary"]["total_duration_ms"] == 2345
    assert report["summary"]["total_tokens"] == 16


def test_report_no_scoring(tmp_path, capsys):
    tests_json = _write_tests_config(tmp_path, [("t1", ["r1"])])
    generate_report(tmp_path / "empty", tmp_path / "out", tests_json)
    assert "No scoring.json" in capsys.readouterr().out
