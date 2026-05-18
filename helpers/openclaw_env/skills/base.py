"""Core skill interfaces used by backend runtime."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from openclaw_env.backend.base import BaseBackend, CommandResult


class Skill(ABC):
    """Abstract executable capability bound to one or more command prefixes."""

    def __init__(self, *, prefixes: tuple[str, ...]) -> None:
        if not prefixes:
            raise ValueError("Skill must declare at least one command prefix")
        self._prefixes = tuple(prefixes)

    @property
    def prefixes(self) -> tuple[str, ...]:
        return self._prefixes

    def can_handle(self, command_prefix: str) -> bool:
        return command_prefix in self._prefixes

    @abstractmethod
    def initialize(self, state_dir: str, env_vars: dict[str, str]) -> None:
        """Initialize skill state for a new episode."""

    @abstractmethod
    def execute(self, command: str) -> CommandResult:
        """Execute one command routed to this skill."""

    def get_state(self) -> dict[str, Any]:
        """Return skill state contributions for evaluator state."""
        return {}

    @abstractmethod
    def cleanup(self) -> None:
        """Release skill resources."""


class BackendSkillAdapter(Skill):
    """Thin adapter that exposes an existing ``BaseBackend`` as a skill."""

    def __init__(self, backend: BaseBackend, *, prefixes: tuple[str, ...]) -> None:
        super().__init__(prefixes=prefixes)
        self.backend = backend

    def initialize(self, state_dir: str, env_vars: dict[str, str]) -> None:
        self.backend.initialize(state_dir, env_vars)

    def execute(self, command: str) -> CommandResult:
        return self.backend.execute_cli(command)

    def get_state(self) -> dict[str, Any]:
        return self.backend.get_state()

    def cleanup(self) -> None:
        self.backend.cleanup()
