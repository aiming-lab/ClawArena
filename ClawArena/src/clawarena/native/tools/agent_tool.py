"""Agent 工具——给 main agent 一个 Spawn subagent 的入口。

参考 AutoHarness ``plugin/tools/agent_tool.py`` 设计。两种 subagent：

- ``Explore``：只读研究 agent。工具集 = {Read, LS, Grep, Glob}
- ``general-purpose``：完整能力 agent。工具集 = {Bash, Read, Write, Edit, Glob,
  Grep, LS}；**不可** spawn 进一步的 subagent（防递归）

实际 spawn 逻辑由 :class:`arcbench.agent.subagent.SubagentManager` 实现；本工具
只是把 (subagent_type, description, prompt) 转交给 manager 并把答案塞回 main。
"""
from __future__ import annotations

from typing import Any

from ..prompts import TOOL_DESCRIPTIONS, TOOL_PARAM_DESCRIPTIONS
from .base import BaseTool, ToolContext, ToolExecResult


_VALID_TYPES = ("Explore", "general-purpose")


class AgentTool(BaseTool):
    name = "Agent"

    @classmethod
    def schema(cls, **_: Any) -> dict[str, Any]:
        p = TOOL_PARAM_DESCRIPTIONS["Agent"]
        return {
            "name": cls.name,
            "description": TOOL_DESCRIPTIONS["Agent"],
            "parameters": {
                "type": "object",
                "properties": {
                    "subagent_type": {
                        "type": "string",
                        "enum": list(_VALID_TYPES),
                        "description": p["subagent_type"],
                    },
                    "description": {"type": "string", "description": p["description"]},
                    "prompt": {"type": "string", "description": p["prompt"]},
                },
                "required": ["subagent_type", "description", "prompt"],
            },
        }

    async def run(self, args: dict[str, Any], ctx: ToolContext) -> ToolExecResult:
        manager = getattr(ctx, "subagent_manager", None)
        if manager is None:
            return ToolExecResult(
                "Agent tool is unavailable: this agent cannot spawn subagents.",
                is_error=True,
            )
        sub_type = args.get("subagent_type", "")
        description = args.get("description", "")
        prompt = args.get("prompt", "")
        if not sub_type:
            return ToolExecResult("subagent_type is required", is_error=True)
        if sub_type not in _VALID_TYPES:
            return ToolExecResult(
                f"unknown subagent_type {sub_type!r}; valid: {list(_VALID_TYPES)}",
                is_error=True,
            )
        if not description:
            return ToolExecResult("description is required", is_error=True)
        if not prompt:
            return ToolExecResult("prompt is required", is_error=True)

        result = await manager.run(
            subagent_type=sub_type, description=description, prompt=prompt
        )
        ctx.tools_used.add(self.name)
        if result.error:
            return ToolExecResult(f"subagent failed: {result.error}", is_error=True)
        header = (
            f"[Agent:{sub_type}] {description}\n"
            f"[iterations={result.iterations_used}]\n"
        )
        return ToolExecResult(header + (result.answer or "[subagent returned no text]"))
