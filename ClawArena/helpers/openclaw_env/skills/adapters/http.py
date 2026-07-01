"""HTTP skill adapter."""

from __future__ import annotations

from openclaw_env.backend.http_backend import HttpBackend
from openclaw_env.skills.base import BackendSkillAdapter


class HttpSkillAdapter(BackendSkillAdapter):
    def __init__(self, backend: HttpBackend) -> None:
        super().__init__(backend, prefixes=("curl",))
