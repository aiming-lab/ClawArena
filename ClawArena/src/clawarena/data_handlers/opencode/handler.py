"""OpenCode DataHandler — orchestrates all data operations."""

from __future__ import annotations

import json
from pathlib import Path

from clawarena.core.provider import ModelConfig
from clawarena.core.types import WorkCopy
from clawarena.data_handlers.base import DataHandler

from .session import init_opencode_session
from .update import execute_opencode_update
from .validate import validate_opencode
from .work_copy import prepare_opencode_work_copy


class OpenCodeDataHandler(DataHandler):

    def load_manifest(self, manifest_path: Path) -> dict:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        config_rel = manifest.get("opencode_config_file")
        if config_rel:
            config_path = manifest_path.parent / config_rel
            if config_path.exists():
                manifest["_opencode_config"] = json.loads(
                    config_path.read_text(encoding="utf-8")
                )
        return manifest

    def validate(self, manifest, manifest_dir, eval_dir, test_entries):
        return validate_opencode(manifest, manifest_dir, eval_dir, test_entries)

    def prepare_work_copy(self, manifest, manifest_dir, project_root):
        return prepare_opencode_work_copy(manifest, manifest_dir, project_root)

    def init_session(self, work_copy, test_id):
        return init_opencode_session(work_copy, test_id)

    def execute_update(self, update_id, work_copy, test_id, session_id):
        execute_opencode_update(update_id, work_copy, test_id, session_id)

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
        return None

    def count_session_tokens(self, state_dir, test_id):
        return 0

    def apply_model_config(self, work_copy: WorkCopy, model: ModelConfig) -> None:
        cfg_path = work_copy.state_dir / "opencode.json"
        if not cfg_path.exists():
            return
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        provider_entry: dict = {}
        if model.api_base:
            provider_entry["api_base"] = model.api_base
        if model.api_key:
            provider_entry["api_key"] = model.api_key
        cfg.setdefault("provider", {})[model.provider] = provider_entry
        cfg["default_model"] = f"{model.provider}/{model.model_id}"
        cfg_path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False))

    def build_model_env(self, work_copy: WorkCopy, model: ModelConfig) -> dict[str, str]:
        cfg_path = work_copy.state_dir / "opencode.json"
        if not cfg_path.exists():
            return {}
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        provider_entry: dict = {}
        if model.api_base:
            provider_entry["api_base"] = model.api_base
        if model.api_key:
            provider_entry["api_key"] = model.api_key
        cfg.setdefault("provider", {})[model.provider] = provider_entry
        cfg["default_model"] = f"{model.provider}/{model.model_id}"
        overlay = _overlay_dir(work_copy, model) / "opencode.json"
        overlay.write_text(json.dumps(cfg, indent=2, ensure_ascii=False))
        return {"OPENCODE_CONFIG": str(overlay)}


def _overlay_dir(work_copy: WorkCopy, model: ModelConfig) -> Path:
    """Create a deterministic overlay directory for per-scene config copies."""
    import hashlib
    key = f"{model.api_base}:{model.api_key or ''}:{model.model_id}"
    h = hashlib.md5(key.encode()).hexdigest()[:8]
    d = work_copy.state_dir / f".metaclaw_overlay_{h}"
    d.mkdir(parents=True, exist_ok=True)
    return d
