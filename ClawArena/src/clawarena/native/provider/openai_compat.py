"""OpenAI-compatible provider，兼容 OpenAI / vLLM / Ollama / DashScope 等。"""
from __future__ import annotations

import json
import os
from typing import Any

import httpx

from ..types import ModelConfig
from .base import BaseProvider, ProviderError
from .usage import extract_openai_usage


class OpenAICompatProvider(BaseProvider):
    name = "openai_compat"

    def __init__(self, config: ModelConfig):
        super().__init__(config)
        self.api_base = (config.api_base or "https://api.openai.com/v1").rstrip("/")
        self.api_key = config.api_key or os.environ.get("OPENAI_API_KEY", "")

    async def chat(
        self,
        *,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": self.config.model_id,
            "messages": messages,
        }
        if tools:
            payload["tools"] = [{"type": "function", "function": t} for t in tools]
            payload["tool_choice"] = "auto"
        for k in ("temperature", "top_p"):
            if k in kwargs:
                payload[k] = kwargs[k]
        if "max_tokens" in kwargs:
            payload["max_completion_tokens"] = kwargs["max_tokens"]
        if "max_completion_tokens" in kwargs:
            payload["max_completion_tokens"] = kwargs["max_completion_tokens"]
        payload.update(self.config.extra)

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        url = f"{self.api_base}/chat/completions"
        timeout_sec = float(os.environ.get("ARCBENCH_PROVIDER_TIMEOUT_SEC", "600"))
        async with httpx.AsyncClient(timeout=httpx.Timeout(timeout_sec)) as client:
            try:
                resp = await client.post(url, json=payload, headers=headers)
                resp.raise_for_status()
            except httpx.HTTPError as e:
                raise ProviderError(f"OpenAI-compat request failed: {e}") from e
            data = resp.json()

        choice = (data.get("choices") or [{}])[0]
        msg = choice.get("message") or {}
        tool_calls_raw = msg.get("tool_calls") or []
        tool_calls = []
        for tc in tool_calls_raw:
            fn = tc.get("function") or {}
            args_raw = fn.get("arguments") or "{}"
            try:
                args = json.loads(args_raw) if isinstance(args_raw, str) else args_raw
            except json.JSONDecodeError:
                args = {"_raw": args_raw}
            tool_calls.append({"id": tc.get("id", ""), "name": fn.get("name", ""), "arguments": args})

        raw_usage, usage_rec = extract_openai_usage(data)
        return self.normalise_response(
            content=msg.get("content") or "",
            tool_calls=tool_calls,
            raw_usage=raw_usage,
            usage_normalized=usage_rec.to_dict(),
            finish_reason=choice.get("finish_reason", "stop"),
        )
