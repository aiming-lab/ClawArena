"""Codex DataHandler — orchestrates all data operations."""

from __future__ import annotations

import json
from pathlib import Path

from clawarena.core.provider import ModelConfig
from clawarena.core.types import WorkCopy
from clawarena.data_handlers.base import DataHandler

from .session import init_codex_session
from .update import execute_codex_update
from .validate import validate_codex
from .work_copy import prepare_codex_work_copy


class CodexDataHandler(DataHandler):

    def load_manifest(self, manifest_path: Path) -> dict:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        config_rel = manifest.get("codex_config_file")
        if config_rel:
            config_path = manifest_path.parent / config_rel
            if config_path.exists():
                manifest["_codex_config"] = json.loads(
                    config_path.read_text(encoding="utf-8")
                )
        return manifest

    def validate(self, manifest, manifest_dir, eval_dir, test_entries):
        return validate_codex(manifest, manifest_dir, eval_dir, test_entries)

    def prepare_work_copy(self, manifest, manifest_dir, project_root):
        return prepare_codex_work_copy(manifest, manifest_dir, project_root)

    def init_session(self, work_copy, test_id):
        return init_codex_session(work_copy, test_id)

    def execute_update(self, update_id, work_copy, test_id, session_id):
        execute_codex_update(update_id, work_copy, test_id, session_id)

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

    def build_model_env(self, work_copy: WorkCopy, model: ModelConfig) -> dict[str, str]:
        env: dict[str, str] = {"OPENAI_MODEL": model.model_id}
        if model.api_base:
            env["OPENAI_BASE_URL"] = model.api_base
        if model.api_key:
            env["OPENAI_API_KEY"] = model.api_key
        return env

    def apply_model_config(self, work_copy: WorkCopy, model: ModelConfig) -> None:
        env = work_copy.extra.setdefault("env_overrides", {})
        if model.api_base:
            env["OPENAI_BASE_URL"] = model.api_base
        env["OPENAI_MODEL"] = model.model_id
        if model.api_key:
            env["OPENAI_API_KEY"] = model.api_key
