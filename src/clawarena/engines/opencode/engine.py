"""OpenCode engine — CLI subprocess with JSON event stream parsing."""

from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path

from clawarena.core.types import AgentResult, WorkCopy
from clawarena.engines.base import AgentEngine


class OpenCodeEngine(AgentEngine):
    """OpenCode engine using ``opencode run`` CLI with JSON output.

    OpenCode creates sessions at runtime.  The first invocation for each
    agent_id returns a ``sessionID`` in the JSON event stream, which is
    cached internally and reused for subsequent rounds via ``--session``.
    """

    def __init__(self) -> None:
        self._session_map: dict[str, str] = {}

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
        cc = work_copy.extra.get("opencode_config", {})
        workspace_path = self._resolve_workspace(work_copy, agent_id or "")

        # Use cached session if available
        effective_session = self._session_map.get(agent_id or "", session_id)

        cmd = ["opencode", "run", message, "--format", "json"]
        if effective_session:
            cmd.extend(["--session", effective_session])
        if cc.get("model"):
            cmd.extend(["--model", cc["model"]])
        if workspace_path:
            cmd.extend(["--dir", str(workspace_path)])

        env = {
            **os.environ,
            "XDG_CONFIG_HOME": str(work_copy.state_dir / "config"),
            "XDG_DATA_HOME": str(work_copy.state_dir / "data"),
            "XDG_CACHE_HOME": str(work_copy.state_dir / "cache"),
            "XDG_STATE_HOME": str(work_copy.state_dir / "state"),
            **(cc.get("env") or {}),
            **(extra_env or {}),
        }

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            env=env,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(), timeout=timeout
            )
        except asyncio.TimeoutError:
            proc.kill()
            await proc.communicate()
            return AgentResult(
                status="timeout",
                answer="",
                error=f"Timeout after {timeout}s",
                returncode=-1,
            )

        # Parse JSON event stream
        answer_parts: list[str] = []
        messages: list[dict] = []
        new_session_id: str | None = None

        for line in stdout.decode().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") == "text":
                text = event.get("part", {}).get("text", "")
                if text:
                    answer_parts.append(text)
            if not new_session_id:
                new_session_id = event.get("sessionID")
            messages.append(event)

        # Cache session ID for subsequent rounds
        if new_session_id and agent_id:
            self._session_map[agent_id] = new_session_id

        llm_log = {
            "agentId": agent_id or "",
            "sessionId": new_session_id or effective_session or "",
            "success": proc.returncode == 0,
            "messageCount": len(messages),
            "messages": messages,
        }

        return AgentResult(
            status="success" if proc.returncode == 0 else "failed",
            answer="\n".join(answer_parts),
            error=stderr.decode() if proc.returncode != 0 else None,
            returncode=proc.returncode,
            llm_log=llm_log,
        )

    @staticmethod
    def _resolve_workspace(work_copy: WorkCopy, agent_id: str) -> Path | None:
        if work_copy.workspace_root and agent_id:
            ws = work_copy.workspace_root / agent_id
            if ws.exists():
                return ws
        return work_copy.workspace_root
