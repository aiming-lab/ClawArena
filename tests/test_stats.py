"""Tests for the stats package."""

import json
from pathlib import Path

import pytest

from clawarena.stats import (
    ALL_CATEGORIES,
    BenchmarkStats,
    ScenarioStats,
    TokenCounter,
    collect_benchmark,
    generate_stats_report,
    get_layout,
    registered_frameworks,
    render_markdown,
    run_stats,
)
from clawarena.stats.base import (
    TC_FB,
    TC_HIST,
    TC_MAIN,
    TC_PREF,
    TC_Q,
    TC_USESS,
    TC_UWS,
    TC_WS,
)
from clawarena.stats.collect import _round_facts
from clawarena.stats.session_parser import (
    ChatMessage,
    count_session_tokens,
    parse_claude_code_session,
    parse_openclaw_session,
    parse_picoclaw_session,
    render_chatml,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def counter() -> TokenCounter:
    return TokenCounter("cl100k_base")


def _round_pair(sid: str) -> list[dict]:
    """Two rounds (mc with pref + ec with regex/timeout)."""
    return [
        {
            "id": "r1", "type": "multi_choice",
            "question": f"{sid}-q1: pick the correct ones",
            "update_ids": [],
            "eval": {
                "options": {"A": "a", "B": "b", "C": "c", "D": "d"},
                "answer": ["A", "C"],
            },
            "feedback": {
                "correct": "well done",
                "options": {"A": "yes", "B": "no", "C": "yes", "D": "no"},
            },
            "pref": {
                "command": "echo pref",
                "feedback": {"correct": "", "incorrect": "violated rule P1"},
            },
        },
        {
            "id": "r2", "type": "exec_check",
            "question": f"{sid}-q2: write the file",
            "update_ids": [f"{sid}_upd1"],
            "eval": {
                "command": "cat ${workspace}/output.txt",
                "expect_exit": 0,
                "expect_stdout": r"result:\s+\d+",
                "expect_stdout_regex": True,
                "timeout": 10,
            },
            "feedback": {"correct": "great", "incorrect": "fix it"},
        },
    ]


def _make_eval(base: Path, sids: list[str]) -> None:
    eval_dir = base / "eval"
    for sid in sids:
        d = eval_dir / sid
        d.mkdir(parents=True, exist_ok=True)
        (d / "questions.json").write_text(
            json.dumps({"id": sid, "rounds": _round_pair(sid)})
        )


def _build_openclaw(base: Path, sids: list[str]) -> dict:
    """Layout: main + history sessions inside state/agents/<sid>/sessions/."""
    fw_dir = base / "openclaw"
    agents: dict[str, dict] = {}
    updates: dict[str, dict] = {}
    for sid in sids:
        sess = f"{sid}/sessions"
        ad = fw_dir / "state" / "agents" / sid / "sessions"
        ad.mkdir(parents=True)
        (ad / "main.jsonl").write_text("main session content " * 5)
        (ad / "hist1.jsonl").write_text("history one " * 4)

        ws_dir = fw_dir / "workspaces" / sid
        ws_dir.mkdir(parents=True)
        (ws_dir / "readme.md").write_text("workspace readme")

        upd_dir = fw_dir / "updates" / sid / "upd1"
        upd_dir.mkdir(parents=True)
        (upd_dir / "patch.txt").write_text("update payload")

        agents[sid] = {
            "agent_id": sid,
            "agent_dir": f"state/agents/{sid}",
            "session": "main",
            "history_sessions": ["hist1"],
            "workspace": f"workspaces/{sid}",
        }
        updates[sid] = {
            f"{sid}_upd1": {
                "type": "workspace",
                "dir": f"updates/{sid}/upd1",
                "files": [{"name": "patch.txt", "action": "append"}],
            },
        }
    (fw_dir / "manifest.json").write_text(json.dumps({
        "framework": "openclaw",
        "agents": agents, "updates": updates,
    }))
    return {"manifest": "openclaw/manifest.json"}


def _build_claude_code(base: Path, sids: list[str]) -> dict:
    """Layout: main jsonl in state/projects, history md in workspace/message_logs."""
    fw_dir = base / "claude-code"
    agents: dict[str, dict] = {}
    updates: dict[str, dict] = {}
    for sid in sids:
        proj = fw_dir / "state" / "projects" / sid
        proj.mkdir(parents=True)
        (proj / "abc-123.jsonl").write_text("claude main session " * 5)

        ws_dir = fw_dir / "workspaces" / sid
        ws_dir.mkdir(parents=True)
        (ws_dir / "CLAUDE.md").write_text("claude workspace readme")
        ml = ws_dir / "message_logs"
        ml.mkdir()
        (ml / "alex_slack.md").write_text("alex history " * 6)
        (ml / "jordan_feishu.md").write_text("jordan history " * 6)

        upd_dir = fw_dir / "updates" / sid / "upd1"
        upd_dir.mkdir(parents=True)
        (upd_dir / "alex_slack.md").write_text("update md content")

        agents[sid] = {
            "agent_id": sid,
            "project_dir": f"state/projects/{sid}",
            "session": "abc-123",
            "history_sessions": [],
            "workspace": f"workspaces/{sid}",
        }
        updates[sid] = {
            f"{sid}_upd1": {
                "type": "workspace_md",
                "dir": f"updates/{sid}/upd1",
                "files": [{"name": "alex_slack.md", "target": "message_logs/alex_slack.md"}],
            },
        }
    (fw_dir / "manifest.json").write_text(json.dumps({
        "framework": "claude-code",
        "agents": agents, "updates": updates,
    }))
    return {"manifest": "claude-code/manifest.json"}


def _build_picoclaw(base: Path, sids: list[str]) -> dict:
    """Layout: main jsonl in memory/, history jsonl in workspace/message_logs."""
    fw_dir = base / "picoclaw"
    (fw_dir / "memory").mkdir(parents=True)
    agents: dict[str, dict] = {}
    updates: dict[str, dict] = {}
    for sid in sids:
        (fw_dir / "memory" / f"bench_{sid}.jsonl").write_text("pico main " * 5)

        ws_dir = fw_dir / "workspaces" / sid
        ws_dir.mkdir(parents=True)
        (ws_dir / "AGENTS.md").write_text("pico workspace readme")
        ml = ws_dir / "message_logs"
        ml.mkdir()
        (ml / "alex_slack.jsonl").write_text("alex jsonl history " * 6)

        upd_dir = fw_dir / "updates" / sid / "upd1"
        upd_dir.mkdir(parents=True)
        (upd_dir / "alex_slack.jsonl").write_text("update jsonl content")

        agents[sid] = {
            "agent_id": sid,
            "session_key": f"bench:{sid}",
            "history_sessions": ["alex_slack"],
            "workspace": f"workspaces/{sid}",
        }
        updates[sid] = {
            f"{sid}_upd1": {
                "type": "workspace_jsonl",
                "dir": f"updates/{sid}/upd1",
                "files": [{"name": "alex_slack.jsonl", "target": "message_logs/alex_slack.jsonl"}],
            },
        }
    (fw_dir / "manifest.json").write_text(json.dumps({
        "framework": "picoclaw",
        "agents": agents, "updates": updates,
    }))
    return {"manifest": "picoclaw/manifest.json"}


def _build_nanobot(base: Path, sids: list[str]) -> dict:
    """Layout: main jsonl in workspace/<sid>/sessions, history md in
    workspace/<sid>/message_logs."""
    fw_dir = base / "nanobot"
    agents: dict[str, dict] = {}
    updates: dict[str, dict] = {}
    for sid in sids:
        ws_dir = fw_dir / "workspaces" / sid
        ws_dir.mkdir(parents=True)
        (ws_dir / "AGENTS.md").write_text("nanobot workspace readme")

        sess_dir = ws_dir / "sessions"
        sess_dir.mkdir()
        (sess_dir / f"bench_{sid}.jsonl").write_text("nanobot main " * 5)

        ml = ws_dir / "message_logs"
        ml.mkdir()
        (ml / "alex_slack.md").write_text("alex md history " * 6)

        upd_dir = fw_dir / "updates" / sid / "upd1"
        upd_dir.mkdir(parents=True)
        (upd_dir / "alex_slack.md").write_text("update content")

        agents[sid] = {
            "agent_id": sid,
            "session_key": f"bench:{sid}",
            "history_sessions": [],
            "workspace": f"workspaces/{sid}",
        }
        updates[sid] = {
            f"{sid}_upd1": {
                "type": "workspace_md",
                "dir": f"updates/{sid}/upd1",
                "files": [{"name": "alex_slack.md", "target": "message_logs/alex_slack.md"}],
            },
        }
    (fw_dir / "manifest.json").write_text(json.dumps({
        "framework": "nanobot",
        "agents": agents, "updates": updates,
    }))
    return {"manifest": "nanobot/manifest.json"}


_BUILDERS = {
    "openclaw": _build_openclaw,
    "claude-code": _build_claude_code,
    "picoclaw": _build_picoclaw,
    "nanobot": _build_nanobot,
}


def _make_bench(
    tmp_path: Path, *,
    frameworks: list[str] = ("openclaw",),
    sids: list[str] = ("hil_a", "hil_b"),
) -> Path:
    """Build a synthetic benchmark with each framework's correct layout."""
    base = tmp_path / "bench"
    base.mkdir()
    _make_eval(base, list(sids))

    fw_cfg: dict[str, dict] = {}
    for fw in frameworks:
        fw_cfg[fw] = _BUILDERS[fw](base, list(sids))

    (base / "tests.json").write_text(json.dumps({
        "name": "synthetic-bench",
        "eval_dir": "eval",
        "frameworks": fw_cfg,
        "tests": [{"id": s, "desc": f"Scenario {s}", "eval": s} for s in sids],
    }))
    return base / "tests.json"


# ---------------------------------------------------------------------------
# TokenCounter
# ---------------------------------------------------------------------------

def test_token_counter_count(counter):
    assert counter.count("") == 0
    assert counter.count("hello world") > 0


def test_token_counter_count_file(tmp_path, counter):
    f = tmp_path / "x.txt"
    f.write_text("hello world from file")
    assert counter.count_file(f) > 0
    assert counter.count_file(tmp_path / "missing") == 0


# ---------------------------------------------------------------------------
# RoundFact collection
# ---------------------------------------------------------------------------

def test_round_facts_mc_shape(counter):
    rounds = [{
        "id": "r1", "type": "multi_choice", "question": "q",
        "update_ids": [], "eval": {"options": {"A": "a", "B": "b"}, "answer": ["A", "B"]},
        "feedback": {"correct": "ok", "options": {"A": "x", "B": "y"}},
    }]
    facts = _round_facts("s", rounds, counter)
    assert facts[0].mc_options == 2
    assert facts[0].mc_answers == 2
    assert facts[0].q_tokens > 0
    assert facts[0].fb_tokens > 0
    assert facts[0].has_pref is False


def test_round_facts_ec_shape(counter):
    rounds = [{
        "id": "r1", "type": "exec_check", "question": "q",
        "update_ids": ["u1"],
        "eval": {
            "command": "echo hi", "expect_exit": 0,
            "expect_stdout": "ok", "expect_stdout_regex": True, "timeout": 5,
        },
        "feedback": {"correct": "y", "incorrect": "n"},
    }]
    facts = _round_facts("s", rounds, counter)
    f = facts[0]
    assert f.ec_has_expect_exit is True
    assert f.ec_has_expect_stdout is True
    assert f.ec_is_regex is True
    assert f.ec_has_timeout is True
    assert f.ec_timeout == 5.0
    assert f.has_updates is True
    assert f.mc_options is None


def test_round_facts_pref_tokens(counter):
    rounds = [{
        "id": "r1", "type": "multi_choice", "question": "q",
        "update_ids": [],
        "eval": {"options": {"A": "a"}, "answer": ["A"]},
        "feedback": {"correct": "ok", "options": {"A": "x"}},
        "pref": {
            "command": "echo pref",
            "feedback": {"correct": "", "incorrect": "violated rule"},
            "rules": ["never look at sessions/private.jsonl"],
        },
    }]
    facts = _round_facts("s", rounds, counter)
    assert facts[0].has_pref is True
    assert facts[0].pref_tokens > 0


# ---------------------------------------------------------------------------
# ScenarioStats aggregation
# ---------------------------------------------------------------------------

def test_scenario_aggregations(counter):
    rounds = [
        {"id": "r1", "type": "multi_choice", "question": "q1", "update_ids": [],
         "eval": {"options": {"A": "a", "B": "b"}, "answer": ["A"]},
         "feedback": {"correct": "ok", "options": {"A": "x", "B": "y"}}},
        {"id": "r2", "type": "multi_choice", "question": "q2", "update_ids": ["u1"],
         "eval": {"options": {"A": "a", "B": "b", "C": "c"}, "answer": ["A", "C"]},
         "feedback": {"correct": "ok", "options": {"A": "x", "B": "y", "C": "z"}},
         "pref": {"command": "echo p", "feedback": {"correct": "", "incorrect": "n"}}},
    ]
    s = ScenarioStats(id="s1", desc="x", rounds=_round_facts("s1", rounds, counter))
    assert s.total_rounds == 2
    assert s.rounds_by_type == {"multi_choice": 2}
    assert s.rounds_with_pref == 1
    assert s.rounds_with_updates == 1
    assert s.mc_options == [2, 3]
    assert s.mc_answers == [1, 2]


# ---------------------------------------------------------------------------
# Layout registry & per-framework path resolution
# ---------------------------------------------------------------------------

def test_registered_frameworks_includes_all_four():
    fws = registered_frameworks()
    for expected in ("openclaw", "claude-code", "picoclaw", "nanobot"):
        assert expected in fws


def test_unknown_framework_falls_back_to_generic():
    layout = get_layout("does-not-exist")
    assert layout.name == "_generic"


def test_openclaw_layout_paths(tmp_path):
    layout = get_layout("openclaw")
    info = {"agent_dir": "state/agents/sid", "session": "main", "history_sessions": ["h1"]}
    assert layout.main_session_path(info, tmp_path, "sid") \
        == tmp_path / "state/agents/sid/sessions/main.jsonl"
    assert layout.history_session_paths(info, tmp_path, "sid") \
        == [tmp_path / "state/agents/sid/sessions/h1.jsonl"]
    assert layout.workspace_excludes == set()


def test_claude_code_layout_paths(tmp_path):
    layout = get_layout("claude-code")
    info = {"project_dir": "state/projects/sid", "session": "abc",
            "workspace": "workspaces/sid"}
    # main goes through project_dir
    assert layout.main_session_path(info, tmp_path, "sid") \
        == tmp_path / "state/projects/sid/abc.jsonl"
    # history globbed from workspace/message_logs
    ml = tmp_path / "workspaces/sid/message_logs"
    ml.mkdir(parents=True)
    (ml / "x.md").write_text("x")
    (ml / "y.md").write_text("y")
    paths = layout.history_session_paths(info, tmp_path, "sid")
    assert {p.name for p in paths} == {"x.md", "y.md"}
    assert layout.workspace_excludes == {"message_logs"}


def test_picoclaw_layout_paths(tmp_path):
    layout = get_layout("picoclaw")
    info = {"session_key": "bench:sid", "workspace": "workspaces/sid"}
    assert layout.main_session_path(info, tmp_path, "sid") \
        == tmp_path / "memory/bench_sid.jsonl"
    assert layout.workspace_excludes == {"message_logs"}


def test_nanobot_layout_paths(tmp_path):
    layout = get_layout("nanobot")
    info = {"session_key": "bench:sid", "workspace": "workspaces/sid"}
    assert layout.main_session_path(info, tmp_path, "sid") \
        == tmp_path / "workspaces/sid/sessions/bench_sid.jsonl"
    assert layout.workspace_excludes == {"sessions", "message_logs"}


# ---------------------------------------------------------------------------
# End-to-end: framework-specific collection
# ---------------------------------------------------------------------------

def test_collect_openclaw_e2e(tmp_path, counter):
    p = _make_bench(tmp_path, frameworks=["openclaw"])
    bench = collect_benchmark(p, "openclaw", counter)
    cats = bench.tokens_by_category
    assert cats[TC_MAIN] > 0
    assert cats[TC_HIST] > 0
    assert cats[TC_WS] > 0  # workspaces have non-message-log files
    assert cats[TC_UWS] > 0
    assert cats[TC_USESS] == 0  # no session-typed updates in fixture
    assert bench.update_actions == {"append": 2}


def test_collect_claude_code_excludes_message_logs(tmp_path, counter):
    p = _make_bench(tmp_path, frameworks=["claude-code"])
    bench = collect_benchmark(p, "claude-code", counter)
    cats = bench.tokens_by_category

    # main session reaches state/projects/<sid>/<session>.jsonl
    assert cats[TC_MAIN] > 0
    # history pulled out of workspace/message_logs/*.md
    assert cats[TC_HIST] > 0
    # workspace excludes message_logs → only CLAUDE.md remains
    assert cats[TC_WS] > 0

    # Verify message_logs files are NOT double-counted in workspace:
    # the bytes in message_logs/ should appear only in TC_HIST, not TC_WS.
    manifest_dir = p.parent / "claude-code"
    layout = get_layout("claude-code")
    history_files_tokens = 0
    for s in bench.scenarios:
        ai = {"workspace": f"workspaces/{s.id}"}
        for hp in layout.history_session_paths(ai, manifest_dir, s.id):
            history_files_tokens += counter.count_file(hp)
    bench_history_tokens = sum(
        s.tokens for sc in bench.scenarios for s in sc.sessions
        if s.kind == "history"
    )
    assert bench_history_tokens == history_files_tokens
    assert history_files_tokens > 0

    # workspace_md updates are session-equivalent for claude-code; they must
    # appear under TC_USESS rather than TC_UWS so that the per-framework token
    # distribution matches openclaw semantics.
    assert cats[TC_USESS] > 0
    assert cats[TC_UWS] == 0
    assert bench.updates_by_type == {"session": 2}


def test_collect_picoclaw_main_in_memory(tmp_path, counter):
    p = _make_bench(tmp_path, frameworks=["picoclaw"])
    bench = collect_benchmark(p, "picoclaw", counter)
    cats = bench.tokens_by_category
    assert cats[TC_MAIN] > 0  # memory/bench_<sid>.jsonl found
    assert cats[TC_HIST] > 0  # workspace/message_logs/*.jsonl
    assert cats[TC_WS] > 0

    # workspace_jsonl updates are session-equivalent for picoclaw.
    assert cats[TC_USESS] > 0
    assert cats[TC_UWS] == 0
    assert bench.updates_by_type == {"session": 2}


def test_collect_nanobot_main_in_workspace_sessions(tmp_path, counter):
    p = _make_bench(tmp_path, frameworks=["nanobot"])
    bench = collect_benchmark(p, "nanobot", counter)
    cats = bench.tokens_by_category
    assert cats[TC_MAIN] > 0  # workspace/<sid>/sessions/bench_<sid>.jsonl
    assert cats[TC_HIST] > 0  # workspace/<sid>/message_logs/*.md
    assert cats[TC_WS] > 0    # remaining workspace files (excl. sessions, message_logs)

    # workspace_md updates are session-equivalent for nanobot.
    assert cats[TC_USESS] > 0
    assert cats[TC_UWS] == 0
    assert bench.updates_by_type == {"session": 2}


# ---------------------------------------------------------------------------
# Action distribution: skipped when no actions present
# ---------------------------------------------------------------------------

def test_render_skips_action_section_when_no_actions(tmp_path, counter):
    p = _make_bench(tmp_path, frameworks=["claude-code"])
    bench = collect_benchmark(p, "claude-code", counter)
    md = render_markdown(bench, charts={})
    # claude-code update files carry `target` not `action` → section omitted.
    assert "### 4.2 Action Distribution" not in md
    assert "unknown" not in md


def test_render_includes_action_section_when_present(tmp_path, counter):
    p = _make_bench(tmp_path, frameworks=["openclaw"])
    bench = collect_benchmark(p, "openclaw", counter)
    md = render_markdown(bench, charts={})
    assert "### 4.2 Action Distribution" in md


# ---------------------------------------------------------------------------
# Markdown rendering structure
# ---------------------------------------------------------------------------

def test_markdown_advertises_tokenizer_and_sections(tmp_path, counter):
    p = _make_bench(tmp_path, frameworks=["openclaw"])
    bench = collect_benchmark(p, "openclaw", counter)
    md = render_markdown(bench, charts={})

    assert "Tokenizer: `cl100k_base`" in md
    for hdr in (
        "## 1. Overall Summary",
        "## 2. Token Distribution",
        "## 3. Question Statistics",
        "### 3.1 Type Distribution",
        "### 3.2 MC Shape",
        "### 3.3 EC Features",
        "### 3.4 Pref Coverage",
        "## 4. Update Statistics",
        "## 5. Per-Scenario Breakdown",
        "## 6. Per-Scenario Token Detail",
        "## 7. Top-N Rankings",
    ):
        assert hdr in md, f"missing section: {hdr}"


def test_generate_stats_report_writes_files(tmp_path, counter):
    p = _make_bench(tmp_path, frameworks=["openclaw"])
    bench = collect_benchmark(p, "openclaw", counter)
    out = tmp_path / "stats_out"
    path = generate_stats_report(bench, out)
    assert path == out / "STATS.md"
    text = path.read_text()
    assert "synthetic-bench" in text
    assert "openclaw" in text


# ---------------------------------------------------------------------------
# run_stats — default framework selection
# ---------------------------------------------------------------------------

def test_run_stats_defaults_to_all_frameworks(tmp_path):
    p = _make_bench(tmp_path, frameworks=["openclaw", "claude-code"])
    out = tmp_path / "out"
    run_stats(p, framework=None, out_dir=out)
    assert (out / "openclaw" / "STATS.md").exists()
    assert (out / "claude-code" / "STATS.md").exists()


def test_run_stats_single_framework_inplace(tmp_path):
    p = _make_bench(tmp_path, frameworks=["openclaw"])
    out = tmp_path / "single"
    run_stats(p, framework="openclaw", out_dir=out)
    assert (out / "STATS.md").exists()


# ---------------------------------------------------------------------------
# Session parsers
# ---------------------------------------------------------------------------

def test_parse_openclaw_session_skips_control_events(tmp_path):
    p = tmp_path / "s.jsonl"
    p.write_text(
        "\n".join([
            json.dumps({"type": "session", "id": "main",
                        "timestamp": "2026-01-01T00:00:00Z"}),
            json.dumps({"type": "model_change", "id": "m",
                        "provider": "anthropic"}),
            json.dumps({"type": "thinking_level_change",
                        "id": "t", "thinkingLevel": "low"}),
            json.dumps({"type": "custom",
                        "customType": "model-snapshot", "data": {}}),
            json.dumps({"type": "message", "id": "u1",
                        "message": {"role": "user",
                                    "content": [{"type": "text",
                                                  "text": "hello"}]}}),
            json.dumps({"type": "message", "id": "a1",
                        "message": {"role": "assistant",
                                    "content": [
                                        {"type": "text",
                                         "text": "hi back"},
                                        {"type": "toolCall",
                                         "id": "c1", "name": "read",
                                         "arguments": {"p": "/tmp/x"}},
                                    ]}}),
        ])
    )
    msgs = parse_openclaw_session(p)
    assert msgs == [
        ChatMessage(role="user", text="hello"),
        ChatMessage(role="assistant",
                    text='hi back\nread({"p": "/tmp/x"})'),
    ]


def test_parse_claude_code_session_flat_and_list_content(tmp_path):
    p = tmp_path / "s.jsonl"
    p.write_text(
        "\n".join([
            json.dumps({"type": "user",
                        "message": {"role": "user", "content": "hello"}}),
            json.dumps({"type": "assistant",
                        "message": {"role": "assistant",
                                    "content": [{"type": "text",
                                                  "text": "hi"}]}}),
        ])
    )
    msgs = parse_claude_code_session(p)
    assert [(m.role, m.text) for m in msgs] == [
        ("user", "hello"),
        ("assistant", "hi"),
    ]


def test_parse_picoclaw_session_skips_metadata_and_keeps_tool_calls(tmp_path):
    p = tmp_path / "s.jsonl"
    p.write_text(
        "\n".join([
            json.dumps({"_type": "metadata", "key": "bench:sid"}),
            json.dumps({"role": "user", "content": "q",
                        "tool_calls": None, "tool_call_id": ""}),
            json.dumps({"role": "assistant", "content": "a",
                        "tool_calls": [{"name": "read",
                                         "arguments": {"p": "x"}}]}),
        ])
    )
    msgs = parse_picoclaw_session(p)
    assert len(msgs) == 2
    assert msgs[0] == ChatMessage(role="user", text="q")
    assert msgs[1].role == "assistant"
    assert "read" in msgs[1].text and "\"arguments\"" in msgs[1].text


def test_render_chatml_wraps_each_message(counter):
    text = render_chatml([
        ChatMessage(role="user", text="hi"),
        ChatMessage(role="assistant", text="ok"),
    ])
    assert text.count("<|im_start|>") == 2
    assert text.count("<|im_end|>") == 2
    # And the counter must accept the special tokens without raising.
    assert counter.count_with_special(text) > 0


def test_count_session_tokens_uses_parser_and_is_below_raw(tmp_path, counter):
    p = tmp_path / "s.jsonl"
    bulky = "x" * 200
    p.write_text(
        "\n".join([
            json.dumps({"type": "session", "id": "a" * 64,
                        "timestamp": "2026-01-01T00:00:00Z"}),
            json.dumps({"type": "model_change", "id": "b" * 64,
                        "provider": "anthropic", "modelId": "claude"}),
            json.dumps({"type": "message", "id": "c",
                        "message": {"role": "user",
                                    "content": [{"type": "text",
                                                  "text": bulky}]}}),
        ])
    )
    parsed = count_session_tokens(p, parse_openclaw_session, counter)
    raw = counter.count_file(p)
    # Parsing strips control-event metadata, so the parsed token count
    # must be strictly below the raw byte count for this fixture.
    assert parsed < raw
    # Bulk content still contributes.
    assert parsed >= counter.count(bulky)


def test_count_session_tokens_falls_back_on_malformed(tmp_path, counter):
    p = tmp_path / "s.jsonl"
    p.write_text("not json at all")
    assert count_session_tokens(
        p, parse_openclaw_session, counter,
    ) == counter.count_file(p)


def test_update_files_accepts_bare_string_entries(tmp_path, counter):
    """manifest['updates'][sid][uid]['files'] may be either
    [{'name': ..., 'action': ...}, ...] or bare ['filename', ...].
    Both shapes must contribute to the file count and token total."""
    base = tmp_path / "bench"
    base.mkdir()
    fw = base / "openclaw"
    fw.mkdir()
    ud = fw / "updates" / "hil_a" / "u1"
    ud.mkdir(parents=True)
    (ud / "bare.txt").write_text("bare string file body")
    ad = fw / "state" / "agents" / "hil_a" / "sessions"
    ad.mkdir(parents=True)
    (ad / "main.jsonl").write_text("")
    ws = fw / "workspaces" / "hil_a"
    ws.mkdir(parents=True)
    (ws / "readme.md").write_text("w")
    (fw / "manifest.json").write_text(json.dumps({
        "framework": "openclaw",
        "agents": {"hil_a": {
            "agent_id": "hil_a", "agent_dir": "state/agents/hil_a",
            "session": "main", "history_sessions": [],
            "workspace": "workspaces/hil_a",
        }},
        "updates": {"hil_a": {"u1": {
            "type": "workspace",
            "dir": "updates/hil_a/u1",
            "files": ["bare.txt"],
        }}},
    }))
    eval_dir = base / "eval" / "hil_a"
    eval_dir.mkdir(parents=True)
    (eval_dir / "questions.json").write_text(json.dumps({"rounds": []}))
    (base / "tests.json").write_text(json.dumps({
        "name": "t", "eval_dir": "eval",
        "frameworks": {"openclaw": {"manifest": "openclaw/manifest.json"}},
        "tests": [{"id": "hil_a", "desc": "", "eval": "hil_a"}],
    }))
    bench = collect_benchmark(base / "tests.json", "openclaw", counter)
    scen = bench.scenarios[0]
    assert scen.update_files_total == 1
    assert scen.updates[0].files[0].name == "bare.txt"
    assert scen.updates[0].files[0].tokens > 0


def test_workspace_file_count_excludes_session_dirs(tmp_path, counter):
    """WorkspaceFact.files should count files physically under workspace/,
    skipping top-level session-equivalent subdirs (message_logs, sessions)."""
    p = _make_bench(tmp_path, frameworks=["openclaw", "claude-code"])
    oc = collect_benchmark(p, "openclaw", counter)
    cc = collect_benchmark(p, "claude-code", counter)
    # openclaw workspace has only readme.md under workspace/<sid>/
    for s in oc.scenarios:
        assert s.workspace.files == 1
    # claude-code workspace has CLAUDE.md at root + 2 md files under
    # message_logs/ (excluded). Only CLAUDE.md counts.
    for s in cc.scenarios:
        assert s.workspace.files == 1


def test_breakdown_table_reports_workspace_file_count(tmp_path, counter):
    p = _make_bench(tmp_path, frameworks=["claude-code"])
    bench = collect_benchmark(p, "claude-code", counter)
    md = render_markdown(bench, charts={})
    # New column header
    assert "WSFiles" in md
    # Per-scenario row has a non-zero workspace file count
    for s in bench.scenarios:
        assert f"| {s.id} |" in md
        assert s.workspace.files >= 1
