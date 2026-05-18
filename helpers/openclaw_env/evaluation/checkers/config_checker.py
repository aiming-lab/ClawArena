"""Config checker - verifies openclaw configuration state."""

from __future__ import annotations

import math
from typing import Any

from openclaw_env.core.observation import CheckResult
from openclaw_env.evaluation.evaluator import Evaluator

_CONFIG_ALIASES: dict[str, list[str]] = {
    # OpenClaw migrated from `agent.model` to `agents.defaults.model.primary`.
    "agent.model": ["agents.defaults.model.primary"],
}


class ConfigChecker(Evaluator):
    """Checks that the openclaw configuration matches expectations.

    Verifies config file values after agent actions.
    """

    def __init__(
        self,
        config_path: str,
        condition: str,
        expected: Any,
        name: str = "",
        weight: float = 1.0,
    ) -> None:
        self.config_path = config_path  # dot-separated, e.g. "agent.model"
        self.condition = condition  # "equals", "contains", "exists", "type_is"
        self.expected = expected
        self.name = name or f"config:{config_path} {condition}"
        self.weight = weight

    def evaluate(
        self, env_state: dict[str, Any], task_data: dict[str, Any]
    ) -> CheckResult:
        config = env_state.get("config", {})
        actual = _resolve_config_value(config, self.config_path)

        if self.condition == "equals":
            passed = _equals_with_numeric_coercion(actual, self.expected)
            msg = f"config.{self.config_path}: expected={self.expected}, actual={actual}"
        elif self.condition == "contains":
            passed = self.expected in actual if actual else False
            msg = f"config.{self.config_path} contains '{self.expected}': {passed}"
        elif self.condition == "exists":
            passed = actual is not None
            msg = f"config.{self.config_path} exists: {passed}"
        elif self.condition == "not_exists":
            passed = actual is None
            msg = f"config.{self.config_path} not exists: {passed}"
        elif self.condition == "type_is":
            passed = type(actual).__name__ == self.expected
            msg = f"config.{self.config_path} type: {type(actual).__name__} == {self.expected}: {passed}"
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
    def from_spec(cls, spec: dict[str, Any]) -> ConfigChecker:
        return cls(
            config_path=spec["config_path"],
            condition=spec.get("condition", "equals"),
            expected=spec.get("expected"),
            name=spec.get("name", ""),
            weight=spec.get("weight", 1.0),
        )


def _get_nested(d: dict[str, Any], path: str) -> Any:
    keys = path.split(".")
    current: Any = d
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key)
        else:
            return None
    return current


def _resolve_config_value(config: dict[str, Any], config_path: str) -> Any:
    """Read config value with legacy-path fallback aliases."""
    actual = _get_nested(config, config_path)
    if actual is not None:
        return actual

    for alias in _CONFIG_ALIASES.get(config_path, []):
        aliased = _get_nested(config, alias)
        if aliased is not None:
            return aliased
    return None


def _as_number(value: Any) -> float | None:
    """Best-effort numeric parsing used for tolerant config equality checks."""
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if not isinstance(value, str):
        return None

    text = value.strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _equals_with_numeric_coercion(actual: Any, expected: Any) -> bool:
    if actual == expected:
        return True

    actual_num = _as_number(actual)
    expected_num = _as_number(expected)
    if actual_num is None or expected_num is None:
        return False
    return math.isclose(actual_num, expected_num, rel_tol=0.0, abs_tol=1e-9)
