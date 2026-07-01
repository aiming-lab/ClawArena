"""HTTP backend for executing raw curl commands.

In real/hybrid modes this backend executes curl as a subprocess so the
trajectory action is the actual HTTP command. In mock/multi mode it returns
deterministic synthetic payloads for known endpoints.
"""

from __future__ import annotations

import json
import shlex
import subprocess
from typing import Any

from openclaw_env.backend.base import BaseBackend, CommandResult


_MOCK_WEATHER_BY_COORD: dict[tuple[str, str], dict[str, Any]] = {
    ("40.7128", "-74.0060"): {
        "time": "2026-03-03T00:45",
        "temperature_2m": 49.1,
        "relative_humidity_2m": 74,
        "weather_code": 61,
    },
    ("51.5074", "-0.1278"): {
        "time": "2026-03-03T05:45",
        "temperature_2m": 43.0,
        "relative_humidity_2m": 82,
        "weather_code": 3,
    },
    ("35.6762", "139.6503"): {
        "time": "2026-03-03T14:45",
        "temperature_2m": 52.0,
        "relative_humidity_2m": 60,
        "weather_code": 2,
    },
    ("48.8566", "2.3522"): {
        "time": "2026-03-03T11:45",
        "temperature_2m": 47.0,
        "relative_humidity_2m": 71,
        "weather_code": 3,
    },
    ("-33.8688", "151.2093"): {
        "time": "2026-03-03T19:45",
        "temperature_2m": 73.0,
        "relative_humidity_2m": 54,
        "weather_code": 1,
    },
}

_MOCK_GEOCODING_BY_NAME: dict[str, dict[str, Any]] = {
    "new york": {
        "id": 5128581,
        "name": "New York",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "timezone": "America/New_York",
        "country": "United States",
    },
    "london": {
        "id": 2643743,
        "name": "London",
        "latitude": 51.5074,
        "longitude": -0.1278,
        "timezone": "Europe/London",
        "country": "United Kingdom",
    },
    "tokyo": {
        "id": 1850144,
        "name": "Tokyo",
        "latitude": 35.6762,
        "longitude": 139.6503,
        "timezone": "Asia/Tokyo",
        "country": "Japan",
    },
    "paris": {
        "id": 2988507,
        "name": "Paris",
        "latitude": 48.8566,
        "longitude": 2.3522,
        "timezone": "Europe/Paris",
        "country": "France",
    },
    "sydney": {
        "id": 2147714,
        "name": "Sydney",
        "latitude": -33.8688,
        "longitude": 151.2093,
        "timezone": "Australia/Sydney",
        "country": "Australia",
    },
}


class HttpBackend(BaseBackend):
    """Execute raw curl commands."""

    def __init__(self, real_http: bool = False) -> None:
        self._real_http = real_http
        self._initialized = False

    def initialize(self, state_dir: str, env_vars: dict[str, str]) -> None:
        self._initialized = True

    def execute_cli(self, command: str) -> CommandResult:
        if not self._initialized:
            return CommandResult(stdout="", stderr="Backend not initialized", exit_code=1)

        try:
            parts = shlex.split(command)
        except ValueError as e:
            return CommandResult(stdout="", stderr=f"Invalid command syntax: {e}", exit_code=1)

        if not parts or parts[0] != "curl":
            return CommandResult(stdout="", stderr="Only curl commands are supported", exit_code=1)

        if self._real_http:
            return self._run_real_curl(parts)
        return self._run_mock_curl(parts)

    def execute_python(self, code: str) -> CommandResult:
        return CommandResult(stdout="", stderr="Python execution not supported", exit_code=1)

    def get_gateway_status(self) -> dict[str, Any] | None:
        return None

    def get_config(self) -> dict[str, Any]:
        return {}

    def cleanup(self) -> None:
        self._initialized = False

    def _run_real_curl(self, parts: list[str]) -> CommandResult:
        try:
            proc = subprocess.run(parts, capture_output=True, text=True, timeout=10)
            return CommandResult(
                stdout=proc.stdout or "",
                stderr=proc.stderr or "",
                exit_code=proc.returncode,
                meta={"http_mode": "real"},
            )
        except FileNotFoundError:
            return CommandResult(
                stdout="",
                stderr="curl not found in PATH",
                exit_code=127,
                meta={"http_mode": "real", "error_tags": ["command_not_found"]},
            )
        except subprocess.TimeoutExpired:
            return CommandResult(
                stdout="",
                stderr="curl command timed out",
                exit_code=124,
                meta={"http_mode": "real", "error_tags": ["timeout"]},
            )

    def _run_mock_curl(self, parts: list[str]) -> CommandResult:
        url = ""
        query: dict[str, str] = {}
        i = 1
        while i < len(parts):
            token = parts[i]
            if token.startswith("http://") or token.startswith("https://"):
                url = token
            elif token == "--data-urlencode" and i + 1 < len(parts):
                raw = parts[i + 1]
                if "=" in raw:
                    k, v = raw.split("=", 1)
                    query[k] = v
                i += 1
            i += 1

        if "api.open-meteo.com/v1/forecast" in url:
            lat = query.get("latitude", "")
            lon = query.get("longitude", "")
            timezone = query.get("timezone", "UTC")
            weather = _MOCK_WEATHER_BY_COORD.get(
                (lat, lon),
                {
                    "time": "2026-03-03T00:45",
                    "temperature_2m": 50.0,
                    "relative_humidity_2m": 70,
                    "weather_code": 0,
                },
            )
            payload = {
                "latitude": float(lat) if lat else 0.0,
                "longitude": float(lon) if lon else 0.0,
                "timezone": timezone,
            }
            if "current" in query:
                payload["current"] = weather
            if "daily" in query:
                try:
                    days = max(1, min(16, int(query.get("forecast_days", "3"))))
                except ValueError:
                    days = 3
                from datetime import date, timedelta
                base_date = date(2026, 3, 3)
                daily_times = [
                    (base_date + timedelta(days=i)).isoformat()
                    for i in range(days)
                ]
                # Keep deterministic shape in mock mode with repeated values.
                payload["daily"] = {
                    "time": daily_times,
                    "weather_code": [int(weather.get("weather_code", 0))] * days,
                    "temperature_2m_max": [round(float(weather.get("temperature_2m", 50.0)) + 2.0, 1)] * days,
                    "temperature_2m_min": [round(float(weather.get("temperature_2m", 50.0)) - 3.0, 1)] * days,
                    "precipitation_sum": [2.1] * days,
                    "wind_speed_10m_max": [18.0] * days,
                }
            return CommandResult(
                stdout=json.dumps(payload, ensure_ascii=False),
                stderr="",
                exit_code=0,
                meta={"http_mode": "mock"},
            )

        if "archive-api.open-meteo.com/v1/archive" in url:
            lat = query.get("latitude", "")
            lon = query.get("longitude", "")
            start_date = query.get("start_date", "2026-03-01")
            end_date = query.get("end_date", start_date)
            timezone = query.get("timezone", "UTC")
            weather = _MOCK_WEATHER_BY_COORD.get(
                (lat, lon),
                {
                    "temperature_2m": 50.0,
                    "weather_code": 0,
                },
            )
            base_temp = float(weather.get("temperature_2m", 50.0))
            payload = {
                "latitude": float(lat) if lat else 0.0,
                "longitude": float(lon) if lon else 0.0,
                "timezone": timezone,
                "daily": {
                    "time": [start_date] if start_date == end_date else [start_date, end_date],
                    "weather_code": [int(weather.get("weather_code", 0))],
                    "temperature_2m_max": [round(base_temp + 2.0, 1)],
                    "temperature_2m_min": [round(base_temp - 3.0, 1)],
                },
            }
            return CommandResult(
                stdout=json.dumps(payload, ensure_ascii=False),
                stderr="",
                exit_code=0,
                meta={"http_mode": "mock"},
            )

        if "geocoding-api.open-meteo.com/v1/search" in url:
            name = (query.get("name", "") or "").strip().lower()
            result = _MOCK_GEOCODING_BY_NAME.get(name)
            if result is None:
                payload = {"results": []}
            else:
                payload = {"results": [result]}
            return CommandResult(
                stdout=json.dumps(payload, ensure_ascii=False),
                stderr="",
                exit_code=0,
                meta={"http_mode": "mock"},
            )

        if "timeapi.io/api/Time/current/zone" in url:
            tz = query.get("timeZone", "UTC")
            payload = {
                "year": 2026,
                "month": 3,
                "day": 3,
                "hour": 5,
                "minute": 26,
                "seconds": 32,
                "dateTime": "2026-03-03T05:26:32.0144639",
                "timeZone": tz,
                "dayOfWeek": "Tuesday",
                "dstActive": False,
            }
            return CommandResult(
                stdout=json.dumps(payload, ensure_ascii=False),
                stderr="",
                exit_code=0,
                meta={"http_mode": "mock"},
            )

        return CommandResult(
            stdout="",
            stderr=f"Unsupported curl endpoint in mock mode: {url or '(missing URL)'}",
            exit_code=1,
            meta={"http_mode": "mock", "error_tags": ["unsupported_curl_endpoint"]},
        )
