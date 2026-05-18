"""Nanobot engine — CLI subprocess (Python binary) with -w/-c flags."""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

from clawarena.core.types import AgentResult, WorkCopy
from clawarena.engines.base import AgentEngine
from clawarena.engines.output_sanitizer import normalize_agent_output
from clawarena.utils import get_project_root

_NANOBOT_RUNNER = get_project_root() / "helpers" / "nanobot_runner.py"


class NanobotEngine(AgentEngine):
    """Nanobot engine using ``nanobot_runner.py agent -m`` CLI.

    Invokes nanobot via helpers/nanobot_runner.py instead of the bare
    ``nanobot`` entry point so that compatibility patches (e.g. stripping
    the legacy ``max_tokens`` field) can be applied without modifying
    nanobot source.

    Inherits AgentEngine directly (not CLISubprocessEngine) because
    nanobot requires ``-w`` and ``-c`` flags that need access to
    work_copy, which is unavailable in ``build_agent_cmd``.
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
        cc = work_copy.extra.get("nanobot_config", {})
        workspace_path = self._resolve_workspace(work_copy, agent_id or "")

        cmd = [sys.executable, str(_NANOBOT_RUNNER), "agent", "-m", message, "--no-markdown"]
        if session_id:
            cmd.extend(["-s", session_id])
        if workspace_path:
            cmd.extend(["-w", str(workspace_path)])
        cfg_path = None
        if extra_env and extra_env.get("NANOBOT_CONFIG"):
            cfg_path = Path(extra_env["NANOBOT_CONFIG"])
        elif work_copy.config_path:
            cfg_path = work_copy.config_path
        if cfg_path:
            cmd.extend(["-c", str(cfg_path)])

        env = {
            **os.environ,
            **(cc.get("env") or {}),
            **(extra_env or {}),
            "CLAWARENA_NANOBOT_NO_MAX_TOKENS": "1",
        }
        if log_dir := work_copy.extra.get("log_dir"):
            env["CLAWARENA_NANOBOT_LOG_DIR"] = str(log_dir)

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            env=env,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(workspace_path) if workspace_path else None,
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
        stdout_text = stdout.decode().strip()
        stderr_text = stderr.decode().strip()
        answer_text, detected_error = normalize_agent_output(stdout_text, framework="nanobot")
        status = "success" if proc.returncode == 0 else "failed"
        error_text = stderr_text if proc.returncode != 0 else None
        if proc.returncode == 0 and detected_error:
            status = "failed"
            error_text = detected_error

        return AgentResult(
            status=status,
            answer=answer_text,
            error=error_text,
            returncode=proc.returncode,
            llm_log=None,
        )

    @staticmethod
    def _resolve_workspace(work_copy: WorkCopy, agent_id: str) -> Path | None:
        if work_copy.workspace_root and agent_id:
            ws = work_copy.workspace_root / agent_id
            if ws.exists():
                return ws
        return work_copy.workspace_root
