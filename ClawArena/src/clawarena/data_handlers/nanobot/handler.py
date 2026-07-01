"""Nanobot DataHandler — orchestrates all data operations."""

from __future__ import annotations

import json
from pathlib import Path

from clawarena.core.provider import ConfigError, ModelConfig
from clawarena.core.types import WorkCopy
from clawarena.data_handlers.base import DataHandler
from clawarena.data_handlers.jsonl_utils import trim_llm_log_messages

from .session import init_nanobot_session
from .update import execute_nanobot_update
from .validate import validate_nanobot
from .work_copy import prepare_nanobot_work_copy

_PROVIDER_KEY_MAP: dict[str, str] = {
    "openai":    "openai",
    "anthropic": "anthropic",
    "google":    "gemini",
    "ollama":    "ollama",
    "azure":     "azure_openai",
}

_DIRECT_PROVIDER_KEYS = {"anthropic", "gemini", "ollama", "azure_openai"}


class NanobotDataHandler(DataHandler):

    def load_manifest(self, manifest_path: Path) -> dict:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        config_rel = manifest.get("nanobot_config_file")
        if config_rel:
            config_path = manifest_path.parent / config_rel
            if config_path.exists():
                manifest["_nanobot_config"] = json.loads(
                    config_path.read_text(encoding="utf-8")
                )
        return manifest

    def validate(self, manifest, manifest_dir, eval_dir, test_entries):
        return validate_nanobot(manifest, manifest_dir, eval_dir, test_entries)

    def prepare_work_copy(self, manifest, manifest_dir, project_root):
        return prepare_nanobot_work_copy(manifest, manifest_dir, project_root)

    def init_session(self, work_copy, test_id):
        return init_nanobot_session(work_copy, test_id)

    def execute_update(self, update_id, work_copy, test_id, session_id):
        execute_nanobot_update(update_id, work_copy, test_id, session_id)

    def resolve_workspace(self, work_copy, test_id):
        manifest = work_copy.extra.get("manifest", {})
        agent_info = manifest.get("agents", {}).get(test_id, {})
        agent_id = agent_info.get("agent_id", test_id)
        if work_copy.workspace_root:
            ws = work_copy.workspace_root / agent_id
            if ws.exists():
                return ws
        return None

    def read_llm_log(self, work_copy, session_id, after_ts):
        log_dir: Path | None = work_copy.extra.get("log_dir")
        if not log_dir:
            return None
        session_dir = log_dir / session_id
        if not session_dir.exists():
            return None
        candidates = [
            p for p in session_dir.glob("*.json")
            if p.stat().st_mtime > after_ts
        ]
        if not candidates:
            all_files = list(session_dir.glob("*.json"))
            if not all_files:
                return None
            candidates = all_files
        newest = max(candidates, key=lambda p: p.stat().st_mtime)
        try:
            data = json.loads(newest.read_text(encoding="utf-8"))
            return trim_llm_log_messages(data)
        except Exception:
            return None

    def count_session_tokens(self, state_dir, test_id):
        return 0

    def apply_model_config(self, work_copy: WorkCopy, model: ModelConfig) -> None:
        if model.provider == "claude":
            raise ConfigError(
                "nanobot does not support provider='claude'. "
                "Use provider='anthropic' with an API key, "
                "or switch to claude_code / openclaw."
            )
        cfg_path = work_copy.state_dir / "config.json"
        if not cfg_path.exists():
            return
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))

        provider_key, provider_name, model_name = _resolve_nanobot_model_target(model)
        cfg.setdefault("providers", {})[provider_key] = _build_provider_entry(model)
        defaults = cfg.setdefault("agents", {}).setdefault("defaults", {})
        defaults["model"] = model_name
        defaults["provider"] = provider_name

        cfg_path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False))

    def build_model_env(self, work_copy: WorkCopy, model: ModelConfig) -> dict[str, str]:
        if model.provider == "claude":
            raise ConfigError(
                "nanobot does not support provider='claude'. "
                "Use provider='anthropic' with an API key, "
                "or switch to claude_code / openclaw."
            )
        cfg_path = work_copy.state_dir / "config.json"
        if not cfg_path.exists():
            return {}
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        provider_key, provider_name, model_name = _resolve_nanobot_model_target(model)
        cfg.setdefault("providers", {})[provider_key] = _build_provider_entry(model)
        defaults = cfg.setdefault("agents", {}).setdefault("defaults", {})
        defaults["model"] = model_name
        defaults["provider"] = provider_name
        overlay = _overlay_dir(work_copy, model) / "config.json"
        overlay.write_text(json.dumps(cfg, indent=2, ensure_ascii=False))
        return {"NANOBOT_CONFIG": str(overlay)}


def _build_provider_entry(model: ModelConfig) -> dict:
    provider_entry: dict = {}
    if model.api_key:
        provider_entry["apiKey"] = model.api_key
    if model.api_base:
        provider_entry["apiBase"] = model.api_base
    return provider_entry


def _resolve_nanobot_model_target(model: ModelConfig) -> tuple[str, str, str]:
    provider_key = _PROVIDER_KEY_MAP.get(model.provider, "custom")
    if model.api_base and provider_key not in _DIRECT_PROVIDER_KEYS:
        return "custom", "custom", model.model_id
    if provider_key == "custom":
        return "custom", "custom", model.model_id
    return provider_key, "auto", f"{model.provider}/{model.model_id}"


def _overlay_dir(work_copy: WorkCopy, model: ModelConfig) -> Path:
    """Create a deterministic overlay directory for per-scene config copies."""
    import hashlib
    key = f"{model.api_base}:{model.api_key or ''}:{model.model_id}"
    h = hashlib.md5(key.encode()).hexdigest()[:8]
    d = work_copy.state_dir / f".metaclaw_overlay_{h}"
    d.mkdir(parents=True, exist_ok=True)
    return d
