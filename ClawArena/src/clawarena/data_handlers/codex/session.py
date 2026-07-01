"""Codex session initialisation."""

from __future__ import annotations

from clawarena.core.types import WorkCopy


def init_codex_session(work_copy: WorkCopy, test_id: str) -> str:
    """Return empty string — Codex creates threads at runtime.

    The Engine manages thread lifecycle internally via thread_start/thread.run.
    """
    return ""
