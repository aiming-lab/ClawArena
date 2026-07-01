"""Prompt 动态拼接与配置模板化：防止 prompt 与 tools.enabled / 配置参数漂移。

覆盖两类问题：
1. MAIN_AGENT_SYSTEM_PROMPT 按 tools.enabled 拼接——关掉 subagent 仅留 Workflow
   （或反之）时不得出现对侧工具名，避免诱导用错工具或自相矛盾。
2. 受配置影响的硬编码值（usage 阈值、大文件 KiB、Bash 超时、Workflow 上限）全部
   随配置走，改配置后 prompt 同步变化。
"""
from __future__ import annotations

from clawarena_team.prompts import build_main_agent_system_prompt as build
from clawarena_team.tools.basic import BashTool, ReadTool
from clawarena_team.tools.subagent import RunSubagentTool
from clawarena_team.tools.workflow import WorkflowTool


_FULL = {"Read", "Write", "Edit", "Bash", "Grep", "Glob",
         "CreateSubagent", "RunSubagent", "ListSubagents", "Workflow"}


def test_all_tools_enabled_mentions_both_paths():
    p = build(enabled_tools=_FULL)
    assert "CreateSubagent" in p and "RunSubagent" in p
    assert "Workflow" in p and "defineAgent" in p
    assert "<task-notification>" in p
    assert "# Delegating work" in p and "# Asset triage" in p


def test_workflow_only_does_not_leak_subagent_tools():
    p = build(enabled_tools={"Read", "Write", "Edit", "Bash", "Grep", "Glob", "Workflow"})
    assert "CreateSubagent" not in p
    assert "RunSubagent" not in p
    # Workflow 仍在，且委派改走 defineAgent
    assert "Workflow" in p and "defineAgent" in p
    assert "<task-notification>" in p  # workflow 本身后台
    assert "# Asset triage" in p


def test_subagent_only_does_not_leak_workflow():
    p = build(enabled_tools={"Read", "Write", "Edit", "Bash", "Grep", "Glob",
                             "CreateSubagent", "RunSubagent"})
    assert "Workflow" not in p
    assert "defineAgent" not in p
    assert "CreateSubagent" in p


def test_no_delegation_no_background_sections():
    # 仅基础只读工具、无 Bash、无 subagent/workflow → 无后台、无委派、无 asset triage
    p = build(enabled_tools={"Read", "Grep", "Glob"})
    assert "<task-notification>" not in p
    assert "# Delegating work" not in p
    assert "# Asset triage" not in p
    # round-end 不应再提 background tasks
    assert "background tasks" not in p


def test_bash_only_background_mentions_bash_not_subagents():
    p = build(enabled_tools={"Read", "Write", "Edit", "Bash", "Grep", "Glob"})
    assert "<task-notification>" in p  # bash 可后台
    assert "backgrounded bash commands" in p
    assert "# Delegating work" not in p  # 无 subagent/workflow


def test_usage_thresholds_templated():
    p = build(thresholds_pct=[30, 60, 90])
    assert "30/60/90%" in p
    assert "50/60/70" not in p
    # consolidate 点取 >=80 的最低阈值
    assert "Above 90%" in p


def test_delegate_notice_kib_templated():
    p = build(delegate_notice_kib=64)
    assert "~64 KiB" in p


def test_dedicated_tools_line_lists_only_enabled():
    p = build(enabled_tools={"Read", "Grep", "Bash"})
    # 启用的专用工具出现，未启用的不出现在 "prefer dedicated" 行
    assert "Read (not cat/head/tail)" in p
    assert "Grep (not grep/rg)" in p
    assert "Edit (not sed/awk)" not in p
    assert "Write (not echo" not in p


def test_read_schema_kib_follows_config():
    d = ReadTool.schema(modalities=["text"], notice_bytes=65536, hard_bytes=131072)["description"]
    assert "~64 KiB" in d and "~128 KiB" in d


def test_bash_schema_timeout_follows_config():
    s = BashTool.schema(default_timeout_ms=300000)
    assert "Default: 300000 (5 min)" in s["description"]
    assert "Default 300000" in s["parameters"]["properties"]["timeout"]["description"]


def test_workflow_schema_caps_follow_config():
    d = WorkflowTool.schema(pool_keys="llm", pool_listing="x",
                            max_concurrency=4, max_agents=500)["description"]
    assert "4 agents at once" in d
    assert "(500)" in d
    # 关键用法段必须在场（pipeline vs parallel、范例、受限子集）
    assert "BARRIER" in d and "pipeline" in d
    assert "Worked example" in d
    assert "restricted interpreter" in d


def test_runsubagent_schema_default_no_braces_crash():
    # 确保 schema 构造不因模板花括号崩（既无 structured_output 也能构造）
    s = RunSubagentTool.schema()
    assert s["name"] == "RunSubagent"
