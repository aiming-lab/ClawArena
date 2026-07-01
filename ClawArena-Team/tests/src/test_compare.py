"""Tests for scoring.compare (cross-run comparison)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from clawarena_team.scoring.compare import build_comparison
from clawarena_team.scoring.report import NOTATION, build_run_report


def _mk_scenario_md(scenario_id: str, *, task_success: float, mqs_components):
    tps, ros, wps, mcs = mqs_components
    return {
        "scenario_id": scenario_id,
        "metrics": {
            "scenario_id": scenario_id,
            "task_success_rate": task_success,
            "rounds_passed": 1 if task_success >= 0.999 else 0,
            "rounds_total": 1,
            "tool_permission_score": tps,
            "readonly_subagent_score": ros,
            "workspace_permission_score": wps,
            "model_choice_score": mcs,
            "main_agent_forbidden_count": 0,
            "subagent_forbidden_total": 0,
            "subagent_forbidden_avg": 0.0,
            "subagent_create_count": 1,
            "model_key_distribution": {"llm": 1},
            "invocation_distribution": {"new+runtime": 1},
            "tools_grant_counts": {"Read": 1},
            "main_agent_context_size_max": 500,
            "main_agent_input_total": 700,
            "main_agent_output_total": 120,
            "main_agent_cache_read_total": 2000,
            "subagent_system_tokens": 50,
            "subagent_context_size_max_sum": 300,
            "subagent_input_total": 150,
            "subagent_output_total": 40,
            "subagent_cache_read_total": 400,
        },
        "rounds": [{"passed": task_success >= 0.999}],
    }


def _write_report(tmp: Path, run_id: str, scenarios) -> Path:
    rj, _ = build_run_report(run_id, scenarios)
    p = tmp / f"{run_id}.json"
    p.write_text(json.dumps(rj, ensure_ascii=False), encoding="utf-8")
    return p


def test_compare_requires_at_least_two(tmp_path: Path):
    p = _write_report(tmp_path, "run_solo",
                      [_mk_scenario_md("sa", task_success=1.0, mqs_components=(1, 1, 1, 1))])
    with pytest.raises(ValueError):
        build_comparison([p])


def test_compare_sorts_by_sms_desc(tmp_path: Path):
    high = _write_report(tmp_path, "run_high",
                         [_mk_scenario_md("sa", task_success=1.0, mqs_components=(1, 1, 1, 1))])
    low = _write_report(tmp_path, "run_low",
                        [_mk_scenario_md("sa", task_success=0.0, mqs_components=(0, 0, 0, 0))])
    # 输入故意把 low 放前面，期望 high 排第一
    comparison, _ = build_comparison([low, high])
    assert comparison["labels"][0] == "run_high"
    assert comparison["labels"][1] == "run_low"
    assert comparison["summary"][0]["composite"]["SMS"] > comparison["summary"][1]["composite"]["SMS"]


def test_compare_md_has_all_sections_and_notation(tmp_path: Path):
    p1 = _write_report(tmp_path, "ra",
                       [_mk_scenario_md("sa", task_success=1.0, mqs_components=(1, 0.5, 0.5, 1))])
    p2 = _write_report(tmp_path, "rb",
                       [_mk_scenario_md("sa", task_success=0.5, mqs_components=(0.5, 1, 0, 1))])
    _, md_text = build_comparison([p1, p2])
    assert "## Composite & Scored — by run" in md_text
    assert "## Statistics — Subagent & Forbidden — by run" in md_text
    assert "## Statistics — Main Agent Tokens — by run" in md_text
    assert "## Statistics — Subagent Tokens — by run" in md_text
    assert "## SMS — per scenario × run" in md_text
    assert "## Notation" in md_text
    for abbr in NOTATION:
        assert f"**{abbr}**" in md_text


def test_compare_per_scenario_pivot(tmp_path: Path):
    p1 = _write_report(tmp_path, "ra", [
        _mk_scenario_md("sa", task_success=1.0, mqs_components=(1, 1, 1, 1)),
        _mk_scenario_md("sb", task_success=0.5, mqs_components=(0.5, 0.5, 0.5, 0.5)),
    ])
    p2 = _write_report(tmp_path, "rb", [
        _mk_scenario_md("sa", task_success=0.5, mqs_components=(0.5, 0.5, 0.5, 0.5)),
        _mk_scenario_md("sc", task_success=1.0, mqs_components=(1, 1, 1, 1)),
    ])
    data, _ = build_comparison([p1, p2])
    sids = [row["scenario_id"] for row in data["by_scenario"]]
    assert set(sids) == {"sa", "sb", "sc"}
    sa = next(r for r in data["by_scenario"] if r["scenario_id"] == "sa")
    assert "ra" in sa["per_experiment"]
    assert "rb" in sa["per_experiment"]
    # sb 只在 ra；sc 只在 rb
    sb = next(r for r in data["by_scenario"] if r["scenario_id"] == "sb")
    assert "ra" in sb["per_experiment"] and "rb" not in sb["per_experiment"]
    sc = next(r for r in data["by_scenario"] if r["scenario_id"] == "sc")
    assert "rb" in sc["per_experiment"] and "ra" not in sc["per_experiment"]
