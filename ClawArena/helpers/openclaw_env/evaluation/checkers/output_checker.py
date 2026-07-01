"""Output checker - verifies command output content."""

from __future__ import annotations

import re
from typing import Any

from openclaw_env.core.observation import CheckResult
from openclaw_env.evaluation.evaluator import Evaluator


class OutputChecker(Evaluator):
    """Checks that command output matches expected patterns.

    Similar to WebArena's string_match evaluator.
    """

    def __init__(
        self,
        match_type: str,
        expected: str | None,
        output_field: str = "last_stdout",
        name: str = "",
        weight: float = 1.0,
        ignore_case: bool = True,
    ) -> None:
        self.match_type = match_type  # "exact", "contains", "regex", "not_contains"
        self.expected = expected
        self.output_field = output_field
        self.name = name or f"output:{match_type}"
        self.weight = weight
        self.ignore_case = ignore_case

    def evaluate(
        self, env_state: dict[str, Any], task_data: dict[str, Any]
    ) -> CheckResult:
        actual_raw = env_state.get(self.output_field, "")
        actual = "" if actual_raw is None else str(actual_raw)
        expected_raw = "" if self.expected is None else str(self.expected)

        if self.match_type == "exit_code_zero":
            exit_code = env_state.get("last_exit_code", None)
            passed = exit_code == 0
            msg = f"exit_code_zero check: actual={exit_code}"
        else:
            actual_cmp = actual
            expected_cmp = expected_raw
            if self.ignore_case:
                actual_cmp = actual_cmp.lower()
                expected_cmp = expected_cmp.lower()

            if self.match_type == "exact":
                passed = actual_cmp.strip() == expected_cmp.strip()
            elif self.match_type == "contains":
                passed = expected_cmp in actual_cmp
            elif self.match_type == "not_contains":
                passed = expected_cmp not in actual_cmp
            elif self.match_type == "regex":
                flags = re.IGNORECASE if self.ignore_case else 0
                passed = bool(re.search(expected_raw, actual, flags))
            else:
                passed = False
            msg = (
                f"{self.match_type} check: expected='{expected_raw[:50]}', "
                f"actual='{actual[:50]}'"
            )

        return CheckResult(
            name=self.name,
            passed=passed,
            score=1.0 if passed else 0.0,
            weight=self.weight,
            message=msg,
        )

    @classmethod
    def from_spec(cls, spec: dict[str, Any]) -> OutputChecker:
        match_type = spec.get("match_type")
        if match_type is None:
            # Many generated task specs use `condition` for output checks.
            match_type = spec.get("condition", "contains")
        return cls(
            match_type=match_type,
            expected=spec.get("expected"),
            output_field=spec.get("output_field", "last_stdout"),
            name=spec.get("name", ""),
            weight=spec.get("weight", 1.0),
            ignore_case=spec.get("ignore_case", True),
        )
