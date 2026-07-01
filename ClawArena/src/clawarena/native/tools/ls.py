"""LS 工具——结构化目录列表，给只有 Read/Grep/Glob 的子代理也能浏览文件系统。

参考 AutoHarness ``plugin/tools/ls.py`` 设计：

- ``path`` 必须是绝对路径或省略（默认 cwd / 当前 accessible_paths 的第一项）
- 目录后缀加 ``/``
- 默认显示 dot-files；``include_hidden=false`` 可跳过
- 受 ``ls.max_entries`` 上限保护（默认 1000）
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ..prompts import TOOL_DESCRIPTIONS, TOOL_PARAM_DESCRIPTIONS
from ..sandbox import ForbiddenPathError
from ._helpers import forbidden, require_absolute
from .base import BaseTool, ToolContext, ToolExecResult


class LSTool(BaseTool):
    name = "LS"

    @classmethod
    def schema(cls, **_: Any) -> dict[str, Any]:
        p = TOOL_PARAM_DESCRIPTIONS["LS"]
        return {
            "name": cls.name,
            "description": TOOL_DESCRIPTIONS["LS"],
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": p["path"]},
                    "include_hidden": {
                        "type": "boolean",
                        "default": True,
                        "description": p["include_hidden"],
                    },
                },
                "required": [],
            },
        }

    async def run(self, args: dict[str, Any], ctx: ToolContext) -> ToolExecResult:
        raw_path = args.get("path")
        if raw_path:
            resolved = require_absolute(raw_path)
            if isinstance(resolved, ToolExecResult):
                return resolved
            try:
                real = ctx.scope.check(resolved)
            except ForbiddenPathError:
                return forbidden(raw_path)
        else:
            real = ctx.cwd
        if not real.exists():
            return ToolExecResult(f"path not found: {real}", is_error=True)
        if not real.is_dir():
            return ToolExecResult(f"path is not a directory: {real}", is_error=True)
        include_hidden = bool(args.get("include_hidden", True))
        try:
            entries = sorted(
                real.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())
            )
        except OSError as exc:
            return ToolExecResult(f"listing error: {exc}", is_error=True)
        if not include_hidden:
            entries = [p for p in entries if not p.name.startswith(".")]
        # 同时尊重 scope 黑名单（如 .git / .arcbench）：让 is_allowed 过滤
        entries = [p for p in entries if ctx.scope.is_allowed(p)]
        max_entries = int(ctx.config.get("ls.max_entries", 1000))
        truncated = entries[:max_entries]
        if not truncated:
            ctx.tools_used.add(self.name)
            return ToolExecResult(f"[empty: {real}]")
        lines = [f"{p.name}/" if p.is_dir() else p.name for p in truncated]
        listing = "\n".join(lines)
        if len(entries) > max_entries:
            listing += f"\n[truncated to {max_entries} of {len(entries)} entries]"
        ctx.tools_used.add(self.name)
        return ToolExecResult(listing)
