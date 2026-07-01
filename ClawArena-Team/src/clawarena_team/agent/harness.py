"""AgentHarness: the agent loop shared by the main / sub agents.

Responsibilities:
- Maintain ``messages`` and token accounting. Token accounting uses a
  **local unified tokenizer** decoupled from the provider; the provider's
  raw_usage / usage_normalized are only written to jsonl as a statistics
  source and are **not** used for harness decisions (design-philosophy §3.5).
- On user / tool_result turns, attach system-level hints inside
  ``<system-reminder>`` blocks: Environment, token-budget thresholds,
  background subagent completion results, and usage hints.
- Dispatch ``tool_calls`` (in parallel) and write the results back as
  ``tool_result``.
- At the end of every turn, check the context-usage cap and raise
  ``TokenLimitExceeded`` when it is exceeded.

Token accounting model (each model call = one assistant-turn granule):
- ``context_size_max``: the peak context usage after adding all turns; under
  monotonically increasing context this equals the total length at the end of
  the scenario. **This quantity is compared against ``token_limit`` to decide
  whether to trip the breaker.**
- ``input_token_total``: the accumulated user / tool_result / system-reminder
  content newly pushed into context since the last assistant completion up to
  the current call.
- ``output_token_total``: the accumulated tokens of each assistant turn itself.
- ``cache_read_total``: the sum of tokens already present in context before
  each model call, corresponding to the volume that can hit the prompt cache.

`<system-reminder>` rendering: ``HarnessTurn.system_reminders`` stores the raw
fragments; ``_provider_messages`` appends them to the end of ``content`` during
serialization (each fragment wrapped independently).
"""
from __future__ import annotations

import asyncio
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from ..prompts import (
    BACKGROUND_ERROR_REMINDER,
    BACKGROUND_RESULT_REMINDER,
    STRUCTURED_OUTPUT_INSTRUCTION,
    STRUCTURED_OUTPUT_RETRY,
    STRUCTURED_OUTPUT_TOOL_DESCRIPTION,
    USAGE_HINT_REMINDER,
    USAGE_THRESHOLD_REMINDER,
    wrap_system_reminder,
    wrap_task_notification,
)
from ..provider import BaseProvider
from ..provider.multimodal import (
    MultimodalConfig,
    attachments_to_parts,
    build_followup_user_message,
    estimate_attachment_tokens,
)
from ..sandbox import AccessibleScope, ReadTracker
from ..tokenizer import UnifiedTokenizer
from ..tools import BaseTool
from ..tools.base import ToolContext, ToolExecResult


class TokenLimitExceeded(RuntimeError):
    """This agent's context exceeded the cap."""


_JSON_TYPE_PY = {
    "object": dict,
    "array": list,
    "string": str,
    "number": (int, float),
    "integer": int,
    "boolean": bool,
}


def _validate_against_schema(value: Any, schema: dict[str, Any]) -> tuple[bool, str]:
    """Lightweight JSON-schema validation: top-level type + object's required + one level of property types.

    Does not pull in the jsonschema dependency; only performs checks strong
    enough to reject "obviously non-conforming" payloads back to a retry, and is
    lenient about nested structures.
    """
    stype = schema.get("type") if isinstance(schema, dict) else None
    if stype and stype in _JSON_TYPE_PY:
        py = _JSON_TYPE_PY[stype]
        if stype == "boolean" and isinstance(value, bool):
            pass
        elif stype in ("number", "integer") and isinstance(value, bool):
            return False, f"expected {stype}, got boolean"
        elif not isinstance(value, py):
            return False, f"expected top-level type {stype}, got {type(value).__name__}"
    if stype == "object" or (isinstance(value, dict) and "properties" in schema):
        if not isinstance(value, dict):
            return False, "expected an object"
        required = schema.get("required") or []
        missing = [k for k in required if k not in value]
        if missing:
            return False, f"missing required field(s): {', '.join(missing)}"
        props = schema.get("properties") or {}
        for k, sub in props.items():
            if k in value and isinstance(sub, dict) and sub.get("type") in _JSON_TYPE_PY:
                py = _JSON_TYPE_PY[sub["type"]]
                v = value[k]
                if sub["type"] in ("number", "integer") and isinstance(v, bool):
                    return False, f"field '{k}' expected {sub['type']}, got boolean"
                if not isinstance(v, py):
                    return False, f"field '{k}' expected {sub['type']}, got {type(v).__name__}"
    return True, ""


@dataclass
class HarnessTurn:
    """A single history record, for ease of persistence."""

    role: str  # system / user / assistant / tool_result
    content: str
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    tool_call_id: Optional[str] = None
    # Current total context length after adding this turn (computed by the local
    # tokenizer; includes system + tools schema + history).
    context_size_after: int = 0
    # Assistant turn only: the three segments for this model call (local view, comparable across providers).
    input_delta: int = 0
    output_delta: int = 0
    cache_read_delta: int = 0
    # Assistant turn only: the usage actually returned by the provider.
    provider_usage: dict[str, Any] = field(default_factory=dict)  # raw, original schema passed through
    usage_normalized: dict[str, Any] = field(default_factory=dict)  # UsageRecord.to_dict()
    # The model id actually echoed by the provider (falls back to config.model_id
    # if the response does not carry one). Useful for auditing after the fact
    # whether the actually-billed model matches the request (e.g. anthropic's
    # fable->opus fallback).
    provider_model_id: str = ""
    # An additional dict freely passed through by the provider (arbitrary
    # structure). Currently used to record the fable refusal fallback
    # ``{fable_refusal_fallback, fallback_from_model, fallback_model, note}``.
    provider_extra: dict[str, Any] = field(default_factory=dict)
    timestamp: float = 0.0
    is_real_user_question: bool = False
    # Raw fragments of system-level hints (without the <system-reminder> tag).
    # Wrapped separately when rendered to the provider.
    system_reminders: list[str] = field(default_factory=list)
    # Raw fragments of background-task completion notifications (without the
    # <task-notification> tag). A separate out-of-band channel from
    # system_reminders; wrapped separately when rendered.
    task_notifications: list[str] = field(default_factory=list)
    # Multimodal attachments (path + modality tag). Only tool_result turns are
    # populated: ``_run_loop`` copies them from ``ToolExecResult.attachments``
    # after tool execution. ``_provider_messages`` uses them to append a
    # synthesized user message after this turn (approach C, see
    # ``/tmp/mm_wire.md``); ``_render_messages_for_count`` uses them to count the
    # 280/2240/750-magnitude mm tokens into the local context view.
    attachments: list[tuple[str, str]] = field(default_factory=list)


@dataclass
class HarnessConfig:
    token_limit: int
    usage_thresholds_pct: list[int]
    always_hint_on_real_user: bool
    max_iterations: int


def _render_content(turn: HarnessTurn) -> str:
    """Concatenate turn.content with system_reminders / task_notifications into the text sent to the provider."""
    if not turn.system_reminders and not turn.task_notifications:
        return turn.content
    parts = [turn.content] if turn.content else []
    parts.extend(wrap_system_reminder(r) for r in turn.system_reminders)
    parts.extend(wrap_task_notification(n) for n in turn.task_notifications)
    return "\n\n".join(p for p in parts if p)


class AgentHarness:
    def __init__(
        self,
        *,
        agent_id: str,
        system_prompt: str,
        provider: BaseProvider,
        tools: dict[str, BaseTool],
        tool_schemas: list[dict[str, Any]],
        scope: AccessibleScope,
        read_tracker: ReadTracker,
        cwd: Path,
        tokenizer: UnifiedTokenizer,
        cfg: HarnessConfig,
        config_dict: dict[str, Any],
        agent_modalities: list[str] | None = None,
        modality_limits: dict[str, int] | None = None,
        subagent_manager: Any | None = None,
    ):
        self.agent_id = agent_id
        self.system_prompt = system_prompt
        self.provider = provider
        self.tools = tools
        self.tool_schemas = tool_schemas
        self.scope = scope
        self.read_tracker = read_tracker
        self.cwd = cwd
        self.tokenizer = tokenizer
        self.cfg = cfg
        self.config_dict = config_dict
        self.agent_modalities = list(agent_modalities or ["text"])
        # Per-modality context attachment cap (image/video/audio); when exceeded,
        # strip the oldest and keep the most recent N.
        self.modality_limits = dict(modality_limits or {})
        # Files already notified via system-reminder about being "stripped",
        # to avoid repeating the reminder every round.
        self._media_elided_notified: set[str] = set()
        self.subagent_manager = subagent_manager
        # Multimodal config: the harness builds it once and passes it to the tool
        # ctx and the wire-construction layer.
        self._mm_cfg = MultimodalConfig.from_dict(config_dict.get("multimodal", {}))

        self.turns: list[HarnessTurn] = []
        # Raw system-reminder fragments pending injection onto the next user / tool_result turn.
        self.pending_system_reminders: list[str] = []
        # Raw task-notification fragments pending injection (background task completion).
        self.pending_task_notifications: list[str] = []
        # Unified background-task registry. Only the main agent is assigned one by
        # scenario_runner after construction; the subagent harness keeps None (its
        # Bash background calls degrade to synchronous execution).
        self.background: Any | None = None
        # Workflow script backup directory (main agent; assigned by scenario_runner after construction).
        self.workflow_script_dir: Any | None = None
        self.modality_counter: dict[str, int] = {}
        self.tools_used: set[str] = set()
        # Bash invocation-mode counts: {"runtime": n, "background": m} (a statistics item alongside the five agent-invocation classes).
        self.bash_mode_counter: dict[str, int] = {}
        # ----- New token accounting (context_size_max is what is compared against token_limit) -----
        self.context_size_max: int = 0
        self.input_token_total: int = 0
        self.output_token_total: int = 0
        self.cache_read_total: int = 0
        # Internal tracking: the context size computed by the last
        # _check_token_budget; and the context size after the last assistant turn
        # was added (= the cache-read volume of the next call).
        self._last_context_size: int = 0
        self._last_post_assistant_size: int = 0
        self._crossed_thresholds: set[int] = set()
        self.turns.append(HarnessTurn(role="system", content=system_prompt, timestamp=time.time()))

    # ------------------------------------------------------------------
    # System-reminder injection API
    # ------------------------------------------------------------------

    def queue_system_reminder(self, body: str) -> None:
        """Attach a system-level hint to the next outgoing turn (user or tool_result)."""
        self.pending_system_reminders.append(body.strip())

    def queue_task_notification(self, body: str) -> None:
        """Attach a background-task completion notification to the next outgoing turn (via <task-notification>)."""
        self.pending_task_notifications.append(body.strip())

    # Backward-compatible alias (background-task completion callback). Background completion now uniformly goes through task-notification.
    def inject_background_user(self, body: str) -> None:
        self.queue_task_notification(body)

    def has_pending_outgoing(self) -> bool:
        return bool(self.pending_system_reminders or self.pending_task_notifications)

    def _flush_pending_onto(self, turn: HarnessTurn) -> None:
        if self.pending_system_reminders:
            turn.system_reminders.extend(self.pending_system_reminders)
            self.pending_system_reminders.clear()
        if self.pending_task_notifications:
            turn.task_notifications.extend(self.pending_task_notifications)
            self.pending_task_notifications.clear()

    # ------------------------------------------------------------------
    # Token accounting
    # ------------------------------------------------------------------

    def _render_messages_for_count(self) -> list[dict[str, Any]]:
        """Build the flat message list used for token counting (includes the serialized tool schema string)."""
        msgs: list[dict[str, Any]] = []
        for t in self.turns:
            content = _render_content(t)
            if t.tool_calls:
                content += "\n" + json.dumps(t.tool_calls)
            msgs.append({"role": t.role, "content": content})
        if self.tool_schemas:
            msgs.append({"role": "system", "content": json.dumps(self.tool_schemas)})
        return msgs

    def _multimodal_token_overhead(self) -> int:
        """The fixed context increment from image/audio/video attachments carried by tool_result.

        The local tokenizer only counts the one ASCII summary line of the
        attachment and cannot see the mm tokens actually consumed by the base64
        binary; here we accumulate conservatively per the ``self._mm_cfg`` anchors
        (default corresponding to the Gemma-4 processor config), so the local view
        uses the same yardstick as the provider's actual billing. video is
        precisely computed via cv2 frame count, audio WAV via stdlib wave duration.
        """
        total = 0
        for t in self.turns:
            if not t.attachments:
                continue
            for raw_path, modality in t.attachments:
                if modality not in self.agent_modalities:
                    continue
                if modality not in {"image", "audio", "video"}:
                    continue
                total += estimate_attachment_tokens(Path(raw_path), modality, self._mm_cfg)
        return total

    def _count_prompt_tokens(self) -> int:
        try:
            base = self.tokenizer.count_messages(self._render_messages_for_count())
        except Exception:
            text = json.dumps([t.content for t in self.turns])
            base = max(1, len(text) // 4)
        return base + self._multimodal_token_overhead()

    def _check_token_budget(self, after_role: str) -> None:
        """After adding a turn, update the counts and, as appropriate, trip the breaker / inject a threshold reminder.

        - ``context_size_max`` takes the rolling maximum of ``cur``; **this is the
          yardstick compared against ``token_limit``**: as soon as
          ``cur > token_limit`` it immediately raises ``TokenLimitExceeded``,
          aligned with claude-code's "context is full" semantics.
        - When ``after_role == "assistant"``, it simultaneously computes and
          accumulates the three segments (input/output/cache_read); it also writes
          the deltas onto the assistant turn just appended to ``self.turns``.
        """
        cur = self._count_prompt_tokens()
        self.context_size_max = max(self.context_size_max, cur)
        if self.turns:
            self.turns[-1].context_size_after = cur

        if after_role == "assistant" and self.turns:
            last = self.turns[-1]
            pre_call = self._last_context_size       # total context length before adding assistant
            post_call = cur                           # total context length after adding assistant
            prev_post_assist = self._last_post_assistant_size
            input_delta = max(0, pre_call - prev_post_assist)
            output_delta = max(0, post_call - pre_call)
            cache_read = prev_post_assist
            last.input_delta = input_delta
            last.output_delta = output_delta
            last.cache_read_delta = cache_read
            self.input_token_total += input_delta
            self.output_token_total += output_delta
            self.cache_read_total += cache_read
            self._last_post_assistant_size = post_call

        self._last_context_size = cur

        if cur > self.cfg.token_limit:
            raise TokenLimitExceeded(
                f"agent {self.agent_id} exceeded token limit {self.cfg.token_limit} (cur={cur})"
            )
        pct = int(cur * 100 / max(1, self.cfg.token_limit))
        for thr in self.cfg.usage_thresholds_pct:
            if pct >= thr and thr not in self._crossed_thresholds:
                self._crossed_thresholds.add(thr)
                reminder = USAGE_THRESHOLD_REMINDER.format(
                    pct=thr, used=cur, limit=self.cfg.token_limit
                )
                if after_role == "tool_result" and self.turns and self.turns[-1].role == "tool_result":
                    self.turns[-1].system_reminders.append(reminder)
                else:
                    self.queue_system_reminder(reminder)

    # ------------------------------------------------------------------
    # Public: send a user turn (real question or injection)
    # ------------------------------------------------------------------

    async def send_user(
        self, text: str, *, is_real_question: bool, schema: dict | None = None
    ) -> Any:
        """Add a user turn and run the agent loop until an assistant answer with no tool_call.

        When ``schema`` is non-empty, enter structured-output mode: inject the
        ``StructuredOutput`` tool and require the agent to return its result via
        that call; returns a validated Python object (rather than text). On
        validation failure it retries up to ``structured_output.max_retries``,
        and if it still fails it falls back to returning text.
        """
        if schema is not None:
            text = text.rstrip() + "\n\n" + STRUCTURED_OUTPUT_INSTRUCTION
        turn = HarnessTurn(
            role="user",
            content=text,
            timestamp=time.time(),
            is_real_user_question=is_real_question,
        )
        self._flush_pending_onto(turn)
        if is_real_question and self.cfg.always_hint_on_real_user:
            cur = self._count_prompt_tokens()
            turn.system_reminders.append(
                USAGE_HINT_REMINDER.format(
                    used=cur,
                    limit=self.cfg.token_limit,
                    pct=cur * 100 / max(1, self.cfg.token_limit),
                )
            )
        self.turns.append(turn)
        self._check_token_budget("user")
        if schema is not None:
            return await self._run_loop_structured(schema)
        return await self._run_loop()

    # ------------------------------------------------------------------
    # Agent loop
    # ------------------------------------------------------------------

    _MM_MODALITIES = ("image", "audio", "video")

    def _media_elision(self) -> tuple[dict[int, set[int]], list[tuple[str, str]]]:
        """Compute, per per-modality context cap, the attachments to strip (keep the most recent N, strip the oldest).

        Aligned with mainstream harnesses (claude-code ``stripExcessMediaItems``:
        strip oldest first, preserve most recent), but enforced per the
        per-modality cap. Returns:
          - ``elided``: ``{turn_index: {attachment_index, ...}}`` -- attachments to exclude from the followup;
          - ``dropped``: ``[(path, modality), ...]`` -- the stripped files (for system-reminder).
        """
        per_modality: dict[str, list[tuple[int, int, str]]] = {}
        for ti, t in enumerate(self.turns):
            for ai, (path, modality) in enumerate(t.attachments or []):
                if modality not in self.agent_modalities or modality not in self._MM_MODALITIES:
                    continue
                per_modality.setdefault(modality, []).append((ti, ai, path))
        elided: dict[int, set[int]] = {}
        dropped: list[tuple[str, str]] = []
        for modality, items in per_modality.items():
            limit = self.modality_limits.get(modality)
            if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
                continue  # with no valid cap, do not strip (the probe already enforces declaration; this is defensive)
            excess = len(items) - limit
            for ti, ai, path in items[:max(0, excess)]:  # the oldest `excess` in appearance order
                elided.setdefault(ti, set()).add(ai)
                dropped.append((path, modality))
        return elided, dropped

    def _provider_messages(self) -> list[dict[str, Any]]:
        elided, _ = self._media_elision()
        msgs: list[dict[str, Any]] = []
        for ti, t in enumerate(self.turns):
            rendered = _render_content(t)
            if t.role == "system":
                msgs.append({"role": "system", "content": rendered})
            elif t.role == "user":
                msgs.append({"role": "user", "content": rendered})
            elif t.role == "assistant":
                m: dict[str, Any] = {"role": "assistant", "content": rendered}
                if t.tool_calls:
                    m["tool_calls"] = [
                        {
                            "id": tc["id"],
                            "type": "function",
                            "function": {
                                "name": tc["name"],
                                "arguments": json.dumps(tc["arguments"]),
                            },
                        }
                        for tc in t.tool_calls
                    ]
                msgs.append(m)
            elif t.role == "tool_result":
                msgs.append(
                    {
                        "role": "tool",
                        "tool_call_id": t.tool_call_id or "",
                        "content": rendered,
                    }
                )
                followup = self._build_mm_followup(t, elided.get(ti, frozenset()))
                if followup is not None:
                    msgs.append(followup)
        return msgs

    def _build_mm_followup(
        self,
        turn: "HarnessTurn",
        elide_indices: "frozenset[int] | set[int]" = frozenset(),
    ) -> dict[str, Any] | None:
        """Approach C: if there are image/audio/video attachments after a tool_result, append a user message carrying base64 parts.

        ``elide_indices`` gives the indices of attachments in this turn that were
        stripped for exceeding the context cap (keep most recent, strip oldest);
        these are excluded from the sent content. Filtering, size limits, mp4 path
        branching, etc. are handled centrally by
        ``provider.multimodal.attachments_to_parts`` (see its docstring).
        """
        if not turn.attachments:
            return None
        kept = [a for i, a in enumerate(turn.attachments) if i not in elide_indices]
        if not kept:
            return None
        parts, paths = attachments_to_parts(
            kept,
            agent_modalities=self.agent_modalities,
            cfg=self._mm_cfg,
        )
        if not parts:
            return None
        note = (
            f"<system>Attachment(s) for the prior Read of {', '.join(paths)}; "
            f"respond as if you had seen the file directly.</system>"
        )
        return build_followup_user_message(parts=parts, note_text=note)

    async def _run_loop(self) -> str:
        for _ in range(self.cfg.max_iterations):
            resp = await self.provider.chat(
                messages=self._provider_messages(),
                tools=self.tool_schemas,
            )
            content = resp.get("content", "") or ""
            tool_calls = resp.get("tool_calls") or []
            provider_usage = resp.get("raw_usage") or {}
            usage_normalized = resp.get("usage_normalized") or {}
            provider_model_id = resp.get("model_id") or ""
            provider_extra = resp.get("extra") or {}

            self.turns.append(
                HarnessTurn(
                    role="assistant",
                    content=content,
                    tool_calls=tool_calls,
                    provider_usage=provider_usage,
                    usage_normalized=usage_normalized,
                    provider_model_id=provider_model_id,
                    provider_extra=provider_extra,
                    timestamp=time.time(),
                )
            )
            self._check_token_budget("assistant")

            if not tool_calls:
                # If there are still pending system-reminders / task-notifications
                # (e.g. a background task completes only on the loop's last step),
                # inject them as a standalone user turn and continue the loop once
                # more, so the agent has a chance to react to the background-task
                # result.
                if self.has_pending_outgoing():
                    bridge = HarnessTurn(role="user", content="", timestamp=time.time())
                    self._flush_pending_onto(bridge)
                    self.turns.append(bridge)
                    self._check_token_budget("user")
                    continue
                return content

            ctx_factory = self._make_tool_context
            tasks = [self._exec_tool(tc, ctx_factory) for tc in tool_calls]
            results = await asyncio.gather(*tasks)
            for tc, res in zip(tool_calls, results):
                tr = HarnessTurn(
                    role="tool_result",
                    content=res.content,
                    tool_call_id=tc.get("id", ""),
                    timestamp=time.time(),
                    attachments=list(res.attachments),
                )
                self.turns.append(tr)
            # Multimodal context cap: after stripping the oldest attachments,
            # notify once (deduplicated) about the **newly** stripped files, so the
            # agent knows which multimodal files have been moved out of context and
            # can Read them again as needed.
            _, dropped = self._media_elision()
            new_dropped = [(p, m) for p, m in dropped if p not in self._media_elided_notified]
            if new_dropped:
                by_mod: dict[str, list[str]] = {}
                for p, m in new_dropped:
                    self._media_elided_notified.add(p)
                    by_mod.setdefault(m, []).append(Path(p).name)
                limit_str = ", ".join(f"{m}={self.modality_limits.get(m)}" for m in sorted(by_mod))
                files_str = "; ".join(
                    f"{m}: {', '.join(names)}" for m, names in sorted(by_mod.items())
                )
                self.queue_system_reminder(
                    f"Multimodal context limit reached ({limit_str}). To stay within the "
                    f"per-modality budget, the OLDEST attachments were dropped from context "
                    f"and are no longer visible: {files_str}. If you still need one, Read it "
                    f"again to bring it back as the most recent attachment."
                )
            # Attach the background completions (task-notification) / system-reminders
            # that arrived during tool execution onto the last tool_result.
            if self.has_pending_outgoing() and self.turns and self.turns[-1].role == "tool_result":
                self._flush_pending_onto(self.turns[-1])
            self._check_token_budget("tool_result")

        # Fix (audit-top10 #7 / W1F2, resolved): when max_iterations is exhausted
        # the last round is usually a tool_result, and the original implementation
        # returned the tool echo as the agent answer -- for a subagent consuming
        # the return string (_run_session) this treated a stray tool output as the
        # answer. Changed to return an explicit truncation marker so the
        # caller/session log can recognize "not finished answering" at a glance.
        # Note: the original patch also set a self.truncated flag, but nobody in
        # the whole repo reads it (the main agent's return string is discarded by
        # scenario_runner anyway, and scoring goes through exec_check), making it a
        # "set but unused" dead state; removed in the same spirit as W1F3.
        return "[TRUNCATED] max_iterations reached without final answer"

    # ------------------------------------------------------------------
    # Structured-output loop (inject the StructuredOutput tool, force the result to be returned via it)
    # ------------------------------------------------------------------
    def _structured_tool_schema(self, schema: dict[str, Any]) -> dict[str, Any]:
        params = schema if isinstance(schema, dict) and schema.get("type") else {
            "type": "object",
            "properties": schema if isinstance(schema, dict) else {},
        }
        return {
            "name": "StructuredOutput",
            "description": STRUCTURED_OUTPUT_TOOL_DESCRIPTION,
            "parameters": params,
        }

    async def _run_loop_structured(self, schema: dict[str, Any]) -> Any:
        so_schema = self._structured_tool_schema(schema)
        all_tools = list(self.tool_schemas) + [so_schema]
        max_retries = int(
            self.config_dict.get("structured_output", {}).get("max_retries", 2)
        )
        retries_left = max_retries
        last_text = ""
        for _ in range(self.cfg.max_iterations):
            resp = await self.provider.chat(messages=self._provider_messages(), tools=all_tools)
            content = resp.get("content", "") or ""
            tool_calls = resp.get("tool_calls") or []
            last_text = content or last_text
            self.turns.append(
                HarnessTurn(
                    role="assistant",
                    content=content,
                    tool_calls=tool_calls,
                    provider_usage=resp.get("raw_usage") or {},
                    usage_normalized=resp.get("usage_normalized") or {},
                    provider_model_id=resp.get("model_id") or "",
                    provider_extra=resp.get("extra") or {},
                    timestamp=time.time(),
                )
            )
            self._check_token_budget("assistant")

            if not tool_calls:
                if self.has_pending_outgoing():
                    bridge = HarnessTurn(role="user", content="", timestamp=time.time())
                    self._flush_pending_onto(bridge)
                    self.turns.append(bridge)
                    self._check_token_budget("user")
                    continue
                if retries_left > 0:
                    retries_left -= 1
                    nudge = HarnessTurn(
                        role="user", content=STRUCTURED_OUTPUT_RETRY, timestamp=time.time()
                    )
                    self.turns.append(nudge)
                    self._check_token_budget("user")
                    continue
                # Retries exhausted: fall back to returning plain text (the caller can use this to judge structured-output failure).
                return last_text

            # Handle StructuredOutput first (terminal); the remaining basic tools execute as usual.
            so_call = next((tc for tc in tool_calls if tc.get("name") == "StructuredOutput"), None)
            if so_call is not None:
                payload = so_call.get("arguments") or {}
                ok, err = _validate_against_schema(payload, schema)
                if ok:
                    self.turns.append(
                        HarnessTurn(
                            role="tool_result",
                            content="structured output accepted",
                            tool_call_id=so_call.get("id", ""),
                            timestamp=time.time(),
                        )
                    )
                    self._check_token_budget("tool_result")
                    return payload
                # Validation failed -> feed back the error so it retries within the same loop.
                self.turns.append(
                    HarnessTurn(
                        role="tool_result",
                        content=f"StructuredOutput rejected: {err}. Fix the arguments and call it again.",
                        tool_call_id=so_call.get("id", ""),
                        timestamp=time.time(),
                    )
                )
                self._check_token_budget("tool_result")
                continue

            ctx_factory = self._make_tool_context
            tasks = [self._exec_tool(tc, ctx_factory) for tc in tool_calls]
            results = await asyncio.gather(*tasks)
            for tc, res in zip(tool_calls, results):
                self.turns.append(
                    HarnessTurn(
                        role="tool_result",
                        content=res.content,
                        tool_call_id=tc.get("id", ""),
                        timestamp=time.time(),
                        attachments=list(res.attachments),
                    )
                )
            if self.has_pending_outgoing() and self.turns and self.turns[-1].role == "tool_result":
                self._flush_pending_onto(self.turns[-1])
            self._check_token_budget("tool_result")

        return last_text

    def _make_tool_context(self) -> ToolContext:
        return ToolContext(
            agent_id=self.agent_id,
            scope=self.scope,
            read_tracker=self.read_tracker,
            cwd=self.cwd,
            config={
                "bash.default_timeout_ms": self.config_dict.get("bash", {}).get("default_timeout_ms", 120000),
                "bash.max_output_bytes": self.config_dict.get("bash", {}).get("max_output_bytes", 65536),
                "grep.context_lines": self.config_dict.get("grep", {}).get("context_lines", 0),
                "grep.default_max_results": self.config_dict.get("grep", {}).get("default_max_results", 200),
                "read.max_text_bytes": self.config_dict.get("read", {}).get("max_text_bytes", 524288),
                "read.notice_bytes": self.config_dict.get("read", {}).get("notice_bytes", 32768),
                "read.hard_bytes": self.config_dict.get("read", {}).get("hard_bytes", 262144),
                # ReadTool uses this value to decide "whether an attachment is too
                # large to deliver as binary" -- the authoritative source is the
                # ``multimodal:`` section; here the harness passes the
                # strongly-typed cfg field through to ReadTool as a dotted scalar.
                "multimodal.attachment_max_bytes": self._mm_cfg.attachment_max_bytes,
                "workflow.max_agents": self.config_dict.get("workflow", {}).get("max_agents", 1000),
                "workflow.max_concurrency": self.config_dict.get("workflow", {}).get("max_concurrency", 8),
                "structured_output.runsubagent_enabled": self.config_dict.get(
                    "structured_output", {}
                ).get("runsubagent_enabled", False),
            },
            subagent_manager=self.subagent_manager,
            background=self.background,
            workflow_script_dir=self.workflow_script_dir,
            modality_counter=self.modality_counter,
            tools_used=self.tools_used,
            bash_mode_counter=self.bash_mode_counter,
            agent_modalities=list(self.agent_modalities),
        )

    async def _exec_tool(self, tc: dict[str, Any], ctx_factory) -> ToolExecResult:
        name = tc.get("name", "")
        tool = self.tools.get(name)
        if tool is None:
            return ToolExecResult(f"unknown tool: {name}", is_error=True)
        try:
            return await tool.run(tc.get("arguments") or {}, ctx_factory())
        except Exception as e:  # noqa: BLE001
            return ToolExecResult(f"tool {name} raised: {e}", is_error=True)
