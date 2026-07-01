"""``BackgroundRegistry.wait_all`` 死锁兜底超时回归测试。

大场景(多并发子代理)上偶发某后台子代理永不收尾,会让 main 在
``wait_for_backgrounds`` 处永久冻结(ep_poll)。wait_all 现加墙钟超时:超时即取消挂起
任务并抛 TimeoutError,使该场景干净判失败(不落 metadata.json)、可由 resume 重试。
"""
from __future__ import annotations

import asyncio

import pytest

from clawarena_team.agent.background import BackgroundRegistry


def _reg() -> BackgroundRegistry:
    return BackgroundRegistry(inject_task_notification=lambda body: None)


async def test_wait_all_returns_when_all_done():
    reg = _reg()
    injected: list[str] = []
    reg = BackgroundRegistry(inject_task_notification=injected.append)

    async def quick() -> str:
        return "done-body"

    reg.spawn("subagent", quick())
    await asyncio.sleep(0)  # 让 _runner 跑完
    await reg.wait_all(timeout=5)  # 全部完成,不应抛错
    assert not reg.any_running()
    assert injected == ["done-body"]  # 完成后注入了通知正文


async def test_wait_all_times_out_and_cancels_hung_task():
    reg = _reg()

    async def hang() -> str:
        await asyncio.sleep(3600)  # 模拟永不收尾的后台子代理
        return "never"

    reg.spawn("subagent", hang())
    with pytest.raises(TimeoutError):
        await reg.wait_all(timeout=0.2)
    # 挂起任务被取消 → 视为 done → 不再 running
    assert not reg.any_running()


async def test_wait_all_no_pending_is_noop():
    reg = _reg()
    await reg.wait_all(timeout=0.2)  # 无任务,直接返回不抛
    assert not reg.any_running()
