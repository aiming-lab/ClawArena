"""PicoClaw engine — CLI subprocess (Go binary)."""

from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path

from clawarena.core.types import AgentResult, WorkCopy
from clawarena.data_handlers.picoclaw.work_copy import (
    build_picoclaw_runtime_config,
    sync_security_yml,
)
from clawarena.engines.base import AgentEngine
from clawarena.engines.output_sanitizer import normalize_agent_output


class PicoClawEngine(AgentEngine):
    """PicoClaw engine using ``picoclaw agent -m`` CLI.

    PicoClaw outputs the agent reply as plain text on stdout.
    Session continuity is via ``-s session_key``.
    """

    def build_agent_cmd(self, session_id: str, message: str) -> list[str]:
        cmd = ["picoclaw", "agent", "-m", message]
        if session_id:
            cmd.extend(["-s", session_id])
        return cmd

    def build_cwd(self, work_copy: WorkCopy, agent_id: str | None) -> Path:
        """Use the agent's workspace dir as CWD so relative file paths resolve correctly."""
        if work_copy.workspace_root and agent_id:
            ws = work_copy.workspace_root / agent_id
            if ws.exists():
                return ws
        return work_copy.project_root

    def build_env(self, work_copy: WorkCopy) -> dict[str, str]:
        cc = work_copy.extra.get("picoclaw_config", {})
        env: dict[str, str] = {
            "PICOCLAW_HOME": str(work_copy.state_dir),
        }
        if work_copy.config_path:
            env["PICOCLAW_CONFIG"] = str(work_copy.config_path)
        env.update(cc.get("env", {}))
        return env

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
        env = {**os.environ, **self.build_env(work_copy), **(extra_env or {})}

        workspace_path = self.build_cwd(work_copy, agent_id)
        runtime_config = self._resolve_runtime_config(work_copy, workspace_path, env)
        if runtime_config is not None:
            env["PICOCLAW_CONFIG"] = str(runtime_config)

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            env=env,
            cwd=str(workspace_path),
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
        answer_text, detected_error = normalize_agent_output(stdout_text, framework="picoclaw")
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
    def _resolve_runtime_config(
        work_copy: WorkCopy,
        workspace_path: Path,
        env: dict[str, str],
    ) -> Path | None:
        source_cfg = env.get("PICOCLAW_CONFIG")
        cfg_path = Path(source_cfg) if source_cfg else work_copy.config_path
        if cfg_path is None or not cfg_path.exists():
            return None

        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        rewritten = build_picoclaw_runtime_config(cfg, workspace_path)

        target_dir = work_copy.state_dir / "agent_configs"
        target_dir.mkdir(parents=True, exist_ok=True)
        agent_cfg = target_dir / f"{workspace_path.name}.json"
        agent_cfg.write_text(
            json.dumps(rewritten, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        sync_security_yml(target_dir, source_dir=cfg_path.parent)
        return agent_cfg
