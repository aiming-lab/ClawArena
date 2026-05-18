"""Compatibility backend wrapper around WeatherSkill."""

from __future__ import annotations

from typing import Any

from openclaw_env.backend.base import BaseBackend, CommandResult
from openclaw_env.skills.impl import weather_skill as weather_skill_mod
from openclaw_env.skills.impl.weather_skill import WeatherSkill

# Re-export helper hooks for backward compatibility with tests/tooling that monkeypatch
# backend module symbols.
_online_today_date = weather_skill_mod._online_today_date
_get_weather_online = weather_skill_mod._get_weather_online


class WeatherBackend(BaseBackend):
    """Compatibility shim; weather logic now lives in WeatherSkill."""

    def __init__(self, skill: WeatherSkill | None = None) -> None:
        self._skill = skill or WeatherSkill()

    def initialize(self, state_dir: str, env_vars: dict[str, str]) -> None:
        self._sync_compat_hooks()
        self._skill.initialize(state_dir, env_vars)

    def execute_cli(self, command: str) -> CommandResult:
        self._sync_compat_hooks()
        return self._skill.execute(command)

    def execute_python(self, code: str) -> CommandResult:
        del code
        return CommandResult(stdout="", stderr="Python interface not supported for WeatherBackend", exit_code=1)

    def get_gateway_status(self) -> dict[str, Any] | None:
        return None

    def get_config(self) -> dict[str, Any]:
        return {}

    def cleanup(self) -> None:
        self._skill.cleanup()

    def get_state(self) -> dict[str, Any]:
        return self._skill.get_state()

    def _sync_compat_hooks(self) -> None:
        weather_skill_mod._online_today_date = _online_today_date
        weather_skill_mod._get_weather_online = _get_weather_online
