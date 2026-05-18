"""Codex update execution."""

from __future__ import annotations

import shutil
from pathlib import Path

from clawarena.core.types import WorkCopy


def execute_codex_update(
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
    update_meta = updates_map.get(update_id)
    if update_meta is None:
        print(f"  [warn] update_id '{update_id}' not found in manifest for {test_id}")
        return

    update_type = update_meta.get("type", "")
    update_dir = manifest_dir / update_meta.get("dir", "")
    files = update_meta.get("files", [])
    agent_info = manifest.get("agents", {}).get(test_id, {})
    agent_id = agent_info.get("agent_id", test_id)

    ws_dir = work_copy.workspace_root / agent_id if work_copy.workspace_root else None
    if ws_dir is None:
        print(f"  [warn] no workspace_root for {test_id}")
        return

    if update_type in ("workspace_md", "workspace"):
        _apply_workspace_updates(files, update_dir, ws_dir)
    else:
        print(f"  [warn] unknown update type: {update_type}")


def _apply_workspace_updates(
    files: list[dict | str],
    source_dir: Path,
    ws_dir: Path,
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
                print(f"  [warn] update source not found: {src}")
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"  [update] workspace new: {target}")

        elif action == "append":
            if not src.exists():
                print(f"  [warn] update source not found: {src}")
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            content = src.read_text(encoding="utf-8")
            with open(dst, "a", encoding="utf-8") as f:
                f.write(content)
            print(f"  [update] workspace append: {target}")

        elif action == "insert":
            if not src.exists():
                print(f"  [warn] update source not found: {src}")
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
            print(f"  [update] workspace insert after line {after}: {target}")

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
            print(f"  [update] workspace delete lines {lines_param}: {target}")

        else:
            print(f"  [warn] unknown action: {action}")
