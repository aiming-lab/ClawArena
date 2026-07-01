"""Write tool: 受 read-before-edit 与 sandbox 双重约束的纯文本写入。"""
from __future__ import annotations

from typing import Any

from ..prompts import READ_BEFORE_EDIT_MESSAGE, TOOL_DESCRIPTIONS
from ..sandbox import ForbiddenPathError
from ._helpers import forbidden, params, require_absolute
from .base import BaseTool, ToolContext, ToolExecResult


class WriteTool(BaseTool):
    name = "Write"
    description = TOOL_DESCRIPTIONS["Write"]

    @classmethod
    def schema(cls, **_: Any) -> dict[str, Any]:
        p = params("Write")
        return {
            "name": cls.name,
            "description": cls.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": p["file_path"]},
                    "content": {"type": "string", "description": p["content"]},
                },
                "required": ["file_path", "content"],
            },
        }

    async def run(self, args: dict[str, Any], ctx: ToolContext) -> ToolExecResult:
        raw = args.get("file_path", "")
        content = args.get("content", "")
        resolved = require_absolute(raw)
        if isinstance(resolved, ToolExecResult):
            return resolved
        try:
            real = ctx.scope.check(resolved)
        except ForbiddenPathError:
            return forbidden(raw)
        if real.exists() and not ctx.read_tracker.can_modify(real):
            return ToolExecResult(READ_BEFORE_EDIT_MESSAGE.format(path=raw), is_error=True)
        real.parent.mkdir(parents=True, exist_ok=True)
        try:
            real.write_text(content, encoding="utf-8")
        except OSError as e:
            return ToolExecResult(f"write error: {e}", is_error=True)
        ctx.tools_used.add(self.name)
        ctx.read_tracker.record_read(real)
        return ToolExecResult(f"wrote {len(content)} chars to {raw}")
