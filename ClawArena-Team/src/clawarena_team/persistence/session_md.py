"""Render a session timeline into human-readable Markdown.

Output path: ``<scenario_out>/session_<owner>.md``, **not** under a round
subdirectory, because a single session may accumulate messages across multiple
rounds.

Rendering principles (aligned with claude-code's user-facing interface):
**render the conversation content only**; do not show statistical fields such as
token counts, provider raw_usage, or UsageRecord. Billing/reconciliation
information always lives in the same-named ``.jsonl`` (the machine-readable data
stream).

Concrete rules:
- The header shows the owner and system_prompt (**system_prompt is not truncated**);
- each turn is rendered as ``## Turn N — <role>``;
- in an ``assistant`` turn, tool_calls are listed as ``### Tool Call: <name>``,
  and each argument value, if it is a string longer than ``MAX_INLINE_CHARS``
  (default 300), is truncated;
- the content of ``tool_result`` and ``user`` turns is likewise truncated past
  ``MAX_INLINE_CHARS``;
- truncation appends a ``…[truncated N chars]`` annotation.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

MAX_INLINE_CHARS = 300


def _truncate(s: str, *, limit: int = MAX_INLINE_CHARS) -> str:
    if not isinstance(s, str):
        s = str(s)
    if len(s) <= limit:
        return s
    return f"{s[:limit]}…[truncated {len(s) - limit} chars]"


def _fmt_value(v: Any, *, limit: int = MAX_INLINE_CHARS) -> str:
    if isinstance(v, str):
        return _truncate(v, limit=limit)
    if isinstance(v, (int, float, bool)) or v is None:
        return repr(v)
    try:
        serialized = json.dumps(v, ensure_ascii=False)
    except (TypeError, ValueError):
        serialized = str(v)
    return _truncate(serialized, limit=limit)


def _render_tool_call(tc: dict[str, Any]) -> list[str]:
    name = tc.get("name", "?")
    args = tc.get("arguments") or {}
    lines = [f"### Tool Call: `{name}`"]
    if isinstance(args, dict):
        if not args:
            lines.append("_(no arguments)_")
        for k, v in args.items():
            lines.append(f"- **{k}**: `{_fmt_value(v)}`")
    else:
        lines.append(f"_arguments_: `{_fmt_value(args)}`")
    return lines


def _render_turn(idx: int, turn: dict[str, Any]) -> list[str]:
    role = turn.get("role", "?")
    lines = [f"## Turn {idx} — {role}"]

    sys_reminders = turn.get("system_reminders") or []
    task_notes = turn.get("task_notifications") or []

    if role == "assistant":
        content = turn.get("content", "")
        if content:
            lines.append("**content**:")
            lines.append("")
            lines.append(_truncate(content))
            lines.append("")
        tool_calls = turn.get("tool_calls") or []
        for tc in tool_calls:
            lines.extend(_render_tool_call(tc))
            lines.append("")
    elif role == "tool_result":
        tcid = turn.get("tool_call_id", "")
        if tcid:
            lines.append(f"_tool_call_id_: `{tcid}`")
        content = turn.get("content", "")
        lines.append("")
        lines.append(_truncate(content))
        lines.append("")
    elif role == "user":
        content = turn.get("content", "") or ""
        if content:
            lines.append(_truncate(content))
            lines.append("")
    elif role == "system":
        return []
    else:
        lines.append(_truncate(turn.get("content", "")))
        lines.append("")

    # Out-of-band channels (any role may carry these): system-reminder / task-notification.
    for r in sys_reminders:
        lines.append(f"> _system-reminder_: {_truncate(r)}")
        lines.append("")
    for n in task_notes:
        lines.append(f"> _task-notification_: {_truncate(n)}")
        lines.append("")

    return lines


def render_session_md(
    owner: str,
    turns: Iterable[Any],
    *,
    system_prompt: str | None = None,
    header_meta: dict[str, Any] | None = None,
) -> str:
    """Render a single session to Markdown.

    ``turns`` may be a list of ``HarnessTurn`` objects or a list of dicts read
    from jsonl. ``system_prompt`` is **not truncated**.
    """
    out: list[str] = []
    out.append(f"# Session: {owner}")
    out.append("")
    if header_meta:
        for k, v in header_meta.items():
            out.append(f"- **{k}**: `{_fmt_value(v, limit=400)}`")
        out.append("")

    if system_prompt:
        out.append("## System Prompt")
        out.append("")
        out.append("```")
        out.append(system_prompt)
        out.append("```")
        out.append("")

    turn_dicts: list[dict[str, Any]] = []
    for t in turns:
        if isinstance(t, dict):
            turn_dicts.append(t)
            continue
        turn_dicts.append({
            "role": getattr(t, "role", "?"),
            "content": getattr(t, "content", ""),
            "tool_calls": list(getattr(t, "tool_calls", []) or []),
            "tool_call_id": getattr(t, "tool_call_id", None),
            "system_reminders": list(getattr(t, "system_reminders", []) or []),
            "task_notifications": list(getattr(t, "task_notifications", []) or []),
        })

    out.append("## Timeline")
    out.append("")
    rendered_turns = 0
    for t in turn_dicts:
        if t.get("role") == "system":
            continue
        rendered_turns += 1
        out.extend(_render_turn(rendered_turns, t))
    if rendered_turns == 0:
        out.append("_(no turns recorded)_")
        out.append("")
    return "\n".join(out)


def write_session_md(
    path: Path,
    *,
    owner: str,
    turns: Iterable[Any],
    system_prompt: str | None = None,
    header_meta: dict[str, Any] | None = None,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    md = render_session_md(
        owner, turns, system_prompt=system_prompt, header_meta=header_meta
    )
    path.write_text(md, encoding="utf-8")
