"""ScenarioRunner.metadata 装配回归测试。

背景：``ScenarioRunner.run`` 中 main agent 的 harness 是**局部变量** ``harness``，
不是 ``self`` 属性。历史上 metadata 装配处误写成 ``self.harness.cfg.token_limit``，
导致每个场景跑到结尾写 metadata.json 时抛 ``AttributeError`` 而整轮中断；该路径此前
无任何单测覆盖（254 个用例全过却漏掉）。本测试直接覆盖 ``_assemble_metadata``：
若再次误用不存在的 ``self`` 属性，fake self 上取不到该属性即报错，用例失败。
"""
from __future__ import annotations

from types import SimpleNamespace

from clawarena_team.runner.scenario_runner import ScenarioRunner


def _fake_self() -> SimpleNamespace:
    """构造仅含 ``_assemble_metadata`` 所需属性的最小 fake ``self``。

    刻意**不**提供 ``harness`` 属性：token_limit 必须取自传入的局部 harness，
    任何 ``self.harness`` 误用都会在此处 AttributeError。
    """
    return SimpleNamespace(
        scenario=SimpleNamespace(scenario_id="s_demo"),
        _started_at=1000.0,
        round_evals=[
            SimpleNamespace(round_id="q1", passed=True, exit_code=0),
            SimpleNamespace(round_id="q2", passed=False, exit_code=2),
        ],
        model_bundle=SimpleNamespace(
            main=SimpleNamespace(
                provider="openai_compat",
                model_id="gemma-4-31b-it",
                api_base="http://127.0.0.1:8900/v1",
                modalities=["text", "image"],
                extra={},
            ),
            pool={},  # 空池：跳过 info_for_metadata，聚焦 token_limit 装配
        ),
    )


def test_assemble_metadata_token_limit_from_local_harness():
    """token_limit 取自局部 harness.cfg；并校验关键字段装配正确。"""
    fake_self = _fake_self()
    harness = SimpleNamespace(cfg=SimpleNamespace(token_limit=245_760))
    metrics = SimpleNamespace(sms=0.7, tcr=0.66)  # __dict__ 即 metrics 序列化体

    md = ScenarioRunner._assemble_metadata(fake_self, harness=harness, metrics=metrics)

    # 回归核心：token_limit 来自局部 harness，而非 self（self 上根本没有该属性）
    assert md["token_limit"] == 245_760
    assert md["scenario_id"] == "s_demo"
    assert md["started_at"] == 1000.0
    assert md["rounds"] == [
        {"id": "q1", "passed": True, "exit_code": 0},
        {"id": "q2", "passed": False, "exit_code": 2},
    ]
    assert md["metrics"] == {"sms": 0.7, "tcr": 0.66}
    assert md["models"]["main"]["model_id"] == "gemma-4-31b-it"
    assert md["models"]["pool"] == {}


def test_assemble_metadata_missing_token_limit_is_none():
    """harness.cfg 无 token_limit 时回退 None（getattr 容错），不抛异常。"""
    fake_self = _fake_self()
    harness = SimpleNamespace(cfg=SimpleNamespace())  # 无 token_limit
    metrics = SimpleNamespace()

    md = ScenarioRunner._assemble_metadata(fake_self, harness=harness, metrics=metrics)
    assert md["token_limit"] is None


# -----------------------------------------------------------------------------
# Round-level wall-clock guard:_run_round_body 必须能被 asyncio.wait_for 取消
# -----------------------------------------------------------------------------


def test_run_round_body_normal_path_completes():
    """正常路径:send_user + wait_for_backgrounds 都返回 None,helper 顺利完成。"""
    import asyncio
    called = []

    class FakeHarness:
        async def send_user(self, body, *, is_real_question):
            called.append(("send_user", body, is_real_question))

    class FakeManager:
        async def wait_for_backgrounds(self):
            called.append(("wait_for_backgrounds",))

    fake_self = SimpleNamespace()
    asyncio.run(
        ScenarioRunner._run_round_body(
            fake_self, harness=FakeHarness(), manager=FakeManager(),
            question_body="hi",
        )
    )
    assert called == [
        ("send_user", "hi", True),
        ("wait_for_backgrounds",),
    ]


def test_seal_dangling_tool_uses_injects_synthetic_results():
    """round cancel 留下 dangling tool_use 时,seal 给每个 id 注入 tool_result。

    Why: Anthropic 严格要求 tool_use 后紧接 tool_result;cancel 中途丢失
    tool_result 会让下一 round 的 chat() 4xx 拒。实战教训:opus 钉子户 q2
    cancel 后 q3 因 toolu_01Lv7bd8kBh7EZ9ZGAW2hwX6 dangling 被 4xx fast-fail。
    """
    from clawarena_team.agent.harness import HarnessTurn

    fake_harness = SimpleNamespace(
        turns=[
            HarnessTurn(role="user", content="q1"),
            HarnessTurn(
                role="assistant",
                content="",
                tool_calls=[
                    {"id": "toolu_a", "name": "Read", "arguments": {}},
                    {"id": "toolu_b", "name": "Write", "arguments": {}},
                    {"id": "toolu_c", "name": "Bash", "arguments": {}},
                ],
            ),
            # 只有 toolu_a 收到 tool_result;b/c dangling
            HarnessTurn(role="tool_result", content="OK", tool_call_id="toolu_a"),
        ]
    )
    injected = ScenarioRunner._seal_dangling_tool_uses(fake_harness)
    assert injected == 2
    # 新增的两条 tool_result 末尾追加,id 分别对应 toolu_b / toolu_c
    new_ids = [t.tool_call_id for t in fake_harness.turns[-2:]]
    assert set(new_ids) == {"toolu_b", "toolu_c"}
    for t in fake_harness.turns[-2:]:
        assert t.role == "tool_result"
        assert "round cancelled" in t.content.lower()


def test_seal_dangling_tool_uses_clean_history_returns_zero():
    """history 已经成对(每个 tool_use 都有 tool_result)时不做任何注入。"""
    from clawarena_team.agent.harness import HarnessTurn

    fake_harness = SimpleNamespace(
        turns=[
            HarnessTurn(role="user", content="q1"),
            HarnessTurn(
                role="assistant", content="",
                tool_calls=[{"id": "toolu_a", "name": "Read", "arguments": {}}],
            ),
            HarnessTurn(role="tool_result", content="OK", tool_call_id="toolu_a"),
            HarnessTurn(role="assistant", content="done", tool_calls=[]),
        ]
    )
    assert ScenarioRunner._seal_dangling_tool_uses(fake_harness) == 0
    # turns 数量没变
    assert len(fake_harness.turns) == 4


def test_seal_dangling_tool_uses_no_tool_calls_history_noop():
    """assistant 无 tool_calls 时直接 noop。"""
    from clawarena_team.agent.harness import HarnessTurn

    fake_harness = SimpleNamespace(
        turns=[
            HarnessTurn(role="user", content="q1"),
            HarnessTurn(role="assistant", content="reply", tool_calls=[]),
        ]
    )
    assert ScenarioRunner._seal_dangling_tool_uses(fake_harness) == 0


def test_run_round_body_can_be_cancelled_by_wait_for():
    """挂死场景:send_user 永久 await 时,外层 wait_for 必须能取消。

    模拟 s_security_pcap_triage 的 q1→q2 死锁——任一 await 永挂时,
    CATEAM_ROUND_TIMEOUT_SEC 必须救得了。
    """
    import asyncio

    class HangingHarness:
        async def send_user(self, body, *, is_real_question):
            # 模拟 anthropic provider socket 静默丢失 / send_user 内某 await 永挂
            await asyncio.sleep(3600)

    class FakeManager:
        async def wait_for_backgrounds(self):
            pass

    fake_self = SimpleNamespace()

    async def _wrap():
        await asyncio.wait_for(
            ScenarioRunner._run_round_body(
                fake_self, harness=HangingHarness(), manager=FakeManager(),
                question_body="hi",
            ),
            timeout=0.2,
        )

    import pytest
    with pytest.raises(asyncio.TimeoutError):
        asyncio.run(_wrap())
