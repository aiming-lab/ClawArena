"""Runtime for dispatching CLI commands to registered skills."""

from __future__ import annotations

from typing import Any

from openclaw_env.backend.base import CommandResult
from openclaw_env.skills.registry import SkillRegistry


class SkillRuntime:
    """Coordinates skill lifecycle and command dispatch."""

    def __init__(self, registry: SkillRegistry) -> None:
        self._registry = registry

    def initialize(self, state_dir: str, env_vars: dict[str, str]) -> None:
        for skill in self._registry.iter_skills():
            skill.initialize(state_dir, env_vars)

    def execute_cli(self, command: str) -> CommandResult:
        prefix = command.strip().split()[0] if command.strip() else ""
        skill = self._registry.resolve(prefix)
        if skill is None:
            return CommandResult(
                stdout="",
                stderr=(
                    f"Unknown command prefix '{prefix}'. "
                    f"Available: {', '.join(self._registry.list_prefixes())}"
                ),
                exit_code=1,
            )
        return skill.execute(command)

    def get_state(self) -> dict[str, Any]:
        state: dict[str, Any] = {}
        for skill in self._registry.iter_skills():
            state.update(skill.get_state())
        return state

    def cleanup(self) -> None:
        for skill in self._registry.iter_skills():
            skill.cleanup()
