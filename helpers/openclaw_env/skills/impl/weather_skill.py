"""Weather skill implementation (local mock + optional online fetch)."""

from __future__ import annotations

import datetime as dt
import json
import shlex
import subprocess
from typing import Any

from openclaw_env.backend.base import CommandResult
from openclaw_env.skills.base import Skill


def _get_arg(args: list[str], flag: str, default: str | None = None) -> str | None:
    for i, a in enumerate(args):
        if a == flag and i + 1 < len(args):
            return args[i + 1]
    return default


def _get_flag(args: list[str], flag: str) -> bool:
    return flag in args


_WEATHER_SCENARIOS: dict[tuple[str, str], dict[str, Any]] = {
    ("new york", "2026-03-01"): {"condition": "rainy", "temp_c": 8, "humidity": 85},
    ("new york", "2026-03-02"): {"condition": "cloudy", "temp_c": 10, "humidity": 70},
    ("new york", "2026-03-03"): {"condition": "sunny", "temp_c": 14, "humidity": 50},
    ("london", "2026-03-01"): {"condition": "rainy", "temp_c": 6, "humidity": 90},
    ("london", "2026-03-02"): {"condition": "rainy", "temp_c": 7, "humidity": 88},
    ("london", "2026-03-03"): {"condition": "cloudy", "temp_c": 9, "humidity": 75},
    ("tokyo", "2026-03-01"): {"condition": "sunny", "temp_c": 12, "humidity": 55},
    ("tokyo", "2026-03-02"): {"condition": "sunny", "temp_c": 15, "humidity": 50},
    ("tokyo", "2026-03-03"): {"condition": "partly cloudy", "temp_c": 13, "humidity": 60},
    ("paris", "2026-03-01"): {"condition": "cloudy", "temp_c": 9, "humidity": 72},
    ("paris", "2026-03-02"): {"condition": "rainy", "temp_c": 8, "humidity": 80},
    ("paris", "2026-03-03"): {"condition": "sunny", "temp_c": 12, "humidity": 55},
    ("sydney", "2026-03-01"): {"condition": "sunny", "temp_c": 25, "humidity": 45},
    ("sydney", "2026-03-02"): {"condition": "sunny", "temp_c": 27, "humidity": 42},
    ("sydney", "2026-03-03"): {"condition": "partly cloudy", "temp_c": 24, "humidity": 50},
}

_DEFAULT_TODAY = "2026-03-01"

_ALERTS: dict[str, list[str]] = {
    "new york": ["Heavy rain warning for 2026-03-01"],
    "london": ["Flood watch in effect 2026-03-01 through 2026-03-02"],
    "tokyo": [],
    "paris": [],
    "sydney": [],
}

_WEATHER_CODE_TO_TEXT: dict[int, str] = {
    0: "clear",
    1: "mainly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "fog",
    48: "rime fog",
    51: "drizzle",
    53: "drizzle",
    55: "drizzle",
    61: "rainy",
    63: "rainy",
    65: "heavy rain",
    71: "snow",
    73: "snow",
    75: "heavy snow",
    80: "rain showers",
    81: "rain showers",
    82: "heavy rain showers",
    95: "thunderstorm",
}

_LAST_WEATHER_TRACE: list[dict[str, Any]] = []
_PLACEHOLDER_VALUES = {"TIMEZONE", "LOCATION", "TITLE", "DATETIME", "DATE", "NAME", "SCHEDULE", "QUERY", "N"}


def _looks_like_placeholder(value: str) -> bool:
    normalized = value.strip().strip("`'\"[](){}.,:;")
    return normalized in _PLACEHOLDER_VALUES


class WeatherSkill(Skill):
    """Weather skill with deterministic mock responses and optional live data."""

    def __init__(self) -> None:
        super().__init__(prefixes=("weather",))
        self._initialized = False
        self._enable_online_data = False
        self._strict_online_data = False

    def initialize(self, state_dir: str, env_vars: dict[str, str]) -> None:
        del state_dir
        self._initialized = True
        val = str(env_vars.get("OPENCLAW_ENV_ENABLE_ONLINE_DATA", "")).lower()
        self._enable_online_data = val in {"1", "true", "yes", "on"}
        strict_val = str(env_vars.get("OPENCLAW_ENV_STRICT_ONLINE_DATA", "")).lower()
        self._strict_online_data = strict_val in {"1", "true", "yes", "on"}

    def execute(self, command: str) -> CommandResult:
        parts = shlex.split(command.strip())
        if not parts or parts[0] != "weather":
            return CommandResult(stdout="", stderr="Not a weather command", exit_code=1)

        if len(parts) < 2:
            return CommandResult(
                stdout="weather <subcommand> [options]\nSubcommands: get, forecast, alerts",
                stderr="",
                exit_code=0,
            )

        sub = parts[1]
        args = parts[2:]

        handlers = {
            "get": self._cmd_get,
            "forecast": self._cmd_forecast,
            "alerts": self._cmd_alerts,
        }

        handler = handlers.get(sub)
        if handler is None:
            return CommandResult(stdout="", stderr=f"Unknown weather subcommand: {sub}", exit_code=1)
        return handler(args)

    def cleanup(self) -> None:
        self._initialized = False

    def get_state(self) -> dict[str, Any]:
        return {}

    def _cmd_get(self, args: list[str]) -> CommandResult:
        location = _get_arg(args, "--location")
        explicit_date = _get_arg(args, "--date")
        use_online = _get_flag(args, "--online") or self._enable_online_data

        if not location:
            return CommandResult(stdout="", stderr="--location is required", exit_code=1)
        if _looks_like_placeholder(location):
            return CommandResult(stdout="", stderr=f"Invalid location value: {location}", exit_code=1)

        if explicit_date:
            date = explicit_date
        elif use_online and self._enable_online_data:
            date = _online_today_date()
        else:
            date = _DEFAULT_TODAY

        source = "mock"
        weather_data: dict[str, Any] | None = None
        execution_trace: list[dict[str, Any]] = []
        if use_online and self._enable_online_data:
            _clear_last_weather_trace()
            weather_data = _get_weather_online(location, date)
            execution_trace = _consume_last_weather_trace()
            if weather_data is not None:
                source = "online"

        if weather_data is None:
            if use_online and self._enable_online_data and self._strict_online_data:
                return CommandResult(
                    stdout="",
                    stderr=(
                        f"Online weather data unavailable for {location} on {date}. "
                        "Strict online mode is enabled, so mock fallback is disabled."
                    ),
                    exit_code=1,
                )
            weather_data = _get_weather(location, date)
            if use_online and self._enable_online_data:
                source = "mock-fallback"

        return CommandResult(
            stdout=(
                f"Weather for {location} on {date}:\n"
                f"  Condition : {weather_data['condition']}\n"
                f"  Temp      : {weather_data['temp_c']}°C\n"
                f"  Humidity  : {weather_data['humidity']}%\n"
                f"  Source    : {source}"
            ),
            stderr="",
            exit_code=0,
            execution_trace=execution_trace or None,
        )

    def _cmd_forecast(self, args: list[str]) -> CommandResult:
        location = _get_arg(args, "--location")
        days_str = _get_arg(args, "--days", "3")

        if not location:
            return CommandResult(stdout="", stderr="--location is required", exit_code=1)
        if _looks_like_placeholder(location):
            return CommandResult(stdout="", stderr=f"Invalid location value: {location}", exit_code=1)
        if days_str and _looks_like_placeholder(days_str):
            return CommandResult(stdout="", stderr=f"Invalid --days value: {days_str}", exit_code=1)

        try:
            days = int(days_str)
        except (ValueError, TypeError):
            days = 3

        base = dt.date(2026, 3, 1)
        lines = [f"{days}-day forecast for {location}:"]
        for i in range(days):
            day = (base + dt.timedelta(days=i)).isoformat()
            weather_data = _get_weather(location, day)
            lines.append(
                f"  {day}: {weather_data['condition']}, {weather_data['temp_c']}°C, {weather_data['humidity']}% humidity"
            )

        return CommandResult(stdout="\n".join(lines), stderr="", exit_code=0)

    def _cmd_alerts(self, args: list[str]) -> CommandResult:
        location = _get_arg(args, "--location")

        if not location:
            return CommandResult(stdout="", stderr="--location is required", exit_code=1)

        alerts = _ALERTS.get(location.lower(), [])
        if not alerts:
            return CommandResult(
                stdout=f"No active weather alerts for {location}.", stderr="", exit_code=0
            )

        lines = [f"Weather alerts for {location}:"]
        for alert in alerts:
            lines.append(f"  ⚠ {alert}")
        return CommandResult(stdout="\n".join(lines), stderr="", exit_code=0)


def _hash_weather(location: str, date: str) -> dict[str, Any]:
    h = sum(ord(c) for c in location + date)
    conditions = ["sunny", "cloudy", "rainy", "partly cloudy"]
    condition = conditions[h % len(conditions)]
    temp_c = 5 + (h % 25)
    humidity = 40 + (h % 50)
    return {"condition": condition, "temp_c": temp_c, "humidity": humidity}


def _get_weather(location: str, date: str) -> dict[str, Any]:
    key = (location.lower(), date)
    if key in _WEATHER_SCENARIOS:
        return _WEATHER_SCENARIOS[key]
    return _hash_weather(location, date)


def _online_today_date() -> str:
    return dt.datetime.now(dt.timezone.utc).date().isoformat()


def _get_weather_online(location: str, date: str) -> dict[str, Any] | None:
    trace: list[dict[str, Any]] = []
    try:
        geo_cmd = [
            "curl",
            "-sG",
            "https://geocoding-api.open-meteo.com/v1/search",
            "--data-urlencode",
            f"name={location}",
            "--data-urlencode",
            "count=1",
            "--data-urlencode",
            "language=en",
            "--data-urlencode",
            "format=json",
        ]
        geo = _run_json_cli(geo_cmd, timeout=6, trace=trace)
        results = geo.get("results") if isinstance(geo, dict) else None
        if not isinstance(results, list) or not results:
            _set_last_weather_trace(trace)
            return None
        top = results[0] if isinstance(results[0], dict) else {}
        lat = top.get("latitude")
        lon = top.get("longitude")
        timezone = str(top.get("timezone") or "UTC")
        if lat is None or lon is None:
            _set_last_weather_trace(trace)
            return None

        # Keep a real time lookup step in the online chain for richer traces.
        time_cmd = [
            "curl",
            "-sG",
            "https://timeapi.io/api/Time/current/zone",
            "--data-urlencode",
            f"timeZone={timezone}",
        ]
        _run_json_cli(time_cmd, timeout=6, trace=trace, required=False)

        if date == _online_today_date():
            weather_cmd = [
                "curl",
                "-sG",
                "https://api.open-meteo.com/v1/forecast",
                "--data-urlencode",
                f"latitude={lat}",
                "--data-urlencode",
                f"longitude={lon}",
                "--data-urlencode",
                "current=temperature_2m,relative_humidity_2m,weather_code",
                "--data-urlencode",
                f"timezone={timezone}",
            ]
            payload = _run_json_cli(weather_cmd, timeout=8, trace=trace)
            current = payload.get("current") if isinstance(payload, dict) else None
            if not isinstance(current, dict):
                _set_last_weather_trace(trace)
                return None
            code = current.get("weather_code")
            temp = current.get("temperature_2m")
            humidity = current.get("relative_humidity_2m")
            if code is None or temp is None:
                _set_last_weather_trace(trace)
                return None
            result = {
                "condition": _WEATHER_CODE_TO_TEXT.get(int(code), "unknown"),
                "temp_c": round(float(temp)),
                "humidity": int(humidity) if humidity is not None else 55,
            }
            _set_last_weather_trace(trace)
            return result

        weather_cmd = [
            "curl",
            "-sG",
            "https://archive-api.open-meteo.com/v1/archive",
            "--data-urlencode",
            f"latitude={lat}",
            "--data-urlencode",
            f"longitude={lon}",
            "--data-urlencode",
            f"start_date={date}",
            "--data-urlencode",
            f"end_date={date}",
            "--data-urlencode",
            "daily=weather_code,temperature_2m_max,temperature_2m_min",
            "--data-urlencode",
            f"timezone={timezone}",
        ]
        payload = _run_json_cli(weather_cmd, timeout=8, trace=trace)
        daily = payload.get("daily") if isinstance(payload, dict) else None
        if not isinstance(daily, dict):
            _set_last_weather_trace(trace)
            return None
        code_list = daily.get("weather_code")
        tmax_list = daily.get("temperature_2m_max")
        tmin_list = daily.get("temperature_2m_min")
        if not (isinstance(code_list, list) and code_list):
            _set_last_weather_trace(trace)
            return None
        code = int(code_list[0])
        tmax = float(tmax_list[0]) if isinstance(tmax_list, list) and tmax_list else 0.0
        tmin = float(tmin_list[0]) if isinstance(tmin_list, list) and tmin_list else tmax
        result = {
            "condition": _WEATHER_CODE_TO_TEXT.get(code, "unknown"),
            "temp_c": round((tmax + tmin) / 2),
            "humidity": 55,
        }
        _set_last_weather_trace(trace)
        return result
    except Exception:
        _set_last_weather_trace(trace)
        return None


def _run_json_cli(
    cmd: list[str],
    *,
    timeout: int,
    trace: list[dict[str, Any]],
    required: bool = True,
) -> dict[str, Any]:
    rc, stdout, stderr = _run_command(cmd, timeout=timeout)
    trace.append(
        {
            "action": shlex.join(cmd),
            "stdout": stdout,
            "stderr": stderr,
            "exit_code": rc,
        }
    )
    if rc != 0:
        if required:
            raise RuntimeError(stderr or f"command failed: {shlex.join(cmd)}")
        return {}
    payload = json.loads((stdout or "").strip() or "{}")
    return payload if isinstance(payload, dict) else {}


def _run_command(cmd: list[str], *, timeout: int) -> tuple[int, str, str]:
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return proc.returncode, proc.stdout or "", proc.stderr or ""
    except Exception as exc:  # pragma: no cover
        return 1, "", str(exc)


def _set_last_weather_trace(trace: list[dict[str, Any]]) -> None:
    global _LAST_WEATHER_TRACE
    _LAST_WEATHER_TRACE = list(trace)


def _consume_last_weather_trace() -> list[dict[str, Any]]:
    global _LAST_WEATHER_TRACE
    value = list(_LAST_WEATHER_TRACE)
    _LAST_WEATHER_TRACE = []
    return value


def _clear_last_weather_trace() -> None:
    global _LAST_WEATHER_TRACE
    _LAST_WEATHER_TRACE = []
