"""Tests for scoring.report (run report + composite scoring)."""
from __future__ import annotations

from clawarena_team.scoring.report import (
    NOTATION,
    _mqs_scenario,
    _sms_scenario,
    build_run_report,
)


def _md(metrics: dict, scenario_id: str = "sX", rounds=None):
    rounds = rounds or [{"id": "q1", "passed": True}]
    return {
        "scenario_id": scenario_id,
        "metrics": {"scenario_id": scenario_id, **metrics},
        "rounds": rounds,
    }


def _base_metrics(**overrides):
    base = {
        "task_success_rate": 1.0,
        "rounds_passed": 1,
        "rounds_total": 1,
        "tool_permission_score": 1.0,
        "readonly_subagent_score": 1.0,
        "workspace_permission_score": 1.0,
        "model_choice_score": 1.0,
        "main_agent_forbidden_count": 0,
        "subagent_forbidden_total": 0,
        "subagent_forbidden_avg": 0.0,
        "subagent_create_count": 0,
        "model_key_distribution": {},
        "invocation_distribution": {},
        "tools_grant_counts": {},
        "main_agent_context_size_max": 0,
        "main_agent_input_total": 0,
        "main_agent_output_total": 0,
        "main_agent_cache_read_total": 0,
        "subagent_system_tokens": 0,
        "subagent_context_size_max_sum": 0,
        "subagent_input_total": 0,
        "subagent_output_total": 0,
        "subagent_cache_read_total": 0,
    }
    base.update(overrides)
    return base


def test_mqs_scenario_average():
    m = {
        "tool_permission_score": 0.5,
        "readonly_subagent_score": 1.0,
        "workspace_permission_score": 0.0,
        "model_choice_score": 0.5,
    }
    assert abs(_mqs_scenario(m) - 0.5) < 1e-9


def test_sms_scenario_half_task_half_mqs():
    m = {
        "task_success_rate": 1.0,
        "tool_permission_score": 0.0,
        "readonly_subagent_score": 0.0,
        "workspace_permission_score": 0.0,
        "model_choice_score": 0.0,
    }
    assert abs(_sms_scenario(m) - 0.5) < 1e-9


def test_build_run_report_perfect_run():
    md_list = [_md(_base_metrics(), scenario_id="sa")]
    report, md_text = build_run_report("run1", md_list)

    comp = report["composite"]
    assert abs(comp["SMS"] - 1.0) < 1e-9
    assert abs(comp["TCS"] - 1.0) < 1e-9
    assert abs(comp["MQS"] - 1.0) < 1e-9
    assert abs(comp["TCR"] - 1.0) < 1e-9
    assert abs(comp["SCR"] - 1.0) < 1e-9
    assert abs(comp["SFR"] - 1.0) < 1e-9
    assert "## Summary" in md_text
    assert "## Notation" in md_text
    assert "**SMS**" in md_text


def test_build_run_report_partial_failure_lowers_sms():
    md_list = [
        _md(
            _base_metrics(
                task_success_rate=0.5,
                rounds_passed=1,
                rounds_total=2,
                tool_permission_score=0.5,
                workspace_permission_score=0.5,
                model_choice_score=0.5,
                readonly_subagent_score=1.0,
            ),
            scenario_id="sa",
            rounds=[{"passed": True}, {"passed": False}],
        )
    ]
    report, _ = build_run_report("run2", md_list)
    comp = report["composite"]
    # MQS_scenario = (0.5+1.0+0.5+0.5)/4 = 0.625; TCR=0.5; SCR=0.5; SFR=0 (1/2 not all-pass)
    # TCS = (0.5 + 0.5 + 0) / 3 = 1/3; MQS = 0.625; SMS = 0.5*(1/3) + 0.5*0.625
    expected_sms = 0.5 * (1 / 3) + 0.5 * 0.625
    assert abs(comp["SMS"] - expected_sms) < 1e-9
    assert abs(comp["SFR"] - 0.0) < 1e-9


def test_build_run_report_full_pass_sets_sfr():
    md_list = [
        _md(_base_metrics(rounds_passed=2, rounds_total=2),
            scenario_id="sa",
            rounds=[{"passed": True}, {"passed": True}]),
        _md(_base_metrics(task_success_rate=0.5, rounds_passed=1, rounds_total=2),
            scenario_id="sb",
            rounds=[{"passed": True}, {"passed": False}]),
    ]
    report, _ = build_run_report("run3", md_list)
    # 仅 sa 全对，sb 缺一题 → SFR = 1/2 = 0.5
    assert abs(report["composite"]["SFR"] - 0.5) < 1e-9


def test_statistics_aggregation_sums_and_max():
    md_list = [
        _md(_base_metrics(
            subagent_create_count=2,
            model_key_distribution={"llm": 2},
            invocation_distribution={"new+runtime": 2},
            tools_grant_counts={"Read": 2},
            subagent_forbidden_total=4,
            main_agent_forbidden_count=1,
            main_agent_context_size_max=500,
            main_agent_input_total=700,
            main_agent_output_total=120,
            main_agent_cache_read_total=2000,
            subagent_system_tokens=50,
            subagent_context_size_max_sum=300,
            subagent_input_total=150,
            subagent_output_total=40,
            subagent_cache_read_total=400,
        ), scenario_id="sa"),
        _md(_base_metrics(
            subagent_create_count=3,
            model_key_distribution={"llm": 1, "vlm": 2},
            invocation_distribution={"new+runtime": 3},
            tools_grant_counts={"Read": 3, "Glob": 1},
            subagent_forbidden_total=2,
            main_agent_forbidden_count=0,
            main_agent_context_size_max=800,
            main_agent_input_total=1300,
            main_agent_output_total=210,
            main_agent_cache_read_total=4500,
            subagent_system_tokens=80,
            subagent_context_size_max_sum=520,
            subagent_input_total=260,
            subagent_output_total=70,
            subagent_cache_read_total=900,
        ), scenario_id="sb"),
    ]
    report, _ = build_run_report("run4", md_list)
    s = report["statistics"]
    assert s["SUB"] == 5
    assert s["MKD"] == {"llm": 3, "vlm": 2}
    assert s["TGC"] == {"Read": 5, "Glob": 1}
    assert s["MAF"] == 1
    assert s["SAFt"] == 6
    # SAFa = total forbidden / total subagents = 6 / 5
    assert abs(s["SAFa"] - 1.2) < 1e-9
    # MCM = max across scenarios; others = sum
    assert s["MCM"] == 800
    assert s["MIT"] == 2000
    assert s["MOT"] == 330
    assert s["MCR"] == 6500
    assert s["SST"] == 130
    assert s["SCM"] == 820
    assert s["SIT"] == 410
    assert s["SOT"] == 110
    assert s["SCH"] == 1300


def test_markdown_renders_tables_and_notation():
    md_list = [_md(_base_metrics(), scenario_id="sa")]
    _, md_text = build_run_report("run_md", md_list)
    assert "## Scored — per scenario" in md_text
    assert "## Statistics — Subagent & Forbidden" in md_text
    assert "## Statistics — Main Agent Tokens" in md_text
    assert "## Statistics — Subagent Tokens" in md_text
    # NOTATION 中每个缩写应出现在 markdown 中
    for abbr in NOTATION:
        assert f"**{abbr}**" in md_text


def test_legacy_keys_preserved():
    """旧 consumer 直接读 avg_* 三个 key，须保持。"""
    md_list = [_md(_base_metrics(), scenario_id="sa")]
    report, _ = build_run_report("run_legacy", md_list)
    assert report["avg_task_success_rate"] == report["composite"]["TCR"]
    assert report["avg_scenario_success_rate"] == report["composite"]["SCR"]
    assert report["avg_scenario_full_pass_rate"] == report["composite"]["SFR"]
