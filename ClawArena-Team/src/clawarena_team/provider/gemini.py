"""Google Gemini provider (``generateContent`` API).

Gemini's message structure differs substantially from OpenAI:

- ``system`` goes into the ``systemInstruction`` field (not inside ``contents``);
- the assistant role is called ``model`` in Gemini;
- a tool_call is expressed as a ``functionCall`` part;
- a tool result is expressed as a ``functionResponse`` part on a user role (no
  ``tool_call_id``, matched by name);
- tool declarations use the ``tools[0].functionDeclarations`` list (OpenAI uses
  ``tools[].function``).

This implementation only performs a minimal translation from ClawArena-Team harness
(OpenAI-style messages) → Gemini format, with no semantic rewriting. usage goes
through :func:`extract_gemini_usage`, with the raw field name ``usageMetadata``.
"""
from __future__ import annotations

import asyncio
import json
import os
from typing import Any

import httpx

from ..types import ModelConfig
from .base import BaseProvider, NonRetryableProviderError, ProviderError
from .usage import extract_gemini_usage


_DEFAULT_BASE = "https://generativelanguage.googleapis.com"
_API_VERSION = "v1beta"


def _retry_after_seconds(resp: httpx.Response) -> float | None:
    raw = resp.headers.get("retry-after") or resp.headers.get("Retry-After")
    if not raw:
        return None
    try:
        return max(0.0, float(raw.strip()))
    except (ValueError, AttributeError):
        return None


def _to_gemini_messages(
    messages: list[dict[str, Any]],
    sig_by_id: dict[str, str] | None = None,
) -> tuple[str | None, list[dict[str, Any]]]:
    """OpenAI-style messages → ``(systemInstruction_text, contents[])``.

    The ``tool_call_id → function_name`` reverse lookup is done by iterating over the
    historical ``tool_calls``.

    ``sig_by_id``: a ``tool_call_id → thoughtSignature`` map (recorded by the provider
    when generating a functionCall). Gemini 3 requires replaying a historical
    functionCall to carry back the original ``thoughtSignature`` on that part, otherwise
    400 "Function call is missing a thought_signature".
    """
    sig_by_id = sig_by_id or {}
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
                fc_part: dict[str, Any] = {"functionCall": {"name": name, "args": args}}
                tcid = tc.get("id") or ""
                sig = sig_by_id.get(tcid)
                if sig:  # Gemini 3: replaying a historical functionCall must carry back the original thoughtSignature
                    fc_part["thoughtSignature"] = sig
                parts.append(fc_part)
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


# The parameters of Gemini functionDeclarations only accept a subset of the OpenAPI
# Schema; keys common in OpenAI/JSON-Schema but **not recognized** by Gemini (such as
# additionalProperties, $schema, default) directly cause 400 "Unknown name ... Cannot
# find field". So recursively keep only the whitelisted keys before sending.
_GEMINI_SCHEMA_KEYS = {
    "type", "format", "title", "description", "nullable", "enum",
    "items", "properties", "required", "anyOf", "propertyOrdering",
    "minimum", "maximum", "minItems", "maxItems", "minLength", "maxLength",
    "pattern", "example",
}


def _sanitize_gemini_schema(node: Any) -> Any:
    """Recursively strip JSON-Schema keys not supported by Gemini, returning the
    sanitized schema."""
    if isinstance(node, dict):
        clean: dict[str, Any] = {}
        for k, v in node.items():
            if k not in _GEMINI_SCHEMA_KEYS:
                continue  # drop additionalProperties / $schema / default, etc.
            if k == "properties" and isinstance(v, dict):
                clean[k] = {pk: _sanitize_gemini_schema(pv) for pk, pv in v.items()}
            elif k in ("items",):
                clean[k] = _sanitize_gemini_schema(v)
            elif k == "anyOf" and isinstance(v, list):
                clean[k] = [_sanitize_gemini_schema(x) for x in v]
            else:
                clean[k] = v
        return clean
    if isinstance(node, list):
        return [_sanitize_gemini_schema(x) for x in node]
    return node


def _to_gemini_tools(tools: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """OpenAI ``{name, description, parameters}`` → Gemini ``functionDeclarations``.

    parameters are passed through :func:`_sanitize_gemini_schema` to strip schema keys
    not supported by Gemini (such as ``additionalProperties``), otherwise Gemini returns
    400 INVALID_ARGUMENT.
    """
    decls: list[dict[str, Any]] = []
    for t in tools or []:
        decl: dict[str, Any] = {
            "name": t.get("name", ""),
            "description": t.get("description", ""),
        }
        if t.get("parameters"):
            decl["parameters"] = _sanitize_gemini_schema(t["parameters"])
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
        # Gemini 3 thought_signature pass-through: record the signatures of functionCalls
        # generated by this instance, indexed by globally-unique tool_call_id, and
        # re-inject them when replaying history (see _to_gemini_messages). The provider
        # instance is reused across the multiple turns of one agent, so the map survives
        # across turns.
        self._sig_by_id: dict[str, str] = {}
        self._call_seq = 0

    async def chat(
        self,
        *,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        system_text, contents = _to_gemini_messages(messages, self._sig_by_id)
        payload: dict[str, Any] = {"contents": contents}
        if system_text:
            payload["systemInstruction"] = {"parts": [{"text": system_text}]}
        if tools:
            decls = _to_gemini_tools(tools)
            if decls:
                payload["tools"] = decls

        # OpenAI-style sampling/limit keys (from per-call kwargs or the target's
        # config.extra) need to be translated into Gemini generationConfig rather than
        # placed directly into the top-level payload (the latter would be rejected by
        # Gemini as "Unknown name"). kwargs take priority over config.extra.
        _gen_map = (
            ("max_tokens", "maxOutputTokens"),
            ("max_completion_tokens", "maxOutputTokens"),
            ("temperature", "temperature"),
            ("top_p", "topP"),
        )
        gen_cfg: dict[str, Any] = {}
        for src, dst in _gen_map:
            if src in kwargs:
                gen_cfg[dst] = kwargs[src]
            elif src in self.config.extra:
                gen_cfg[dst] = self.config.extra[src]
        if gen_cfg:
            payload["generationConfig"] = gen_cfg
        _gen_src_keys = {s for s, _ in _gen_map}
        payload.update(
            {
                k: v
                for k, v in self.config.extra.items()
                if k != "gemini_api_version" and k not in _gen_src_keys
            }
        )

        url = (
            f"{self.api_base}/{self.api_version}/models/"
            f"{self.config.model_id}:generateContent"
        )
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["x-goog-api-key"] = self.api_key

        # The retry strategy fully matches :mod:`.openai_compat` / :mod:`.anthropic`:
        # same-name env variables, backoff retries on transport/5xx/429, and a direct
        # raise of ``NonRetryableProviderError`` on 4xx other than 429.
        timeout_sec = float(os.environ.get("CATEAM_PROVIDER_TIMEOUT_SEC", "600"))
        total_timeout_sec = float(os.environ.get("CATEAM_PROVIDER_TOTAL_TIMEOUT_SEC", "0") or "0")
        max_attempts = max(1, int(os.environ.get("CATEAM_PROVIDER_MAX_RETRIES", "3")))
        rl_attempts = max(1, int(os.environ.get("CATEAM_PROVIDER_RATELIMIT_RETRIES", "8")))

        last_err: Exception | None = None
        data: dict[str, Any] | None = None
        attempt = 0
        rl_used = 0
        # Per-phase timeouts: aligned with anthropic / openai_compat, to prevent
        # handshake/write from hanging forever.
        http_timeout = httpx.Timeout(
            connect=30.0, read=timeout_sec, write=60.0, pool=30.0,
        )
        async with httpx.AsyncClient(timeout=http_timeout) as client:
            while True:
                delay = 1.5 * (attempt + 1)
                retryable = False
                try:
                    if total_timeout_sec > 0:
                        resp = await asyncio.wait_for(
                            client.post(url, json=payload, headers=headers),
                            timeout=total_timeout_sec,
                        )
                    else:
                        resp = await client.post(url, json=payload, headers=headers)
                    resp.raise_for_status()
                    data = resp.json()
                    break
                except (asyncio.TimeoutError, httpx.TimeoutException) as e:
                    last_err = e
                    retryable = True
                except httpx.HTTPStatusError as e:
                    code = e.response.status_code
                    body = ""
                    try:
                        body = e.response.text[:600]
                    except Exception:  # noqa: BLE001
                        pass
                    if code == 429:
                        last_err = e
                        rl_used += 1
                        if rl_used >= rl_attempts:
                            break
                        ra = _retry_after_seconds(e.response)
                        delay = ra if ra is not None else min(45.0, 2.0 * (2 ** min(rl_used, 5)))
                        await asyncio.sleep(delay)
                        continue
                    if code < 500:
                        raise NonRetryableProviderError(
                            f"Gemini request failed: {e}; body={body}"
                        ) from e
                    last_err = e
                    retryable = True
                except httpx.TransportError as e:
                    last_err = e
                    retryable = True
                attempt += 1
                if retryable and attempt < max_attempts:
                    await asyncio.sleep(delay)
                    continue
                break
            if data is None:
                raise ProviderError(
                    f"Gemini request failed after {max_attempts} attempts: {last_err}"
                ) from last_err

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
                    # Gemini does not return a tool_call_id; generate a cross-turn
                    # globally-unique id (auto-incremented within the instance) so this
                    # functionCall's thoughtSignature can be recorded into
                    # self._sig_by_id and re-injected by id when replaying history
                    # (mandatory for Gemini 3).
                    tcid = f"gm_{self._call_seq}"
                    self._call_seq += 1
                    sig = part.get("thoughtSignature")
                    if sig:
                        self._sig_by_id[tcid] = sig
                    tool_calls.append(
                        {
                            "id": tcid,
                            "name": fc.get("name", ""),
                            "arguments": fc.get("args") or {},
                        }
                    )

        raw_usage, usage_rec = extract_gemini_usage(data)
        # Gemini generateContent does not echo a model field at the top level of the
        # response, so fall back to config.
        return self.normalise_response(
            content=content_text,
            tool_calls=tool_calls,
            raw_usage=raw_usage,
            usage_normalized=usage_rec.to_dict(),
            finish_reason=finish_reason,
            model_id=(data.get("modelVersion") or self.config.model_id),
        )
