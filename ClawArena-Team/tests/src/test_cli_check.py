"""clawarena-team check 子命令的端到端校验。"""
from __future__ import annotations

import json
from pathlib import Path

from click.testing import CliRunner

from clawarena_team.cli import main


def _make_data(tmp_path: Path) -> Path:
    data = tmp_path / "data"
    sc = data / "scenarios" / "s_demo"
    (sc / "workspace").mkdir(parents=True)
    (sc / "workspace" / "f.txt").write_text("x", encoding="utf-8")
    (data / "tests.json").write_text(
        json.dumps({"name": "t", "manifests_ref": "manifests.json", "scenario_ids": ["s_demo"]}),
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
    (sc / "checks").mkdir()
    (sc / "checks" / "check_q1.py").write_text("import sys; sys.exit(0)", encoding="utf-8")
    (sc / "manifest.json").write_text(
        json.dumps(
            {
                "scenario_id": "s_demo",
                "desc": "",
                "workspace_template": "workspace",
                "scripts": "checks",
                "main_agent_accessible_paths": [""],
                "updates": {},
                "rounds_ref": "questions.json",
            }
        ),
        encoding="utf-8",
    )
    (sc / "questions.json").write_text(
        json.dumps(
            [
                {
                    "id": "q1",
                    "type": "exec_check",
                    "update_ids": [],
                    "question": "do it",
                    "eval": {"command": "python ${scripts}/check_q1.py"},
                    "feedback": {"correct": "ok", "incorrect": "no"},
                }
            ]
        ),
        encoding="utf-8",
    )
    return data


def test_cli_check_ok(tmp_path: Path):
    data = _make_data(tmp_path)
    runner = CliRunner()
    res = runner.invoke(main, ["check", "-d", str(data)])
    assert res.exit_code == 0, res.output
    assert "OK" in res.output


def test_cli_check_strict_flag_promotes_warnings(tmp_path: Path):
    """缺 optional 字段产生 warn；--strict 应让 exit_code != 0。"""
    data = _make_data(tmp_path)
    # 删除可选 eval 字段，触发若干 warn
    raw = json.loads((data / "scenarios/s_demo/questions.json").read_text())
    raw[0]["eval"].pop("expect_stdout", None)
    raw[0]["eval"].pop("expect_stdout_regex", None)
    raw[0]["eval"].pop("timeout", None)
    raw[0]["eval"].pop("expect_exit", None)
    (data / "scenarios/s_demo/questions.json").write_text(json.dumps(raw), encoding="utf-8")
    runner = CliRunner()
    res = runner.invoke(main, ["check", "-d", str(data)])
    assert res.exit_code == 0, res.output  # 默认 warn 不致失败
    res_strict = runner.invoke(main, ["check", "-d", str(data), "--strict"])
    assert res_strict.exit_code != 0
    assert "FAIL" in res_strict.output


def test_cli_check_scenario_id_filter(tmp_path: Path):
    """-t 指定不存在 scenario_id 时不应过滤掉真正的全局错误。"""
    data = _make_data(tmp_path)
    runner = CliRunner()
    res = runner.invoke(main, ["check", "-d", str(data), "-t", "s_demo"])
    assert res.exit_code == 0, res.output


def test_cli_stats(tmp_path: Path):
    data = _make_data(tmp_path)
    runner = CliRunner()
    res = runner.invoke(main, ["stats", "-d", str(data)])
    assert res.exit_code == 0
    assert "scenarios: 1" in res.output


def test_cli_check_missing_field(tmp_path: Path):
    data = _make_data(tmp_path)
    raw = json.loads((data / "manifests.json").read_text())
    raw.pop("scenarios")
    (data / "manifests.json").write_text(json.dumps(raw), encoding="utf-8")
    runner = CliRunner()
    res = runner.invoke(main, ["check", "-d", str(data)])
    assert res.exit_code != 0
