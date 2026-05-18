"""State change checker - verifies environment state mutations."""

from __future__ import annotations

from typing import Any

from openclaw_env.core.observation import CheckResult
from openclaw_env.evaluation.evaluator import Evaluator


class StateChecker(Evaluator):
    """Checks that specific state changes occurred.

    Verifies things like: agent was created, channel was configured,
    gateway is running, etc.
    """

    def __init__(
        self,
        field: str,
        condition: str,
        expected: Any,
        name: str = "",
        weight: float = 1.0,
    ) -> None:
        self.field = field  # dot-separated path, e.g. "agents.researcher"
        self.condition = condition  # "exists", "equals", "contains", "not_exists"
        self.expected = expected
        self.name = name or f"state:{field} {condition}"
        self.weight = weight

    def evaluate(
        self, env_state: dict[str, Any], task_data: dict[str, Any]
    ) -> CheckResult:
        actual = _get_nested(env_state, self.field)

        if self.condition == "exists":
            passed = actual is not None
            msg = f"{self.field} exists: {passed}"
        elif self.condition == "not_exists":
            passed = actual is None
            msg = f"{self.field} not exists: {passed}"
        elif self.condition == "equals":
            passed = actual == self.expected
            msg = f"{self.field}: expected={self.expected}, actual={actual}"
        elif self.condition == "contains":
            passed = self.expected in actual if actual else False
            msg = f"{self.field} contains '{self.expected}': {passed}"
        elif self.condition == "count_gte":
            count = len(actual) if actual else 0
            passed = count >= self.expected
            msg = f"{self.field} count: {count} >= {self.expected}: {passed}"
        else:
            passed = False
            msg = f"Unknown condition: {self.condition}"

        return CheckResult(
            name=self.name,
            passed=passed,
            score=1.0 if passed else 0.0,
            weight=self.weight,
            message=msg,
        )

    @classmethod
    def from_spec(cls, spec: dict[str, Any]) -> StateChecker:
        return cls(
            field=spec["field"],
            condition=spec["condition"],
            expected=spec.get("expected"),
            name=spec.get("name", ""),
            weight=spec.get("weight", 1.0),
        )


def _get_nested(d: dict[str, Any], path: str) -> Any:
    """Get a nested value using dot-separated path."""
    keys = path.split(".")
    current: Any = d
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key)
        elif isinstance(current, list) and key.isdigit():
            idx = int(key)
            current = current[idx] if idx < len(current) else None
        else:
            return None
    return current
