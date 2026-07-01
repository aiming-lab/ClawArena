"""State isolation and snapshot management.

Each task runs in an isolated temporary directory with its own openclaw
configuration. Snapshots allow saving/restoring state for checkpointing.
"""

from __future__ import annotations

import copy
import json
import shutil
import tempfile
import uuid
from pathlib import Path
from typing import Any

BASE_CONFIGS_DIR = Path(__file__).parent.parent / "data" / "base_configs"

# Default minimal openclaw configuration
DEFAULT_CONFIG: dict[str, Any] = {
    "agent": {
        "model": "anthropic/claude-sonnet-4-5-20250929",
    },
    "agents": {
        "defaults": {
            "model": {
                "primary": "anthropic/claude-sonnet-4-5-20250929",
                "fallbacks": [],
            }
        }
    },
    "tools": {},
    "gateway": {
        "bind": "loopback",
        "port": 18789,
        "auth": {"mode": "token", "token": "test-token-for-env"},
        "remote": {
            "url": "ws://127.0.0.1:18789",
            "token": "test-token-for-env",
        },
    },
    "channels": {},
}


class StateManager:
    """Manages isolated state directories for task execution."""

    def __init__(self, base_config_name: str = "default"):
        self._base_config_name = base_config_name
        self._state_dir: Path | None = None
        self._snapshots: dict[str, Path] = {}

    @property
    def state_dir(self) -> Path:
        if self._state_dir is None:
            raise RuntimeError("State not initialized. Call initialize() first.")
        return self._state_dir

    @property
    def config_path(self) -> Path:
        return self.state_dir / "openclaw.json"

    @property
    def workspace_dir(self) -> Path:
        return self.state_dir / "workspace"

    @property
    def sessions_dir(self) -> Path:
        return self.state_dir / "sessions"

    @property
    def credentials_dir(self) -> Path:
        return self.state_dir / "credentials"

    def initialize(self) -> Path:
        """Create an isolated state directory from a base config."""
        self._state_dir = Path(tempfile.mkdtemp(prefix="openclaw_env_"))

        base_config_dir = BASE_CONFIGS_DIR / self._base_config_name
        if base_config_dir.exists():
            shutil.copytree(base_config_dir, self._state_dir, dirs_exist_ok=True)
        else:
            # Create default structure
            self._create_default_state()

        return self._state_dir

    def apply_state_overrides(self, overrides: dict[str, Any]) -> None:
        """Apply per-task state file overrides after the base config is copied."""
        if not overrides:
            return
        if self._state_dir is None:
            raise RuntimeError("State not initialized. Call initialize() first.")
        for rel_path, value in overrides.items():
            target = self.state_dir / rel_path
            target.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(value, str):
                target.write_text(value)
            else:
                with open(target, 'w') as f:
                    json.dump(value, f, indent=2, ensure_ascii=False)

    def _create_default_state(self) -> None:
        """Create a default openclaw state directory."""
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.credentials_dir.mkdir(parents=True, exist_ok=True)

        config = _build_default_config()
        with open(self.config_path, "w") as f:
            json.dump(config, f, indent=2)

        # Create default workspace files
        (self.workspace_dir / "AGENTS.md").write_text(
            "# Agent Instructions\n\nDefault agent configuration.\n"
        )
        (self.workspace_dir / "SOUL.md").write_text(
            "# Assistant Personality\n\nYou are a helpful assistant.\n"
        )

    def get_config(self) -> dict[str, Any]:
        """Read the current openclaw configuration."""
        if not self.config_path.exists():
            return {}
        with open(self.config_path) as f:
            return json.load(f)

    def set_config(self, config: dict[str, Any]) -> None:
        """Write the openclaw configuration."""
        with open(self.config_path, "w") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    def update_config(self, updates: dict[str, Any]) -> dict[str, Any]:
        """Merge updates into the current configuration."""
        config = self.get_config()
        _deep_merge(config, updates)
        self.set_config(config)
        return config

    def save_snapshot(self) -> str:
        """Save a snapshot of the current state. Returns snapshot ID."""
        snapshot_id = str(uuid.uuid4())[:8]
        snapshot_dir = Path(tempfile.mkdtemp(prefix=f"openclaw_snap_{snapshot_id}_"))
        shutil.copytree(self.state_dir, snapshot_dir, dirs_exist_ok=True)
        self._snapshots[snapshot_id] = snapshot_dir
        return snapshot_id

    def load_snapshot(self, snapshot_id: str) -> None:
        """Restore state from a snapshot."""
        if snapshot_id not in self._snapshots:
            raise ValueError(f"Snapshot {snapshot_id} not found")
        snapshot_dir = self._snapshots[snapshot_id]
        # Clear current state and copy from snapshot
        shutil.rmtree(self.state_dir)
        shutil.copytree(snapshot_dir, self.state_dir)

    def get_env_vars(self) -> dict[str, str]:
        """Get environment variables that point to this isolated state."""
        return {
            "OPENCLAW_STATE_DIR": str(self.state_dir),
            "OPENCLAW_CONFIG_PATH": str(self.config_path),
            "HOME": str(self.state_dir),  # Isolate home directory
        }

    def cleanup(self) -> None:
        """Remove the state directory and all snapshots."""
        if self._state_dir and self._state_dir.exists():
            shutil.rmtree(self._state_dir, ignore_errors=True)
        for snapshot_dir in self._snapshots.values():
            if snapshot_dir.exists():
                shutil.rmtree(snapshot_dir, ignore_errors=True)
        self._snapshots.clear()
        self._state_dir = None


def _deep_merge(base: dict, updates: dict) -> None:
    """Recursively merge updates into base dict."""
    for key, value in updates.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value


def _build_default_config() -> dict[str, Any]:
    """Build isolated default config with best-effort host gateway alignment."""
    config = copy.deepcopy(DEFAULT_CONFIG)
    overrides = _host_gateway_overrides()
    if overrides:
        _deep_merge(config, overrides)
    return config


def _host_gateway_overrides() -> dict[str, Any]:
    """Read host OpenClaw config and derive gateway token/url overrides.

    This keeps isolated task configs able to talk to the user's running local
    gateway (hybrid/real modes) without requiring manual token synchronization.
    """
    host_config_path = Path.home() / ".openclaw" / "openclaw.json"
    if not host_config_path.exists():
        return {}

    try:
        with open(host_config_path) as f:
            host_cfg = json.load(f)
    except Exception:
        return {}

    gateway = host_cfg.get("gateway")
    if not isinstance(gateway, dict):
        return {}

    auth = gateway.get("auth")
    auth_token = auth.get("token") if isinstance(auth, dict) else None
    auth_mode = auth.get("mode") if isinstance(auth, dict) else None

    remote = gateway.get("remote")
    remote_token = remote.get("token") if isinstance(remote, dict) else None
    remote_url = remote.get("url") if isinstance(remote, dict) else None

    bind = gateway.get("bind")
    port = gateway.get("port")
    if not isinstance(port, int):
        port = 18789

    # Prefer remote token if explicitly present, otherwise use auth token.
    resolved_token = remote_token or auth_token
    if not isinstance(resolved_token, str) or not resolved_token:
        return {}

    if not isinstance(remote_url, str) or not remote_url:
        remote_url = f"ws://127.0.0.1:{port}"

    result: dict[str, Any] = {
        "gateway": {
            "remote": {
                "url": remote_url,
                "token": resolved_token,
            },
            "auth": {
                "mode": auth_mode if isinstance(auth_mode, str) and auth_mode else "token",
                "token": resolved_token,
            },
            "port": port,
        }
    }
    if isinstance(bind, str) and bind:
        result["gateway"]["bind"] = bind
    return result
