"""Tests for core data types."""
import asyncio
from pathlib import Path

from clawarena.core.types import (
    AgentResult, GatewayHandle, NoOpGatewayHandle,
    RoundContext, RoundResult, ScoringResult, TestContext, WorkCopy,
)
from clawarena.core.provider import ModelConfig, resolve_model_config
from clawarena.engines.base import AgentEngine


def test_agent_result_success():
    r = AgentResult(status="success", answer="hello")
    assert r.status == "success"
    assert r.answer == "hello"
    assert r.error is None
    assert r.returncode is None


def test_agent_result_failed():
    r = AgentResult(status="failed", answer="", error="boom", returncode=1)
    assert r.status == "failed"
    assert r.error == "boom"


def test_gateway_handle():
    h = GatewayHandle(
        process=None,
        port=8080,
        stdout_chunks=["gateway started\n"],
        stderr_chunks=["warning\n"],
    )
    assert h.port == 8080
    detail = h.debug_output()
    assert "stdout:" in detail
    assert "gateway started" in detail
    assert "stderr:" in detail


def test_noop_gateway():
    h = NoOpGatewayHandle()
    assert h.process is None
    assert h.port is None
    assert h.debug_output() == ""


def test_work_copy(tmp_path):
    wc = WorkCopy(
        state_dir=tmp_path / "state",
        config_path=tmp_path / "config.json",
        project_root=tmp_path,
    )
    assert wc.workspace_root is None
    assert wc.extra == {}


def test_test_context():
    ctx = TestContext(framework="openclaw", test_id="t1")
    assert ctx["framework"] == "openclaw"
    assert ctx["test_id"] == "t1"


def test_scoring_result():
    sr = ScoringResult(
        extracted_answer=["A"], correct_answer=["A", "B"],
        score=0.5, metrics={"f1": 0.67},
    )
    assert sr.score == 0.5


def test_round_context():
    ctx = RoundContext(
        framework="openclaw", test_id="t1", round_id="r1",
        round_index=0, total_rounds=3, is_last_round=False,
        round_record={}, query="q", result={}, inline_score={"passed": True},
        prev_inline_score=None, all_results=None, all_inline_scores=None,
        result_path=Path("/tmp/r.json"), workspace_path=None, out_dir=Path("/tmp"),
    )
    assert ctx.round_index == 0
    assert ctx.session_id == ""
    assert ctx.work_copy is None


def test_round_context_with_session(tmp_path):
    wc = WorkCopy(state_dir=tmp_path, config_path=None, project_root=tmp_path)
    ctx = RoundContext(
        framework="claude-code", test_id="t1", round_id="r1",
        round_index=0, total_rounds=3, is_last_round=False,
        round_record={}, query="q", result={}, inline_score={"passed": True},
        prev_inline_score=None, all_results=None, all_inline_scores=None,
        result_path=Path("/tmp/r.json"), workspace_path=None, out_dir=Path("/tmp"),
        session_id="sess-123", work_copy=wc,
    )
    assert ctx.session_id == "sess-123"
    assert ctx.work_copy is wc


def test_round_result_defaults():
    rr = RoundResult()
    assert rr.skip_remaining is False
    assert rr.override_feedback is None
    assert rr.extra_data is None


def test_stop_gateway_ignores_missing_process():
    class _Process:
        returncode = None

        def terminate(self):
            raise ProcessLookupError()

        async def wait(self):
            raise ProcessLookupError()

    class _Engine(AgentEngine):
        async def run_agent(self, *args, **kwargs):  # pragma: no cover - unused
            raise NotImplementedError

    engine = _Engine()
    handle = GatewayHandle(process=_Process(), port=1234)
    asyncio.run(engine.stop_gateway(handle))


def test_resolve_model_config_prefers_env_over_framework(monkeypatch):
    monkeypatch.setenv("CLAWARENA_PROVIDER", "openai")
    monkeypatch.setenv("CLAWARENA_MODEL_ID", "gpt-5.1")
    monkeypatch.setenv("CLAWARENA_API_BASE", "https://example.invalid/v1")
    monkeypatch.setenv("CLAWARENA_API_KEY", "test-key")
    cfg = resolve_model_config(
        {
            "frameworks": {
                "openclaw": {
                    "model": {
                        "provider": "anthropic",
                        "model_id": "claude-sonnet-4.5",
                    }
                }
            }
        },
        "openclaw",
    )
    assert cfg is not None
    assert cfg.provider == "openai"
    assert cfg.model_id == "gpt-5.1"
    assert cfg.api_base == "https://example.invalid/v1"


def test_resolve_model_config_prefers_cli_over_env(monkeypatch):
    monkeypatch.setenv("CLAWARENA_PROVIDER", "openai")
    monkeypatch.setenv("CLAWARENA_MODEL_ID", "gpt-5.1")
    cli_model = ModelConfig(
        provider="anthropic",
        model_id="claude-sonnet-4.5",
        api_base="https://api.anthropic.com",
        api_key="anthropic-key",
    )
    cfg = resolve_model_config({}, "openclaw", cli_model=cli_model)
    assert cfg is cli_model
