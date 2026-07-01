"""Tool 基类。

ToolContext 在每次 tool 调用前由 AgentHarness 构造，含 sandbox、read_tracker、
cwd（Bash 等的固定工作目录）、agent 原生支持的模态等。
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from ..sandbox import AccessibleScope, ReadTracker


@dataclass
class ToolContext:
    agent_id: str
    scope: AccessibleScope
    read_tracker: ReadTracker
    cwd: Path
    config: dict[str, Any]
    modality_counter: dict[str, int] = field(default_factory=dict)
    tools_used: set[str] = field(default_factory=set)
    # 本 agent 原生支持的内容模态（至少含 "text"）。ReadTool 据此决定哪些后缀
    # 走原生返回，哪些降级为文本占位符。
    agent_modalities: list[str] = field(default_factory=lambda: ["text"])
    # 仅 main agent 持有：构造子代理的 manager（Agent 工具走它）。
    # subagent 自身的 ToolContext 中此项为 None，从而递归 Agent 调用直接 forbidden。
    subagent_manager: Optional[Any] = None
    # 仅 main agent 持有：统一后台任务注册表（Workflow 工具走它做异步后台 + 通知）。
    # subagent 为 None，从而 subagent 内不能跑 Workflow。
    background: Optional[Any] = None
    # 仅 main agent 持有：Workflow 脚本备份目录（落盘 + scriptPath 复用）。
    workflow_script_dir: Optional[Any] = None
    # 仅 main agent 持有：跨 session 历史读取器（SessionHistory 工具走它）。
    session_history: Optional[Any] = None


@dataclass
class ToolExecResult:
    content: str
    is_error: bool = False
    # 多模态附件：(绝对路径, modality)。harness 在拼装 provider messages 时按 modality
    # 转 image_block / audio_block / video_block。
    attachments: list[tuple[str, str]] = field(default_factory=list)


class BaseTool(ABC):
    name: str = ""
    description: str = ""

    @classmethod
    @abstractmethod
    def schema(cls, **format_kwargs: Any) -> dict[str, Any]:
        """返回 OpenAI-style function schema。"""

    @abstractmethod
    async def run(self, args: dict[str, Any], ctx: ToolContext) -> ToolExecResult: ...
