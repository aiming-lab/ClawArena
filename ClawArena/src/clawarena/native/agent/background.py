"""统一后台任务注册表。

SMbench 有三类「后台」工作，全部对齐 claude-code 原生语义：调用立即返回一个
task id，真正的工作在 asyncio task 中跑，完成后以 ``<task-notification>`` 通知
main agent；且三类都纳入「回合结束判定」——只要还有任一后台任务在跑，本回合
就不算结束。

- ``subagent``：``RunSubagent(run_in_background=true)``；
- ``bash``：``Bash(run_in_background=true)``；
- ``workflow``：``Workflow`` 工具（整段脚本作为一个后台任务）。

设计要点：
- 注册表挂在 **main** AgentHarness 上（回合判定与通知注入都以 main 为中心）。
  subagent 的 harness 不持有注册表——subagent 内的 Bash 后台调用退化为同步执行
  （subagent 本就必须在返回 main 前跑完，详见 ``tools/basic.py``）。
- 每个后台任务包一个 coroutine，该 coroutine 须返回一段**通知正文**（不含
  ``<task-notification>`` 标签）；注册表在其完成后把正文经
  ``inject_task_notification`` 排入 main 的下一个对外 turn。
- task id 形如 ``bash_1`` / ``sub_3`` / ``wf_2``，对 agent 可见，便于其在
  transcript 中关联「启动」与「完成」两条消息。
"""
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Awaitable, Callable, Optional


@dataclass
class BackgroundHandle:
    task_id: str
    kind: str  # "subagent" | "bash" | "workflow"
    task: asyncio.Task


class BackgroundRegistry:
    def __init__(self, inject_task_notification: Callable[[str], None]):
        # inject_task_notification: 把一段通知正文排入 main 的下一个对外 turn。
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
        """登记一个后台任务。``body_coro`` 完成后其返回的字符串被作为 task-notification 注入。

        返回分配的 ``task_id``（若调用方未自带）。
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

    async def wait_all(self) -> None:
        pending = [h.task for h in self._handles.values() if not h.task.done()]
        if pending:
            await asyncio.gather(*pending, return_exceptions=True)

    def summary(self) -> dict[str, int]:
        """按 kind 统计已登记的后台任务数（统计用）。"""
        out: dict[str, int] = {}
        for h in self._handles.values():
            out[h.kind] = out.get(h.kind, 0) + 1
        return out
