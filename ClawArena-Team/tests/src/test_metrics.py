from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from clawarena_team.scoring.metrics import compute_scenario_metrics
from clawarena_team.types import (
    Modality,
    RoundEval,
    SubagentLifecycleStat,
)


def _make_stat(
    *,
    model_key: Modality = Modality.LLM,
    tools_granted=("Read",),
    tools_used=("Read",),
    files_accessible_total=10,
    files_accessed=5,
    modality_usage=None,
    forbidden=0,
) -> SubagentLifecycleStat:
    stat = SubagentLifecycleStat(
        subagent_id="s1",
        name="n",
        model_key=model_key,
        tools_granted=list(tools_granted),
        tools_used=set(tools_used),
        accessible_paths=[],
    )
    stat.files_accessible_total = files_accessible_total
    stat.files_accessed = {Path(f"/x/{i}") for i in range(files_accessed)}
    stat.modality_usage = modality_usage or {"text": 1}
    stat.forbidden_count = forbidden
    return stat


def _make_manager(stats):
    records = {}
    for i, s in enumerate(stats):
        rec = SimpleNamespace(stat=s, harnesses={})
        records[f"s{i}"] = rec
    return SimpleNamespace(records=records, invocation_distribution={"new+runtime": 1})


def _make_main_harness():
    return SimpleNamespace(
        scope=SimpleNamespace(forbidden_count=0),
        context_size_max=50,
        input_token_total=40,
        output_token_total=10,
        cache_read_total=80,
    )


def _call_full(stats, round_evals=None):
    return compute_scenario_metrics(
        scenario_id="x",
        round_evals=round_evals or [],
        manager=_make_manager(stats),
        main_harness=_make_main_harness(),
    )


def test_tool_perm_score_full():
    m = _call_full(
        [_make_stat(tools_granted=("Read", "Write"), tools_used=("Read", "Write"))],
        round_evals=[RoundEval("q1", True, 0, "", "", 0.0)],
    )
    assert m.tool_permission_score == 1.0


def test_tool_perm_score_partial():
    m = _call_full([_make_stat(tools_granted=("Read", "Write", "Bash"), tools_used=("Read",))])
    assert abs(m.tool_permission_score - 1 / 3) < 1e-6


def _call(stats, round_evals=None):
    return compute_scenario_metrics(
        scenario_id="x",
        round_evals=round_evals or [],
        manager=_make_manager(stats),
        main_harness=_make_main_harness(),
    )


def test_readonly_subagent_score():
    # 实际只用 Read，且授权也仅含只读集合 → 1
    m = _call([_make_stat(tools_granted=("Read",), tools_used=("Read",))])
    assert m.readonly_subagent_score == 1.0
    # 实际只用 Read，但授权含 Write → 0（越授可变工具）
    m = _call([_make_stat(tools_granted=("Read", "Write"), tools_used=("Read",))])
    assert m.readonly_subagent_score == 0.0


def test_readonly_subagent_score_grep_glob_count_as_readonly():
    # 实际用了 Read+Grep+Glob，授权也是只读三件套 → 1
    m = _call(
        [_make_stat(tools_granted=("Read", "Grep", "Glob"), tools_used=("Read", "Grep", "Glob"))]
    )
    assert m.readonly_subagent_score == 1.0
    # 实际只用 Grep，授权含 Bash → 0
    m = _call([_make_stat(tools_granted=("Grep", "Bash"), tools_used=("Grep",))])
    assert m.readonly_subagent_score == 0.0
    # 实际只用 Glob，授权含 Edit → 0
    m = _call([_make_stat(tools_granted=("Glob", "Edit"), tools_used=("Glob",))])
    assert m.readonly_subagent_score == 0.0


def test_readonly_subagent_score_mutating_use_not_in_scope():
    # 实际用了 Write → 非只读角色，不在指标范围 → 1
    m = _call(
        [_make_stat(tools_granted=("Read", "Write"), tools_used=("Read", "Write"))]
    )
    assert m.readonly_subagent_score == 1.0


def test_readonly_subagent_score_empty_use():
    # 未使用任何工具 → 不在指标范围 → 1
    m = _call([_make_stat(tools_granted=("Read",), tools_used=())])
    assert m.readonly_subagent_score == 1.0


def test_workspace_score():
    m = _call([_make_stat(files_accessible_total=20, files_accessed=5)])
    assert abs(m.workspace_permission_score - 0.25) < 1e-6


def test_model_choice_vlm_without_image_zero():
    m = _call([_make_stat(model_key=Modality.VLM, modality_usage={"text": 5})])
    assert m.model_choice_score == 0.0


def test_model_choice_omni_image_only_zero():
    m = _call([_make_stat(model_key=Modality.OMNI, modality_usage={"image": 3})])
    assert m.model_choice_score == 0.0


def test_model_choice_omni_audio_one():
    m = _call([_make_stat(model_key=Modality.OMNI, modality_usage={"audio": 1})])
    assert m.model_choice_score == 1.0


def test_task_success_rate():
    m = _call(
        [_make_stat()],
        round_evals=[RoundEval("q1", True, 0, "", "", 0.0), RoundEval("q2", False, 1, "", "", 0.0)],
    )
    assert m.task_success_rate == 0.5
    assert m.rounds_passed == 1
    assert m.rounds_total == 2
