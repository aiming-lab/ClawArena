"""CoPaw work-copy creation."""

from __future__ import annotations

import os
import json
import shutil
from datetime import datetime
from pathlib import Path

from clawarena.core.types import WorkCopy


def prepare_copaw_work_copy(
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

    # 2. Create state_dir (COPAW_WORKING_DIR)
    state_dst = work_dir / f"state_{run_id}"
    state_dst.mkdir(parents=True)

    # 3. Initialize CoPaw working directory structure
    (state_dst / "agents").mkdir(exist_ok=True)
    (state_dst / "sessions").mkdir(exist_ok=True)

    # 4. Generate CoPaw config.json
    copaw_config = manifest.get("_copaw_config", {})
    config_dst = state_dst / "config.json"
    config_dst.write_text(
        json.dumps(copaw_config, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    return WorkCopy(
        state_dir=state_dst,
        config_path=config_dst,
        project_root=project_root,
        workspace_root=workspaces_dst if workspaces_dst.exists() else None,
        extra={
            "manifest": manifest,
            "manifest_dir": manifest_dir,
            "copaw_config": copaw_config,
        },
    )
