"""RunRunner 跨场景鲁棒性回归测试。

背景：``RunRunner.run`` 曾用 ``asyncio.gather(..., return_exceptions=False)``,
任一场景抛异常即取消全部在跑场景、整轮报废(仅已完成场景留有 metadata,无 report)。
全集实跑时一个 provider 400 就让 41 场景的整轮挂掉。修复后 ``_guarded`` 逐场景兜底:
失败场景跳过(可由 resume 补跑),其余照常完成并汇入 report。
"""
from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

from clawarena_team.runner.run_runner import RunRunner


@pytest.mark.asyncio
async def test_single_scenario_failure_does_not_abort_run(tmp_path, monkeypatch):
    captured: dict = {}

    def _fake_build_report(run_id, results):
        captured["results"] = results
        return ({"run_id": run_id, "scenarios": len(results)}, "# fake report\n")

    # run() 内部 ``from ..scoring.report import build_run_report`` 在调用时求值,
    # 故 monkeypatch 模块属性即可生效。
    monkeypatch.setattr("clawarena_team.scoring.report.build_run_report", _fake_build_report)

    class _RR(RunRunner):
        async def _run_one(self, sc, run_dir):  # type: ignore[override]
            if sc.scenario_id == "bad":
                raise RuntimeError("simulated provider 400")
            return {"scenario_id": sc.scenario_id}

    scenarios = {
        sid: SimpleNamespace(scenario_id=sid) for sid in ("good_1", "bad", "good_2")
    }
    rr = _RR(
        manifests=None,
        scenarios=scenarios,
        model_bundle=None,
        tokenizer=None,
        config_dict={},
        output_root=tmp_path,
        concurrency=2,
    )

    out = await rr.run()

    # 失败场景被跳过,其余两场景照常汇入 report——整轮未被一个异常拖垮
    ids = sorted(r["scenario_id"] for r in captured["results"])
    assert ids == ["good_1", "good_2"]
    # report 仍正常落盘
    run_dir = tmp_path / out["run_id"]
    assert (run_dir / "report.json").exists()
    assert (run_dir / "report.md").exists()


@pytest.mark.asyncio
async def test_all_scenarios_pass_through_when_none_fail(tmp_path, monkeypatch):
    captured: dict = {}
    monkeypatch.setattr(
        "clawarena_team.scoring.report.build_run_report",
        lambda run_id, results: (captured.update(results=results) or {"run_id": run_id}, "md"),
    )

    class _RR(RunRunner):
        async def _run_one(self, sc, run_dir):  # type: ignore[override]
            return {"scenario_id": sc.scenario_id}

    scenarios = {sid: SimpleNamespace(scenario_id=sid) for sid in ("a", "b", "c")}
    rr = _RR(
        manifests=None, scenarios=scenarios, model_bundle=None, tokenizer=None,
        config_dict={}, output_root=tmp_path, concurrency=1,
    )
    await rr.run()
    assert sorted(r["scenario_id"] for r in captured["results"]) == ["a", "b", "c"]


@pytest.mark.asyncio
async def test_retry_succeeds_on_later_attempt(tmp_path, monkeypatch):
    """前几次执行异常、最终成功 → 场景被重试并最终汇入 report。"""
    captured: dict = {}
    monkeypatch.setattr(
        "clawarena_team.scoring.report.build_run_report",
        lambda rid, res: (captured.update(results=res) or {"run_id": rid}, "md"),
    )
    attempts = {"n": 0}

    class _RR(RunRunner):
        async def _run_one(self, sc, run_dir):  # type: ignore[override]
            attempts["n"] += 1
            if attempts["n"] < 3:
                raise RuntimeError("transient provider error")
            return {"scenario_id": sc.scenario_id}

    scenarios = {"s": SimpleNamespace(scenario_id="s")}
    rr = _RR(
        manifests=None, scenarios=scenarios, model_bundle=None, tokenizer=None,
        config_dict={"scenario": {"retry": 3}}, output_root=tmp_path, concurrency=1,
    )
    await rr.run()
    assert attempts["n"] == 3  # 试到第 3 次才成功
    assert [r["scenario_id"] for r in captured["results"]] == ["s"]


@pytest.mark.asyncio
async def test_retry_exhausted_skips_scenario(tmp_path, monkeypatch):
    """重试耗尽仍失败 → 场景被跳过，且恰好尝试 retry 次。"""
    captured: dict = {}
    monkeypatch.setattr(
        "clawarena_team.scoring.report.build_run_report",
        lambda rid, res: (captured.update(results=res) or {"run_id": rid}, "md"),
    )
    attempts = {"n": 0}

    class _RR(RunRunner):
        async def _run_one(self, sc, run_dir):  # type: ignore[override]
            attempts["n"] += 1
            raise RuntimeError("always fails")

    scenarios = {"s": SimpleNamespace(scenario_id="s")}
    rr = _RR(
        manifests=None, scenarios=scenarios, model_bundle=None, tokenizer=None,
        config_dict={"scenario": {"retry": 2}}, output_root=tmp_path, concurrency=1,
    )
    await rr.run()
    assert attempts["n"] == 2  # 试满 2 次
    assert captured["results"] == []  # 被跳过，不汇入 report


def test_retry_default_and_floor(tmp_path):
    """retry 默认 3；config 给 <1 时下取整为 1（至少跑一次）。"""
    sc = {"s": SimpleNamespace(scenario_id="s")}
    common = dict(manifests=None, scenarios=sc, model_bundle=None, tokenizer=None,
                  output_root=tmp_path, concurrency=1)
    assert RunRunner(config_dict={}, **common).retry == 3
    assert RunRunner(config_dict={"scenario": {"retry": 5}}, **common).retry == 5
    assert RunRunner(config_dict={"scenario": {"retry": 0}}, **common).retry == 1


def test_scenario_timeout_default_disabled_and_env(tmp_path, monkeypatch):
    """墙钟超时默认 0（禁用）；CATEAM_SCENARIO_TIMEOUT_SEC 生效且负值地板为 0。"""
    sc = {"s": SimpleNamespace(scenario_id="s")}
    common = dict(manifests=None, scenarios=sc, model_bundle=None, tokenizer=None,
                  config_dict={}, output_root=tmp_path, concurrency=1)
    monkeypatch.delenv("CATEAM_SCENARIO_TIMEOUT_SEC", raising=False)
    assert RunRunner(**common).scenario_timeout == 0.0
    monkeypatch.setenv("CATEAM_SCENARIO_TIMEOUT_SEC", "30")
    assert RunRunner(**common).scenario_timeout == 30.0
    monkeypatch.setenv("CATEAM_SCENARIO_TIMEOUT_SEC", "-5")
    assert RunRunner(**common).scenario_timeout == 0.0


@pytest.mark.asyncio
async def test_hung_scenario_times_out_and_is_skipped(tmp_path, monkeypatch):
    """挂死场景（永不返回）被墙钟超时取消、跳过；其余场景照常汇入 report。"""
    captured: dict = {}
    monkeypatch.setattr(
        "clawarena_team.scoring.report.build_run_report",
        lambda rid, res: (captured.update(results=res) or {"run_id": rid}, "md"),
    )
    monkeypatch.setenv("CATEAM_SCENARIO_TIMEOUT_SEC", "0.2")
    cancelled: dict = {"hung": False}

    class _RR(RunRunner):
        async def _run_one(self, sc, run_dir):  # type: ignore[override]
            if sc.scenario_id == "hung":
                try:
                    await asyncio.sleep(3600)  # 模拟永久挂死的无界 await
                except asyncio.CancelledError:
                    cancelled["hung"] = True  # 墙钟超时取消时应抛 CancelledError 进协程
                    raise
                return {"scenario_id": "hung"}
            return {"scenario_id": sc.scenario_id}

    scenarios = {sid: SimpleNamespace(scenario_id=sid) for sid in ("good_1", "hung", "good_2")}
    rr = _RR(
        manifests=None, scenarios=scenarios, model_bundle=None, tokenizer=None,
        config_dict={"scenario": {"retry": 1}}, output_root=tmp_path, concurrency=3,
    )
    out = await rr.run()

    ids = sorted(r["scenario_id"] for r in captured["results"])
    assert ids == ["good_1", "good_2"]   # 挂死场景被跳过，其余照常
    assert cancelled["hung"] is True      # 确认超时确实取消了挂死协程
    assert (tmp_path / out["run_id"] / "report.json").exists()


@pytest.mark.asyncio
async def test_timeout_then_success_on_retry(tmp_path, monkeypatch):
    """首次挂死被超时取消 → 重试；第二次快速返回 → 场景最终汇入 report。"""
    captured: dict = {}
    monkeypatch.setattr(
        "clawarena_team.scoring.report.build_run_report",
        lambda rid, res: (captured.update(results=res) or {"run_id": rid}, "md"),
    )
    monkeypatch.setenv("CATEAM_SCENARIO_TIMEOUT_SEC", "0.2")
    attempts = {"n": 0}

    class _RR(RunRunner):
        async def _run_one(self, sc, run_dir):  # type: ignore[override]
            attempts["n"] += 1
            if attempts["n"] == 1:
                await asyncio.sleep(3600)  # 首次挂死 → 被墙钟取消
            return {"scenario_id": sc.scenario_id}

    scenarios = {"s": SimpleNamespace(scenario_id="s")}
    rr = _RR(
        manifests=None, scenarios=scenarios, model_bundle=None, tokenizer=None,
        config_dict={"scenario": {"retry": 2}}, output_root=tmp_path, concurrency=1,
    )
    await rr.run()
    assert attempts["n"] == 2
    assert [r["scenario_id"] for r in captured["results"]] == ["s"]


# -----------------------------------------------------------------------------
# L2 异常分流:NonRetryableProviderError / TokenLimitExceeded 不消耗 retry 预算
# -----------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_non_retryable_provider_error_fast_fails_without_retry(tmp_path, monkeypatch):
    """4xx 客户端错(NonRetryableProviderError)→ 立刻放弃此场景,不消耗 retry。"""
    from clawarena_team.provider.base import NonRetryableProviderError

    captured: dict = {}
    monkeypatch.setattr(
        "clawarena_team.scoring.report.build_run_report",
        lambda rid, res: (captured.update(results=res) or {"run_id": rid}, "md"),
    )
    attempts = {"n": 0}

    class _RR(RunRunner):
        async def _run_one(self, sc, run_dir):  # type: ignore[override]
            attempts["n"] += 1
            raise NonRetryableProviderError("400 bad request")

    scenarios = {"s": SimpleNamespace(scenario_id="s")}
    rr = _RR(
        manifests=None, scenarios=scenarios, model_bundle=None, tokenizer=None,
        config_dict={"scenario": {"retry": 5}},  # 预算 5,但只该跑 1 次
        output_root=tmp_path, concurrency=1,
    )
    await rr.run()
    assert attempts["n"] == 1  # 不重试,直接 fast-fail
    assert captured["results"] == []  # 场景被跳过


@pytest.mark.asyncio
async def test_token_limit_exceeded_fast_fails_without_retry(tmp_path, monkeypatch):
    """context 超 token_limit 重跑必再现,也属于不可重试。"""
    from clawarena_team.agent.harness import TokenLimitExceeded

    captured: dict = {}
    monkeypatch.setattr(
        "clawarena_team.scoring.report.build_run_report",
        lambda rid, res: (captured.update(results=res) or {"run_id": rid}, "md"),
    )
    attempts = {"n": 0}

    class _RR(RunRunner):
        async def _run_one(self, sc, run_dir):  # type: ignore[override]
            attempts["n"] += 1
            raise TokenLimitExceeded("ctx 250k > 200k")

    scenarios = {"s": SimpleNamespace(scenario_id="s")}
    rr = _RR(
        manifests=None, scenarios=scenarios, model_bundle=None, tokenizer=None,
        config_dict={"scenario": {"retry": 3}},
        output_root=tmp_path, concurrency=1,
    )
    await rr.run()
    assert attempts["n"] == 1
    assert captured["results"] == []


@pytest.mark.asyncio
async def test_transient_error_still_retries(tmp_path, monkeypatch):
    """ProviderError(非 NonRetryable)仍照常 retry,与异常分流改动兼容。"""
    from clawarena_team.provider.base import ProviderError

    captured: dict = {}
    monkeypatch.setattr(
        "clawarena_team.scoring.report.build_run_report",
        lambda rid, res: (captured.update(results=res) or {"run_id": rid}, "md"),
    )
    attempts = {"n": 0}

    class _RR(RunRunner):
        async def _run_one(self, sc, run_dir):  # type: ignore[override]
            attempts["n"] += 1
            if attempts["n"] < 2:
                raise ProviderError("500 server error after retries used up")
            return {"scenario_id": sc.scenario_id}

    scenarios = {"s": SimpleNamespace(scenario_id="s")}
    rr = _RR(
        manifests=None, scenarios=scenarios, model_bundle=None, tokenizer=None,
        config_dict={"scenario": {"retry": 3}},
        output_root=tmp_path, concurrency=1,
    )
    await rr.run()
    assert attempts["n"] == 2  # 第 2 次成功
    assert [r["scenario_id"] for r in captured["results"]] == ["s"]
