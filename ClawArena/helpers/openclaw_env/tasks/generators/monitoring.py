"""Task generators for Monitoring & Diagnostics domain (D5)."""

from __future__ import annotations

from typing import Any, Iterator

from openclaw_env.core.task import TaskData
from openclaw_env.tasks.registry import BaseTaskGenerator, Pass, SetupResult


@BaseTaskGenerator.register("check_system_status")
class CheckSystemStatusGenerator(BaseTaskGenerator):
    """Generate tasks for checking system status."""

    required_domains = ("monitoring",)
    difficulty = 1
    parameters = {
        "format": ["text", "json"],
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(public={"format": params["format"]})
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        if params["format"] == "json":
            return "Check the openclaw system status and output it in JSON format."
        return "Check the current openclaw system status."

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        if params["format"] == "json":
            return ["openclaw status --json"]
        return ["openclaw status"]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        if params["format"] == "json":
            return [
                {
                    "type": "output",
                    "match_type": "contains",
                    "expected": "gateway",
                    "output_field": "last_stdout",
                    "name": "status output contains gateway info",
                }
            ]
        return [
            {
                "type": "output",
                "match_type": "regex",
                "expected": r"(Gateway|gateway|running|stopped)",
                "output_field": "last_stdout",
                "name": "status output shown",
                "ignore_case": True,
            }
        ]


@BaseTaskGenerator.register("run_doctor")
class RunDoctorGenerator(BaseTaskGenerator):
    """Generate tasks for running diagnostics."""

    required_domains = ("monitoring",)
    difficulty = 1
    parameters = {}

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        yield Pass(), TaskData()

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return "Run the openclaw diagnostic tool to check the system health."

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return ["openclaw doctor"]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "output",
                "match_type": "contains",
                "expected": "doctor",
                "output_field": "last_stdout",
                "name": "doctor output shown",
                "ignore_case": True,
            }
        ]


@BaseTaskGenerator.register("start_gateway_and_check")
class StartGatewayAndCheckGenerator(BaseTaskGenerator):
    """Multi-step: start gateway then verify it's running."""

    required_domains = ("monitoring",)
    difficulty = 2
    parameters = {}

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        yield Pass(), TaskData()

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            "Start the openclaw gateway, then verify it is running by checking "
            "the system health."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return [
            "openclaw gateway start",
            "openclaw health",
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "state",
                "field": "gateway_status.running",
                "condition": "equals",
                "expected": True,
                "name": "gateway is running",
            },
            {
                "type": "output",
                "match_type": "contains",
                "expected": "ok",
                "output_field": "last_stdout",
                "name": "health check passed",
                "ignore_case": True,
            },
        ]


@BaseTaskGenerator.register("diagnose_channel_issue")
class DiagnoseChannelIssueGenerator(BaseTaskGenerator):
    """Reasoning task: diagnose why a channel isn't working."""

    required_domains = ("monitoring", "channel_mgmt")
    difficulty = 3
    parameters = {
        "channel": ["telegram", "discord", "slack"],
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={"channel": params["channel"]},
            private={"root_cause": "channel_not_configured"},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"The {params['channel']} channel is not working. Diagnose the issue "
            f"by checking the system status and channel configuration, then fix it "
            f"by logging into the channel."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return [
            "openclaw status",
            "openclaw channels status --json",
            f"openclaw channels login --channel {params['channel']}",
            "openclaw status",
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "state",
                "field": f"channels.{params['channel']}",
                "condition": "exists",
                "expected": None,
                "name": f"{params['channel']} channel configured",
            },
            {
                "type": "state",
                "field": f"channels.{params['channel']}.status",
                "condition": "equals",
                "expected": "connected",
                "name": f"{params['channel']} connected",
            },
        ]
