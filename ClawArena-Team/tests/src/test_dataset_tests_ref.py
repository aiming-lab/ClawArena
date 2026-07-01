"""合并数据集的 tests 文件选择：load_dataset(tests_filename=...) 与 CLI --tests。

clawarena-team 把所有场景合并到一个目录，默认全集 tests.json；用户可在同目录另建
tests-*.json 自定义子集，loader 与 run/resume/stats 经 tests_filename / --tests 选中。
"""
from __future__ import annotations

import json
from pathlib import Path

from click.testing import CliRunner

from clawarena_team.cli import main
from clawarena_team.runner.dataset import load_dataset


def _scenario(data: Path, sid: str) -> None:
    sc = data / "scenarios" / sid
    (sc / "workspace").mkdir(parents=True)
    (sc / "workspace" / "f.txt").write_text("x", encoding="utf-8")
    (sc / "checks").mkdir()
    (sc / "checks" / "check_q1.py").write_text("import sys; sys.exit(0)", encoding="utf-8")
    (sc / "manifest.json").write_text(
        json.dumps({
            "scenario_id": sid, "desc": "", "workspace_template": "workspace",
            "scripts": "checks", "main_agent_accessible_paths": [""],
            "updates": {}, "rounds_ref": "questions.json",
        }), encoding="utf-8")
    (sc / "questions.json").write_text(
        json.dumps([{
            "id": "q1", "type": "exec_check", "update_ids": [], "question": "do it",
            "eval": {"command": "python ${scripts}/check_q1.py"},
            "feedback": {"correct": "ok", "incorrect": "no"},
        }]), encoding="utf-8")


def _make_merged(tmp_path: Path) -> Path:
    data = tmp_path / "data"
    (data / "scenarios").mkdir(parents=True)
    for sid in ("s_a", "s_b"):
        _scenario(data, sid)
    (data / "manifests.json").write_text(json.dumps({"scenarios": {
        "s_a": "scenarios/s_a/manifest.json",
        "s_b": "scenarios/s_b/manifest.json",
    }}), encoding="utf-8")
    # 全集 + 子集
    (data / "tests.json").write_text(json.dumps(
        {"name": "all", "manifests_ref": "manifests.json", "scenario_ids": ["s_a", "s_b"]}
    ), encoding="utf-8")
    (data / "tests-sub.json").write_text(json.dumps(
        {"name": "sub", "manifests_ref": "manifests.json", "scenario_ids": ["s_b"]}
    ), encoding="utf-8")
    return data


def test_load_dataset_default_full_set(tmp_path: Path):
    data = _make_merged(tmp_path)
    tests, _, scenarios = load_dataset(data)  # 默认 tests.json
    assert tests.name == "all"
    assert set(scenarios) == {"s_a", "s_b"}


def test_load_dataset_subset_via_tests_filename(tmp_path: Path):
    data = _make_merged(tmp_path)
    tests, _, scenarios = load_dataset(data, tests_filename="tests-sub.json")
    assert tests.name == "sub"
    assert set(scenarios) == {"s_b"}  # 子集只含 s_b


def test_cli_stats_honours_tests_option(tmp_path: Path):
    data = _make_merged(tmp_path)
    runner = CliRunner()
    full = runner.invoke(main, ["stats", "-d", str(data)])
    assert full.exit_code == 0 and "scenarios: 2" in full.output
    sub = runner.invoke(main, ["stats", "-d", str(data), "--tests", "tests-sub.json"])
    assert sub.exit_code == 0 and "scenarios: 1" in sub.output


def test_missing_tests_file_errors(tmp_path: Path):
    data = _make_merged(tmp_path)
    runner = CliRunner()
    res = runner.invoke(main, ["stats", "-d", str(data), "--tests", "tests-nope.json"])
    assert res.exit_code != 0
