"""IronClaw session initialisation."""

from __future__ import annotations

from clawarena.core.types import WorkCopy


def init_ironclaw_session(work_copy: WorkCopy, test_id: str) -> str:
    """Return empty string — IronClaw manages sessions via database.

    Session continuity is handled by the libSQL database in state_dir.
    The ``-m`` mode operates within the current database context.
    """
    return ""
