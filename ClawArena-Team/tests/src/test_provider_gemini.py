"""GeminiProvider 的工具 schema 净化与 Gemini 3 thought_signature 透传单测。

两者均为接入真实 Gemini(尤其 gemini-3.x)所必需:
- ``additionalProperties`` 等 JSON-Schema 键会被 Gemini functionDeclarations 以 400
  INVALID_ARGUMENT 拒绝,须递归剔除;
- Gemini 3 要求回放历史 functionCall 时带回原 ``thoughtSignature``,否则 400
  "Function call is missing a thought_signature"。provider 以实例内 ``{id: sig}`` 映射
  跨轮记录并重注入。
"""
from __future__ import annotations

import asyncio

import httpx

from clawarena_team.provider.gemini import (
    GeminiProvider,
    _sanitize_gemini_schema,
    _to_gemini_messages,
    _to_gemini_tools,
)
from clawarena_team.types import ModelConfig


def _cfg() -> ModelConfig:
    return ModelConfig(provider="gemini", model_id="gemini-3.5-flash", api_key="x")


def test_sanitize_strips_unsupported_keys():
    schema = {
        "type": "object",
        "additionalProperties": False,
        "$schema": "http://json-schema.org/draft-07/schema#",
        "properties": {
            "path": {"type": "string", "default": "a", "description": "p"},
            "n": {"type": "integer", "exclusiveMinimum": 0},
        },
        "required": ["path"],
    }
    out = _sanitize_gemini_schema(schema)
    assert "additionalProperties" not in out
    assert "$schema" not in out
    # 嵌套属性内的非白名单键也被剔除
    assert "default" not in out["properties"]["path"]
    assert "exclusiveMinimum" not in out["properties"]["n"]
    # 白名单键保留
    assert out["properties"]["path"]["description"] == "p"
    assert out["required"] == ["path"]


def test_to_gemini_tools_sanitizes():
    tools = [{"name": "read", "description": "r",
              "parameters": {"type": "object", "additionalProperties": False,
                             "properties": {"p": {"type": "string"}}}}]
    decls = _to_gemini_tools(tools)
    params = decls[0]["functionDeclarations"][0]["parameters"]
    assert "additionalProperties" not in params
    assert params["properties"]["p"]["type"] == "string"


def test_thought_signature_replayed_on_history():
    sig_by_id = {"gm_0": "SIG_ABC"}
    messages = [
        {"role": "user", "content": "go"},
        {"role": "assistant", "content": "",
         "tool_calls": [{"id": "gm_0", "function": {"name": "read", "arguments": "{}"}}]},
        {"role": "tool", "tool_call_id": "gm_0", "content": "result"},
    ]
    _sys, contents = _to_gemini_messages(messages, sig_by_id)
    model_turn = next(c for c in contents if c["role"] == "model")
    fc_part = next(p for p in model_turn["parts"] if "functionCall" in p)
    assert fc_part["thoughtSignature"] == "SIG_ABC"


def test_thought_signature_absent_when_unknown():
    messages = [
        {"role": "assistant", "content": "",
         "tool_calls": [{"id": "gm_9", "function": {"name": "read", "arguments": "{}"}}]},
    ]
    _sys, contents = _to_gemini_messages(messages, {})
    fc_part = next(p for p in contents[0]["parts"] if "functionCall" in p)
    assert "thoughtSignature" not in fc_part


def test_provider_instance_has_sig_map():
    p = GeminiProvider(_cfg())
    assert p._sig_by_id == {}
    assert p._call_seq == 0


def _capture_payload(monkeypatch, provider: GeminiProvider) -> dict:
    """跑一次 chat() 但拦截 HTTP,返回实际发出的 JSON payload。"""
    captured: dict = {}

    class _Resp:
        def raise_for_status(self):  # noqa: D401
            return None

        def json(self):
            return {"candidates": [{"content": {"parts": [{"text": "ok"}]},
                                    "finishReason": "STOP"}]}

    async def _fake_post(self, url, json=None, headers=None):  # noqa: A002
        captured.update(json or {})
        return _Resp()

    monkeypatch.setattr(httpx.AsyncClient, "post", _fake_post)
    asyncio.run(provider.chat(messages=[{"role": "user", "content": "hi"}], tools=[]))
    return captured


def test_extra_max_tokens_routed_to_generation_config(monkeypatch):
    """target 配置里的 max_tokens(经 config.extra)须翻译为 generationConfig
    .maxOutputTokens,而非原样塞进顶层 payload —— 否则 Gemini 原生 API 以
    400 "Unknown name max_tokens" 拒绝。"""
    cfg = ModelConfig(provider="gemini", model_id="gemini-3.1-pro-preview",
                      api_key="x", extra={"max_tokens": 24000})
    payload = _capture_payload(monkeypatch, GeminiProvider(cfg))
    assert "max_tokens" not in payload  # 不得泄漏到顶层
    assert payload["generationConfig"]["maxOutputTokens"] == 24000


def test_per_call_kwargs_override_extra(monkeypatch):
    """per-call kwargs 优先于 config.extra。"""
    cfg = ModelConfig(provider="gemini", model_id="gemini-3.5-flash",
                      api_key="x", extra={"max_tokens": 24000})
    provider = GeminiProvider(cfg)
    captured: dict = {}

    class _Resp:
        def raise_for_status(self):
            return None

        def json(self):
            return {"candidates": [{"content": {"parts": [{"text": "ok"}]},
                                    "finishReason": "STOP"}]}

    async def _fake_post(self, url, json=None, headers=None):  # noqa: A002
        captured.update(json or {})
        return _Resp()

    monkeypatch.setattr(httpx.AsyncClient, "post", _fake_post)
    asyncio.run(provider.chat(messages=[{"role": "user", "content": "hi"}],
                              tools=[], max_tokens=100))
    assert captured["generationConfig"]["maxOutputTokens"] == 100
