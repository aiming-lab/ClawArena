"""Abstract base class for question types."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from clawarena.core.types import TestContext


class QuestionType(ABC):
    """Interface for question type handlers.

    Pipeline order per round:
      infer:   format_query -> (agent) -> compute_inline_score -> build_feedback
      scoring: score
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Canonical type name (e.g. 'multi_choice', 'exec_check')."""

    @abstractmethod
    def format_query(self, round_record: dict, ctx: TestContext) -> str:
        """Format the query string sent to the agent."""

    @abstractmethod
    def compute_inline_score(
        self, round_record: dict, answer_text: str, ctx: TestContext,
    ) -> dict:
        """Score immediately after agent responds. Must return {'passed': bool, ...}."""

    @abstractmethod
    def build_feedback(
        self, round_record: dict, inline_score: dict, ctx: TestContext,
    ) -> str:
        """Generate feedback text for the next round. Empty string = no feedback."""

    @abstractmethod
    def validate_round(
        self, round_data: dict, scenario: str,
        eval_dir: Path | None = None,
        workspace: Path | None = None,
    ) -> tuple[list[str], list[str]]:
        """Validate type-specific fields. Returns (errors, warnings)."""

    @abstractmethod
    def score(
        self, answer_text: str, round_record: dict, ctx: TestContext,
        infer_result: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Final scoring. Must return {extracted_answer, correct_answer, score, metrics}."""
