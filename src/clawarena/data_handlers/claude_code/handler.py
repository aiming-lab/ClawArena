"""Claude Code DataHandler — orchestrates all data operations."""

from __future__ import annotations

import json
import logging
import os
import secrets
import shutil
import warnings
from pathlib import Path

from clawarena.core.provider import ConfigError, ModelConfig
from clawarena.core.types import WorkCopy
from clawarena.data_handlers.base import DataHandler

from .session import init_claude_code_session
from .update import execute_claude_code_update
from .validate import validate_claude_code
from .work_copy import prepare_claude_code_work_copy

_logger = logging.getLogger(__name__)
_CCR_PROVIDER_ALIASES = {"ccr", "claude-code-router"}

# Providers claude-code cannot route via the auto-spawned CCR bridge.
# bedrock: AWS SigV4 signing is out of CCR's scope.
# codex: OAuth-bound, not a standard chat/completions endpoint.
_CCR_INCOMPATIBLE = frozenset({"bedrock", "codex"})
_DEFAULT_CLAUDE_CREDENTIALS = Path.home() / ".claude" / ".credentials.json"


def _classify_claude_provider(provider: str) -> str:
    """Return one of: native-oauth / native-api / external-ccr / auto-ccr."""
    if provider == "claude":
        return "native-oauth"
    if provider == "anthropic":
        return "native-api"
    if provider in _CCR_PROVIDER_ALIASES:
        return "external-ccr"
    return "auto-ccr"


class ClaudeCodeDataHandler(DataHandler):

    def load_manifest(self, manifest_path: Path) -> dict:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        config_rel = manifest.get("claude_config_file")
        if config_rel:
            config_path = manifest_path.parent / config_rel
            if config_path.exists():
                manifest["_claude_config"] = json.loads(
                    config_path.read_text(encoding="utf-8")
                )
        return manifest

    def validate(self, manifest, manifest_dir, eval_dir, test_entries):
        return validate_claude_code(manifest, manifest_dir, eval_dir, test_entries)

    def prepare_work_copy(self, manifest, manifest_dir, project_root):
        return prepare_claude_code_work_copy(manifest, manifest_dir, project_root)

    def rebuild_work_copy(self, manifest, manifest_dir, project_root, state_dir, workspace_dir,
                          inplace: bool = False):
        import os
        import shutil
        from datetime import datetime
        from clawarena.data_handlers.claude_code.work_copy import (
            _expand_vars, canonicalize_path, sanitize_path,
        )

        run_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f") + f"_{os.getpid()}"
        work_dir = manifest_dir / "work"
        work_dir.mkdir(exist_ok=True)

        _var_ctx = {**os.environ, "BENCHMARK_ROOT": str(project_root)}
        claude_config = _expand_vars(manifest.get("_claude_config", {}), _var_ctx)

        if inplace:
            # Backup originals, then use them in-place
            backup_state = work_dir / f"state_{run_id}_backup"
            shutil.copytree(state_dir, backup_state)
            print(f"  [backup] state -> {backup_state}")

            workspace_root = None
            if workspace_dir and Path(workspace_dir).exists():
                backup_ws = work_dir / f"workspaces_{run_id}_backup"
                shutil.copytree(workspace_dir, backup_ws)
                print(f"  [backup] workspace -> {backup_ws}")
                workspace_root = Path(workspace_dir)

            return WorkCopy(
                state_dir=state_dir,
                config_path=None,
                project_root=project_root,
                workspace_root=workspace_root,
                extra={
                    "manifest": manifest,
                    "manifest_dir": manifest_dir,
                    "claude_config": claude_config,
                },
            )

        # Default: copy to new location
        # 1. Copy workspace
        workspace_dst = None
        if workspace_dir and Path(workspace_dir).exists():
            workspace_dst = work_dir / f"workspaces_{run_id}"
            shutil.copytree(workspace_dir, workspace_dst)

        # 2. Copy state
        state_dst = work_dir / f"state_{run_id}"
        shutil.copytree(state_dir, state_dst)

        # 3. Remap session JSONL dirs: old sanitized(workspace) → new sanitized(workspace)
        #    because Claude Code resolves sessions via sanitize(canonicalize(cwd))
        if workspace_dst:
            projects_dir = state_dst / "projects"
            if projects_dir.exists():
                for _test_id, agent_info in manifest.get("agents", {}).items():
                    agent_id = agent_info.get("agent_id", _test_id)
                    old_san = sanitize_path(canonicalize_path(
                        str(Path(workspace_dir) / agent_id)))
                    new_san = sanitize_path(canonicalize_path(
                        str(workspace_dst / agent_id)))
                    if old_san != new_san:
                        old_p = projects_dir / old_san
                        new_p = projects_dir / new_san
                        if old_p.exists() and not new_p.exists():
                            old_p.rename(new_p)

        return WorkCopy(
            state_dir=state_dst,
            config_path=None,
            project_root=project_root,
            workspace_root=workspace_dst,
            extra={
                "manifest": manifest,
                "manifest_dir": manifest_dir,
                "claude_config": claude_config,
            },
        )

    def init_session(self, work_copy, test_id):
        return init_claude_code_session(work_copy, test_id)

    def execute_update(self, update_id, work_copy, test_id, session_id):
        execute_claude_code_update(update_id, work_copy, test_id, session_id)

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
        env: dict[str, str] = {}
        route = _classify_claude_provider(model.provider)

        if route == "native-oauth":
            _validate_native_oauth_config(model)
            if model.api_key:
                env["CLAUDE_CODE_OAUTH_TOKEN"] = model.api_key
        elif route == "native-api":
            if model.api_base:
                env["ANTHROPIC_BASE_URL"] = model.api_base
            if model.api_key:
                env["ANTHROPIC_API_KEY"] = model.api_key
        elif route == "external-ccr":
            if model.api_base:
                env["ANTHROPIC_BASE_URL"] = model.api_base
            if model.api_key:
                env["ANTHROPIC_AUTH_TOKEN"] = model.api_key
        else:  # auto-ccr
            runtime = work_copy.extra.get("_claude_ccr_runtime")
            if runtime:
                env.update(_build_ccr_env(runtime["port"], runtime["token"]))
        return env

    def apply_model_config(self, work_copy: WorkCopy, model: ModelConfig) -> None:
        env = work_copy.extra.setdefault("env_overrides", {})
        _clear_ccr_state(work_copy, env)
        route = _classify_claude_provider(model.provider)

        if route == "native-oauth":
            _logger.info("[claude-code] route=native-oauth provider=%s model=%s",
                         model.provider, model.model_id)
            _validate_native_oauth_config(model)
            if model.api_key:
                env["CLAUDE_CODE_OAUTH_TOKEN"] = model.api_key
            elif model.api_base:
                _copy_credentials_file(
                    work_copy.state_dir,
                    Path(model.api_base).expanduser(),
                )
            else:
                # No explicit token: copy ~/.claude/.credentials.json so the CLI
                # can authenticate via the system OAuth session.
                warnings.warn(
                    "provider='claude' native-oauth received neither api_base nor "
                    "api_key; api_base points to a .credentials.json path and "
                    "api_key is a claude-setup-token. Falling back to "
                    f"{_DEFAULT_CLAUDE_CREDENTIALS}",
                    stacklevel=2,
                )
                _copy_credentials_file(work_copy.state_dir, _DEFAULT_CLAUDE_CREDENTIALS)

        elif route == "native-api":
            _logger.info("[claude-code] route=native-api provider=%s model=%s api_base=%s",
                         model.provider, model.model_id, model.api_base or "<default>")
            if model.api_base:
                env["ANTHROPIC_BASE_URL"] = model.api_base
            if model.api_key:
                env["ANTHROPIC_API_KEY"] = model.api_key

        elif route == "external-ccr":
            _logger.info("[claude-code] route=external-ccr provider=%s model=%s api_base=%s",
                         model.provider, model.model_id, model.api_base or "<unset>")
            if model.api_base:
                env["ANTHROPIC_BASE_URL"] = model.api_base
            if model.api_key:
                env["ANTHROPIC_AUTH_TOKEN"] = model.api_key

        else:  # auto-ccr
            if model.provider in _CCR_INCOMPATIBLE:
                raise ConfigError(
                    f"claude-code cannot route provider={model.provider!r} through "
                    f"the built-in CCR bridge (not supported by claude-code-router). "
                    "Use framework='openclaw' for this provider, or switch to "
                    "provider='anthropic' / 'claude' / 'ccr'."
                )
            if not shutil.which("ccr"):
                raise RuntimeError(
                    "claude-code-router (ccr) is required for claude-code "
                    f"provider={model.provider!r}, but 'ccr' was not found in PATH"
                )
            _logger.info("[claude-code] route=auto-ccr provider=%s model=%s api_base=%s",
                         model.provider, model.model_id, model.resolved_api_base())
            work_copy.extra["_claude_ccr_model"] = {
                "provider": model.provider,
                "model_id": model.model_id,
                "api_base": model.resolved_api_base(),
                "api_key": model.api_key or "",
                "token": secrets.token_hex(16),
                "home_dir": str(work_copy.state_dir / ".ccr_home"),
            }


def _clear_ccr_state(work_copy: WorkCopy, env: dict[str, str]) -> None:
    work_copy.extra.pop("_claude_ccr_model", None)
    work_copy.extra.pop("_claude_ccr_runtime", None)
    env.pop("ANTHROPIC_BASE_URL", None)
    env.pop("ANTHROPIC_AUTH_TOKEN", None)
    env.pop("ANTHROPIC_API_KEY", None)
    env.pop("CLAUDE_CODE_OAUTH_TOKEN", None)
    env.pop("NO_PROXY", None)
    env.pop("DISABLE_TELEMETRY", None)
    env.pop("DISABLE_COST_WARNINGS", None)
    env.pop("API_TIMEOUT_MS", None)


def _build_ccr_env(port: int, token: str) -> dict[str, str]:
    return {
        "ANTHROPIC_BASE_URL": f"http://127.0.0.1:{port}",
        "ANTHROPIC_AUTH_TOKEN": token,
        "NO_PROXY": "127.0.0.1",
        "DISABLE_TELEMETRY": "true",
        "DISABLE_COST_WARNINGS": "true",
        "API_TIMEOUT_MS": str(600000),
    }


def _validate_native_oauth_config(model: ModelConfig) -> None:
    if model.api_base and model.api_key:
        raise ConfigError(
            "provider='claude' native-oauth does not allow api_base and api_key "
            "at the same time: api_base points to a .credentials.json path, "
            "while api_key is a claude-setup-token."
        )


def _copy_credentials_file(state_dir: Path, creds_src: Path) -> None:
    """Copy a Claude credentials file into state_dir for native-oauth."""
    if not creds_src.exists():
        raise ConfigError(
            f"Claude native-oauth credentials file not found: {creds_src}"
        )
    if not creds_src.is_file():
        raise ConfigError(
            f"Claude native-oauth credentials path is not a file: {creds_src}"
        )
    shutil.copy2(creds_src, state_dir / ".credentials.json")

