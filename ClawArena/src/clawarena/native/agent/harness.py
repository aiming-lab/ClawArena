"""AgentHarness：ArcBench v1 单 agent loop，跨整个 benchmark。

要点：

1. **不在内存中维护 turns**：所有消息 append 到 :class:`SessionLog`；每次组装 provider
   messages 都从 jsonl 重读 + 应用最后一条 compact boundary 做切片，并把所有
   microcompact boundary 的 redactions 重放到旧 tool_result 上。
2. **语义边界缓压（B1）**：触发区间 ``[trigger_tokens, force_tokens)`` 内仅在自然
   边界（assistant 刚返回 final answer / real-user 输入之前）触发 compact；强制阈
   值 ``force_tokens`` 之上无视位置直接压。
3. **system-reminder 通道**：``queue_system_reminder`` 把待注入文本挂到下一个对外
   turn（user / tool_result 邻接的 bridge user）末尾，transcript 渲染时拼为
   ``<system-reminder>...</system-reminder>``。

agent loop 终止条件：assistant 给出无 tool_call 的 answer。
"""
from __future__ import annotations

import asyncio
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from ..prompts import (
    COMPACTION_SUMMARY_WRAPPER,
    MEMORY_PERSIST_REMINDER,
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
from .compaction import Compactor, Microcompactor
from .messages import (
    AssistantMessage,
    CompactBoundaryMessage,
    Message,
    MicrocompactBoundaryMessage,
    SystemMessage,
    ToolResultMessage,
    UserMessage,
    apply_microcompact_redactions,
    messages_after_last_compact,
)
from .session_log import SessionLog


@dataclass
class HarnessConfig:
    token_limit: int
    usage_thresholds_pct: list[int]
    always_hint_on_real_user: bool
    max_iterations: int
    memory_notification_enabled: bool = True
    # 触发"记忆写入提醒"的用量阈值（须为 usage_thresholds_pct 的子集）。空 → 不提醒。
    memory_persist_thresholds: list[int] = field(default_factory=list)


_JSON_TYPE_PY: dict[str, Any] = {
    "object": dict,
    "array": list,
    "string": str,
    "number": (int, float),
    "integer": int,
    "boolean": bool,
}


def _validate_against_schema(value: Any, schema: dict[str, Any]) -> tuple[bool, str]:
    """轻量 JSON-schema 校验：顶层类型 + object 的 required + 一层 property 类型。

    不引入 jsonschema 依赖；只做足够把"明显不符"挡回去重试的检查，对嵌套结构宽松。
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


class AgentHarness:
    """ArcBench v1 main agent harness。"""

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
        session_log: SessionLog,
        compactor: Optional[Compactor] = None,
        microcompactor: Optional[Microcompactor] = None,
        agent_modalities: Optional[list[str]] = None,
        subagent_manager: Optional[Any] = None,
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
        self.session_log = session_log
        self.compactor = compactor
        self.microcompactor = microcompactor
        self.agent_modalities = list(agent_modalities or ["text"])
        self.subagent_manager = subagent_manager
        # multimodal 配置：harness 一次性 build，传给 tool ctx 与 wire 构造层。
        self._mm_cfg = MultimodalConfig.from_dict(config_dict.get("multimodal", {}))

        # 系统级状态
        self.pending_system_reminders: list[str] = []
        # 待注入的 task-notification 原文片段（背景任务完成）。
        self.pending_task_notifications: list[str] = []
        # 统一后台任务注册表 + Workflow 脚本备份目录。仅 main agent 由 engine 在构造后
        # 赋值；subagent harness 保持 None（其内不能跑 Workflow / 后台任务）。
        self.background: Any | None = None
        self.workflow_script_dir: Any | None = None
        # 跨 session 历史读取器（SessionHistoryStore）。仅 main agent 由 engine 赋值。
        self.session_history: Any | None = None
        self.modality_counter: dict[str, int] = {}
        self.tools_used: set[str] = set()
        self.context_size_max: int = 0
        self.input_token_total: int = 0
        self.output_token_total: int = 0
        self.cache_read_total: int = 0
        self._crossed_thresholds: set[int] = set()
        self._last_post_assistant_size: int = 0
        self._turn_index: int = 0

        # 写入 system prompt 作为 session 第一条
        if not list(self.session_log.iter_raw()):
            self.session_log.append(SystemMessage(content=system_prompt, subtype="prompt"))

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def queue_system_reminder(self, body: str) -> None:
        """把一段系统级提示挂到下一个对外 turn（user / tool_result）。"""
        self.pending_system_reminders.append(body.strip())

    def queue_task_notification(self, body: str) -> None:
        """把一段背景任务完成通知挂到下一个对外 turn（走 <task-notification>）。"""
        self.pending_task_notifications.append(body.strip())

    # 背景任务（Workflow / background subagent）完成回调统一入口。
    def inject_background_user(self, body: str) -> None:
        self.queue_task_notification(body)

    def _has_pending_outgoing(self) -> bool:
        return bool(self.pending_system_reminders or self.pending_task_notifications)

    def _make_bridge_user(self) -> UserMessage:
        """把所有挂起的 system-reminder / task-notification 排到一条合成 user turn 上。"""
        bridge = UserMessage(
            content="",
            system_reminders=list(self.pending_system_reminders),
            task_notifications=list(self.pending_task_notifications),
        )
        self.pending_system_reminders.clear()
        self.pending_task_notifications.clear()
        return bridge

    async def send_user(
        self,
        text: str,
        *,
        is_real_question: bool,
        meta: Optional[dict[str, Any]] = None,
        schema: Optional[dict[str, Any]] = None,
    ) -> Any:
        """添加一个 user turn 并跑 agent loop 至 assistant 给出无 tool_call 的 answer。

        ``schema`` 非空时进入结构化输出模式：注入 ``StructuredOutput`` 工具并要求 agent
        以其调用返回结果；返回经校验的 Python 对象（而非文本）。校验/调用失败按
        ``structured_output.max_retries`` 重试，仍失败则回退返回文本。
        """
        # B1 自然边界：在 append 新 user 之前先检查是否要 compact（"real-user 输入
        # 之前"是合法触发位）。
        await self._maybe_compact(at_boundary=True)

        if schema is not None:
            text = text.rstrip() + "\n\n" + STRUCTURED_OUTPUT_INSTRUCTION

        reminders = list(self.pending_system_reminders)
        self.pending_system_reminders.clear()
        notifications = list(self.pending_task_notifications)
        self.pending_task_notifications.clear()
        if is_real_question and self.cfg.always_hint_on_real_user:
            cur = self._count_context()
            reminders.append(
                USAGE_HINT_REMINDER.format(
                    used=cur,
                    limit=self.cfg.token_limit,
                    pct=cur * 100 / max(1, self.cfg.token_limit),
                )
            )
        user_msg = UserMessage(
            content=text,
            is_real_user_question=is_real_question,
            system_reminders=reminders,
            task_notifications=notifications,
            meta=dict(meta or {}),
        )
        self.session_log.append(user_msg)
        self._turn_index += 1
        if schema is not None:
            return await self._run_loop_structured(schema)
        return await self._run_loop()

    async def request_arc_selection(self, menu_reminder: str) -> str:
        """agent_choice 选弧：把候选菜单作为 system_reminder 挂在一个合成 user turn 上，
        跑 agent loop，返回 agent 的回复文本供 session_runner 解析 ``CHOICE: <n>``。

        这是"当前弧结束被迫选下一步"，而非 agent 自发调用工具——故走 reminder 通道、
        ``is_real_question=False``（不追加用量提示）。"""
        self.queue_system_reminder(menu_reminder)
        return await self.send_user(
            "", is_real_question=False, meta={"kind": "arc_selection"}
        )

    # ------------------------------------------------------------------
    # Agent loop
    # ------------------------------------------------------------------

    async def _run_loop(self) -> str:
        for _ in range(self.cfg.max_iterations):
            provider_messages = self._build_provider_messages()
            pre_call_ctx = self._count_context()
            resp = await self.provider.chat(
                messages=provider_messages,
                tools=self.tool_schemas,
            )
            content = resp.get("content", "") or ""
            tool_calls = resp.get("tool_calls") or []
            provider_usage = resp.get("raw_usage") or {}
            usage_normalized = resp.get("usage_normalized") or {}

            assistant_msg = AssistantMessage(
                content=content,
                tool_calls=tool_calls,
                provider_usage=provider_usage,
                usage_normalized=usage_normalized,
            )
            self.session_log.append(assistant_msg)
            self._turn_index += 1
            self._record_usage_after_assistant(pre_call_ctx)
            self._check_usage_thresholds()

            if not tool_calls:
                # final answer：自然边界。先把仍在跑的后台任务（Workflow / background
                # subagent）等完——其完成通知经 inject_background_user 排入 pending；
                # 若由此产生待注入内容，则补一条 bridge user 并继续 loop 一次，让 agent
                # 有机会对背景任务结果作出反应。
                if self.background is not None and self.background.any_running():
                    await self.background.wait_all()
                if self._has_pending_outgoing():
                    self.session_log.append(self._make_bridge_user())
                    self._turn_index += 1
                    self._check_usage_thresholds()
                    await self._maybe_compact(at_boundary=True)
                    continue
                await self._maybe_compact(at_boundary=True)
                return content

            # mid-loop：执行 tool_calls。**不在此处触发 soft compact**，避免把
            # assistant(tool_call) 与对应 tool_result 切到 boundary 两侧。
            tasks = [self._exec_tool(tc) for tc in tool_calls]
            results = await asyncio.gather(*tasks)
            for tc, res in zip(tool_calls, results):
                name = tc.get("name", "")
                tr_meta: dict[str, Any] = {"tool": name}
                # 把首个 attachment 的路径挂到 meta["path"]，供 microcompact /
                # post-compact reinjection 识别"被 Read 的文件"。
                if res.attachments:
                    tr_meta["path"] = res.attachments[0][0]
                tr = ToolResultMessage(
                    content=res.content,
                    tool_call_id=tc.get("id", ""),
                    is_error=res.is_error,
                    attachments=[(a, m) for a, m in res.attachments],
                    meta=tr_meta,
                )
                self.session_log.append(tr)
                self._turn_index += 1
            if self._has_pending_outgoing():
                self.session_log.append(self._make_bridge_user())
                self._turn_index += 1
            self._check_usage_thresholds()
            # mid-loop：先尝试 microcompact 削旧 tool_result；如仍越过 force_pct
            # 则强制 compact（B1 兜底）。
            await self._maybe_microcompact()
            await self._maybe_compact(at_boundary=False)
        return ""

    # ------------------------------------------------------------------
    # Structured-output loop（注入 StructuredOutput 工具，强制以其返回结果）
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
            provider_messages = self._build_provider_messages()
            pre_call_ctx = self._count_context()
            resp = await self.provider.chat(messages=provider_messages, tools=all_tools)
            content = resp.get("content", "") or ""
            tool_calls = resp.get("tool_calls") or []
            last_text = content or last_text

            self.session_log.append(
                AssistantMessage(
                    content=content,
                    tool_calls=tool_calls,
                    provider_usage=resp.get("raw_usage") or {},
                    usage_normalized=resp.get("usage_normalized") or {},
                )
            )
            self._turn_index += 1
            self._record_usage_after_assistant(pre_call_ctx)
            self._check_usage_thresholds()

            if not tool_calls:
                if self.background is not None and self.background.any_running():
                    await self.background.wait_all()
                if self._has_pending_outgoing():
                    self.session_log.append(self._make_bridge_user())
                    self._turn_index += 1
                    self._check_usage_thresholds()
                    continue
                if retries_left > 0:
                    retries_left -= 1
                    self.session_log.append(UserMessage(content=STRUCTURED_OUTPUT_RETRY))
                    self._turn_index += 1
                    self._check_usage_thresholds()
                    continue
                # 重试耗尽：回退返回纯文本（调用方可据此判定结构化失败）。
                return last_text

            # 先处理 StructuredOutput（终结），其余基础工具照常执行。
            so_call = next(
                (tc for tc in tool_calls if tc.get("name") == "StructuredOutput"), None
            )
            if so_call is not None:
                payload = so_call.get("arguments") or {}
                ok, err = _validate_against_schema(payload, schema)
                if ok:
                    self.session_log.append(
                        ToolResultMessage(
                            content="structured output accepted",
                            tool_call_id=so_call.get("id", ""),
                            meta={"tool": "StructuredOutput"},
                        )
                    )
                    self._turn_index += 1
                    self._check_usage_thresholds()
                    return payload
                self.session_log.append(
                    ToolResultMessage(
                        content=f"StructuredOutput rejected: {err}. Fix the arguments and call it again.",
                        tool_call_id=so_call.get("id", ""),
                        is_error=True,
                        meta={"tool": "StructuredOutput"},
                    )
                )
                self._turn_index += 1
                self._check_usage_thresholds()
                continue

            tasks = [self._exec_tool(tc) for tc in tool_calls]
            results = await asyncio.gather(*tasks)
            for tc, res in zip(tool_calls, results):
                name = tc.get("name", "")
                tr_meta: dict[str, Any] = {"tool": name}
                if res.attachments:
                    tr_meta["path"] = res.attachments[0][0]
                self.session_log.append(
                    ToolResultMessage(
                        content=res.content,
                        tool_call_id=tc.get("id", ""),
                        is_error=res.is_error,
                        attachments=[(a, m) for a, m in res.attachments],
                        meta=tr_meta,
                    )
                )
                self._turn_index += 1
            if self._has_pending_outgoing():
                self.session_log.append(self._make_bridge_user())
                self._turn_index += 1
            self._check_usage_thresholds()
            await self._maybe_microcompact()
            await self._maybe_compact(at_boundary=False)
        return last_text

    # ------------------------------------------------------------------
    # Compaction / token accounting
    # ------------------------------------------------------------------

    def _record_usage_after_assistant(self, pre_call_ctx: int) -> None:
        cur = self._count_context()
        self.context_size_max = max(self.context_size_max, cur)
        input_delta = max(0, pre_call_ctx - self._last_post_assistant_size)
        output_delta = max(0, cur - pre_call_ctx)
        self.input_token_total += input_delta
        self.output_token_total += output_delta
        self.cache_read_total += self._last_post_assistant_size
        self._last_post_assistant_size = cur

    def _check_usage_thresholds(self) -> None:
        cur = self._count_context()
        self.context_size_max = max(self.context_size_max, cur)
        pct = int(cur * 100 / max(1, self.cfg.token_limit))
        for thr in self.cfg.usage_thresholds_pct:
            if pct >= thr and thr not in self._crossed_thresholds:
                self._crossed_thresholds.add(thr)
                self.queue_system_reminder(
                    USAGE_THRESHOLD_REMINDER.format(
                        pct=thr, used=cur, limit=self.cfg.token_limit
                    )
                )
                # 记忆写入提醒紧跟用量提醒之后（仅在配置的高阈值处）。
                if (
                    self.cfg.memory_notification_enabled
                    and thr in self.cfg.memory_persist_thresholds
                ):
                    self.queue_system_reminder(MEMORY_PERSIST_REMINDER)

    async def _maybe_compact(self, *, at_boundary: bool) -> None:
        if self.compactor is None:
            return
        cur = self._count_context()
        decision = self.compactor.classify(cur)
        if decision == "none":
            return
        if decision == "soft" and not at_boundary:
            return  # B1：缓押到下一个自然边界
        trigger = "force" if decision == "force" else "auto"
        await self._do_compact(trigger=trigger)

    async def _maybe_microcompact(self) -> None:
        if self.microcompactor is None:
            return
        messages = self.session_log.load()
        boundary = self.microcompactor.maybe_compact(messages)
        if boundary is None:
            return
        self.session_log.append(boundary)
        self._turn_index += 1

    async def _do_compact(self, *, trigger: str) -> None:
        assert self.compactor is not None
        messages = self.session_log.load()
        result = await self.compactor.compact(
            messages, trigger=trigger, current_turn_index=self._turn_index
        )
        if result is None:
            return  # 熔断 / 无可压；compaction_events.jsonl 已记
        self.session_log.append(result.boundary)
        self._turn_index += 1
        for msg in result.reinjection_messages:
            self.session_log.append(msg)
            self._turn_index += 1

    def _count_context(self) -> int:
        try:
            base = self.tokenizer.count_messages(self._build_provider_messages())
        except Exception:
            messages = apply_microcompact_redactions(self.session_log.load())
            visible, _ = messages_after_last_compact(messages)
            text = "\n".join(m.content for m in visible)
            base = max(1, len(text) // 4)
        return base + self._multimodal_token_overhead()

    def _multimodal_token_overhead(self) -> int:
        """tool_result 携带的 image/audio/video 附件对 context 的固定增量。

        本地 tokenizer 只会算附件那一行 ASCII 摘要，无法看到 base64 binary 实际
        消耗的 mm token；这里按 ``self._mm_cfg`` 锚点（默认对应 Gemma-4 processor
        config）保守累加，使本地视图与 provider 真实计费同口径。video 走 cv2 帧
        数精算，audio WAV 走 stdlib wave 时长精算。

        口径与 wire 一致：扫描最后一次 compact boundary 之后的 ``visible_after``
        中所有 ``ToolResultMessage.attachments``——boundary 之前的附件早已折叠
        进 summary，不再下发；按用户决策"followup user 允许压入 summary"，因此
        此处不主动剔除已被 microcompact redact 的 attachments。
        """
        total = 0
        all_messages = apply_microcompact_redactions(self.session_log.load())
        visible_after, _ = messages_after_last_compact(all_messages)
        for m in visible_after:
            attachments = getattr(m, "attachments", None) or []
            for raw_path, modality in attachments:
                if modality not in self.agent_modalities:
                    continue
                if modality not in {"image", "audio", "video"}:
                    continue
                total += estimate_attachment_tokens(
                    Path(raw_path), modality, self._mm_cfg
                )
        return total

    # ------------------------------------------------------------------
    # Provider message assembly
    # ------------------------------------------------------------------

    def _build_provider_messages(self) -> list[dict[str, Any]]:
        """从 jsonl 装配 provider 端 messages。

        步骤：

        1. ``apply_microcompact_redactions``：把所有 microcompact boundary 的 redactions
           在内存里重放到对应 tool_result.content；
        2. 提取 ``SystemMessage(subtype=prompt)`` 作为顶层 system；
        3. ``messages_after_last_compact`` 切到最后一条 compact_boundary 之后；
        4. 若存在 boundary，合成一条 user 消息携带 summary（claude-code 风格包装文案，
           不加 ``<system-reminder>``）；
        5. 渲染 tail，过滤掉 microcompact boundary（已重放完毕）与系统 prompt；
        6. 合并连续同 role 消息为一条，保证 user→assistant→...→user 严格交替。
        """
        all_messages = apply_microcompact_redactions(self.session_log.load())
        prompt_msgs = [
            m for m in all_messages
            if isinstance(m, SystemMessage) and m.subtype == "prompt"
        ]
        visible_after, boundary = messages_after_last_compact(all_messages)
        # 过滤掉残留的 system prompt 与 microcompact boundary
        visible_after = [
            m for m in visible_after
            if not isinstance(m, MicrocompactBoundaryMessage)
            and not (isinstance(m, SystemMessage) and m.subtype == "prompt")
        ]

        # 渲染 tail；对每条 ToolResultMessage 追加方案 C followup user 携带 base64 部件
        tail: list[dict[str, Any]] = []
        for m in visible_after:
            tail.append(self._message_to_provider(m))
            if isinstance(m, ToolResultMessage):
                followup = self._build_mm_followup(m)
                if followup is not None:
                    tail.append(followup)

        # 注入 summary 合成 user
        if boundary is not None:
            summary_user = {
                "role": "user",
                "content": COMPACTION_SUMMARY_WRAPPER.format(summary=boundary.content),
            }
            tail.insert(0, summary_user)

        # system + 合并同 role
        out: list[dict[str, Any]] = []
        for m in prompt_msgs:
            out.append({"role": "system", "content": m.content})
        out.extend(_merge_consecutive_same_role(tail))
        return out

    def _message_to_provider(self, m: Message) -> dict[str, Any]:
        rendered = self._render_content_with_reminders(m)
        if isinstance(m, UserMessage):
            return {"role": "user", "content": rendered}
        if isinstance(m, AssistantMessage):
            d: dict[str, Any] = {"role": "assistant", "content": rendered}
            if m.tool_calls:
                d["tool_calls"] = [
                    {
                        "id": tc["id"],
                        "type": "function",
                        "function": {
                            "name": tc["name"],
                            "arguments": json.dumps(tc["arguments"])
                            if not isinstance(tc.get("arguments"), str)
                            else tc["arguments"],
                        },
                    }
                    for tc in m.tool_calls
                ]
            return d
        if isinstance(m, ToolResultMessage):
            return {
                "role": "tool",
                "tool_call_id": m.tool_call_id,
                "content": rendered,
            }
        if isinstance(m, SystemMessage):
            return {"role": "system", "content": rendered}
        return {"role": m.role, "content": rendered}

    @staticmethod
    def _render_content_with_reminders(m: Message) -> str:
        notifications = getattr(m, "task_notifications", None) or []
        if not m.system_reminders and not notifications:
            return m.content
        parts = [m.content] if m.content else []
        parts.extend(wrap_system_reminder(r) for r in m.system_reminders)
        parts.extend(wrap_task_notification(n) for n in notifications)
        return "\n\n".join(p for p in parts if p)

    def _build_mm_followup(self, msg: ToolResultMessage) -> dict[str, Any] | None:
        """方案 C：tool_result 之后若有 image/audio/video 附件，追加 user 消息携带 base64 部件。

        过滤、size 限制、mp4 路径分支等由 ``provider.multimodal.attachments_to_parts``
        集中处理（见其 docstring）；本方法只负责拼接说明文字。
        """
        if not msg.attachments:
            return None
        parts, paths = attachments_to_parts(
            msg.attachments,
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

    # ------------------------------------------------------------------
    # Tool execution
    # ------------------------------------------------------------------

    def _make_tool_context(self) -> ToolContext:
        return ToolContext(
            agent_id=self.agent_id,
            scope=self.scope,
            read_tracker=self.read_tracker,
            cwd=self.cwd,
            config={
                "bash.default_timeout_ms": self.config_dict.get("bash", {}).get(
                    "default_timeout_sec", 60
                )
                * 1000,
                "bash.max_output_bytes": self.config_dict.get("bash", {}).get(
                    "max_output_bytes", 65536
                ),
                "bash.forbidden_prefixes": self.config_dict.get("bash", {}).get(
                    "forbidden_prefixes", ["git"]
                ),
                "grep.context_lines": self.config_dict.get("grep", {}).get("context_lines", 0),
                "grep.default_max_results": self.config_dict.get("grep", {}).get(
                    "default_max_results", 200
                ),
                "read.max_text_bytes": self.config_dict.get("read", {}).get(
                    "max_text_bytes", 524288
                ),
                "read.notice_bytes": self.config_dict.get("read", {}).get(
                    "notice_bytes", 32768
                ),
                "read.hard_bytes": self.config_dict.get("read", {}).get("hard_bytes", 262144),
                "multimodal.attachment_max_bytes": self._mm_cfg.attachment_max_bytes,
                "ls.max_entries": self.config_dict.get("ls", {}).get("max_entries", 1000),
                "workflow.max_agents": self.config_dict.get("workflow", {}).get(
                    "max_agents", 1000
                ),
                "workflow.max_concurrency": self.config_dict.get("workflow", {}).get(
                    "max_concurrency", 8
                ),
            },
            modality_counter=self.modality_counter,
            tools_used=self.tools_used,
            agent_modalities=list(self.agent_modalities),
            subagent_manager=self.subagent_manager,
            background=self.background,
            workflow_script_dir=self.workflow_script_dir,
            session_history=self.session_history,
        )

    async def _exec_tool(self, tc: dict[str, Any]) -> ToolExecResult:
        name = tc.get("name", "")
        tool = self.tools.get(name)
        if tool is None:
            return ToolExecResult(f"unknown tool: {name}", is_error=True)
        try:
            return await tool.run(tc.get("arguments") or {}, self._make_tool_context())
        except Exception as e:  # noqa: BLE001
            return ToolExecResult(f"tool {name} raised: {e}", is_error=True)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _merge_consecutive_same_role(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """合并连续同 role 消息为一条（content 用两换行拼接）。

    Anthropic API 要求 user/assistant 严格交替，但允许单条消息内 multi-part 文本。
    把"summary user + tail[0]=user"、"两条 reinjection user"、"连续 tool_result"
    等情形统一压成一条，避免触发 alternation 错误。

    对带 ``tool_calls`` 的 assistant 不做合并（保留结构完整性）。
    对 ``role="tool"`` 不合并（每条都对应特定 tool_call_id）。
    """
    if not messages:
        return messages
    out: list[dict[str, Any]] = []
    for m in messages:
        if not out:
            out.append(dict(m))
            continue
        prev = out[-1]
        if prev["role"] != m["role"]:
            out.append(dict(m))
            continue
        if m["role"] == "tool":
            out.append(dict(m))
            continue
        if m["role"] == "assistant" and (m.get("tool_calls") or prev.get("tool_calls")):
            out.append(dict(m))
            continue
        prev_content = prev.get("content", "") or ""
        m_content = m.get("content", "") or ""
        # multimodal followup user 携带 list-content（image_url / video_url /
        # input_audio parts）；不合并，保留独立消息以让 provider 正确投递 base64 部件。
        if not isinstance(prev_content, str) or not isinstance(m_content, str):
            out.append(dict(m))
            continue
        merged = "\n\n".join(p for p in (prev_content, m_content) if p)
        prev["content"] = merged
    return out
