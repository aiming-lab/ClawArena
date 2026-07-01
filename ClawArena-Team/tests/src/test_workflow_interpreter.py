"""Workflow JS-DSL 解释器与原语（agent/parallel/pipeline/defineAgent/...）。

解释器是与 SMbench 解耦的纯执行引擎；这里用一个记录调用的 StubManager 验证：
受限 JS 子集的求值正确性、并发原语、defineAgent↔agent 共享池、invocation=workflow。
"""
from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from clawarena_team.tools.workflow.interpreter import Interpreter, UNDEFINED
from clawarena_team.tools.workflow.runtime import WorkflowRuntime
from clawarena_team.tools.workflow.errors import WorkflowScriptError


class StubManager:
    def __init__(self):
        self.specs: dict[str, dict] = {}
        self.calls: list[tuple] = []
        self.structured_output_calls = 0

    async def create(self, *, creator_cwd, name, system_prompt, model_key, tools, accessible_paths):
        sid = f"sub_{len(self.specs)}"
        self.specs[sid] = {
            "name": name, "model_key": model_key, "tools": tools,
            "paths": accessible_paths, "system_prompt": system_prompt,
        }
        return sid

    def find_by_name(self, name):
        match = None
        for sid, s in self.specs.items():
            if s["name"] == name:
                match = sid
        return match

    async def invoke(self, *, subagent_id, message, session_id, mode, schema=None, workflow_prompt_suffix=None):
        self.calls.append((subagent_id, message, mode, schema is not None, workflow_prompt_suffix))
        if schema is not None:
            self.structured_output_calls += 1
        await asyncio.sleep(0)
        if schema is not None:
            return {"ok": True, "msg": message[:20]}
        return f"[result: {message[:40]}]"


async def _run(src, args=None, *, mgr=None, max_concurrency=4):
    mgr = mgr or StubManager()
    rt = WorkflowRuntime(manager=mgr, creator_cwd=Path("/tmp"), max_concurrency=max_concurrency)
    interp = Interpreter(rt.builtins())
    rt.bind_interpreter(interp)
    result = await interp.run(src, {"args": args if args is not None else UNDEFINED})
    return result, mgr, rt


async def test_basic_control_flow_and_array_methods():
    src = """
    const xs = args.xs;
    let total = 0;
    for (const x of xs) { total += x; }
    const doubled = xs.map(v => v * 2).filter(v => v > 2);
    const joined = ['a', 'b', 'c'].join('-');
    return { total, doubled, joined, n: xs.length, up: 'hi'.toUpperCase() };
    """
    result, _mgr, _rt = await _run(src, {"xs": [1, 2, 3]})
    assert result["total"] == 6
    assert result["doubled"] == [4, 6]
    assert result["joined"] == "a-b-c"
    assert result["n"] == 3
    assert result["up"] == "HI"


async def test_define_agent_then_agent_runs_via_pool():
    src = """
    defineAgent({ name: 'reader', model_key: 'llm', tools: ['Read'], paths: ['docs/'], system_prompt: 'r' });
    const r = await agent('read the file', { agentType: 'reader' });
    return { r };
    """
    result, mgr, _rt = await _run(src)
    assert "reader" in [s["name"] for s in mgr.specs.values()]
    assert result["r"].startswith("[result:")
    # 单次 agent 调用，mode=workflow，带 workflow system 后缀
    assert len(mgr.calls) == 1
    assert mgr.calls[0][2] == "workflow"
    assert mgr.calls[0][4] is not None  # workflow_prompt_suffix


async def test_agent_requires_known_agent_type():
    src = "const r = await agent('x', { agentType: 'ghost' }); return r;"
    with pytest.raises(WorkflowScriptError):
        await _run(src)
    src2 = "const r = await agent('x', {}); return r;"
    with pytest.raises(WorkflowScriptError):
        await _run(src2)


async def test_agent_shares_pool_with_precreated_subagent():
    """模拟「CreateSubagent 先建，Workflow 直接用」：预先在 manager 里建好 spec。"""
    mgr = StubManager()
    await mgr.create(
        creator_cwd=Path("/tmp"), name="explorer", system_prompt="e",
        model_key="llm", tools=["Read"], accessible_paths=["src/"],
    )
    src = "const r = await agent('explore', { agentType: 'explorer' }); return r;"
    result, mgr2, _ = await _run(src, mgr=mgr)
    assert result["r"] if isinstance(result, dict) else result  # truthy
    assert mgr.calls and mgr.calls[0][2] == "workflow"


async def test_parallel_runs_all_thunks():
    src = """
    defineAgent({ name: 'w', model_key: 'llm', tools: ['Read'], paths: ['d/'], system_prompt: 's' });
    const items = args.items;
    const out = await parallel(items.map(it => () => agent('do ' + it, { agentType: 'w' })));
    return { count: out.length };
    """
    result, mgr, _rt = await _run(src, {"items": ["a", "b", "c", "d"]})
    assert result["count"] == 4
    assert sum(1 for c in mgr.calls if c[2] == "workflow") == 4


async def test_pipeline_stages_per_item():
    src = """
    defineAgent({ name: 'w', model_key: 'llm', tools: ['Read'], paths: ['d/'], system_prompt: 's' });
    const out = await pipeline(args.items,
      d => agent('stage1 ' + d, { agentType: 'w' }),
      r => ({ wrapped: r })
    );
    return { out };
    """
    result, mgr, _rt = await _run(src, {"items": ["x", "y"]})
    assert len(result["out"]) == 2
    assert all("wrapped" in o for o in result["out"])


async def test_structured_schema_threads_through():
    src = """
    defineAgent({ name: 'w', model_key: 'llm', tools: ['Read'], paths: ['d/'], system_prompt: 's' });
    const r = await agent('give json', { agentType: 'w', schema: { type: 'object', required: ['ok'] } });
    return r;
    """
    result, mgr, _rt = await _run(src)
    assert result == {"ok": True, "msg": "give json"}
    assert mgr.structured_output_calls == 1


async def test_phase_and_log_recorded_for_default_summary():
    src = """
    phase('Scan');
    log('hello');
    log('world');
    """
    _result, _mgr, rt = await _run(src)
    assert rt.phases == ["Scan"]
    assert rt.logs == ["hello", "world"]
    summary = rt.default_summary()
    assert "phases: Scan" in summary
    assert "hello" in summary


async def test_max_agents_cap():
    mgr = StubManager()
    rt = WorkflowRuntime(manager=mgr, creator_cwd=Path("/tmp"), max_agents=2, max_concurrency=2)
    interp = Interpreter(rt.builtins())
    rt.bind_interpreter(interp)
    src = """
    defineAgent({ name: 'w', model_key: 'llm', tools: ['Read'], paths: ['d/'], system_prompt: 's' });
    for (const i of [1,2,3,4]) { await agent('x' + i, { agentType: 'w' }); }
    """
    with pytest.raises(WorkflowScriptError):
        await interp.run(src, {"args": UNDEFINED})


async def test_unsupported_syntax_raises():
    # class 声明不在支持子集内
    with pytest.raises(WorkflowScriptError):
        await _run("class Foo {}")
