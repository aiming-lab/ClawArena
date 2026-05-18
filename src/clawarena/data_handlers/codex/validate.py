"""Codex data validation."""

from __future__ import annotations

import json
from pathlib import Path

from clawarena.data_handlers.update_refs import resolve_update_entries


def validate_codex(
    manifest: dict,
    manifest_dir: Path,
    eval_dir: Path,
    test_entries: list[dict],
) -> list[str]:
    errors: list[str] = []
    e = errors.append

    # CX-001: framework
    if manifest.get("framework") != "codex":
        e("[CX-001] manifest.framework != 'codex'")

    # CX-002: codex_config_file
    config_rel = manifest.get("codex_config_file")
    if config_rel:
        config_path = manifest_dir / config_rel
        if not config_path.exists():
            e(f"[CX-002] codex_config_file not found: {config_path}")
        else:
            try:
                json.loads(config_path.read_text(encoding="utf-8"))
            except Exception as ex:
                e(f"[CX-002] codex_config_file invalid JSON: {ex}")

    # CX-003: workspaces_dir
    workspaces_rel = manifest.get("workspaces_dir", "workspaces")
    workspaces_dir = manifest_dir / workspaces_rel
    if not workspaces_dir.exists():
        e(f"[CX-003] workspaces_dir not found: {workspaces_dir}")

    # CX-010: agents cover all test_ids
    agents = manifest.get("agents", {})
    test_ids = {t["id"] for t in test_entries}
    for tid in test_ids:
        if tid not in agents:
            e(f"[CX-010] test_id '{tid}' not in manifest.agents")

    # CX-011: per-agent checks
    for test_id, info in agents.items():
        prefix = f"[CX-011:{test_id}]"

        if info.get("agent_id") != test_id:
            e(f"{prefix} agent_id != test_id")

        ws_rel = info.get("workspace")
        if ws_rel:
            ws_dir = manifest_dir / ws_rel
            if not ws_dir.exists():
                e(f"{prefix} workspace not found: {ws_dir}")
            else:
                if not (ws_dir / "AGENTS.md").exists():
                    e(f"{prefix} AGENTS.md not found in workspace")

    # CX-020: updates
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
                    e(f"[CX-020:{test_id}] update_id '{uid}' not in manifest.updates")

    # CX-021: update file existence
    for test_id, test_updates in updates.items():
        for uid, meta in test_updates.items():
            prefix = f"[CX-021:{test_id}/{uid}]"
            update_dir = manifest_dir / meta.get("dir", "")
            if not update_dir.exists():
                e(f"{prefix} dir not found: {update_dir}")
                continue
            for item in meta.get("files", []):
                name = item.get("name", item) if isinstance(item, dict) else item
                if not (update_dir / name).exists():
                    e(f"{prefix} file not found: {name}")

    return errors
