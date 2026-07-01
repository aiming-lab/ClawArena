"""ZeroClaw DataHandler — orchestrates all data operations."""

from __future__ import annotations

import json
from pathlib import Path

from clawarena.core.provider import ConfigError, ModelConfig
from clawarena.core.types import WorkCopy
from clawarena.data_handlers.base import DataHandler

from .session import init_zeroclaw_session
from .update import execute_zeroclaw_update
from .validate import validate_zeroclaw
from .work_copy import prepare_zeroclaw_work_copy


class ZeroClawDataHandler(DataHandler):

    def load_manifest(self, manifest_path: Path) -> dict:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        config_rel = manifest.get("zeroclaw_config_file")
        if config_rel:
            config_path = manifest_path.parent / config_rel
            if config_path.exists():
                manifest["_zeroclaw_config"] = json.loads(
                    config_path.read_text(encoding="utf-8")
                )
        return manifest

    def validate(self, manifest, manifest_dir, eval_dir, test_entries):
        return validate_zeroclaw(manifest, manifest_dir, eval_dir, test_entries)

    def prepare_work_copy(self, manifest, manifest_dir, project_root):
        return prepare_zeroclaw_work_copy(manifest, manifest_dir, project_root)

    def init_session(self, work_copy, test_id):
        return init_zeroclaw_session(work_copy, test_id)

    def execute_update(self, update_id, work_copy, test_id, session_id):
        execute_zeroclaw_update(update_id, work_copy, test_id, session_id)

    def resolve_workspace(self, work_copy, test_id):
        manifest = work_copy.extra.get("manifest", {})
        agent_info = manifest.get("agents", {}).get(test_id, {})
        agent_id = agent_info.get("agent_id", test_id)
        if work_copy.workspace_root:
            # ZeroClaw uses workspace_root/agent_id/workspace/ as the actual workspace
            ws_sub = work_copy.workspace_root / agent_id / "workspace"
            if ws_sub.exists():
                return ws_sub.resolve()
            ws = work_copy.workspace_root / agent_id
            if ws.exists():
                return ws.resolve()
        return None

    def read_llm_log(self, work_copy, session_id, after_ts):
        return None

    def count_session_tokens(self, state_dir, test_id):
        return 0

    def apply_model_config(self, work_copy: WorkCopy, model: ModelConfig) -> None:
        if model.provider == "claude":
            raise ConfigError(
                "ZeroClaw does not support provider='claude'. "
                "Use provider='anthropic' with an API key, "
                "or switch to claude_code / openclaw."
            )
        # Update state_dir config (used by overlay copies in per-scene mode)
        cfg_path = work_copy.state_dir / "config.toml"
        if cfg_path.exists():
            _apply_zeroclaw_toml(cfg_path, model)
        # Update workspace_root/.zeroclaw/config.toml (primary config for zeroclaw)
        if work_copy.workspace_root:
            ws_cfg = work_copy.workspace_root / ".zeroclaw" / "config.toml"
            if ws_cfg.exists():
                _apply_zeroclaw_toml(ws_cfg, model)
        # Inject api_key via env var (avoids zeroclaw false-positive warning
        # on unknown config key — its known-keys check skips Option::None fields).
        if model.api_key:
            zc = work_copy.extra.setdefault("zeroclaw_config", {})
            zc.setdefault("env", {})["ZEROCLAW_API_KEY"] = model.api_key

    def build_model_env(self, work_copy: WorkCopy, model: ModelConfig) -> dict[str, str]:
        if model.provider == "claude":
            raise ConfigError(
                "ZeroClaw does not support provider='claude'. "
                "Use provider='anthropic' with an API key, "
                "or switch to claude_code / openclaw."
            )
        cfg_path = work_copy.state_dir / "config.toml"
        if not cfg_path.exists():
            return {}
        overlay_dir = _overlay_dir(work_copy, model)
        overlay = overlay_dir / "config.toml"
        try:
            import shutil
            shutil.copy2(cfg_path, overlay)
        except OSError:
            return {}
        _apply_zeroclaw_toml(overlay, model)
        # zeroclaw reads config.toml from ZEROCLAW_CONFIG_DIR directory
        env: dict[str, str] = {"ZEROCLAW_CONFIG_DIR": str(overlay_dir)}
        if model.api_key:
            env["ZEROCLAW_API_KEY"] = model.api_key
        return env


def _apply_zeroclaw_toml(cfg_path: Path, model: ModelConfig) -> None:
    """Overwrite zeroclaw config.toml top-level provider fields.

    ZeroClaw uses top-level ``default_provider``, ``default_model``,
    ``api_key``, and ``api_url`` — NOT nested ``[provider.<name>]`` sections.

    Also injects ``[autonomy]`` with ``workspace_only = false`` so the agent
    can access project files that live alongside (not inside) the zeroclaw
    workspace directory.
    """
    try:
        import tomli
        import tomli_w
        cfg = tomli.loads(cfg_path.read_text(encoding="utf-8"))
        cfg["default_provider"] = model.provider
        if model.model_id:
            cfg["default_model"] = model.model_id
            if "model" in cfg and isinstance(cfg["model"], dict):
                del cfg["model"]
        api_base = model.resolved_api_base()
        if api_base:
            cfg["api_url"] = api_base
        cfg.pop("api_key", None)
        # Grant full autonomy so the agent can access project/ alongside workspace/
        autonomy = cfg.setdefault("autonomy", {})
        autonomy["level"] = "full"
        autonomy["workspace_only"] = False
        cfg_path.write_text(tomli_w.dumps(cfg))
    except ImportError:
        text = cfg_path.read_text(encoding="utf-8")
        if model.model_id:
            text = _toml_remove_section(text, "model")
            text = _toml_set_toplevel(text, "default_model", model.model_id)
        text = _toml_set_toplevel(text, "default_provider", model.provider)
        api_base = model.resolved_api_base()
        if api_base:
            text = _toml_set_toplevel(text, "api_url", api_base)
        # Ensure [autonomy] section exists with correct values
        text = _toml_remove_section(text, "autonomy")
        text += '\n[autonomy]\nlevel = "full"\nworkspace_only = false\n'
        cfg_path.write_text(text)


def _toml_set_toplevel(text: str, key: str, value: str) -> str:
    """Set or replace a top-level TOML key (before any [section] header)."""
    import re
    # Find first section header position
    first_section = re.search(r"^\[", text, re.MULTILINE)
    boundary = first_section.start() if first_section else len(text)
    top = text[:boundary]
    rest = text[boundary:]
    # Replace existing key or append
    pattern = re.compile(rf'^{re.escape(key)}\s*=.*$', re.MULTILINE)
    new_line = f'{key} = "{value}"'
    if pattern.search(top):
        top = pattern.sub(new_line, top, count=1)
    else:
        top = top.rstrip("\n") + f"\n{new_line}\n"
    return top + rest


def _toml_remove_section(text: str, section: str) -> str:
    """Remove an entire [section] block (header + body) from TOML text."""
    import re
    pattern = re.compile(
        rf'^\[{re.escape(section)}\]\s*\n(?:(?!\[).+\n)*',
        re.MULTILINE,
    )
    return pattern.sub("", text)


def _overlay_dir(work_copy: WorkCopy, model: ModelConfig) -> Path:
    """Create a deterministic overlay directory for per-scene config copies."""
    import hashlib
    key = f"{model.api_base}:{model.api_key or ''}:{model.model_id}"
    h = hashlib.md5(key.encode()).hexdigest()[:8]
    d = work_copy.state_dir / f".metaclaw_overlay_{h}"
    d.mkdir(parents=True, exist_ok=True)
    return d
