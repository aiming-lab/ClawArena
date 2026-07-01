from __future__ import annotations

from pathlib import Path

from clawarena_team.runner.scenario_runner import _format_command
from clawarena_team.scoring import run_exec_check


def test_exec_check_pass(tmp_path: Path):
    result = run_exec_check(command="true", cwd=tmp_path)
    assert result["passed"]
    assert result["exit_code"] == 0


def test_exec_check_fail(tmp_path: Path):
    result = run_exec_check(command="false", cwd=tmp_path)
    assert not result["passed"]
    assert result["exit_code"] == 1


def test_exec_check_stdout_match(tmp_path: Path):
    result = run_exec_check(command="echo hello", cwd=tmp_path, expect_stdout="hel")
    assert result["passed"]


def test_exec_check_regex(tmp_path: Path):
    result = run_exec_check(command="echo 42", cwd=tmp_path, expect_stdout=r"\d+", regex=True)
    assert result["passed"]


def test_exec_check_timeout(tmp_path: Path):
    result = run_exec_check(command="sleep 2", cwd=tmp_path, timeout=1)
    assert not result["passed"]
    assert "TIMEOUT" in result["stderr"]


def test_format_command_substitutes_known_placeholders():
    cmd = _format_command(
        "python ${scripts}/check_q1.py ${workspace}",
        {
            "workspace": "/tmp/run/work",
            "scripts": "/data/sc/checks",
            "scenario_dir": "/data/sc",
            "scenario_id": "s_demo",
        },
    )
    assert cmd == "python /data/sc/checks/check_q1.py /tmp/run/work"


def test_format_command_quotes_paths_with_spaces():
    cmd = _format_command(
        "python ${scripts}/check.py ${workspace}",
        {"workspace": "/tmp/run a/work", "scripts": "/d/has space/checks"},
    )
    # shlex.quote 包裹含空格的路径
    assert "'/tmp/run a/work'" in cmd
    assert "'/d/has space/checks'" in cmd


def test_format_command_leaves_unknown_placeholders_as_is():
    cmd = _format_command(
        "echo ${HOME} ${workspace}",
        {"workspace": "/tmp/w"},
    )
    assert cmd == "echo ${HOME} /tmp/w"
