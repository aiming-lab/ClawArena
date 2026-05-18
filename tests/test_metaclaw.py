"""Tests for the MetaClaw integration module."""

import json
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, patch

from clawarena.core.provider import ModelConfig
from clawarena.overlays.metaclaw.config import (
    MetaClawConfig,
    TriggerCfg,
    load_config,
    parse_trigger_config,
    _expand_env,
)
from clawarena.overlays.metaclaw.hooks import MetaClawHooks
from clawarena.overlays.metaclaw.run_dir import MetaClawRunDir, BENCH_POLICY
from clawarena.overlays.metaclaw.report import MetaClawRunReport, _render_markdown, write_report


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

class TestConfig:
    def test_expand_env(self, monkeypatch):
        monkeypatch.setenv("X", "hello")
        assert _expand_env("${X}") == "hello"
        assert _expand_env("${MISSING:-default}") == "default"

    def test_load_config(self, tmp_path):
        cfg_path = tmp_path / "mc.yaml"
        cfg_path.write_text(
            "memory:\n  enabled: true\n  scope: default\n"
            "skills:\n  enabled: false\n"
            "rl:\n  enabled: false\n"
            "served_model_name: test-model\n"
        )
        cfg = load_config(cfg_path)
        assert cfg.memory.enabled is True
        assert cfg.skills.enabled is False
        assert cfg.served_model_name == "test-model"

    def test_parse_trigger_config(self, monkeypatch):
        monkeypatch.setenv("MEM_ROUNDS", "3")
        raw = {
            "memory_trigger": {
                "every_n_rounds": "${MEM_ROUNDS}",
                "every_n_scenes": 1,
                "on_last_round": True,
            },
            "rl_trigger": {
                "every_n_rounds": 0,
                "every_n_scenes": 5,
                "on_last_round": False,
            },
        }
        mem, rl = parse_trigger_config(raw)
        assert mem.every_n_rounds == 3
        assert mem.on_last_round is True
        assert rl.every_n_scenes == 5


# ---------------------------------------------------------------------------
# RunDir
# ---------------------------------------------------------------------------

class TestRunDir:
    def test_create_memory_only(self, tmp_path):
        cfg = MetaClawConfig(memory=type(cfg.memory)(enabled=True) if False else None)
        # Build config properly
        from clawarena.overlays.metaclaw.config import MemoryCfg, SkillsCfg, RLCfg
        cfg = MetaClawConfig(
            memory=MemoryCfg(enabled=True),
            skills=SkillsCfg(enabled=False),
            rl=RLCfg(enabled=False),
        )
        rd = MetaClawRunDir.create(cfg, tmp_path, "test_run")
        assert rd.root.exists()
        assert rd.memory_store_dir is not None
        assert rd.memory_store_dir.exists()
        assert rd.skills_snapshot_dir is None
        # policy.json written
        policy = json.loads((rd.memory_store_dir / "policy.json").read_text())
        assert policy["retrieval_mode"] == "hybrid"

    def test_create_skills(self, tmp_path):
        from clawarena.overlays.metaclaw.config import MemoryCfg, SkillsCfg, RLCfg
        skills_src = tmp_path / "src_skills"
        skills_src.mkdir()
        (skills_src / "skill1.py").write_text("pass")

        cfg = MetaClawConfig(
            memory=MemoryCfg(enabled=False),
            skills=SkillsCfg(enabled=True, dir=str(skills_src)),
            rl=RLCfg(enabled=False),
        )
        work = tmp_path / "work"
        work.mkdir()
        rd = MetaClawRunDir.create(cfg, work, "test_skills")
        assert rd.skills_snapshot_dir is not None
        assert (rd.skills_snapshot_dir / "skill1.py").exists()
        meta = json.loads((rd.root / "skills_meta.json").read_text())
        assert meta["count_before"] == 1

    def test_cleanup_tmp(self, tmp_path):
        from clawarena.overlays.metaclaw.config import MemoryCfg, SkillsCfg, RLCfg
        cfg = MetaClawConfig(
            memory=MemoryCfg(enabled=False),
            skills=SkillsCfg(enabled=False),
            rl=RLCfg(enabled=False),
        )
        rd = MetaClawRunDir.create(cfg, tmp_path, "clean_test")
        assert rd.tmp_config_path.exists()
        rd.cleanup_tmp()
        assert not rd.tmp_config_path.exists()


# ---------------------------------------------------------------------------
# Hooks — trigger logic
# ---------------------------------------------------------------------------

class TestHooks:
    """Trigger logic tests.

    Key behavioural rule (matching the original MetaClaw benchmark):
    triggers are **skipped** on the final interaction of a run because no
    subsequent rounds would benefit from the updated state.
    - Global mode: skip on last round of last scene.
    - Isolation mode: skip on each scene's last round.
    """

    def _make_hooks(self, mem_cfg=None, rl_cfg=None, isolation=False, total_scenes=2):
        from clawarena.overlays.metaclaw.config import MemoryCfg, SkillsCfg, RLCfg
        mc = MetaClawConfig(
            memory=MemoryCfg(enabled=True, manual_trigger=True),
            skills=SkillsCfg(enabled=False),
            rl=RLCfg(enabled=True, manual_train_trigger=True),
        )
        return MetaClawHooks(
            proxy_url="http://127.0.0.1:9999",
            mc_config=mc,
            memory_trigger=mem_cfg or TriggerCfg(every_n_rounds=3, on_last_round=True),
            rl_trigger=rl_cfg or TriggerCfg(every_n_scenes=2, on_last_round=False),
            per_scene_isolation=isolation,
            total_scenes=total_scenes,
        )

    @pytest.mark.asyncio
    async def test_unmanaged_mode_no_config(self):
        """mc_config=None (unmanaged mode) — hooks still fire based on trigger cfg."""
        hooks = MetaClawHooks(
            proxy_url="http://127.0.0.1:30000",
            mc_config=None,
            memory_trigger=TriggerCfg(every_n_rounds=2, on_last_round=False),
            rl_trigger=TriggerCfg(every_n_rounds=0, on_last_round=False),
            per_scene_isolation=False,
            total_scenes=1,
        )
        with patch("clawarena.overlays.metaclaw.hooks._http_post_json", new_callable=AsyncMock, return_value=True):
            await hooks.on_round_complete(0, 4, False)
            await hooks.on_round_complete(1, 4, False)
        assert hooks.memory_ingest_count == 1

    @pytest.mark.asyncio
    async def test_global_every_n_rounds(self):
        """every_n_rounds=3 + on_last_round=True (default), 2 scenes × 4 rounds.
        - seen=3 (round 3, not last) → every_n_rounds ✓
        - seen=4 (scene 1 last round, not last scene) → on_last_round ✓
        - seen=6 (round 6, not last) → every_n_rounds ✓
        - seen=8 (scene 2 last round, last scene) → skipped
        Total: 3 triggers.
        """
        hooks = self._make_hooks(total_scenes=2)
        with (
            patch("clawarena.overlays.metaclaw.hooks._http_post_json", new_callable=AsyncMock, return_value=True),
            patch("clawarena.overlays.metaclaw.hooks._run_train_step", new_callable=AsyncMock, return_value=True),
        ):
            for i in range(8):
                await hooks.on_round_complete(
                    round_index=i % 4, total_rounds=4, is_last_round=(i % 4 == 3),
                )
        assert hooks.memory_ingest_count == 3

    @pytest.mark.asyncio
    async def test_global_on_last_round(self):
        """on_last_round triggers on each scene's last round EXCEPT the last scene."""
        hooks = self._make_hooks(
            mem_cfg=TriggerCfg(every_n_rounds=0, on_last_round=True),
        )
        with patch("clawarena.overlays.metaclaw.hooks._http_post_json", new_callable=AsyncMock, return_value=True):
            # Scene 1: 2 rounds — last round triggers (not last scene)
            await hooks.on_round_complete(0, 2, False)
            await hooks.on_round_complete(1, 2, True)
            # Scene 2: 2 rounds (last scene) — last round skipped
            await hooks.on_round_complete(0, 2, False)
            await hooks.on_round_complete(1, 2, True)
        assert hooks.memory_ingest_count == 1

    @pytest.mark.asyncio
    async def test_isolation_every_n_rounds_skips_last(self):
        hooks = self._make_hooks(
            mem_cfg=TriggerCfg(every_n_rounds=2, on_last_round=False),
            isolation=True,
        )
        with patch("clawarena.overlays.metaclaw.hooks._http_post_json", new_callable=AsyncMock, return_value=True):
            # 4 rounds in one scene
            await hooks.on_round_complete(0, 4, False)  # idx 0 → (0+1)%2≠0
            await hooks.on_round_complete(1, 4, False)  # idx 1 → (1+1)%2=0 ✓
            await hooks.on_round_complete(2, 4, False)  # idx 2 → (2+1)%2≠0
            await hooks.on_round_complete(3, 4, True)   # last round → skip
        assert hooks.memory_ingest_count == 1

    @pytest.mark.asyncio
    async def test_isolation_on_last_round_always_skipped(self):
        """In isolation mode, last round is always skipped (nothing follows)."""
        hooks = self._make_hooks(
            mem_cfg=TriggerCfg(every_n_rounds=0, on_last_round=True),
            isolation=True,
        )
        with patch("clawarena.overlays.metaclaw.hooks._http_post_json", new_callable=AsyncMock, return_value=True):
            await hooks.on_round_complete(0, 2, False)
            await hooks.on_round_complete(1, 2, True)
        # on_last_round would fire but isolation skips all last-round triggers
        assert hooks.memory_ingest_count == 0

    @pytest.mark.asyncio
    async def test_rl_every_n_scenes(self):
        """every_n_scenes=1 with 3 scenes: scene 1 and 2 trigger, scene 3 skipped (last)."""
        hooks = self._make_hooks(
            rl_cfg=TriggerCfg(every_n_scenes=1, on_last_round=False),
            total_scenes=3,
        )
        with patch("clawarena.overlays.metaclaw.hooks._run_train_step", new_callable=AsyncMock, return_value=True):
            for scene in range(3):
                for r in range(2):
                    await hooks.on_round_complete(r, 2, r == 1)
        # 3 scenes, every_n_scenes=1 → triggers after scene 1 & 2, skips scene 3 (last)
        assert hooks.rl_train_count == 2

    @pytest.mark.asyncio
    async def test_global_last_scene_last_round_never_triggers(self):
        """The very last round of the very last scene never triggers anything."""
        hooks = self._make_hooks(
            mem_cfg=TriggerCfg(every_n_rounds=1, on_last_round=True),
            rl_cfg=TriggerCfg(every_n_rounds=1, on_last_round=True),
            total_scenes=1,
        )
        with (
            patch("clawarena.overlays.metaclaw.hooks._http_post_json", new_callable=AsyncMock, return_value=True),
            patch("clawarena.overlays.metaclaw.hooks._run_train_step", new_callable=AsyncMock, return_value=True),
        ):
            # Single scene, single round → last round of last scene
            await hooks.on_round_complete(0, 1, True)
        assert hooks.memory_ingest_count == 0
        assert hooks.rl_train_count == 0


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

class TestReport:
    def test_render_markdown(self):
        r = MetaClawRunReport(
            run_id="test",
            elapsed_seconds=42.0,
            framework="openclaw",
            test_count=5,
            mode_flags={"memory": True, "skills": False, "rl": False},
            triggers={"memory_ingest": 10, "rl_train": 0, "scenes_completed": 5},
            config_summary={"served_model_name": "mc", "max_context_tokens": 50000},
        )
        md = _render_markdown(r)
        assert "# MetaClaw Run Report" in md
        assert "memory_ingest" in md
        assert "memory" in md  # mode

    def test_write_report(self, tmp_path):
        r = MetaClawRunReport(
            run_id="test",
            config_summary={},
            mode_flags={},
            triggers={},
        )
        write_report(r, tmp_path)
        assert (tmp_path / "metaclaw_report.json").exists()
        assert (tmp_path / "metaclaw_report.md").exists()


# ---------------------------------------------------------------------------
# Check integration — model / metaclaw validation
# ---------------------------------------------------------------------------

class TestCheckModelValidation:
    def _make_tests_json(self, tmp_path, model=None, metaclaw=None, fw_model=None):
        """Create a minimal valid tests.json with optional model/metaclaw fields."""
        base = tmp_path / "bench"
        base.mkdir()

        eval_dir = base / "eval" / "t1"
        eval_dir.mkdir(parents=True)
        q = {"rounds": [
            {"id": "r1", "type": "multi_choice", "question": "?",
             "update_ids": [],
             "eval": {"options": {"A": "a"}, "answer": ["A"]},
             "feedback": {"correct": "ok", "options": {"A": "explanation"}}},
        ]}
        (eval_dir / "questions.json").write_text(json.dumps(q))

        oc = base / "openclaw"
        (oc / "config").mkdir(parents=True)
        (oc / "state" / "agents" / "t1" / "sessions").mkdir(parents=True)
        (oc / "workspaces" / "t1").mkdir(parents=True)
        config = {"agents": {"list": [{"id": "t1"}]}}
        (oc / "config" / "openclaw.json").write_text(json.dumps(config))
        sess_dir = oc / "state" / "agents" / "t1" / "sessions"
        (sess_dir / "main.jsonl").touch()
        (sess_dir / "sessions.json").write_text("{}")

        manifest = {
            "framework": "openclaw",
            "config_file": "config/openclaw.json",
            "state_dir": "state",
            "agents": {
                "t1": {
                    "agent_id": "t1", "agent_dir": "state/agents/t1",
                    "session": "main", "history_sessions": [],
                    "workspace": "workspaces/t1",
                },
            },
            "updates": {},
        }
        (oc / "manifest.json").write_text(json.dumps(manifest))

        fw_cfg: dict = {"manifest": "openclaw/manifest.json"}
        if fw_model:
            fw_cfg["model"] = fw_model

        tests_json: dict = {
            "eval_dir": "eval",
            "frameworks": {"openclaw": fw_cfg},
            "tests": [{"id": "t1", "desc": "Test 1", "eval": "t1"}],
        }
        if model:
            tests_json["model"] = model
        if metaclaw:
            tests_json["metaclaw"] = metaclaw

        p = base / "tests.json"
        p.write_text(json.dumps(tests_json))
        return p

    def test_invalid_provider(self, tmp_path, capsys):
        from clawarena.core.check import run_check
        p = self._make_tests_json(tmp_path, model={"model_id": "x", "provider": "bad"})
        ok = run_check(p)
        assert ok is False
        assert "unknown provider" in capsys.readouterr().out

    def test_plaintext_api_key_warning(self, tmp_path, capsys):
        from clawarena.core.check import run_check
        p = self._make_tests_json(tmp_path, model={
            "model_id": "x", "api_key": "sk-plaintext"
        })
        ok = run_check(p)
        # Should pass but with warning
        assert ok is True
        assert "plaintext" in capsys.readouterr().out

    def test_metaclaw_missing_config(self, tmp_path, capsys):
        from clawarena.core.check import run_check
        p = self._make_tests_json(tmp_path, metaclaw={
            "enabled": True, "config_path": "nonexistent.yaml"
        })
        ok = run_check(p)
        assert ok is False
        assert "not found" in capsys.readouterr().out

    def test_valid_model_passes(self, tmp_path, capsys):
        from clawarena.core.check import run_check
        p = self._make_tests_json(tmp_path, model={
            "model_id": "gpt-4o", "provider": "openai", "api_key": "${API_KEY}"
        })
        ok = run_check(p)
        assert ok is True


# ---------------------------------------------------------------------------
# Isolation concurrency — overlay isolation
# ---------------------------------------------------------------------------

class TestIsolationOverlay:
    """Verify that concurrent build_model_env calls with different proxy URLs
    produce separate overlay files (no file-level race)."""

    def test_different_proxies_create_different_overlays(self, tmp_path):
        from clawarena.data_handlers.openclaw.handler import OpenClawDataHandler
        from clawarena.core.types import WorkCopy

        state = tmp_path / "state"
        state.mkdir()
        cfg = {"models": {}, "agents": {"defaults": {}, "list": []}}
        (state / "openclaw.json").write_text(json.dumps(cfg))

        wc = WorkCopy(state_dir=state, config_path=None, project_root=tmp_path)
        handler = OpenClawDataHandler()

        model_a = ModelConfig(model_id="gpt-4o", provider="openai",
                              api_base="http://proxy-A:8080")
        model_b = ModelConfig(model_id="gpt-4o", provider="openai",
                              api_base="http://proxy-B:8081")

        env_a = handler.build_model_env(wc, model_a)
        env_b = handler.build_model_env(wc, model_b)

        # Different proxy URLs → different overlay paths
        assert env_a["OPENCLAW_CONFIG_PATH"] != env_b["OPENCLAW_CONFIG_PATH"]

        # Each overlay has its own api_base
        cfg_a = json.loads(Path(env_a["OPENCLAW_CONFIG_PATH"]).read_text())
        cfg_b = json.loads(Path(env_b["OPENCLAW_CONFIG_PATH"]).read_text())
        base_a = cfg_a["models"]["providers"]["openai"]["baseUrl"]
        base_b = cfg_b["models"]["providers"]["openai"]["baseUrl"]
        assert "proxy-A" in base_a
        assert "proxy-B" in base_b

    def test_same_proxy_reuses_overlay(self, tmp_path):
        from clawarena.data_handlers.picoclaw.handler import PicoClawDataHandler
        from clawarena.core.types import WorkCopy

        state = tmp_path / "state"
        state.mkdir()
        (state / "config.json").write_text(json.dumps({"model_list": [], "agents": {}}))

        wc = WorkCopy(state_dir=state, config_path=None, project_root=tmp_path)
        handler = PicoClawDataHandler()

        model = ModelConfig(model_id="gpt-4o", provider="openai",
                            api_base="http://proxy:8080")
        env1 = handler.build_model_env(wc, model)
        env2 = handler.build_model_env(wc, model)
        assert env1["PICOCLAW_CONFIG"] == env2["PICOCLAW_CONFIG"]
