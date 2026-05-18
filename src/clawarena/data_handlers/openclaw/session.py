"""OpenClaw session management — init, uniquify, register."""

from __future__ import annotations

import json
import uuid
from pathlib import Path

from clawarena.core.types import WorkCopy


def init_openclaw_session(work_copy: WorkCopy, test_id: str) -> str:
    """Uniquify + prepare + register the main session for a test.

    Returns the new unique session_id.
    """
    manifest = work_copy.extra.get("manifest", {})
    agent_info = manifest.get("agents", {}).get(test_id, {})
    agent_id = agent_info.get("agent_id", test_id)
    old_session_id = agent_info.get("session", "main")

    new_session_id = _uniquify_session(
        work_copy.state_dir, agent_id, old_session_id
    )

    # Ensure session file exists
    _prepare_session(work_copy.state_dir, agent_id, new_session_id)

    return new_session_id


def _uniquify_session(
    state_dir: Path,
    agent_id: str,
    old_session_id: str,
) -> str:
    """Rename session file and update sessions.json with unique suffix."""
    suffix = uuid.uuid4().hex[:8]
    new_session_id = f"{old_session_id}_{suffix}"

    sessions_dir = state_dir / "agents" / agent_id / "sessions"
    old_path = sessions_dir / f"{old_session_id}.jsonl"
    new_path = sessions_dir / f"{new_session_id}.jsonl"

    if old_path.exists():
        # Update first-line id field if present
        lines = old_path.read_text(encoding="utf-8").splitlines(keepends=True)
        if lines:
            try:
                first = json.loads(lines[0])
                if "id" in first:
                    first["id"] = new_session_id
                    lines[0] = json.dumps(first, ensure_ascii=False) + "\n"
            except (json.JSONDecodeError, KeyError):
                pass
        new_path.write_text("".join(lines), encoding="utf-8")
        old_path.unlink()
    else:
        sessions_dir.mkdir(parents=True, exist_ok=True)
        new_path.touch()

    # Update sessions.json
    sessions_json = sessions_dir / "sessions.json"
    if sessions_json.exists():
        try:
            data = json.loads(sessions_json.read_text(encoding="utf-8"))
        except Exception:
            data = {}

        old_key = f"agent:{agent_id}:{old_session_id}"
        new_key = f"agent:{agent_id}:{new_session_id}"
        if old_key in data:
            entry = data.pop(old_key)
            entry["sessionId"] = new_session_id
            entry["sessionFile"] = f"{new_session_id}.jsonl"
            data[new_key] = entry
            sessions_json.write_text(
                json.dumps(data, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

    return new_session_id


def _prepare_session(
    state_dir: Path,
    agent_id: str,
    session_id: str,
) -> None:
    """Ensure the session transcript file exists."""
    sessions_dir = state_dir / "agents" / agent_id / "sessions"
    sessions_dir.mkdir(parents=True, exist_ok=True)
    session_path = sessions_dir / f"{session_id}.jsonl"
    if not session_path.exists():
        session_path.touch()


def register_session_in_json(
    state_dir: Path,
    agent_id: str,
    filename: str,
    channel: str,
) -> None:
    """Register a new session in sessions.json."""
    sessions_dir = state_dir / "agents" / agent_id / "sessions"
    sessions_json = sessions_dir / "sessions.json"

    try:
        data = json.loads(sessions_json.read_text(encoding="utf-8")) if sessions_json.exists() else {}
    except Exception:
        data = {}

    session_id = filename.replace(".jsonl", "")
    key = f"agent:{agent_id}:{session_id}"
    if key in data:
        return

    data[key] = {
        "sessionId": session_id,
        "sessionFile": filename,
        "channel": channel,
        "lastChannel": channel,
    }
    sessions_json.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
