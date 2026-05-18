"""Tests for scoring pipeline."""

import json
import pytest
from pathlib import Path

from clawarena.core.scoring import run_scoring


def _create_infer_result(tmp_path, test_id="t1", round_id="r1", answer="\\bbox{A,C}"):
    """Create a minimal infer_result.json and matching questions.json."""
    # Create infer result
    infer_dir = tmp_path / "infer" / test_id / round_id
    infer_dir.mkdir(parents=True)
    result = {
        "meta": {
            "framework": "openclaw",
            "test_id": test_id,
            "round_id": round_id,
            "question_type": "multi_choice",
            "eval_question_path": f"eval/{test_id}/questions.json",
        },
        "answer": {"status": "success", "text": answer},
        "timing": {"duration_ms": 1000},
    }
    (infer_dir / "infer_result.json").write_text(json.dumps(result))

    # Create questions.json reachable from infer_dir
    eval_dir = tmp_path / "eval" / test_id
    eval_dir.mkdir(parents=True)
    q = {"rounds": [{
        "id": round_id,
        "type": "multi_choice",
        "question": "Which?",
        "eval": {"options": {"A": "a", "B": "b", "C": "c"}, "answer": ["A", "C"]},
    }]}
    (eval_dir / "questions.json").write_text(json.dumps(q))

    return tmp_path / "infer"


def test_scoring_correct(tmp_path, capsys):
    infer_dir = _create_infer_result(tmp_path, answer="\\bbox{A,C}")
    run_scoring(infer_dir)
    scoring_path = infer_dir / "t1" / "r1" / "scoring.json"
    assert scoring_path.exists()
    data = json.loads(scoring_path.read_text())
    assert data["score"] == 1.0
    assert data["extracted_answer"] == ["A", "C"]


def test_scoring_wrong(tmp_path):
    infer_dir = _create_infer_result(tmp_path, answer="\\bbox{B}")
    run_scoring(infer_dir)
    data = json.loads((infer_dir / "t1" / "r1" / "scoring.json").read_text())
    assert data["score"] < 1.0


def test_scoring_to_separate_dir(tmp_path):
    infer_dir = _create_infer_result(tmp_path, answer="\\bbox{A,C}")
    out_dir = tmp_path / "scoring_out"
    run_scoring(infer_dir, out_dir)
    assert (out_dir / "t1" / "r1" / "scoring.json").exists()


def test_scoring_no_files(tmp_path, capsys):
    empty = tmp_path / "empty"
    empty.mkdir()
    run_scoring(empty)
    assert "No infer_result.json" in capsys.readouterr().out
