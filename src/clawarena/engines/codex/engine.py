"""Codex engine — Python SDK (codex_app_server_sdk)."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

from clawarena.core.types import AgentResult, GatewayHandle, WorkCopy
from clawarena.engines.base import AgentEngine


class CodexEngine(AgentEngine):
    """Codex engine using codex-app-server Python SDK.

    The CodexClient is long-lived: initialized once in start_gateway,
    reused across all tests/rounds, and shut down in stop_gateway.
    Each test_id gets its own ThreadHandle (start_thread on first call,
    reuse handle on subsequent calls via chat_once).
    """

    def __init__(self) -> None:
        self._client: Any | None = None
        self._threads: dict[str, Any] = {}  # agent_id → ThreadHandle

    async def start_gateway(self, work_copy: WorkCopy, port: int) -> GatewayHandle:
        """Initialize the CodexClient instance."""
        from codex_app_server_sdk import CodexClient

        cc = work_copy.extra.get("codex_config", {})
        self._client = CodexClient.connect_stdio(
            cwd=str(work_copy.workspace_root) if work_copy.workspace_root else None,
            env={"CODEX_HOME": str(work_copy.state_dir), **(cc.get("env") or {})},
        )
        await self._client.start()
        return GatewayHandle(process=None, port=None)

    async def stop_gateway(self, handle: GatewayHandle) -> None:
        """Shut down the CodexClient instance."""
        if self._client is not None:
            client = self._client
            self._client = None
            self._threads.clear()
            await client.close()

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
        from codex_app_server_sdk import CodexError, ThreadConfig

        if self._client is None:
            return AgentResult(
                status="failed", answer="",
                error="CodexClient not initialized — start_gateway was not called",
            )

        cc = work_copy.extra.get("codex_config", {})
        workspace_path = self._resolve_workspace(work_copy, agent_id or "")
        cwd = str(workspace_path) if workspace_path else None
        test_key = agent_id or ""

        try:
            # First round for this test → start_thread; subsequent → reuse handle
            if test_key not in self._threads:
                config = ThreadConfig(
                    cwd=cwd,
                    model=cc.get("model"),
                    sandbox=cc.get("sandbox"),
                    approval_policy=cc.get("approval_policy"),
                )
                handle = await self._client.start_thread(config)
                self._threads[test_key] = handle

            handle = self._threads[test_key]

            if timeout:
                result = await asyncio.wait_for(
                    handle.chat_once(message), timeout=timeout,
                )
            else:
                result = await handle.chat_once(message)

            llm_log = self._build_llm_log(result, session_id, agent_id)

            return AgentResult(
                status="success",
                answer=result.final_text or "",
                raw=result,
                llm_log=llm_log,
            )
        except (asyncio.TimeoutError, TimeoutError):
            return AgentResult(
                status="timeout", answer="",
                error=f"Timeout after {timeout}s", returncode=-1,
            )
        except CodexError as e:
            return AgentResult(status="failed", answer="", error=str(e))
        except Exception as e:
            return AgentResult(status="failed", answer="", error=str(e))

    # ── helpers ──

    @staticmethod
    def _resolve_workspace(work_copy: WorkCopy, agent_id: str) -> Path | None:
        if work_copy.workspace_root and agent_id:
            ws = work_copy.workspace_root / agent_id
            if ws.exists():
                return ws
        return work_copy.workspace_root

    @staticmethod
    def _build_llm_log(result, session_id: str | None, agent_id: str | None) -> dict:
        events = result.raw_events or []
        log: dict = {
            "agentId": agent_id or "",
            "sessionId": session_id or "",
            "threadId": result.thread_id,
            "turnId": result.turn_id,
            "success": result.final_text is not None,
            "messageCount": len(events),
            "messages": events,
        }
        return log
