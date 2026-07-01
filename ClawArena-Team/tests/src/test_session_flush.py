"""会话流水落盘：harness 修复——session jsonl 必须同时写到 scenario_out/sessions/
与 work_root/sessions/。

根因：check_*.py 收到的 ${workspace} 是 work_root，它们读 ${workspace}/sessions/main.jsonl；
若只写 scenario_out/sessions/，则所有依赖 session 的检查（委派证据、session 复用、越权扫描）
永远读不到，要么误判失败、要么 warn-only 静默跳过。修复后两处都写。
"""
from __future__ import annotations

from types import SimpleNamespace

from clawarena_team.agent.harness import HarnessTurn
from clawarena_team.runner.scenario_runner import ScenarioRunner


def _runner(tmp_path):
    # 绕开完整构造，仅设置 _flush_sessions 所需属性
    r = ScenarioRunner.__new__(ScenarioRunner)
    r.sessions_dir = tmp_path / "scenario_out" / "sessions"
    r.work_sessions_dir = tmp_path / "scenario_out" / "work" / "sessions"
    r.sessions_dir.mkdir(parents=True, exist_ok=True)
    r.work_sessions_dir.mkdir(parents=True, exist_ok=True)
    return r


def test_flush_writes_main_jsonl_to_both_dirs(tmp_path):
    r = _runner(tmp_path)
    harness = SimpleNamespace(turns=[
        HarnessTurn(role="user", content="hi"),
        HarnessTurn(role="assistant", content="hello"),
    ])
    manager = SimpleNamespace(records={})

    r._flush_sessions(harness, manager)

    canonical = r.sessions_dir / "main.jsonl"
    work_copy = r.work_sessions_dir / "main.jsonl"
    assert canonical.exists(), "规范副本 scenario_out/sessions/main.jsonl 缺失"
    assert work_copy.exists(), "check 读取的 work_root/sessions/main.jsonl 缺失（修复未生效）"
    # 两份都含同样的 turn 内容（meta 行可能带写入时刻，故只比对 turn 负载）
    assert "hello" in work_copy.read_text(encoding="utf-8")


def test_flush_writes_sub_sessions_to_both_dirs(tmp_path):
    r = _runner(tmp_path)
    harness = SimpleNamespace(turns=[HarnessTurn(role="user", content="q")])
    sub_h = SimpleNamespace(turns=[HarnessTurn(role="assistant", content="a")])
    rec = SimpleNamespace(harnesses={"sess_1": sub_h})
    manager = SimpleNamespace(records={"sub_x": rec})

    r._flush_sessions(harness, manager)

    name = "sub_sub_x_sess_1.jsonl"
    assert (r.sessions_dir / name).exists()
    assert (r.work_sessions_dir / name).exists(), "子会话未镜像到 work_root/sessions/"
