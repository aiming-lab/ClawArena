"""Tool registration and execution.

Every tool inherits from ``BaseTool`` and registers into ``TOOL_REGISTRY``. When
dispatching ``tool_calls``, AgentHarness injects runtime dependencies such as the
sandbox / read_tracker / cwd via ``ToolContext``; the tools themselves stay stateless.
"""
from __future__ import annotations

from .base import BaseTool, ToolContext, ToolExecResult
from .basic import BashTool, EditTool, GlobTool, GrepTool, ReadTool, WriteTool
from .subagent import (
    CreateSubagentTool,
    InspectSubagentTool,
    ListSubagentsTool,
    RunSubagentTool,
)
from .workflow import WorkflowTool

BASIC_TOOLS: dict[str, type[BaseTool]] = {
    ReadTool.name: ReadTool,
    WriteTool.name: WriteTool,
    EditTool.name: EditTool,
    BashTool.name: BashTool,
    GrepTool.name: GrepTool,
    GlobTool.name: GlobTool,
}

SUBAGENT_TOOLS: dict[str, type[BaseTool]] = {
    CreateSubagentTool.name: CreateSubagentTool,
    RunSubagentTool.name: RunSubagentTool,
    ListSubagentsTool.name: ListSubagentsTool,
    InspectSubagentTool.name: InspectSubagentTool,
}

# Workflow family (dynamic orchestration). Like SUBAGENT_TOOLS, available only to the main agent (subagents do not recurse).
WORKFLOW_TOOLS: dict[str, type[BaseTool]] = {
    WorkflowTool.name: WorkflowTool,
}

TOOL_REGISTRY: dict[str, type[BaseTool]] = {**BASIC_TOOLS, **SUBAGENT_TOOLS, **WORKFLOW_TOOLS}

__all__ = [
    "BaseTool",
    "ToolContext",
    "ToolExecResult",
    "BASIC_TOOLS",
    "SUBAGENT_TOOLS",
    "WORKFLOW_TOOLS",
    "TOOL_REGISTRY",
]
