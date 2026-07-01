"""AnthropicProvider 的 messages/tools 转换单测。

之前 ``anthropic.py`` 半成品直接透传 OpenAI 风格 messages/tools,Anthropic ``/v1/messages``
以 400 Bad Request 拒绝。本测覆盖 OpenAI → Anthropic 的关键转换:

- ``system`` 拎出顶级;
- ``role: tool`` 转 ``user`` 消息内的 ``tool_result`` block;
- assistant 的 ``tool_calls`` 转 ``tool_use`` block;
- 工具 schema 从 ``parameters`` 转 ``input_schema`` 且强制 ``type:object``;
- 多模态:image_url(data: URI)→ Anthropic ``image`` block;audio/video 跳过。
"""
from __future__ import annotations

import asyncio
import httpx
import pytest

from clawarena_team.provider.anthropic import (
    FABLE_FALLBACK_MODEL,
    AnthropicProvider,
    _convert_user_or_assistant_content,
    _to_anthropic_messages,
    _to_anthropic_tools,
    _wrap_system_with_cache,
)
from clawarena_team.provider.base import NonRetryableProviderError
from clawarena_team.types import ModelConfig


def test_system_extracted_to_top_level():
    sys_text, msgs = _to_anthropic_messages([
        {"role": "system", "content": "you are helpful"},
        {"role": "user", "content": "hi"},
    ])
    assert sys_text == "you are helpful"
    assert msgs == [{"role": "user", "content": "hi"}]


def test_multiple_system_concatenated():
    sys_text, _ = _to_anthropic_messages([
        {"role": "system", "content": "A"},
        {"role": "system", "content": "B"},
        {"role": "user", "content": "hi"},
    ])
    assert sys_text == "A\n\nB"


def test_assistant_tool_calls_to_tool_use_blocks():
    _, msgs = _to_anthropic_messages([
        {"role": "user", "content": "list files"},
        {
            "role": "assistant",
            "content": "let me check",
            "tool_calls": [
                {
                    "id": "call_1",
                    "type": "function",
                    "function": {"name": "ls", "arguments": '{"path": "/tmp"}'},
                }
            ],
        },
    ])
    assert msgs[1]["role"] == "assistant"
    blocks = msgs[1]["content"]
    assert blocks[0] == {"type": "text", "text": "let me check"}
    assert blocks[1] == {
        "type": "tool_use",
        "id": "call_1",
        "name": "ls",
        "input": {"path": "/tmp"},
    }


def test_tool_role_becomes_user_tool_result_block():
    _, msgs = _to_anthropic_messages([
        {"role": "user", "content": "ls"},
        {
            "role": "assistant",
            "content": "",
            "tool_calls": [
                {"id": "c1", "type": "function", "function": {"name": "ls", "arguments": "{}"}}
            ],
        },
        {"role": "tool", "tool_call_id": "c1", "content": "a.txt\nb.txt"},
    ])
    assert msgs[2]["role"] == "user"
    assert msgs[2]["content"] == [
        {"type": "tool_result", "tool_use_id": "c1", "content": "a.txt\nb.txt"}
    ]


def test_multiple_tool_results_merged_into_single_user():
    _, msgs = _to_anthropic_messages([
        {"role": "user", "content": "do two things"},
        {
            "role": "assistant",
            "content": "",
            "tool_calls": [
                {"id": "c1", "type": "function", "function": {"name": "a", "arguments": "{}"}},
                {"id": "c2", "type": "function", "function": {"name": "b", "arguments": "{}"}},
            ],
        },
        {"role": "tool", "tool_call_id": "c1", "content": "r1"},
        {"role": "tool", "tool_call_id": "c2", "content": "r2"},
    ])
    # 两个 tool_result 合并入同一个 user 消息
    assert msgs[2]["role"] == "user"
    assert msgs[2]["content"] == [
        {"type": "tool_result", "tool_use_id": "c1", "content": "r1"},
        {"type": "tool_result", "tool_use_id": "c2", "content": "r2"},
    ]


def test_consecutive_user_messages_merged():
    _, msgs = _to_anthropic_messages([
        {"role": "user", "content": "part 1"},
        {"role": "user", "content": "part 2"},
    ])
    assert len(msgs) == 1
    assert msgs[0]["role"] == "user"
    # 合并为 list 块
    assert msgs[0]["content"] == [
        {"type": "text", "text": "part 1"},
        {"type": "text", "text": "part 2"},
    ]


def test_empty_assistant_gets_placeholder():
    """空 assistant content + 无 tool_calls 不该让 Anthropic 因 content 空而 400。"""
    _, msgs = _to_anthropic_messages([
        {"role": "user", "content": "x"},
        {"role": "assistant", "content": ""},
    ])
    assert msgs[1]["content"] == [{"type": "text", "text": ""}]


def test_leading_assistant_gets_user_placeholder():
    _, msgs = _to_anthropic_messages([
        {"role": "assistant", "content": "stray opener"},
        {"role": "user", "content": "hi"},
    ])
    assert msgs[0]["role"] == "user"


def test_image_data_url_to_anthropic_image_block():
    parts = _convert_user_or_assistant_content([
        {"type": "text", "text": "see image"},
        {
            "type": "image_url",
            "image_url": {"url": "data:image/png;base64,iVBORw0KGgo="},
        },
    ])
    assert parts == [
        {"type": "text", "text": "see image"},
        {
            "type": "image",
            "source": {"type": "base64", "media_type": "image/png", "data": "iVBORw0KGgo="},
        },
    ]


def test_audio_and_video_parts_dropped():
    parts = _convert_user_or_assistant_content([
        {"type": "text", "text": "ok"},
        {"type": "video_url", "video_url": {"url": "data:video/mp4;base64,XXX"}},
        {"type": "input_audio", "input_audio": {"data": "YYY", "format": "wav"}},
    ])
    # Anthropic 不接受 audio/video,只保留 text
    assert parts == [{"type": "text", "text": "ok"}]


def test_tools_converted_with_input_schema():
    out = _to_anthropic_tools([
        {
            "name": "read_file",
            "description": "read a file",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
        }
    ])
    assert out == [
        {
            "name": "read_file",
            "description": "read a file",
            "input_schema": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
        }
    ]


def test_tools_default_input_schema_when_missing_params():
    out = _to_anthropic_tools([{"name": "noop", "description": "no args"}])
    assert out[0]["input_schema"] == {"type": "object", "properties": {}}


def test_tools_missing_type_object_filled_in():
    out = _to_anthropic_tools([
        {"name": "t", "description": "", "parameters": {"properties": {}}}
    ])
    assert out[0]["input_schema"]["type"] == "object"


def test_tools_skip_unnamed():
    out = _to_anthropic_tools([{"description": "x"}])
    assert out == []


# -----------------------------------------------------------------------------
# Prompt cache(5 分钟 ephemeral)启用与关闭
# -----------------------------------------------------------------------------


def test_wrap_system_with_cache_returns_block_list():
    blocks = _wrap_system_with_cache("you are helpful")
    assert blocks == [
        {"type": "text", "text": "you are helpful",
         "cache_control": {"type": "ephemeral"}},
    ]


def test_tools_cache_last_marks_only_last_tool():
    out = _to_anthropic_tools(
        [{"name": "a", "description": ""}, {"name": "b", "description": ""}],
        cache_last=True,
    )
    assert "cache_control" not in out[0]
    assert out[1]["cache_control"] == {"type": "ephemeral"}


def test_tools_cache_last_disabled_no_marks():
    out = _to_anthropic_tools(
        [{"name": "a", "description": ""}, {"name": "b", "description": ""}],
        cache_last=False,
    )
    assert all("cache_control" not in t for t in out)


def test_provider_default_enables_cache():
    cfg = ModelConfig(provider="anthropic", model_id="claude-haiku-4-5", api_key="x")
    p = AnthropicProvider(cfg)
    assert p.prompt_cache_enabled is True


def test_provider_extra_can_disable_cache():
    cfg = ModelConfig(
        provider="anthropic", model_id="claude-haiku-4-5", api_key="x",
        extra={"prompt_cache": False},
    )
    p = AnthropicProvider(cfg)
    assert p.prompt_cache_enabled is False


def test_provider_env_can_disable_cache(monkeypatch):
    monkeypatch.setenv("CATEAM_ANTHROPIC_CACHE", "0")
    cfg = ModelConfig(provider="anthropic", model_id="claude-haiku-4-5", api_key="x")
    p = AnthropicProvider(cfg)
    assert p.prompt_cache_enabled is False


# -----------------------------------------------------------------------------
# Model id 透传(从 response.model 取,缺则回退 config.model_id)
# -----------------------------------------------------------------------------


class _FakeResp:
    def __init__(self, status: int, payload: dict):
        self.status_code = status
        self._payload = payload
        self.headers = {}

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPStatusError("err", request=None, response=self)

    @property
    def text(self):
        return str(self._payload)


def _patch_post(monkeypatch, responses: list):
    """让 httpx.AsyncClient.post 顺序返回 ``responses``;耗尽即 IndexError。"""
    calls: list[dict] = []

    async def fake_post(self, url, *, json=None, headers=None):
        calls.append({"url": url, "json": json})
        return responses[len(calls) - 1]

    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)
    return calls


def test_chat_passes_through_response_model_id(monkeypatch):
    cfg = ModelConfig(provider="anthropic", model_id="claude-sonnet-4-6", api_key="x")
    p = AnthropicProvider(cfg)
    resp = _FakeResp(200, {
        "model": "claude-sonnet-4-6-20251022",
        "content": [{"type": "text", "text": "ok"}],
        "stop_reason": "end_turn",
        "usage": {"input_tokens": 5, "output_tokens": 1},
    })
    _patch_post(monkeypatch, [resp])
    out = asyncio.run(p.chat(messages=[{"role": "user", "content": "hi"}]))
    assert out["model_id"] == "claude-sonnet-4-6-20251022"
    assert out["extra"] == {}


def test_chat_4xx_raises_non_retryable(monkeypatch):
    cfg = ModelConfig(provider="anthropic", model_id="claude-sonnet-4-6", api_key="x")
    p = AnthropicProvider(cfg)
    bad = _FakeResp(400, {"error": "invalid request"})
    _patch_post(monkeypatch, [bad])
    with pytest.raises(NonRetryableProviderError):
        asyncio.run(p.chat(messages=[{"role": "user", "content": "hi"}]))


# -----------------------------------------------------------------------------
# Fable refusal → opus-4-8 fallback
# -----------------------------------------------------------------------------


def test_fable_refusal_triggers_opus_fallback(monkeypatch):
    cfg = ModelConfig(provider="anthropic", model_id="claude-fable-5", api_key="x")
    p = AnthropicProvider(cfg)
    refused = _FakeResp(200, {
        "model": "claude-fable-5",
        "content": [],
        "stop_reason": "refusal",
        "usage": {"input_tokens": 5, "output_tokens": 0},
    })
    ok = _FakeResp(200, {
        "model": "claude-opus-4-8",
        "content": [{"type": "text", "text": "ok"}],
        "stop_reason": "end_turn",
        "usage": {"input_tokens": 5, "output_tokens": 2},
    })
    calls = _patch_post(monkeypatch, [refused, ok])
    out = asyncio.run(p.chat(messages=[{"role": "user", "content": "hi"}]))
    # 第 2 次请求 model 被改成 opus-4-8
    assert calls[0]["json"]["model"] == "claude-fable-5"
    assert calls[1]["json"]["model"] == FABLE_FALLBACK_MODEL
    # extra 标记被附上
    assert out["extra"]["fable_refusal_fallback"] is True
    assert out["extra"]["fallback_from_model"] == "claude-fable-5"
    assert out["extra"]["fallback_model"] == FABLE_FALLBACK_MODEL
    assert "fable" in out["extra"]["note"]
    # model_id 反映最终成功的 model
    assert out["model_id"] == FABLE_FALLBACK_MODEL


def test_fable_substring_also_triggers_fallback(monkeypatch):
    """``fable`` 子串匹配(忽略大小写),不限于精确 claude-fable-5。"""
    cfg = ModelConfig(provider="anthropic", model_id="custom-Fable-preview", api_key="x")
    p = AnthropicProvider(cfg)
    refused = _FakeResp(200, {
        "model": "custom-Fable-preview",
        "content": [],
        "stop_reason": "refusal",
        "usage": {"input_tokens": 5, "output_tokens": 0},
    })
    ok = _FakeResp(200, {
        "model": FABLE_FALLBACK_MODEL,
        "content": [{"type": "text", "text": "ok"}],
        "stop_reason": "end_turn",
        "usage": {"input_tokens": 5, "output_tokens": 2},
    })
    _patch_post(monkeypatch, [refused, ok])
    out = asyncio.run(p.chat(messages=[{"role": "user", "content": "hi"}]))
    assert out["extra"]["fable_refusal_fallback"] is True


def test_non_fable_refusal_does_not_fallback(monkeypatch):
    """非 fable 模型 refusal 不触发兜底,extra 保持空。"""
    cfg = ModelConfig(provider="anthropic", model_id="claude-sonnet-4-6", api_key="x")
    p = AnthropicProvider(cfg)
    refused = _FakeResp(200, {
        "model": "claude-sonnet-4-6",
        "content": [],
        "stop_reason": "refusal",
        "usage": {"input_tokens": 5, "output_tokens": 0},
    })
    calls = _patch_post(monkeypatch, [refused])
    out = asyncio.run(p.chat(messages=[{"role": "user", "content": "hi"}]))
    assert len(calls) == 1  # 没二次请求
    assert out["extra"] == {}


def test_fable_non_refusal_does_not_fallback(monkeypatch):
    """fable 模型但非 refusal 直接返回,不二次请求。"""
    cfg = ModelConfig(provider="anthropic", model_id="claude-fable-5", api_key="x")
    p = AnthropicProvider(cfg)
    ok = _FakeResp(200, {
        "model": "claude-fable-5",
        "content": [{"type": "text", "text": "ok"}],
        "stop_reason": "end_turn",
        "usage": {"input_tokens": 5, "output_tokens": 2},
    })
    calls = _patch_post(monkeypatch, [ok])
    out = asyncio.run(p.chat(messages=[{"role": "user", "content": "hi"}]))
    assert len(calls) == 1
    assert out["extra"] == {}


# -----------------------------------------------------------------------------
# 共享总时限 deadline:原 POST 与 fable refusal 回退 POST 不得各自独占预算
# -----------------------------------------------------------------------------


def test_fable_fallback_shares_total_deadline(monkeypatch):
    """fable 回退的两次 POST 必须共享同一 deadline。

    Why: ``CATEAM_PROVIDER_TOTAL_TIMEOUT_SEC=480`` 是单 turn 总时限;若两次
    POST 各自起一份新预算,实际单 turn 可耗 ~960s → 高拒答场景几个 turn 即可
    撑爆 SCENARIO_TIMEOUT_SEC=2400 墙钟(s_security_pcap_triage 实测教训)。
    """
    monkeypatch.setenv("CATEAM_PROVIDER_TOTAL_TIMEOUT_SEC", "480")
    cfg = ModelConfig(provider="anthropic", model_id="claude-fable-5", api_key="x")
    p = AnthropicProvider(cfg)

    refused = {
        "model": "claude-fable-5",
        "content": [],
        "stop_reason": "refusal",
        "usage": {"input_tokens": 5, "output_tokens": 0},
    }
    ok = {
        "model": FABLE_FALLBACK_MODEL,
        "content": [{"type": "text", "text": "ok"}],
        "stop_reason": "end_turn",
        "usage": {"input_tokens": 5, "output_tokens": 2},
    }

    captured: list[float | None] = []

    async def spy_post(payload, *, deadline=None):
        captured.append(deadline)
        return refused if len(captured) == 1 else ok

    monkeypatch.setattr(p, "_post_messages", spy_post)
    asyncio.run(p.chat(messages=[{"role": "user", "content": "hi"}]))

    assert len(captured) == 2
    assert captured[0] is not None and captured[1] is not None
    # 两次 POST 收到同一 deadline 值;若 chat 各自起新预算,这里会差好几百秒。
    assert captured[0] == captured[1]


def test_chat_without_total_timeout_passes_none_deadline(monkeypatch):
    """未设 CATEAM_PROVIDER_TOTAL_TIMEOUT_SEC 时 chat 必须传 deadline=None。

    保证向后兼容:旧场景无 env 时不应被强加任何时限。
    """
    monkeypatch.delenv("CATEAM_PROVIDER_TOTAL_TIMEOUT_SEC", raising=False)
    cfg = ModelConfig(provider="anthropic", model_id="claude-sonnet-4-6", api_key="x")
    p = AnthropicProvider(cfg)
    ok = {
        "model": "claude-sonnet-4-6",
        "content": [{"type": "text", "text": "ok"}],
        "stop_reason": "end_turn",
        "usage": {"input_tokens": 5, "output_tokens": 2},
    }
    captured: list[float | None] = []

    async def spy_post(payload, *, deadline=None):
        captured.append(deadline)
        return ok

    monkeypatch.setattr(p, "_post_messages", spy_post)
    asyncio.run(p.chat(messages=[{"role": "user", "content": "hi"}]))
    assert captured == [None]


def test_post_messages_deadline_zero_remaining_raises(monkeypatch):
    """deadline 已过(剩余 ≤ 0)再起 attempt 直接 TimeoutError,不无谓发包。"""
    import time as _time

    cfg = ModelConfig(provider="anthropic", model_id="claude-sonnet-4-6", api_key="x")
    p = AnthropicProvider(cfg)
    posted = []

    async def fake_post(self, url, *, json=None, headers=None):  # noqa: ARG001
        posted.append(url)
        return _FakeResp(200, {})

    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)
    expired = _time.time() - 1.0
    with pytest.raises(Exception):  # ProviderError 包裹的 TimeoutError
        asyncio.run(p._post_messages({"x": 1}, deadline=expired))
    assert posted == []  # deadline 过期前未真正发包
