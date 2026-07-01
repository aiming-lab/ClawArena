"""使用 stub provider 验证 agent loop 行为：tool 调用 → tool_result → 终止。"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from clawarena_team.agent.harness import AgentHarness, HarnessConfig
from clawarena_team.provider.base import BaseProvider
from clawarena_team.sandbox import AccessibleScope, ReadTracker
from clawarena_team.tools.basic import ReadTool


class _ScriptedProvider(BaseProvider):
    name = "scripted"

    def __init__(self, script: list[dict[str, Any]]):
        from clawarena_team.types import ModelConfig
        super().__init__(ModelConfig(provider="scripted", model_id="x"))
        self.script = script
        self.idx = 0

    async def chat(self, *, messages, tools=None, **kw):
        msg = self.script[self.idx]
        self.idx += 1
        return self.normalise_response(
            content=msg.get("content", ""),
            tool_calls=msg.get("tool_calls") or [],
            raw_usage={"prompt_tokens": 1, "completion_tokens": 1},
            usage_normalized={
                "input_tokens": 1,
                "output_tokens": 1,
                "cache_read_tokens": 0,
                "cache_write_tokens": 0,
                "reasoning_tokens": 0,
                "total_tokens": 2,
                "provider": "scripted",
                "raw": {"prompt_tokens": 1, "completion_tokens": 1},
            },
        )


async def test_agent_loop_one_tool_call(tmp_workspace: Path, stub_tokenizer):
    scope = AccessibleScope([tmp_workspace / "inbox"], scenario_root=tmp_workspace)
    abs_path = str(tmp_workspace / "inbox" / "hello.txt")
    provider = _ScriptedProvider(
        [
            {
                "tool_calls": [
                    {"id": "1", "name": "Read", "arguments": {"file_path": abs_path}}
                ]
            },
            {"content": "done"},
        ]
    )
    harness = AgentHarness(
        agent_id="main",
        system_prompt="sys",
        provider=provider,
        tools={"Read": ReadTool()},
        tool_schemas=[ReadTool.schema(modalities=["text"])],
        scope=scope,
        read_tracker=ReadTracker(),
        cwd=tmp_workspace / "inbox",
        tokenizer=stub_tokenizer,
        cfg=HarnessConfig(token_limit=10_000, usage_thresholds_pct=[50], always_hint_on_real_user=True, max_iterations=5),
        config_dict={},
    )
    ans = await harness.send_user("read hello", is_real_question=True)
    assert ans == "done"
    assert "Read" in harness.tools_used


async def test_token_limit_exceeded(tmp_workspace: Path, stub_tokenizer):
    scope = AccessibleScope([tmp_workspace / "inbox"], scenario_root=tmp_workspace)
    provider = _ScriptedProvider([{"content": "x" * 4000}])
    harness = AgentHarness(
        agent_id="main",
        system_prompt="sys",
        provider=provider,
        tools={"Read": ReadTool()},
        tool_schemas=[ReadTool.schema(modalities=["text"])],
        scope=scope,
        read_tracker=ReadTracker(),
        cwd=tmp_workspace / "inbox",
        tokenizer=stub_tokenizer,
        cfg=HarnessConfig(token_limit=10, usage_thresholds_pct=[50], always_hint_on_real_user=False, max_iterations=5),
        config_dict={},
    )
    from clawarena_team.agent import TokenLimitExceeded
    with pytest.raises(TokenLimitExceeded):
        await harness.send_user("hello", is_real_question=True)


async def test_three_segment_accounting(tmp_workspace: Path, stub_tokenizer):
    """三段 token 累计语义：每次 assistant turn 对应一次模型调用。

    校验项：
    - context_size_max 单调递增至最终 context 总长；
    - 第一次调用 cache_read=0；
    - 后续调用 cache_read = 上一次 post_call 的 context size；
    - input/output/cache_read 累加值 = 各 turn delta 之和。
    """
    scope = AccessibleScope([tmp_workspace / "inbox"], scenario_root=tmp_workspace)
    abs_path = str(tmp_workspace / "inbox" / "hello.txt")
    # 让模型先发 1 个工具调用、然后给出最终回答（共 2 次模型调用）
    provider = _ScriptedProvider(
        [
            {"tool_calls": [{"id": "1", "name": "Read", "arguments": {"file_path": abs_path}}]},
            {"content": "done"},
        ]
    )
    harness = AgentHarness(
        agent_id="main",
        system_prompt="sys",
        provider=provider,
        tools={"Read": ReadTool()},
        tool_schemas=[ReadTool.schema(modalities=["text"])],
        scope=scope,
        read_tracker=ReadTracker(),
        cwd=tmp_workspace / "inbox",
        tokenizer=stub_tokenizer,
        cfg=HarnessConfig(token_limit=10_000, usage_thresholds_pct=[50], always_hint_on_real_user=False, max_iterations=5),
        config_dict={},
    )
    await harness.send_user("read hello", is_real_question=True)

    assistant_turns = [t for t in harness.turns if t.role == "assistant"]
    assert len(assistant_turns) == 2

    # 第一次调用：cache_read 必须为 0；input 等于此时 context 总长 - output
    a0, a1 = assistant_turns
    assert a0.cache_read_delta == 0
    assert a0.input_delta > 0
    assert a0.output_delta >= 0

    # 第二次调用：cache_read 应等于 a0 加完后的 context size（= a0.context_size_after）
    assert a1.cache_read_delta == a0.context_size_after

    # 总累计 = 各 turn delta 之和
    assert harness.input_token_total == a0.input_delta + a1.input_delta
    assert harness.output_token_total == a0.output_delta + a1.output_delta
    assert harness.cache_read_total == a0.cache_read_delta + a1.cache_read_delta

    # context_size_max 应等于最后一 turn 的 context_size_after
    assert harness.context_size_max == harness.turns[-1].context_size_after
