"""Nanobot data validation."""

from __future__ import annotations

import json
from pathlib import Path

from clawarena.data_handlers.update_refs import resolve_update_entries


def _sanitize_session_key(key: str) -> str:
    """Nanobot sanitizes session keys: ``:`` ``/`` ``\\`` -> ``_``."""
    return key.replace(":", "_").replace("/", "_").replace("\\", "_")


def validate_nanobot(
    manifest: dict,
    manifest_dir: Path,
    eval_dir: Path,
    test_entries: list[dict],
) -> list[str]:
    errors: list[str] = []
    e = errors.append

    # NB-001: framework
    if manifest.get("framework") != "nanobot":
        e("[NB-001] manifest.framework != 'nanobot'")

    # NB-002: nanobot_config_file
    config_rel = manifest.get("nanobot_config_file")
    if config_rel:
        config_path = manifest_dir / config_rel
        if not config_path.exists():
            e(f"[NB-002] nanobot_config_file not found: {config_path}")
        else:
            try:
                json.loads(config_path.read_text(encoding="utf-8"))
            except Exception as ex:
                e(f"[NB-002] nanobot_config_file invalid JSON: {ex}")

    # NB-003: workspaces_dir
    workspaces_rel = manifest.get("workspaces_dir", "workspaces")
    workspaces_dir = manifest_dir / workspaces_rel
    if not workspaces_dir.exists():
        e(f"[NB-003] workspaces_dir not found: {workspaces_dir}")

    # NB-010: agents cover all test_ids
    agents = manifest.get("agents", {})
    test_ids = {t["id"] for t in test_entries}
    for tid in test_ids:
        if tid not in agents:
            e(f"[NB-010] test_id '{tid}' not in manifest.agents")

    # NB-011: per-agent checks
    for test_id, info in agents.items():
        prefix = f"[NB-011:{test_id}]"

        if info.get("agent_id") != test_id:
            e(f"{prefix} agent_id != test_id")

        # Session key + JSONL existence with metadata first line
        session_key = info.get("session_key", "")
        ws_rel = info.get("workspace")
        ws_dir = manifest_dir / ws_rel if ws_rel else None

        if session_key and ws_dir:
            safe_key = _sanitize_session_key(session_key)
            jsonl_path = ws_dir / "sessions" / f"{safe_key}.jsonl"
            if not jsonl_path.exists():
                e(f"{prefix} session JSONL not found: {jsonl_path}")
            else:
                # Check metadata first line
                first_line = ""
                with open(jsonl_path, encoding="utf-8") as f:
                    for raw in f:
                        raw = raw.strip()
                        if raw:
                            first_line = raw
                            break
                if first_line:
                    try:
                        first_obj = json.loads(first_line)
                        if first_obj.get("_type") != "metadata":
                            e(f"{prefix} session JSONL first line missing _type='metadata'")
                    except json.JSONDecodeError:
                        e(f"{prefix} session JSONL first line invalid JSON")

        # Workspace + AGENTS.md
        if ws_dir:
            if not ws_dir.exists():
                e(f"{prefix} workspace not found: {ws_dir}")
            else:
                if not (ws_dir / "AGENTS.md").exists():
                    e(f"{prefix} AGENTS.md not found in workspace")

    # NB-020: updates
    updates = manifest.get("updates", {})
    for test_id in test_ids:
        questions_path = eval_dir / test_id / "questions.json"
        if not questions_path.exists():
            continue
        try:
            questions = json.loads(questions_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        test_updates = updates.get(test_id, {})
        for rnd in questions.get("rounds", []):
            for uid in rnd.get("update_ids", []):
                if not resolve_update_entries(test_updates, uid):
                    e(f"[NB-020:{test_id}] update_id '{uid}' not in manifest.updates")

    # NB-021: update file existence
    for test_id, test_updates in updates.items():
        for uid, meta in test_updates.items():
            prefix = f"[NB-021:{test_id}/{uid}]"
            update_dir = manifest_dir / meta.get("dir", "")
            if not update_dir.exists():
                e(f"{prefix} dir not found: {update_dir}")
                continue
            for item in meta.get("files", []):
                name = item.get("name", item) if isinstance(item, dict) else item
                if not (update_dir / name).exists():
                    e(f"{prefix} file not found: {name}")

    return errors
