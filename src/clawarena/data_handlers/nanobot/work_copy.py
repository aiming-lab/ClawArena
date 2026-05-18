"""Nanobot work-copy creation."""

from __future__ import annotations

import os
import json
import shutil
from datetime import datetime
from pathlib import Path

from clawarena.core.types import WorkCopy


def _resolve_log_dir(manifest: dict, project_root: Path) -> Path | None:
    """Resolve llm_log.log_dir from manifest, expanding ${BENCHMARK_ROOT}."""
    llm_log = manifest.get("llm_log", {})
    log_dir_str = llm_log.get("log_dir", "")
    if not log_dir_str:
        return None
    resolved = log_dir_str.replace("${BENCHMARK_ROOT}", project_root.as_posix())
    return Path(resolved)


def build_nanobot_runtime_config(
    nanobot_config: dict,
    workspace_path: Path,
) -> dict:
    """Normalize legacy benchmark config into Nanobot's current schema."""
    rewritten = json.loads(json.dumps(nanobot_config))

    agents = rewritten.setdefault("agents", {})
    defaults = agents.setdefault("defaults", {})
    defaults["workspace"] = str(workspace_path)

    if "model" in rewritten and "model" not in defaults:
        defaults["model"] = rewritten.pop("model")
    defaults.setdefault("provider", "auto")

    if "max_tool_iterations" in rewritten and "max_tool_iterations" not in defaults:
        defaults["max_tool_iterations"] = rewritten.pop("max_tool_iterations")

    tools = rewritten.setdefault("tools", {})
    if "restrict_to_workspace" in rewritten and "restrict_to_workspace" not in tools:
        tools["restrict_to_workspace"] = rewritten.pop("restrict_to_workspace")

    exec_cfg = tools.setdefault("exec", {})
    if "exec_enable" in rewritten and "enable" not in exec_cfg:
        exec_cfg["enable"] = rewritten.pop("exec_enable")
    if "exec_timeout" in rewritten and "timeout" not in exec_cfg:
        exec_cfg["timeout"] = rewritten.pop("exec_timeout")

    providers = rewritten.setdefault("providers", {})
    env_cfg = rewritten.pop("env", None)
    if isinstance(env_cfg, dict) and env_cfg:
        providers.setdefault("custom", {}).setdefault("extra_headers", {})

    return rewritten


def prepare_nanobot_work_copy(
    manifest: dict,
    manifest_dir: Path,
    project_root: Path,
) -> WorkCopy:
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f") + f"_{os.getpid()}"
    work_dir = manifest_dir / "work"
    work_dir.mkdir(exist_ok=True)

    # 1. Copy workspaces (contain sessions/ subdirs with pre-seeded JSONL)
    workspaces_rel = manifest.get("workspaces_dir", "workspaces")
    workspaces_src = manifest_dir / workspaces_rel
    workspaces_dst = work_dir / f"workspaces_{run_id}"
    if workspaces_src.exists():
        shutil.copytree(workspaces_src, workspaces_dst)
    else:
        workspaces_dst.mkdir(parents=True)

    # 2. Create state_dir
    state_dst = work_dir / f"state_{run_id}"
    state_dst.mkdir(parents=True)

    # 3. Generate nanobot config.json in state_dir
    nanobot_config = manifest.get("_nanobot_config", {})
    config_dst = state_dst / "config.json"

    rewritten = build_nanobot_runtime_config(nanobot_config, workspaces_dst)
    config_dst.write_text(
        json.dumps(rewritten, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    log_dir = _resolve_log_dir(manifest, project_root)
    if log_dir:
        log_dir.mkdir(parents=True, exist_ok=True)

    return WorkCopy(
        state_dir=state_dst,
        config_path=config_dst,
        project_root=project_root,
        workspace_root=workspaces_dst if workspaces_dst.exists() else None,
        extra={
            "manifest": manifest,
            "manifest_dir": manifest_dir,
            "nanobot_config": nanobot_config,
            "log_dir": log_dir,
            "nanobot_workspace_path": str(workspaces_dst),
            "nanobot_config_path": str(config_dst),
        },
    )
