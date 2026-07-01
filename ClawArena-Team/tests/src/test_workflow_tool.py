"""Workflow 工具 / 后台统一 / Bash run_in_background / 结构化输出 / task-notification。"""
from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

import pytest

from clawarena_team.agent.background import BackgroundRegistry
from clawarena_team.agent.harness import AgentHarness, HarnessConfig, _validate_against_schema
from clawarena_team.provider.base import BaseProvider
from clawarena_team.sandbox import AccessibleScope, ReadTracker
from clawarena_team.tools.base import ToolContext
from clawarena_team.tools.basic import BashTool
from clawarena_team.tools.workflow import WorkflowTool


class StubManager:
    def __init__(self):
        self.specs: dict[str, dict] = {}
        self.calls: list[tuple] = []
        self.structured_output_calls = 0

    async def create(self, *, creator_cwd, name, system_prompt, model_key, tools, accessible_paths):
        sid = f"sub_{len(self.specs)}"
        self.specs[sid] = {"name": name}
        return sid

    def find_by_name(self, name):
        return next((sid for sid, s in self.specs.items() if s["name"] == name), None)

    async def invoke(self, *, subagent_id, message, session_id, mode, schema=None, workflow_prompt_suffix=None):
        self.calls.append((subagent_id, message, mode))
        await asyncio.sleep(0)
        return f"[res:{message[:20]}]"


def _ctx(*, manager=None, background=None, cwd: Path, script_dir: Path | None = None) -> ToolContext:
    return ToolContext(
        agent_id="main",
        scope=AccessibleScope([cwd], scenario_root=cwd),
        read_tracker=ReadTracker(),
        cwd=cwd,
        config={"workflow.max_agents": 1000, "workflow.max_concurrency": 8,
                "bash.default_timeout_ms": 120000, "bash.max_output_bytes": 65536},
        subagent_manager=manager,
        background=background,
        workflow_script_dir=script_dir,
    )


# ---------------------------------------------------------------------------
# Workflow 工具
# ---------------------------------------------------------------------------
async def test_workflow_tool_background_and_notification(tmp_path: Path):
    notes: list[str] = []
    reg = BackgroundRegistry(notes.append)
    mgr = StubManager()
    script_dir = tmp_path / "workflows"
    ctx = _ctx(manager=mgr, background=reg, cwd=tmp_path, script_dir=script_dir)
    script = """
    defineAgent({ name: 'w', model_key: 'llm', tools: ['Read'], paths: ['d/'], system_prompt: 's' });
    const out = await parallel([1,2,3].map(i => () => agent('task ' + i, { agentType: 'w' })));
    return { count: out.length };
    """
    tool = WorkflowTool()
    res = await tool.run({"script": script, "name": "demo"}, ctx)
    # 立即返回 task id + 脚本路径
    assert not res.is_error
    assert "task_id=" in res.content
    assert "Script saved to" in res.content
    assert "Workflow" in ctx.tools_used
    # 脚本已落盘
    saved = list(script_dir.glob("workflow_*.js"))
    assert len(saved) == 1
    # 等后台完成 → 收到一条 task-notification 携带 return 值
    await reg.wait_all()
    assert len(notes) == 1
    assert "Workflow run completed" in notes[0]
    assert '"count": 3' in notes[0]
    assert sum(1 for c in mgr.calls if c[2] == "workflow") == 3


async def test_workflow_tool_script_path_reuse(tmp_path: Path):
    notes: list[str] = []
    reg = BackgroundRegistry(notes.append)
    mgr = StubManager()
    script_dir = tmp_path / "workflows"
    ctx = _ctx(manager=mgr, background=reg, cwd=tmp_path, script_dir=script_dir)
    tool = WorkflowTool()
    await tool.run({"script": "return { ok: 1 };", "name": "first"}, ctx)
    await reg.wait_all()
    saved = list(script_dir.glob("workflow_*.js"))[0]
    notes.clear()
    res = await tool.run({"scriptPath": str(saved), "name": "reuse"}, ctx)
    assert not res.is_error
    await reg.wait_all()
    assert any("ok" in n for n in notes)


async def test_workflow_tool_no_background_for_subagent(tmp_path: Path):
    # 无 background 注册表（subagent 上下文）→ Workflow 不可用
    ctx = _ctx(manager=StubManager(), background=None, cwd=tmp_path, script_dir=tmp_path)
    res = await WorkflowTool().run({"script": "return 1;"}, ctx)
    assert res.is_error
    assert "only the main agent" in res.content


async def test_workflow_tool_requires_source(tmp_path: Path):
    reg = BackgroundRegistry(lambda b: None)
    ctx = _ctx(manager=StubManager(), background=reg, cwd=tmp_path, script_dir=tmp_path)
    res = await WorkflowTool().run({}, ctx)
    assert res.is_error


async def test_workflow_default_summary_when_no_return(tmp_path: Path):
    notes: list[str] = []
    reg = BackgroundRegistry(notes.append)
    ctx = _ctx(manager=StubManager(), background=reg, cwd=tmp_path, script_dir=tmp_path / "wf")
    script = "phase('A'); log('did stuff');"
    await WorkflowTool().run({"script": script}, ctx)
    await reg.wait_all()
    assert len(notes) == 1
    assert "phases: A" in notes[0]


# ---------------------------------------------------------------------------
# Bash run_in_background
# ---------------------------------------------------------------------------
async def test_bash_background(tmp_path: Path):
    notes: list[str] = []
    reg = BackgroundRegistry(notes.append)
    ctx = _ctx(background=reg, cwd=tmp_path, script_dir=tmp_path)
    res = await BashTool().run(
        {"command": "echo hi", "description": "echo", "run_in_background": True}, ctx
    )
    assert not res.is_error
    assert "background bash started" in res.content
    assert ctx.bash_mode_counter.get("background") == 1
    await reg.wait_all()
    assert len(notes) == 1
    assert "Background bash command completed" in notes[0]
    assert "hi" in notes[0]


async def test_bash_runtime_default(tmp_path: Path):
    ctx = _ctx(background=None, cwd=tmp_path, script_dir=tmp_path)
    res = await BashTool().run({"command": "echo hi", "description": "echo"}, ctx)
    assert "hi" in res.content
    assert ctx.bash_mode_counter.get("runtime") == 1


async def test_bash_background_falls_back_to_sync_without_registry(tmp_path: Path):
    # subagent 上下文（background=None）：run_in_background 退化为同步执行
    ctx = _ctx(background=None, cwd=tmp_path, script_dir=tmp_path)
    res = await BashTool().run(
        {"command": "echo sync", "description": "echo", "run_in_background": True}, ctx
    )
    assert "sync" in res.content
    assert ctx.bash_mode_counter.get("runtime") == 1


# ---------------------------------------------------------------------------
# 结构化输出（schema 校验 + 重试 + 回退）
# ---------------------------------------------------------------------------
class _ScriptedProvider(BaseProvider):
    name = "scripted"

    def __init__(self, script: list[dict[str, Any]]):
        from clawarena_team.types import ModelConfig
        super().__init__(ModelConfig(provider="scripted", model_id="x"))
        self.script = script
        self.idx = 0

    async def chat(self, *, messages, tools=None, **kw):
        msg = self.script[min(self.idx, len(self.script) - 1)]
        self.idx += 1
        return self.normalise_response(
            content=msg.get("content", ""),
            tool_calls=msg.get("tool_calls") or [],
            raw_usage={"prompt_tokens": 1, "completion_tokens": 1},
            usage_normalized={"input_tokens": 1, "output_tokens": 1, "cache_read_tokens": 0,
                              "cache_write_tokens": 0, "reasoning_tokens": 0, "total_tokens": 2,
                              "provider": "scripted", "raw": {}},
        )


def _harness(provider, tmp_path: Path, stub_tokenizer) -> AgentHarness:
    scope = AccessibleScope([tmp_path], scenario_root=tmp_path)
    return AgentHarness(
        agent_id="sub:1",
        system_prompt="sys",
        provider=provider,
        tools={},
        tool_schemas=[],
        scope=scope,
        read_tracker=ReadTracker(),
        cwd=tmp_path,
        tokenizer=stub_tokenizer,
        cfg=HarnessConfig(token_limit=100000, usage_thresholds_pct=[50],
                          always_hint_on_real_user=False, max_iterations=8),
        config_dict={"structured_output": {"max_retries": 2}},
    )


async def test_structured_output_accepts_valid(tmp_path: Path, stub_tokenizer):
    provider = _ScriptedProvider([
        {"tool_calls": [{"id": "1", "name": "StructuredOutput",
                         "arguments": {"verdict": "real", "score": 3}}]},
    ])
    h = _harness(provider, tmp_path, stub_tokenizer)
    schema = {"type": "object", "required": ["verdict", "score"],
              "properties": {"verdict": {"type": "string"}, "score": {"type": "integer"}}}
    result = await h.send_user("classify", is_real_question=True, schema=schema)
    assert result == {"verdict": "real", "score": 3}


async def test_structured_output_retries_then_succeeds(tmp_path: Path, stub_tokenizer):
    provider = _ScriptedProvider([
        {"content": "here is my answer in prose"},  # 无 StructuredOutput 调用 → 触发重试
        {"tool_calls": [{"id": "2", "name": "StructuredOutput", "arguments": {"verdict": "x"}}]},
    ])
    h = _harness(provider, tmp_path, stub_tokenizer)
    schema = {"type": "object", "required": ["verdict"]}
    result = await h.send_user("classify", is_real_question=True, schema=schema)
    assert result == {"verdict": "x"}


async def test_structured_output_rejects_then_fixes(tmp_path: Path, stub_tokenizer):
    provider = _ScriptedProvider([
        {"tool_calls": [{"id": "1", "name": "StructuredOutput", "arguments": {"wrong": 1}}]},  # 缺 required
        {"tool_calls": [{"id": "2", "name": "StructuredOutput", "arguments": {"verdict": "ok"}}]},
    ])
    h = _harness(provider, tmp_path, stub_tokenizer)
    schema = {"type": "object", "required": ["verdict"]}
    result = await h.send_user("classify", is_real_question=True, schema=schema)
    assert result == {"verdict": "ok"}


async def test_structured_output_fallback_to_text(tmp_path: Path, stub_tokenizer):
    provider = _ScriptedProvider([
        {"content": "prose 1"}, {"content": "prose 2"}, {"content": "prose 3"},
    ])
    h = _harness(provider, tmp_path, stub_tokenizer)
    schema = {"type": "object", "required": ["verdict"]}
    result = await h.send_user("classify", is_real_question=True, schema=schema)
    # 重试耗尽 → 回退返回文本
    assert isinstance(result, str)


def test_runsubagent_schema_param_gated():
    from clawarena_team.tools.subagent import RunSubagentTool
    off = RunSubagentTool.schema()
    assert "schema" not in off["parameters"]["properties"]
    on = RunSubagentTool.schema(structured_output_enabled=True)
    assert "schema" in on["parameters"]["properties"]


def test_validate_against_schema():
    ok, _ = _validate_against_schema({"a": 1}, {"type": "object", "required": ["a"]})
    assert ok
    ok, err = _validate_against_schema({}, {"type": "object", "required": ["a"]})
    assert not ok and "a" in err
    ok, _ = _validate_against_schema(
        {"n": 5}, {"type": "object", "properties": {"n": {"type": "integer"}}}
    )
    assert ok
    ok, _ = _validate_against_schema(
        {"n": "x"}, {"type": "object", "properties": {"n": {"type": "integer"}}}
    )
    assert not ok


# ---------------------------------------------------------------------------
# task-notification 渲染（与 system-reminder 分家）
# ---------------------------------------------------------------------------
async def test_task_notification_rendering(tmp_path: Path, stub_tokenizer):
    provider = _ScriptedProvider([{"content": "done"}])
    h = _harness(provider, tmp_path, stub_tokenizer)
    h.queue_task_notification("background bash done: hi")
    h.queue_system_reminder("token budget at 50%")
    await h.send_user("go", is_real_question=True)
    rendered = "\n".join(_t for t in h.turns for _t in [__import__("clawarena_team.agent.harness", fromlist=["_render_content"])._render_content(t)])
    assert "<task-notification>" in rendered
    assert "background bash done: hi" in rendered
    assert "<system-reminder>" in rendered
