"""Tests for the mm-metaclaw overlay.

Covers:
* config parsing (load_config, parse_trigger_config)
* hooks in proxy mode (trigger logic, skip-on-final)
* hooks in http mode (before_round inject, on_round_complete collect)
* apply_overlay utility
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio

from clawarena.core.io import apply_overlay
from clawarena.overlays.mm_metaclaw.config import (
    MmMetaClawConfig,
    TriggerCfg,
    load_config,
    parse_trigger_config,
)
from clawarena.overlays.mm_metaclaw.run_dir import MmMetaClawRunDir
from clawarena.overlays.mm_metaclaw.hooks import MmMetaClawHooks


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def gateway_dir(tmp_path: Path) -> Path:
    gd = tmp_path / "gateway-modules"
    gd.mkdir()
    return gd


@pytest.fixture()
def proxy_cfg(gateway_dir: Path) -> MmMetaClawConfig:
    return MmMetaClawConfig(
        gateway_dir=gateway_dir,
        enabled_modules=["proxy", "memory", "skill"],
        transport_mode="proxy",
        hook_mode="proxy",
    )


@pytest.fixture()
def http_cfg(gateway_dir: Path) -> MmMetaClawConfig:
    return MmMetaClawConfig(
        gateway_dir=gateway_dir,
        enabled_modules=["proxy", "memory", "skill"],
        transport_mode="proxy",
        hook_mode="http",
    )


# ---------------------------------------------------------------------------
# Config tests
# ---------------------------------------------------------------------------


class TestConfig:
    def test_load_config_minimal(self, gateway_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GW_DIR", str(gateway_dir))
        raw = {
            "gateway_dir": "${GW_DIR}",
            "transport_mode": "proxy",
            "enabled_modules": ["proxy", "memory"],
            "hook_mode": "proxy",
        }
        cfg = load_config(raw)
        assert cfg.gateway_dir == gateway_dir
        assert cfg.enabled_modules == ["proxy", "memory"]
        assert cfg.transport_mode == "proxy"
        assert cfg.hook_mode == "proxy"

    def test_load_config_http_mode(self, gateway_dir: Path) -> None:
        raw = {"gateway_dir": str(gateway_dir), "hook_mode": "http"}
        cfg = load_config(raw)
        assert cfg.hook_mode == "http"

    def test_load_config_http_plugin_strips_proxy(self, gateway_dir: Path) -> None:
        raw = {
            "gateway_dir": str(gateway_dir),
            "transport_mode": "http_plugin",
            "enabled_modules": ["proxy", "memory", "skill"],
        }
        cfg = load_config(raw)
        assert cfg.transport_mode == "http_plugin"
        assert cfg.enabled_modules == ["memory", "skill"]

    def test_load_config_proxy_mode_adds_proxy(self, gateway_dir: Path) -> None:
        raw = {
            "gateway_dir": str(gateway_dir),
            "transport_mode": "proxy",
            "enabled_modules": ["memory", "skill"],
        }
        cfg = load_config(raw)
        assert cfg.enabled_modules == ["proxy", "memory", "skill"]

    def test_load_config_invalid_module(self, gateway_dir: Path) -> None:
        with pytest.raises(ValueError, match="unsupported modules"):
            load_config({"gateway_dir": str(gateway_dir), "enabled_modules": ["proxy", "rl"]})

    def test_load_config_invalid_hook_mode(self, gateway_dir: Path) -> None:
        with pytest.raises(ValueError, match="hook_mode"):
            load_config({"gateway_dir": str(gateway_dir), "hook_mode": "magic"})

    def test_load_config_missing_gateway_dir(self) -> None:
        with pytest.raises(ValueError, match="gateway_dir"):
            load_config({})

    def test_parse_trigger_every_n(self, gateway_dir: Path) -> None:
        raw = {
            "gateway_dir": str(gateway_dir),
            "memory_trigger": {"every_n_rounds": 3, "on_last_round": False},
        }
        trig = parse_trigger_config(raw)
        assert trig.every_n_rounds == 3
        assert trig.on_last_round is False

    def test_parse_trigger_on_last_round(self, gateway_dir: Path) -> None:
        raw = {"gateway_dir": str(gateway_dir), "memory_trigger": {"on_last_round": True}}
        trig = parse_trigger_config(raw)
        assert trig.on_last_round is True

    def test_run_dir_isolates_memory_per_run(self, gateway_dir: Path, tmp_path: Path) -> None:
        cfg = MmMetaClawConfig(
            gateway_dir=gateway_dir,
            enabled_modules=["proxy", "memory"],
            transport_mode="proxy",
        )
        run_dir = MmMetaClawRunDir.create(cfg, tmp_path, "run123")
        try:
            assert run_dir.memory_data_dir == tmp_path / "mm_metaclaw_run123" / "memory_data"
            assert run_dir.memory_data_dir is not None
            assert str(run_dir.memory_data_dir).startswith(str(tmp_path))
            assert not str(run_dir.memory_data_dir).startswith(str(gateway_dir / "memory_data"))
        finally:
            run_dir.cleanup()


# ---------------------------------------------------------------------------
# apply_overlay tests
# ---------------------------------------------------------------------------


class TestApplyOverlay:
    def _base(self) -> dict:
        return {
            "frameworks": {"openclaw": {"manifest": "x"}},
            "tests": [],
            "metaclaw": {"enabled": False},
            "mm_metaclaw": {"enabled": False, "transport_mode": "proxy", "hook_mode": "proxy"},
        }

    def test_no_overlay(self) -> None:
        cfg = self._base()
        assert apply_overlay(cfg, None) is cfg

    def test_overlay_mm_metaclaw(self) -> None:
        cfg = self._base()
        result = apply_overlay(
            cfg,
            '{"mm_metaclaw": {"enabled": true, "transport_mode": "http_plugin", "hook_mode": "http"}}',
        )
        assert result["mm_metaclaw"]["enabled"] is True
        assert result["mm_metaclaw"]["transport_mode"] == "http_plugin"
        assert result["mm_metaclaw"]["hook_mode"] == "http"
        # Unmentioned key preserved
        assert "enabled" in result["mm_metaclaw"]

    def test_overlay_metaclaw(self) -> None:
        cfg = self._base()
        result = apply_overlay(cfg, '{"metaclaw": {"enabled": true}}')
        assert result["metaclaw"]["enabled"] is True

    def test_overlay_both_sections(self) -> None:
        cfg = self._base()
        result = apply_overlay(cfg, '{"metaclaw": {"enabled": false}, "mm_metaclaw": {"enabled": true}}')
        assert result["metaclaw"]["enabled"] is False
        assert result["mm_metaclaw"]["enabled"] is True

    def test_overlay_invalid_json(self) -> None:
        with pytest.raises(ValueError, match="invalid JSON"):
            apply_overlay(self._base(), "{not json}")

    def test_overlay_disallowed_key(self) -> None:
        with pytest.raises(ValueError, match="only"):
            apply_overlay(self._base(), '{"frameworks": {}}')

    def test_overlay_preserves_original(self) -> None:
        """apply_overlay must not mutate the original dict."""
        cfg = self._base()
        _ = apply_overlay(cfg, '{"mm_metaclaw": {"enabled": true}}')
        assert cfg["mm_metaclaw"]["enabled"] is False


# ---------------------------------------------------------------------------
# Hooks — proxy mode
# ---------------------------------------------------------------------------


class TestHooksProxyMode:
    def _make_hooks(self, cfg: MmMetaClawConfig, trigger: TriggerCfg, total_scenes: int = 2) -> MmMetaClawHooks:
        return MmMetaClawHooks(
            gateway_url="http://127.0.0.1:30100",
            config=cfg,
            memory_trigger=trigger,
            total_scenes=total_scenes,
        )

    @pytest.mark.asyncio
    async def test_before_round_is_noop_in_proxy_mode(self, proxy_cfg: MmMetaClawConfig) -> None:
        hooks = self._make_hooks(proxy_cfg, TriggerCfg())
        result = await hooks.before_round("sess1", [{"role": "user", "content": "hi"}])
        assert result == {}
        assert hooks.memory_inject_count == 0
        assert hooks.skill_inject_count == 0

    @pytest.mark.asyncio
    async def test_collect_triggered_every_n_rounds(self, proxy_cfg: MmMetaClawConfig) -> None:
        hooks = self._make_hooks(proxy_cfg, TriggerCfg(every_n_rounds=2), total_scenes=2)
        with patch(
            "clawarena.overlays.mm_metaclaw.hooks._http_post",
            new_callable=AsyncMock,
            return_value={"ok": True},
        ):
            # Round 0 (count=1) — not yet
            await hooks.on_round_complete(0, 3, False, "s", [])
            assert hooks.memory_collect_count == 0
            # Round 1 (count=2) — trigger
            await hooks.on_round_complete(1, 3, False, "s", [])
            assert hooks.memory_collect_count == 1

    @pytest.mark.asyncio
    async def test_collect_on_last_round(self, proxy_cfg: MmMetaClawConfig) -> None:
        hooks = self._make_hooks(proxy_cfg, TriggerCfg(on_last_round=True), total_scenes=2)
        with patch(
            "clawarena.overlays.mm_metaclaw.hooks._http_post",
            new_callable=AsyncMock,
            return_value={"ok": True},
        ):
            await hooks.on_round_complete(0, 2, False, "s", [])
            assert hooks.memory_collect_count == 0
            # Last round of scene 1 (not last scene) — triggers
            await hooks.on_round_complete(1, 2, True, "s", [])
            assert hooks.memory_collect_count == 1

    @pytest.mark.asyncio
    async def test_skip_on_final_interaction(self, proxy_cfg: MmMetaClawConfig) -> None:
        """Trigger must be skipped on the last round of the last scene."""
        hooks = self._make_hooks(proxy_cfg, TriggerCfg(on_last_round=True), total_scenes=1)
        with patch(
            "clawarena.overlays.mm_metaclaw.hooks._http_post",
            new_callable=AsyncMock,
            return_value={"ok": True},
        ) as mock_post:
            await hooks.on_round_complete(0, 1, True, "s", [])
            mock_post.assert_not_called()
            assert hooks.memory_collect_count == 0

    @pytest.mark.asyncio
    async def test_no_collect_when_module_disabled(self, gateway_dir: Path) -> None:
        cfg = MmMetaClawConfig(
            gateway_dir=gateway_dir,
            enabled_modules=["proxy"],   # memory NOT enabled
            hook_mode="proxy",
        )
        hooks = self._make_hooks(cfg, TriggerCfg(on_last_round=True), total_scenes=2)
        with patch(
            "clawarena.overlays.mm_metaclaw.hooks._http_post",
            new_callable=AsyncMock,
            return_value={"ok": True},
        ) as mock_post:
            await hooks.on_round_complete(0, 2, True, "s", [])
            mock_post.assert_not_called()


# ---------------------------------------------------------------------------
# Hooks — http mode
# ---------------------------------------------------------------------------


class TestHooksHttpMode:
    def _make_hooks(self, cfg: MmMetaClawConfig, trigger: TriggerCfg, total_scenes: int = 2) -> MmMetaClawHooks:
        return MmMetaClawHooks(
            gateway_url="http://127.0.0.1:30100",
            config=cfg,
            memory_trigger=trigger,
            total_scenes=total_scenes,
        )

    @pytest.mark.asyncio
    async def test_before_round_calls_inject_endpoints(self, http_cfg: MmMetaClawConfig) -> None:
        hooks = self._make_hooks(http_cfg, TriggerCfg())
        with patch(
            "clawarena.overlays.mm_metaclaw.hooks._http_post",
            new_callable=AsyncMock,
            return_value={"additional_context": "test context"},
        ) as mock_post:
            result = await hooks.before_round("sess1", [{"role": "user", "content": "hi"}])
            # Both memory/inject and skill/inject should be called
            calls = [str(c.args[0]) for c in mock_post.call_args_list]
            assert any("/v1/memory/inject" in u for u in calls)
            assert any("/v1/skill/inject" in u for u in calls)
            assert result  # non-empty context returned

    @pytest.mark.asyncio
    async def test_on_round_complete_calls_collect_every_round(self, http_cfg: MmMetaClawConfig) -> None:
        hooks = self._make_hooks(http_cfg, TriggerCfg(), total_scenes=2)
        with patch(
            "clawarena.overlays.mm_metaclaw.hooks._http_post",
            new_callable=AsyncMock,
            return_value={"ok": True},
        ) as mock_post:
            await hooks.on_round_complete(0, 3, False, "s", [])
            calls = [str(c.args[0]) for c in mock_post.call_args_list]
            assert any("/v1/memory/collect" in u for u in calls)
            assert any("/v1/skill/collect" in u for u in calls)

    @pytest.mark.asyncio
    async def test_on_round_complete_http_ignores_trigger_cfg(self, http_cfg: MmMetaClawConfig) -> None:
        """In http mode, collect runs on every round regardless of trigger config."""
        hooks = self._make_hooks(
            http_cfg, TriggerCfg(every_n_rounds=100, on_last_round=False), total_scenes=5
        )
        with patch(
            "clawarena.overlays.mm_metaclaw.hooks._http_post",
            new_callable=AsyncMock,
            return_value={"ok": True},
        ) as mock_post:
            await hooks.on_round_complete(0, 5, False, "s", [])
            assert mock_post.call_count >= 1  # collect fired despite trigger cfg

    @pytest.mark.asyncio
    async def test_before_round_only_calls_enabled_modules(self, gateway_dir: Path) -> None:
        """Only memory/inject should be called when skill is not in enabled_modules."""
        cfg = MmMetaClawConfig(
            gateway_dir=gateway_dir,
            enabled_modules=["proxy", "memory"],   # skill NOT enabled
            hook_mode="http",
        )
        hooks = self._make_hooks(cfg, TriggerCfg())
        with patch(
            "clawarena.overlays.mm_metaclaw.hooks._http_post",
            new_callable=AsyncMock,
            return_value={"ok": True},
        ) as mock_post:
            await hooks.before_round("sess1", [])
            calls = [str(c.args[0]) for c in mock_post.call_args_list]
            assert any("/v1/memory/inject" in u for u in calls)
            assert not any("/v1/skill/inject" in u for u in calls)
