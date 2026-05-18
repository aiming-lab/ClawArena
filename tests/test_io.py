"""Tests for core I/O utilities."""

import json
import pytest
from pathlib import Path

from clawarena.core.io import apply_overlay, load_json, load_tests_config, load_questions, write_json


def test_load_json(tmp_path):
    f = tmp_path / "test.json"
    f.write_text('{"key": "value"}')
    data = load_json(f)
    assert data == {"key": "value"}


def test_load_tests_config(tmp_path):
    cfg = {"frameworks": {"openclaw": {}}, "tests": [{"id": "t1"}]}
    f = tmp_path / "tests.json"
    f.write_text(json.dumps(cfg))
    data = load_tests_config(f)
    assert "frameworks" in data


def test_load_tests_config_missing_frameworks(tmp_path):
    f = tmp_path / "tests.json"
    f.write_text('{"tests": []}')
    with pytest.raises(ValueError, match="frameworks"):
        load_tests_config(f)


def test_load_questions(tmp_path):
    eval_dir = tmp_path / "eval"
    (eval_dir / "t1").mkdir(parents=True)
    q = {"rounds": [{"id": "r1", "question": "?", "type": "multi_choice"}]}
    (eval_dir / "t1" / "questions.json").write_text(json.dumps(q))
    data = load_questions(eval_dir, "t1")
    assert len(data["rounds"]) == 1


def test_load_questions_missing(tmp_path):
    data = load_questions(tmp_path, "nonexistent")
    assert data["rounds"] == []


def test_write_json(tmp_path):
    p = tmp_path / "sub" / "out.json"
    write_json(p, {"result": 42})
    assert p.exists()
    assert json.loads(p.read_text())["result"] == 42


def test_apply_overlay_merges_metaclaw():
    cfg = {"metaclaw": {"enabled": False, "managed": True}, "tests": [], "frameworks": {}}
    result = apply_overlay(cfg, '{"metaclaw":{"enabled":true}}')
    assert result["metaclaw"] == {"enabled": True, "managed": True}
    assert cfg["metaclaw"] == {"enabled": False, "managed": True}


def test_apply_overlay_rejects_non_metaclaw_key():
    with pytest.raises(ValueError, match="only"):
        apply_overlay({"tests": [], "frameworks": {}}, '{"unknown_overlay":{"enabled":true}}')
