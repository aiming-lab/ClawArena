"""Bash tool: 配额受 ``bash.*`` 配置驱动，前缀禁用与 ``.git/`` 黑名单互补。"""
from __future__ import annotations

import asyncio
import shlex
from typing import Any

from ..prompts import FORBIDDEN_COMMAND_MESSAGE, TOOL_DESCRIPTIONS
from ._helpers import params
from .base import BaseTool, ToolContext, ToolExecResult


def _first_token(command: str) -> str:
    """提取命令首 token，用于前缀禁用判断。"""
    try:
        toks = shlex.split(command, posix=True)
    except ValueError:
        toks = command.strip().split()
    if not toks:
        return ""
    # 处理形如 ``ENV=VAR git status``：跳过 KEY=VAL 形式的环境变量赋值。
    for tok in toks:
        if "=" in tok and tok.split("=", 1)[0].replace("_", "").isalnum():
            continue
        return tok
    return toks[-1]


class BashTool(BaseTool):
    name = "Bash"
    description = TOOL_DESCRIPTIONS["Bash"]

    @classmethod
    def schema(cls, **format_kwargs: Any) -> dict[str, Any]:
        p = params("Bash")
        default_timeout_ms = int(format_kwargs.get("bash_default_timeout_ms", 120000))
        desc = TOOL_DESCRIPTIONS["Bash"].format(default_timeout_ms=default_timeout_ms)
        return {
            "name": cls.name,
            "description": desc,
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": p["command"]},
                    "description": {"type": "string", "description": p["description"]},
                    "timeout": {"type": "number", "description": p["timeout"]},
                },
                "required": ["command", "description"],
            },
        }

    async def run(self, args: dict[str, Any], ctx: ToolContext) -> ToolExecResult:
        command = args.get("command", "")
        forbidden_prefixes = ctx.config.get("bash.forbidden_prefixes", ["git"]) or []
        head = _first_token(command).strip()
        base = head.rsplit("/", 1)[-1]  # 处理 ``/usr/bin/git`` 这种情况
        for prefix in forbidden_prefixes:
            if base == prefix or head.startswith(prefix + " ") or head == prefix:
                return ToolExecResult(
                    FORBIDDEN_COMMAND_MESSAGE.format(prefix=prefix), is_error=True
                )
        default_ms = int(ctx.config.get("bash.default_timeout_ms", 120000))
        timeout_ms = int(args.get("timeout", default_ms))
        timeout_ms = max(1, min(timeout_ms, 600000))
        timeout_sec = timeout_ms / 1000.0
        max_bytes = int(ctx.config.get("bash.max_output_bytes", 65536))

        proc = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(ctx.cwd),
        )
        try:
            stdout_b, stderr_b = await asyncio.wait_for(proc.communicate(), timeout=timeout_sec)
        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
            return ToolExecResult(f"bash timeout after {timeout_ms}ms", is_error=True)
        ctx.tools_used.add(self.name)
        stdout = stdout_b[:max_bytes].decode("utf-8", errors="replace")
        stderr = stderr_b[:max_bytes].decode("utf-8", errors="replace")
        rc = proc.returncode if proc.returncode is not None else -1
        payload = f"exit={rc}\n--- stdout ---\n{stdout}\n--- stderr ---\n{stderr}"
        return ToolExecResult(payload, is_error=rc != 0)
