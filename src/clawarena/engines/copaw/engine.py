"""CoPaw engine — HTTP API with managed server lifecycle."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import Any

from clawarena.core.types import AgentResult, GatewayHandle, WorkCopy
from clawarena.engines.base import AgentEngine


class CoPawEngine(AgentEngine):
    """CoPaw engine using ``copaw app`` server + HTTP API.

    CoPaw is the only framework that **requires** a running web server.
    ``start_gateway`` launches ``copaw app``, ``wait_for_gateway`` polls
    the health endpoint, and ``run_agent`` sends messages via HTTP POST.

    Session IDs are created by the server on first call and cached
    internally for subsequent rounds (similar to OpenCode).
    """

    def __init__(self) -> None:
        self._session_map: dict[str, str] = {}

    async def start_gateway(
        self, work_copy: WorkCopy, port: int
    ) -> GatewayHandle:
        """Launch ``copaw app`` server."""
        cc = work_copy.extra.get("copaw_config", {})
        env = {
            **os.environ,
            "COPAW_WORKING_DIR": str(work_copy.state_dir),
            **(cc.get("env") or {}),
        }
        cmd = ["copaw", "app", "--port", str(port)]
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            env=env,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        return GatewayHandle(process=proc, port=port)

    async def wait_for_gateway(
        self, handle: GatewayHandle, timeout: float = 30.0
    ) -> None:
        """Poll health endpoint until CoPaw server is ready."""
        import aiohttp

        deadline = asyncio.get_event_loop().time() + timeout
        while asyncio.get_event_loop().time() < deadline:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"http://127.0.0.1:{handle.port}/api/health"
                    ) as resp:
                        if resp.status == 200:
                            return
            except Exception:
                await asyncio.sleep(0.5)
        raise RuntimeError(
            f"CoPaw server on port {handle.port} did not become ready"
        )

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
        import aiohttp

        cc = work_copy.extra.get("copaw_config", {})
        from_agent = cc.get("from_agent", "benchmark")
        to_agent = agent_id or cc.get("to_agent", "default")

        # Use cached session if available
        effective_session = self._session_map.get(
            agent_id or "", session_id
        )

        url = f"http://127.0.0.1:{gateway_port}/api/agent/process"
        payload: dict[str, Any] = {
            "from_agent": from_agent,
            "to_agent": to_agent,
            "text": message,
        }
        if effective_session:
            payload["session_id"] = effective_session

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=timeout),
                ) as resp:
                    data = await resp.json()
                    answer = data.get("response", data.get("text", ""))
                    new_session_id = data.get("session_id", "")

                    # Cache session ID for subsequent rounds
                    if new_session_id and agent_id:
                        self._session_map[agent_id] = new_session_id

                    llm_log = {
                        "agentId": agent_id or "",
                        "sessionId": new_session_id or effective_session or "",
                        "success": resp.status == 200,
                        "response": data,
                    }

                    return AgentResult(
                        status="success" if resp.status == 200 else "failed",
                        answer=answer,
                        error=data.get("error") if resp.status != 200 else None,
                        raw=data,
                        llm_log=llm_log,
                    )
        except asyncio.TimeoutError:
            return AgentResult(
                status="timeout",
                answer="",
                error=f"Timeout after {timeout}s",
            )
        except Exception as e:
            return AgentResult(
                status="failed",
                answer="",
                error=str(e),
            )

    @staticmethod
    def _resolve_workspace(work_copy: WorkCopy, agent_id: str) -> Path | None:
        if work_copy.workspace_root and agent_id:
            ws = work_copy.workspace_root / agent_id
            if ws.exists():
                return ws
        return work_copy.workspace_root
