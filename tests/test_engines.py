"""Tests for engine base classes."""

import asyncio
import json
from pathlib import Path
from unittest.mock import AsyncMock

import pytest

from clawarena.core.types import (
    GatewayHandle, NoOpGatewayHandle, RoundContext, RoundResult, WorkCopy,
)
from clawarena.engines.base import AgentEngine
from clawarena.engines.claude_code.engine import ClaudeCodeEngine
from clawarena.engines.openclaw.engine import OpenClawEngine
from clawarena.engines.picoclaw.engine import PicoClawEngine


def _make_round_ctx(**overrides) -> RoundContext:
    defaults = dict(
        framework="openclaw", test_id="t1", round_id="r1",
        round_index=0, total_rounds=1, is_last_round=True,
        round_record={}, query="q", result={}, inline_score={"passed": True},
        prev_inline_score=None, all_results=None, all_inline_scores=None,
        result_path=Path("/tmp/r.json"), workspace_path=None, out_dir=Path("/tmp"),
    )
    defaults.update(overrides)
    return RoundContext(**defaults)


class TestOpenClawEngine:
    def test_build_agent_cmd(self):
        engine = OpenClawEngine()
        cmd = engine.build_agent_cmd("sess1", "hello world")
        assert cmd == ["openclaw", "agent", "--session-id", "sess1", "--message", "hello world"]

    def test_build_agent_cmd_with_agent_id(self):
        engine = OpenClawEngine()
        cmd = engine.build_agent_cmd("sess1", "hello world", agent_id="hil_s1")
        assert cmd == [
            "openclaw", "agent", "--agent", "hil_s1",
            "--session-id", "sess1", "--message", "hello world",
        ]

    def test_build_env(self, tmp_path):
        engine = OpenClawEngine()
        wc = WorkCopy(
            state_dir=tmp_path / "state",
            config_path=tmp_path / "config.json",
            project_root=tmp_path,
        )
        env = engine.build_env(wc, 9999)
        assert env["OPENCLAW_STATE_DIR"] == str(tmp_path / "state")
        assert env["OPENCLAW_CONFIG_PATH"] == str(tmp_path / "config.json")
        assert env["OPENCLAW_GATEWAY_PORT"] == "9999"
        assert env["BENCHMARK_ROOT"] == str(tmp_path)

    def test_build_env_no_gateway(self, tmp_path):
        engine = OpenClawEngine()
        wc = WorkCopy(state_dir=tmp_path, config_path=None, project_root=tmp_path)
        env = engine.build_env(wc, None)
        assert env["BENCHMARK_ROOT"] == str(tmp_path)
        assert "OPENCLAW_GATEWAY_PORT" not in env

    def test_build_gateway_cmd(self, tmp_path):
        engine = OpenClawEngine()
        wc = WorkCopy(state_dir=tmp_path, config_path=None, project_root=tmp_path)
        cmd = engine.build_gateway_cmd(wc, 8888)
        assert "openclaw" in cmd
        assert "--port" in cmd
        assert "8888" in cmd

    def test_wait_for_gateway_timeout_includes_output(self):
        engine = OpenClawEngine()
        handle = GatewayHandle(
            process=None,
            port=65530,
            stdout_chunks=["gateway booting\n"],
            stderr_chunks=["bad config\n"],
        )

        with pytest.raises(RuntimeError, match="Captured gateway output"):
            asyncio.run(engine.wait_for_gateway(handle, timeout=0.01))

    def test_wait_for_gateway_early_exit_includes_returncode(self):
        engine = OpenClawEngine()

        class DoneTask:
            def __await__(self):
                if False:
                    yield None
                return None

        class ExitedProcess:
            returncode = 7

        handle = GatewayHandle(
            process=ExitedProcess(),
            port=9999,
            stdout_chunks=["gateway booting\n"],
            stderr_chunks=["bad config\n"],
            stdout_task=DoneTask(),
            stderr_task=DoneTask(),
        )

        with pytest.raises(RuntimeError, match="exited early with return code 7"):
            asyncio.run(engine.wait_for_gateway(handle, timeout=0.01))

    def test_build_cwd_uses_workspace_when_exists(self, tmp_path):
        engine = OpenClawEngine()
        workspace_root = tmp_path / "workspaces"
        (workspace_root / "agent1").mkdir(parents=True)
        wc = WorkCopy(
            state_dir=tmp_path / "state",
            config_path=None,
            project_root=tmp_path,
            workspace_root=workspace_root,
        )
        result = engine.build_cwd(wc, "agent1")
        assert result == workspace_root / "agent1"

    def test_build_cwd_falls_back_when_workspace_missing(self, tmp_path):
        engine = OpenClawEngine()
        workspace_root = tmp_path / "workspaces"
        workspace_root.mkdir()
        wc = WorkCopy(
            state_dir=tmp_path / "state",
            config_path=None,
            project_root=tmp_path,
            workspace_root=workspace_root,
        )
        result = engine.build_cwd(wc, "nonexistent_agent")
        assert result == tmp_path

    def test_build_cwd_falls_back_when_no_agent_id(self, tmp_path):
        engine = OpenClawEngine()
        wc = WorkCopy(
            state_dir=tmp_path / "state",
            config_path=None,
            project_root=tmp_path,
            workspace_root=tmp_path / "workspaces",
        )
        assert engine.build_cwd(wc, None) == tmp_path

    def test_build_cwd_falls_back_when_no_workspace_root(self, tmp_path):
        engine = OpenClawEngine()
        wc = WorkCopy(
            state_dir=tmp_path / "state",
            config_path=None,
            project_root=tmp_path,
            workspace_root=None,
        )
        assert engine.build_cwd(wc, "agent1") == tmp_path

    def test_run_agent_appends_local_flag_when_mm_metaclaw_mode(self, tmp_path):
        engine = OpenClawEngine()
        captured_cmd = []

        async def fake_run(session_id, message, work_copy, agent_id=None,
                           gateway_port=None, timeout=None, extra_env=None):
            cmd = engine.build_agent_cmd(session_id, message, agent_id=agent_id)
            if (extra_env or {}).get("OPENCLAW_LOCAL_MODE") == "1":
                cmd.append("--local")
            captured_cmd.extend(cmd)
            from clawarena.core.types import AgentResult
            return AgentResult(status="success", answer="ok", error=None,
                               returncode=0, llm_log=None)

        wc = WorkCopy(state_dir=tmp_path, config_path=None, project_root=tmp_path)
        asyncio.run(fake_run(
            "sess1", "hello", wc,
            extra_env={"OPENCLAW_LOCAL_MODE": "1"},
        ))
        assert "--local" in captured_cmd

    def test_run_agent_no_local_flag_without_mm_metaclaw(self, tmp_path):
        engine = OpenClawEngine()
        captured_cmd = []

        async def fake_run(session_id, message, work_copy, agent_id=None,
                           gateway_port=None, timeout=None, extra_env=None):
            cmd = engine.build_agent_cmd(session_id, message, agent_id=agent_id)
            if (extra_env or {}).get("OPENCLAW_LOCAL_MODE") == "1":
                cmd.append("--local")
            captured_cmd.extend(cmd)
            from clawarena.core.types import AgentResult
            return AgentResult(status="success", answer="ok", error=None,
                               returncode=0, llm_log=None)

        wc = WorkCopy(state_dir=tmp_path, config_path=None, project_root=tmp_path)
        asyncio.run(fake_run("sess1", "hello", wc, extra_env=None))
        assert "--local" not in captured_cmd

        asyncio.run(fake_run("sess1", "hello", wc, extra_env={"OTHER_KEY": "1"}))
        assert "--local" not in captured_cmd


class TestPicoClawEngine:
    def test_resolve_runtime_config_rewrites_workspace(self, tmp_path):
        engine = PicoClawEngine()
        cfg_path = tmp_path / "config.json"
        cfg_path.write_text('{"agents":{"defaults":{"model_name":"benchmark"}}}')
        work_copy = WorkCopy(
            state_dir=tmp_path / "state",
            config_path=cfg_path,
            project_root=tmp_path,
            workspace_root=tmp_path / "workspaces",
        )
        work_copy.state_dir.mkdir()
        workspace = tmp_path / "workspaces" / "t1"
        workspace.mkdir(parents=True)

        runtime = engine._resolve_runtime_config(work_copy, workspace, {})
        assert runtime is not None
        cfg = json.loads(runtime.read_text())
        assert cfg["agents"]["defaults"]["workspace"] == str(workspace)

    def test_resolve_runtime_config_copies_security_yml(self, tmp_path):
        engine = PicoClawEngine()
        cfg_path = tmp_path / "config.json"
        cfg_path.write_text('{"agents":{"defaults":{"model_name":"benchmark"}}}')
        (tmp_path / ".security.yml").write_text(
            "model_list:\n  benchmark:\n    api_keys:\n      - secret\n",
            encoding="utf-8",
        )
        work_copy = WorkCopy(
            state_dir=tmp_path / "state",
            config_path=cfg_path,
            project_root=tmp_path,
            workspace_root=tmp_path / "workspaces",
        )
        work_copy.state_dir.mkdir()
        workspace = tmp_path / "workspaces" / "t1"
        workspace.mkdir(parents=True)

        runtime = engine._resolve_runtime_config(work_copy, workspace, {})
        assert runtime is not None
        sec_path = runtime.parent / ".security.yml"
        assert sec_path.exists()
        assert "secret" in sec_path.read_text(encoding="utf-8")


class TestClaudeCodeEngine:
    def test_normalize_ccr_api_base(self):
        engine = ClaudeCodeEngine()
        assert engine._normalize_ccr_api_base("https://proxy.example/v1") == (
            "https://proxy.example/v1/chat/completions"
        )
        assert engine._normalize_ccr_api_base(
            "https://proxy.example/v1/chat/completions"
        ) == "https://proxy.example/v1/chat/completions"

    def test_build_ccr_config(self, tmp_path):
        engine = ClaudeCodeEngine()
        runtime = {
            "provider": "openai",
            "model_id": "gpt-5.1",
            "api_base": "https://proxy.example/v1",
            "api_key": "sk-test",
        }
        cfg = engine._build_ccr_config(runtime, 3456, "secret-token", tmp_path)
        assert cfg["PORT"] == 3456
        assert cfg["APIKEY"] == "secret-token"
        assert cfg["API_TIMEOUT_MS"] == 600000
        assert cfg["NON_INTERACTIVE_MODE"] is False
        assert cfg["Providers"][0]["api_base_url"] == (
            "https://proxy.example/v1/chat/completions"
        )
        assert cfg["Providers"][0]["models"] == ["gpt-5.1"]
        assert cfg["Providers"][0]["transformer"] == {
            "use": ["stripreasoning", "maxcompletiontokens"]
        }
        assert cfg["Router"]["default"] == "openai,gpt-5.1"
        assert cfg["Router"]["background"] == "openai,gpt-5.1"

    def test_build_ccr_config_openrouter_transformer(self, tmp_path):
        engine = ClaudeCodeEngine()
        runtime = {
            "provider": "openrouter",
            "model_id": "anthropic/claude-sonnet-4",
            "api_base": "https://openrouter.ai/api/v1",
            "api_key": "sk-or-test",
        }
        cfg = engine._build_ccr_config(runtime, 3457, "tok", tmp_path)
        assert cfg["Providers"][0]["transformer"] == {"use": ["openrouter"]}

    def test_build_ccr_config_unknown_provider_has_no_transformer(self, tmp_path):
        engine = ClaudeCodeEngine()
        runtime = {
            "provider": "custom",
            "model_id": "foo",
            "api_base": "https://example.com/v1",
            "api_key": "k",
        }
        cfg = engine._build_ccr_config(runtime, 3458, "tok", tmp_path)
        assert "transformer" not in cfg["Providers"][0]

    @pytest.mark.parametrize("provider", [
        "openai", "azure", "ollama",
        "deepseek", "moonshot", "glm", "groq", "xai",
        "qwen", "minimax", "mistral",
    ])
    def test_openai_compat_providers_share_transformer(self, provider):
        engine = ClaudeCodeEngine()
        assert engine._ccr_transformer(provider) == ["stripreasoning", "maxcompletiontokens"]

    def test_openrouter_and_google_keep_dedicated_transformers(self):
        engine = ClaudeCodeEngine()
        assert engine._ccr_transformer("openrouter") == ["openrouter"]
        assert engine._ccr_transformer("google") == ["gemini"]
        assert engine._ccr_transformer("anthropic") is None

    def test_build_ccr_env(self):
        engine = ClaudeCodeEngine()
        env = engine._build_ccr_env(3456, "secret-token")
        assert env["ANTHROPIC_BASE_URL"] == "http://127.0.0.1:3456"
        assert env["ANTHROPIC_AUTH_TOKEN"] == "secret-token"
        assert env["NO_PROXY"] == "127.0.0.1"

    def test_stop_gateway_terminates_background_ccr(self, tmp_path, monkeypatch):
        engine = ClaudeCodeEngine()

        class DummyProc:
            def __init__(self):
                self.returncode = None
                self.terminated = False
                self.killed = False
                self.wait = AsyncMock(return_value=0)

            def terminate(self):
                self.terminated = True
                self.returncode = 0

            def kill(self):
                self.killed = True
                self.returncode = -9

        proc = DummyProc()
        home_dir = tmp_path / "home"
        (home_dir / ".claude-code-router").mkdir(parents=True)
        handle = GatewayHandle(process=proc, port=3456)
        handle.ccr_home_dir = home_dir

        async def fake_exec(*args, **kwargs):
            class StopProc:
                async def communicate(self):
                    return (b"stopped\n", b"")
            return StopProc()

        monkeypatch.setattr(asyncio, "create_subprocess_exec", fake_exec)
        asyncio.run(engine.stop_gateway(handle))

        assert proc.terminated is True
        assert "stopped" in "".join(handle.stdout_chunks)


class TestEngineHook:
    def test_default_on_round_complete_returns_none(self):
        engine = OpenClawEngine()
        result = asyncio.run(engine.on_round_complete(_make_round_ctx()))
        assert result is None

    def test_custom_engine_hook(self):
        """A subclassed engine can override on_round_complete."""
        class CustomEngine(OpenClawEngine):
            async def on_round_complete(self, ctx):
                return RoundResult(skip_remaining=True, extra_data={"custom": 1})

        engine = CustomEngine()
        result = asyncio.run(engine.on_round_complete(_make_round_ctx()))
        assert result is not None
        assert result.skip_remaining is True
        assert result.extra_data == {"custom": 1}


class TestNoOpGateway:
    def test_stop_noop(self):
        engine = OpenClawEngine()
        handle = NoOpGatewayHandle()
        asyncio.run(engine.stop_gateway(handle))
