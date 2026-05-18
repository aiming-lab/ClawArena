"""Compatibility backend wrapper around CalendarSkill."""

from __future__ import annotations

from typing import Any

from openclaw_env.backend.base import BaseBackend, CommandResult
from openclaw_env.skills.impl import calendar_skill as calendar_skill_mod
from openclaw_env.skills.impl.calendar_skill import CalendarSkill

# Re-export helper hooks for backward compatibility with tests/tooling that monkeypatch
# backend module symbols.
_get_online_time = calendar_skill_mod._get_online_time
_resolve_calendar_provider = calendar_skill_mod._resolve_calendar_provider
_run_calendar_provider_command = calendar_skill_mod._run_calendar_provider_command


class CalendarBackend(BaseBackend):
    """Compatibility shim; calendar logic now lives in CalendarSkill."""

    def __init__(self, skill: CalendarSkill | None = None) -> None:
        self._skill = skill or CalendarSkill()

    def initialize(self, state_dir: str, env_vars: dict[str, str]) -> None:
        self._sync_compat_hooks()
        self._skill.initialize(state_dir, env_vars)

    def execute_cli(self, command: str) -> CommandResult:
        self._sync_compat_hooks()
        return self._skill.execute(command)

    def execute_python(self, code: str) -> CommandResult:
        del code
        return CommandResult(stdout="", stderr="Python interface not supported for CalendarBackend", exit_code=1)

    def get_gateway_status(self) -> dict[str, Any] | None:
        return None

    def get_config(self) -> dict[str, Any]:
        return {}

    def cleanup(self) -> None:
        self._skill.cleanup()

    def get_state(self) -> dict[str, Any]:
        return self._skill.get_state()

    # Compatibility accessor for older callers/tests.
    @property
    def _events(self) -> list[dict[str, Any]]:  # noqa: SLF001 - compatibility
        return self._skill._events

    @_events.setter
    def _events(self, value: list[dict[str, Any]]) -> None:  # noqa: SLF001 - compatibility
        self._skill._events = value

    def _sync_compat_hooks(self) -> None:
        calendar_skill_mod._get_online_time = _get_online_time
        calendar_skill_mod._resolve_calendar_provider = _resolve_calendar_provider
        calendar_skill_mod._run_calendar_provider_command = _run_calendar_provider_command
