"""Compatibility backend wrapper around EmailSkill."""

from __future__ import annotations

from typing import Any

from openclaw_env.backend.base import BaseBackend, CommandResult
from openclaw_env.skills.impl import email_skill as email_skill_mod
from openclaw_env.skills.impl.email_skill import EmailSkill

# Re-export helper hooks for backward compatibility with tests/tooling that
# monkeypatch backend module symbols.
_resolve_email_provider = email_skill_mod._resolve_email_provider
_run_email_online_action = email_skill_mod._run_email_online_action
_build_google_gmail_settings = email_skill_mod._build_google_gmail_settings
_build_google_gmail_service = email_skill_mod._build_google_gmail_service
_build_himalaya_settings = email_skill_mod._build_himalaya_settings


class EmailBackend(BaseBackend):
    """Compatibility shim; email logic now lives in EmailSkill."""

    def __init__(self, skill: EmailSkill | None = None) -> None:
        self._skill = skill or EmailSkill()

    def initialize(self, state_dir: str, env_vars: dict[str, str]) -> None:
        self._sync_compat_hooks()
        self._skill.initialize(state_dir, env_vars)

    def execute_cli(self, command: str) -> CommandResult:
        self._sync_compat_hooks()
        return self._skill.execute(command)

    def execute_python(self, code: str) -> CommandResult:
        del code
        return CommandResult(stdout="", stderr="Python interface not supported for EmailBackend", exit_code=1)

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
    def _emails(self) -> list[dict[str, Any]]:  # noqa: SLF001 - compatibility
        return self._skill._emails

    @_emails.setter
    def _emails(self, value: list[dict[str, Any]]) -> None:  # noqa: SLF001 - compatibility
        self._skill._emails = value

    def _sync_compat_hooks(self) -> None:
        email_skill_mod._resolve_email_provider = _resolve_email_provider
        email_skill_mod._run_email_online_action = _run_email_online_action
        email_skill_mod._build_google_gmail_settings = _build_google_gmail_settings
        email_skill_mod._build_google_gmail_service = _build_google_gmail_service
        email_skill_mod._build_himalaya_settings = _build_himalaya_settings
