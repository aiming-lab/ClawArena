"""Task generators for online-read tasks using weather/calendar backends."""

from __future__ import annotations

from typing import Any, Iterator

from openclaw_env.core.task import TaskData
from openclaw_env.tasks.generation_options import get_generation_options
from openclaw_env.tasks.generators.weather_tasks import (
    build_universal_weather_current_commands,
)
from openclaw_env.tasks.registry import BaseTaskGenerator, Pass, SetupResult

_ONLINE_LOCATIONS = ["New York", "London", "Tokyo"]
_ONLINE_TIMEZONES = ["UTC", "America/New_York", "Europe/London"]


def _is_universal_profile() -> bool:
    return get_generation_options().command_profile == "universal"


def _calendar_online_command(timezone: str) -> str:
    if _is_universal_profile():
        return f"gcalcli now --timezone {timezone}"
    return f"calendar today --timezone {timezone}"


@BaseTaskGenerator.register("openclaw_online_weather_read")
class OpenClawOnlineWeatherReadGenerator(BaseTaskGenerator):
    """Read live weather with either local-skill or universal online path."""

    required_domains = ("weather",)
    difficulty = 2
    parameters = {
        "location": _ONLINE_LOCATIONS,
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={"location": params["location"]},
            private={},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"I'm traveling soon and need a live weather check for {params['location']}. "
            "Please fetch the latest conditions and summarize them clearly."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        if _is_universal_profile():
            return build_universal_weather_current_commands(params["location"])
        return [f"weather get --location '{params['location']}'"]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        if _is_universal_profile():
            return [
                {
                    "type": "output",
                    "condition": "exit_code_zero",
                    "expected": None,
                    "name": "weather get online succeeds",
                },
                {
                    "type": "output",
                    "condition": "contains",
                    "expected": '"current"',
                    "name": "output contains current weather object",
                },
                {
                    "type": "output",
                    "condition": "contains",
                    "expected": '"temperature_2m"',
                    "name": "output contains temperature field",
                },
            ]

        return [
            {
                "type": "output",
                "condition": "exit_code_zero",
                "expected": None,
                "name": "weather get online succeeds",
            },
            {
                "type": "output",
                "condition": "contains",
                "expected": f"Weather for {params['location']}",
                "name": "output includes location",
            },
            {
                "type": "output",
                "condition": "contains",
                "expected": "Source",
                "name": "output includes data source",
            },
        ]


@BaseTaskGenerator.register("openclaw_online_calendar_read")
class OpenClawOnlineCalendarReadGenerator(BaseTaskGenerator):
    """Read live date/time with either local-skill or universal calendar path."""

    required_domains = ("calendar",)
    difficulty = 2
    parameters = {
        "timezone": _ONLINE_TIMEZONES,
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={"timezone": params["timezone"]},
            private={},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"I need the current date and time in {params['timezone']} right now. "
            "Please fetch it and give a concise summary."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return [_calendar_online_command(params["timezone"])]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "output",
                "condition": "exit_code_zero",
                "expected": None,
                "name": "calendar today online succeeds",
            },
            {
                "type": "output",
                "condition": "contains",
                "expected": f"Current date-time for {params['timezone']}:",
                "name": "output contains requested timezone",
            },
            {
                "type": "output",
                "condition": "contains",
                "expected": "Source:",
                "name": "output includes data source",
            },
        ]
