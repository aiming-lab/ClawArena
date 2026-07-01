"""SubagentManager: handles the main agent's full-lifecycle management of subagents.

Responsibilities:
- Validate creation parameters: tool allowlist (excludes the subagent family);
  accessible_paths must be a subset of the creator's.
- Instantiate the subagent's AgentHarness (without the subagent tools).
- runtime invocation: block and wait for the subagent loop to finish.
- background invocation: asyncio.create_task, and after completion inject a user
  message into main via a callback.
"""
from __future__ import annotations

import asyncio
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from ..prompts import (
    BACKGROUND_ERROR_REMINDER,
    BACKGROUND_RESULT_REMINDER,
    SUBAGENT_DEFAULT_SYSTEM_PROMPT,
)
from ..provider import build_provider
from ..sandbox import AccessibleScope, ReadTracker
from ..tokenizer import UnifiedTokenizer
from ..tools import BASIC_TOOLS
from ..types import (
    Modality,
    ModelBundle,
    SessionMeta,
    SubagentLifecycleStat,
    SubagentSpec,
)
from .harness import AgentHarness, HarnessConfig


@dataclass
class SubagentRecord:
    spec: SubagentSpec
    harnesses: dict[str, AgentHarness] = field(default_factory=dict)  # session_id -> harness
    stat: SubagentLifecycleStat = None  # type: ignore[assignment]
    background_tasks: dict[str, asyncio.Task] = field(default_factory=dict)


class SubagentManager:
    def __init__(
        self,
        *,
        scenario_root: Path,
        creator_scope: AccessibleScope,
        model_bundle: ModelBundle,
        tokenizer: UnifiedTokenizer,
        config_dict: dict[str, Any],
        sub_token_limit: int,
        usage_thresholds_pct: list[int],
        max_iterations: int,
        on_session_complete=None,
        on_background_complete=None,
    ):
        self.scenario_root = scenario_root
        self.creator_scope = creator_scope
        self.model_bundle = model_bundle
        self.tokenizer = tokenizer
        self.config_dict = config_dict
        self.sub_token_limit = sub_token_limit
        self.usage_thresholds_pct = usage_thresholds_pct
        self.max_iterations = max_iterations
        self.on_session_complete = on_session_complete
        self.on_background_complete = on_background_complete

        self.records: dict[str, SubagentRecord] = {}
        self.invocation_distribution: dict[str, int] = {}
        # Number of subagent calls with schema-forced structured output (statistics item).
        self.structured_output_calls: int = 0
        self._main_inject = None  # set later
        # Unified background-task registry (owned by the main harness); assigned after attach_main.
        self.background_registry = None
        # Background subagent session id -> its task_id in the registry (for summary to query running state).
        self._bg_sessions: dict[str, str] = {}

    def attach_main(self, main_harness) -> None:
        self._main_inject = main_harness.inject_background_user
        self.background_registry = main_harness.background

    def find_by_name(self, name: str) -> Optional[str]:
        """Find an already-created/already-defined subagent_id by name (CreateSubagent
        and Workflow.defineAgent share the same pool). On name collisions, takes the most recently created one."""
        match = None
        for sub_id, rec in self.records.items():
            if rec.spec.name == name:
                match = sub_id
        return match

    # ------------------------------------------------------------------
    # create
    # ------------------------------------------------------------------

    async def create(
        self,
        *,
        creator_cwd: Path,
        name: str,
        system_prompt: str,
        model_key: str,
        tools: list[str],
        accessible_paths: list[str],
    ) -> str:
        try:
            modality = Modality(model_key)
        except ValueError:
            raise ValueError(f"unknown model_key: {model_key}")
        if modality not in self.model_bundle.pool:
            raise ValueError(f"model_key {model_key} is not configured in pool")

        # tool allowlist: forbid the subagent family + basic tools only
        invalid = [t for t in tools if t not in BASIC_TOOLS]
        if invalid:
            raise ValueError(f"invalid tools for subagent: {invalid}")

        # path allowlist: must be a subset of the creator's scope
        resolved_paths: list[Path] = []
        for raw in accessible_paths:
            p = Path(raw)
            if not p.is_absolute():
                p = (creator_cwd / p).resolve(strict=False)
            else:
                p = p.resolve(strict=False)
            if not self.creator_scope.is_allowed(p):
                raise ValueError(f"path {raw} not allowed for this subagent")
            resolved_paths.append(p)

        sub_id = f"sub_{uuid.uuid4().hex[:8]}"
        spec = SubagentSpec(
            subagent_id=sub_id,
            name=name,
            system_prompt=system_prompt or SUBAGENT_DEFAULT_SYSTEM_PROMPT,
            model_key=modality,
            tools=list(tools),
            accessible_paths=resolved_paths,
        )
        stat = SubagentLifecycleStat(
            subagent_id=sub_id,
            name=name,
            model_key=modality,
            tools_granted=list(tools),
            tools_used=set(),
            accessible_paths=resolved_paths,
        )
        # Compute the total number of reachable files (for scoring)
        sub_scope = AccessibleScope(resolved_paths, scenario_root=self.scenario_root)
        stat.files_accessible_total = len(sub_scope.enumerate_reachable_files())
        self.records[sub_id] = SubagentRecord(spec=spec, stat=stat)
        return sub_id

    # ------------------------------------------------------------------
    # invoke
    # ------------------------------------------------------------------

    def _build_harness(
        self,
        rec: SubagentRecord,
        session_id: str,
        *,
        workflow_prompt_suffix: Optional[str] = None,
    ) -> AgentHarness:
        sub_scope = AccessibleScope(rec.spec.accessible_paths, scenario_root=self.scenario_root)
        sub_tracker = ReadTracker()
        pool_entry = self.model_bundle.pool[rec.spec.model_key]
        provider = build_provider(pool_entry.config)
        agent_modalities = list(pool_entry.effective_modalities)
        agent_limits = dict(pool_entry.config.modality_limits)
        tools = {n: cls() for n, cls in BASIC_TOOLS.items() if n in rec.spec.tools}
        read_cfg = self.config_dict.get("read", {})
        basic_kwargs = dict(
            modalities=agent_modalities,
            modality_limits=agent_limits,
            notice_bytes=int(read_cfg.get("notice_bytes", 32768)),
            hard_bytes=int(read_cfg.get("hard_bytes", 262144)),
            default_timeout_ms=int(self.config_dict.get("bash", {}).get("default_timeout_ms", 120000)),
        )
        schemas = [
            cls.schema(**basic_kwargs)
            for n, cls in BASIC_TOOLS.items()
            if n in rec.spec.tools
        ]
        cfg = HarnessConfig(
            token_limit=self.sub_token_limit,
            usage_thresholds_pct=self.usage_thresholds_pct,
            always_hint_on_real_user=True,
            max_iterations=self.max_iterations,
        )
        cwd = rec.spec.accessible_paths[0] if rec.spec.accessible_paths else self.scenario_root
        system_prompt = rec.spec.system_prompt
        # When invoked via Workflow's agent() path, append the "final text is the
        # return value" suffix to the end of the system prompt, aligned with
        # claude-code native (subagents return raw data rather than human-facing messages).
        if workflow_prompt_suffix:
            system_prompt = system_prompt.rstrip() + "\n\n" + workflow_prompt_suffix
        h = AgentHarness(
            agent_id=f"{rec.spec.subagent_id}:{session_id}",
            system_prompt=system_prompt,
            provider=provider,
            tools=tools,
            tool_schemas=schemas,
            scope=sub_scope,
            read_tracker=sub_tracker,
            cwd=cwd,
            tokenizer=self.tokenizer,
            cfg=cfg,
            config_dict=self.config_dict,
            agent_modalities=agent_modalities,
            modality_limits=agent_limits,
            subagent_manager=None,
        )
        return h

    async def invoke(
        self,
        *,
        subagent_id: str,
        message: str,
        session_id: Optional[str],
        mode: str,
        schema: Optional[dict] = None,
        workflow_prompt_suffix: Optional[str] = None,
    ) -> Any:
        if subagent_id not in self.records:
            raise KeyError(f"subagent {subagent_id} not found")
        rec = self.records[subagent_id]
        new_session = session_id is None or session_id not in rec.harnesses
        sid = session_id or f"sess_{uuid.uuid4().hex[:8]}"
        if new_session:
            rec.harnesses[sid] = self._build_harness(
                rec, sid, workflow_prompt_suffix=workflow_prompt_suffix
            )
            rec.stat.sessions.append(
                SessionMeta(
                    session_id=sid,
                    owner_id=subagent_id,
                    started_at=time.time(),
                    mode=mode if mode != "workflow" else "runtime",  # type: ignore[arg-type]
                )
            )
        # invocation distribution: workflow is the flattened 5th class, the rest are {new,continue}x{runtime,background}.
        key = "workflow" if mode == "workflow" else (("new" if new_session else "continue") + "+" + mode)
        self.invocation_distribution[key] = self.invocation_distribution.get(key, 0) + 1
        if schema is not None:
            self.structured_output_calls += 1

        harness = rec.harnesses[sid]

        if mode in ("runtime", "workflow"):
            return await self._run_session(rec, harness, message, schema=schema)
        elif mode == "background":
            if self.background_registry is None:
                # No registry (in theory only in test scenarios detached from main): degrade to synchronous execution.
                return await self._run_session(rec, harness, message)
            coro = self._background_body(rec, harness, sid, message)
            task_id = self.background_registry.spawn("subagent", coro)
            self._bg_sessions[sid] = task_id
            return (
                f"background started, task_id={task_id}, subagent_id={subagent_id}, "
                f"session_id={sid}. You'll receive a <task-notification> when it completes."
            )
        else:
            raise ValueError(f"unknown mode: {mode}")

    async def _run_session(
        self,
        rec: SubagentRecord,
        harness: AgentHarness,
        message: str,
        *,
        schema: Optional[dict] = None,
    ) -> Any:
        try:
            answer = await harness.send_user(message, is_real_question=True, schema=schema)
        except Exception as e:  # noqa: BLE001
            answer = f"[subagent error] {e}"
        self._merge_lifecycle(rec, harness)
        return answer

    async def _background_body(
        self, rec: SubagentRecord, harness: AgentHarness, sid: str, message: str
    ) -> str:
        try:
            answer = await harness.send_user(message, is_real_question=True)
            payload = BACKGROUND_RESULT_REMINDER.format(
                subagent_id=rec.spec.subagent_id, session_id=sid, result=answer
            )
        except Exception as e:  # noqa: BLE001
            payload = BACKGROUND_ERROR_REMINDER.format(
                subagent_id=rec.spec.subagent_id, session_id=sid, error=str(e)
            )
        self._merge_lifecycle(rec, harness)
        if self.on_background_complete is not None:
            self.on_background_complete(rec.spec.subagent_id, sid, payload)
        return payload

    def _merge_lifecycle(self, rec: SubagentRecord, harness: AgentHarness) -> None:
        # Fix (fix/audit-top10 #6 + W1 F1):
        # harness.{input/output/cache}_token_total, scope.forbidden_count, modality_counter
        # are **monotonically accumulated** over the harness lifecycle; continue mode
        # reuses the same harness, and the original `+=` would add the historical total
        # again, producing an O(N^2) cumulative error after N invokes.
        # Here we use `harness._last_merged` to record the last watermark and aggregate
        # only the delta this time; we also change endswith to == strict matching to
        # avoid false matches.
        rec.stat.tools_used.update(harness.tools_used)
        last = getattr(harness, "_last_merged", None) or {}

        # delta-aware aggregation
        rec.stat.forbidden_count += max(0, harness.scope.forbidden_count - last.get("forb", 0))
        for k, v in harness.modality_counter.items():
            d = v - last.get(f"m:{k}", 0)
            if d > 0:
                rec.stat.modality_usage[k] = rec.stat.modality_usage.get(k, 0) + d
        rec.stat.files_accessed.update(harness.read_tracker._hashes.keys())  # noqa: SLF001

        own_sid = harness.agent_id.split(":", 1)[1] if ":" in harness.agent_id else harness.agent_id
        for sess in rec.stat.sessions:
            if sess.session_id == own_sid:
                sess.context_size_max = max(sess.context_size_max, harness.context_size_max)
                sess.input_token_total += max(0, harness.input_token_total - last.get("in", 0))
                sess.output_token_total += max(0, harness.output_token_total - last.get("out", 0))
                sess.cache_read_total += max(0, harness.cache_read_total - last.get("cache", 0))
                sess.ended_at = time.time()

        # Record this watermark for the next invoke merge to take the delta
        harness._last_merged = {
            "forb": harness.scope.forbidden_count,
            "in": harness.input_token_total,
            "out": harness.output_token_total,
            "cache": harness.cache_read_total,
            **{f"m:{k}": v for k, v in harness.modality_counter.items()},
        }

    # ------------------------------------------------------------------
    # background completion check (used by runner round-end judgement)
    # ------------------------------------------------------------------

    def any_background_running(self) -> bool:
        # Delegate to the unified registry: covers all three classes of background subagent / bash / workflow.
        if self.background_registry is None:
            return False
        return self.background_registry.any_running()

    async def wait_for_backgrounds(self) -> None:
        if self.background_registry is not None:
            await self.background_registry.wait_all()

    # ------------------------------------------------------------------
    # summary / inspection
    # ------------------------------------------------------------------

    def summary(self) -> str:
        lines = ["== created subagents =="]
        for sub_id, rec in self.records.items():
            lines.append(
                f"  {sub_id}  name={rec.spec.name}  model_key={rec.spec.model_key.value}  tools={rec.spec.tools}"
            )
        lines.append("== finished sessions ==")
        for sub_id, rec in self.records.items():
            for sess in rec.stat.sessions:
                if sess.ended_at is not None:
                    lines.append(f"  {sub_id} :: {sess.session_id}")
        lines.append("== running background sessions ==")
        reg = self.background_registry
        for sid, task_id in self._bg_sessions.items():
            if reg is not None and reg.is_running(task_id):
                lines.append(f"  {sid} :: task_id={task_id}")
        return "\n".join(lines)

    def inspect(self, session_id: str) -> str:
        for rec in self.records.values():
            if session_id in rec.harnesses:
                h = rec.harnesses[session_id]
                parts: list[str] = []
                for t in h.turns:
                    if t.role == "system":
                        continue
                    parts.append(f"--- {t.role} ---\n{t.content}")
                return "\n".join(parts)
        raise KeyError(f"session {session_id} not found")
