"""Claude Code data validation."""

from __future__ import annotations

import json
import re
from pathlib import Path

from clawarena.data_handlers.update_refs import resolve_update_entries

_UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


def validate_claude_code(
    manifest: dict,
    manifest_dir: Path,
    eval_dir: Path,
    test_entries: list[dict],
) -> list[str]:
    errors: list[str] = []
    e = errors.append

    # CC-001: framework
    if manifest.get("framework") != "claude-code":
        e("[CC-001] manifest.framework != 'claude-code'")

    # CC-002: claude_config_file
    config_rel = manifest.get("claude_config_file")
    if config_rel:
        config_path = manifest_dir / config_rel
        if not config_path.exists():
            e(f"[CC-002] claude_config_file not found: {config_path}")
        else:
            try:
                json.loads(config_path.read_text(encoding="utf-8"))
            except Exception as ex:
                e(f"[CC-002] claude_config_file invalid JSON: {ex}")

    # CC-003: projects_dir
    projects_rel = manifest.get("projects_dir", "state/projects")
    projects_dir = manifest_dir / projects_rel
    if not projects_dir.exists():
        e(f"[CC-003] projects_dir not found: {projects_dir}")

    # CC-004: workspaces_dir
    workspaces_rel = manifest.get("workspaces_dir", "workspaces")
    workspaces_dir = manifest_dir / workspaces_rel
    if not workspaces_dir.exists():
        e(f"[CC-004] workspaces_dir not found: {workspaces_dir}")

    # CC-010: agents cover all test_ids
    agents = manifest.get("agents", {})
    test_ids = {t["id"] for t in test_entries}
    for tid in test_ids:
        if tid not in agents:
            e(f"[CC-010] test_id '{tid}' not in manifest.agents")

    # CC-011: per-agent checks
    for test_id, info in agents.items():
        prefix = f"[CC-011:{test_id}]"

        if info.get("agent_id") != test_id:
            e(f"{prefix} agent_id != test_id")

        session = info.get("session", "")
        if session and not _UUID_RE.match(session):
            e(f"{prefix} session '{session}' is not a valid UUID")

        if session:
            project_dir = manifest_dir / (info.get("project_dir", f"state/projects/{test_id}"))
            jsonl = project_dir / f"{session}.jsonl"
            if not jsonl.exists():
                e(f"{prefix} session JSONL not found: {jsonl}")
            else:
                _validate_jsonl(jsonl, prefix, errors)

        ws_rel = info.get("workspace")
        if ws_rel:
            ws_dir = manifest_dir / ws_rel
            if not ws_dir.exists():
                e(f"{prefix} workspace not found: {ws_dir}")
            else:
                if not (ws_dir / "CLAUDE.md").exists():
                    e(f"{prefix} CLAUDE.md not found in workspace")

    # CC-020: updates
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
                    e(f"[CC-021:{test_id}] update_id '{uid}' not in manifest.updates")

    # CC-022: update file existence
    for test_id, test_updates in updates.items():
        for uid, meta in test_updates.items():
            prefix = f"[CC-022:{test_id}/{uid}]"
            update_dir = manifest_dir / meta.get("dir", "")
            if not update_dir.exists():
                e(f"{prefix} dir not found: {update_dir}")
                continue
            for item in meta.get("files", []):
                name = item.get("name", item) if isinstance(item, dict) else item
                if not (update_dir / name).exists():
                    e(f"{prefix} file not found: {name}")

    return errors


def _validate_jsonl(path: Path, prefix: str, errors: list[str]) -> None:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception as ex:
        errors.append(f"{prefix} cannot read JSONL: {ex}")
        return

    if not lines:
        return

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError as ex:
            errors.append(f"{prefix} JSONL line {i+1} invalid JSON: {ex}")
            continue

        if not isinstance(entry, dict):
            continue

        entry_type = entry.get("type")
        if entry_type in ("user", "assistant"):
            if not isinstance(entry.get("uuid"), str):
                errors.append(f"{prefix} JSONL line {i+1} missing uuid")
            msg = entry.get("message", {})
            if not isinstance(msg, dict) or "role" not in msg:
                errors.append(f"{prefix} JSONL line {i+1} missing message.role")
