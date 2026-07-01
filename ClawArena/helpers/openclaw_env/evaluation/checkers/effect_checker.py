"""Effect checker - verifies side effects of agent actions."""

from __future__ import annotations

from typing import Any

from openclaw_env.core.observation import CheckResult
from openclaw_env.evaluation.evaluator import Evaluator


class EffectChecker(Evaluator):
    """Checks that expected side effects occurred.

    Verifies things like: message was sent, cron job was created,
    plugin was installed, etc.
    """

    def __init__(
        self,
        effect_type: str,
        condition: str,
        expected: Any,
        name: str = "",
        weight: float = 1.0,
    ) -> None:
        self.effect_type = effect_type  # "message_sent", "cron_created", etc.
        self.condition = condition  # "exists", "count", "field_equals"
        self.expected = expected
        self.name = name or f"effect:{effect_type} {condition}"
        self.weight = weight

    def evaluate(
        self, env_state: dict[str, Any], task_data: dict[str, Any]
    ) -> CheckResult:
        effects = env_state.get("effects", {})
        effect_list = effects.get(self.effect_type, [])

        if self.condition == "exists":
            passed = len(effect_list) > 0
            msg = f"{self.effect_type} occurred: {passed}"

        elif self.condition == "count":
            passed = len(effect_list) == self.expected
            msg = f"{self.effect_type} count: {len(effect_list)} == {self.expected}: {passed}"

        elif self.condition == "count_equals":
            passed = len(effect_list) == self.expected
            msg = f"{self.effect_type} count: {len(effect_list)} == {self.expected}: {passed}"

        elif self.condition == "count_gte":
            passed = len(effect_list) >= self.expected
            msg = f"{self.effect_type} count: {len(effect_list)} >= {self.expected}: {passed}"

        elif self.condition == "count_lte":
            passed = len(effect_list) <= self.expected
            msg = f"{self.effect_type} count: {len(effect_list)} <= {self.expected}: {passed}"

        elif self.condition == "field_equals":
            # expected is {"field": "target", "value": "+1234567890"}
            field = self.expected.get("field", "")
            value = self.expected.get("value", "")
            passed = any(
                e.get(field) == value for e in effect_list
            )
            msg = f"{self.effect_type}.{field} == '{value}': {passed}"

        elif self.condition == "field_contains":
            field = self.expected.get("field", "")
            value = self.expected.get("value", "")
            needle = str(value).lower()
            passed = any(
                needle in str(e.get(field, "")).lower() for e in effect_list
            )
            msg = f"{self.effect_type}.{field} contains '{value}': {passed}"

        elif self.condition == "not_exists":
            passed = len(effect_list) == 0
            msg = f"{self.effect_type} did not occur: {passed}"

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
    def from_spec(cls, spec: dict[str, Any]) -> EffectChecker:
        return cls(
            effect_type=spec["effect_type"],
            condition=spec.get("condition", "exists"),
            expected=spec.get("expected"),
            name=spec.get("name", ""),
            weight=spec.get("weight", 1.0),
        )
