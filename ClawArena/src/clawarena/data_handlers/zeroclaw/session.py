"""ZeroClaw session initialisation."""

from __future__ import annotations

import uuid
from pathlib import Path

from clawarena.core.types import WorkCopy


def init_zeroclaw_session(work_copy: WorkCopy, test_id: str) -> str:
    """Create a session state file path for ZeroClaw's --session-state-file.

    Returns a path to a JSON file that ZeroClaw uses to persist conversation
    history across multiple rounds. The file is created in the state directory
    and uniquified with a short UUID suffix to avoid conflicts with previous runs.
    """
    # Store current agent_id so the engine can set ZEROCLAW_WORKSPACE
    manifest = work_copy.extra.get("manifest", {})
    agent_info = manifest.get("agents", {}).get(test_id, {})
    agent_id = agent_info.get("agent_id", test_id)
    work_copy.extra["current_agent_id"] = agent_id

    suffix = uuid.uuid4().hex[:8]
    state_dir = work_copy.state_dir / "sessions"
    state_dir.mkdir(parents=True, exist_ok=True)
    session_file = state_dir / f"{test_id}_{suffix}.json"
    return str(session_file)
