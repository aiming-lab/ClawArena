"""Provider 基类。

所有 provider 子类暴露统一的 ``async chat(messages, tools, **kw)`` 接口，
返回标准化 dict::

    {
        "content":          str,
        "tool_calls":       [{"id": str, "name": str, "arguments": dict}, ...],
        "raw_usage":        dict,            # 原始 usage 字段，任意 schema 透传
        "usage_normalized": dict,            # UsageRecord.to_dict()
        "finish_reason":    str,
    }

``raw_usage`` 与 ``usage_normalized`` 仅作统计/对账，**harness 不消费**——harness
内的 token 计数走本地统一 tokenizer，与 provider 解耦。
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from ..types import ModelConfig


class ProviderError(RuntimeError):
    """Provider 调用失败。"""


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

    @staticmethod
    def normalise_response(
        *,
        content: str = "",
        tool_calls: list[dict[str, Any]] | None = None,
        raw_usage: dict[str, Any] | None = None,
        usage_normalized: dict[str, Any] | None = None,
        finish_reason: str = "stop",
    ) -> dict[str, Any]:
        return {
            "content": content or "",
            "tool_calls": tool_calls or [],
            "raw_usage": raw_usage or {},
            "usage_normalized": usage_normalized or {},
            "finish_reason": finish_reason,
        }
