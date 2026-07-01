"""Composable evaluation framework for task verification."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from openclaw_env.core.observation import CheckResult, EvaluationResult


class Evaluator(ABC):
    """Base evaluator interface."""

    @abstractmethod
    def evaluate(
        self, env_state: dict[str, Any], task_data: dict[str, Any]
    ) -> CheckResult:
        """Evaluate the current state against task expectations."""


class EvaluatorComb:
    """Combines multiple evaluators into a single evaluation."""

    def __init__(self, evaluators: list[Evaluator]) -> None:
        self.evaluators = evaluators

    def __call__(
        self, env_state: dict[str, Any], task_data: dict[str, Any]
    ) -> EvaluationResult:
        results = [e.evaluate(env_state, task_data) for e in self.evaluators]
        total_weight = sum(r.weight for r in results)
        if total_weight == 0:
            score = 0.0
        else:
            score = sum(r.score * r.weight for r in results) / total_weight
        return EvaluationResult(
            success=all(r.passed for r in results),
            score=score,
            details=results,
        )


def build_evaluator(checks: list[dict[str, Any]]) -> EvaluatorComb:
    """Build an EvaluatorComb from a list of check specifications.

    Each check dict has a "type" key and type-specific parameters.
    """
    from openclaw_env.evaluation.checkers.config_checker import ConfigChecker
    from openclaw_env.evaluation.checkers.effect_checker import EffectChecker
    from openclaw_env.evaluation.checkers.output_checker import OutputChecker
    from openclaw_env.evaluation.checkers.state_checker import StateChecker

    from openclaw_env.evaluation.checkers.llm_checker import LLMChecker

    type_map: dict[str, type[Evaluator]] = {
        "state": StateChecker,
        "output": OutputChecker,
        "config": ConfigChecker,
        "effect": EffectChecker,
        "llm": LLMChecker,
    }

    evaluators: list[Evaluator] = []
    for check in checks:
        check_type = check.get("type", "")
        cls = type_map.get(check_type)
        if cls is None:
            raise ValueError(f"Unknown check type: {check_type}")
        evaluators.append(cls.from_spec(check))

    return EvaluatorComb(evaluators)
