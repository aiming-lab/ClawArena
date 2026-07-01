"""Tasks skill adapter."""

from __future__ import annotations

from openclaw_env.backend.tasks_backend import TasksBackend
from openclaw_env.skills.base import BackendSkillAdapter


class TasksSkillAdapter(BackendSkillAdapter):
    def __init__(self, backend: TasksBackend) -> None:
        super().__init__(backend, prefixes=("tasks",))
