"""Tests for the unified provider platform (ModelConfig + apply_model_config)."""

import json
import os
import pytest
from pathlib import Path

from clawarena.core.provider import (
    ConfigError,
    ModelConfig,
    expand_env_vars,
    mask_api_key,
    resolve_model_config,
)


# ---------------------------------------------------------------------------
# expand_env_vars
# ---------------------------------------------------------------------------

class TestExpandEnvVars:
    def test_simple(self, monkeypatch):
        monkeypatch.setenv("FOO", "bar")
        assert expand_env_vars("${FOO}") == "bar"

    def test_default(self, monkeypatch):
        monkeypatch.delenv("MISSING", raising=False)
        assert expand_env_vars("${MISSING:-fallback}") == "fallback"

    def test_no_match(self):
        assert expand_env_vars("plain text") == "plain text"

    def test_multiple(self, monkeypatch):
        monkeypatch.setenv("A", "1")
        monkeypatch.setenv("B", "2")
        assert expand_env_vars("${A}-${B}") == "1-2"


# ---------------------------------------------------------------------------
# mask_api_key
# ---------------------------------------------------------------------------

class TestMaskApiKey:
    def test_long_key(self):
        assert mask_api_key("sk-1234567890") == "sk-123***"

    def test_short_key(self):
        assert mask_api_key("abc") == "***"


# ---------------------------------------------------------------------------
# ModelConfig
# ---------------------------------------------------------------------------

class TestModelConfig:
    def test_from_dict_basic(self):
        m = ModelConfig.from_dict({"model_id": "gpt-4o", "provider": "openai"})
        assert m.model_id == "gpt-4o"
        assert m.provider == "openai"

    def test_from_dict_env_interpolation(self, monkeypatch):
        monkeypatch.setenv("TEST_MODEL", "claude-opus-4-6")
        m = ModelConfig.from_dict({"model_id": "${TEST_MODEL}", "provider": "anthropic"})
        assert m.model_id == "claude-opus-4.6"

    def test_from_dict_api_key_warning(self, caplog):
        import logging
        with caplog.at_level(logging.WARNING):
            m = ModelConfig.from_dict({
                "model_id": "x",
                "api_key": "sk-plaintext-key",
            })
        assert m.api_key == "sk-plaintext-key"
        assert "plaintext" in caplog.text

    def test_from_env(self, monkeypatch):
        monkeypatch.setenv("CLAWARENA_MODEL_ID", "llama3.2")
        monkeypatch.setenv("CLAWARENA_PROVIDER", "ollama")
        m = ModelConfig.from_env()
        assert m is not None
        assert m.model_id == "llama3.2"
        assert m.provider == "ollama"

    def test_from_env_none(self, monkeypatch):
        monkeypatch.delenv("CLAWARENA_MODEL_ID", raising=False)
        assert ModelConfig.from_env() is None

    def test_from_cli(self):
        m = ModelConfig.from_cli("openai", "gpt-4o", "http://localhost:8080", "sk-x")
        assert m.model_id == "gpt-4o"
        assert m.api_base == "http://localhost:8080"

    def test_from_cli_with_model_config(self):
        m = ModelConfig.from_cli(
            "openai", "gpt-5.1", "http://localhost:8080", "sk-x",
            '{"reasoning": true, "contextWindow": 200000}',
        )
        assert m.extra == {"reasoning": True, "contextWindow": 200000}

    def test_from_cli_none(self):
        assert ModelConfig.from_cli(None, None, None, None) is None

    def test_resolved_api_base_with_value(self):
        m = ModelConfig(model_id="x", api_base="http://custom")
        assert m.resolved_api_base() == "http://custom"

    def test_resolved_api_base_default(self):
        m = ModelConfig(model_id="x", provider="ollama")
        assert "11434" in m.resolved_api_base()


# ---------------------------------------------------------------------------
# resolve_model_config
# ---------------------------------------------------------------------------

class TestResolveModelConfig:
    def test_cli_highest_priority(self):
        cli = ModelConfig(model_id="cli-model")
        result = resolve_model_config(
            {"model": {"model_id": "top-model"}, "frameworks": {}},
            "openclaw",
            cli_model=cli,
        )
        assert result.model_id == "cli-model"

    def test_env_over_tests_json(self, monkeypatch):
        monkeypatch.setenv("CLAWARENA_MODEL_ID", "env-model")
        result = resolve_model_config(
            {"model": {"model_id": "top-model"}, "frameworks": {}},
            "openclaw",
        )
        assert result.model_id == "env-model"

    def test_framework_over_top(self):
        cfg = {
            "model": {"model_id": "top-model"},
            "frameworks": {
                "openclaw": {
                    "manifest": "x",
                    "model": {"model_id": "fw-model"},
                }
            },
        }
        result = resolve_model_config(cfg, "openclaw")
        assert result.model_id == "fw-model"

    def test_top_level_fallback(self):
        cfg = {
            "model": {"model_id": "top-model"},
            "frameworks": {"openclaw": {"manifest": "x"}},
        }
        result = resolve_model_config(cfg, "openclaw")
        assert result.model_id == "top-model"

    def test_none_when_no_config(self):
        assert resolve_model_config({"frameworks": {}}, "openclaw") is None


# ---------------------------------------------------------------------------
# apply_model_config — per-framework
# ---------------------------------------------------------------------------

class TestOpenClawApply:
    def test_openai_provider(self, tmp_path):
        from clawarena.data_handlers.openclaw.handler import OpenClawDataHandler
        from clawarena.core.types import WorkCopy

        state = tmp_path / "state"
        state.mkdir()
        cfg = {"models": {}, "agents": {"defaults": {}, "list": []}}
        (state / "openclaw.json").write_text(json.dumps(cfg))

        wc = WorkCopy(state_dir=state, config_path=None, project_root=tmp_path)
        handler = OpenClawDataHandler()
        model = ModelConfig(model_id="gpt-4o", provider="openai", api_key="sk-test")
        handler.apply_model_config(wc, model)

        result = json.loads((state / "openclaw.json").read_text())
        assert "openai" in result["models"]["providers"]
        p = result["models"]["providers"]["openai"]
        assert p["apiKey"] == "sk-test"
        assert "gpt-4o" in result["agents"]["defaults"]["model"]["primary"]

    def test_claude_provider(self, tmp_path):
        from clawarena.data_handlers.openclaw.handler import OpenClawDataHandler
        from clawarena.core.types import WorkCopy

        state = tmp_path / "state"
        state.mkdir()
        cfg = {"agents": {"defaults": {}, "list": []}}
        (state / "openclaw.json").write_text(json.dumps(cfg))

        wc = WorkCopy(state_dir=state, config_path=None, project_root=tmp_path)
        handler = OpenClawDataHandler()
        model = ModelConfig(model_id="claude-opus-4-6", provider="claude", api_key="sk-ant-oat01-x")
        handler.apply_model_config(wc, model)

        result = json.loads((state / "openclaw.json").read_text())
        assert "anthropic:manual" in result.get("auth", {}).get("profiles", {})
        assert "anthropic/claude-opus-4.6" in result["agents"]["defaults"]["model"]["primary"]

    def test_codex_provider(self, tmp_path):
        from clawarena.data_handlers.openclaw.handler import OpenClawDataHandler
        from clawarena.core.types import WorkCopy

        state = tmp_path / "state"
        state.mkdir()
        agent_dir = state / "agents" / "hil_e5"
        agent_dir.mkdir(parents=True)
        cfg = {
            "agents": {
                "defaults": {},
                "list": [{"agentDir": str(agent_dir)}],
            }
        }
        (state / "openclaw.json").write_text(json.dumps(cfg))
        auth_json = tmp_path / "auth.json"
        auth_json.write_text(json.dumps({
            "tokens": {
                "access_token": "ey-access",
                "refresh_token": "rt-refresh",
                "account_id": "acct-123",
            },
            "last_refresh": "2026-04-12T09:08:18.507920Z",
        }))

        wc = WorkCopy(state_dir=state, config_path=None, project_root=tmp_path)
        handler = OpenClawDataHandler()
        model = ModelConfig(
            model_id="gpt-5-codex",
            provider="codex",
            api_key=str(auth_json),
        )
        handler.apply_model_config(wc, model)

        result = json.loads((state / "openclaw.json").read_text())
        assert "openai-codex" in result["models"]["providers"]
        model_entry = result["models"]["providers"]["openai-codex"]["models"][0]
        provider_entry = result["models"]["providers"]["openai-codex"]
        assert provider_entry["baseUrl"] == "https://chatgpt.com/backend-api"
        assert provider_entry["api"] == "openai-codex-responses"
        assert model_entry["id"] == "gpt-5-codex"
        assert "openai-codex:default" in result.get("auth", {}).get("profiles", {})
        assert result["auth"]["order"]["openai-codex"] == ["openai-codex:default"]
        assert result["agents"]["defaults"]["model"]["primary"] == "openai-codex/gpt-5-codex"

        auth_profile = json.loads((agent_dir / "auth-profiles.json").read_text())
        profile = auth_profile["profiles"]["openai-codex:default"]
        assert profile["type"] == "oauth"
        assert profile["provider"] == "openai-codex"
        assert profile["access"] == "ey-access"
        assert profile["refresh"] == "rt-refresh"
        assert profile["accountId"] == "acct-123"
        assert profile["expires"] == 1778576898507
        assert auth_profile["order"]["openai-codex"] == ["openai-codex:default"]

    def test_codex_provider_merges_model_extra(self, tmp_path):
        from clawarena.data_handlers.openclaw.handler import OpenClawDataHandler
        from clawarena.core.types import WorkCopy

        state = tmp_path / "state"
        state.mkdir()
        agent_dir = state / "agents" / "hil_e5"
        agent_dir.mkdir(parents=True)
        cfg = {
            "agents": {
                "defaults": {},
                "list": [{"agentDir": str(agent_dir)}],
            }
        }
        (state / "openclaw.json").write_text(json.dumps(cfg))
        auth_json = tmp_path / "auth.json"
        auth_json.write_text(json.dumps({
            "tokens": {
                "access_token": "ey-access",
                "refresh_token": "rt-refresh",
                "account_id": "acct-123",
            },
            "last_refresh": "2026-04-12T09:08:18.507920Z",
        }))

        wc = WorkCopy(state_dir=state, config_path=None, project_root=tmp_path)
        handler = OpenClawDataHandler()
        model = ModelConfig(
            model_id="gpt-5.4",
            provider="codex",
            api_key=str(auth_json),
            extra={"contextTokens": 160000},
        )
        handler.apply_model_config(wc, model)

        result = json.loads((state / "openclaw.json").read_text())
        model_entry = result["models"]["providers"]["openai-codex"]["models"][0]
        assert model_entry["id"] == "gpt-5.4"
        assert model_entry["contextTokens"] == 160000

    def test_openai_provider_merges_model_extra(self, tmp_path):
        from clawarena.data_handlers.openclaw.handler import OpenClawDataHandler
        from clawarena.core.types import WorkCopy

        state = tmp_path / "state"
        state.mkdir()
        cfg = {"models": {}, "agents": {"defaults": {}, "list": []}}
        (state / "openclaw.json").write_text(json.dumps(cfg))

        wc = WorkCopy(state_dir=state, config_path=None, project_root=tmp_path)
        handler = OpenClawDataHandler()
        model = ModelConfig(
            model_id="gpt-5.1",
            provider="openai",
            api_key="sk-test",
            extra={"reasoning": True, "contextWindow": 200000},
        )
        handler.apply_model_config(wc, model)

        result = json.loads((state / "openclaw.json").read_text())
        model_entry = result["models"]["providers"]["openai"]["models"][0]
        assert model_entry["reasoning"] is True
        assert model_entry["contextWindow"] == 200000


class TestPicoClawApply:
    def test_openai_provider(self, tmp_path):
        from clawarena.data_handlers.picoclaw.handler import PicoClawDataHandler
        from clawarena.core.types import WorkCopy

        state = tmp_path / "state"
        state.mkdir()
        (state / "config.json").write_text(json.dumps({"model_list": [], "agents": {}}))

        wc = WorkCopy(state_dir=state, config_path=None, project_root=tmp_path)
        handler = PicoClawDataHandler()
        model = ModelConfig(model_id="gpt-4o", provider="openai",
                            api_base="http://proxy:8080", api_key="sk-test")
        handler.apply_model_config(wc, model)

        result = json.loads((state / "config.json").read_text())
        assert result["model_list"][0]["model"] == "openai/gpt-4o"
        assert result["model_list"][0]["api_base"] == "http://proxy:8080"
        assert result["model_list"][0]["api_key"] == "sk-test"

    def test_claude_raises(self, tmp_path):
        from clawarena.data_handlers.picoclaw.handler import PicoClawDataHandler
        from clawarena.core.types import WorkCopy

        state = tmp_path / "state"
        state.mkdir()
        (state / "config.json").write_text(json.dumps({}))

        wc = WorkCopy(state_dir=state, config_path=None, project_root=tmp_path)
        handler = PicoClawDataHandler()
        model = ModelConfig(model_id="x", provider="claude")
        with pytest.raises(ConfigError):
            handler.apply_model_config(wc, model)


class TestNanobotApply:
    def test_ollama_provider(self, tmp_path):
        from clawarena.data_handlers.nanobot.handler import NanobotDataHandler
        from clawarena.core.types import WorkCopy

        state = tmp_path / "state"
        state.mkdir()
        (state / "config.json").write_text(json.dumps({"providers": {}, "agents": {}}))

        wc = WorkCopy(state_dir=state, config_path=None, project_root=tmp_path)
        handler = NanobotDataHandler()
        model = ModelConfig(model_id="llama3", provider="ollama",
                            api_base="http://localhost:11434")
        handler.apply_model_config(wc, model)

        result = json.loads((state / "config.json").read_text())
        assert "ollama" in result["providers"]
        assert result["agents"]["defaults"]["model"] == "ollama/llama3"
        assert result["agents"]["defaults"]["provider"] == "auto"

    def test_openai_compatible_proxy_uses_custom_provider(self, tmp_path):
        from clawarena.data_handlers.nanobot.handler import NanobotDataHandler
        from clawarena.core.types import WorkCopy

        state = tmp_path / "state"
        state.mkdir()
        (state / "config.json").write_text(json.dumps({"providers": {}, "agents": {}}))

        wc = WorkCopy(state_dir=state, config_path=None, project_root=tmp_path)
        handler = NanobotDataHandler()
        model = ModelConfig(
            model_id="gpt-5.1",
            provider="openai",
            api_base="https://proxy.example/v1",
            api_key="sk-test",
        )
        handler.apply_model_config(wc, model)

        result = json.loads((state / "config.json").read_text())
        assert "custom" in result["providers"]
        assert result["providers"]["custom"]["apiBase"] == "https://proxy.example/v1"
        assert result["providers"]["custom"]["apiKey"] == "sk-test"
        assert result["agents"]["defaults"]["model"] == "gpt-5.1"
        assert result["agents"]["defaults"]["provider"] == "custom"


class TestClaudeCodeApply:
    def test_claude_oauth(self, tmp_path):
        from clawarena.data_handlers.claude_code.handler import ClaudeCodeDataHandler
        from clawarena.core.types import WorkCopy

        wc = WorkCopy(state_dir=tmp_path, config_path=None, project_root=tmp_path,
                       extra={})
        handler = ClaudeCodeDataHandler()
        model = ModelConfig(model_id="claude-opus-4.6", provider="claude",
                            api_key="sk-ant-oat01-token")
        handler.apply_model_config(wc, model)

        env = wc.extra["env_overrides"]
        assert env["CLAUDE_CODE_OAUTH_TOKEN"] == "sk-ant-oat01-token"
        assert "ANTHROPIC_BASE_URL" not in env

    def test_claude_oauth_custom_credentials_path(self, tmp_path):
        from clawarena.data_handlers.claude_code.handler import ClaudeCodeDataHandler
        from clawarena.core.types import WorkCopy

        creds_src = tmp_path / "custom.credentials.json"
        creds_src.write_text(json.dumps({"accessToken": "oauth-token"}))

        wc = WorkCopy(state_dir=tmp_path, config_path=None, project_root=tmp_path,
                      extra={})
        handler = ClaudeCodeDataHandler()
        model = ModelConfig(
            model_id="claude-opus-4.6",
            provider="claude",
            api_base=str(creds_src),
        )
        handler.apply_model_config(wc, model)

        env = wc.extra["env_overrides"]
        assert "CLAUDE_CODE_OAUTH_TOKEN" not in env
        assert json.loads((tmp_path / ".credentials.json").read_text()) == {
            "accessToken": "oauth-token"
        }

    def test_claude_oauth_default_credentials_warns(self, tmp_path, monkeypatch):
        import clawarena.data_handlers.claude_code.handler as handler_mod
        from clawarena.data_handlers.claude_code.handler import ClaudeCodeDataHandler
        from clawarena.core.types import WorkCopy

        default_creds = tmp_path / "default.credentials.json"
        default_creds.write_text(json.dumps({"refreshToken": "refresh-token"}))
        monkeypatch.setattr(handler_mod, "_DEFAULT_CLAUDE_CREDENTIALS", default_creds)

        wc = WorkCopy(state_dir=tmp_path, config_path=None, project_root=tmp_path,
                      extra={})
        handler = ClaudeCodeDataHandler()
        model = ModelConfig(model_id="claude-opus-4.6", provider="claude")

        with pytest.warns(UserWarning, match="api_base points to a \\.credentials\\.json path"):
            handler.apply_model_config(wc, model)

        assert json.loads((tmp_path / ".credentials.json").read_text()) == {
            "refreshToken": "refresh-token"
        }

    def test_claude_oauth_rejects_api_base_and_api_key(self, tmp_path):
        from clawarena.data_handlers.claude_code.handler import ClaudeCodeDataHandler
        from clawarena.core.types import WorkCopy

        wc = WorkCopy(state_dir=tmp_path, config_path=None, project_root=tmp_path,
                      extra={})
        handler = ClaudeCodeDataHandler()
        model = ModelConfig(
            model_id="claude-opus-4.6",
            provider="claude",
            api_base=str(tmp_path / "custom.credentials.json"),
            api_key="sk-ant-oat01-token",
        )

        with pytest.raises(ConfigError, match="api_base points to a \\.credentials\\.json path"):
            handler.apply_model_config(wc, model)

    def test_anthropic_direct(self, tmp_path):
        from clawarena.data_handlers.claude_code.handler import ClaudeCodeDataHandler
        from clawarena.core.types import WorkCopy

        wc = WorkCopy(state_dir=tmp_path, config_path=None, project_root=tmp_path,
                       extra={})
        handler = ClaudeCodeDataHandler()
        model = ModelConfig(model_id="claude-opus-4.6", provider="anthropic",
                            api_key="sk-ant-key", api_base="https://api.anthropic.com")
        handler.apply_model_config(wc, model)

        env = wc.extra["env_overrides"]
        assert env["ANTHROPIC_API_KEY"] == "sk-ant-key"
        assert env["ANTHROPIC_BASE_URL"] == "https://api.anthropic.com"

    def test_ccr_alias(self, tmp_path):
        from clawarena.data_handlers.claude_code.handler import ClaudeCodeDataHandler
        from clawarena.core.types import WorkCopy

        wc = WorkCopy(state_dir=tmp_path, config_path=None, project_root=tmp_path, extra={})
        handler = ClaudeCodeDataHandler()
        model = ModelConfig(
            model_id="gpt-5.1",
            provider="claude-code-router",
            api_base="http://127.0.0.1:3456",
            api_key="secret",
        )
        handler.apply_model_config(wc, model)

        env = wc.extra["env_overrides"]
        assert env["ANTHROPIC_BASE_URL"] == "http://127.0.0.1:3456"
        assert env["ANTHROPIC_AUTH_TOKEN"] == "secret"

    def test_classify_claude_provider(self):
        from clawarena.data_handlers.claude_code.handler import _classify_claude_provider

        assert _classify_claude_provider("claude") == "native-oauth"
        assert _classify_claude_provider("anthropic") == "native-api"
        assert _classify_claude_provider("ccr") == "external-ccr"
        assert _classify_claude_provider("claude-code-router") == "external-ccr"
        assert _classify_claude_provider("openai") == "auto-ccr"
        assert _classify_claude_provider("google") == "auto-ccr"
        assert _classify_claude_provider("bedrock") == "auto-ccr"

    def test_incompatible_provider_rejected(self, tmp_path):
        from clawarena.core.provider import ConfigError
        from clawarena.data_handlers.claude_code.handler import ClaudeCodeDataHandler
        from clawarena.core.types import WorkCopy

        wc = WorkCopy(state_dir=tmp_path, config_path=None, project_root=tmp_path, extra={})
        handler = ClaudeCodeDataHandler()
        for bad in ("bedrock", "codex"):
            model = ModelConfig(model_id="m", provider=bad, api_key="k")
            with pytest.raises(ConfigError):
                handler.apply_model_config(wc, model)




# ---------------------------------------------------------------------------
# build_model_env — per-framework
# ---------------------------------------------------------------------------

class TestClaudeCodeBuildModelEnv:
    def test_claude_oauth(self, tmp_path):
        from clawarena.data_handlers.claude_code.handler import ClaudeCodeDataHandler
        from clawarena.core.types import WorkCopy

        wc = WorkCopy(state_dir=tmp_path, config_path=None, project_root=tmp_path,
                       extra={})
        handler = ClaudeCodeDataHandler()
        model = ModelConfig(model_id="claude-opus-4.6", provider="claude",
                            api_key="sk-ant-oat01-token")
        env = handler.build_model_env(wc, model)
        assert env["CLAUDE_CODE_OAUTH_TOKEN"] == "sk-ant-oat01-token"
        assert "ANTHROPIC_BASE_URL" not in env

    def test_claude_oauth_credentials_path_returns_no_env(self, tmp_path):
        from clawarena.data_handlers.claude_code.handler import ClaudeCodeDataHandler
        from clawarena.core.types import WorkCopy

        creds_src = tmp_path / "custom.credentials.json"
        creds_src.write_text(json.dumps({"accessToken": "oauth-token"}))

        wc = WorkCopy(state_dir=tmp_path, config_path=None, project_root=tmp_path,
                      extra={})
        handler = ClaudeCodeDataHandler()
        model = ModelConfig(
            model_id="claude-opus-4.6",
            provider="claude",
            api_base=str(creds_src),
        )

        env = handler.build_model_env(wc, model)
        assert env == {}

    def test_claude_oauth_rejects_api_base_and_api_key(self, tmp_path):
        from clawarena.data_handlers.claude_code.handler import ClaudeCodeDataHandler
        from clawarena.core.types import WorkCopy

        wc = WorkCopy(state_dir=tmp_path, config_path=None, project_root=tmp_path,
                      extra={})
        handler = ClaudeCodeDataHandler()
        model = ModelConfig(
            model_id="claude-opus-4.6",
            provider="claude",
            api_base=str(tmp_path / "custom.credentials.json"),
            api_key="sk-ant-oat01-token",
        )

        with pytest.raises(ConfigError, match="api_base points to a \\.credentials\\.json path"):
            handler.build_model_env(wc, model)

    def test_anthropic(self, tmp_path):
        from clawarena.data_handlers.claude_code.handler import ClaudeCodeDataHandler
        from clawarena.core.types import WorkCopy

        wc = WorkCopy(state_dir=tmp_path, config_path=None, project_root=tmp_path,
                       extra={})
        handler = ClaudeCodeDataHandler()
        model = ModelConfig(model_id="claude-opus-4.6", provider="anthropic",
                            api_key="sk-ant-key", api_base="https://api.anthropic.com")
        env = handler.build_model_env(wc, model)
        assert env["ANTHROPIC_API_KEY"] == "sk-ant-key"
        assert env["ANTHROPIC_BASE_URL"] == "https://api.anthropic.com"




class TestOpenClawBuildModelEnv:
    def test_overlay_created(self, tmp_path):
        from clawarena.data_handlers.openclaw.handler import OpenClawDataHandler
        from clawarena.core.types import WorkCopy

        state = tmp_path / "state"
        state.mkdir()
        cfg = {"models": {}, "agents": {"defaults": {}, "list": []}}
        (state / "openclaw.json").write_text(json.dumps(cfg))

        wc = WorkCopy(state_dir=state, config_path=None, project_root=tmp_path)
        handler = OpenClawDataHandler()
        model = ModelConfig(model_id="gpt-4o", provider="openai",
                            api_key="sk-test", api_base="http://proxy")
        env = handler.build_model_env(wc, model)

        assert "OPENCLAW_CONFIG_PATH" in env
        overlay_cfg = json.loads(Path(env["OPENCLAW_CONFIG_PATH"]).read_text())
        assert "openai" in overlay_cfg["models"]["providers"]

    def test_overlay_idempotent(self, tmp_path):
        from clawarena.data_handlers.openclaw.handler import OpenClawDataHandler
        from clawarena.core.types import WorkCopy

        state = tmp_path / "state"
        state.mkdir()
        cfg = {"models": {}, "agents": {"defaults": {}, "list": []}}
        (state / "openclaw.json").write_text(json.dumps(cfg))

        wc = WorkCopy(state_dir=state, config_path=None, project_root=tmp_path)
        handler = OpenClawDataHandler()
        model = ModelConfig(model_id="gpt-4o", provider="openai", api_base="http://proxy")
        env1 = handler.build_model_env(wc, model)
        env2 = handler.build_model_env(wc, model)
        assert env1["OPENCLAW_CONFIG_PATH"] == env2["OPENCLAW_CONFIG_PATH"]

    def test_codex_overlay_writes_auth_profiles(self, tmp_path):
        from clawarena.data_handlers.openclaw.handler import OpenClawDataHandler
        from clawarena.core.types import WorkCopy

        state = tmp_path / "state"
        state.mkdir()
        agent_dir = state / "agents" / "hil_e5"
        agent_dir.mkdir(parents=True)
        cfg = {
            "agents": {
                "defaults": {},
                "list": [{"agentDir": str(agent_dir)}],
            }
        }
        (state / "openclaw.json").write_text(json.dumps(cfg))
        auth_json = tmp_path / "auth.json"
        auth_json.write_text(json.dumps({
            "tokens": {
                "access_token": "ey-access",
                "refresh_token": "rt-refresh",
                "account_id": "acct-123",
            },
            "last_refresh": "2026-04-12T09:08:18.507920Z",
        }))

        wc = WorkCopy(state_dir=state, config_path=None, project_root=tmp_path)
        handler = OpenClawDataHandler()
        model = ModelConfig(
            model_id="gpt-5-codex",
            provider="codex",
            api_key=str(auth_json),
        )
        env = handler.build_model_env(wc, model)

        assert "OPENCLAW_CONFIG_PATH" in env
        overlay_cfg = json.loads(Path(env["OPENCLAW_CONFIG_PATH"]).read_text())
        assert "openai-codex" in overlay_cfg["models"]["providers"]
        assert overlay_cfg["models"]["providers"]["openai-codex"]["baseUrl"] == "https://chatgpt.com/backend-api"
        assert overlay_cfg["models"]["providers"]["openai-codex"]["api"] == "openai-codex-responses"
        assert "openai-codex:default" in overlay_cfg["auth"]["profiles"]
        assert overlay_cfg["auth"]["order"]["openai-codex"] == ["openai-codex:default"]
        auth_profile = json.loads((agent_dir / "auth-profiles.json").read_text())
        assert auth_profile["profiles"]["openai-codex:default"]["expires"] == 1778576898507


class TestPicoClawBuildModelEnv:
    def test_overlay_created(self, tmp_path):
        from clawarena.data_handlers.picoclaw.handler import PicoClawDataHandler
        from clawarena.core.types import WorkCopy

        state = tmp_path / "state"
        state.mkdir()
        (state / "config.json").write_text(json.dumps({"model_list": [], "agents": {}}))

        wc = WorkCopy(state_dir=state, config_path=None, project_root=tmp_path)
        handler = PicoClawDataHandler()
        model = ModelConfig(model_id="gpt-4o", provider="openai",
                            api_base="http://proxy", api_key="sk-test")
        env = handler.build_model_env(wc, model)

        assert "PICOCLAW_CONFIG" in env
        overlay_cfg = json.loads(Path(env["PICOCLAW_CONFIG"]).read_text())
        assert overlay_cfg["model_list"][0]["model"] == "openai/gpt-4o"
        assert overlay_cfg["model_list"][0]["api_key"] == "sk-test"


class TestNanobotBuildModelEnv:
    def test_overlay_created(self, tmp_path):
        from clawarena.data_handlers.nanobot.handler import NanobotDataHandler
        from clawarena.core.types import WorkCopy

        state = tmp_path / "state"
        state.mkdir()
        (state / "config.json").write_text(json.dumps({"providers": {}, "agents": {}}))

        wc = WorkCopy(state_dir=state, config_path=None, project_root=tmp_path)
        handler = NanobotDataHandler()
        model = ModelConfig(model_id="llama3", provider="ollama",
                            api_base="http://localhost:11434")
        env = handler.build_model_env(wc, model)

        assert "NANOBOT_CONFIG" in env
        overlay_cfg = json.loads(Path(env["NANOBOT_CONFIG"]).read_text())
        assert "ollama" in overlay_cfg["providers"]

    def test_openai_compatible_proxy_uses_custom_provider(self, tmp_path):
        from clawarena.data_handlers.nanobot.handler import NanobotDataHandler
        from clawarena.core.types import WorkCopy

        state = tmp_path / "state"
        state.mkdir()
        (state / "config.json").write_text(json.dumps({"providers": {}, "agents": {}}))

        wc = WorkCopy(state_dir=state, config_path=None, project_root=tmp_path)
        handler = NanobotDataHandler()
        model = ModelConfig(
            model_id="gpt-5.1",
            provider="openai",
            api_base="https://proxy.example/v1",
            api_key="sk-test",
        )
        env = handler.build_model_env(wc, model)

        assert "NANOBOT_CONFIG" in env
        overlay_cfg = json.loads(Path(env["NANOBOT_CONFIG"]).read_text())
        assert "custom" in overlay_cfg["providers"]
        assert overlay_cfg["providers"]["custom"]["apiBase"] == "https://proxy.example/v1"
        assert overlay_cfg["providers"]["custom"]["apiKey"] == "sk-test"
        assert overlay_cfg["agents"]["defaults"]["model"] == "gpt-5.1"
        assert overlay_cfg["agents"]["defaults"]["provider"] == "custom"

    def test_claude_raises(self, tmp_path):
        from clawarena.data_handlers.nanobot.handler import NanobotDataHandler
        from clawarena.core.types import WorkCopy

        state = tmp_path / "state"
        state.mkdir()
        wc = WorkCopy(state_dir=state, config_path=None, project_root=tmp_path)
        handler = NanobotDataHandler()
        model = ModelConfig(model_id="x", provider="claude")
        with pytest.raises(ConfigError):
            handler.build_model_env(wc, model)




# ---------------------------------------------------------------------------
# Extended providers — validation
# ---------------------------------------------------------------------------

class TestExtendedProviders:
    """Verify extended providers pass VALID_PROVIDERS check and resolve defaults."""

    from clawarena.core.provider import VALID_PROVIDERS, DEFAULT_API_BASE

    @pytest.mark.parametrize("provider", [
        "openrouter", "groq", "mistral", "xai",
        "qwen", "moonshot", "glm", "minimax",
        "copilot", "telnyx", "codex",
    ])
    def test_in_valid_providers(self, provider):
        from clawarena.core.provider import VALID_PROVIDERS
        assert provider in VALID_PROVIDERS

    @pytest.mark.parametrize("provider,expected_fragment", [
        ("openrouter", "openrouter.ai"),
        ("groq", "groq.com"),
        ("mistral", "mistral.ai"),
        ("xai", "x.ai"),
        ("qwen", "dashscope"),
        ("moonshot", "moonshot.cn"),
        ("glm", "bigmodel.cn"),
        ("minimax", "minimax.chat"),
        ("codex", ""),
    ])
    def test_default_api_base(self, provider, expected_fragment):
        m = ModelConfig(model_id="test", provider=provider)
        assert expected_fragment in m.resolved_api_base()
