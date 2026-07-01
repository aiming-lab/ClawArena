"""Deterministic episode memory for CLI-agent rollouts.

This module keeps a compact, testable summary of prior observations so the
agent can retain important context without replaying the full transcript.
"""

from __future__ import annotations

import shlex
from typing import Any

_READ_ONLY_COMMAND_PREFIXES: tuple[tuple[str, ...], ...] = (
    ("email", "search"),
    ("email", "read"),
    ("calendar", "today"),
    ("calendar", "list"),
    ("calendar", "search"),
    ("weather", "get"),
    ("weather", "forecast"),
    ("weather", "alerts"),
    ("tasks", "list"),
    ("tasks", "search"),
    ("openclaw", "cron", "list"),
    ("openclaw", "agents", "list"),
    ("openclaw", "channel", "list"),
    ("openclaw", "monitor", "show"),
    ("openclaw", "monitor", "status"),
)


def clip_text(value: str, limit: int = 240) -> str:
    text = " ".join((value or "").strip().split())
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 3)].rstrip() + "..."


def is_read_only_action(action: str) -> bool:
    try:
        tokens = tuple(shlex.split((action or "").strip()))
    except ValueError:
        return False
    return any(
        len(tokens) >= len(prefix) and tokens[: len(prefix)] == prefix
        for prefix in _READ_ONLY_COMMAND_PREFIXES
    )


def _history_bucket(action: str) -> str | None:
    try:
        tokens = tuple(shlex.split((action or "").strip()))
    except ValueError:
        return None
    if len(tokens) >= 2 and tokens[:2] in {
        ("weather", "get"),
        ("weather", "forecast"),
        ("weather", "alerts"),
    }:
        return "weather"
    if len(tokens) >= 2 and tokens[:2] in {
        ("calendar", "today"),
        ("calendar", "list"),
    }:
        return "calendar"
    if len(tokens) >= 2 and tokens[:2] in {
        ("tasks", "list"),
        ("tasks", "search"),
    }:
        return "tasks"
    if len(tokens) >= 3 and tokens[:3] == ("openclaw", "cron", "list"):
        return "cron"
    if (
        len(tokens) >= 4
        and tokens[:3] == ("openclaw", "config", "get")
        and tokens[3] == "agent.model"
    ):
        return "config"
    if len(tokens) >= 2 and tokens[:2] in {
        ("email", "list"),
        ("email", "read"),
        ("email", "search"),
    }:
        return "email"
    if len(tokens) >= 3 and tokens[:3] in {
        ("openclaw", "channels", "list"),
        ("openclaw", "channels", "status"),
    }:
        return "channels"
    return None


def _format_history_fact(
    item: dict[str, Any],
    *,
    stdout_limit: int,
    stderr_limit: int,
    include_exit: bool = False,
) -> str:
    stdout = clip_text(item.get("stdout", ""), limit=stdout_limit) or "(empty)"
    stderr = clip_text(item.get("stderr", ""), limit=stderr_limit) or "(none)"
    text = f"{item['action']} => stdout={stdout}"
    if item.get("stderr"):
        text += f"; stderr={stderr}"
    elif include_exit or item.get("exit_code", 0) != 0:
        text += f"; stderr={stderr}"
    if include_exit:
        text += f"; exit={item.get('exit_code', 0)}"
    return text


def build_memory_summary(
    history: list[dict[str, Any]],
    *,
    compact: bool = False,
) -> str:
    if not history:
        return ""

    latest_by_bucket: dict[str, dict[str, Any]] = {}
    recent_state_changes: list[dict[str, Any]] = []
    last_failed: dict[str, Any] | None = None

    for item in history:
        bucket = _history_bucket(item["action"])
        if bucket:
            latest_by_bucket[bucket] = item
        if item.get("exit_code", 0) != 0:
            last_failed = item
        if not is_read_only_action(item["action"]) and item["action"].upper() != "DONE":
            recent_state_changes.append(item)

    facts: list[str] = []
    bucket_order = ["weather", "calendar", "tasks", "cron", "config", "email", "channels"]
    stdout_limit = 100 if compact else 160
    stderr_limit = 80 if compact else 120

    for bucket in bucket_order:
        item = latest_by_bucket.get(bucket)
        if item:
            facts.append(
                _format_history_fact(
                    item,
                    stdout_limit=stdout_limit,
                    stderr_limit=stderr_limit,
                )
            )

    if recent_state_changes:
        label = "recent state-changing action" if compact else "last state-changing action"
        keep = 1 if compact else 2
        for item in recent_state_changes[-keep:]:
            facts.append(
                f"{label}: "
                + _format_history_fact(
                    item,
                    stdout_limit=stdout_limit,
                    stderr_limit=stderr_limit,
                )
            )
            label = "recent state-changing action"

    if last_failed is not None:
        facts.append(
            "last failed action: "
            + _format_history_fact(
                last_failed,
                stdout_limit=stdout_limit,
                stderr_limit=stderr_limit,
                include_exit=True,
            )
        )

    if compact and len(facts) > 6:
        facts = facts[:6]
    if not facts:
        return ""
    return "Known context:\n" + "\n".join(f"- {fact}" for fact in facts)


def build_openai_request_messages(
    messages: list[dict[str, str]],
    history: list[dict[str, Any]],
    *,
    recent_tail_messages: int = 8,
) -> list[dict[str, str]]:
    if not messages:
        return []
    head = messages[:1]
    tail = messages[1:]
    if len(tail) > recent_tail_messages:
        tail = tail[-recent_tail_messages:]
    summary = build_memory_summary(history)
    if not summary and len(messages) <= recent_tail_messages + 1:
        return list(messages)
    request_messages = list(head)
    if summary:
        request_messages.append({"role": "user", "content": summary})
    request_messages.extend(tail)
    return request_messages
