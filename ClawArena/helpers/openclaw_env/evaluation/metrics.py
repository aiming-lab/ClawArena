"""Aggregate evaluation metrics."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

from openclaw_env.core.observation import EvaluationResult


@dataclass
class AggregateMetrics:
    """Aggregate metrics across multiple task evaluations."""

    total_tasks: int = 0
    passed_tasks: int = 0
    total_score: float = 0.0
    by_domain: dict[str, DomainMetrics] = field(default_factory=dict)
    by_difficulty: dict[int, DifficultyMetrics] = field(default_factory=dict)

    @property
    def tgc(self) -> float:
        """Task Goal Completion rate."""
        return self.passed_tasks / self.total_tasks if self.total_tasks > 0 else 0.0

    @property
    def avg_score(self) -> float:
        return self.total_score / self.total_tasks if self.total_tasks > 0 else 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_tasks": self.total_tasks,
            "passed_tasks": self.passed_tasks,
            "tgc": round(self.tgc * 100, 2),
            "avg_score": round(self.avg_score, 4),
            "by_domain": {k: v.to_dict() for k, v in self.by_domain.items()},
            "by_difficulty": {k: v.to_dict() for k, v in self.by_difficulty.items()},
        }


@dataclass
class DomainMetrics:
    total: int = 0
    passed: int = 0
    total_score: float = 0.0

    @property
    def tgc(self) -> float:
        return self.passed / self.total if self.total > 0 else 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "total": self.total,
            "passed": self.passed,
            "tgc": round(self.tgc * 100, 2),
        }


@dataclass
class DifficultyMetrics:
    total: int = 0
    passed: int = 0
    total_score: float = 0.0

    @property
    def tgc(self) -> float:
        return self.passed / self.total if self.total > 0 else 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "total": self.total,
            "passed": self.passed,
            "tgc": round(self.tgc * 100, 2),
        }


def compute_metrics(
    results: list[tuple[dict[str, Any], EvaluationResult]],
) -> AggregateMetrics:
    """Compute aggregate metrics from a list of (task_metadata, evaluation_result) pairs."""
    metrics = AggregateMetrics()

    for task_meta, eval_result in results:
        metrics.total_tasks += 1
        metrics.total_score += eval_result.score
        if eval_result.success:
            metrics.passed_tasks += 1

        # By domain
        for domain in task_meta.get("domains", []):
            if domain not in metrics.by_domain:
                metrics.by_domain[domain] = DomainMetrics()
            dm = metrics.by_domain[domain]
            dm.total += 1
            dm.total_score += eval_result.score
            if eval_result.success:
                dm.passed += 1

        # By difficulty
        diff = task_meta.get("difficulty", 0)
        if diff not in metrics.by_difficulty:
            metrics.by_difficulty[diff] = DifficultyMetrics()
        dfm = metrics.by_difficulty[diff]
        dfm.total += 1
        dfm.total_score += eval_result.score
        if eval_result.success:
            dfm.passed += 1

    return metrics
