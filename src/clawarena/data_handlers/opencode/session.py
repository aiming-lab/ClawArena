"""OpenCode session initialisation."""

from __future__ import annotations

from clawarena.core.types import WorkCopy


def init_opencode_session(work_copy: WorkCopy, test_id: str) -> str:
    """Return empty string — OpenCode creates sessions at runtime.

    The Engine extracts sessionID from the JSON event stream on first
    invocation and caches it for subsequent rounds.
    """
    return ""
