"""Base backend interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class CommandResult:
    """Result of executing a command."""

    stdout: str
    stderr: str
    exit_code: int
    state_changes: dict[str, Any] | None = None
    meta: dict[str, Any] | None = None
    execution_trace: list[dict[str, Any]] | None = None


class BaseBackend(ABC):
    """Abstract backend for executing openclaw commands."""

    @abstractmethod
    def initialize(self, state_dir: str, env_vars: dict[str, str]) -> None:
        """Initialize the backend with a state directory."""

    @abstractmethod
    def execute_cli(self, command: str) -> CommandResult:
        """Execute a CLI command and return the result."""

    @abstractmethod
    def execute_python(self, code: str) -> CommandResult:
        """Execute Python code and return the result."""

    @abstractmethod
    def get_gateway_status(self) -> dict[str, Any] | None:
        """Get the current gateway status, or None if not running."""

    @abstractmethod
    def get_config(self) -> dict[str, Any]:
        """Get the current openclaw configuration."""

    @abstractmethod
    def cleanup(self) -> None:
        """Clean up backend resources."""

    def get_state(self) -> dict[str, Any]:
        """Return backend-provided evaluator state fragments."""
        return {}
