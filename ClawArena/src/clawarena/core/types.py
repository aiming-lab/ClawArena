"""Public data types used across the clawarena framework."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal, TypedDict


# ---------------------------------------------------------------------------
# Engine types
# ---------------------------------------------------------------------------


@dataclass
class AgentResult:
    """Result of a single agent invocation."""

    status: Literal["success", "failed", "timeout"]
    answer: str
    error: str | None = None
    returncode: int | None = None
    raw: Any = None
    llm_log: dict | None = None


@dataclass
class GatewayHandle:
    """Handle to a running gateway process."""

    process: asyncio.subprocess.Process | None = None
    port: int | None = None
    stdout_chunks: list[str] = field(default_factory=list)
    stderr_chunks: list[str] = field(default_factory=list)
    stdout_task: asyncio.Task | None = None
    stderr_task: asyncio.Task | None = None

    def debug_output(self) -> str:
        """Return captured gateway stdout/stderr for diagnostics."""
        sections: list[str] = []
        if self.stdout_chunks:
            sections.append("stdout:\n" + "".join(self.stdout_chunks).strip())
        if self.stderr_chunks:
            sections.append("stderr:\n" + "".join(self.stderr_chunks).strip())
        return "\n\n".join(s for s in sections if s.strip())


class NoOpGatewayHandle(GatewayHandle):
    """Sentinel for frameworks that don't need a gateway."""

    pass


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------


@dataclass
class WorkCopy:
    """Isolated working copy for a benchmark run."""

    state_dir: Path
    config_path: Path | None
    project_root: Path
    workspace_root: Path | None = None
    extra: dict = field(default_factory=dict)


class TestContext(TypedDict, total=False):
    """Context passed to QType methods and engine hooks."""

    framework: str
    test_id: str
    eval_dir: Path
    eval_name: str
    workspace: Path | None
    agent_id: str
    session_id: str
    history_sessions: list[str]
    gateway_port: int | None
    work_copy: WorkCopy


# ---------------------------------------------------------------------------
# Scoring types
# ---------------------------------------------------------------------------


@dataclass
class ScoringResult:
    """Result of scoring a single round."""

    extracted_answer: list[str] | None
    correct_answer: list[str] | None
    score: float
    metrics: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Round hook types (used by AgentEngine.on_round_complete)
# ---------------------------------------------------------------------------


@dataclass
class RoundContext:
    """Context passed to engine round hooks."""

    framework: str
    test_id: str
    round_id: str
    round_index: int
    total_rounds: int
    is_last_round: bool
    round_record: dict
    query: str
    result: dict
    inline_score: dict
    prev_inline_score: dict | None
    all_results: list[dict] | None
    all_inline_scores: list[dict] | None
    result_path: Path
    workspace_path: Path | None
    out_dir: Path
    session_id: str = ""
    work_copy: WorkCopy | None = None


@dataclass
class RoundResult:
    """Return value from engine round hooks. All fields optional."""

    skip_remaining: bool = False
    override_feedback: str | None = None
    override_inline_score: dict | None = None
    extra_data: dict | None = None
    skip_standalone_feedback: bool = False
