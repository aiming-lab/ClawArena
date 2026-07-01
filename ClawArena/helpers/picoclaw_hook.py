#!/usr/bin/env python3
"""PicoClaw LLM logger hook — writes agent_end JSON after each turn.

Implements picoclaw's process-hook JSON-RPC 2.0 / stdio protocol.
Communication is one JSON object per line over stdin/stdout.

Protocol summary
----------------
  Calls (have "id"):   hook.hello, hook.before_llm, hook.after_llm
                       → must write a JSON-RPC response back
  Notifications (no "id"):  hook.event
                       → fire-and-forget, no response written

Data capture strategy
---------------------
  before_llm  : buffer messages[] (overwritten each iteration;
                last one contains the full accumulated context)
  after_llm   : buffer final LLM response; accumulate usage across
                all iterations within the turn
  turn_end    : merge buffered data, write agent-end.json, clear buffer

Required env var
----------------
  CLAWARENA_PICOCLAW_LOG_DIR   root directory for log files
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

_log_root = Path(os.environ.get("CLAWARENA_PICOCLAW_LOG_DIR", ""))

# Per-session buffer keyed by session_key.
# Schema: { "messages": [...], "last_response": {...}, "usage": {...} }
_buffers: dict[str, dict] = {}

# turn_end EventKind value (from events.go iota: TurnStart=0, TurnEnd=1)
_KIND_TURN_END = 1


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def _filename_ts() -> str:
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%dT%H-%M-%S-") + f"{now.microsecond // 1000:03d}Z"


def _get_usage(usage_obj: dict) -> dict:
    """Normalise usage dict — providers may use snake_case or PascalCase."""
    if not isinstance(usage_obj, dict):
        return {}
    return {
        "prompt_tokens": (
            usage_obj.get("prompt_tokens") or usage_obj.get("PromptTokens") or 0
        ),
        "completion_tokens": (
            usage_obj.get("completion_tokens") or usage_obj.get("CompletionTokens") or 0
        ),
        "total_tokens": (
            usage_obj.get("total_tokens") or usage_obj.get("TotalTokens") or 0
        ),
    }


def _write_agent_end(session_key: str, duration_ms: float, success: bool) -> None:
    buf = _buffers.pop(session_key, {})
    messages: list = list(buf.get("messages") or [])
    last_response: dict = buf.get("last_response") or {}
    usage: dict = buf.get("usage") or {}

    # Append the final assistant message so the snapshot is complete.
    if last_response:
        final_msg: dict = {"role": "assistant", "content": last_response.get("content")}
        tool_calls = last_response.get("tool_calls")
        if tool_calls:
            final_msg["tool_calls"] = tool_calls
        messages.append(final_msg)

    data = {
        "stage": "agent_end",
        "timestamp": _iso_now(),
        "sessionKey": session_key,
        "success": success,
        "durationMs": round(duration_ms, 1),
        "messageCount": len(messages),
        "messages": messages,
        "usage": usage,
    }

    session_dir = _log_root / session_key
    try:
        session_dir.mkdir(parents=True, exist_ok=True)
        fname = f"{_filename_ts()}_agent-end.json"
        (session_dir / fname).write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Message handlers
# ---------------------------------------------------------------------------

def _handle(msg: dict) -> dict | None:
    """Process one JSON-RPC message; return response dict or None (notifications)."""
    method: str = msg.get("method", "")

    # ── Notifications (no id) ── fire & forget, no response
    if "id" not in msg:
        if method == "hook.event":
            params = msg.get("params") or {}
            # EventKind is PascalCase (no json tags on Go struct)
            kind = params.get("Kind")
            if kind == _KIND_TURN_END:
                meta = params.get("Meta") or {}
                payload = params.get("Payload") or {}
                session_key = meta.get("SessionKey") or "unknown"
                # Duration is time.Duration (int64 nanoseconds)
                duration_ns = payload.get("Duration") or 0
                duration_ms = duration_ns / 1_000_000
                status = payload.get("Status") or "completed"
                _write_agent_end(session_key, duration_ms, status == "completed")
        return None

    # ── Calls (have id) ── must respond
    msg_id = msg["id"]

    if method == "hook.hello":
        return {"id": msg_id, "result": {}}

    if method == "hook.before_llm":
        # Outer fields have json tags (snake_case); EventMeta sub-fields are PascalCase
        params = msg.get("params") or {}
        meta = params.get("meta") or {}
        session_key = meta.get("SessionKey") or "unknown"
        buf = _buffers.setdefault(session_key, {})
        buf["messages"] = params.get("messages") or []
        return {"id": msg_id, "result": {"action": "continue"}}

    if method == "hook.after_llm":
        params = msg.get("params") or {}
        meta = params.get("meta") or {}
        session_key = meta.get("SessionKey") or "unknown"
        buf = _buffers.setdefault(session_key, {})
        response = params.get("response") or {}
        buf["last_response"] = response
        # Accumulate usage across all LLM iterations within this turn
        call_usage = _get_usage(response.get("usage") or {})
        acc = buf.setdefault("usage", {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0})
        acc["prompt_tokens"] += call_usage["prompt_tokens"]
        acc["completion_tokens"] += call_usage["completion_tokens"]
        acc["total_tokens"] += call_usage["total_tokens"]
        return {"id": msg_id, "result": {"action": "continue"}}

    # Unknown method — return JSON-RPC method-not-found error
    return {"id": msg_id, "error": {"code": -32601, "message": f"unknown method: {method}"}}


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def main() -> None:
    for raw_line in sys.stdin:
        raw_line = raw_line.strip()
        if not raw_line:
            continue
        try:
            msg = json.loads(raw_line)
        except json.JSONDecodeError:
            continue

        resp = _handle(msg)
        if resp is None:
            continue

        resp["jsonrpc"] = "2.0"
        sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
