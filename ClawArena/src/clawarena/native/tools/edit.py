"""Edit tool: 受 read-before-edit 约束的精确替换。"""
from __future__ import annotations

from typing import Any

from ..prompts import READ_BEFORE_EDIT_MESSAGE, TOOL_DESCRIPTIONS
from ..sandbox import ForbiddenPathError
from ._helpers import forbidden, params, require_absolute
from .base import BaseTool, ToolContext, ToolExecResult


class EditTool(BaseTool):
    name = "Edit"
    description = TOOL_DESCRIPTIONS["Edit"]

    @classmethod
    def schema(cls, **_: Any) -> dict[str, Any]:
        p = params("Edit")
        return {
            "name": cls.name,
            "description": cls.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": p["file_path"]},
                    "old_string": {"type": "string", "description": p["old_string"]},
                    "new_string": {"type": "string", "description": p["new_string"]},
                    "replace_all": {
                        "type": "boolean",
                        "default": False,
                        "description": p["replace_all"],
                    },
                },
                "required": ["file_path", "old_string", "new_string"],
            },
        }

    async def run(self, args: dict[str, Any], ctx: ToolContext) -> ToolExecResult:
        raw = args.get("file_path", "")
        old_s = args.get("old_string", "")
        new_s = args.get("new_string", "")
        replace_all = bool(args.get("replace_all", False))
        resolved = require_absolute(raw)
        if isinstance(resolved, ToolExecResult):
            return resolved
        try:
            real = ctx.scope.check(resolved)
        except ForbiddenPathError:
            return forbidden(raw)
        if not real.exists():
            return ToolExecResult(f"file not found: {raw}", is_error=True)
        if not ctx.read_tracker.can_modify(real):
            return ToolExecResult(READ_BEFORE_EDIT_MESSAGE.format(path=raw), is_error=True)
        text = real.read_text(encoding="utf-8", errors="replace")
        if old_s not in text:
            return ToolExecResult(f"edit error: old_string not found in {raw}", is_error=True)
        if not replace_all and text.count(old_s) > 1:
            return ToolExecResult(
                f"edit error: old_string is ambiguous ({text.count(old_s)} matches) in {raw}; "
                "provide more surrounding context or set replace_all=true.",
                is_error=True,
            )
        new_text = text.replace(old_s, new_s) if replace_all else text.replace(old_s, new_s, 1)
        real.write_text(new_text, encoding="utf-8")
        ctx.tools_used.add(self.name)
        ctx.read_tracker.record_read(real)
        return ToolExecResult(f"edited {raw}")
