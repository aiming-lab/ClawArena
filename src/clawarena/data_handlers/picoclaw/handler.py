"""PicoClaw DataHandler — orchestrates all data operations."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from clawarena.core.provider import ConfigError, ModelConfig
from clawarena.core.types import WorkCopy
from clawarena.data_handlers.base import DataHandler
from clawarena.data_handlers.jsonl_utils import trim_llm_log_messages

from .session import init_picoclaw_session
from .update import execute_picoclaw_update
from .validate import validate_picoclaw
from .work_copy import prepare_picoclaw_work_copy, sync_security_yml

_PROTOCOL_MAP: dict[str, str] = {
    "openai":    "openai",
    "anthropic": "anthropic-messages",
    "google":    "gemini",
    "bedrock":   "bedrock",
    "ollama":    "ollama",
    "azure":     "azure",
}


class PicoClawDataHandler(DataHandler):

    def load_manifest(self, manifest_path: Path) -> dict:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        config_rel = manifest.get("picoclaw_config_file")
        if config_rel:
            config_path = manifest_path.parent / config_rel
            if config_path.exists():
                manifest["_picoclaw_config"] = json.loads(
                    config_path.read_text(encoding="utf-8")
                )
        return manifest

    def validate(self, manifest, manifest_dir, eval_dir, test_entries):
        return validate_picoclaw(manifest, manifest_dir, eval_dir, test_entries)

    def prepare_work_copy(self, manifest, manifest_dir, project_root):
        return prepare_picoclaw_work_copy(manifest, manifest_dir, project_root)

    def init_session(self, work_copy, test_id):
        return init_picoclaw_session(work_copy, test_id)

    def execute_update(self, update_id, work_copy, test_id, session_id):
        execute_picoclaw_update(update_id, work_copy, test_id, session_id)

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
        # picoclaw writes logs keyed by its internal SessionKey (picoclaw_storage_key),
        # not the CLI session key we pass via -s.  Resolve via manifest agents.
        manifest = work_copy.extra.get("manifest", {})
        log_key = session_id  # fallback
        for agent_info in manifest.get("agents", {}).values():
            if agent_info.get("session_key") == session_id:
                storage_key = agent_info.get("picoclaw_storage_key")
                if storage_key:
                    log_key = storage_key
                break
        session_dir = log_dir / log_key
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

    def build_model_env(self, work_copy: WorkCopy, model: ModelConfig) -> dict[str, str]:
        if model.provider == "claude":
            raise ConfigError(
                "PicoClaw does not support provider='claude'. "
                "Use provider='anthropic' with an API key, "
                "or switch to claude_code / openclaw."
            )
        cfg_path = work_copy.state_dir / "config.json"
        if not cfg_path.exists():
            return {}
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        protocol = _PROTOCOL_MAP.get(model.provider, "openai")
        entry: dict = {"model_name": "clawarena", "model": f"{protocol}/{model.model_id}"}
        if model.api_base:
            entry["api_base"] = model.api_base
        if model.api_key:
            entry["api_key"] = model.api_key
        model_list: list = cfg.setdefault("model_list", [])
        model_list[:] = [m for m in model_list if m.get("model_name") != "clawarena"]
        model_list.insert(0, entry)
        cfg.setdefault("agents", {}).setdefault("defaults", {})["model_name"] = "clawarena"
        overlay_dir = _overlay_dir(work_copy, model)
        overlay = overlay_dir / "config.json"
        overlay.write_text(json.dumps(cfg, indent=2, ensure_ascii=False))
        sync_security_yml(
            overlay_dir,
            source_dir=work_copy.state_dir,
            model_name="clawarena" if model.api_key else None,
            api_key=model.api_key,
        )
        return {"PICOCLAW_CONFIG": str(overlay)}

    def apply_model_config(self, work_copy: WorkCopy, model: ModelConfig) -> None:
        if model.provider == "claude":
            raise ConfigError(
                "PicoClaw does not support provider='claude'. "
                "Use provider='anthropic' with an API key, "
                "or switch to claude_code / openclaw."
            )
        cfg_path = work_copy.state_dir / "config.json"
        if not cfg_path.exists():
            return
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))

        protocol = _PROTOCOL_MAP.get(model.provider, "openai")
        entry: dict = {
            "model_name": "clawarena",
            "model": f"{protocol}/{model.model_id}",
        }
        if model.api_base:
            entry["api_base"] = model.api_base
        if model.api_key:
            entry["api_key"] = model.api_key

        model_list: list = cfg.setdefault("model_list", [])
        model_list[:] = [m for m in model_list if m.get("model_name") != "clawarena"]
        model_list.insert(0, entry)
        cfg.setdefault("agents", {}).setdefault("defaults", {})["model_name"] = "clawarena"
        cfg_path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False))

        if model.api_key:
            sync_security_yml(
                work_copy.state_dir,
                model_name="clawarena",
                api_key=model.api_key,
            )


def _overlay_dir(work_copy: WorkCopy, model: ModelConfig) -> Path:
    """Create a deterministic overlay directory for per-scene config copies."""
    import hashlib
    key = f"{model.api_base}:{model.api_key or ''}:{model.model_id}"
    h = hashlib.md5(key.encode()).hexdigest()[:8]
    d = work_copy.state_dir / f".metaclaw_overlay_{h}"
    d.mkdir(parents=True, exist_ok=True)
    return d
