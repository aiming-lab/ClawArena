"""Anthropic Messages API provider.

The wire format of Anthropic ``/v1/messages`` differs substantially from the
OpenAI-style messages used internally by ClawArena-Team:

- ``system`` goes into a top-level ``system`` field (not inside messages);
- assistant tool calls are ``{type:tool_use, id, name, input}`` parts rather than
  OpenAI's ``message.tool_calls``;
- tool results are ``{type:tool_result, tool_use_id, content}`` parts on a user
  role, not standalone ``role: tool`` messages;
- tool declarations use ``input_schema`` instead of OpenAI's ``parameters``;
- ``max_tokens`` is required; the set of ``stop_reason`` values differs.

This implementation performs a minimal translation from ClawArena-Team harness
(OpenAI-style) to Anthropic Messages. Images use
``{type:image, source:{type:base64,...}}``; audio/video are not currently accepted
by Anthropic and are dropped (when the ClawArena-Team main pool declares modalities
without these two, this path is never reached). The retry / rate-limit backoff
strategy matches :mod:`.openai_compat` (same ``CATEAM_PROVIDER_*`` environment
variables).
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
import re
import time
from typing import Any

import httpx

from ..types import ModelConfig
from .base import BaseProvider, NonRetryableProviderError, ProviderError
from .usage import extract_anthropic_usage

# fable refusal fallback model: when the fable family refuses (refusal), automatically
# resend the same payload with this model. opus 4.8 is chosen because it is in the same
# tier as fable but has a different refusal policy (memory notes that this account has
# verified opus-4-8 is not available via Bedrock on-demand, but works via the native
# Anthropic API).
FABLE_FALLBACK_MODEL = "claude-opus-4-8"

log = logging.getLogger(__name__)


_FINISH_REASON_MAP = {
    "end_turn": "stop",
    "stop_sequence": "stop",
    "max_tokens": "length",
    "tool_use": "tool_calls",
    "pause_turn": "stop",
    "refusal": "stop",
}


def _retry_after_seconds(resp: httpx.Response) -> float | None:
    raw = resp.headers.get("retry-after") or resp.headers.get("Retry-After")
    if not raw:
        return None
    try:
        return max(0.0, float(raw.strip()))
    except (ValueError, AttributeError):
        return None


_DATA_URL_RE = re.compile(r"^data:(?P<mime>[^;]+);base64,(?P<data>.+)$", re.DOTALL)


def _convert_user_or_assistant_content(content: Any) -> str | list[dict[str, Any]]:
    """ClawArena-Team user/assistant content (str or OpenAI parts list) → Anthropic content.

    - a plain string is returned as-is (kept as str form, which Anthropic accepts);
    - OpenAI-style parts:
      - ``text``           → ``{type:text, text}``
      - ``image_url``      → ``{type:image, source:{type:base64, media_type, data}}``
                              (only data: URIs are recognized; http(s) URLs use ``{type:url}``)
      - ``video_url``/``input_audio`` → skipped (Anthropic does not yet support video/audio input)
    """
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return str(content or "")
    out: list[dict[str, Any]] = []
    for part in content:
        if not isinstance(part, dict):
            continue
        ptype = part.get("type")
        if ptype == "text":
            txt = part.get("text") or ""
            if txt:
                out.append({"type": "text", "text": txt})
        elif ptype == "image_url":
            url = (part.get("image_url") or {}).get("url", "")
            m = _DATA_URL_RE.match(url)
            if m:
                out.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": m.group("mime"),
                        "data": m.group("data"),
                    },
                })
            elif url.startswith(("http://", "https://")):
                out.append({"type": "image", "source": {"type": "url", "url": url}})
            # other forms (raw base64 without a data: URI header) are skipped — the
            # upstream convention is the data: URI
        elif ptype in ("video_url", "input_audio"):
            # The Anthropic Messages API does not currently accept audio/video input,
            # so skip it (the modalities config should not enable audio/video for main,
            # so this branch is normally unreachable; reaching it merely drops the part,
            # which is not fatal).
            log.warning("anthropic: skipping unsupported %s part", ptype)
        else:
            log.warning("anthropic: skipping unknown content part type %r", ptype)
    return out


def _to_anthropic_messages(
    messages: list[dict[str, Any]],
) -> tuple[str | None, list[dict[str, Any]]]:
    """OpenAI-style messages → ``(system_text, anthropic_messages)``.

    - ``system`` is concatenated into the top-level system;
    - an ``assistant`` message's ``tool_calls`` become ``{type:tool_use, id, name, input}``
      blocks, merged with the optional text block into a content list;
    - a ``tool`` message becomes ``{type:tool_result, tool_use_id, content}`` and is
      attached to the following user message; multiple consecutive tool results are
      merged into the same user message; if the previous entry is already a user
      message, it is appended there;
    - it is also merged when adjacent to the previous user message (Anthropic allows
      consecutive same-role messages, but merging is more robust).
    - Anthropic requires the first non-system message to be a user role; if the first
      history entry is an assistant message (rare), a placeholder empty user message
      ("." filler) is prepended to satisfy this constraint.
    """
    system_parts: list[str] = []
    out: list[dict[str, Any]] = []

    def _append_block_to_user(block: dict[str, Any]) -> None:
        if out and out[-1].get("role") == "user":
            cur = out[-1]["content"]
            if isinstance(cur, str):
                cur = [{"type": "text", "text": cur}] if cur else []
            cur.append(block)
            out[-1]["content"] = cur
        else:
            out.append({"role": "user", "content": [block]})

    for m in messages:
        role = m.get("role")
        if role == "system":
            txt = m.get("content") or ""
            if isinstance(txt, str) and txt:
                system_parts.append(txt)
            continue
        if role == "user":
            content = _convert_user_or_assistant_content(m.get("content"))
            if out and out[-1].get("role") == "user":
                prev = out[-1]["content"]
                if isinstance(prev, str):
                    prev = [{"type": "text", "text": prev}] if prev else []
                if isinstance(content, str):
                    if content:
                        prev.append({"type": "text", "text": content})
                else:
                    prev.extend(content)
                out[-1]["content"] = prev
            else:
                out.append({"role": "user", "content": content})
            continue
        if role == "assistant":
            text = m.get("content") or ""
            blocks: list[dict[str, Any]] = []
            if isinstance(text, str) and text:
                blocks.append({"type": "text", "text": text})
            elif isinstance(text, list):
                for part in text:
                    if isinstance(part, dict) and part.get("type") == "text":
                        t = part.get("text") or ""
                        if t:
                            blocks.append({"type": "text", "text": t})
            for tc in m.get("tool_calls") or []:
                fn = tc.get("function") or {}
                name = fn.get("name", "")
                args_raw = fn.get("arguments")
                if isinstance(args_raw, str):
                    try:
                        args = json.loads(args_raw) if args_raw else {}
                    except json.JSONDecodeError:
                        args = {"_raw": args_raw}
                elif isinstance(args_raw, dict):
                    args = args_raw
                else:
                    args = {}
                blocks.append({
                    "type": "tool_use",
                    "id": tc.get("id", ""),
                    "name": name,
                    "input": args,
                })
            if not blocks:
                blocks = [{"type": "text", "text": ""}]
            out.append({"role": "assistant", "content": blocks})
            continue
        if role == "tool":
            tcid = m.get("tool_call_id") or ""
            text = m.get("content") or ""
            if not isinstance(text, str):
                text = json.dumps(text, ensure_ascii=False)
            _append_block_to_user({
                "type": "tool_result",
                "tool_use_id": tcid,
                "content": text,
            })
            continue
        log.warning("anthropic: skipping unknown role %r in messages", role)

    if out and out[0].get("role") != "user":
        out.insert(0, {"role": "user", "content": "."})

    sys_text = "\n\n".join(system_parts) if system_parts else None
    return sys_text, out


def _to_anthropic_tools(
    tools: list[dict[str, Any]], *, cache_last: bool = False
) -> list[dict[str, Any]]:
    """OpenAI ``{name, description, parameters}`` → Anthropic ``{name, description, input_schema}``.

    When ``parameters`` is missing, ``{"type":"object","properties":{}}`` is supplied
    (Anthropic mandates ``input_schema.type == "object"``). Anthropic accepts the
    standard subset of JSON Schema itself, so no sanitization is needed as with Gemini.

    ``cache_last``: if true, marks the last tool with ``cache_control: ephemeral``;
    Anthropic treats "from the start of the request up to this tool" as the cache
    prefix, so subsequent changes to messages do not affect the cache hit on
    system+tools. The default TTL is 5 minutes (no beta header required).
    """
    out: list[dict[str, Any]] = []
    for t in tools or []:
        name = t.get("name", "")
        if not name:
            continue
        params = t.get("parameters")
        if not isinstance(params, dict) or not params:
            params = {"type": "object", "properties": {}}
        else:
            params = dict(params)
            if "type" not in params:
                params["type"] = "object"
            if params.get("type") == "object" and "properties" not in params:
                params["properties"] = {}
        decl: dict[str, Any] = {
            "name": name,
            "description": t.get("description", ""),
            "input_schema": params,
        }
        out.append(decl)
    if cache_last and out:
        out[-1] = {**out[-1], "cache_control": {"type": "ephemeral"}}
    return out


def _wrap_system_with_cache(system_text: str) -> list[dict[str, Any]]:
    """Wrap a plain-text system into an Anthropic block list and tag it with ephemeral
    cache_control (5 minutes).

    Anthropic requires cache_control to be attached to a block
    (``{type:text, text, cache_control}``), not to a string-form system; so without
    cache the str form can still be passed, while enabling cache switches to a list.
    A single system block is one cache breakpoint (Anthropic allows at most 4
    breakpoints per request).
    """
    return [
        {
            "type": "text",
            "text": system_text,
            "cache_control": {"type": "ephemeral"},
        }
    ]


class AnthropicProvider(BaseProvider):
    name = "anthropic"

    def __init__(self, config: ModelConfig):
        super().__init__(config)
        self.api_base = (config.api_base or "https://api.anthropic.com").rstrip("/")
        self.api_key = config.api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        self.api_version = config.extra.get("anthropic_version", "2023-06-01")
        # Prompt cache (5-minute ephemeral) switch: on by default, significantly reducing
        # the input billing for resending the system+tools prefix in long sonnet/opus/haiku
        # sessions (the hit price is 1/10 of normal input). Can be disabled via
        # config.extra["prompt_cache"]=false or CATEAM_ANTHROPIC_CACHE=0.
        cache_extra = config.extra.get("prompt_cache")
        env_off = os.environ.get("CATEAM_ANTHROPIC_CACHE", "").lower() in {"0", "false", "no", "off"}
        self.prompt_cache_enabled = (cache_extra is not False) and not env_off

    def _is_fable_model(self, model_id: str) -> bool:
        """Identify the fable family (claude-fable-5 or any model_id containing ``fable``,
        case-insensitive).

        fable is stricter on content moderation than sonnet/opus, and often triggers
        ``stop_reason: refusal`` on topics/PII/medical/legal material handled by the
        "management" role in ClawArena-Team scenarios. Patch: when fable refuses,
        automatically resend the same payload with ``opus-4-8`` and mark
        ``extra.fable_refusal_fallback``.
        """
        return "fable" in (model_id or "").lower()

    async def _post_messages(
        self,
        payload: dict[str, Any],
        *,
        deadline: float | None = None,
    ) -> dict[str, Any]:
        """One full POST /v1/messages (total time budget + retries + rate-limit backoff
        + non-retry on 4xx).

        ``deadline``: an absolute cutoff timestamp (same clock as ``time.time()``, in
        seconds). When given, all wait_for and retry calls use the "remaining time" as
        their upper bound and terminate immediately once the deadline passes; otherwise
        it falls back to the relative-timeout semantics of
        ``CATEAM_PROVIDER_TOTAL_TIMEOUT_SEC``.

        This parameter lets ``chat()`` and the fable refusal fallback POST share a single
        total time budget — otherwise the 480s × 2 of two independent POSTs would let a
        single turn blow past the budget and indirectly overrun the upper-layer
        ``CATEAM_SCENARIO_TIMEOUT_SEC`` wall clock (a lesson measured on
        s_security_pcap_triage).
        """
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": self.api_version,
        }
        url = f"{self.api_base}/v1/messages"

        timeout_sec = float(os.environ.get("CATEAM_PROVIDER_TIMEOUT_SEC", "600"))
        total_timeout_sec = float(os.environ.get("CATEAM_PROVIDER_TOTAL_TIMEOUT_SEC", "0") or "0")
        max_attempts = max(1, int(os.environ.get("CATEAM_PROVIDER_MAX_RETRIES", "3")))
        rl_attempts = max(1, int(os.environ.get("CATEAM_PROVIDER_RATELIMIT_RETRIES", "8")))

        # If no deadline is passed but env provides a total time budget, this call gets
        # its own exclusive budget.
        if deadline is None and total_timeout_sec > 0:
            deadline = time.time() + total_timeout_sec

        def _remaining() -> float | None:
            if deadline is None:
                return None
            return deadline - time.time()

        last_err: Exception | None = None
        data: dict[str, Any] | None = None
        attempt = 0
        rl_used = 0
        # Per-phase timeouts: connect/write/pool each get a short 30s fallback, read uses
        # timeout_sec (default 600s); this lets silent socket-loss phases
        # (handshake/write/pool half-open) be detected quickly, while a long read wait is
        # a reasonable upper bound for non-streaming responses. The original
        # ``httpx.Timeout(timeout_sec)`` set all four phases equally long, so a handshake
        # failure would wait 600s before erroring, defeating the fallback.
        http_timeout = httpx.Timeout(
            connect=30.0, read=timeout_sec, write=60.0, pool=30.0,
        )
        async with httpx.AsyncClient(timeout=http_timeout) as client:
            while True:
                delay = 1.5 * (attempt + 1)
                retryable = False
                try:
                    rem = _remaining()
                    if rem is not None and rem <= 0:
                        raise asyncio.TimeoutError(
                            "anthropic: total deadline exceeded before next POST attempt"
                        )
                    if rem is not None:
                        resp = await asyncio.wait_for(
                            client.post(url, json=payload, headers=headers),
                            timeout=rem,
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
                        # 4xx other than 429: deterministic client error, the scenario
                        # layer should not retry.
                        raise NonRetryableProviderError(
                            f"Anthropic request failed: {e}; body={body}"
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
                    f"Anthropic request failed after {max_attempts} attempts: {last_err}"
                ) from last_err
        return data

    async def chat(
        self,
        *,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        system_text, anth_messages = _to_anthropic_messages(messages)

        payload: dict[str, Any] = {
            "model": self.config.model_id,
            "messages": anth_messages,
        }
        if system_text:
            payload["system"] = (
                _wrap_system_with_cache(system_text)
                if self.prompt_cache_enabled
                else system_text
            )
        if tools:
            anth_tools = _to_anthropic_tools(tools, cache_last=self.prompt_cache_enabled)
            if anth_tools:
                payload["tools"] = anth_tools
        for k in ("temperature", "top_p"):
            if k in kwargs:
                payload[k] = kwargs[k]
        max_tok = kwargs.get("max_tokens")
        if max_tok is None:
            max_tok = self.config.extra.get("max_tokens", 4096)
        payload["max_tokens"] = int(max_tok)

        _skip = {"anthropic_version", "max_tokens", "temperature", "top_p",
                 "max_completion_tokens", "prompt_cache"}
        payload.update({k: v for k, v in self.config.extra.items() if k not in _skip})

        # Shared total time budget for a single chat() (env: CATEAM_PROVIDER_TOTAL_TIMEOUT_SEC):
        # the original POST and the fable refusal fallback POST share the same deadline,
        # preventing a doubled budget from overrunning the upper-layer wall clock.
        total_timeout_sec = float(os.environ.get("CATEAM_PROVIDER_TOTAL_TIMEOUT_SEC", "0") or "0")
        chat_deadline = time.time() + total_timeout_sec if total_timeout_sec > 0 else None

        data = await self._post_messages(payload, deadline=chat_deadline)
        extra: dict[str, Any] = {}

        # fable refusal → opus-4-8 fallback: triggered only for fable models +
        # stop_reason=refusal, a single fallback (if opus also refuses, its result is
        # accepted; no second fallback, to avoid an infinite chain). It shares
        # chat_deadline, ensuring the fallback POST can only use the remaining time of the
        # original budget and does not duplicate a fresh 480s budget.
        if (
            self._is_fable_model(payload["model"])
            and data.get("stop_reason") == "refusal"
        ):
            original_model = payload["model"]
            log.warning(
                "anthropic: %s returned stop_reason=refusal; retrying with %s",
                original_model, FABLE_FALLBACK_MODEL,
            )
            payload = {**payload, "model": FABLE_FALLBACK_MODEL}
            data = await self._post_messages(payload, deadline=chat_deadline)
            extra["fable_refusal_fallback"] = True
            extra["fallback_from_model"] = original_model
            extra["fallback_model"] = FABLE_FALLBACK_MODEL
            extra["note"] = (
                f"original model {original_model} returned stop_reason=refusal; "
                f"automatically resent the same payload with {FABLE_FALLBACK_MODEL}"
            )

        content_text = ""
        tool_calls: list[dict[str, Any]] = []
        for block in data.get("content") or []:
            btype = block.get("type")
            if btype == "text":
                content_text += block.get("text", "")
            elif btype == "tool_use":
                tool_calls.append({
                    "id": block.get("id", ""),
                    "name": block.get("name", ""),
                    "arguments": block.get("input") or {},
                })

        stop_reason = data.get("stop_reason") or "end_turn"
        finish = _FINISH_REASON_MAP.get(stop_reason, stop_reason)

        raw_usage, usage_rec = extract_anthropic_usage(data)
        return self.normalise_response(
            content=content_text,
            tool_calls=tool_calls,
            raw_usage=raw_usage,
            usage_normalized=usage_rec.to_dict(),
            finish_reason=finish,
            model_id=data.get("model"),
            extra=extra or None,
        )
