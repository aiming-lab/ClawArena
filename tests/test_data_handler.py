"""Tests for OpenClaw DataHandler."""

import json
import pytest
from pathlib import Path

from clawarena.data_handlers.openclaw.handler import OpenClawDataHandler
from clawarena.data_handlers.openclaw.work_copy import (
    _build_agents_list, prepare_openclaw_work_copy,
)
from clawarena.data_handlers.nanobot.work_copy import build_nanobot_runtime_config
from clawarena.data_handlers.picoclaw.work_copy import (
    build_picoclaw_runtime_config, prepare_picoclaw_work_copy, sync_security_yml,
)
from clawarena.data_handlers.openclaw.session import (
    _uniquify_session, _prepare_session, register_session_in_json,
)
from clawarena.data_handlers.openclaw.validate import validate_openclaw
from clawarena.data_handlers.openclaw.validate import _validate_session_message_order
from clawarena.data_handlers.picoclaw.validate import validate_picoclaw
from clawarena.data_handlers.update_refs import resolve_update_entries
from clawarena.data_handlers.openclaw.update import _guess_channel
from clawarena.data_handlers.jsonl_utils import read_jsonl, trim_llm_log_messages
from clawarena.core.types import WorkCopy


# ---------------------------------------------------------------------------
# JSONL utils
# ---------------------------------------------------------------------------

class TestJsonlUtils:
    def test_read_jsonl(self, tmp_path):
        f = tmp_path / "test.jsonl"
        f.write_text('{"a":1}\n{"b":2}\n')
        data = read_jsonl(f)
        assert len(data) == 2
        assert data[0]["a"] == 1

    def test_read_jsonl_missing(self, tmp_path):
        data = read_jsonl(tmp_path / "missing.jsonl")
        assert data == []

    def test_trim_llm_log(self):
        log = {
            "messages": [
                {"role": "user", "content": "q1"},
                {"role": "assistant", "content": "a1"},
                {"role": "user", "content": "q2"},
                {"role": "assistant", "content": "a2"},
            ]
        }
        trimmed = trim_llm_log_messages(log)
        assert len(trimmed["messages"]) == 2
        assert trimmed["messages"][0]["content"] == "q2"

    def test_trim_llm_log_no_user(self):
        log = {"messages": [{"role": "assistant", "content": "a"}]}
        assert trim_llm_log_messages(log) == log

    def test_trim_llm_log_non_dict(self):
        assert trim_llm_log_messages("not a dict") == "not a dict"


# ---------------------------------------------------------------------------
# Session management
# ---------------------------------------------------------------------------

class TestSessionManagement:
    def test_uniquify_session(self, tmp_path):
        agent_id = "test_agent"
        sessions_dir = tmp_path / "agents" / agent_id / "sessions"
        sessions_dir.mkdir(parents=True)

        old_id = "main_abc123"
        (sessions_dir / f"{old_id}.jsonl").write_text(
            json.dumps({"id": old_id}) + "\n"
        )
        sessions_json = {"agent:test_agent:main_abc123": {
            "sessionId": old_id, "sessionFile": f"{old_id}.jsonl",
        }}
        (sessions_dir / "sessions.json").write_text(json.dumps(sessions_json))

        new_id = _uniquify_session(tmp_path, agent_id, old_id)
        assert new_id.startswith("main_abc123_")
        assert len(new_id) > len(old_id)
        assert not (sessions_dir / f"{old_id}.jsonl").exists()
        assert (sessions_dir / f"{new_id}.jsonl").exists()

        # Check sessions.json updated
        updated = json.loads((sessions_dir / "sessions.json").read_text())
        assert f"agent:test_agent:{new_id}" in updated

    def test_prepare_session_creates_file(self, tmp_path):
        _prepare_session(tmp_path, "agent1", "sess1")
        path = tmp_path / "agents" / "agent1" / "sessions" / "sess1.jsonl"
        assert path.exists()

    def test_register_session(self, tmp_path):
        sessions_dir = tmp_path / "agents" / "a1" / "sessions"
        sessions_dir.mkdir(parents=True)
        (sessions_dir / "sessions.json").write_text("{}")

        register_session_in_json(tmp_path, "a1", "new_session.jsonl", "slack")
        data = json.loads((sessions_dir / "sessions.json").read_text())
        assert "agent:a1:new_session" in data

    def test_register_session_idempotent(self, tmp_path):
        sessions_dir = tmp_path / "agents" / "a1" / "sessions"
        sessions_dir.mkdir(parents=True)
        (sessions_dir / "sessions.json").write_text("{}")

        register_session_in_json(tmp_path, "a1", "s.jsonl", "slack")
        register_session_in_json(tmp_path, "a1", "s.jsonl", "slack")
        data = json.loads((sessions_dir / "sessions.json").read_text())
        assert len(data) == 1


# ---------------------------------------------------------------------------
# Channel guessing
# ---------------------------------------------------------------------------

def test_guess_channel():
    assert _guess_channel("alice_slack_abc.jsonl") == "slack"
    assert _guess_channel("bob_feishu_xyz.jsonl") == "feishu"
    assert _guess_channel("random_file.jsonl") == "unknown"


def test_resolve_update_entries_supports_shorthand_refs():
    test_updates = {
        "upd1_sessions": {"type": "session"},
        "upd1_workspace": {"type": "workspace"},
        "upd2_workspace": {"type": "workspace"},
    }
    assert [k for k, _ in resolve_update_entries(test_updates, 1)] == [
        "upd1_sessions", "upd1_workspace",
    ]
    assert [k for k, _ in resolve_update_entries(test_updates, "U1")] == [
        "upd1_sessions", "upd1_workspace",
    ]
    assert [k for k, _ in resolve_update_entries(test_updates, "upd2_workspace")] == [
        "upd2_workspace",
    ]


def test_resolve_update_entries_expands_group_refs():
    test_updates = {
        "upd1": {"type": "group", "children": ["upd1_sessions", "upd1_workspace"]},
        "upd1_sessions": {"type": "session"},
        "upd1_workspace": {"type": "workspace"},
    }
    assert [k for k, _ in resolve_update_entries(test_updates, "upd1")] == [
        "upd1_sessions", "upd1_workspace",
    ]


def test_build_nanobot_runtime_config_has_no_private_helper_keys(tmp_path):
    cfg = {
        "model": "openai/gpt-5.1",
        "max_tool_iterations": 40,
        "restrict_to_workspace": False,
        "exec_enable": True,
        "exec_timeout": 120,
    }
    runtime = build_nanobot_runtime_config(cfg, tmp_path / "ws")
    assert "_workspace_path" not in runtime
    assert "_config_path" not in runtime


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

class TestValidation:
    def _make_minimal_data(self, tmp_path):
        """Create minimal valid data structure for testing."""
        manifest_dir = tmp_path / "openclaw"
        manifest_dir.mkdir()
        (manifest_dir / "config").mkdir()
        state_dir = manifest_dir / "state"
        (state_dir / "agents" / "t1" / "sessions").mkdir(parents=True)
        (manifest_dir / "workspaces" / "t1").mkdir(parents=True)

        config = {"agents": {"list": [{"id": "t1"}]}}
        (manifest_dir / "config" / "openclaw.json").write_text(json.dumps(config))

        sess_dir = state_dir / "agents" / "t1" / "sessions"
        (sess_dir / "main.jsonl").touch()
        (sess_dir / "sessions.json").write_text("{}")

        eval_dir = tmp_path / "eval"
        (eval_dir / "t1").mkdir(parents=True)
        q = {"rounds": [{"id": "r1", "question": "?", "type": "multi_choice",
                         "eval": {"answer": ["A"]}, "update_ids": []}]}
        (eval_dir / "t1" / "questions.json").write_text(json.dumps(q))

        manifest = {
            "framework": "openclaw",
            "config_file": "config/openclaw.json",
            "state_dir": "state",
            "agents": {
                "t1": {
                    "agent_id": "t1",
                    "agent_dir": "state/agents/t1",
                    "session": "main",
                    "history_sessions": [],
                    "workspace": "workspaces/t1",
                },
            },
            "updates": {},
        }
        tests = [{"id": "t1", "eval": "t1"}]
        return manifest, manifest_dir, eval_dir, tests

    def test_valid_data(self, tmp_path):
        manifest, mdir, edir, tests = self._make_minimal_data(tmp_path)
        errors = validate_openclaw(manifest, mdir, edir, tests)
        assert errors == []

    def test_wrong_framework(self, tmp_path):
        manifest, mdir, edir, tests = self._make_minimal_data(tmp_path)
        manifest["framework"] = "wrong"
        errors = validate_openclaw(manifest, mdir, edir, tests)
        assert any("framework" in e for e in errors)

    def test_missing_agent(self, tmp_path):
        manifest, mdir, edir, tests = self._make_minimal_data(tmp_path)
        tests.append({"id": "t2", "eval": "t2"})
        errors = validate_openclaw(manifest, mdir, edir, tests)
        assert any("t2" in e for e in errors)

    def test_missing_session_file(self, tmp_path):
        manifest, mdir, edir, tests = self._make_minimal_data(tmp_path)
        manifest["agents"]["t1"]["session"] = "nonexistent"
        errors = validate_openclaw(manifest, mdir, edir, tests)
        assert any("session" in e.lower() for e in errors)

    def test_consecutive_user_messages_are_allowed(self, tmp_path):
        session_file = tmp_path / "session.jsonl"
        session_file.write_text(
            "\n".join(
                [
                    json.dumps({"message": {"role": "user", "content": [{"type": "text", "text": "u1"}]}}),
                    json.dumps({"message": {"role": "user", "content": [{"type": "text", "text": "u2"}]}}),
                    json.dumps({"message": {"role": "assistant", "content": [{"type": "text", "text": "a1"}]}}),
                ]
            ),
            encoding="utf-8",
        )
        errors: list[str] = []
        _validate_session_message_order(session_file, "t1", errors)
        assert errors == []


# ---------------------------------------------------------------------------
# DataHandler integration
# ---------------------------------------------------------------------------

class TestOpenClawDataHandler:
    def test_load_manifest(self, tmp_path):
        handler = OpenClawDataHandler()
        manifest = {"framework": "openclaw", "agents": {}}
        p = tmp_path / "manifest.json"
        p.write_text(json.dumps(manifest))
        loaded = handler.load_manifest(p)
        assert loaded["framework"] == "openclaw"

    def test_configure_mm_metaclaw_plugin_writes_plugin_fields(self, tmp_path):
        handler = OpenClawDataHandler()
        state_dir = tmp_path / "state"
        state_dir.mkdir()
        cfg_path = state_dir / "openclaw.json"
        cfg_path.write_text(json.dumps({"agents": {"defaults": {}}}))

        plugin_dir = tmp_path / "mm-metaclaw-src"
        plugin_dir.mkdir()

        wc = WorkCopy(state_dir=state_dir, config_path=None, project_root=tmp_path)
        handler.configure_mm_metaclaw_plugin(wc, plugin_dir)

        cfg = json.loads(cfg_path.read_text())
        assert cfg["plugins"]["entries"]["mm-metaclaw"]["enabled"] is True
        assert "mm-metaclaw" in cfg["plugins"]["allow"]
        paths = cfg["plugins"]["load"]["paths"]
        assert any("mm-metaclaw" in p for p in paths)

    def test_configure_mm_metaclaw_plugin_is_idempotent(self, tmp_path):
        handler = OpenClawDataHandler()
        state_dir = tmp_path / "state"
        state_dir.mkdir()
        cfg_path = state_dir / "openclaw.json"
        cfg_path.write_text(json.dumps({}))

        plugin_dir = tmp_path / "mm-metaclaw-src"
        plugin_dir.mkdir()

        wc = WorkCopy(state_dir=state_dir, config_path=None, project_root=tmp_path)
        handler.configure_mm_metaclaw_plugin(wc, plugin_dir)
        handler.configure_mm_metaclaw_plugin(wc, plugin_dir)

        cfg = json.loads(cfg_path.read_text())
        assert cfg["plugins"]["allow"].count("mm-metaclaw") == 1
        assert len(cfg["plugins"]["load"]["paths"]) == 1

    def test_configure_mm_metaclaw_plugin_no_op_when_cfg_missing(self, tmp_path):
        handler = OpenClawDataHandler()
        state_dir = tmp_path / "state"
        state_dir.mkdir()
        plugin_dir = tmp_path / "mm-metaclaw-src"
        plugin_dir.mkdir()

        wc = WorkCopy(state_dir=state_dir, config_path=None, project_root=tmp_path)
        handler.configure_mm_metaclaw_plugin(wc, plugin_dir)

        assert not (state_dir / "openclaw.json").exists()


class TestOpenClawWorkCopy:
    def test_build_agents_list_from_manifest(self, tmp_path):
        manifest = {
            "agents": {
                "t1": {"agent_id": "t1", "agent_dir": "state/agents/t1", "workspace": "workspaces/t1"},
                "t2": {"agent_id": "t2", "agent_dir": "state/agents/t2", "workspace": "workspaces/t2"},
            }
        }
        agents = _build_agents_list(
            manifest,
            state_root=tmp_path / "state_copy",
            workspace_root=tmp_path / "workspaces_copy",
        )
        assert [a["id"] for a in agents] == ["t1", "t2"]
        assert agents[0]["workspace"].endswith("/workspaces_copy/t1")
        assert agents[1]["agentDir"].endswith("/state_copy/agents/t2/agent")

    def test_prepare_work_copy_rebuilds_agents_from_manifest(self, tmp_path):
        manifest_dir = tmp_path / "openclaw"
        (manifest_dir / "config").mkdir(parents=True)
        (manifest_dir / "state" / "agents" / "t1" / "agent").mkdir(parents=True)
        (manifest_dir / "state" / "agents" / "t2" / "agent").mkdir(parents=True)
        (manifest_dir / "workspaces" / "t1").mkdir(parents=True)
        (manifest_dir / "workspaces" / "t2").mkdir(parents=True)

        config = {
            "agents": {
                "defaults": {"model": {"primary": "benchmark/test"}},
                "list": [{"id": "t1", "name": "t1", "skills": []}],
            },
            "tools": {},
        }
        (manifest_dir / "config" / "openclaw.json").write_text(json.dumps(config))

        manifest = {
            "config_file": "config/openclaw.json",
            "state_dir": "state",
            "workspaces_dir": "workspaces",
            "agents": {
                "t1": {"agent_id": "t1", "agent_dir": "state/agents/t1", "workspace": "workspaces/t1"},
                "t2": {"agent_id": "t2", "agent_dir": "state/agents/t2", "workspace": "workspaces/t2"},
            },
        }
        work_copy = prepare_openclaw_work_copy(manifest, manifest_dir, tmp_path)
        cfg = json.loads((work_copy.state_dir / "openclaw.json").read_text())
        ids = [a["id"] for a in cfg["agents"]["list"]]
        assert ids == ["t1", "t2"]
        assert (work_copy.workspace_root / "t1").exists()
        assert (work_copy.workspace_root / "t2").exists()


class TestPicoClawValidation:
    def test_build_nanobot_runtime_config_normalizes_legacy_keys(self, tmp_path):
        cfg = build_nanobot_runtime_config(
            {
                "model": "anthropic/claude-sonnet-4.5",
                "max_tool_iterations": 40,
                "restrict_to_workspace": False,
                "exec_enable": True,
                "exec_timeout": 120,
                "env": {},
            },
            tmp_path / "workspaces",
        )
        assert cfg["agents"]["defaults"]["workspace"].endswith("/workspaces")
        assert cfg["agents"]["defaults"]["model"] == "anthropic/claude-sonnet-4.5"
        assert cfg["agents"]["defaults"]["max_tool_iterations"] == 40
        assert cfg["tools"]["restrict_to_workspace"] is False
        assert cfg["tools"]["exec"]["enable"] is True
        assert cfg["tools"]["exec"]["timeout"] == 120
        assert "model" not in cfg
        assert "exec_enable" not in cfg

    def test_build_runtime_config_uses_requested_workspace(self, tmp_path):
        cfg = build_picoclaw_runtime_config(
            {"agents": {"defaults": {"model_name": "benchmark"}}},
            tmp_path / "workspaces" / "t1",
        )
        assert cfg["version"] == 1
        assert cfg["agents"]["defaults"]["workspace"].endswith("/workspaces/t1")

    def test_prepare_work_copy_uses_shared_workspace_root(self, tmp_path):
        manifest_dir = tmp_path / "picoclaw"
        (manifest_dir / "config").mkdir(parents=True)
        (manifest_dir / "workspaces" / "t1").mkdir(parents=True)
        (manifest_dir / "workspaces" / "t1" / "AGENTS.md").write_text("x")
        (manifest_dir / "memory").mkdir(parents=True)
        (manifest_dir / "memory" / "bench_t1.jsonl").write_text("{}\n")
        (manifest_dir / "memory" / "bench_t1.meta.json").write_text("{}")

        manifest = {
            "picoclaw_config_file": "config/config.json",
            "_picoclaw_config": {"agents": {"defaults": {"model_name": "benchmark"}}},
            "memory_dir": "memory",
            "workspaces_dir": "workspaces",
            "agents": {
                "t1": {
                    "agent_id": "t1",
                    "session_key": "bench:t1",
                    "workspace": "workspaces/t1",
                },
            },
        }
        work_copy = prepare_picoclaw_work_copy(manifest, manifest_dir, tmp_path)
        cfg = json.loads(work_copy.config_path.read_text())
        assert cfg["agents"]["defaults"]["workspace"] == str(work_copy.workspace_root)

    def test_sync_security_yml_copies_and_merges_model_key(self, tmp_path):
        src = tmp_path / "src"
        dst = tmp_path / "dst"
        src.mkdir()
        (src / ".security.yml").write_text(
            "model_list:\n  benchmark:\n    api_keys:\n      - old-key\n",
            encoding="utf-8",
        )
        sync_security_yml(dst, source_dir=src, model_name="clawarena", api_key="new-key")
        text = (dst / ".security.yml").read_text(encoding="utf-8")
        assert "benchmark" in text
        assert "clawarena" in text
        assert "new-key" in text

    def test_validate_accepts_memory_backed_sessions(self, tmp_path):
        manifest_dir = tmp_path / "picoclaw"
        (manifest_dir / "config").mkdir(parents=True)
        (manifest_dir / "workspaces" / "t1").mkdir(parents=True)
        (manifest_dir / "workspaces" / "t1" / "AGENTS.md").write_text("x")
        (manifest_dir / "memory").mkdir(parents=True)
        (manifest_dir / "config" / "config.json").write_text("{}")
        (manifest_dir / "memory" / "bench_t1.jsonl").write_text("{}\n")
        (manifest_dir / "memory" / "bench_t1.meta.json").write_text("{}")

        eval_dir = tmp_path / "eval"
        (eval_dir / "t1").mkdir(parents=True)
        (eval_dir / "t1" / "questions.json").write_text(json.dumps({"rounds": []}))

        manifest = {
            "framework": "picoclaw",
            "picoclaw_config_file": "config/config.json",
            "memory_dir": "memory",
            "workspaces_dir": "workspaces",
            "agents": {
                "t1": {
                    "agent_id": "t1",
                    "session_key": "bench:t1",
                    "workspace": "workspaces/t1",
                },
            },
            "updates": {},
        }

        errors = validate_picoclaw(manifest, manifest_dir, eval_dir, [{"id": "t1"}])
        assert errors == []
