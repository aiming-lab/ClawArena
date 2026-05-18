"""OpenClaw work-copy creation and path remapping."""

from __future__ import annotations

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

from clawarena.core.types import WorkCopy


def _replace_str_in_json(obj: Any, old: str, new: str) -> Any:
    """Recursively replace old with new in all string values."""
    if isinstance(obj, dict):
        return {k: _replace_str_in_json(v, old, new) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_replace_str_in_json(v, old, new) for v in obj]
    if isinstance(obj, str) and old in obj:
        return obj.replace(old, new)
    return obj


def _build_agents_list(
    manifest: dict,
    state_root: Path,
    workspace_root: Path,
    *,
    project_root: Path | None = None,
    use_benchmark_root: bool = False,
    template: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Build openclaw agents.list entries from manifest agents."""
    built: list[dict[str, Any]] = []
    template = template or {}

    for test_id, agent_info in manifest.get("agents", {}).items():
        agent_id = agent_info.get("agent_id", test_id)
        workspace_rel = agent_info.get("workspace", f"workspaces/{agent_id}")
        agent_dir_rel = agent_info.get("agent_dir", f"state/agents/{agent_id}")

        workspace_path = workspace_root / agent_id
        agent_dir_path = state_root / "agents" / agent_id / "agent"

        if use_benchmark_root:
            if project_root is None:
                raise ValueError("project_root is required when use_benchmark_root=True")
            manifest_dir = state_root.parent
            workspace_src = (manifest_dir / workspace_rel).resolve()
            agent_dir_src = (manifest_dir / agent_dir_rel).resolve()
            workspace_value = "${BENCHMARK_ROOT}/" + workspace_src.relative_to(project_root).as_posix()
            agent_dir_value = "${BENCHMARK_ROOT}/" + agent_dir_src.relative_to(project_root).as_posix()
        else:
            workspace_value = workspace_path.as_posix()
            agent_dir_value = agent_dir_path.as_posix()

        built.append({
            "id": agent_id,
            "name": agent_id,
            "skills": list(template.get("skills", [])),
            "workspace": workspace_value,
            "agentDir": agent_dir_value,
        })

    return built


def prepare_openclaw_work_copy(
    manifest: dict,
    manifest_dir: Path,
    project_root: Path,
) -> WorkCopy:
    """Create isolated work copy from manifest data.

    Copies state_dir and workspaces into a sibling work/ folder,
    rewrites paths in openclaw.json.
    """
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f") + f"_{os.getpid()}"

    state_rel = manifest.get("state_dir", "state")
    state_src = manifest_dir / state_rel
    config_rel = manifest.get("config_file", "config/openclaw.json")
    config_src = manifest_dir / config_rel
    workspaces_rel = manifest.get("workspaces_dir", "workspaces")
    workspaces_src = manifest_dir / workspaces_rel

    work_dir = manifest_dir / "work"
    work_dir.mkdir(exist_ok=True)

    state_dst = work_dir / f"state_{run_id}"
    workspaces_dst = work_dir / f"workspaces_{run_id}"

    # Copy state directory
    if state_src.exists():
        shutil.copytree(state_src, state_dst)
    else:
        state_dst.mkdir(parents=True)

    # Copy config into state work copy
    config_dst = state_dst / "openclaw.json"
    if config_src.exists():
        shutil.copy2(config_src, config_dst)

    # Copy workspaces and remap agent configs
    if config_dst.exists():
        config = json.loads(config_dst.read_text(encoding="utf-8"))

        # Remap state dir paths (use as_posix() for cross-platform JSON string matching)
        config = _replace_str_in_json(config, state_src.as_posix(), state_dst.as_posix())

        # Try relative path forms
        try:
            orig_rel = state_src.relative_to(project_root).as_posix()
            new_rel = state_dst.relative_to(project_root).as_posix()
            config = _replace_str_in_json(config, "./" + orig_rel, "./" + new_rel)
            config = _replace_str_in_json(
                config,
                "${BENCHMARK_ROOT}/" + orig_rel,
                state_dst.as_posix(),
            )
        except ValueError:
            pass

        # Copy workspaces per agent using manifest as the source of truth.
        for test_id, agent_info in manifest.get("agents", {}).items():
            agent_id = agent_info.get("agent_id", test_id)
            workspace_rel = agent_info.get("workspace", f"workspaces/{agent_id}")
            ws_src = manifest_dir / workspace_rel
            ws_dst = workspaces_dst / agent_id
            if ws_src.exists():
                shutil.copytree(ws_src, ws_dst, dirs_exist_ok=True)
            else:
                ws_dst.mkdir(parents=True, exist_ok=True)

        template_agent = {}
        agents_list = config.get("agents", {}).get("list", [])
        if agents_list:
            template_agent = agents_list[0]
        config.setdefault("agents", {})["list"] = _build_agents_list(
            manifest,
            state_root=state_dst,
            workspace_root=workspaces_dst,
            template=template_agent,
        )

        # Ensure agent-level session visibility
        tools_cfg = config.setdefault("tools", {})
        sessions_cfg = tools_cfg.setdefault("sessions", {})
        sessions_cfg.setdefault("visibility", "agent")

        config_dst.write_text(
            json.dumps(config, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    # Resolve log dir from config
    log_dir = _resolve_log_dir(config_dst, project_root)

    return WorkCopy(
        state_dir=state_dst,
        config_path=config_dst,
        project_root=project_root,
        workspace_root=workspaces_dst if workspaces_dst.exists() else None,
        extra={
            "manifest": manifest,
            "manifest_dir": manifest_dir,
            "log_dir": log_dir,
        },
    )


def _resolve_log_dir(config_path: Path, project_root: Path) -> Path | None:
    """Read log directory from openclaw.json plugins config.

    Supports two plugin config formats:
    - Dict format (``plugins.entries.<name>.config.logDir``)
    - List format (``plugins.list[n].config.logDir``)
    """
    if not config_path.exists():
        return None
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except Exception:
        return None

    plugins_cfg = config.get("plugins", {})

    # Dict format: plugins.entries.<plugin-name>.config.logDir
    entries = plugins_cfg.get("entries", {})
    if isinstance(entries, dict):
        for _name, entry in entries.items():
            if not isinstance(entry, dict):
                continue
            log_dir_str = entry.get("config", {}).get("logDir") or entry.get("config", {}).get("log_dir")
            if log_dir_str:
                resolved = log_dir_str.replace("${BENCHMARK_ROOT}", project_root.as_posix())
                return Path(resolved)

    # List format: plugins.list[n].config.logDir  (legacy / alternative)
    for p in plugins_cfg.get("list", []):
        cfg = p.get("config", {})
        log_dir_str = cfg.get("logDir") or cfg.get("log_dir")
        if log_dir_str:
            resolved = log_dir_str.replace("${BENCHMARK_ROOT}", project_root.as_posix())
            return Path(resolved)

    return None
