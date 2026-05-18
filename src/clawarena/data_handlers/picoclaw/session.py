"""PicoClaw session initialisation."""

from __future__ import annotations

from clawarena.core.types import WorkCopy


def init_picoclaw_session(work_copy: WorkCopy, test_id: str) -> str:
    """Return the session key for *test_id* (e.g. ``bench:trace_s1``).

    The session JSONL + .meta.json were pre-seeded in the memory
    directory during prepare_work_copy.
    """
    manifest = work_copy.extra.get("manifest", {})
    agent_info = manifest.get("agents", {}).get(test_id, {})
    return agent_info.get("session_key", "")
