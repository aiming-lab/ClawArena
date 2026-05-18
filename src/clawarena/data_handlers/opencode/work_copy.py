"""OpenCode work-copy creation with XDG isolation."""

from __future__ import annotations

import os
import json
import shutil
from datetime import datetime
from pathlib import Path

from clawarena.core.types import WorkCopy


def prepare_opencode_work_copy(
    manifest: dict,
    manifest_dir: Path,
    project_root: Path,
) -> WorkCopy:
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f") + f"_{os.getpid()}"
    work_dir = manifest_dir / "work"
    work_dir.mkdir(exist_ok=True)

    # 1. Copy workspaces
    workspaces_rel = manifest.get("workspaces_dir", "workspaces")
    workspaces_src = manifest_dir / workspaces_rel
    workspaces_dst = work_dir / f"workspaces_{run_id}"
    if workspaces_src.exists():
        shutil.copytree(workspaces_src, workspaces_dst)
    else:
        workspaces_dst.mkdir(parents=True)

    # 2. Create state_dir with XDG sub-directories
    state_dst = work_dir / f"state_{run_id}"
    for subdir in ("config", "data", "cache", "state"):
        (state_dst / subdir).mkdir(parents=True, exist_ok=True)

    # 3. Write opencode.jsonc config into each workspace's .opencode/ dir
    opencode_config = manifest.get("_opencode_config", {})
    jsonc_content = {
        "model": opencode_config.get("model", "anthropic/claude-sonnet-4-5"),
    }
    permission = opencode_config.get("permission")
    if permission:
        jsonc_content["permission"] = permission
    plugin = opencode_config.get("plugin")
    if plugin:
        jsonc_content["plugin"] = plugin

    for agent_info in manifest.get("agents", {}).values():
        agent_id = agent_info.get("agent_id", "")
        ws_dir = workspaces_dst / agent_id
        if ws_dir.exists():
            oc_dir = ws_dir / ".opencode"
            oc_dir.mkdir(exist_ok=True)
            (oc_dir / "opencode.jsonc").write_text(
                json.dumps(jsonc_content, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )

    return WorkCopy(
        state_dir=state_dst,
        config_path=None,
        project_root=project_root,
        workspace_root=workspaces_dst if workspaces_dst.exists() else None,
        extra={
            "manifest": manifest,
            "manifest_dir": manifest_dir,
            "opencode_config": opencode_config,
        },
    )
