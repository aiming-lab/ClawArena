"""Subagent management tools: CreateSubagent / RunSubagent / ListSubagents / InspectSubagent.

The naming style mirrors claude-code's ``Agent`` tool: CapitalCase; ``RunSubagent``
reuses the ``description`` + ``prompt`` + ``run_in_background`` field convention.

The actual work (creation, scheduling, recording) is forwarded to
``ctx.subagent_manager`` (a SubagentManager instance). This layer only parses
arguments and exposes the schema.
"""
from __future__ import annotations

from typing import Any

from ..prompts import TOOL_DESCRIPTIONS, TOOL_PARAM_DESCRIPTIONS
from .base import BaseTool, ToolContext, ToolExecResult


def _params(tool: str) -> dict[str, str]:
    return TOOL_PARAM_DESCRIPTIONS[tool]


def _require_manager(ctx: ToolContext) -> Any | None:
    if ctx.subagent_manager is None:
        return None
    return ctx.subagent_manager


class CreateSubagentTool(BaseTool):
    name = "CreateSubagent"

    @classmethod
    def schema(cls, **format_kwargs: Any) -> dict[str, Any]:
        pool_keys = format_kwargs.get("pool_keys", "llm/vlm/omni")
        pool_listing = format_kwargs.get("pool_listing", "(none)")
        subagent_token_limit = int(format_kwargs.get("subagent_token_limit", 100000))
        desc = TOOL_DESCRIPTIONS["CreateSubagent"].format(
            pool_keys=pool_keys,
            pool_listing=pool_listing,
            subagent_token_limit=f"{subagent_token_limit:,}",
            subagent_token_limit_quarter=f"{subagent_token_limit // 4:,}",
        )
        p = _params("CreateSubagent")
        return {
            "name": cls.name,
            "description": desc,
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": p["name"]},
                    "system_prompt": {"type": "string", "description": p["system_prompt"]},
                    "model_key": {
                        "type": "string",
                        "enum": ["llm", "vlm", "omni"],
                        "description": p["model_key"].format(pool_keys=pool_keys),
                    },
                    "tools": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": p["tools"],
                    },
                    "accessible_paths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": p["accessible_paths"],
                    },
                },
                "required": ["name", "system_prompt", "model_key", "tools", "accessible_paths"],
            },
        }

    async def run(self, args: dict[str, Any], ctx: ToolContext) -> ToolExecResult:
        mgr = _require_manager(ctx)
        if mgr is None:
            return ToolExecResult("CreateSubagent unavailable (no subagent manager)", is_error=True)
        ctx.tools_used.add(self.name)
        try:
            sub_id = await mgr.create(
                creator_cwd=ctx.cwd,
                name=args["name"],
                system_prompt=args["system_prompt"],
                model_key=args["model_key"],
                tools=args["tools"],
                accessible_paths=args["accessible_paths"],
            )
        except (KeyError, ValueError) as e:
            return ToolExecResult(f"CreateSubagent error: {e}", is_error=True)
        return ToolExecResult(f"subagent_id={sub_id}")


class RunSubagentTool(BaseTool):
    name = "RunSubagent"
    description = TOOL_DESCRIPTIONS["RunSubagent"]

    @classmethod
    def schema(cls, **format_kwargs: Any) -> dict[str, Any]:
        p = _params("RunSubagent")
        props: dict[str, Any] = {
            "subagent_id": {"type": "string", "description": p["subagent_id"]},
            "description": {"type": "string", "description": p["description"]},
            "prompt": {"type": "string", "description": p["prompt"]},
            "session_id": {"type": "string", "description": p["session_id"]},
            "run_in_background": {
                "type": "boolean",
                "default": False,
                "description": p["run_in_background"],
            },
        }
        # The schema parameter is off by default (the native Agent tool has no such
        # capability); it is exposed only when structured_output.runsubagent_enabled is
        # set, to avoid advertising a parameter to the model that the runtime ignores.
        if format_kwargs.get("structured_output_enabled"):
            props["schema"] = {"type": "object", "description": p["schema"]}
        return {
            "name": cls.name,
            "description": cls.description,
            "parameters": {
                "type": "object",
                "properties": props,
                "required": ["subagent_id", "description", "prompt"],
            },
        }

    async def run(self, args: dict[str, Any], ctx: ToolContext) -> ToolExecResult:
        mgr = _require_manager(ctx)
        if mgr is None:
            return ToolExecResult("RunSubagent unavailable", is_error=True)
        ctx.tools_used.add(self.name)
        background = bool(args.get("run_in_background", False))
        mode = "background" if background else "runtime"
        # schema takes effect only when enabled in config (off by default); structured
        # output is not supported in background mode (results flow through the notification channel).
        schema = None
        if ctx.config.get("structured_output.runsubagent_enabled") and not background:
            raw = args.get("schema")
            schema = raw if isinstance(raw, dict) else None
        try:
            result = await mgr.invoke(
                subagent_id=args["subagent_id"],
                message=args["prompt"],
                session_id=args.get("session_id"),
                mode=mode,
                schema=schema,
            )
        except (KeyError, ValueError) as e:
            return ToolExecResult(f"RunSubagent error: {e}", is_error=True)
        # Serialize a structured result (dict) to text before returning, so it fits into tool_result.
        if isinstance(result, (dict, list)):
            import json
            return ToolExecResult(json.dumps(result, ensure_ascii=False, default=str))
        return ToolExecResult(result)


class ListSubagentsTool(BaseTool):
    name = "ListSubagents"
    description = TOOL_DESCRIPTIONS["ListSubagents"]

    @classmethod
    def schema(cls, **_: Any) -> dict[str, Any]:
        return {
            "name": cls.name,
            "description": cls.description,
            "parameters": {"type": "object", "properties": {}},
        }

    async def run(self, args: dict[str, Any], ctx: ToolContext) -> ToolExecResult:
        mgr = _require_manager(ctx)
        if mgr is None:
            return ToolExecResult("ListSubagents unavailable", is_error=True)
        ctx.tools_used.add(self.name)
        return ToolExecResult(mgr.summary())


class InspectSubagentTool(BaseTool):
    name = "InspectSubagent"
    description = TOOL_DESCRIPTIONS["InspectSubagent"]

    @classmethod
    def schema(cls, **_: Any) -> dict[str, Any]:
        return {
            "name": cls.name,
            "description": cls.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": _params("InspectSubagent")["session_id"],
                    }
                },
                "required": ["session_id"],
            },
        }

    async def run(self, args: dict[str, Any], ctx: ToolContext) -> ToolExecResult:
        mgr = _require_manager(ctx)
        if mgr is None:
            return ToolExecResult("InspectSubagent unavailable", is_error=True)
        ctx.tools_used.add(self.name)
        try:
            transcript = mgr.inspect(args["session_id"])
        except KeyError as e:
            return ToolExecResult(f"InspectSubagent error: {e}", is_error=True)
        return ToolExecResult(transcript)
