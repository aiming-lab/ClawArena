"""clawarena-native harness 接入测试（不依赖真实 LLM —— 用 fake provider）。

覆盖：
- provider 名映射；
- data_handler 的 prepare_work_copy / init_session（sessions.json 索引）；
- SessionHistoryStore 跨 session 读取；
- engine.run_agent 端到端（fake provider 直接给最终答案）；
- engine 内 SessionHistory 工具被 agent 调用的链路；
- WorkflowTool 在 native harness 内异步后台执行 + <task-notification> 注入。
"""
from __future__ import annotations

import asyncio
import json
from pathlib import Path

import pytest

import clawarena.native.assembly as assembly
from clawarena.core.provider import ModelConfig
from clawarena.core.types import WorkCopy
from clawarena.data_handlers.clawarena_native.handler import ClawArenaNativeDataHandler
from clawarena.engines.clawarena_native.engine import (
    ClawArenaNativeEngine,
    native_model_json_from_claw,
)
from clawarena.native.agent.session_history import SessionHistoryStore


# ---------------------------------------------------------------------------
# Fake provider：按脚本逐次返回，驱动 agent loop
# ---------------------------------------------------------------------------
class FakeProvider:
    def __init__(self, script):
        # script: list[dict]，每项 {"content":..., "tool_calls":[...]}（无 tool_calls 即终结）
        self._script = list(script)
        self.calls = 0

    async def chat(self, *, messages, tools=None, **kwargs):
        self.calls += 1
        step = self._script.pop(0) if self._script else {"content": "(no more script)"}
        return {
            "content": step.get("content", ""),
            "tool_calls": step.get("tool_calls", []),
            "raw_usage": {},
            "usage_normalized": {},
            "finish_reason": "stop",
        }


def _patch_provider(monkeypatch, script):
    fake = FakeProvider(script)
    monkeypatch.setattr(assembly, "build_provider", lambda cfg: fake)
    return fake


class RuleProvider:
    """基于消息内容决策的 provider（用于并发场景，避免共享脚本乱序）。

    rules: list[(predicate(text)->bool, response_dict)]，按序匹配第一个命中。
    """

    def __init__(self, rules, default):
        self.rules = rules
        self.default = default
        self.calls = 0

    async def chat(self, *, messages, tools=None, **kwargs):
        self.calls += 1
        text = json.dumps(messages, ensure_ascii=False)
        for pred, resp in self.rules:
            if pred(text):
                step = resp
                break
        else:
            step = self.default
        return {
            "content": step.get("content", ""),
            "tool_calls": step.get("tool_calls", []),
            "raw_usage": {},
            "usage_normalized": {},
            "finish_reason": "stop",
        }


def _patch_rule_provider(monkeypatch, rules, default):
    fake = RuleProvider(rules, default)
    monkeypatch.setattr(assembly, "build_provider", lambda cfg: fake)
    return fake


def _write_jsonl(path: Path, rows):
    path.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows), encoding="utf-8"
    )


def _setup_dataset(root: Path) -> dict:
    """造一个最小 clawarena-native 数据集，返回 manifest。"""
    manifest = {
        "agents": {
            "t1": {
                "agent_id": "t1",
                "session": "main_s1",
                "history_sessions": ["hist_wechat"],
                "workspace": "workspaces/t1",
            }
        },
        "state_dir": "state",
        "workspaces_dir": "workspaces",
    }
    (root / "state" / "t1").mkdir(parents=True)
    (root / "workspaces" / "t1").mkdir(parents=True)
    (root / "workspaces" / "t1" / "readme.txt").write_text("hello workspace", encoding="utf-8")
    # 预置历史 session（native 紧凑 jsonl）
    _write_jsonl(
        root / "state" / "t1" / "hist_wechat.jsonl",
        [
            {"role": "system", "content": "sys", "subtype": "prompt"},
            {"role": "user", "content": "客户问：项目什么时候交付？"},
            {"role": "assistant", "content": "我答复：下周五前交付。"},
        ],
    )
    # sessions.json 索引（含历史，标注 channel）
    (root / "state" / "t1" / "sessions.json").write_text(
        json.dumps(
            {
                "hist_wechat": {
                    "session_file": "hist_wechat.jsonl",
                    "channel": "wechat",
                    "is_active": False,
                    "updated_at": 0,
                }
            }
        ),
        encoding="utf-8",
    )
    (root / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    return manifest


# ---------------------------------------------------------------------------
# 单元测试
# ---------------------------------------------------------------------------
def test_provider_mapping():
    assert native_model_json_from_claw(
        ModelConfig(model_id="m", provider="anthropic")
    )["provider"] == "anthropic"
    assert native_model_json_from_claw(
        ModelConfig(model_id="m", provider="google")
    )["provider"] == "gemini"
    assert native_model_json_from_claw(
        ModelConfig(model_id="m", provider="openai")
    )["provider"] == "openai_compat"
    # 未知 provider → openai_compat 兜底
    assert native_model_json_from_claw(
        ModelConfig(model_id="m", provider="something")
    )["provider"] == "openai_compat"


def test_prepare_and_init_session(tmp_path):
    manifest = _setup_dataset(tmp_path)
    h = ClawArenaNativeDataHandler()
    wc = h.prepare_work_copy(manifest, tmp_path, tmp_path)
    assert wc.state_dir.exists() and wc.workspace_root is not None
    sid = h.init_session(wc, "t1")
    assert sid == "main_s1"
    idx = json.loads((wc.state_dir / "t1" / "sessions.json").read_text())
    assert idx["main_s1"]["is_active"] is True
    assert "hist_wechat" in idx  # 历史条目保留
    assert h.resolve_workspace(wc, "t1").name == "t1"


def test_session_history_store(tmp_path):
    manifest = _setup_dataset(tmp_path)
    h = ClawArenaNativeDataHandler()
    wc = h.prepare_work_copy(manifest, tmp_path, tmp_path)
    h.init_session(wc, "t1")
    store = SessionHistoryStore(wc.state_dir / "t1", "main_s1")
    hist = store.list_history()
    assert len(hist) == 1 and hist[0]["session_id"] == "hist_wechat"
    assert hist[0]["channel"] == "wechat" and hist[0]["messages"] == 2
    transcript = store.read_session("hist_wechat")
    assert "下周五前交付" in transcript
    # 越权读取被拒
    assert store.read_session("nonexistent").startswith("forbidden")


def test_engine_end_to_end_plain(monkeypatch, tmp_path):
    manifest = _setup_dataset(tmp_path)
    h = ClawArenaNativeDataHandler()
    wc = h.prepare_work_copy(manifest, tmp_path, tmp_path)
    h.apply_model_config(wc, ModelConfig(model_id="fake", provider="openai", api_base="http://x/v1"))
    sid = h.init_session(wc, "t1")

    _patch_provider(monkeypatch, [{"content": "最终答案：42"}])
    eng = ClawArenaNativeEngine()
    res = asyncio.run(eng.run_agent(sid, "问题？", wc, agent_id="t1", timeout=30))
    assert res.status == "success", res.error
    assert res.answer == "最终答案：42"
    # active session jsonl 已写入
    assert (wc.state_dir / "t1" / "main_s1.jsonl").exists()


def test_engine_uses_session_history_tool(monkeypatch, tmp_path):
    manifest = _setup_dataset(tmp_path)
    h = ClawArenaNativeDataHandler()
    wc = h.prepare_work_copy(manifest, tmp_path, tmp_path)
    h.apply_model_config(wc, ModelConfig(model_id="fake", provider="openai", api_base="http://x/v1"))
    sid = h.init_session(wc, "t1")

    # 第 1 步调 SessionHistory 读历史；第 2 步基于工具结果给最终答案。
    script = [
        {
            "content": "我去看历史",
            "tool_calls": [
                {
                    "id": "c1",
                    "name": "SessionHistory",
                    "arguments": {"action": "read", "session_id": "hist_wechat"},
                }
            ],
        },
        {"content": "历史里说下周五交付"},
    ]
    _patch_provider(monkeypatch, script)
    eng = ClawArenaNativeEngine()
    res = asyncio.run(eng.run_agent(sid, "交付时间？", wc, agent_id="t1", timeout=30))
    assert res.status == "success", res.error
    assert "下周五" in res.answer


def test_engine_no_model_fails(tmp_path):
    manifest = _setup_dataset(tmp_path)
    h = ClawArenaNativeDataHandler()
    wc = h.prepare_work_copy(manifest, tmp_path, tmp_path)
    sid = h.init_session(wc, "t1")  # 未 apply_model_config
    eng = ClawArenaNativeEngine()
    res = asyncio.run(eng.run_agent(sid, "x", wc, agent_id="t1"))
    assert res.status == "failed" and "no model" in (res.error or "")


def test_engine_workflow_background(monkeypatch, tmp_path):
    """main agent 调 Workflow（后台），workflow 脚本里 agent() spawn 一个 subagent。

    fake provider 同时驱动 main 与 subagent 两类 loop：
    - 第 1 次 chat（main）：调 Workflow 工具，脚本里 agent('summarize') 一次；
    - 第 2 次 chat（subagent）：直接给最终文本（subagent loop 终结）；
    - 第 3 次 chat（main）：收到 <task-notification> 后给最终答案。
    """
    manifest = _setup_dataset(tmp_path)
    h = ClawArenaNativeDataHandler()
    wc = h.prepare_work_copy(manifest, tmp_path, tmp_path)
    h.apply_model_config(wc, ModelConfig(model_id="fake", provider="openai", api_base="http://x/v1"))
    sid = h.init_session(wc, "t1")

    wf_script = "const r = await agent('summarize the workspace'); return { r };"
    rules = [
        # subagent loop：其 system prompt 含 "general-purpose subagent"（main 不含）
        (lambda t: "general-purpose subagent" in t,
         {"content": "[subagent] workspace 内有 readme.txt"}),
        # main：已收到后台完成通知 → 给最终答案
        (lambda t: "task-notification" in t,
         {"content": "工作流完成，已汇总"}),
        # main：workflow 已在后台启动但通知未到 → 给个无工具的临时答案，触发等待后台
        (lambda t: "started in background" in t,
         {"content": "等待工作流结果"}),
    ]
    # main 第一步：发起 Workflow 工具
    default = {
        "content": "起一个 workflow",
        "tool_calls": [
            {"id": "w1", "name": "Workflow", "arguments": {"script": wf_script, "name": "demo"}}
        ],
    }
    fake = _patch_rule_provider(monkeypatch, rules, default)
    eng = ClawArenaNativeEngine()
    res = asyncio.run(eng.run_agent(sid, "汇总下工作区", wc, agent_id="t1", timeout=30))
    assert res.status == "success", res.error
    assert res.answer == "工作流完成，已汇总"
    assert fake.calls >= 3  # main + subagent + main
    # 主 session 记录里应出现 <task-notification>
    log_text = (wc.state_dir / "t1" / "main_s1.jsonl").read_text()
    assert "task-notification" in log_text


def test_execute_update_session_workspace_group(tmp_path):
    """execute_update 对齐 openclaw：session new/append + workspace + group 展开。"""
    manifest = _setup_dataset(tmp_path)
    manifest["updates"] = {
        "t1": {
            "u_new": {
                "type": "session",
                "dir": "updates/t1/u_new",
                "files": [{"name": "newchan_email.jsonl", "action": "new"}],
            },
            "u_app": {
                "type": "session",
                "dir": "updates/t1/u_app",
                "files": [{"name": "hist_wechat.jsonl", "action": "append"}],
            },
            "u_ws": {
                "type": "workspace",
                "dir": "updates/t1/u_ws",
                "files": [{"name": "added.txt", "action": "new"}],
            },
            "u_grp": {"type": "group", "children": ["u_new", "u_ws"]},
        }
    }
    (tmp_path / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    # update 源文件
    (tmp_path / "updates" / "t1" / "u_new").mkdir(parents=True)
    _write_jsonl(
        tmp_path / "updates" / "t1" / "u_new" / "newchan_email.jsonl",
        [{"role": "user", "content": "新邮件：请尽快回复"}],
    )
    (tmp_path / "updates" / "t1" / "u_app").mkdir(parents=True)
    _write_jsonl(
        tmp_path / "updates" / "t1" / "u_app" / "hist_wechat.jsonl",
        [{"role": "user", "content": "追加：还有个新问题"}],
    )
    (tmp_path / "updates" / "t1" / "u_ws").mkdir(parents=True)
    (tmp_path / "updates" / "t1" / "u_ws" / "added.txt").write_text("update content", encoding="utf-8")

    h = ClawArenaNativeDataHandler()
    wc = h.prepare_work_copy(manifest, tmp_path, tmp_path)
    sid = h.init_session(wc, "t1")

    # group → 展开 u_new(session) + u_ws(workspace)
    h.execute_update("u_grp", wc, "t1", sid)
    new_sess = wc.state_dir / "t1" / "newchan_email.jsonl"
    assert new_sess.exists()
    idx = json.loads((wc.state_dir / "t1" / "sessions.json").read_text())
    assert "newchan_email" in idx and idx["newchan_email"]["is_active"] is False
    ws_file = h.resolve_workspace(wc, "t1") / "added.txt"
    assert ws_file.exists() and ws_file.read_text() == "update content"

    # append → 历史 session 增长
    before = (wc.state_dir / "t1" / "hist_wechat.jsonl").read_text()
    h.execute_update("u_app", wc, "t1", sid)
    after = (wc.state_dir / "t1" / "hist_wechat.jsonl").read_text()
    assert len(after) > len(before) and "还有个新问题" in after


if __name__ == "__main__":
    import sys

    sys.exit(pytest.main([__file__, "-v"]))
