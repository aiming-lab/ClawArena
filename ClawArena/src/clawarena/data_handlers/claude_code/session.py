"""Claude Code session initialisation."""

from __future__ import annotations

from clawarena.core.types import WorkCopy


def init_claude_code_session(work_copy: WorkCopy, test_id: str) -> str:
    """Return the session UUID for *test_id*.

    The session JSONL was already placed at the correct sanitized path
    during prepare_work_copy.  This function simply looks up the UUID
    from the manifest.  An empty string means "start a new session"
    (Engine will not pass --resume).
    """
    manifest = work_copy.extra.get("manifest", {})
    agent_info = manifest.get("agents", {}).get(test_id, {})
    return agent_info.get("session", "")
