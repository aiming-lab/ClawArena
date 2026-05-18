"""Abstract base class for agent engines."""

from __future__ import annotations

from abc import ABC, abstractmethod

from clawarena.core.types import (
    AgentResult, GatewayHandle, NoOpGatewayHandle,
    RoundContext, RoundResult, WorkCopy,
)


class AgentEngine(ABC):
    """Base class for all framework engines.

    Subclasses must implement run_agent(). They may also override
    on_round_complete() to inject framework-specific post-round logic
    (feedback override, score override, early termination, etc.).
    """

    @abstractmethod
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
        """Execute a single agent call.

        extra_env: per-invocation environment overrides (highest priority).
        Used by MetaClaw isolation mode to inject per-scene proxy env vars.
        """

    async def start_gateway(
        self, work_copy: WorkCopy, port: int
    ) -> GatewayHandle:
        """Start a gateway process. Default: no-op."""
        return NoOpGatewayHandle()

    async def wait_for_gateway(self, handle: GatewayHandle) -> None:
        """Wait until the gateway is ready."""
        pass

    async def stop_gateway(self, handle: GatewayHandle) -> None:
        """Stop the gateway process."""
        if handle.process is not None:
            if handle.process.returncode is None:
                try:
                    handle.process.terminate()
                except ProcessLookupError:
                    pass
            try:
                await handle.process.wait()
            except ProcessLookupError:
                pass
        for task in (handle.stdout_task, handle.stderr_task):
            if task is None:
                continue
            await task

    async def on_round_complete(self, ctx: RoundContext) -> RoundResult | None:
        """Called after each round's inline scoring.

        Override in framework-specific engines to inject custom logic.
        Return None for no intervention.
        """
        return None
