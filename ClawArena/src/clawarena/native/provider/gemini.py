"""Google Gemini provider (``generateContent`` API)。"""
from __future__ import annotations

import json
import os
from typing import Any

import httpx

from ..types import ModelConfig
from .base import BaseProvider, ProviderError
from .usage import extract_gemini_usage


_DEFAULT_BASE = "https://generativelanguage.googleapis.com"
_API_VERSION = "v1beta"


def _to_gemini_messages(
    messages: list[dict[str, Any]],
) -> tuple[str | None, list[dict[str, Any]]]:
    system_parts: list[str] = []
    contents: list[dict[str, Any]] = []
    call_name_by_id: dict[str, str] = {}
    for m in messages:
        role = m.get("role")
        if role == "system":
            text = m.get("content") or ""
            if text:
                system_parts.append(text)
            continue
        if role == "user":
            text = m.get("content") or ""
            contents.append({"role": "user", "parts": [{"text": text}]})
            continue
        if role == "assistant":
            text = m.get("content") or ""
            parts: list[dict[str, Any]] = []
            if text:
                parts.append({"text": text})
            for tc in m.get("tool_calls") or []:
                fn = tc.get("function") or {}
                name = fn.get("name", "")
                args_raw = fn.get("arguments") or "{}"
                try:
                    args = json.loads(args_raw) if isinstance(args_raw, str) else args_raw
                except json.JSONDecodeError:
                    args = {"_raw": args_raw}
                parts.append({"functionCall": {"name": name, "args": args}})
                tcid = tc.get("id") or ""
                if tcid:
                    call_name_by_id[tcid] = name
            if parts:
                contents.append({"role": "model", "parts": parts})
            continue
        if role == "tool":
            tcid = m.get("tool_call_id") or ""
            fname = call_name_by_id.get(tcid, "")
            text = m.get("content") or ""
            contents.append(
                {
                    "role": "user",
                    "parts": [
                        {
                            "functionResponse": {
                                "name": fname,
                                "response": {"content": text},
                            }
                        }
                    ],
                }
            )
            continue
    sys_text = "\n\n".join(system_parts) if system_parts else None
    return sys_text, contents


def _to_gemini_tools(tools: list[dict[str, Any]]) -> list[dict[str, Any]]:
    decls: list[dict[str, Any]] = []
    for t in tools or []:
        decl: dict[str, Any] = {
            "name": t.get("name", ""),
            "description": t.get("description", ""),
        }
        if t.get("parameters"):
            decl["parameters"] = t["parameters"]
        decls.append(decl)
    return [{"functionDeclarations": decls}] if decls else []


class GeminiProvider(BaseProvider):
    name = "gemini"

    def __init__(self, config: ModelConfig):
        super().__init__(config)
        self.api_base = (config.api_base or _DEFAULT_BASE).rstrip("/")
        self.api_key = (
            config.api_key
            or os.environ.get("GEMINI_API_KEY")
            or os.environ.get("GOOGLE_API_KEY", "")
        )
        self.api_version = config.extra.get("gemini_api_version", _API_VERSION)

    async def chat(
        self,
        *,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        system_text, contents = _to_gemini_messages(messages)
        payload: dict[str, Any] = {"contents": contents}
        if system_text:
            payload["systemInstruction"] = {"parts": [{"text": system_text}]}
        if tools:
            decls = _to_gemini_tools(tools)
            if decls:
                payload["tools"] = decls

        gen_cfg: dict[str, Any] = {}
        for src, dst in (
            ("max_tokens", "maxOutputTokens"),
            ("max_completion_tokens", "maxOutputTokens"),
            ("temperature", "temperature"),
            ("top_p", "topP"),
        ):
            if src in kwargs:
                gen_cfg[dst] = kwargs[src]
        if gen_cfg:
            payload["generationConfig"] = gen_cfg
        payload.update(
            {k: v for k, v in self.config.extra.items() if k != "gemini_api_version"}
        )

        url = (
            f"{self.api_base}/{self.api_version}/models/"
            f"{self.config.model_id}:generateContent"
        )
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["x-goog-api-key"] = self.api_key

        async with httpx.AsyncClient(timeout=httpx.Timeout(120.0)) as client:
            try:
                resp = await client.post(url, json=payload, headers=headers)
                resp.raise_for_status()
            except httpx.HTTPError as e:
                raise ProviderError(f"Gemini request failed: {e}") from e
            data = resp.json()

        content_text = ""
        tool_calls: list[dict[str, Any]] = []
        candidates = data.get("candidates") or []
        finish_reason = "stop"
        if candidates:
            cand0 = candidates[0]
            finish_reason = cand0.get("finishReason", "stop")
            parts = (cand0.get("content") or {}).get("parts") or []
            for part in parts:
                if part.get("text") is not None:
                    content_text += part["text"]
                if "functionCall" in part:
                    fc = part["functionCall"] or {}
                    tool_calls.append(
                        {
                            "id": f"call_{len(tool_calls)}",
                            "name": fc.get("name", ""),
                            "arguments": fc.get("args") or {},
                        }
                    )

        raw_usage, usage_rec = extract_gemini_usage(data)
        return self.normalise_response(
            content=content_text,
            tool_calls=tool_calls,
            raw_usage=raw_usage,
            usage_normalized=usage_rec.to_dict(),
            finish_reason=finish_reason,
        )
