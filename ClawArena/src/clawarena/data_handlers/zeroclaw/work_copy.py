"""ZeroClaw work-copy creation."""

from __future__ import annotations

import os
import shutil
from datetime import datetime
from pathlib import Path

from clawarena.core.types import WorkCopy


def prepare_zeroclaw_work_copy(
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

    # 2. Create state_dir (ZEROCLAW_HOME)
    state_dst = work_dir / f"state_{run_id}"
    state_dst.mkdir(parents=True)

    # 3. Copy TOML config if present
    zeroclaw_config = manifest.get("_zeroclaw_config", {})
    config_rel = manifest.get("zeroclaw_config_file")
    config_path: Path | None = None
    if config_rel:
        config_src = manifest_dir / config_rel
        if config_src.exists():
            config_path = state_dst / config_src.name
            shutil.copy2(config_src, config_path)

    # 4. Find config.toml (zeroclaw runtime config)
    #    Search order: next to JSON config, config/ subdir, any agent workspace
    toml_src: Path | None = None
    if config_rel:
        toml_candidate = (manifest_dir / config_rel).parent / "config.toml"
        if toml_candidate.exists():
            toml_src = toml_candidate
    if toml_src is None:
        toml_candidate = manifest_dir / "config" / "config.toml"
        if toml_candidate.exists():
            toml_src = toml_candidate
    if toml_src is None and workspaces_src.exists():
        # Fall back to config.toml from any agent workspace
        for candidate in workspaces_src.glob("*/config.toml"):
            toml_src = candidate
            break

    if toml_src is not None:
        # Copy to state_dir (used by apply_model_config and overlays)
        dst_toml = state_dst / "config.toml"
        shutil.copy2(toml_src, dst_toml)
        dst_toml.chmod(0o600)

    # 5. Set up .zeroclaw/ layout for workspace resolution.
    #    zeroclaw's resolve_config_dir_for_workspace checks parent/.zeroclaw/
    #    (case 2 — legacy layout) which uses the ZEROCLAW_WORKSPACE value
    #    directly as workspace_dir, giving the agent access to project/,
    #    archive/ etc. alongside workspace/.
    #
    #    Remove per-agent config.toml (copied by copytree) so it doesn't
    #    trigger case 1 (which appends /workspace to workspace_dir).
    if workspaces_dst.exists():
        # Move one agent config.toml to .zeroclaw/ (or use state_dir copy)
        zc_cfg_dir = workspaces_dst / ".zeroclaw"
        zc_cfg_dir.mkdir(parents=True, exist_ok=True)
        zc_toml = zc_cfg_dir / "config.toml"
        for agent_toml in workspaces_dst.glob("*/config.toml"):
            if not zc_toml.exists():
                shutil.copy2(agent_toml, zc_toml)
                zc_toml.chmod(0o600)
            agent_toml.unlink()
        # If no agent config.toml was found, copy from state_dir
        if not zc_toml.exists() and (state_dst / "config.toml").exists():
            shutil.copy2(state_dst / "config.toml", zc_toml)
            zc_toml.chmod(0o600)

    return WorkCopy(
        state_dir=state_dst,
        config_path=config_path,
        project_root=project_root,
        workspace_root=workspaces_dst if workspaces_dst.exists() else None,
        extra={
            "manifest": manifest,
            "manifest_dir": manifest_dir,
            "zeroclaw_config": zeroclaw_config,
        },
    )
