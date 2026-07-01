"""OpenAI-compatible provider, compatible with OpenAI / vLLM / the Ollama OpenAI
interface / DashScope, etc."""
from __future__ import annotations

import asyncio
import json
import os
from typing import Any

import httpx

from ..types import ModelConfig
from .base import BaseProvider, NonRetryableProviderError, ProviderError
from .usage import extract_openai_usage


def _retry_after_seconds(resp: httpx.Response) -> float | None:
    """Parse the ``Retry-After`` header of 429/503 (only the integer-seconds form is
    supported; the HTTP-date form is ignored, with backoff falling back to exponential).
    Returns a non-negative number of seconds or None."""
    raw = resp.headers.get("retry-after") or resp.headers.get("Retry-After")
    if not raw:
        return None
    try:
        return max(0.0, float(raw.strip()))
    except (ValueError, AttributeError):
        return None


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
        # OpenAI's newer reasoning models have deprecated ``max_tokens`` in favor of
        # ``max_completion_tokens``; both vLLM 0.19 and the legacy OpenAI endpoint are
        # backward-compatible with this alias, so it is sent uniformly.
        if "max_tokens" in kwargs:
            payload["max_completion_tokens"] = kwargs["max_tokens"]
        if "max_completion_tokens" in kwargs:
            payload["max_completion_tokens"] = kwargs["max_completion_tokens"]
        payload.update(self.config.extra)

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        url = f"{self.api_base}/chat/completions"
        timeout_sec = float(os.environ.get("CATEAM_PROVIDER_TIMEOUT_SEC", "600"))
        # Total-time fallback (``CATEAM_PROVIDER_TOTAL_TIMEOUT_SEC``, default 0=disabled,
        # preserving the original semantics). httpx.Timeout is only a "per-socket-read"
        # timeout: some upstreams (such as ChatMock buffering gpt-5.5 streaming output)
        # intermittently trickle bytes, continually resetting the per-read timeout, so the
        # body of the entire ``client.post`` never completes, the read timeout never fires,
        # and main freezes the whole scenario forever at ep_poll. When >0, use
        # ``asyncio.wait_for`` to wrap a single request in a real total time budget: on
        # timeout the request is cancelled and handled as a retryable transport-layer error
        # (going through limited backoff retries) rather than hanging indefinitely.
        total_timeout_sec = float(os.environ.get("CATEAM_PROVIDER_TOTAL_TIMEOUT_SEC", "0") or "0")
        # Transient connection jitter (ReadError/RemoteProtocolError/timeout, etc.) occurs
        # occasionally when running long scenarios concurrently, failing the whole scenario
        # with an empty-message ProviderError and losing a result. Do limited retries
        # (exponential backoff) on transport-layer errors and 5xx; 4xx is a deterministic
        # client error (out-of-range modality / limit, etc.) and is not retried. Exception:
        # 429 Too Many Requests is rate limiting (especially the RPM/TPM of bedrock
        # on-demand) and is retryable — honor Retry-After first, otherwise a longer
        # exponential backoff; the rate-limit retry budget is enlarged independently
        # (CATEAM_PROVIDER_RATELIMIT_RETRIES, default 8), since rate-limit windows often last
        # tens of seconds.
        max_attempts = max(1, int(os.environ.get("CATEAM_PROVIDER_MAX_RETRIES", "3")))
        rl_attempts = max(1, int(os.environ.get("CATEAM_PROVIDER_RATELIMIT_RETRIES", "8")))
        last_err: Exception | None = None
        data: dict[str, Any] | None = None
        attempt = 0
        rl_used = 0  # 429 retries do not count toward max_attempts (otherwise rate limiting would eat up the normal retry budget)
        # Per-phase timeouts: see the same design in anthropic (to prevent silent
        # handshake/write loss from waiting forever).
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
                    # Total/per-read timeout: the upstream stalled, handled as a retryable
                    # transient error (resend after backoff).
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
                        # Retry-After first; otherwise exponential backoff, capped at 45s to give the rate-limit window room to breathe
                        delay = ra if ra is not None else min(45.0, 2.0 * (2 ** min(rl_used, 5)))
                        await asyncio.sleep(delay)
                        continue  # do not increment attempt
                    if code < 500:
                        # 4xx other than 429: deterministic client error, the scenario layer should not retry.
                        raise NonRetryableProviderError(
                            f"OpenAI-compat request failed: {e}; body={body}"
                        ) from e
                    last_err = e  # 5xx is retryable
                    retryable = True
                except httpx.TransportError as e:
                    last_err = e  # transient errors (connection/read/protocol, etc.) are retryable
                    retryable = True
                attempt += 1
                if retryable and attempt < max_attempts:
                    await asyncio.sleep(delay)
                    continue
                break
            if data is None:
                raise ProviderError(
                    f"OpenAI-compat request failed after {max_attempts} attempts: {last_err}"
                ) from last_err

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
            model_id=data.get("model"),
        )
