"""WorkflowRuntime: backs the Workflow script's built-in primitives onto ``SubagentManager``.

The primitive signatures mirror claude-code dynamic workflows; the only addition is
``defineAgent`` (= a script-level version of CreateSubagent), because claude-code's
workflow cannot create agents and can only reference existing agentTypes. ClawArena-Team
adds it to fit the benchmark, and it **shares the same subagent pool as CreateSubagent**
-- agents defined via defineAgent inside the script and via CreateSubagent outside it are
mutually visible and callable through agent({agentType}).

Concurrency comes only from ``parallel`` / ``pipeline`` (which drive thunks / stages with
true concurrency via ``asyncio.gather``); the concurrency degree is bounded by a semaphore
from ``workflow.max_concurrency``, and ``workflow.max_agents`` is a hard cap on the total
number of ``agent()`` calls within a single run (to prevent runaways).
"""
from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

from ...prompts import WORKFLOW_AGENT_SYSTEM_SUFFIX
from .errors import WorkflowScriptError
from .interpreter import UNDEFINED, Interpreter, JsFunction, js_to_str


class WorkflowRuntime:
    def __init__(
        self,
        *,
        manager: Any,
        creator_cwd: Path,
        max_agents: int = 1000,
        max_concurrency: int = 8,
    ):
        self.manager = manager
        self.creator_cwd = creator_cwd
        self.max_agents = max_agents
        self._sem = asyncio.Semaphore(max(1, max_concurrency))
        self.interp: Interpreter | None = None
        # Progress / log records (used to generate the default summary when the script does not return).
        self.phases: list[str] = []
        self.logs: list[str] = []
        self.agent_calls = 0

    def bind_interpreter(self, interp: Interpreter) -> None:
        self.interp = interp

    # ------------------------------------------------------------------
    # builtins
    # ------------------------------------------------------------------
    def builtins(self) -> dict[str, Any]:
        import json as _json
        import math as _math

        def _math_ns() -> dict[str, Any]:
            return {
                "floor": lambda x: int(_math.floor(float(x))),
                "ceil": lambda x: int(_math.ceil(float(x))),
                "round": lambda x: int(round(float(x))),
                "abs": lambda x: abs(float(x)),
                "max": lambda *a: max(float(x) for x in a) if a else float("-inf"),
                "min": lambda *a: min(float(x) for x in a) if a else float("inf"),
                "sqrt": lambda x: _math.sqrt(float(x)),
                "pow": lambda a, b: float(a) ** float(b),
            }

        def _json_ns() -> dict[str, Any]:
            return {
                "stringify": lambda v, *rest: _json.dumps(_to_jsonable(v), ensure_ascii=False),
                "parse": lambda s, *rest: _json.loads(js_to_str(s)),
            }

        def _object_ns() -> dict[str, Any]:
            return {
                "keys": lambda o: list(o.keys()) if isinstance(o, dict) else [],
                "values": lambda o: list(o.values()) if isinstance(o, dict) else [],
                "entries": lambda o: [[k, v] for k, v in o.items()] if isinstance(o, dict) else [],
                "assign": _object_assign,
                "freeze": lambda o: o,
            }

        def _array_ns() -> dict[str, Any]:
            return {
                "from": _array_from,
                "isArray": lambda v: isinstance(v, list),
            }

        return {
            "agent": self._agent,
            "parallel": self._parallel,
            "pipeline": self._pipeline,
            "phase": self._phase,
            "log": self._log,
            "defineAgent": self._define_agent,
            "workflow": self._nested_workflow,
            "Math": _math_ns(),
            "JSON": _json_ns(),
            "Object": _object_ns(),
            "Array": _array_ns(),
            "console": {"log": self._log, "error": self._log, "warn": self._log},
        }

    # ------------------------------------------------------------------
    # Primitive implementations
    # ------------------------------------------------------------------
    def _opts(self, opts: Any) -> dict[str, Any]:
        return opts if isinstance(opts, dict) else {}

    async def _define_agent(self, spec: Any = UNDEFINED) -> str:
        s = self._opts(spec)
        name = js_to_str(s.get("name", "")) if s.get("name") not in (None, UNDEFINED) else ""
        if not name:
            raise WorkflowScriptError("defineAgent requires a 'name'")
        model_key = js_to_str(s.get("model_key") or s.get("modelKey") or "llm")
        tools = s.get("tools") or []
        if not isinstance(tools, list):
            raise WorkflowScriptError("defineAgent 'tools' must be an array")
        paths = s.get("accessible_paths") or s.get("paths") or []
        if not isinstance(paths, list):
            raise WorkflowScriptError("defineAgent 'accessible_paths' must be an array")
        system_prompt = js_to_str(s.get("system_prompt") or s.get("systemPrompt") or "")
        try:
            sub_id = await self.manager.create(
                creator_cwd=self.creator_cwd,
                name=name,
                system_prompt=system_prompt,
                model_key=model_key,
                tools=[js_to_str(t) for t in tools],
                accessible_paths=[js_to_str(p) for p in paths],
            )
        except (KeyError, ValueError) as e:
            raise WorkflowScriptError(f"defineAgent error: {e}") from e
        return name

    async def _agent(self, prompt: Any = "", opts: Any = UNDEFINED) -> Any:
        o = self._opts(opts)
        agent_type = o.get("agentType") or o.get("agent_type")
        if not agent_type or agent_type is UNDEFINED:
            raise WorkflowScriptError(
                "agent() requires opts.agentType naming a defined agent "
                "(use defineAgent({...}) first, or reference one created via CreateSubagent)"
            )
        name = js_to_str(agent_type)
        sub_id = self.manager.find_by_name(name)
        if sub_id is None:
            raise WorkflowScriptError(
                f"agent() agentType '{name}' not found; define it with defineAgent first"
            )
        schema = o.get("schema")
        schema = schema if isinstance(schema, dict) else None
        self.agent_calls += 1
        if self.agent_calls > self.max_agents:
            raise WorkflowScriptError(
                f"workflow exceeded max_agents={self.max_agents} (runaway loop?)"
            )
        async with self._sem:
            return await self.manager.invoke(
                subagent_id=sub_id,
                message=js_to_str(prompt),
                session_id=None,
                mode="workflow",
                schema=schema,
                workflow_prompt_suffix=WORKFLOW_AGENT_SYSTEM_SUFFIX,
            )

    async def _parallel(self, thunks: Any = UNDEFINED) -> list[Any]:
        items = thunks if isinstance(thunks, list) else []
        assert self.interp is not None

        async def _one(thunk: Any) -> Any:
            # Mirrors claude-code native: if a single thunk throws, that item resolves to
            # null and parallel itself does not reject (the caller can .filter(Boolean)).
            # Consistent with pipeline's "stage throws -> item becomes null".
            try:
                if isinstance(thunk, JsFunction):
                    return await self.interp.invoke_fn(thunk, [])
                if asyncio.iscoroutine(thunk):
                    return await thunk
                return thunk
            except Exception:  # noqa: BLE001
                return None

        return list(await asyncio.gather(*[_one(t) for t in items]))

    async def _pipeline(self, items: Any = UNDEFINED, *stages: Any) -> list[Any]:
        seq = items if isinstance(items, list) else []
        assert self.interp is not None

        async def _run_item(item: Any, idx: int) -> Any:
            cur = item
            for st in stages:
                if isinstance(st, JsFunction):
                    try:
                        cur = await self.interp.invoke_fn(st, [cur, item, idx])
                    except Exception:  # noqa: BLE001 -- if a stage throws, the item is dropped to None (mirrors native)
                        return None
                else:
                    cur = st
            return cur

        return list(await asyncio.gather(*[_run_item(it, i) for i, it in enumerate(seq)]))

    def _phase(self, title: Any = "", *rest: Any) -> Any:
        self.phases.append(js_to_str(title))
        return UNDEFINED

    def _log(self, *args: Any) -> Any:
        self.logs.append(" ".join(js_to_str(a) for a in args))
        return UNDEFINED

    async def _nested_workflow(self, ref: Any = "", sub_args: Any = UNDEFINED) -> Any:
        """Nested workflow(): run ref as a script source in place again (sharing the same manager / pool).

        ClawArena-Team has no "named saved workflow" registry, so ref is interpreted as a
        script source string (or a {script} object). Returns the return value of the
        sub-script.
        """
        if isinstance(ref, dict):
            source = js_to_str(ref.get("script", ""))
        else:
            source = js_to_str(ref)
        if not source.strip():
            raise WorkflowScriptError("nested workflow() needs a script source string")
        sub_interp = Interpreter(self.builtins())
        # The sub-script shares the same runtime's interp binding for parallel/pipeline callbacks.
        prev = self.interp
        self.bind_interpreter(sub_interp)
        try:
            globals_for_sub = {"args": sub_args if sub_args is not UNDEFINED else UNDEFINED}
            return await sub_interp.run(source, globals_for_sub)
        finally:
            self.bind_interpreter(prev)

    # ------------------------------------------------------------------
    # Default summary (when the script does not return)
    # ------------------------------------------------------------------
    def default_summary(self) -> str:
        parts = [f"agent() calls: {self.agent_calls}"]
        if self.phases:
            parts.append("phases: " + " -> ".join(self.phases))
        if self.logs:
            tail = self.logs[-10:]
            parts.append("logs:\n" + "\n".join(f"  - {x}" for x in tail))
        return "\n".join(parts)


def _to_jsonable(v: Any) -> Any:
    if v is UNDEFINED:
        return None
    if isinstance(v, dict):
        return {k: _to_jsonable(x) for k, x in v.items()}
    if isinstance(v, list):
        return [_to_jsonable(x) for x in v]
    return v


def _object_assign(target: Any, *sources: Any) -> Any:
    if not isinstance(target, dict):
        target = {}
    for s in sources:
        if isinstance(s, dict):
            target.update(s)
    return target


def _array_from(v: Any, *rest: Any) -> list[Any]:
    if isinstance(v, list):
        return list(v)
    if isinstance(v, str):
        return list(v)
    if isinstance(v, dict):
        # Array.from({length: n}) form
        if "length" in v:
            try:
                n = int(v["length"])
                return [UNDEFINED] * n
            except (ValueError, TypeError):
                return []
        return list(v.values())
    return []
