"""Cross-provider normalized usage structure.

The usage field names differ greatly across providers:

- **OpenAI (chat.completions)**::

    "usage": {"prompt_tokens", "completion_tokens", "total_tokens",
              "prompt_tokens_details": {"cached_tokens": int, ...},
              "completion_tokens_details": {"reasoning_tokens": int, ...}}

- **Anthropic (v1/messages)**::

    "usage": {"input_tokens", "output_tokens",
              "cache_read_input_tokens", "cache_creation_input_tokens"}

- **Gemini (generateContent)** — the outer field name is ``usageMetadata``, **not**
  ``usage``::

    "usageMetadata": {"promptTokenCount", "candidatesTokenCount",
                      "cachedContentTokenCount", "thoughtsTokenCount",
                      "toolUsePromptTokenCount", "totalTokenCount"}

This module defines the cross-provider reconcilable :class:`UsageRecord` and provides
the extraction functions for all three providers. The raw dict is also passed through
and preserved via the ``raw_usage`` field (which may contain finer-grained sub-items
such as audio_tokens) for later fine-grained analysis. **The harness does not consume
these fields**; they are only written to jsonl as a statistics source.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class UsageRecord:
    """A unified billing view aligned across providers."""

    # new input tokens (the cache-miss portion; excludes cache_read)
    input_tokens: int = 0
    # model-visible output tokens; reasoning_tokens is a sub-item of output in several
    # providers and is listed separately as well
    output_tokens: int = 0
    # the portion read from a cache hit
    cache_read_tokens: int = 0
    # the portion written to cache (only Anthropic has this explicitly; OpenAI/Gemini set 0)
    cache_write_tokens: int = 0
    # reasoning tokens (OpenAI reasoning_tokens / Gemini thoughtsTokenCount;
    # Anthropic does not break this out separately, set 0)
    reasoning_tokens: int = 0
    # the three providers' total measures are inconsistent, so prefer each provider's raw;
    # when missing, fall back to summing the four items above
    total_tokens: int = 0
    # the source provider name (matching the registered name in the registry)
    provider: str = ""
    # the raw provider usage dict (any schema passed through; fine-grained items such as
    # audio_tokens are preserved here)
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
    """Extract raw + normalized usage from an OpenAI chat.completions response."""
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
    """Extract raw + normalized usage from an Anthropic Messages API response."""
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
    """Extract raw + normalized usage from a Gemini generateContent response.

    Note the outer field name is ``usageMetadata``. ``cachedContentTokenCount`` and
    ``thoughtsTokenCount`` may be entirely absent when cache is not used / thinking is
    not enabled.
    """
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
