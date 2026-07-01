"""IronClaw work-copy creation with libSQL isolation."""

from __future__ import annotations

import os
import shutil
from datetime import datetime
from pathlib import Path

from clawarena.core.types import WorkCopy


def prepare_ironclaw_work_copy(
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

    # 2. Create state_dir (IRONCLAW_BASE_DIR)
    state_dst = work_dir / f"state_{run_id}"
    state_dst.mkdir(parents=True)

    # 3. Copy seed.sql files if present (for future DB seeding)
    state_rel = manifest.get("state_dir", "state")
    state_src = manifest_dir / state_rel
    if state_src.exists():
        for item in state_src.iterdir():
            if item.is_dir():
                dst = state_dst / item.name
                shutil.copytree(item, dst)
            elif item.is_file():
                shutil.copy2(item, state_dst / item.name)

    # 4. Write .env file for IronClaw
    env_content = (
        f"DATABASE_BACKEND=libsql\n"
        f"LIBSQL_PATH={state_dst / 'ironclaw.db'}\n"
    )
    (state_dst / ".env").write_text(env_content, encoding="utf-8")

    ironclaw_config = manifest.get("_ironclaw_config", {})

    return WorkCopy(
        state_dir=state_dst,
        config_path=state_dst / ".env",
        project_root=project_root,
        workspace_root=workspaces_dst if workspaces_dst.exists() else None,
        extra={
            "manifest": manifest,
            "manifest_dir": manifest_dir,
            "ironclaw_config": ironclaw_config,
        },
    )
