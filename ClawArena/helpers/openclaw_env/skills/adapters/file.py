"""File skill adapter."""

from __future__ import annotations

from openclaw_env.backend.file_backend import FileSystemBackend
from openclaw_env.skills.base import BackendSkillAdapter


class FileSkillAdapter(BackendSkillAdapter):
    def __init__(self, backend: FileSystemBackend) -> None:
        super().__init__(backend, prefixes=("file",))
