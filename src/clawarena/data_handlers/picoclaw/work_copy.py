"""PicoClaw work-copy creation."""

from __future__ import annotations

import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

import re

from clawarena.core.types import WorkCopy
from clawarena.utils import get_project_root

_ENV_VAR_RE = re.compile(r"\$\{(\w+)\}")


def _expand_env_vars(obj):
    """Recursively replace ${VAR} placeholders with environment variable values."""
    if isinstance(obj, str):
        return _ENV_VAR_RE.sub(lambda m: os.environ.get(m.group(1), m.group(0)), obj)
    if isinstance(obj, dict):
        return {k: _expand_env_vars(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_expand_env_vars(item) for item in obj]
    return obj


def build_picoclaw_runtime_config(
    picoclaw_config: dict,
    workspace_path: Path,
) -> dict:
    """Build a runtime config whose workspace matches the active agent."""
    rewritten = dict(picoclaw_config)
    # Use the current schema path so PicoClaw does not auto-migrate and
    # overwrite benchmark-specific hooks or model routing.
    rewritten["version"] = 1
    agents_defaults = dict(rewritten.get("agents", {}).get("defaults", {}))
    agents_defaults["workspace"] = str(workspace_path)
    rewritten.setdefault("agents", {})["defaults"] = agents_defaults
    return _expand_env_vars(rewritten)

_HOOK_SCRIPT = get_project_root() / "helpers" / "picoclaw_hook.py"


def _resolve_log_dir(manifest: dict, project_root: Path) -> Path | None:
    """Resolve llm_log.log_dir from manifest, expanding ${BENCHMARK_ROOT}."""
    llm_log = manifest.get("llm_log", {})
    log_dir_str = llm_log.get("log_dir", "")
    if not log_dir_str:
        return None
    resolved = log_dir_str.replace("${BENCHMARK_ROOT}", project_root.as_posix())
    return Path(resolved)


def _write_security_yml(state_dst: Path, api_key: str, model_name: str) -> None:
    """Write .security.yml alongside config.json so picoclaw can load the API key.

    PicoClaw loads .security.yml from the same directory as config.json.
    The model_list key must match the model_name used in agents.defaults.
    """
    content = (
        "model_list:\n"
        f"  {model_name}:\n"
        "    api_keys:\n"
        f'      - "{api_key}"\n'
    )
    (state_dst / ".security.yml").write_text(content, encoding="utf-8")


def sync_security_yml(
    target_dir: Path,
    source_dir: Path | None = None,
    model_name: str | None = None,
    api_key: str | None = None,
) -> Path | None:
    """Ensure a runtime config directory has a sibling .security.yml."""
    target_dir.mkdir(parents=True, exist_ok=True)
    sec_path = target_dir / ".security.yml"
    if source_dir is not None:
        source_sec = source_dir / ".security.yml"
        if source_sec.exists():
            shutil.copy2(source_sec, sec_path)

    if model_name is None or api_key is None:
        return sec_path if sec_path.exists() else None

    try:
        import yaml
    except ImportError:
        if not sec_path.exists():
            _write_security_yml(target_dir, api_key, model_name)
        return sec_path

    sec: dict = {}
    if sec_path.exists():
        sec = yaml.safe_load(sec_path.read_text(encoding="utf-8")) or {}
    sec.setdefault("model_list", {})[model_name] = {"api_keys": [api_key]}
    sec_path.write_text(
        yaml.safe_dump(sec, default_flow_style=False, sort_keys=True),
        encoding="utf-8",
    )
    return sec_path


def prepare_picoclaw_work_copy(
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

    # 1b. Copy memory session files into each agent workspace's sessions/ directory.
    # PicoClaw loads session history from {workspace}/sessions/{sanitized_key}.jsonl,
    # so the pre-seeded files must be present there before the first run.
    memory_rel = manifest.get("memory_dir", "memory")
    memory_src = manifest_dir / memory_rel
    if memory_src.exists():
        for test_id, agent_info in manifest.get("agents", {}).items():
            agent_id = agent_info.get("agent_id", test_id)
            session_key = agent_info.get("session_key", "")
            if not session_key:
                continue
            sanitized = session_key.replace(":", "_").replace("/", "_")
            memory_file = memory_src / f"{sanitized}.jsonl"
            meta_file = memory_src / f"{sanitized}.meta.json"
            if memory_file.exists():
                ws_sessions_dir = workspaces_dst / agent_id / "sessions"
                ws_sessions_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(memory_file, ws_sessions_dir / f"{sanitized}.jsonl")
                if meta_file.exists():
                    shutil.copy2(meta_file, ws_sessions_dir / f"{sanitized}.meta.json")

    # 2. Create state_dir (PICOCLAW_HOME)
    state_dst = work_dir / f"state_{run_id}"
    state_dst.mkdir(parents=True)

    # 3. Build runtime config: start from the committed template (which already
    # contains model_list, api_base, etc.) and point the default workspace at
    # the shared workspaces root. Per-agent invocations will narrow this to the
    # concrete agent workspace at runtime.
    picoclaw_config = manifest.get("_picoclaw_config", {})
    config_dst = state_dst / "config.json"
    rewritten = build_picoclaw_runtime_config(picoclaw_config, workspaces_dst)

    config_dst.write_text(
        json.dumps(rewritten, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # 4. Write .security.yml with the API key (same dir as config.json).
    # The env var name is read from the manifest so no var names are hardcoded here.
    model_name = rewritten.get("agents", {}).get("defaults", {}).get("model_name", "benchmark")
    api_key_env = manifest.get("picoclaw_api_key_env", "")
    api_key = os.getenv(api_key_env) or os.getenv("OPENAI_API_KEY", "")
    _write_security_yml(state_dst, api_key, model_name)

    # 5. Inject hooks config for LLM logging (if llm_log is configured).
    log_dir = _resolve_log_dir(manifest, project_root)
    if log_dir and _HOOK_SCRIPT.exists():
        log_dir.mkdir(parents=True, exist_ok=True)
        rewritten.setdefault("hooks", {})
        rewritten["hooks"]["enabled"] = True
        rewritten["hooks"].setdefault("processes", {})
        rewritten["hooks"]["processes"]["llm_logger"] = {
            "enabled": True,
            "command": [sys.executable, str(_HOOK_SCRIPT)],
            "intercept": ["before_llm", "after_llm"],
            "observe": ["turn_end"],
            "env": {
                "CLAWARENA_PICOCLAW_LOG_DIR": str(log_dir),
            },
        }
        # Re-write config with hooks injected
        config_dst.write_text(
            json.dumps(rewritten, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    return WorkCopy(
        state_dir=state_dst,
        config_path=config_dst,
        project_root=project_root,
        workspace_root=workspaces_dst if workspaces_dst.exists() else None,
        extra={
            "manifest": manifest,
            "manifest_dir": manifest_dir,
            "picoclaw_config": picoclaw_config,
            "log_dir": log_dir,
        },
    )
