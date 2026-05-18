"""Email skill adapter."""

from __future__ import annotations

from openclaw_env.backend.email_backend import EmailBackend
from openclaw_env.skills.base import BackendSkillAdapter


class EmailSkillAdapter(BackendSkillAdapter):
    def __init__(self, backend: EmailBackend) -> None:
        super().__init__(backend, prefixes=("email",))
