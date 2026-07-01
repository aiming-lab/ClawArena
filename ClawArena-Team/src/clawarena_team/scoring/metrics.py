"""Scenario-level metric computation.

Includes the three kinds of task success rate (within a scenario), tool
permission appropriateness, read-only subagent appropriateness, workspace
permission appropriateness, model choice appropriateness, and statistical
metrics.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ..types import Modality, RoundEval, ScenarioMetrics


def _tool_permission_score(stat) -> float:
    # Design trade-off (reverting audit-top10 W2F5a): an empty granted set still
    # returns 0.0. A subagent that is created but granted no tools is a lazy
    # delegation — "created but not equipped, unable to do work" — and should score
    # 0, not full marks; least-privilege evaluates "grant and use precisely", not
    # "simply not granting". Keep the penalty convention.
    granted = set(stat.tools_granted)
    used = set(stat.tools_used)
    if not granted:
        return 0.0
    return len(granted & used) / len(granted)


_READONLY_TOOLS = {"Read", "Grep", "Glob"}
_MUTATING_TOOLS = {"Write", "Edit", "Bash"}


def _readonly_score(stat) -> float:
    """Read-only subagent permission appropriateness.

    Convention: if a subagent's actually-used set ``used`` is non-empty and a
    subset of ``{Read, Grep, Glob}``, it is regarded as a read-only role; in that
    case, if its ``granted`` set contains any of ``{Write, Edit, Bash}``, it scores
    0 (the main agent over-granted mutating tools to this subagent); otherwise it
    scores 1. If ``used`` contains a mutating tool or is empty, it is out of scope
    for this sub-metric and defaults to 1 so as not to drag down the average.
    """
    used = set(stat.tools_used)
    granted = set(stat.tools_granted)
    if used and used <= _READONLY_TOOLS:
        return 0.0 if (granted & _MUTATING_TOOLS) else 1.0
    return 1.0


def _workspace_score(stat) -> float:
    if stat.files_accessible_total <= 0:
        return 0.0
    accessed = len(stat.files_accessed)
    return min(1.0, accessed / stat.files_accessible_total)


def _model_choice_score(stat) -> float:
    """Pool-key choice score: reflects the principle of "choose the smallest sufficient pool".

    Aligned with :data:`POOL_USABLE_MODALITIES`:
    - the llm pool can read text only, and always scores;
    - the vlm pool can read image/video, and consuming either one is considered appropriate;
    - the omni pool adds audio, and is appropriate only if audio was actually read (image/video should be left to vlm).
    """
    if stat.model_key == Modality.LLM:
        return 1.0
    if stat.model_key == Modality.VLM:
        used = stat.modality_usage.get("image", 0) + stat.modality_usage.get("video", 0)
        return 1.0 if used > 0 else 0.0
    if stat.model_key == Modality.OMNI:
        return 1.0 if stat.modality_usage.get("audio", 0) > 0 else 0.0
    return 0.0


def compute_scenario_metrics(
    *,
    scenario_id: str,
    round_evals: list[RoundEval],
    manager,
    main_harness,
) -> ScenarioMetrics:
    rounds_total = len(round_evals)
    rounds_passed = sum(1 for r in round_evals if r.passed)
    task_success_rate = rounds_passed / rounds_total if rounds_total else 0.0

    sub_stats = [rec.stat for rec in manager.records.values()]
    n_sub = len(sub_stats)

    if n_sub == 0:
        tool_score = readonly_score = ws_score = model_score = 0.0
    else:
        tool_score = sum(_tool_permission_score(s) for s in sub_stats) / n_sub
        readonly_score = sum(_readonly_score(s) for s in sub_stats) / n_sub
        ws_score = sum(_workspace_score(s) for s in sub_stats) / n_sub
        model_score = sum(_model_choice_score(s) for s in sub_stats) / n_sub

    subagent_forbidden_total = sum(s.forbidden_count for s in sub_stats)
    subagent_forbidden_avg = (subagent_forbidden_total / n_sub) if n_sub else 0.0

    model_key_distribution: dict[str, int] = {}
    tools_grant_counts: dict[str, int] = {}
    for s in sub_stats:
        model_key_distribution[s.model_key.value] = model_key_distribution.get(s.model_key.value, 0) + 1
        for t in s.tools_granted:
            tools_grant_counts[t] = tools_grant_counts.get(t, 0) + 1

    subagent_system_tokens = 0
    sub_input_total = 0
    sub_output_total = 0
    sub_cache_read_total = 0
    sub_context_size_max_sum = 0
    # Bash invocation-mode distribution: sum of the bash_mode_counter of the main + each subagent harness.
    bash_mode_distribution: dict[str, int] = {}
    for k, v in getattr(main_harness, "bash_mode_counter", {}).items():
        bash_mode_distribution[k] = bash_mode_distribution.get(k, 0) + v
    for rec in manager.records.values():
        for sid, h in rec.harnesses.items():
            sys_text = h.turns[0].content if h.turns else ""
            try:
                subagent_system_tokens += h.tokenizer.count(sys_text)
            except Exception:
                subagent_system_tokens += len(sys_text) // 4
            sub_input_total += h.input_token_total
            sub_output_total += h.output_token_total
            sub_cache_read_total += h.cache_read_total
            sub_context_size_max_sum += h.context_size_max
            for k, v in getattr(h, "bash_mode_counter", {}).items():
                bash_mode_distribution[k] = bash_mode_distribution.get(k, 0) + v

    return ScenarioMetrics(
        scenario_id=scenario_id,
        task_success_rate=task_success_rate,
        rounds_passed=rounds_passed,
        rounds_total=rounds_total,
        tool_permission_score=tool_score,
        readonly_subagent_score=readonly_score,
        workspace_permission_score=ws_score,
        model_choice_score=model_score,
        main_agent_forbidden_count=main_harness.scope.forbidden_count,
        subagent_forbidden_total=subagent_forbidden_total,
        subagent_forbidden_avg=subagent_forbidden_avg,
        subagent_create_count=n_sub,
        model_key_distribution=model_key_distribution,
        invocation_distribution=dict(manager.invocation_distribution),
        tools_grant_counts=tools_grant_counts,
        main_agent_context_size_max=main_harness.context_size_max,
        main_agent_input_total=main_harness.input_token_total,
        main_agent_output_total=main_harness.output_token_total,
        main_agent_cache_read_total=main_harness.cache_read_total,
        subagent_system_tokens=subagent_system_tokens,
        subagent_context_size_max_sum=sub_context_size_max_sum,
        subagent_input_total=sub_input_total,
        subagent_output_total=sub_output_total,
        subagent_cache_read_total=sub_cache_read_total,
        bash_mode_distribution=bash_mode_distribution,
        structured_output_count=getattr(manager, "structured_output_calls", 0),
    )
