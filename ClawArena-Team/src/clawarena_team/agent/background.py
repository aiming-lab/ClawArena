"""Unified background-task registry.

ClawArena-Team has three classes of "background" work, all aligned with
claude-code native semantics: the call returns a task id immediately, the real
work runs in an asyncio task, and on completion the main agent is notified via
``<task-notification>``; all three are also included in the "round-end
judgement" -- as long as any background task is still running, this round does
not count as finished.

- ``subagent``: ``RunSubagent(run_in_background=true)``;
- ``bash``: ``Bash(run_in_background=true)``;
- ``workflow``: the ``Workflow`` tool (the whole script as one background task).

Design points:
- The registry is mounted on the **main** AgentHarness (both round judgement and
  notification injection are centered on main). The subagent's harness does not
  hold a registry -- a Bash background call inside a subagent degrades to
  synchronous execution (a subagent must finish before returning to main anyway,
  see ``tools/basic.py``).
- Each background task wraps a coroutine that must return a **notification body**
  (without the ``<task-notification>`` tag); on its completion the registry
  enqueues the body into main's next outgoing turn via
  ``inject_task_notification``.
- task ids look like ``bash_1`` / ``sub_3`` / ``wf_2``, visible to the agent so it
  can correlate the "start" and "completion" messages in the transcript.
"""
from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass
from typing import Awaitable, Callable, Optional


@dataclass
class BackgroundHandle:
    task_id: str
    kind: str  # "subagent" | "bash" | "workflow"
    task: asyncio.Task


class BackgroundRegistry:
    def __init__(self, inject_task_notification: Callable[[str], None]):
        # inject_task_notification: enqueue a notification body into main's next outgoing turn.
        self._inject = inject_task_notification
        self._handles: dict[str, BackgroundHandle] = {}
        self._counters: dict[str, int] = {}

    def new_task_id(self, kind: str) -> str:
        n = self._counters.get(kind, 0) + 1
        self._counters[kind] = n
        prefix = {"subagent": "sub", "bash": "bash", "workflow": "wf"}.get(kind, kind)
        return f"{prefix}_{n}"

    def spawn(
        self,
        kind: str,
        body_coro: Awaitable[str],
        *,
        task_id: Optional[str] = None,
    ) -> str:
        """Register a background task. After ``body_coro`` completes, the string it returns is injected as a task-notification.

        Returns the allocated ``task_id`` (if the caller did not provide one).
        """
        tid = task_id or self.new_task_id(kind)

        async def _runner() -> None:
            try:
                body = await body_coro
            except Exception as e:  # noqa: BLE001
                body = f"Background {kind} task {tid} FAILED.\nerror: {e}"
            self._inject(body)

        task = asyncio.create_task(_runner())
        self._handles[tid] = BackgroundHandle(task_id=tid, kind=kind, task=task)
        return tid

    def any_running(self) -> bool:
        return any(not h.task.done() for h in self._handles.values())

    def is_running(self, task_id: str) -> bool:
        h = self._handles.get(task_id)
        return h is not None and not h.task.done()

    async def wait_all(self, timeout: float | None = None) -> None:
        """Wait for all background tasks to wrap up (the round-end criterion).

        **Deadlock safety net**: some background subagent occasionally never wraps
        up in large scenarios (many concurrent subagents), which would freeze the
        whole scenario with main stuck permanently in ``ep_poll`` at
        ``wait_for_backgrounds``. Here we add a wall-clock timeout
        (``CATEAM_BACKGROUND_WAIT_TIMEOUT_SEC``, default 900s): on timeout it cancels
        the pending tasks and raises ``TimeoutError`` -- propagating this exception
        makes the scenario **fail cleanly (without writing metadata.json)**, so it
        can be retried via ``clawarena-team resume``, rather than hanging
        indefinitely or carrying a half-baked false completion.
        """
        pending = [h.task for h in self._handles.values() if not h.task.done()]
        if not pending:
            return
        if timeout is None:
            timeout = float(os.environ.get("CATEAM_BACKGROUND_WAIT_TIMEOUT_SEC", "900"))
        _, still = await asyncio.wait(pending, timeout=timeout)
        if not still:
            return
        for t in still:
            t.cancel()
        # Give cancellation a moment to propagate (cancel points take effect at await); do not wait forever to avoid getting stuck again
        await asyncio.wait(still, timeout=30)
        raise TimeoutError(
            f"wait_for_backgrounds timed out after {timeout:.0f}s: {len(still)} background subagent(s) did not wrap up "
            f"(suspected deadlock), cancelled; this scenario is judged failed and can be retried via clawarena-team resume"
        )

    def summary(self) -> dict[str, int]:
        """Count the registered background tasks by kind (for statistics)."""
        out: dict[str, int] = {}
        for h in self._handles.values():
            out[h.kind] = out.get(h.kind, 0) + 1
        return out
