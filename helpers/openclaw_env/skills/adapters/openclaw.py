"""OpenClaw skill adapters."""

from __future__ import annotations

from openclaw_env.backend.base import BaseBackend, CommandResult
from openclaw_env.backend.mock_backend import MockBackend
from openclaw_env.skills.base import Skill
from openclaw_env.skills.policies.openclaw_fallback import should_fallback_to_mock


class OpenClawSkillAdapter(Skill):
    """Skill that runs openclaw via primary backend with optional mock fallback."""

    def __init__(
        self,
        *,
        primary_backend: BaseBackend,
        mock_fallback_backend: MockBackend | None,
        fallback_enabled: bool,
    ) -> None:
        super().__init__(prefixes=("openclaw",))
        self.primary_backend = primary_backend
        self.mock_fallback_backend = mock_fallback_backend
        self.fallback_enabled = fallback_enabled

    def initialize(self, state_dir: str, env_vars: dict[str, str]) -> None:
        self.primary_backend.initialize(state_dir, env_vars)
        if self.mock_fallback_backend is not None:
            self.mock_fallback_backend.initialize(state_dir, env_vars)

    def execute(self, command: str) -> CommandResult:
        result = self.primary_backend.execute_cli(command)
        if (
            self.mock_fallback_backend is not None
            and should_fallback_to_mock(
                enabled=self.fallback_enabled,
                command=command,
                result=result,
            )
        ):
            mock_result = self.mock_fallback_backend.execute_cli(command)
            merged_meta = dict(result.meta or {})
            merged_meta.update(
                {
                    "fallback_to_mock": True,
                    "fallback_reason": "network_or_external_dependency_failure",
                    "real_exit_code": result.exit_code,
                    "real_stdout": result.stdout,
                    "real_stderr": result.stderr,
                }
            )
            mock_tags = list((mock_result.meta or {}).get("error_tags", []))
            mock_tags.append("fallback_to_mock")
            merged_meta["error_tags"] = list(dict.fromkeys(mock_tags))
            return CommandResult(
                stdout=mock_result.stdout,
                stderr=mock_result.stderr,
                exit_code=mock_result.exit_code,
                state_changes=mock_result.state_changes,
                meta=merged_meta,
            )
        return result

    def get_state(self) -> dict[str, object]:
        return self.primary_backend.get_state()

    def cleanup(self) -> None:
        self.primary_backend.cleanup()
        if self.mock_fallback_backend is not None:
            self.mock_fallback_backend.cleanup()
