"""Glob tool: 走 :meth:`pathlib.Path.glob`，按 mtime 倒序，受 scope 过滤。"""
from __future__ import annotations

from typing import Any

from ..prompts import TOOL_DESCRIPTIONS
from ..sandbox import ForbiddenPathError
from ._helpers import forbidden, params, require_absolute
from .base import BaseTool, ToolContext, ToolExecResult


class GlobTool(BaseTool):
    name = "Glob"
    description = TOOL_DESCRIPTIONS["Glob"]

    @classmethod
    def schema(cls, **_: Any) -> dict[str, Any]:
        p = params("Glob")
        return {
            "name": cls.name,
            "description": cls.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": p["pattern"]},
                    "path": {"type": "string", "description": p["path"]},
                },
                "required": ["pattern"],
            },
        }

    async def run(self, args: dict[str, Any], ctx: ToolContext) -> ToolExecResult:
        pattern = args.get("pattern", "")
        raw_path = args.get("path")
        if raw_path is None:
            real = ctx.cwd
        else:
            resolved = require_absolute(raw_path)
            if isinstance(resolved, ToolExecResult):
                return resolved
            try:
                real = ctx.scope.check(resolved)
            except ForbiddenPathError:
                return forbidden(raw_path)
        if not real.exists():
            return ToolExecResult("(no matches)")

        candidates = [p for p in real.glob(pattern) if ctx.scope.is_allowed(p)]
        candidates.sort(key=lambda p: p.stat().st_mtime if p.exists() else 0.0, reverse=True)
        ctx.tools_used.add(self.name)
        if not candidates:
            return ToolExecResult("(no matches)")
        return ToolExecResult("\n".join(str(p) for p in candidates[:1000]))
