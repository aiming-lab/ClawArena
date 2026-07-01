"""WorkflowRuntime：把 Workflow 脚本的内置原语 backed 到 ``SubagentManager``。

与 SMbench 版本的差异（clawarena-native 改造点）：

- **删除 ``defineAgent``**：本 harness 对齐 ArcBench 的 ``Agent`` 工具——subagent 类型
  是 harness 固定提供的，不允许脚本自创建。
- ``agent(prompt, opts)`` 的 ``opts.subagent_type`` 只能取 ``"Explore"`` /
  ``"general-purpose"``，**默认 ``"general-purpose"``**；非法值报 ``WorkflowScriptError``。
- ``agent()`` 直接调 :meth:`SubagentManager.run`（ArcBench 接口），而非 SMbench 的
  ``find_by_name`` + ``invoke``。``opts.schema`` 非空时走结构化输出，resolve 为校验过的
  对象。

并发只来自 ``parallel`` / ``pipeline``（用 ``asyncio.gather`` 真并发驱动 thunk / stage），
并发度由 ``workflow.max_concurrency`` 经信号量约束；``workflow.max_agents`` 是单次运行
内 ``agent()`` 调用总数的硬上限（防失控）。
"""
from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

from ...prompts import WORKFLOW_AGENT_SYSTEM_SUFFIX
from .errors import WorkflowScriptError
from .interpreter import UNDEFINED, Interpreter, JsFunction, js_to_str

# harness 固定提供的 subagent 类型（对齐 ArcBench Agent 工具）。
_VALID_SUBAGENT_TYPES = ("Explore", "general-purpose")
_DEFAULT_SUBAGENT_TYPE = "general-purpose"


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
        # 进度/日志记录（脚本未 return 时用于生成默认摘要）。
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
            "workflow": self._nested_workflow,
            "Math": _math_ns(),
            "JSON": _json_ns(),
            "Object": _object_ns(),
            "Array": _array_ns(),
            "console": {"log": self._log, "error": self._log, "warn": self._log},
        }

    # ------------------------------------------------------------------
    # 原语实现
    # ------------------------------------------------------------------
    def _opts(self, opts: Any) -> dict[str, Any]:
        return opts if isinstance(opts, dict) else {}

    async def _agent(self, prompt: Any = "", opts: Any = UNDEFINED) -> Any:
        o = self._opts(opts)
        raw_type = o.get("subagent_type") or o.get("subagentType") or o.get("agentType")
        sub_type = (
            js_to_str(raw_type)
            if raw_type not in (None, UNDEFINED, "")
            else _DEFAULT_SUBAGENT_TYPE
        )
        if sub_type not in _VALID_SUBAGENT_TYPES:
            raise WorkflowScriptError(
                f"agent() subagent_type {sub_type!r} is invalid; choose one of "
                f"{list(_VALID_SUBAGENT_TYPES)} (there is no defineAgent in this harness)"
            )
        schema = o.get("schema")
        schema = schema if isinstance(schema, dict) else None
        description = js_to_str(o.get("description") or o.get("label") or "workflow step")
        self.agent_calls += 1
        if self.agent_calls > self.max_agents:
            raise WorkflowScriptError(
                f"workflow exceeded max_agents={self.max_agents} (runaway loop?)"
            )
        async with self._sem:
            result = await self.manager.run(
                subagent_type=sub_type,
                description=description,
                prompt=js_to_str(prompt),
                schema=schema,
                system_suffix=WORKFLOW_AGENT_SYSTEM_SUFFIX,
            )
        if getattr(result, "error", None):
            raise WorkflowScriptError(f"agent() failed: {result.error}")
        # schema 非空 → 返回校验过的结构化对象；否则返回文本。
        if schema is not None and getattr(result, "data", None) is not None:
            return result.data
        return result.answer

    async def _parallel(self, thunks: Any = UNDEFINED) -> list[Any]:
        items = thunks if isinstance(thunks, list) else []
        assert self.interp is not None

        async def _one(thunk: Any) -> Any:
            # 单个 thunk 抛错则该项解析为 null，parallel 本身不 reject
            # （调用方 .filter(Boolean) 即可）。与 pipeline 的「stage 抛错→item 落 null」一致。
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
                    except Exception:  # noqa: BLE001 —— 某 stage 抛错则该 item 丢为 None
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
        """嵌套 workflow()：把 ref 作为脚本源就地再跑一遍（共享同一 manager / 池）。

        ref 解释为脚本源字符串（或 ``{script}`` 对象）。返回子脚本的 return 值。
        """
        if isinstance(ref, dict):
            source = js_to_str(ref.get("script", ""))
        else:
            source = js_to_str(ref)
        if not source.strip():
            raise WorkflowScriptError("nested workflow() needs a script source string")
        sub_interp = Interpreter(self.builtins())
        prev = self.interp
        self.bind_interpreter(sub_interp)
        try:
            globals_for_sub = {"args": sub_args if sub_args is not UNDEFINED else UNDEFINED}
            return await sub_interp.run(source, globals_for_sub)
        finally:
            self.bind_interpreter(prev)

    # ------------------------------------------------------------------
    # 默认摘要（脚本未 return 时）
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
        # Array.from({length: n}) 形态
        if "length" in v:
            try:
                n = int(v["length"])
                return [UNDEFINED] * n
            except (ValueError, TypeError):
                return []
        return list(v.values())
    return []
