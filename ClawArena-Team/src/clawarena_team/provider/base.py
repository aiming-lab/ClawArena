"""Provider base class.

All provider subclasses expose a unified ``async chat(messages, tools, **kw)`` interface
and return a standardized dict::

    {
        "content":         str,
        "tool_calls":      [{"id": str, "name": str, "arguments": dict}, ...],
        "raw_usage":       dict,            # raw provider usage fields, any schema passed straight through
        "usage_normalized": dict,           # UsageRecord.to_dict(), the cross-provider reconcilable unified view
        "finish_reason":   str,
        "model_id":        str,             # the model id actually echoed by the provider (falls back to config.model_id if missing)
        "extra":           dict,            # an additional dict freely passed through by the provider (e.g. fallback notes)
    }

``raw_usage`` and ``usage_normalized`` are only for statistics/reconciliation and are
**not consumed by the harness** — the harness's token counting uses a local unified
tokenizer, decoupled from the provider (see design-philosophy §3.5).

Exception hierarchy:

- :class:`ProviderError` — the generic exception base class for provider call failures
  (transient / rate-limited / retries exhausted, etc.); by default the upper-layer
  scenario runner reruns the whole scenario according to ``--retry``.
- :class:`NonRetryableProviderError` — a **deterministic** client error (4xx, not 429),
  e.g. 400 invalid payload, 401 authentication, 403 forbidden, 404 model not found.
  Rerunning the same scenario will inevitably reproduce the same error, so when the
  scenario runner sees this exception it should **abandon the scenario directly** without
  consuming the retry budget.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from ..types import ModelConfig


class ProviderError(RuntimeError):
    """Provider call failure."""


class NonRetryableProviderError(ProviderError):
    """Deterministic client error (4xx other than 429). Rerunning the same scenario will
    reproduce it, so the scenario layer should not retry."""


class BaseProvider(ABC):
    name: str = "base"

    def __init__(self, config: ModelConfig):
        self.config = config

    @abstractmethod
    async def chat(
        self,
        *,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        raise NotImplementedError

    def normalise_response(
        self,
        *,
        content: str = "",
        tool_calls: list[dict[str, Any]] | None = None,
        raw_usage: dict[str, Any] | None = None,
        usage_normalized: dict[str, Any] | None = None,
        finish_reason: str = "stop",
        model_id: str | None = None,
        extra: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Build the unified response dict.

        ``model_id``: the value actually echoed by the provider; falls back to
        ``self.config.model_id`` if empty.
        ``extra``: a provider's free-form additional fields (any dict); used for example
        by the fable refusal fallback to record refusal/fallback information. The harness
        passes it through to ``provider_extra`` in main.jsonl.
        """
        return {
            "content": content or "",
            "tool_calls": tool_calls or [],
            "raw_usage": raw_usage or {},
            "usage_normalized": usage_normalized or {},
            "finish_reason": finish_reason,
            "model_id": model_id or self.config.model_id,
            "extra": extra or {},
        }
