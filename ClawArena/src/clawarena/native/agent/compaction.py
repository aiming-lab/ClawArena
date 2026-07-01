"""Compaction：大压缩（Compactor）+ 工具结果级裁剪（Microcompactor）。

设计参考 claude-code ``services/compact/{autoCompact,compact,microCompact}.ts``，
并在以下两点做 ArcBench 特化：

1. **语义边界缓压（B1）**：触发区间 ``[trigger_tokens, force_tokens)`` 内仅在
   "real-user-input 之前 / final-answer 之后"这样的自然边界触发；harness 通过
   :meth:`Compactor.classify` 拿到决策。``force_tokens`` 之上无论位置强制压缩，
   避免硬上限 OOM。
2. **uuid 范围 + reinjection 持久化**：压缩边界自带 ``summarized_head/tail_uuid``
   与 ``preserved_head_uuid``，重注入的最近文件以正规 UserMessage 直接追加到 jsonl
   boundary 之后，load 时无需特殊处理。

外部依赖：

- ``provider``：用于调 LLM 生成 summary。可用 main 模型，也可用专门的 compaction
  模型；compaction.modalities 强制 text-only。
- ``tokenizer``：本地估算 pre/post token 体量与文件 reinject 体量。
- ``read_tool_reader``：可选的"file path -> 文本内容"读取回调，用于 C2 reinjection。
"""
from __future__ import annotations

import asyncio
import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Awaitable, Callable, Literal, Optional

from ..prompts import (
    COMPACTION_SUMMARY_WRAPPER,
    COMPACTION_SYSTEM_PROMPT,
    COMPACTION_USER_PROMPT,
    POST_COMPACT_FILE_REINJECTION_WRAPPER,
)
from ..provider import BaseProvider
from ..tokenizer import UnifiedTokenizer
from .messages import (
    AssistantMessage,
    CompactBoundaryMessage,
    Message,
    MicrocompactBoundaryMessage,
    SystemMessage,
    ToolResultMessage,
    UserMessage,
)

# ---------------------------------------------------------------------------
# 数据结构
# ---------------------------------------------------------------------------


CompactDecision = Literal["none", "soft", "force"]


@dataclass
class CompactionEvent:
    triggered_at: float
    trigger: str                              # "auto" | "manual" | "force"
    pre_tokens: int
    post_tokens: int
    messages_summarized: int
    summary_chars: int
    boundary_uuid: str
    is_recompaction_in_chain: bool = False
    turns_since_previous_compact: int = -1
    reinjected_count: int = 0
    failed: bool = False
    failure_reason: str = ""
    extras: dict[str, Any] = field(default_factory=dict)


@dataclass
class CompactionResult:
    boundary: CompactBoundaryMessage
    reinjection_messages: list[UserMessage]
    event: CompactionEvent


# ---------------------------------------------------------------------------
# 主压缩
# ---------------------------------------------------------------------------


class Compactor:
    """生成压缩 boundary 与最近文件重注入。

    Args:
        provider: 调 LLM 写 summary 用的 provider。compaction modalities 已被
            ``parse_model_json`` 强制为 ``["text"]``。
        tokenizer: 本地 unified tokenizer，估 pre/post token 与 reinjection 文件体积。
        token_limit: main agent 的 context 上限。
        auto_compact_buffer_tokens: 触发阈值与 token_limit 之间的缓冲量（claude-code
            ``AUTOCOMPACT_BUFFER_TOKENS=13000`` 同义）。
        reserved_summary_output_tokens: 给 summary 输出预留的额度，从 token_limit 扣减
            后才形成"有效上限"（claude-code ``MAX_OUTPUT_TOKENS_FOR_SUMMARY=20000``）。
        force_pct: 强制阈值百分比。``ctx >= token_limit * force_pct / 100`` 强制压缩，
            忽略 B1 语义边界缓压。
        max_consecutive_failures: 连续 N 次压缩失败后熔断（不再尝试，仅 warn）；任一
            成功压缩重置计数。
        summarizer_max_output_tokens: 调 provider 时 ``max_tokens`` 上限。
        reinjection_enabled / reinjection_token_budget / reinjection_max_files /
        reinjection_max_tokens_per_file: C2 最近文件重注入相关配置。
        reinjection_reader: ``async (path: str) -> str`` 回调，给定绝对路径返回文件
            文本（应使用与 Read 工具一致的边界——大文件截断、binary 跳过等）；为 None
            时禁用重注入。
        events_log_path: 写 ``compaction_events.jsonl`` 的路径。
    """

    def __init__(
        self,
        *,
        provider: BaseProvider,
        tokenizer: UnifiedTokenizer,
        token_limit: int,
        auto_compact_buffer_tokens: int = 13000,
        reserved_summary_output_tokens: int = 20000,
        force_pct: int = 92,
        max_consecutive_failures: int = 3,
        summarizer_max_output_tokens: int = 20000,
        reinjection_enabled: bool = True,
        reinjection_token_budget: int = 50000,
        reinjection_max_files: int = 5,
        reinjection_max_tokens_per_file: int = 5000,
        reinjection_reader: Optional[Callable[[str], Awaitable[Optional[str]]]] = None,
        events_log_path: Optional[Path] = None,
    ):
        self.provider = provider
        self.tokenizer = tokenizer
        self.token_limit = int(token_limit)
        self.auto_compact_buffer_tokens = int(auto_compact_buffer_tokens)
        self.reserved_summary_output_tokens = int(reserved_summary_output_tokens)
        self.force_pct = int(force_pct)
        self.max_consecutive_failures = int(max_consecutive_failures)
        self.summarizer_max_output_tokens = int(summarizer_max_output_tokens)
        self.reinjection_enabled = bool(reinjection_enabled)
        self.reinjection_token_budget = int(reinjection_token_budget)
        self.reinjection_max_files = int(reinjection_max_files)
        self.reinjection_max_tokens_per_file = int(reinjection_max_tokens_per_file)
        self.reinjection_reader = reinjection_reader
        self.events_log_path = events_log_path

        # 链路状态
        self.consecutive_failures: int = 0
        self.compact_count: int = 0
        self._last_compact_turn_index: int = -1

    # ------------------------------------------------------------------
    # 触发判定
    # ------------------------------------------------------------------

    @property
    def effective_context_window(self) -> int:
        return max(1, self.token_limit - self.reserved_summary_output_tokens)

    @property
    def trigger_tokens(self) -> int:
        """软触发阈值（claude-code ``getAutoCompactThreshold`` 同义）。"""
        return max(1, self.effective_context_window - self.auto_compact_buffer_tokens)

    @property
    def force_tokens(self) -> int:
        """强制触发阈值，依 force_pct。"""
        return max(1, self.token_limit * self.force_pct // 100)

    def classify(self, ctx_tokens: int) -> CompactDecision:
        """返回压缩决策：``none`` / ``soft`` / ``force``。harness 负责把 ``soft``
        在 mid-tool-loop 缓押到自然边界再调用 :meth:`compact`。"""
        if ctx_tokens >= self.force_tokens:
            return "force"
        if ctx_tokens >= self.trigger_tokens:
            return "soft"
        return "none"

    def circuit_open(self) -> bool:
        """已连续失败 N 次，外部应跳过本次压缩。"""
        return self.consecutive_failures >= self.max_consecutive_failures

    # ------------------------------------------------------------------
    # 主调用
    # ------------------------------------------------------------------

    async def compact(
        self,
        messages: list[Message],
        *,
        trigger: str = "auto",
        current_turn_index: int = -1,
    ) -> Optional[CompactionResult]:
        """对 messages 做一次压缩。返回 ``None`` 表示熔断或无可压。

        切窗规则（严格保证 user→assistant→...→user 交替）：

        - 在 ``messages`` 中反向找最后一条 ``UserMessage(is_real_user_question=True)``
          所在 index ``split``。
        - ``window = messages[:split]``、``tail = messages[split:]``。
          tail 必以一个真实 user 起首；其后 assistant/tool_result 交替由原 agent loop
          天然保证。
        - 若 ``window`` 为空（用户连第一轮都还没结束），不压缩、返回 ``None``。
        - 若 ``messages`` 中根本没有 ``is_real_user_question=True``，回退到"反向找最
          后一条 ``CompactBoundaryMessage`` 之后的第一条 user"作 split（即 boundary
          后的第一个对外 turn）。
        """
        if self.circuit_open():
            return None

        split = self._choose_split(messages)
        if split <= 0:
            return None
        window = messages[:split]
        tail_first = messages[split]

        # 跳过非语义的 system prompt（仅参与"被压缩但不再注入到 summary 文本"，
        # 因为 transcript 投影端永远会把 SystemMessage(subtype=prompt) 单独取出）
        summarizable_window = [
            m for m in window
            if not (isinstance(m, SystemMessage) and m.subtype == "prompt")
        ]
        # 空窗：典型场景是 round 1 的第一发就触发了 force，但只有 [system, user_round1]
        # 在 log 上、根本没历史可压。直接放过即可，harness 会在下次自然边界再 evaluate。
        if not summarizable_window:
            return None
        # A4 显式 image strip 防御：把 ToolResultMessage.attachments 里的非 text
        # 模态以 "[image]" / "[audio]" / "[video]" 占位塞进文本——确保送 LLM 时
        # 不携带任何二进制 token。当前 Message.content 已是文本，但 future-proof
        # 还是在序列化阶段过一遍。
        history_text = _serialize_for_summary(summarizable_window)
        pre_text = _serialize_for_summary(summarizable_window + [tail_first] + messages[split + 1 :])
        pre_tokens = self.tokenizer.count(pre_text)

        # 链路追踪
        is_recompaction = self._last_compact_turn_index >= 0
        turns_since = (
            current_turn_index - self._last_compact_turn_index
            if is_recompaction and current_turn_index >= 0
            else -1
        )

        try:
            summary_text = await self._summarize(history_text)
        except Exception as e:  # noqa: BLE001
            self.consecutive_failures += 1
            evt = CompactionEvent(
                triggered_at=time.time(),
                trigger=trigger,
                pre_tokens=pre_tokens,
                post_tokens=pre_tokens,
                messages_summarized=len(summarizable_window),
                summary_chars=0,
                boundary_uuid="",
                is_recompaction_in_chain=is_recompaction,
                turns_since_previous_compact=turns_since,
                failed=True,
                failure_reason=str(e),
            )
            self._log_event(evt)
            return None

        # 成功 → 重置熔断计数
        self.consecutive_failures = 0

        boundary = CompactBoundaryMessage(
            content=summary_text,
            trigger=trigger,  # type: ignore[arg-type]
            pre_tokens=pre_tokens,
            summarized_head_uuid=summarizable_window[0].uuid if summarizable_window else None,
            summarized_tail_uuid=summarizable_window[-1].uuid if summarizable_window else None,
            preserved_head_uuid=tail_first.uuid,
            is_recompaction_in_chain=is_recompaction,
            turns_since_previous_compact=turns_since,
            logical_parent_uuid=(
                summarizable_window[-1].uuid if summarizable_window else None
            ),
        )

        # C2 reinjection：从 summarized_window 反向找最近 Read 过的文件
        reinjection_msgs: list[UserMessage] = []
        if self.reinjection_enabled and self.reinjection_reader is not None:
            reinjection_msgs = await self._build_reinjection_messages(
                summarizable_window, tail_messages=messages[split:]
            )
        boundary.reinjected_message_uuids = [m.uuid for m in reinjection_msgs]

        post_text = _serialize_for_summary(
            [boundary] + reinjection_msgs + messages[split:]
        )
        post_tokens = self.tokenizer.count(post_text)
        boundary.post_tokens = post_tokens

        self.compact_count += 1
        if current_turn_index >= 0:
            self._last_compact_turn_index = current_turn_index

        event = CompactionEvent(
            triggered_at=time.time(),
            trigger=trigger,
            pre_tokens=pre_tokens,
            post_tokens=post_tokens,
            messages_summarized=len(summarizable_window),
            summary_chars=len(summary_text),
            boundary_uuid=boundary.uuid,
            is_recompaction_in_chain=is_recompaction,
            turns_since_previous_compact=turns_since,
            reinjected_count=len(reinjection_msgs),
        )
        self._log_event(event)
        return CompactionResult(
            boundary=boundary,
            reinjection_messages=reinjection_msgs,
            event=event,
        )

    # ------------------------------------------------------------------
    # 内部辅助
    # ------------------------------------------------------------------

    @staticmethod
    def _choose_split(messages: list[Message]) -> int:
        """挑选切点：最后一条 real-user-input 的 index；找不到则退而求其次。"""
        last_compact_idx = -1
        for i in range(len(messages) - 1, -1, -1):
            if isinstance(messages[i], CompactBoundaryMessage):
                last_compact_idx = i
                break

        # 优先：最后一条 is_real_user_question=True 的 UserMessage（且位于 last
        # compact 之后）
        for i in range(len(messages) - 1, last_compact_idx, -1):
            m = messages[i]
            if isinstance(m, UserMessage) and m.is_real_user_question:
                return i
        # 次选：last compact 之后的第一条 UserMessage
        for i in range(last_compact_idx + 1, len(messages)):
            if isinstance(messages[i], UserMessage):
                return i
        return -1

    async def _summarize(self, history_text: str) -> str:
        system_prompt = COMPACTION_SYSTEM_PROMPT.format(
            max_tokens=self.summarizer_max_output_tokens
        )
        user_prompt = COMPACTION_USER_PROMPT.format(history_text=history_text)
        resp = await self.provider.chat(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            tools=None,
            max_tokens=self.summarizer_max_output_tokens,
        )
        summary = (resp.get("content") or "").strip()
        return summary or "(empty summary)"

    async def _build_reinjection_messages(
        self,
        summarized_window: list[Message],
        *,
        tail_messages: list[Message],
    ) -> list[UserMessage]:
        """C2：找出 summarized_window 中最近被 Read 过的文件路径，重新读盘
        并打包成 ``UserMessage`` 列表（每个文件一条）。

        筛选策略：

        - 仅扫 ``ToolResultMessage``，从 ``meta["tool"]`` 或 ``content`` 抽取曾经被
          Read 的路径；以最近优先
        - 已在 ``tail_messages`` 内出现的路径跳过——避免 tail 已有 fresh Read 又
          重注入造成重复
        - 单文件超 ``reinjection_max_tokens_per_file`` 则截到该上限
        - 累计 ``reinjection_token_budget`` 内最多 ``reinjection_max_files`` 条
        """
        if self.reinjection_reader is None:
            return []
        tail_paths = _collect_read_paths(tail_messages)
        candidates = _collect_read_paths(summarized_window, reverse=True)
        out: list[UserMessage] = []
        used_tokens = 0
        for path in candidates:
            if len(out) >= self.reinjection_max_files:
                break
            if path in tail_paths:
                continue
            if any(m.meta.get("path") == path for m in out):
                continue
            try:
                text = await self.reinjection_reader(path)
            except Exception:  # noqa: BLE001
                continue
            if not text:
                continue
            file_tokens = self.tokenizer.count(text)
            if file_tokens > self.reinjection_max_tokens_per_file:
                # 截断到单文件上限
                chars_per_token = max(1, len(text) // max(1, file_tokens))
                text = text[: self.reinjection_max_tokens_per_file * chars_per_token]
                file_tokens = self.tokenizer.count(text)
            if used_tokens + file_tokens > self.reinjection_token_budget:
                continue
            wrapped = POST_COMPACT_FILE_REINJECTION_WRAPPER.format(
                path=path, content=text
            )
            msg = UserMessage(
                content=wrapped,
                meta={"kind": "post_compact_file_attachment", "path": path},
            )
            out.append(msg)
            used_tokens += file_tokens
        return out

    def _log_event(self, evt: CompactionEvent) -> None:
        if self.events_log_path is None:
            return
        self.events_log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.events_log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(evt), ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# 微压缩（tool_result 级裁剪）
# ---------------------------------------------------------------------------


@dataclass
class MicrocompactorConfig:
    enabled: bool = True
    # 距离当前 tail 末尾 >= N 条消息的 tool_result 才算"陈旧"
    stale_after_messages: int = 30
    # 单条 tool_result 体量超过此 token 才裁
    size_threshold_tokens: int = 800
    # 单次 microcompact 最多裁多少条，避免一口气改太多
    max_redactions_per_event: int = 8


class Microcompactor:
    """tool_result 级别"陈旧大块"裁剪。

    与 claude-code ``microCompact.ts`` 思路一致：把工作循环已经"消化过"的旧 Read /
    Bash 输出替换为短占位 ``[old tool result trimmed: <tool> path=...]``，保留消息
    结构与 tool_call_id 配对，从而不影响 alternation 也不破坏 model 对工具历史的
    粗粒度感知。

    本类只**判断与产出 boundary**；boundary 落 jsonl 后由 ``apply_microcompact_
    redactions`` 在 load 时重放。
    """

    def __init__(
        self,
        *,
        tokenizer: UnifiedTokenizer,
        cfg: MicrocompactorConfig,
    ):
        self.tokenizer = tokenizer
        self.cfg = cfg

    def maybe_compact(self, messages: list[Message]) -> Optional[MicrocompactBoundaryMessage]:
        if not self.cfg.enabled:
            return None
        if len(messages) <= self.cfg.stale_after_messages:
            return None
        # 候选：messages[:-stale_after_messages] 内尚未被裁过的大 tool_result
        cutoff = len(messages) - self.cfg.stale_after_messages
        already_redacted: set[str] = set()
        for m in messages:
            if isinstance(m, MicrocompactBoundaryMessage):
                already_redacted.update(m.redactions.keys())

        redactions: dict[str, str] = {}
        tokens_saved_estimate = 0
        for m in messages[:cutoff]:
            if not isinstance(m, ToolResultMessage):
                continue
            if not m.tool_call_id or m.tool_call_id in already_redacted:
                continue
            tok = self.tokenizer.count(m.content or "")
            if tok < self.cfg.size_threshold_tokens:
                continue
            tool_name = m.meta.get("tool") or "tool"
            path_hint = m.meta.get("path") or ""
            placeholder = (
                f"[old tool result trimmed: {tool_name}"
                + (f" path={path_hint}" if path_hint else "")
                + f"; ~{tok} tokens reclaimed]"
            )
            redactions[m.tool_call_id] = placeholder
            tokens_saved_estimate += tok - self.tokenizer.count(placeholder)
            if len(redactions) >= self.cfg.max_redactions_per_event:
                break
        if not redactions:
            return None
        return MicrocompactBoundaryMessage(
            content="Context microcompacted",
            pre_tokens=0,
            tokens_saved=tokens_saved_estimate,
            redactions=redactions,
        )


# ---------------------------------------------------------------------------
# 工具
# ---------------------------------------------------------------------------


def _serialize_for_summary(messages: list[Message]) -> str:
    """把消息粗略拼成单段文本用于 token 计数 / summary 输入。

    A4 防御：ToolResultMessage 的 ``attachments`` 列表里若有非 text 模态，以
    占位符 ``[image: <path>]`` 等替换，确保 LLM 输入纯文本。
    """
    parts: list[str] = []
    for m in messages:
        if isinstance(m, AssistantMessage):
            tc_repr = json.dumps(m.tool_calls) if m.tool_calls else ""
            parts.append(f"[assistant] {m.content}\n{tc_repr}")
        elif isinstance(m, ToolResultMessage):
            atts = "".join(
                f"\n[{mod}: {path}]" for path, mod in m.attachments if mod != "text"
            )
            parts.append(f"[tool_result {m.tool_call_id}] {m.content}{atts}")
        elif isinstance(m, UserMessage):
            parts.append(f"[user] {m.content}")
        elif isinstance(m, CompactBoundaryMessage):
            parts.append(f"[compact_boundary] {m.content}")
        elif isinstance(m, MicrocompactBoundaryMessage):
            parts.append(f"[microcompact_boundary]")
        elif isinstance(m, SystemMessage):
            parts.append(f"[system:{m.subtype}] {m.content}")
        else:
            parts.append(f"[{m.role}] {m.content}")
    return "\n".join(parts)


def _collect_read_paths(messages: list[Message], *, reverse: bool = False) -> list[str]:
    """从 ToolResultMessage 列里抽取被 Read 的绝对路径。

    meta 中 ``tool == "Read"`` 时优先取 ``meta["path"]``；缺失就跳过。返回保持出现
    顺序去重；``reverse=True`` 则按消息倒序遍历（用于"最近优先"）。
    """
    seen: set[str] = set()
    out: list[str] = []
    iterator = reversed(messages) if reverse else iter(messages)
    for m in iterator:
        if not isinstance(m, ToolResultMessage):
            continue
        if m.meta.get("tool") != "Read":
            continue
        path = m.meta.get("path")
        if not path or path in seen:
            continue
        seen.add(path)
        out.append(path)
    return out
