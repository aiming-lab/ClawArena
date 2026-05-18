"""Compatibility backend wrapper around TasksSkill."""

from __future__ import annotations

from typing import Any

from openclaw_env.backend.base import BaseBackend, CommandResult
from openclaw_env.skills.impl import tasks_skill as tasks_skill_mod
from openclaw_env.skills.impl.tasks_skill import TasksSkill

# Re-export helper hooks for backward compatibility with tests/tooling that
# monkeypatch backend module symbols.
_build_google_tasks_settings = tasks_skill_mod._build_google_tasks_settings
_build_google_tasks_service = tasks_skill_mod._build_google_tasks_service
_resolve_tasks_provider = tasks_skill_mod._resolve_tasks_provider
_run_tasks_online_action = tasks_skill_mod._run_tasks_online_action
_SEEDED_TASKS = tasks_skill_mod._SEEDED_TASKS


class TasksBackend(BaseBackend):
    """Compatibility shim; tasks logic now lives in TasksSkill."""

    def __init__(self, skill: TasksSkill | None = None) -> None:
        self._skill = skill or TasksSkill()

    def initialize(self, state_dir: str, env_vars: dict[str, str]) -> None:
        self._sync_compat_hooks()
        self._skill.initialize(state_dir, env_vars)

    def execute_cli(self, command: str) -> CommandResult:
        self._sync_compat_hooks()
        return self._skill.execute(command)

    def execute_python(self, code: str) -> CommandResult:
        del code
        return CommandResult(stdout="", stderr="Python interface not supported for TasksBackend", exit_code=1)

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
    def _tasks(self) -> list[dict[str, Any]]:  # noqa: SLF001 - compatibility
        return self._skill._tasks

    @_tasks.setter
    def _tasks(self, value: list[dict[str, Any]]) -> None:  # noqa: SLF001 - compatibility
        self._skill._tasks = value

    def _sync_compat_hooks(self) -> None:
        tasks_skill_mod._build_google_tasks_settings = _build_google_tasks_settings
        tasks_skill_mod._build_google_tasks_service = _build_google_tasks_service
        tasks_skill_mod._resolve_tasks_provider = _resolve_tasks_provider
        tasks_skill_mod._run_tasks_online_action = _run_tasks_online_action
