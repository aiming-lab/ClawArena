"""Claude Code update execution."""

from __future__ import annotations

import shutil
from pathlib import Path

from clawarena.utils import framework_line
from clawarena.core.types import WorkCopy

from ..update_refs import resolve_update_entries


def execute_claude_code_update(
    update_id: str,
    work_copy: WorkCopy,
    test_id: str,
    session_id: str,
) -> None:
    manifest = work_copy.extra.get("manifest", {})
    manifest_dir: Path | None = work_copy.extra.get("manifest_dir")
    if manifest_dir is None:
        raise RuntimeError(f"WorkCopy.extra missing 'manifest_dir' for update '{update_id}'")

    updates_map = manifest.get("updates", {}).get(test_id, {})
    resolved_updates = resolve_update_entries(updates_map, update_id)
    framework = manifest.get("framework", "claude-code")
    if not resolved_updates:
        print(framework_line("  [warn]", f"update_id '{update_id}' not found in manifest for {test_id}", framework))
        return

    agent_info = manifest.get("agents", {}).get(test_id, {})
    agent_id = agent_info.get("agent_id", test_id)

    ws_dir = work_copy.workspace_root / agent_id if work_copy.workspace_root else None
    if ws_dir is None:
        print(framework_line("  [warn]", f"no workspace_root for {test_id}", framework))
        return

    for resolved_id, update_meta in resolved_updates:
        update_type = update_meta.get("type", "")
        update_dir = manifest_dir / update_meta.get("dir", "")
        files = update_meta.get("files", [])

        if update_type in ("workspace_md", "workspace"):
            _apply_workspace_updates(files, update_dir, ws_dir, framework)
        else:
            print(framework_line("  [warn]", f"unknown update type for '{resolved_id}': {update_type}", framework))


def _apply_workspace_updates(
    files: list[dict | str],
    source_dir: Path,
    ws_dir: Path,
    framework: str,
) -> None:
    """Apply workspace updates with action support (new/append/insert/delete)."""
    for item in files:
        if isinstance(item, str):
            filename = item
            action = "new"
            target = filename
        else:
            filename = item.get("name", "")
            action = item.get("action", "new")
            target = item.get("target", filename)

        src = source_dir / filename
        dst = ws_dir / target

        if action == "new":
            if not src.exists():
                print(framework_line("  [warn]", f"update source not found: {src}", framework))
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(framework_line("  [update]", f"workspace new: {target}", framework))

        elif action == "append":
            if not src.exists():
                print(framework_line("  [warn]", f"update source not found: {src}", framework))
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            content = src.read_text(encoding="utf-8")
            with open(dst, "a", encoding="utf-8") as f:
                f.write(content)
            print(framework_line("  [update]", f"workspace append: {target}", framework))

        elif action == "insert":
            if not src.exists():
                print(framework_line("  [warn]", f"update source not found: {src}", framework))
                continue
            param = item.get("param", {}) if isinstance(item, dict) else {}
            after = int(param.get("after", 0)) if isinstance(param, dict) else 0
            existing_lines = (
                dst.read_text(encoding="utf-8").splitlines(keepends=True)
                if dst.exists()
                else []
            )
            insert_content = src.read_text(encoding="utf-8")
            new_content = (
                "".join(existing_lines[:after])
                + insert_content
                + "".join(existing_lines[after:])
            )
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(new_content, encoding="utf-8")
            print(framework_line("  [update]", f"workspace insert after line {after}: {target}", framework))

        elif action == "delete":
            if not dst.exists():
                continue
            param = item.get("param", {}) if isinstance(item, dict) else {}
            lines_param = param.get("lines", []) if isinstance(param, dict) else []
            existing_lines = dst.read_text(encoding="utf-8").splitlines(keepends=True)
            to_delete: set[int] = set()
            for line_spec in lines_param:
                if isinstance(line_spec, int):
                    to_delete.add(line_spec - 1)
                elif isinstance(line_spec, str) and ":" in line_spec:
                    parts = line_spec.split(":", 1)
                    start = int(parts[0]) if parts[0] else 0
                    end = int(parts[1]) if parts[1] else len(existing_lines)
                    to_delete.update(range(start, end))
            new_lines = [line for i, line in enumerate(existing_lines) if i not in to_delete]
            dst.write_text("".join(new_lines), encoding="utf-8")
            print(framework_line("  [update]", f"workspace delete lines {lines_param}: {target}", framework))

        else:
            print(framework_line("  [warn]", f"unknown action: {action}", framework))
