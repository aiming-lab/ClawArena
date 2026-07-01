"""SessionHistory 工具——让 main agent 读取本 agent 的其它（历史）session 记录。

仿 openclaw：一个 agent 可有多条 session，main agent 能跨 session 回看历史对话。
实际读取由 :class:`clawarena.native.agent.session_history.SessionHistoryStore` 完成；
本工具只把 (action, session_id) 转交给它。仅 main agent 持有 ``ctx.session_history``，
subagent 处为 None，从而自动不可用。
"""
from __future__ import annotations

from typing import Any

from .base import BaseTool, ToolContext, ToolExecResult

_TOOL_DESCRIPTION = (
    "Read message transcripts from this agent's OTHER sessions. This agent may own "
    "several sessions (the current one plus pre-existing history sessions from other "
    "channels / earlier timelines); use this to recall what happened in those.\n\n"
    "Usage:\n"
    "- action='list' (default): list the available history sessions with their "
    "channel and message count.\n"
    "- action='read': return the user/assistant/tool_result transcript of the session "
    "named by `session_id` (must be one of the listed history sessions).\n"
    "You can only read sessions registered for this agent; the current active session "
    "is not re-readable through this tool."
)


class SessionHistoryTool(BaseTool):
    name = "SessionHistory"

    @classmethod
    def schema(cls, **_: Any) -> dict[str, Any]:
        return {
            "name": cls.name,
            "description": _TOOL_DESCRIPTION,
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["list", "read"],
                        "description": "'list' the history sessions or 'read' one of them.",
                    },
                    "session_id": {
                        "type": "string",
                        "description": "Required when action='read': the history session to read.",
                    },
                },
                "required": [],
            },
        }

    async def run(self, args: dict[str, Any], ctx: ToolContext) -> ToolExecResult:
        store = getattr(ctx, "session_history", None)
        if store is None:
            return ToolExecResult(
                "SessionHistory is unavailable for this agent.", is_error=True
            )
        ctx.tools_used.add(self.name)
        action = (args.get("action") or "list").strip()
        if action == "list":
            entries = store.list_history()
            if not entries:
                return ToolExecResult("No history sessions are available for this agent.")
            lines = ["Available history sessions:"]
            for e in entries:
                lines.append(
                    f"  - session_id={e['session_id']}  channel={e['channel']}  "
                    f"messages={e['messages']}"
                )
            lines.append(
                "\nUse SessionHistory(action='read', session_id=<one of the above>) to read it."
            )
            return ToolExecResult("\n".join(lines))
        if action == "read":
            session_id = (args.get("session_id") or "").strip()
            if not session_id:
                return ToolExecResult(
                    "session_id is required when action='read'.", is_error=True
                )
            return ToolExecResult(store.read_session(session_id))
        return ToolExecResult(
            f"unknown action {action!r}; valid: 'list' | 'read'", is_error=True
        )
