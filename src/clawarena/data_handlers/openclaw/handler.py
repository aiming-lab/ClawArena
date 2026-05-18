"""OpenClaw DataHandler — orchestrates all data operations."""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path

from clawarena.core.provider import ConfigError, ModelConfig
from clawarena.core.types import WorkCopy
from clawarena.data_handlers.base import DataHandler

from .session import init_openclaw_session
from .update import execute_openclaw_update
from .validate import validate_openclaw
from .work_copy import prepare_openclaw_work_copy

# Provider → (api_value, auth_value, use_auth_header)
_PROVIDER_API_MAP: dict[str, tuple[str, str | None, bool]] = {
    "openai":    ("openai-completions",      None,       True),
    "anthropic": ("anthropic-messages",      "api-key",  False),
    "google":    ("google-generative-ai",    None,       True),
    "bedrock":   ("bedrock-converse-stream", "aws-sdk",  False),
    "ollama":    ("ollama",                  None,       False),
    "azure":     ("openai-completions",      None,       True),
}


class OpenClawDataHandler(DataHandler):
    """Data handler for the OpenClaw framework."""

    def load_manifest(self, manifest_path: Path) -> dict:
        return json.loads(manifest_path.read_text(encoding="utf-8"))

    def validate(
        self,
        manifest: dict,
        manifest_dir: Path,
        eval_dir: Path,
        test_entries: list[dict],
    ) -> list[str]:
        return validate_openclaw(manifest, manifest_dir, eval_dir, test_entries)

    def prepare_work_copy(
        self,
        manifest: dict,
        manifest_dir: Path,
        project_root: Path,
    ) -> WorkCopy:
        return prepare_openclaw_work_copy(manifest, manifest_dir, project_root)

    def init_session(self, work_copy: WorkCopy, test_id: str) -> str:
        return init_openclaw_session(work_copy, test_id)

    def execute_update(
        self,
        update_id: str,
        work_copy: WorkCopy,
        test_id: str,
        session_id: str,
    ) -> None:
        execute_openclaw_update(update_id, work_copy, test_id, session_id)

    def resolve_workspace(
        self, work_copy: WorkCopy, test_id: str
    ) -> Path | None:
        manifest = work_copy.extra.get("manifest", {})
        agent_info = manifest.get("agents", {}).get(test_id, {})
        agent_id = agent_info.get("agent_id", test_id)
        ws_rel = agent_info.get("workspace")
        if not ws_rel:
            return None
        # workspace_root is remapped during work_copy creation using agent_id
        if work_copy.workspace_root:
            return work_copy.workspace_root / agent_id
        manifest_dir: Path | None = work_copy.extra.get("manifest_dir")
        if manifest_dir:
            return manifest_dir / ws_rel
        return None

    def read_llm_log(
        self, work_copy: WorkCopy, session_id: str, after_ts: float
    ) -> dict | None:
        log_dir: Path | None = work_copy.extra.get("log_dir")
        if not log_dir:
            return None
        return _read_newest_log(log_dir, session_id, after_ts)

    def count_session_tokens(self, state_dir: Path, test_id: str) -> int:
        return 0

    # ── Model config ─────────────────────────────────

    def build_model_env(self, work_copy: WorkCopy, model: ModelConfig) -> dict[str, str]:
        cfg_path = work_copy.state_dir / "openclaw.json"
        if not cfg_path.exists():
            cfg_path = work_copy.extra.get("config_path") or cfg_path
        if not cfg_path.exists():
            return {}
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        if model.provider == "claude":
            _apply_claude_oauth(work_copy, cfg, model)
        elif model.provider == "codex":
            _apply_codex_oauth(work_copy, cfg, model)
        else:
            _apply_api_key(cfg, model)
        overlay_dir = _overlay_dir(work_copy, model)
        overlay_path = overlay_dir / "openclaw.json"
        overlay_path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False))
        return {"OPENCLAW_CONFIG_PATH": str(overlay_path)}

    def configure_mm_metaclaw_plugin(
        self,
        work_copy: WorkCopy,
        plugin_dir: Path,
    ) -> None:
        """Enable the local MM-MetaClaw OpenClaw plugin in the work-copy config.

        Only called when mm_metaclaw.transport_mode='http_plugin' is active.
        Has no effect on any other inference path.
        """
        cfg_path = work_copy.state_dir / "openclaw.json"
        if not cfg_path.exists():
            cfg_path = work_copy.extra.get("config_path") or cfg_path
        if not cfg_path.exists():
            return

        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        plugins = cfg.setdefault("plugins", {})
        load_cfg = plugins.setdefault("load", {})
        load_paths = load_cfg.setdefault("paths", [])
        plugin_dir_str = str(_ensure_mm_metaclaw_plugin_alias(work_copy, plugin_dir))
        if plugin_dir_str not in load_paths:
            load_paths.append(plugin_dir_str)

        entries = plugins.setdefault("entries", {})
        entry = entries.setdefault("mm-metaclaw", {})
        entry["enabled"] = True

        allow = plugins.setdefault("allow", [])
        if "mm-metaclaw" not in allow:
            allow.append("mm-metaclaw")

        cfg_path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False))

    def apply_model_config(self, work_copy: WorkCopy, model: ModelConfig) -> None:
        cfg_path = work_copy.state_dir / "openclaw.json"
        if not cfg_path.exists():
            cfg_path = work_copy.extra.get("config_path") or cfg_path
        if not cfg_path.exists():
            return
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))

        if model.provider == "claude":
            _apply_claude_oauth(work_copy, cfg, model)
        elif model.provider == "codex":
            _apply_codex_oauth(work_copy, cfg, model)
        else:
            _apply_api_key(cfg, model)

        cfg_path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False))


def _apply_api_key(cfg: dict, model: ModelConfig) -> None:
    """Standard API key / provider injection path."""
    from clawarena.core.provider import DEFAULT_API_BASE

    api_val, auth_val, auth_header = _PROVIDER_API_MAP.get(
        model.provider, ("openai-completions", None, True)
    )
    model_entry: dict = {"id": model.model_id, "name": model.model_id, "api": api_val}
    if model.extra:
        model_entry.update(model.extra)
    provider_entry: dict = {
        "baseUrl": model.api_base or DEFAULT_API_BASE.get(model.provider, ""),
        "api": api_val,
        "models": [model_entry],
    }
    if model.api_key:
        provider_entry["apiKey"] = model.api_key
    if auth_val:
        provider_entry["auth"] = auth_val
    if auth_header:
        provider_entry["authHeader"] = True

    cfg.setdefault("models", {}).setdefault("providers", {})[model.provider] = provider_entry
    (cfg.setdefault("agents", {})
         .setdefault("defaults", {})
         .setdefault("model", {}))["primary"] = f"{model.provider}/{model.model_id}"


def _apply_claude_oauth(work_copy: WorkCopy, cfg: dict, model: ModelConfig) -> None:
    """Claude subscription OAuth (setup-token) path."""
    cfg.setdefault("auth", {}).setdefault("profiles", {})["anthropic:manual"] = {
        "provider": "anthropic",
        "mode": "token",
    }
    (cfg.setdefault("agents", {})
         .setdefault("defaults", {})
         .setdefault("model", {}))["primary"] = f"anthropic/{model.model_id}"

    if not model.api_key:
        return
    auth_profile_content = json.dumps({
        "version": 1,
        "profiles": {
            "anthropic:manual": {
                "type": "token",
                "provider": "anthropic",
                "token": model.api_key,
            }
        }
    }, indent=2)

    for agent in cfg.get("agents", {}).get("list", []):
        agent_dir = agent.get("agentDir", "")
        if not agent_dir:
            continue
        auth_path = Path(agent_dir) / "auth-profiles.json"
        auth_path.parent.mkdir(parents=True, exist_ok=True)
        auth_path.write_text(auth_profile_content)


def _apply_codex_oauth(work_copy: WorkCopy, cfg: dict, model: ModelConfig) -> None:
    """Codex subscription OAuth path using a token JSON file."""
    model_entry: dict = {"id": model.model_id, "name": model.model_id}
    if model.extra:
        model_entry.update(model.extra)
    cfg.setdefault("models", {}).setdefault("providers", {})["openai-codex"] = {
        "baseUrl": "https://chatgpt.com/backend-api",
        "api": "openai-codex-responses",
        "models": [model_entry],
    }
    auth_cfg = cfg.setdefault("auth", {})
    auth_cfg.setdefault("profiles", {})["openai-codex:default"] = {
        "provider": "openai-codex",
        "mode": "oauth",
    }
    auth_cfg.setdefault("order", {})["openai-codex"] = ["openai-codex:default"]
    (cfg.setdefault("agents", {})
         .setdefault("defaults", {})
         .setdefault("model", {}))["primary"] = f"openai-codex/{model.model_id}"

    if not model.api_key:
        raise ConfigError(
            "provider='codex' requires api_key to be a JSON file path containing OAuth tokens."
        )

    token_payload = _load_codex_token_payload(Path(model.api_key))
    auth_profile = {
        "type": "oauth",
        "provider": "openai-codex",
        "access": token_payload["access"],
        "refresh": token_payload["refresh"],
        "accountId": token_payload["accountId"],
        "expires": token_payload["expires"],
    }
    auth_profile_content = json.dumps({
        "version": 1,
        "profiles": {
            "openai-codex:default": auth_profile,
        },
        "order": {
            "openai-codex": ["openai-codex:default"],
        },
    }, indent=2)

    for agent in cfg.get("agents", {}).get("list", []):
        agent_dir = agent.get("agentDir", "")
        if not agent_dir:
            continue
        auth_path = Path(agent_dir) / "auth-profiles.json"
        auth_path.parent.mkdir(parents=True, exist_ok=True)
        auth_path.write_text(auth_profile_content)


def _load_codex_token_payload(auth_json_path: Path) -> dict[str, str | int]:
    if not auth_json_path.exists():
        raise ConfigError(
            f"provider='codex' token file not found: {auth_json_path}"
        )

    try:
        raw = json.loads(auth_json_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ConfigError(
            f"provider='codex' token file is not valid JSON: {auth_json_path}"
        ) from exc

    tokens = raw.get("tokens")
    if not isinstance(tokens, dict):
        raise ConfigError(
            "provider='codex' token file must contain a 'tokens' object."
        )

    access = tokens.get("access_token")
    refresh = tokens.get("refresh_token")
    account_id = tokens.get("account_id")
    last_refresh = raw.get("last_refresh")
    if not all(isinstance(v, str) and v for v in (access, refresh, account_id, last_refresh)):
        raise ConfigError(
            "provider='codex' token file must contain non-empty "
            "'tokens.access_token', 'tokens.refresh_token', 'tokens.account_id', and 'last_refresh'."
        )

    try:
        refreshed_at = datetime.fromisoformat(last_refresh.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ConfigError(
            "provider='codex' token file has invalid 'last_refresh' timestamp."
        ) from exc

    expires_at = refreshed_at.astimezone(timezone.utc) + timedelta(days=30)
    return {
        "access": access,
        "refresh": refresh,
        "accountId": account_id,
        "expires": int(expires_at.timestamp() * 1000),
    }


def _ensure_mm_metaclaw_plugin_alias(work_copy: WorkCopy, plugin_dir: Path) -> str:
    """Create a symlink under work_copy so the plugin directory name matches its manifest id."""
    plugin_root = work_copy.state_dir / "plugins"
    plugin_root.mkdir(parents=True, exist_ok=True)
    alias_path = plugin_root / "mm-metaclaw"
    target = plugin_dir.resolve()

    if alias_path.exists() or alias_path.is_symlink():
        if alias_path.is_symlink() and alias_path.resolve() == target:
            return str(alias_path)
        if alias_path.is_dir() and not alias_path.is_symlink():
            shutil.rmtree(alias_path)
        else:
            alias_path.unlink()

    alias_path.symlink_to(target, target_is_directory=True)
    return str(alias_path)


def _overlay_dir(work_copy: WorkCopy, model: ModelConfig) -> Path:
    """Create a deterministic overlay directory for per-scene config copies."""
    import hashlib
    key = f"{model.api_base}:{model.api_key or ''}:{model.model_id}"
    h = hashlib.md5(key.encode()).hexdigest()[:8]
    d = work_copy.state_dir / f".metaclaw_overlay_{h}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _read_newest_log(
    log_dir: Path, session_id: str, after_ts: float
) -> dict | None:
    """Read newest log file created after after_ts."""
    from clawarena.data_handlers.jsonl_utils import trim_llm_log_messages

    session_log_dir = log_dir / session_id
    if not session_log_dir.exists():
        return None
    candidates = [
        p for p in session_log_dir.glob("*.json")
        if p.stat().st_mtime > after_ts
    ]
    if not candidates:
        all_files = list(session_log_dir.glob("*.json"))
        if not all_files:
            return None
        candidates = all_files
    newest = max(candidates, key=lambda p: p.stat().st_mtime)
    try:
        data = json.loads(newest.read_text(encoding="utf-8"))
        return trim_llm_log_messages(data)
    except Exception:
        return None
