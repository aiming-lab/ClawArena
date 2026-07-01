"""Task generators for Device & Node domain (D9)."""

from __future__ import annotations

from typing import Any, Iterator

from openclaw_env.core.task import TaskData
from openclaw_env.tasks.registry import BaseTaskGenerator, Pass, SetupResult


@BaseTaskGenerator.register("pair_device")
class PairDeviceGenerator(BaseTaskGenerator):
    """Initiate device pairing."""

    required_domains = ("device_node",)
    difficulty = 1
    parameters = {}

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        yield Pass(), TaskData()

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return "Initiate device pairing to connect a new device to openclaw."

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return ["openclaw devices pair"]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "output",
                "match_type": "contains",
                "expected": "pairing",
                "output_field": "last_stdout",
                "name": "device pairing initiated",
                "ignore_case": True,
            }
        ]


@BaseTaskGenerator.register("list_devices")
class ListDevicesGenerator(BaseTaskGenerator):
    """List all paired devices."""

    required_domains = ("device_node",)
    difficulty = 1
    parameters = {}

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        yield Pass(), TaskData()

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return "List all devices currently paired with openclaw."

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return ["openclaw devices list"]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "output",
                "match_type": "regex",
                "expected": r"(device|Device|No devices|paired)",
                "output_field": "last_stdout",
                "name": "devices listed",
                "ignore_case": True,
            }
        ]


@BaseTaskGenerator.register("pair_and_list_devices")
class PairAndListDevicesGenerator(BaseTaskGenerator):
    """Multi-step: pair a device and list devices to verify."""

    required_domains = ("device_node",)
    difficulty = 2
    parameters = {}

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        yield Pass(), TaskData()

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            "Initiate device pairing to connect a new device, "
            "then list all paired devices to verify the pairing process started."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return [
            "openclaw devices pair",
            "openclaw devices list",
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "output",
                "match_type": "regex",
                "expected": r"(device|Device|No devices|paired)",
                "output_field": "last_stdout",
                "name": "devices listed after pairing",
                "ignore_case": True,
            }
        ]
