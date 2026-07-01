"""Grep tool: 委托给 ripgrep；参数模型贴合 claude-code 真实下发版本。"""
from __future__ import annotations

import asyncio
import shutil
from typing import Any

from ..prompts import TOOL_DESCRIPTIONS
from ..sandbox import ForbiddenPathError
from ._helpers import forbidden, params, require_absolute
from .base import BaseTool, ToolContext, ToolExecResult


class GrepTool(BaseTool):
    name = "Grep"
    description = TOOL_DESCRIPTIONS["Grep"]

    @classmethod
    def schema(cls, **_: Any) -> dict[str, Any]:
        p = params("Grep")
        return {
            "name": cls.name,
            "description": cls.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": p["pattern"]},
                    "path": {"type": "string", "description": p["path"]},
                    "glob": {"type": "string", "description": p["glob"]},
                    "type": {"type": "string", "description": p["type"]},
                    "output_mode": {
                        "type": "string",
                        "enum": ["content", "files_with_matches", "count"],
                        "description": p["output_mode"],
                    },
                    "-i": {"type": "boolean", "description": p["-i"]},
                    "-n": {"type": "boolean", "description": p["-n"]},
                    "-A": {"type": "number", "description": p["-A"]},
                    "-B": {"type": "number", "description": p["-B"]},
                    "-C": {"type": "number", "description": p["-C"]},
                    "head_limit": {"type": "number", "description": p["head_limit"]},
                    "offset": {"type": "number", "description": p["offset"]},
                    "multiline": {"type": "boolean", "description": p["multiline"]},
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

        rg = shutil.which("rg")
        if rg is None:
            return ToolExecResult("grep error: ripgrep (rg) is not installed", is_error=True)

        output_mode = args.get("output_mode", "files_with_matches")
        cmd = [rg, "--no-heading"]
        if output_mode == "content":
            show_n = args.get("-n", True)
            cmd.append("--with-filename")
            if show_n:
                cmd.append("-n")
            for flag, key in (("-A", "-A"), ("-B", "-B"), ("-C", "-C")):
                v = args.get(key)
                if v is not None:
                    cmd.extend([flag, str(int(v))])
        elif output_mode == "files_with_matches":
            cmd.append("-l")
        elif output_mode == "count":
            cmd.append("-c")
        else:
            return ToolExecResult(f"grep error: unknown output_mode {output_mode!r}", is_error=True)

        if args.get("-i"):
            cmd.append("-i")
        if args.get("multiline"):
            cmd.extend(["-U", "--multiline-dotall"])
        if args.get("glob"):
            cmd.extend(["--glob", args["glob"]])
        if args.get("type"):
            cmd.extend(["--type", args["type"]])

        cmd.append(pattern)
        cmd.append(str(real))

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(ctx.cwd),
        )
        stdout_b, stderr_b = await proc.communicate()
        ctx.tools_used.add(self.name)
        out = stdout_b.decode("utf-8", errors="replace")
        if not out and proc.returncode not in (0, 1) and stderr_b:
            return ToolExecResult(stderr_b.decode("utf-8", errors="replace"), is_error=True)

        lines = out.splitlines()
        offset = int(args.get("offset", 0) or 0)
        head = args.get("head_limit")
        if head is not None:
            lines = lines[offset : offset + int(head)]
        elif offset:
            lines = lines[offset:]
        if not lines:
            return ToolExecResult("(no matches)")
        return ToolExecResult("\n".join(lines))
