"""ZeroClaw engine — CLI subprocess (Rust binary).

Key adaptations for GPT-compatible endpoints:
- ANSI log stripping (ZeroClaw outputs tracing logs to stdout)
- ZEROCLAW_WORKSPACE isolation (per-agent workspace with project files)
- --session-state-file (cross-round conversation resume via interactive mode)
- API key passthrough (ZEROCLAW_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY)

Session continuity: ZeroClaw's ``-m`` (single-message) mode does NOT support
``--session-state-file``.  Session load/save only happens in interactive mode.
We therefore launch zeroclaw in interactive mode (without ``-m``), pipe the
message via stdin, and close stdin to trigger a clean exit after one turn.

Critical config requirement: ZeroClaw's history_pruner collapses
assistant(tool_calls)+tool_result pairs into plain text, breaking
tool_call_id alignment. GPT APIs then reject orphaned tool messages.
Fix: set [agent.history_pruning] enabled = false in config.toml.
"""

from __future__ import annotations

import asyncio
import os
import re
from pathlib import Path

from clawarena.core.types import AgentResult, WorkCopy
from clawarena.engines.cli_subprocess import CLISubprocessEngine

_ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')


def _clean_output(text: str) -> str:
    """Strip ZeroClaw interactive chrome, tracing logs, and ANSI codes.

    Interactive-mode stdout layout (message piped via stdin)::

        🦀 ZeroClaw Interactive Mode\\n
        Type /help for commands.\\n
        \\n
        > response line 1\\n      ← prompt prefix glued to first response line
        response line 2\\n
        >                         ← next prompt before EOF exit
    """
    text = _ANSI_RE.sub('', text)
    lines = text.split('\n')
    clean: list[str] = []
    for line in lines:
        stripped = line.strip()
        # Strip leading prompt so downstream checks see raw content
        content = stripped.lstrip('> ')
        # Skip tracing timestamp lines (e.g. "2026-04-04 …")
        if content[:5].replace('-', '').isdigit() and len(content) > 10:
            continue
        # Skip interactive-mode header lines
        if stripped.startswith('\U0001f980') or stripped.startswith('Type /help'):
            continue
        # Skip standalone prompt lines (just "> " with nothing after)
        if stripped == '>' or stripped == '> ':
            continue
        clean.append(line)
    result = '\n'.join(clean).strip()
    # The first content line may start with "> " (prompt prefix glued to
    # the response because print!("> ") has no newline).  Strip it once.
    if result.startswith('> '):
        result = result[2:]
    return result


class ZeroClawEngine(CLISubprocessEngine):
    """ZeroClaw engine using interactive mode with stdin pipe.

    Instead of ``-m``, we launch ``zeroclaw agent --session-state-file <path>``
    in interactive mode.  The user message is written to stdin, then stdin is
    closed so zeroclaw sees EOF and exits after saving the session state.
    This allows multi-round conversation continuity across clawarena rounds.
    """

    async def run_agent(
        self,
        session_id: str,
        message: str,
        work_copy: WorkCopy,
        agent_id: str | None = None,
        gateway_port: int | None = None,
        timeout: float | None = None,
        extra_env: dict[str, str] | None = None,
    ) -> AgentResult:
        cmd = self.build_agent_cmd(session_id, message)
        env = {
            **os.environ,
            **self.build_env(work_copy, gateway_port, agent_id),
            **(extra_env or {}),
        }
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            env=env,
            cwd=str(self.build_cwd(work_copy, agent_id)),
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(input=message.encode() + b'\n'),
                timeout=timeout,
            )
        except asyncio.TimeoutError:
            proc.kill()
            await proc.communicate()
            return AgentResult(
                status="timeout",
                answer="",
                error=f"Timeout after {timeout}s",
                returncode=-1,
                llm_log=None,
            )
        answer = _clean_output(stdout.decode())
        return AgentResult(
            status="success" if proc.returncode == 0 else "failed",
            answer=answer,
            error=stderr.decode() if proc.returncode != 0 else None,
            returncode=proc.returncode,
            llm_log=None,
        )

    def build_cwd(self, work_copy: WorkCopy, agent_id: str | None) -> Path:
        if work_copy.workspace_root and agent_id:
            ws = work_copy.workspace_root / agent_id
            if ws.exists():
                return ws
        return work_copy.project_root

    def build_agent_cmd(self, session_id: str, message: str) -> list[str]:
        """Build command for interactive mode (message is sent via stdin)."""
        cmd = ["zeroclaw", "agent"]
        if session_id:
            cmd.extend(["--session-state-file", session_id])
        return cmd

    def build_env(
        self, work_copy: WorkCopy, gateway_port: int | None,
        agent_id: str | None = None,
    ) -> dict[str, str]:
        cc = work_copy.extra.get("zeroclaw_config", {})
        env: dict[str, str] = {}

        # Set ZEROCLAW_WORKSPACE so zeroclaw resolves the agent directory as
        # its workspace.  The parent .zeroclaw/config.toml triggers legacy
        # layout where workspace_dir == the ZEROCLAW_WORKSPACE value (no
        # /workspace suffix), giving the agent access to project/, archive/
        # etc. alongside workspace/.
        eid = agent_id or work_copy.extra.get("current_agent_id")
        if work_copy.workspace_root and eid:
            ws = work_copy.workspace_root / eid
            if ws.exists():
                env["ZEROCLAW_WORKSPACE"] = str(ws.resolve())

        if gateway_port is not None:
            env["ZEROCLAW_GATEWAY_PORT"] = str(gateway_port)

        for key in ("ZEROCLAW_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY"):
            val = os.environ.get(key)
            if val:
                env[key] = val
        env.update(cc.get("env", {}))
        return env

    def build_gateway_cmd(
        self, work_copy: WorkCopy, port: int
    ) -> list[str] | None:
        cc = work_copy.extra.get("zeroclaw_config", {})
        if not cc.get("gateway_enabled", False):
            return None
        return ["zeroclaw", "gateway", "--port", str(port)]
