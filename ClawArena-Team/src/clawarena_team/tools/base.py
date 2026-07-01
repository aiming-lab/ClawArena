"""Tool base classes.

ToolContext is constructed by AgentHarness before every tool call. It carries the
sandbox, read_tracker, cwd (the fixed working directory for bash and friends), and
the callbacks into the subagent manager.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional

from ..sandbox import AccessibleScope, ReadTracker


@dataclass
class ToolContext:
    agent_id: str
    scope: AccessibleScope
    read_tracker: ReadTracker
    cwd: Path
    config: dict[str, Any]
    subagent_manager: Optional[Any] = None  # main agent only
    # Unified background task registry (BackgroundRegistry). Present only on the main
    # agent's ctx; None for subagents -- because of this, Bash's run_in_background takes
    # effect only on main, and degrades to synchronous execution inside a subagent.
    background: Optional[Any] = None
    # Directory where Workflow script backups are persisted (workflows/ alongside the
    # scenario's sessions/). main only.
    workflow_script_dir: Optional[Any] = None
    modality_counter: dict[str, int] = field(default_factory=dict)
    tools_used: set[str] = field(default_factory=set)
    # Count of Bash invocation modes {"runtime": n, "background": m} (a statistic).
    bash_mode_counter: dict[str, int] = field(default_factory=dict)
    # The content modalities this agent natively supports (always includes "text").
    # ReadTool uses this to decide which extensions return natively and which are
    # downgraded to a text placeholder.
    agent_modalities: list[str] = field(default_factory=lambda: ["text"])


@dataclass
class ToolExecResult:
    content: str
    is_error: bool = False
    attachments: list[tuple[str, str]] = field(default_factory=list)


class BaseTool(ABC):
    name: str = ""
    description: str = ""

    @classmethod
    @abstractmethod
    def schema(cls, **format_kwargs: Any) -> dict[str, Any]:
        """Return an OpenAI-style function schema."""

    @abstractmethod
    async def run(self, args: dict[str, Any], ctx: ToolContext) -> ToolExecResult: ...
