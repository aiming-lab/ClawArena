"""SubagentManager：spawn 子代理。

每次 :meth:`run` 调用：

1. 分配 ``sub_<8hex>`` 作为 sub_id
2. 新建独立的 :class:`SessionLog`（``sessions/<sub_id>.jsonl``）
3. 新建独立的 :class:`ReadTracker`（子代理不继承父代理 read 状态）
4. 沿用同一 :class:`AccessibleScope`（workspace 共享）
5. 按 ``subagent_type`` 选工具集：
    - ``Explore``：Read / LS / Grep / Glob（纯只读）
    - ``general-purpose``：Bash / Read / Write / Edit / Glob / Grep / LS（**无 Agent**）
6. 构造一个新的 :class:`AgentHarness`（``compactor=None`` —— 子代理短命，不压缩；
   超 ``max_iterations`` 直接返回当前最后一段 assistant 文本）
7. ``send_user(prompt, is_real_question=True)`` → 取 assistant 答案

子代理结束后由 main 自行决定是否再次 spawn。子代理产物对 workspace 的副作用对 main
可见（共享 workspace），但因 main 的 ReadTracker 不被子代理改动，main 后续 Edit 仍受
own read-before-edit 限制——这与 AutoHarness 行为一致。
"""
from __future__ import annotations

import uuid as _uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from ..provider import BaseProvider
from ..sandbox import AccessibleScope, ReadTracker
from ..tokenizer import UnifiedTokenizer
from ..tools import BASIC_TOOLS, BaseTool, schema_format_kwargs
from ..tools.ls import LSTool
from .harness import AgentHarness, HarnessConfig
from .messages import AssistantMessage
from .session_log import SessionLog


# Explore + general-purpose 的工具子集
_EXPLORE_TOOLS = ("Read", "LS", "Grep", "Glob")
_GP_TOOLS = ("Bash", "Read", "Write", "Edit", "Glob", "Grep", "LS")


# Subagent system prompts —— 短促、强调"只回最终答案"
_EXPLORE_SYSTEM_PROMPT = """\
You are an Explore subagent — a read-only research worker called by a main agent to investigate a workspace and report back. Use Read / LS / Grep / Glob to navigate, gather evidence, and answer the question you were asked. Return a concise final assistant message; do not produce additional commentary or follow-up questions. You cannot Write, Edit, or run Bash; you cannot spawn further subagents."""

_GP_SYSTEM_PROMPT = """\
You are a general-purpose subagent invoked by a main agent to complete a focused subtask. You have Bash / Read / Write / Edit / Glob / Grep / LS. Do exactly what the prompt asks — no more, no less — and return a concise final assistant message describing what you did and any pertinent facts the main agent needs. You cannot spawn further subagents. Files you Read/Edit/Write/Bash on are visible on disk to the main agent."""


@dataclass
class SubagentResult:
    answer: str
    error: Optional[str] = None
    iterations_used: int = 0
    sub_id: str = ""
    # 结构化输出模式（schema 非空）下，校验过的对象；否则 None。
    data: Any = None


class SubagentManager:
    """单 main 一份；负责构造与运行 subagent。"""

    def __init__(
        self,
        *,
        provider: BaseProvider,
        tokenizer: UnifiedTokenizer,
        workspace_root: Path,
        sessions_dir: Path,
        config_dict: dict[str, Any],
        agent_modalities: list[str],
        token_limit: int,
        max_iterations: int,
        explore_enabled: bool = True,
        general_purpose_enabled: bool = True,
    ):
        self.provider = provider
        self.tokenizer = tokenizer
        self.workspace_root = workspace_root
        self.sessions_dir = sessions_dir
        self.config_dict = config_dict
        self.agent_modalities = list(agent_modalities)
        self.token_limit = token_limit
        self.max_iterations = max_iterations
        self.explore_enabled = explore_enabled
        self.general_purpose_enabled = general_purpose_enabled

    async def run(
        self,
        *,
        subagent_type: str,
        description: str,
        prompt: str,
        schema: Optional[dict] = None,
        system_suffix: Optional[str] = None,
    ) -> SubagentResult:
        """运行一个 subagent。

        ``schema`` 非空时走结构化输出，返回的 ``SubagentResult.data`` 为校验过的对象。
        ``system_suffix`` 非空时追加到 subagent 的 system prompt 末尾（Workflow 的
        agent() 路径用它告知 subagent "最终文本即返回值"）。
        """
        if subagent_type == "Explore" and not self.explore_enabled:
            return SubagentResult(answer="", error="Explore subagent is disabled")
        if subagent_type == "general-purpose" and not self.general_purpose_enabled:
            return SubagentResult(answer="", error="general-purpose subagent is disabled")
        sub_id = "sub_" + _uuid.uuid4().hex[:8]
        try:
            tool_names = (
                _EXPLORE_TOOLS if subagent_type == "Explore" else _GP_TOOLS
            )
            tools: dict[str, BaseTool] = {}
            schemas: list[dict[str, Any]] = []
            schema_kwargs = schema_format_kwargs(self.config_dict, self.agent_modalities)
            for name in tool_names:
                if name == "LS":
                    cls: type[BaseTool] = LSTool
                else:
                    cls = BASIC_TOOLS[name]
                tools[name] = cls()
                schemas.append(cls.schema(**schema_kwargs))

            system_prompt = (
                _EXPLORE_SYSTEM_PROMPT
                if subagent_type == "Explore"
                else _GP_SYSTEM_PROMPT
            )
            if system_suffix:
                system_prompt = system_prompt.rstrip() + "\n\n" + system_suffix
            scope = AccessibleScope(
                allowed=[self.workspace_root], workspace_root=self.workspace_root
            )
            session_log = SessionLog(self.sessions_dir / f"{sub_id}.jsonl")
            read_tracker = ReadTracker()
            cfg = HarnessConfig(
                token_limit=self.token_limit,
                usage_thresholds_pct=[80, 90, 95],
                always_hint_on_real_user=False,
                max_iterations=self.max_iterations,
            )
            harness = AgentHarness(
                agent_id=sub_id,
                system_prompt=system_prompt,
                provider=self.provider,
                tools=tools,
                tool_schemas=schemas,
                scope=scope,
                read_tracker=read_tracker,
                cwd=self.workspace_root,
                tokenizer=self.tokenizer,
                cfg=cfg,
                config_dict=self.config_dict,
                session_log=session_log,
                compactor=None,                       # 子代理无 compaction
                agent_modalities=self.agent_modalities,
            )
            raw = await harness.send_user(
                prompt, is_real_question=True, schema=schema
            )
            # 统计 iterations：以 assistant turn 数量近似
            iters = sum(
                1 for m in session_log.load() if isinstance(m, AssistantMessage)
            )
            if schema is not None and not isinstance(raw, str):
                # 结构化输出成功：raw 是校验过的对象。
                import json as _json

                return SubagentResult(
                    answer=_json.dumps(raw, ensure_ascii=False, default=str),
                    data=raw,
                    iterations_used=iters,
                    sub_id=sub_id,
                )
            return SubagentResult(
                answer=raw if isinstance(raw, str) else str(raw),
                iterations_used=iters,
                sub_id=sub_id,
            )
        except Exception as e:  # noqa: BLE001
            return SubagentResult(answer="", error=f"{type(e).__name__}: {e}", sub_id=sub_id)
