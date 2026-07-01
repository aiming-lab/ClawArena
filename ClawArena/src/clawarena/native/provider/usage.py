"""Provider usage 跨家规范化结构。

OpenAI / Anthropic / Gemini 三家 usage 字段名差异极大；本模块定义跨家可对账的
:class:`UsageRecord`，并给出三家的提取函数。harness 不消费这些字段——它们仅落
jsonl 作统计来源；正式决策走本地统一 tokenizer。
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class UsageRecord:
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0
    reasoning_tokens: int = 0
    total_tokens: int = 0
    provider: str = ""
    raw: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _i(d: dict[str, Any] | None, key: str, default: int = 0) -> int:
    if not d:
        return default
    v = d.get(key)
    if v is None:
        return default
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def extract_openai_usage(data: dict[str, Any]) -> tuple[dict[str, Any], UsageRecord]:
    u = data.get("usage") or {}
    pd = u.get("prompt_tokens_details") or {}
    cd = u.get("completion_tokens_details") or {}
    cache_read = _i(pd, "cached_tokens")
    reasoning = _i(cd, "reasoning_tokens")
    prompt = _i(u, "prompt_tokens")
    completion = _i(u, "completion_tokens")
    total = _i(u, "total_tokens", prompt + completion)
    rec = UsageRecord(
        input_tokens=max(0, prompt - cache_read),
        output_tokens=completion,
        cache_read_tokens=cache_read,
        cache_write_tokens=0,
        reasoning_tokens=reasoning,
        total_tokens=total,
        provider="openai_compat",
        raw=dict(u),
    )
    return dict(u), rec


def extract_anthropic_usage(data: dict[str, Any]) -> tuple[dict[str, Any], UsageRecord]:
    u = data.get("usage") or {}
    it = _i(u, "input_tokens")
    ot = _i(u, "output_tokens")
    cr = _i(u, "cache_read_input_tokens")
    cw = _i(u, "cache_creation_input_tokens")
    rec = UsageRecord(
        input_tokens=it,
        output_tokens=ot,
        cache_read_tokens=cr,
        cache_write_tokens=cw,
        reasoning_tokens=0,
        total_tokens=it + ot + cr + cw,
        provider="anthropic",
        raw=dict(u),
    )
    return dict(u), rec


def extract_gemini_usage(data: dict[str, Any]) -> tuple[dict[str, Any], UsageRecord]:
    u = data.get("usageMetadata") or {}
    prompt = _i(u, "promptTokenCount")
    candidates = _i(u, "candidatesTokenCount")
    cached = _i(u, "cachedContentTokenCount")
    thoughts = _i(u, "thoughtsTokenCount")
    total = _i(u, "totalTokenCount", prompt + candidates + thoughts)
    rec = UsageRecord(
        input_tokens=max(0, prompt - cached),
        output_tokens=candidates,
        cache_read_tokens=cached,
        cache_write_tokens=0,
        reasoning_tokens=thoughts,
        total_tokens=total,
        provider="gemini",
        raw=dict(u),
    )
    return dict(u), rec
