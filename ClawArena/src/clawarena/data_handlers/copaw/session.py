"""CoPaw session initialisation."""

from __future__ import annotations

from clawarena.core.types import WorkCopy


def init_copaw_session(work_copy: WorkCopy, test_id: str) -> str:
    """Return empty string — CoPaw sessions are created at runtime by the server.

    The engine's ``_session_map`` caches the server-assigned session ID
    from the first round's response for use in subsequent rounds.
    """
    return ""
