"""OpenClaw engine — CLI subprocess runner."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

from clawarena.core.types import AgentResult, GatewayHandle, WorkCopy
from clawarena.engines.cli_subprocess import CLISubprocessEngine
from clawarena.utils import get_project_root


class OpenClawEngine(CLISubprocessEngine):
    """Engine for the OpenClaw framework."""

    @staticmethod
    def _format_gateway_failure(handle: GatewayHandle, reason: str) -> RuntimeError:
        detail = handle.debug_output().strip()
        if detail:
            return RuntimeError(
                f"Gateway on port {handle.port} {reason}\n\nCaptured gateway output:\n{detail}",
            )
        return RuntimeError(f"Gateway on port {handle.port} {reason}")

    def build_agent_cmd(
        self, session_id: str, message: str, agent_id: str | None = None
    ) -> list[str]:
        cmd = ["openclaw", "agent"]
        if agent_id:
            cmd += ["--agent", agent_id]
        cmd += ["--session-id", session_id, "--message", message]
        return cmd

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
        cmd = self.build_agent_cmd(session_id, message, agent_id=agent_id)
        if (extra_env or {}).get("OPENCLAW_LOCAL_MODE") == "1":
            cmd.append("--local")
        env = {
            **os.environ,
            **self.build_env(work_copy, gateway_port),
            **(extra_env or {}),
        }
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
        from clawarena.engines.output_sanitizer import normalize_agent_output
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

    def build_cwd(self, work_copy: WorkCopy, agent_id: str | None) -> Path:
        if agent_id and work_copy.workspace_root:
            candidate = work_copy.workspace_root / agent_id
            if candidate.exists():
                return candidate
        return super().build_cwd(work_copy, agent_id)

    def build_env(
        self, work_copy: WorkCopy, gateway_port: int | None
    ) -> dict[str, str]:
        benchmark_root = work_copy.project_root
        if not benchmark_root:
            benchmark_root = get_project_root()
        env: dict[str, str] = {
            "OPENCLAW_STATE_DIR": str(work_copy.state_dir),
            "BENCHMARK_ROOT": str(benchmark_root),
        }
        if work_copy.config_path:
            env["OPENCLAW_CONFIG_PATH"] = str(work_copy.config_path)
        if gateway_port is not None:
            env["OPENCLAW_GATEWAY_PORT"] = str(gateway_port)
        return env

    def build_gateway_cmd(
        self, work_copy: WorkCopy, port: int
    ) -> list[str] | None:
        return [
            "openclaw", "gateway", "run",
            "--port", str(port),
            "--allow-unconfigured",
        ]

    async def wait_for_gateway(
        self, handle: GatewayHandle, timeout: float = 120.0
    ) -> None:
        if handle.port is None:
            return
        deadline = asyncio.get_event_loop().time() + timeout
        while asyncio.get_event_loop().time() < deadline:
            if handle.process is not None and handle.process.returncode is not None:
                if handle.stdout_task is not None:
                    await handle.stdout_task
                if handle.stderr_task is not None:
                    await handle.stderr_task
                raise self._format_gateway_failure(
                    handle,
                    f"exited early with return code {handle.process.returncode}",
                )
            try:
                _, writer = await asyncio.wait_for(
                    asyncio.open_connection("127.0.0.1", handle.port),
                    timeout=0.5,
                )
                writer.close()
                await writer.wait_closed()
                return
            except Exception:
                await asyncio.sleep(0.2)
        raise self._format_gateway_failure(
            handle,
            f"did not become ready within {timeout:.1f}s",
        )
