"""Weather skill adapter."""

from __future__ import annotations

from openclaw_env.backend.weather_backend import WeatherBackend
from openclaw_env.skills.base import BackendSkillAdapter


class WeatherSkillAdapter(BackendSkillAdapter):
    def __init__(self, backend: WeatherBackend) -> None:
        super().__init__(backend, prefixes=("weather",))
