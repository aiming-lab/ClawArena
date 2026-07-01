"""Shared base for CLI-subprocess-based engines."""

from __future__ import annotations

import asyncio
import os
from abc import abstractmethod
from pathlib import Path

from clawarena.core.types import AgentResult, GatewayHandle, NoOpGatewayHandle, WorkCopy
from clawarena.engines.output_sanitizer import normalize_agent_output

from .base import AgentEngine


class CLISubprocessEngine(AgentEngine):
    """Base class for frameworks invoked via CLI subprocess."""

    @staticmethod
    async def _capture_stream(
        stream: asyncio.StreamReader | None, sink: list[str],
    ) -> None:
        """Continuously drain a subprocess stream into an in-memory buffer."""
        if stream is None:
            return
        while True:
            chunk = await stream.read(4096)
            if not chunk:
                return
            sink.append(chunk.decode("utf-8", errors="replace"))

    @abstractmethod
    def build_agent_cmd(self, session_id: str, message: str) -> list[str]:
        """Build the command-line arguments for running the agent."""

    @abstractmethod
    def build_env(
        self, work_copy: WorkCopy, gateway_port: int | None
    ) -> dict[str, str]:
        """Build extra environment variables for the subprocess."""

    def build_gateway_cmd(
        self, work_copy: WorkCopy, port: int
    ) -> list[str] | None:
        """Build gateway command. Return None if not needed."""
        return None

    def build_gateway_env(
        self, work_copy: WorkCopy, port: int
    ) -> dict[str, str]:
        """Build extra environment variables for the gateway subprocess."""
        return self.build_env(work_copy, port)

    def build_cwd(self, work_copy: WorkCopy, agent_id: str | None) -> Path:
        """Return the working directory for the agent subprocess.

        Defaults to project_root.  Override in subclasses that need the
        agent workspace as CWD so that relative file paths resolve correctly.
        """
        return work_copy.project_root

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
        env = {**os.environ, **self.build_env(work_copy, gateway_port),
               **(extra_env or {})}
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            env=env,
            cwd=str(self.build_cwd(work_copy, agent_id)),
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
                llm_log=None,
            )
        stdout_text = stdout.decode().strip()
        stderr_text = stderr.decode().strip()
        answer_text, detected_error = normalize_agent_output(stdout_text)
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

    async def start_gateway(
        self, work_copy: WorkCopy, port: int
    ) -> GatewayHandle:
        cmd = self.build_gateway_cmd(work_copy, port)
        if cmd is None:
            return NoOpGatewayHandle()
        env = {**os.environ, **self.build_gateway_env(work_copy, port)}
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            env=env,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        handle = GatewayHandle(process=proc, port=port)
        handle.stdout_task = asyncio.create_task(
            self._capture_stream(proc.stdout, handle.stdout_chunks),
        )
        handle.stderr_task = asyncio.create_task(
            self._capture_stream(proc.stderr, handle.stderr_chunks),
        )
        return handle
