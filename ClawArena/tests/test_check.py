"""Tests for the check command."""

import json
import pytest
from pathlib import Path

from clawarena.core.check import run_check


def _make_valid_data(tmp_path):
    """Create minimal valid data structure."""
    base = tmp_path / "bench"
    base.mkdir()

    # eval
    eval_dir = base / "eval" / "t1"
    eval_dir.mkdir(parents=True)
    q = {"rounds": [
        {"id": "r1", "type": "multi_choice", "question": "?",
         "update_ids": [],
         "eval": {"options": {"A": "a"}, "answer": ["A"]},
         "feedback": {"correct": "ok", "options": {"A": "explanation"}}},
    ]}
    (eval_dir / "questions.json").write_text(json.dumps(q))

    # openclaw
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

    tests_json = {
        "eval_dir": "eval",
        "frameworks": {"openclaw": {"manifest": "openclaw/manifest.json"}},
        "tests": [{"id": "t1", "desc": "Test 1", "eval": "t1"}],
    }
    tests_path = base / "tests.json"
    tests_path.write_text(json.dumps(tests_json))
    return tests_path


def test_check_valid(tmp_path, capsys):
    p = _make_valid_data(tmp_path)
    ok = run_check(p)
    assert ok is True
    assert "PASS" in capsys.readouterr().out


def test_check_missing_eval_dir(tmp_path, capsys):
    p = _make_valid_data(tmp_path)
    # Remove eval dir
    import shutil
    shutil.rmtree(p.parent / "eval")
    ok = run_check(p)
    assert ok is False


def test_check_missing_questions(tmp_path, capsys):
    p = _make_valid_data(tmp_path)
    (p.parent / "eval" / "t1" / "questions.json").unlink()
    ok = run_check(p)
    assert ok is False


def test_check_strict_mode(tmp_path, capsys):
    import shutil
    p = _make_valid_data(tmp_path)
    # Trigger a warning-only violation (G-006c: test.id != test.eval) by
    # renaming the eval dir and pointing the tests.json entry at the new name.
    src = p.parent / "eval" / "t1"
    dst = p.parent / "eval" / "t1_alias"
    shutil.copytree(src, dst)
    cfg = json.loads(p.read_text())
    cfg["tests"][0]["eval"] = "t1_alias"
    p.write_text(json.dumps(cfg))

    ok_normal = run_check(p)
    assert ok_normal is True

    ok_strict = run_check(p, strict=True)
    assert ok_strict is False


# ---------------------------------------------------------------------------
# Helpers for session message order tests
# ---------------------------------------------------------------------------

def _msg_line(role, text="x"):
    """Build a JSONL line with the given role."""
    return json.dumps({
        "type": "message",
        "id": "id",
        "message": {"role": role, "content": [{"type": "text", "text": text}]},
    })


def _compaction_line():
    return json.dumps({"type": "compaction", "id": "c1", "timestamp": "2024-01-01T00:00:00Z"})


def _non_message_line(entry_type="model_change"):
    """A JSONL line that readSessionMessages ignores (no 'message' key, not compaction)."""
    return json.dumps({"type": entry_type, "data": {}})


def _write_session(path, lines):
    path.write_text("\n".join(lines) + "\n")


def _sess_path(p):
    return p.parent / "openclaw" / "state" / "agents" / "t1" / "sessions" / "main.jsonl"


# ---------------------------------------------------------------------------
# Session message order — main session
# ---------------------------------------------------------------------------

def test_session_valid_alternating(tmp_path):
    """正常交错的 user/assistant 序列应通过校验。"""
    p = _make_valid_data(tmp_path)
    _write_session(_sess_path(p), [
        _msg_line("user"),
        _msg_line("assistant"),
        _msg_line("user"),
        _msg_line("assistant"),
    ])
    assert run_check(p) is True


def test_session_consecutive_user_allowed(tmp_path):
    """连续两条 user 消息由上游 validateAnthropicTurns 合并，应允许。"""
    p = _make_valid_data(tmp_path)
    _write_session(_sess_path(p), [
        _msg_line("user"),
        _msg_line("user"),
        _msg_line("assistant"),
    ])
    assert run_check(p) is True


def _thinking_line(text="..."):
    """Build an assistant JSONL line containing ONLY a thinking block."""
    return json.dumps({
        "type": "message",
        "id": "id",
        "message": {
            "role": "assistant",
            "content": [{"type": "thinking", "thinking": text}],
        },
    })


def test_session_consecutive_assistant_fails(tmp_path):
    """连续两条普通 assistant 消息应报错。"""
    p = _make_valid_data(tmp_path)
    _write_session(_sess_path(p), [
        _msg_line("user"),
        _msg_line("assistant"),
        _msg_line("assistant"),
    ])
    assert run_check(p) is False


def test_session_thinking_then_assistant_allowed(tmp_path):
    """thinking-only assistant 后接正式 assistant 回答是合法的 thinking 模型写法。"""
    p = _make_valid_data(tmp_path)
    _write_session(_sess_path(p), [
        _msg_line("user"),
        _thinking_line(),
        _msg_line("assistant"),
        _msg_line("user"),
        _thinking_line(),
        _msg_line("assistant"),
    ])
    assert run_check(p) is True


def test_session_non_thinking_consecutive_assistant_fails(tmp_path):
    """前一条 assistant 含 text（非纯 thinking），连续 assistant 仍应报错。"""
    p = _make_valid_data(tmp_path)
    mixed = json.dumps({
        "type": "message", "id": "id",
        "message": {
            "role": "assistant",
            "content": [
                {"type": "thinking", "thinking": "..."},
                {"type": "text", "text": "hi"},
            ],
        },
    })
    _write_session(_sess_path(p), [
        _msg_line("user"),
        mixed,
        _msg_line("assistant"),
    ])
    assert run_check(p) is False


def test_session_consecutive_tool_result_allowed(tmp_path):
    """连续 toolResult 由 repairToolUseResultPairing 处理，应允许。"""
    p = _make_valid_data(tmp_path)
    _write_session(_sess_path(p), [
        _msg_line("user"),
        _msg_line("assistant"),
        _msg_line("toolResult"),
        _msg_line("toolResult"),
        _msg_line("assistant"),
    ])
    assert run_check(p) is True


def test_session_compaction_breaks_chain(tmp_path):
    """compaction 行作为链断点，夹在两个 user 消息间不触发错误。"""
    p = _make_valid_data(tmp_path)
    _write_session(_sess_path(p), [
        _msg_line("user"),
        _compaction_line(),
        _msg_line("user"),
        _msg_line("assistant"),
    ])
    assert run_check(p) is True


def test_session_non_message_lines_ignored(tmp_path):
    """model_change 等非 message 行完全忽略；连续 user 由上游合并，应允许。"""
    p = _make_valid_data(tmp_path)
    _write_session(_sess_path(p), [
        _non_message_line("session"),
        _msg_line("user"),
        _non_message_line("model_change"),
        _msg_line("user"),
        _msg_line("assistant"),
    ])
    assert run_check(p) is True


def test_session_non_message_lines_between_valid(tmp_path):
    """非 message 行出现在合法交错序列中不引发误报。"""
    p = _make_valid_data(tmp_path)
    _write_session(_sess_path(p), [
        _non_message_line("session"),
        _msg_line("user"),
        _non_message_line("model_change"),
        _msg_line("assistant"),
        _msg_line("user"),
    ])
    assert run_check(p) is True


# ---------------------------------------------------------------------------
# Session message order — update session files
# ---------------------------------------------------------------------------

def _add_session_update(p, lines):
    """向 manifest 添加一个 type=session 的 update 条目，并写入源文件。"""
    oc = p.parent / "openclaw"
    upd_dir = oc / "updates" / "t1" / "upd1"
    upd_dir.mkdir(parents=True)
    upd_file = upd_dir / "patch.jsonl"
    _write_session(upd_file, lines)

    # 在 questions.json 中引用该 update_id
    q_path = p.parent / "eval" / "t1" / "questions.json"
    q = json.loads(q_path.read_text())
    q["rounds"][0]["update_ids"] = ["upd1"]
    q_path.write_text(json.dumps(q))

    # 在 manifest 中注册
    manifest_path = oc / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["updates"] = {
        "t1": {
            "upd1": {
                "type": "session",
                "dir": "updates/t1/upd1",
                "files": [{"name": "patch.jsonl", "action": "append",
                           "target": "main.jsonl"}],
            }
        }
    }
    manifest_path.write_text(json.dumps(manifest))
    return p


def test_update_session_valid(tmp_path):
    """update session 文件内消息交错正常应通过。"""
    p = _make_valid_data(tmp_path)
    p = _add_session_update(p, [
        _msg_line("user"),
        _msg_line("assistant"),
    ])
    assert run_check(p) is True


def test_update_session_consecutive_user_allowed(tmp_path):
    """update session 文件内连续 user 由上游 validateAnthropicTurns 合并，应允许。"""
    p = _make_valid_data(tmp_path)
    p = _add_session_update(p, [
        _msg_line("user"),
        _msg_line("user"),
    ])
    assert run_check(p) is True


def test_update_session_consecutive_tool_result_allowed(tmp_path):
    """update session 文件内连续 toolResult 应允许。"""
    p = _make_valid_data(tmp_path)
    p = _add_session_update(p, [
        _msg_line("assistant"),
        _msg_line("toolResult"),
        _msg_line("toolResult"),
    ])
    assert run_check(p) is True


# ---------------------------------------------------------------------------
# OMIT_WORKSPACE workspace file existence warnings
# ---------------------------------------------------------------------------

def _make_exec_check_data(tmp_path):
    """Create data with an exec_check round referencing ${workspace}/output.txt."""
    p = _make_valid_data(tmp_path)
    q_path = p.parent / "eval" / "t1" / "questions.json"
    q = {
        "rounds": [{
            "id": "r1",
            "type": "exec_check",
            "question": "Check output",
            "update_ids": [],
            "eval": {"command": "cat ${workspace}/output.txt"},
            "feedback": {"correct": "Correct!", "incorrect": "Wrong!"},
        }]
    }
    q_path.write_text(json.dumps(q))
    return p


def test_workspace_warning_disabled_by_default(tmp_path, capsys, monkeypatch):
    """默认情况下 OMIT_WORKSPACE 未设置，workspace 文件缺失不触发 warning。"""
    monkeypatch.delenv("OMIT_WORKSPACE", raising=False)
    p = _make_exec_check_data(tmp_path)
    ok = run_check(p)
    assert ok is True
    out = capsys.readouterr().out
    assert "workspace file not found" not in out


def test_workspace_warning_enabled_missing_file(tmp_path, capsys, monkeypatch):
    """OMIT_WORKSPACE=0 时，workspace 文件缺失应产生 warning，check 仍通过。"""
    monkeypatch.setenv("OMIT_WORKSPACE", "0")
    p = _make_exec_check_data(tmp_path)
    ok = run_check(p)
    assert ok is True
    out = capsys.readouterr().out
    assert "workspace file not found" in out


def test_workspace_warning_file_exists_no_warning(tmp_path, capsys, monkeypatch):
    """OMIT_WORKSPACE=0 时，workspace 文件存在不触发 warning。"""
    monkeypatch.setenv("OMIT_WORKSPACE", "0")
    p = _make_exec_check_data(tmp_path)
    ws = p.parent / "openclaw" / "workspaces" / "t1"
    (ws / "output.txt").write_text("result")
    ok = run_check(p)
    assert ok is True
    out = capsys.readouterr().out
    assert "workspace file not found" not in out


def test_workspace_warning_strict_fails(tmp_path, capsys, monkeypatch):
    """OMIT_WORKSPACE=0 + --strict 时，workspace warning 导致 check 失败。"""
    monkeypatch.setenv("OMIT_WORKSPACE", "0")
    p = _make_exec_check_data(tmp_path)
    ok = run_check(p, strict=True)
    assert ok is False
