"""The ``Workflow`` tool: dynamic orchestration (mirrors claude-code dynamic workflows).

The main agent under test submits a script in JS syntax (``script``, or reuses a
previously persisted script via ``scriptPath``); ClawArena-Team parses it into an AST and
runs it with the built-in async interpreter. The orchestration primitives in the script
are backed by ``SubagentManager`` and share the same subagent pool as
``CreateSubagent`` / ``RunSubagent``.

Execution semantics (finalized per the ClawArena-Team design):
- **Background execution**: the tool call returns a ``task id`` + script backup path
  immediately; once the script finishes it notifies via ``<task-notification>``, and the
  result is whatever the script ``return``s (falling back to a summary if there is no return).
- After ``script`` is written, a backup is persisted to the ``workflows/`` directory
  alongside the scenario's ``sessions/``; the path is given in the immediately-returned
  tool result so it can later be reused via ``scriptPath``.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ...prompts import (
    TOOL_PARAM_DESCRIPTIONS,
    WORKFLOW_ERROR_REMINDER,
    WORKFLOW_RESULT_REMINDER,
    build_workflow_description,
)
from ..base import BaseTool, ToolContext, ToolExecResult
from .errors import WorkflowError
from .interpreter import UNDEFINED, Interpreter
from .runtime import WorkflowRuntime, _to_jsonable


def _params() -> dict[str, str]:
    return TOOL_PARAM_DESCRIPTIONS["Workflow"]


class WorkflowTool(BaseTool):
    name = "Workflow"

    @classmethod
    def schema(cls, **format_kwargs: Any) -> dict[str, Any]:
        desc = build_workflow_description(
            pool_keys=format_kwargs.get("pool_keys", "llm/vlm/omni"),
            pool_listing=format_kwargs.get("pool_listing", "(none)"),
            max_concurrency=int(format_kwargs.get("max_concurrency", 8)),
            max_agents=int(format_kwargs.get("max_agents", 1000)),
        )
        p = _params()
        return {
            "name": cls.name,
            "description": desc,
            "parameters": {
                "type": "object",
                "properties": {
                    "script": {"type": "string", "description": p["script"]},
                    "name": {"type": "string", "description": p["name"]},
                    "args": {"description": p["args"]},
                    "scriptPath": {"type": "string", "description": p["scriptPath"]},
                },
                "required": [],
            },
        }

    def _resolve_source(self, args: dict[str, Any], ctx: ToolContext) -> tuple[str, Path | None]:
        script = args.get("script")
        script_path = args.get("scriptPath")
        if script_path:
            p = Path(script_path)
            if not p.is_absolute() and ctx.workflow_script_dir is not None:
                p = Path(ctx.workflow_script_dir) / p
            if not p.exists():
                raise WorkflowError(f"scriptPath not found: {script_path}")
            return p.read_text(encoding="utf-8"), p
        if not script:
            raise WorkflowError("Workflow requires either 'script' or 'scriptPath'")
        return script, None

    def _persist(self, source: str, ctx: ToolContext) -> Path | None:
        if ctx.workflow_script_dir is None:
            return None
        d = Path(ctx.workflow_script_dir)
        d.mkdir(parents=True, exist_ok=True)
        n = len(list(d.glob("workflow_*.js"))) + 1
        path = d / f"workflow_{n:03d}.js"
        path.write_text(source, encoding="utf-8")
        return path

    async def run(self, args: dict[str, Any], ctx: ToolContext) -> ToolExecResult:
        if ctx.subagent_manager is None:
            return ToolExecResult("Workflow unavailable (no subagent manager)", is_error=True)
        if ctx.background is None:
            return ToolExecResult(
                "Workflow unavailable: only the main agent can run workflows.", is_error=True
            )
        ctx.tools_used.add(self.name)
        try:
            source, existing = self._resolve_source(args, ctx)
        except WorkflowError as e:
            return ToolExecResult(str(e), is_error=True)

        saved = existing if existing is not None else self._persist(source, ctx)
        wf_name = str(args.get("name") or "workflow")
        wf_args = args.get("args", UNDEFINED)

        cfg = ctx.config
        runtime = WorkflowRuntime(
            manager=ctx.subagent_manager,
            creator_cwd=ctx.cwd,
            max_agents=int(cfg.get("workflow.max_agents", 1000)),
            max_concurrency=int(cfg.get("workflow.max_concurrency", 8)),
        )
        interp = Interpreter(runtime.builtins())
        runtime.bind_interpreter(interp)

        task_id = ctx.background.new_task_id("workflow")

        async def _body() -> str:
            try:
                result = await interp.run(
                    source, {"args": wf_args if wf_args is not UNDEFINED else UNDEFINED}
                )
                if result is UNDEFINED or result is None:
                    rendered = runtime.default_summary()
                else:
                    rendered = _render_result(result)
                return WORKFLOW_RESULT_REMINDER.format(
                    task_id=task_id, name=wf_name, result=rendered
                )
            except Exception as e:  # noqa: BLE001
                return WORKFLOW_ERROR_REMINDER.format(
                    task_id=task_id, name=wf_name, error=str(e)
                )

        ctx.background.spawn("workflow", _body(), task_id=task_id)

        path_note = f" Script saved to {saved}." if saved is not None else ""
        return ToolExecResult(
            f"workflow '{wf_name}' started in background, task_id={task_id}."
            f"{path_note} You'll receive a <task-notification> with its result when it "
            f"completes; do not poll — continue with other work or wait for the round to settle."
        )


def _render_result(result: Any) -> str:
    jsonable = _to_jsonable(result)
    try:
        return json.dumps(jsonable, ensure_ascii=False, indent=2, default=str)
    except (TypeError, ValueError):
        return str(result)
