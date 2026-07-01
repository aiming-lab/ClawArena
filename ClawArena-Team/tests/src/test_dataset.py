from __future__ import annotations

import json
from pathlib import Path

import pytest

from clawarena_team.runner import load_dataset, validate_dataset


def _make_dataset(tmp_path: Path) -> Path:
    data = tmp_path / "data"
    sc_dir = data / "scenarios" / "s_demo"
    (sc_dir / "workspace" / "inbox").mkdir(parents=True)
    (sc_dir / "workspace" / "inbox" / "task.md").write_text("hi", encoding="utf-8")
    (sc_dir / "updates" / "u1").mkdir(parents=True)
    (sc_dir / "updates" / "u1" / "memo.md").write_text("memo", encoding="utf-8")
    (sc_dir / "checks").mkdir()
    (sc_dir / "checks" / "check_q1.sh").write_text("#!/bin/sh\nexit 0", encoding="utf-8")
    (sc_dir / "checks" / "check_q1.py").write_text("import sys; sys.exit(0)", encoding="utf-8")

    (data / "tests.json").write_text(
        json.dumps(
            {
                "name": "demo",
                "desc": "demo set",
                "manifests_ref": "manifests.json",
                "scenario_ids": ["s_demo"],
                "extra_meta": "ok",
            }
        ),
        encoding="utf-8",
    )
    (data / "manifests.json").write_text(
        json.dumps(
            {
                "scenarios": {"s_demo": "scenarios/s_demo/manifest.json"},
            }
        ),
        encoding="utf-8",
    )
    (sc_dir / "manifest.json").write_text(
        json.dumps(
            {
                "scenario_id": "s_demo",
                "desc": "demo",
                "workspace_template": "workspace",
                "scripts": "checks",
                "main_agent_accessible_paths": ["inbox"],
                "updates": {
                    "u1": {"op": "new", "files": [{"src": "updates/u1/memo.md", "dst": "inbox/memo.md"}]}
                },
                "rounds_ref": "questions.json",
            }
        ),
        encoding="utf-8",
    )
    (sc_dir / "questions.json").write_text(
        json.dumps(
            [
                {
                    "id": "q1",
                    "type": "exec_check",
                    "update_ids": [],
                    "question": "do nothing",
                    "eval": {
                        "command": "python ${scripts}/check_q1.py",
                        "expect_exit": 0,
                        "timeout": 5,
                        "expect_stdout": None,
                        "expect_stdout_regex": False,
                    },
                    "feedback": {"correct": "good", "incorrect": "bad"},
                }
            ]
        ),
        encoding="utf-8",
    )
    return data


def test_load_dataset_resolves_paths(tmp_path: Path):
    data = _make_dataset(tmp_path)
    tests, manifests, scenarios = load_dataset(data)
    sc = scenarios["s_demo"]
    assert sc.workspace_template.is_absolute()
    assert sc.workspace_template.exists()
    assert sc.rounds[0].id == "q1"
    assert sc.updates["u1"].op == "new"


def test_tests_json_extra_field_allowed(tmp_path: Path):
    data = _make_dataset(tmp_path)
    tests, _, _ = load_dataset(data)
    assert tests.extras.get("extra_meta") == "ok"


def test_validate_dataset_ok(tmp_path: Path):
    data = _make_dataset(tmp_path)
    report = validate_dataset(data)
    assert report.ok, report.errors


def test_manifests_extra_key_rejected(tmp_path: Path):
    data = _make_dataset(tmp_path)
    raw = json.loads((data / "manifests.json").read_text())
    raw["surprise"] = 1
    (data / "manifests.json").write_text(json.dumps(raw), encoding="utf-8")
    report = validate_dataset(data)
    assert not report.ok


def test_questions_must_be_list(tmp_path: Path):
    data = _make_dataset(tmp_path)
    (data / "scenarios" / "s_demo" / "questions.json").write_text(
        json.dumps({"rounds": []}), encoding="utf-8"
    )
    report = validate_dataset(data)
    assert not report.ok
