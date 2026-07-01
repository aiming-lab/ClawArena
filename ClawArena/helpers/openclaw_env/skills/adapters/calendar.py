"""Calendar skill adapter."""

from __future__ import annotations

from openclaw_env.backend.calendar_backend import CalendarBackend
from openclaw_env.skills.base import BackendSkillAdapter


class CalendarSkillAdapter(BackendSkillAdapter):
    def __init__(self, backend: CalendarBackend) -> None:
        super().__init__(backend, prefixes=("calendar", "gcalcli"))
