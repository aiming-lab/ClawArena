"""Task generators for Security domain (D8)."""

from __future__ import annotations

from typing import Any, Iterator

from openclaw_env.core.task import TaskData
from openclaw_env.tasks.registry import BaseTaskGenerator, Pass, SetupResult


@BaseTaskGenerator.register("set_security_token")
class SetSecurityTokenGenerator(BaseTaskGenerator):
    """Configure a security token for gateway authentication."""

    required_domains = ("security",)
    difficulty = 1
    parameters = {}

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={},
            private={"expected_token": "my-secret-token-abc123"},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            "Set a security token for the openclaw gateway. "
            "Use 'my-secret-token-abc123' as the token value."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return ["openclaw config set gateway.auth.token my-secret-token-abc123"]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "config",
                "config_path": "gateway.auth.token",
                "condition": "equals",
                "expected": "my-secret-token-abc123",
                "name": "auth token set",
            },
            {
                "type": "output",
                "match_type": "contains",
                "expected": "updated",
                "output_field": "last_stdout",
                "name": "security token updated",
                "ignore_case": True,
            },
        ]


@BaseTaskGenerator.register("check_security_status")
class CheckSecurityStatusGenerator(BaseTaskGenerator):
    """Check the current security configuration."""

    required_domains = ("security",)
    difficulty = 1
    parameters = {}

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        yield Pass(), TaskData()

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return "Check the current openclaw security configuration and report the authentication mode."

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return ["openclaw security audit"]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "output",
                "match_type": "regex",
                "expected": r"(Summary|critical|warn|audit|security)",
                "output_field": "last_stdout",
                "name": "security status shown",
                "ignore_case": True,
            }
        ]


@BaseTaskGenerator.register("rotate_security_token")
class RotateSecurityTokenGenerator(BaseTaskGenerator):
    """Multi-step: set a new security token and verify the configuration."""

    required_domains = ("security",)
    difficulty = 2
    parameters = {}

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={},
            private={"expected_token": "rotated-token-xyz789"},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            "Rotate the gateway security token: set a new token value "
            "'rotated-token-xyz789', then verify the security configuration "
            "shows the token is configured."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return [
            "openclaw config set gateway.auth.token rotated-token-xyz789",
            "openclaw security audit",
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "config",
                "config_path": "gateway.auth.token",
                "condition": "equals",
                "expected": "rotated-token-xyz789",
                "name": "auth token rotated",
            },
            {
                "type": "output",
                "match_type": "regex",
                "expected": r"(Summary|critical|warn|audit|security)",
                "output_field": "last_stdout",
                "name": "token configured verified",
                "ignore_case": True,
            },
        ]
