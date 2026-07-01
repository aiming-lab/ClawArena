"""消息类型 + 切片 / 微压缩重放。

参考 claude-code 设计——每条消息有 ``uuid`` 与 ``parent_uuid``，可形成链表；
``CompactBoundaryMessage`` 与 ``MicrocompactBoundaryMessage`` 是两类 system 子类，
分别表示"大压缩"与"工具结果级裁剪"事件。

落盘到 JSONL 的约束：

- **append-only，永不删旧消息**。压缩事件以一条新 boundary 消息追加，自身携带 uuid
  范围、保留段锚点、链路追踪等元信息。
- 每次组装发给 provider 的 messages，都从 jsonl 读 + 应用最后一条 compact boundary
  做切片 + 应用所有 microcompact boundary 对 tool_result 做重写（v1 上下文量级足够
  轻量，线性扫描即可）。

注意 ``Message`` 与"模型消费的 provider message dict"是两层：前者是仓内表示，后者
由 ``transcript_for_provider`` 在每次 chat() 前现编。
"""
from __future__ import annotations

import time
import uuid as _uuid
from dataclasses import asdict, dataclass, field
from typing import Any, Literal, Optional


def _new_uuid() -> str:
    return _uuid.uuid4().hex


@dataclass
class Message:
    """所有消息共享基础字段。"""

    role: str                              # system / user / assistant / tool_result
    content: str = ""
    uuid: str = field(default_factory=_new_uuid)
    parent_uuid: Optional[str] = None
    timestamp: float = field(default_factory=time.time)
    # system-reminder 原文片段（拼接到 content 末尾时由 transcript 模块包装）
    system_reminders: list[str] = field(default_factory=list)
    # 背景任务（Workflow / background subagent）完成通知原文片段。与 system_reminders
    # 分两类带外通道，渲染时分别包成 <task-notification>...</task-notification>。
    task_notifications: list[str] = field(default_factory=list)
    # 自由扩展元数据，便于上层 runner 携带 round_id / scenario_id / arc_id 等上下文
    meta: dict[str, Any] = field(default_factory=dict)

    def to_jsonl(self) -> dict[str, Any]:
        d = asdict(self)
        return d


@dataclass
class SystemMessage(Message):
    """``role=system`` 的消息。常见于 session 首条 system prompt。

    ``subtype`` 区分语义：``"prompt"`` (默认)、``"compact_boundary"``、
    ``"microcompact_boundary"`` 等。
    """

    role: str = "system"
    subtype: str = "prompt"


@dataclass
class UserMessage(Message):
    role: str = "user"
    # 标识该 user turn 是否为"真实用户问题"——影响 usage hint 注入策略。
    is_real_user_question: bool = False


@dataclass
class AssistantMessage(Message):
    role: str = "assistant"
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    # context tracking（仅本条 assistant turn 对应的本地视图三段）
    input_delta: int = 0
    output_delta: int = 0
    cache_read_delta: int = 0
    context_size_after: int = 0
    provider_usage: dict[str, Any] = field(default_factory=dict)
    usage_normalized: dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolResultMessage(Message):
    role: str = "tool_result"
    tool_call_id: str = ""
    is_error: bool = False
    # 多模态附件：[(path, modality), ...]
    attachments: list[tuple[str, str]] = field(default_factory=list)


@dataclass
class CompactBoundaryMessage(Message):
    """压缩边界标记。``content`` 即压缩后的 summary 文本。

    重建 transcript 时遇到最后一条 boundary 即"丢弃其之前的所有非系统消息"，
    并把 ``content`` 投影为一条 user 消息（claude-code 风格，"This session is being
    continued..." 包装），与紧随其后的 tail 头部 user 合并。

    uuid 范围字段（``summarized_head_uuid`` / ``summarized_tail_uuid`` /
    ``preserved_head_uuid``）让 load 端可以确定性还原切片，且不依赖消息计数。
    """

    role: str = "system"
    subtype: Literal["compact_boundary"] = "compact_boundary"
    trigger: Literal["manual", "auto", "force"] = "auto"
    pre_tokens: int = 0
    post_tokens: int = 0
    # 被压缩窗口的 uuid 范围 [head, tail]，闭区间。
    summarized_head_uuid: Optional[str] = None
    summarized_tail_uuid: Optional[str] = None
    # 保留尾的首条 uuid；空保留段则为 None。
    preserved_head_uuid: Optional[str] = None
    # 链路追踪（claude-code recompactionInfo 同款）
    is_recompaction_in_chain: bool = False
    turns_since_previous_compact: int = -1
    # C2 文件重注入：紧跟 boundary 之后追加的 UserMessage uuid 列表
    reinjected_message_uuids: list[str] = field(default_factory=list)
    # 与 summarized_tail_uuid 等价，保留作冗余审计字段
    logical_parent_uuid: Optional[str] = None


@dataclass
class MicrocompactBoundaryMessage(Message):
    """工具结果级裁剪事件。

    `content` 仅人类可读说明（"Context microcompacted"），真正裁剪信息在
    ``redactions``：``{tool_call_id: placeholder_text}``。load 端线性扫描时遇到
    本边界即把 ``redactions`` 中提到的所有 **更早出现** 的 ToolResultMessage 的
    ``content`` 字段就地替换为对应 placeholder（仍保留在内存里，但 provider 投影
    时只看 placeholder）。

    与 CompactBoundaryMessage 区别：**不切片**，message 数不变，仅减字节。
    """

    role: str = "system"
    subtype: Literal["microcompact_boundary"] = "microcompact_boundary"
    trigger: Literal["auto"] = "auto"
    pre_tokens: int = 0
    tokens_saved: int = 0
    # tool_call_id -> 占位文本（如 "[old tool result trimmed: Read /path/to.py]"）
    redactions: dict[str, str] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def is_compact_boundary(d: dict[str, Any]) -> bool:
    """判断一条 jsonl 记录是否是 compact boundary（不含 microcompact）。"""
    return d.get("role") == "system" and d.get("subtype") == "compact_boundary"


def is_microcompact_boundary(d: dict[str, Any]) -> bool:
    return d.get("role") == "system" and d.get("subtype") == "microcompact_boundary"


def message_from_dict(d: dict[str, Any]) -> Message:
    """从 jsonl 行重建消息对象。未知字段保留在 meta 内。"""
    role = d.get("role", "user")
    common = {
        "role": role,
        "content": d.get("content", ""),
        "uuid": d.get("uuid", _new_uuid()),
        "parent_uuid": d.get("parent_uuid"),
        "timestamp": d.get("timestamp", time.time()),
        "system_reminders": list(d.get("system_reminders") or []),
        "task_notifications": list(d.get("task_notifications") or []),
        "meta": dict(d.get("meta") or {}),
    }
    if role == "system":
        subtype = d.get("subtype", "prompt")
        if subtype == "compact_boundary":
            return CompactBoundaryMessage(
                **common,
                subtype="compact_boundary",
                trigger=d.get("trigger", "auto"),
                pre_tokens=int(d.get("pre_tokens", 0)),
                post_tokens=int(d.get("post_tokens", 0)),
                summarized_head_uuid=d.get("summarized_head_uuid"),
                summarized_tail_uuid=d.get("summarized_tail_uuid"),
                preserved_head_uuid=d.get("preserved_head_uuid"),
                is_recompaction_in_chain=bool(d.get("is_recompaction_in_chain", False)),
                turns_since_previous_compact=int(d.get("turns_since_previous_compact", -1)),
                reinjected_message_uuids=list(d.get("reinjected_message_uuids") or []),
                logical_parent_uuid=d.get("logical_parent_uuid"),
            )
        if subtype == "microcompact_boundary":
            return MicrocompactBoundaryMessage(
                **common,
                subtype="microcompact_boundary",
                trigger=d.get("trigger", "auto"),
                pre_tokens=int(d.get("pre_tokens", 0)),
                tokens_saved=int(d.get("tokens_saved", 0)),
                redactions=dict(d.get("redactions") or {}),
            )
        return SystemMessage(**common, subtype=subtype)
    if role == "user":
        return UserMessage(
            **common,
            is_real_user_question=bool(d.get("is_real_user_question", False)),
        )
    if role == "assistant":
        return AssistantMessage(
            **common,
            tool_calls=list(d.get("tool_calls") or []),
            input_delta=int(d.get("input_delta", 0)),
            output_delta=int(d.get("output_delta", 0)),
            cache_read_delta=int(d.get("cache_read_delta", 0)),
            context_size_after=int(d.get("context_size_after", 0)),
            provider_usage=dict(d.get("provider_usage") or {}),
            usage_normalized=dict(d.get("usage_normalized") or {}),
        )
    if role == "tool_result":
        return ToolResultMessage(
            **common,
            tool_call_id=d.get("tool_call_id", ""),
            is_error=bool(d.get("is_error", False)),
            attachments=[tuple(a) for a in (d.get("attachments") or [])],
        )
    return Message(**common)


def apply_microcompact_redactions(messages: list[Message]) -> list[Message]:
    """在线性顺序上重放所有 microcompact boundary：把更早出现的同 ``tool_call_id``
    ToolResultMessage 的 content 就地替换为对应 placeholder。

    返回新列表（messages 自身不被改写，便于多次 load 调用不互相污染）。
    """
    out: list[Message] = []
    for m in messages:
        out.append(m)
    for i, m in enumerate(out):
        if not isinstance(m, MicrocompactBoundaryMessage):
            continue
        for j in range(i):
            tgt = out[j]
            if isinstance(tgt, ToolResultMessage) and tgt.tool_call_id in m.redactions:
                placeholder = m.redactions[tgt.tool_call_id]
                # 复制一份避免原对象被多次重写
                out[j] = ToolResultMessage(
                    role=tgt.role,
                    content=placeholder,
                    uuid=tgt.uuid,
                    parent_uuid=tgt.parent_uuid,
                    timestamp=tgt.timestamp,
                    system_reminders=list(tgt.system_reminders),
                    meta=dict(tgt.meta),
                    tool_call_id=tgt.tool_call_id,
                    is_error=tgt.is_error,
                    attachments=list(tgt.attachments),
                )
    return out


def messages_after_last_compact(
    messages: list[Message],
) -> tuple[list[Message], Optional[CompactBoundaryMessage]]:
    """切片：返回最后一次 compact boundary 之后的消息 + boundary 自身。

    若无 boundary 返回 (全部消息, None)。microcompact boundary 在此**不参与切片**，
    它们会留在返回的列表中（如果位于 last-compact 之后），供其他逻辑参考——但其本身
    在投影到 provider 时会被丢弃（只用于 load-time 重放 redactions）。
    """
    idx = -1
    for i in range(len(messages) - 1, -1, -1):
        if isinstance(messages[i], CompactBoundaryMessage):
            idx = i
            break
    if idx == -1:
        return list(messages), None
    return list(messages[idx + 1 :]), messages[idx]  # type: ignore[return-value]
