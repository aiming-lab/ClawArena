"""Claude Code work-copy creation with sanitized path alignment."""

from __future__ import annotations

import json
import os
import re
import shutil
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Any

from clawarena.core.types import WorkCopy

# ── ${var} expansion ──

_VAR_RE = re.compile(r"\$\{([^}]+)\}")


def _expand_vars(obj: Any, ctx: dict[str, str]) -> Any:
    """Recursively replace ``${VAR}`` placeholders in all string values.

    Unknown variables are left unchanged (i.e. ``${UNKNOWN}`` stays as-is).
    *ctx* is typically ``os.environ`` merged with built-in keys like
    ``BENCHMARK_ROOT``.
    """
    if isinstance(obj, str):
        return _VAR_RE.sub(lambda m: ctx.get(m.group(1), m.group(0)), obj)
    if isinstance(obj, dict):
        return {k: _expand_vars(v, ctx) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_expand_vars(v, ctx) for v in obj]
    return obj


# ── sanitize (must match claude-agent-sdk sessions.py exactly) ──

MAX_SANITIZED_LENGTH = 200
_SANITIZE_RE = re.compile(r"[^a-zA-Z0-9]")


def _simple_hash(s: str) -> str:
    h = 0
    for ch in s:
        h = (h << 5) - h + ord(ch)
        h = h & 0xFFFFFFFF
        if h >= 0x80000000:
            h -= 0x100000000
    h = abs(h)
    if h == 0:
        return "0"
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    out = []
    n = h
    while n > 0:
        out.append(digits[n % 36])
        n //= 36
    return "".join(reversed(out))


def sanitize_path(name: str) -> str:
    sanitized = _SANITIZE_RE.sub("-", name)
    if len(sanitized) <= MAX_SANITIZED_LENGTH:
        return sanitized
    return f"{sanitized[:MAX_SANITIZED_LENGTH]}-{_simple_hash(name)}"


def canonicalize_path(d: str) -> str:
    try:
        resolved = os.path.realpath(d)
        return unicodedata.normalize("NFC", resolved)
    except OSError:
        return unicodedata.normalize("NFC", d)


# ── work copy ──

def prepare_claude_code_work_copy(
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

    # 2. Copy settings.json into each workspace's .claude/
    _var_ctx: dict[str, str] = {**os.environ, "BENCHMARK_ROOT": str(project_root)}
    claude_config: dict = _expand_vars(manifest.get("_claude_config", {}), _var_ctx)
    settings_rel = claude_config.get("settings_file")
    if settings_rel:
        settings_src = manifest_dir / settings_rel
        if settings_src.exists():
            for agent_dir in workspaces_dst.iterdir():
                if agent_dir.is_dir():
                    dst = agent_dir / ".claude" / "settings.json"
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(settings_src, dst)

    # 3. Create state_dir (CLAUDE_CONFIG_DIR points here)
    #    Session JSONL goes to state_dir/projects/{sanitized_cwd}/{uuid}.jsonl
    state_dst = work_dir / f"state_{run_id}"
    state_dst.mkdir(parents=True)

    projects_rel = manifest.get("projects_dir", "state/projects")
    projects_src = manifest_dir / projects_rel

    for test_id, agent_info in manifest.get("agents", {}).items():
        agent_id = agent_info.get("agent_id", test_id)
        session_uuid = agent_info.get("session", "")
        if not session_uuid:
            continue

        # Compute workspace path → canonicalize → sanitize
        # Must use absolute path: SDK sets PWD=str(cwd) and claude uses PWD for session lookup
        ws_path = workspaces_dst.resolve() / agent_id
        canonical = canonicalize_path(str(ws_path))
        sanitized = sanitize_path(canonical)

        # Target directory
        target_dir = state_dst / "projects" / sanitized
        target_dir.mkdir(parents=True, exist_ok=True)

        # Copy session JSONL to sanitized path
        src_file = projects_src / test_id / f"{session_uuid}.jsonl"
        if src_file.exists():
            shutil.copy2(src_file, target_dir / f"{session_uuid}.jsonl")

    if state_dst.is_dir():
        dst2 = state_dst / "settings.json"
        shutil.copy2(settings_src, dst2)

    return WorkCopy(
        state_dir=state_dst,
        config_path=None,
        project_root=project_root,
        workspace_root=workspaces_dst if workspaces_dst.exists() else None,
        extra={
            "manifest": manifest,
            "manifest_dir": manifest_dir,
            "claude_config": claude_config,
        },
    )
