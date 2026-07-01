"""Anthropic Messages API provider。"""
from __future__ import annotations

import os
from typing import Any

import httpx

from ..types import ModelConfig
from .base import BaseProvider, ProviderError
from .usage import extract_anthropic_usage


class AnthropicProvider(BaseProvider):
    name = "anthropic"

    def __init__(self, config: ModelConfig):
        super().__init__(config)
        self.api_base = (config.api_base or "https://api.anthropic.com").rstrip("/")
        self.api_key = config.api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        self.api_version = config.extra.get("anthropic_version", "2023-06-01")

    async def chat(
        self,
        *,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        system_parts = [m["content"] for m in messages if m.get("role") == "system"]
        non_system = [m for m in messages if m.get("role") != "system"]

        payload: dict[str, Any] = {
            "model": self.config.model_id,
            "messages": non_system,
            "max_tokens": kwargs.get("max_tokens", 4096),
        }
        if system_parts:
            payload["system"] = "\n\n".join(system_parts)
        if tools:
            payload["tools"] = tools
        for k in ("temperature", "top_p"):
            if k in kwargs:
                payload[k] = kwargs[k]
        payload.update({k: v for k, v in self.config.extra.items() if k != "anthropic_version"})

        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": self.api_version,
        }
        url = f"{self.api_base}/v1/messages"
        async with httpx.AsyncClient(timeout=httpx.Timeout(120.0)) as client:
            try:
                resp = await client.post(url, json=payload, headers=headers)
                resp.raise_for_status()
            except httpx.HTTPError as e:
                raise ProviderError(f"Anthropic request failed: {e}") from e
            data = resp.json()

        content_text = ""
        tool_calls: list[dict[str, Any]] = []
        for block in data.get("content") or []:
            btype = block.get("type")
            if btype == "text":
                content_text += block.get("text", "")
            elif btype == "tool_use":
                tool_calls.append(
                    {
                        "id": block.get("id", ""),
                        "name": block.get("name", ""),
                        "arguments": block.get("input") or {},
                    }
                )

        raw_usage, usage_rec = extract_anthropic_usage(data)
        return self.normalise_response(
            content=content_text,
            tool_calls=tool_calls,
            raw_usage=raw_usage,
            usage_normalized=usage_rec.to_dict(),
            finish_reason=data.get("stop_reason", "stop"),
        )
