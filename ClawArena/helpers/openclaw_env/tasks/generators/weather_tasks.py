"""Task generators for Weather domain (D13)."""

from __future__ import annotations

from typing import Any, Iterator

from openclaw_env.core.task import TaskData
from openclaw_env.tasks.generation_options import get_generation_options
from openclaw_env.tasks.registry import BaseTaskGenerator, Pass, SetupResult

_LOCATIONS = ["New York", "London", "Tokyo", "Paris", "Sydney"]
_DATES = ["2026-03-01", "2026-03-02", "2026-03-03"]
_FORECAST_DAYS = [3, 5, 7]
_ONLINE_LOCATION_COORDS = {
    "New York": ("40.7128", "-74.0060", "America/New_York"),
    "London": ("51.5074", "-0.1278", "Europe/London"),
    "Tokyo": ("35.6762", "139.6503", "Asia/Tokyo"),
    "Paris": ("48.8566", "2.3522", "Europe/Paris"),
    "Sydney": ("-33.8688", "151.2093", "Australia/Sydney"),
}


def _is_universal_profile() -> bool:
    return get_generation_options().command_profile == "universal"


def build_universal_weather_current_commands(location: str) -> list[str]:
    lat, lon, timezone = _ONLINE_LOCATION_COORDS[location]
    return [
        'curl -sG "https://geocoding-api.open-meteo.com/v1/search" '
        f'--data-urlencode "name={location}" '
        '--data-urlencode "count=1" '
        '--data-urlencode "language=en" '
        '--data-urlencode "format=json"',
        'curl -sG "https://timeapi.io/api/Time/current/zone" '
        f'--data-urlencode "timeZone={timezone}"',
        'curl -sG "https://api.open-meteo.com/v1/forecast" '
        f'--data-urlencode "latitude={lat}" '
        f'--data-urlencode "longitude={lon}" '
        '--data-urlencode "current=temperature_2m,relative_humidity_2m,weather_code" '
        f'--data-urlencode "timezone={timezone}"',
    ]


def build_universal_weather_on_date_commands(location: str, date: str) -> list[str]:
    lat, lon, timezone = _ONLINE_LOCATION_COORDS[location]
    return [
        'curl -sG "https://geocoding-api.open-meteo.com/v1/search" '
        f'--data-urlencode "name={location}" '
        '--data-urlencode "count=1" '
        '--data-urlencode "language=en" '
        '--data-urlencode "format=json"',
        'curl -sG "https://timeapi.io/api/Time/current/zone" '
        f'--data-urlencode "timeZone={timezone}"',
        'curl -sG "https://archive-api.open-meteo.com/v1/archive" '
        f'--data-urlencode "latitude={lat}" '
        f'--data-urlencode "longitude={lon}" '
        f'--data-urlencode "start_date={date}" '
        f'--data-urlencode "end_date={date}" '
        '--data-urlencode "daily=weather_code,temperature_2m_max,temperature_2m_min" '
        f'--data-urlencode "timezone={timezone}"',
    ]


def build_universal_weather_forecast_commands(location: str, days: int) -> list[str]:
    lat, lon, timezone = _ONLINE_LOCATION_COORDS[location]
    return [
        'curl -sG "https://geocoding-api.open-meteo.com/v1/search" '
        f'--data-urlencode "name={location}" '
        '--data-urlencode "count=1" '
        '--data-urlencode "language=en" '
        '--data-urlencode "format=json"',
        'curl -sG "https://timeapi.io/api/Time/current/zone" '
        f'--data-urlencode "timeZone={timezone}"',
        'curl -sG "https://api.open-meteo.com/v1/forecast" '
        f'--data-urlencode "latitude={lat}" '
        f'--data-urlencode "longitude={lon}" '
        '--data-urlencode "daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum" '
        f'--data-urlencode "forecast_days={days}" '
        f'--data-urlencode "timezone={timezone}"',
    ]


def build_universal_weather_alert_check_commands(location: str) -> list[str]:
    lat, lon, timezone = _ONLINE_LOCATION_COORDS[location]
    return [
        'curl -sG "https://geocoding-api.open-meteo.com/v1/search" '
        f'--data-urlencode "name={location}" '
        '--data-urlencode "count=1" '
        '--data-urlencode "language=en" '
        '--data-urlencode "format=json"',
        'curl -sG "https://timeapi.io/api/Time/current/zone" '
        f'--data-urlencode "timeZone={timezone}"',
        'curl -sG "https://api.open-meteo.com/v1/forecast" '
        f'--data-urlencode "latitude={lat}" '
        f'--data-urlencode "longitude={lon}" '
        '--data-urlencode "daily=weather_code,precipitation_sum,wind_speed_10m_max" '
        '--data-urlencode "forecast_days=2" '
        f'--data-urlencode "timezone={timezone}"',
    ]


def _local_weather_current_commands(location: str) -> list[str]:
    return [f"weather get --location '{location}'"]


def _local_weather_on_date_commands(location: str, date: str) -> list[str]:
    return [f"weather get --location '{location}' --date {date}"]


def _local_weather_forecast_commands(location: str, days: int) -> list[str]:
    return [f"weather forecast --location '{location}' --days {days}"]


def _local_weather_alert_check_commands(location: str) -> list[str]:
    return [f"weather alerts --location '{location}'"]


def _local_weather_online_commands(location: str) -> list[str]:
    return [f"weather get --location '{location}'"]


def _weather_current_checks(location: str) -> list[dict[str, Any]]:
    if _is_universal_profile():
        return [
            {
                "type": "output",
                "condition": "exit_code_zero",
                "expected": None,
                "name": "weather get succeeds",
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
            "name": "weather get succeeds",
        },
        {
            "type": "output",
            "condition": "contains",
            "expected": f"Weather for {location}",
            "name": "output contains location weather line",
        },
        {
            "type": "output",
            "condition": "contains",
            "expected": "Condition",
            "name": "output contains condition field",
        },
    ]


def _weather_on_date_checks(date: str) -> list[dict[str, Any]]:
    if _is_universal_profile():
        return [
            {
                "type": "output",
                "condition": "exit_code_zero",
                "expected": None,
                "name": "weather get on date succeeds",
            },
            {
                "type": "output",
                "condition": "contains",
                "expected": '"daily"',
                "name": "output contains daily weather data",
            },
            {
                "type": "output",
                "condition": "contains",
                "expected": date,
                "name": "output includes requested date",
            },
        ]
    return [
        {
            "type": "output",
            "condition": "exit_code_zero",
            "expected": None,
            "name": "weather get on date succeeds",
        },
        {
            "type": "output",
            "condition": "contains",
            "expected": date,
            "name": "output includes requested date",
        },
        {
            "type": "output",
            "condition": "contains",
            "expected": "Condition",
            "name": "output contains condition field",
        },
    ]


def _weather_forecast_checks(location: str, days: int) -> list[dict[str, Any]]:
    if _is_universal_profile():
        return [
            {
                "type": "output",
                "condition": "exit_code_zero",
                "expected": None,
                "name": "forecast succeeds",
            },
            {
                "type": "output",
                "condition": "contains",
                "expected": '"daily"',
                "name": "output contains daily forecast object",
            },
            {
                "type": "output",
                "condition": "contains",
                "expected": '"temperature_2m_max"',
                "name": "output contains max temperature field",
            },
        ]
    return [
        {
            "type": "output",
            "condition": "exit_code_zero",
            "expected": None,
            "name": "forecast succeeds",
        },
        {
            "type": "output",
            "condition": "contains",
            "expected": f"{days}-day forecast for {location}",
            "name": "output contains forecast summary line",
        },
        {
            "type": "output",
            "condition": "contains",
            "expected": "humidity",
            "name": "output includes humidity values",
        },
    ]


def _weather_alert_checks(location: str) -> list[dict[str, Any]]:
    if _is_universal_profile():
        return [
            {
                "type": "output",
                "condition": "exit_code_zero",
                "expected": None,
                "name": "alerts check succeeds",
            },
            {
                "type": "output",
                "condition": "contains",
                "expected": '"daily"',
                "name": "output contains weather daily block for alert analysis",
            },
            {
                "type": "output",
                "condition": "contains",
                "expected": '"wind_speed_10m_max"',
                "name": "output includes wind severity signal",
            },
        ]
    return [
        {
            "type": "output",
            "condition": "exit_code_zero",
            "expected": None,
            "name": "alerts check succeeds",
        },
        {
            "type": "output",
            "condition": "contains",
            "expected": location,
            "name": "output references requested location",
        },
    ]


def _weather_online_checks(location: str) -> list[dict[str, Any]]:
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
            "expected": f"Weather for {location}",
            "name": "output contains location weather line",
        },
        {
            "type": "output",
            "condition": "contains",
            "expected": "Source",
            "name": "output includes data source",
        },
    ]


@BaseTaskGenerator.register("weather_get")
class GetWeatherGenerator(BaseTaskGenerator):
    """Get current weather for a location."""

    required_domains = ("weather",)
    difficulty = 1
    parameters = {
        "location": _LOCATIONS,
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={"location": params["location"]},
            private={"expected_location": params["location"]},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return f"I'm heading out soon. What's the weather like right now in {params['location']}?"

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        if _is_universal_profile():
            return build_universal_weather_current_commands(params["location"])
        return _local_weather_current_commands(params["location"])

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return _weather_current_checks(params["location"])


@BaseTaskGenerator.register("weather_get_on_date")
class GetWeatherOnDateGenerator(BaseTaskGenerator):
    """Get weather for a specific location and date."""

    required_domains = ("weather",)
    difficulty = 1
    parameters = {
        "location": _LOCATIONS[:3],
        "date": _DATES,
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={"location": params["location"], "date": params["date"]},
            private={},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"I have plans in {params['location']} on {params['date']}. "
            f"What will the weather be like that day?"
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        if _is_universal_profile():
            return build_universal_weather_on_date_commands(
                params["location"],
                params["date"],
            )
        return _local_weather_on_date_commands(params["location"], params["date"])

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return _weather_on_date_checks(params["date"])


@BaseTaskGenerator.register("weather_forecast")
class GetForecastGenerator(BaseTaskGenerator):
    """Get a multi-day forecast for a location."""

    required_domains = ("weather",)
    difficulty = 1
    parameters = {
        "location": _LOCATIONS,
        "days": _FORECAST_DAYS,
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={"location": params["location"], "days": params["days"]},
            private={},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"I need to plan my week. "
            f"Pull up a {params['days']}-day weather forecast for {params['location']}."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        if _is_universal_profile():
            return build_universal_weather_forecast_commands(
                params["location"],
                params["days"],
            )
        return _local_weather_forecast_commands(params["location"], params["days"])

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return _weather_forecast_checks(params["location"], params["days"])


@BaseTaskGenerator.register("weather_check_alerts")
class CheckWeatherAlertsGenerator(BaseTaskGenerator):
    """Check weather alerts for a location."""

    required_domains = ("weather",)
    difficulty = 1
    parameters = {
        "location": _LOCATIONS,
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
        return f"Before I head to {params['location']}, check if there are any active weather alerts there."

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        if _is_universal_profile():
            return build_universal_weather_alert_check_commands(params["location"])
        return _local_weather_alert_check_commands(params["location"])

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return _weather_alert_checks(params["location"])


@BaseTaskGenerator.register("weather_get_online")
class GetWeatherOnlineGenerator(BaseTaskGenerator):
    """Get live weather for a location."""

    required_domains = ("weather",)
    difficulty = 2
    parameters = {
        "location": _LOCATIONS[:3],
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
            f"I'm heading out soon and need a live weather check for {params['location']}. "
            "Please look it up online and summarize the current conditions."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        if _is_universal_profile():
            return build_universal_weather_current_commands(params["location"])
        return _local_weather_online_commands(params["location"])

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return _weather_online_checks(params["location"])
