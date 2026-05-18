"""mm-metaclaw configuration — dataclass and tests.json parser."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path

_ENV_VAR_RE = re.compile(r"\$\{([^}:]+?)(?::-([^}]*))?\}")


def _expand_env(value: str) -> str:
    """Expand ``${VAR}`` and ``${VAR:-default}`` patterns in a string."""
    def _repl(m: re.Match) -> str:
        return os.environ.get(m.group(1), m.group(2) if m.group(2) is not None else "")
    return _ENV_VAR_RE.sub(_repl, value)


# ---------------------------------------------------------------------------
# Structured config
# ---------------------------------------------------------------------------

#: Modules supported by gateway-modules (RL excluded by design).
SUPPORTED_MODULES = frozenset({"proxy", "memory", "skill", "multimodal_image", "multimodal_video"})


@dataclass
class MmMetaClawConfig:
    """Parsed representation of the ``mm_metaclaw`` section in tests.json."""

    # Gateway location
    gateway_dir: Path
    """Absolute path to the gateway-modules project root (CWD for the daemon)."""

    # Module selection
    enabled_modules: list[str] = field(default_factory=lambda: ["proxy"])
    """Which gateway modules to enable.  Must be a subset of SUPPORTED_MODULES."""

    # Transport path
    transport_mode: str = "proxy"
    """
    ``"proxy"`` — OpenClaw points its model provider at MM-MetaClaw's
    OpenAI-compatible proxy.

    ``"http_plugin"`` — OpenClaw keeps its own upstream provider config and
    reaches MM-MetaClaw only through framework plugin HTTP calls.
    """

    # Hook behaviour
    hook_mode: str = "proxy"
    """
    ``"proxy"`` — modules exercised transparently; hooks only call ``/collect``
    endpoints at trigger points.

    ``"http"`` — hooks explicitly call ``/inject`` *before* each round and
    ``/collect`` *after* each round, testing endpoints in isolation.
    """

    # Network
    proxy_host: str = "127.0.0.1"
    proxy_port: int = 0  # 0 = auto-discover a free port at start time

    # Upstream LLM credentials (written to gateway config.yaml)
    upstream_api_base: str = ""
    upstream_api_key: str = ""
    upstream_model: str = ""

    # Agent-visible model name
    served_model_name: str = "mm-metaclaw"
    max_context_tokens: int = 50000

    # Isolation / lifecycle
    per_scene_isolation: bool = False
    managed: bool = True


# ---------------------------------------------------------------------------
# Trigger config (from tests.json, not gateway config)
# ---------------------------------------------------------------------------


@dataclass
class TriggerCfg:
    every_n_rounds: int = 0
    every_n_scenes: int = 0
    on_last_round: bool = False


def parse_trigger_config(mmmc_raw: dict) -> TriggerCfg:
    """Parse ``mm_metaclaw.memory_trigger`` from tests.json into a TriggerCfg."""
    raw = mmmc_raw.get("memory_trigger", {})
    return TriggerCfg(
        every_n_rounds=int(_expand_env(str(raw.get("every_n_rounds", 0)))),
        every_n_scenes=int(_expand_env(str(raw.get("every_n_scenes", 0)))),
        on_last_round=bool(raw.get("on_last_round", False)),
    )


# ---------------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------------


def load_config(mmmc_raw: dict) -> MmMetaClawConfig:
    """Build an ``MmMetaClawConfig`` from the ``mm_metaclaw`` dict in tests.json.

    All string fields support ``${VAR}`` and ``${VAR:-default}`` expansion.
    """
    gw_dir_raw = mmmc_raw.get("gateway_dir", "")
    if not gw_dir_raw:
        raise ValueError("mm_metaclaw.gateway_dir must be set in tests.json")
    gateway_dir = Path(_expand_env(str(gw_dir_raw))).expanduser().resolve()

    modules_raw = mmmc_raw.get("enabled_modules", ["proxy"])
    enabled_modules = [str(m) for m in modules_raw]
    unknown = set(enabled_modules) - SUPPORTED_MODULES
    if unknown:
        raise ValueError(
            f"mm_metaclaw.enabled_modules contains unsupported modules: {sorted(unknown)}. "
            f"Supported: {sorted(SUPPORTED_MODULES)}"
        )

    transport_mode = str(mmmc_raw.get("transport_mode", "proxy"))
    if transport_mode not in ("proxy", "http_plugin"):
        raise ValueError(
            "mm_metaclaw.transport_mode must be 'proxy' or 'http_plugin', "
            f"got: {transport_mode!r}"
        )

    if transport_mode == "proxy":
        if "proxy" not in enabled_modules:
            enabled_modules = ["proxy", *enabled_modules]
    else:
        enabled_modules = [m for m in enabled_modules if m != "proxy"]

    hook_mode = str(mmmc_raw.get("hook_mode", "proxy"))
    if hook_mode not in ("proxy", "http"):
        raise ValueError(f"mm_metaclaw.hook_mode must be 'proxy' or 'http', got: {hook_mode!r}")

    return MmMetaClawConfig(
        gateway_dir=gateway_dir,
        enabled_modules=enabled_modules,
        transport_mode=transport_mode,
        hook_mode=hook_mode,
        proxy_host=str(mmmc_raw.get("proxy_host", "127.0.0.1")),
        proxy_port=int(mmmc_raw.get("port", 0)),
        upstream_api_base=_expand_env(str(mmmc_raw.get("upstream_api_base", ""))),
        upstream_api_key=_expand_env(str(mmmc_raw.get("upstream_api_key", ""))),
        upstream_model=_expand_env(str(mmmc_raw.get("upstream_model", ""))),
        served_model_name=str(mmmc_raw.get("served_model_name", "mm-metaclaw")),
        max_context_tokens=int(mmmc_raw.get("max_context_tokens", 50000)),
        per_scene_isolation=bool(mmmc_raw.get("per_scene_isolation", False)),
        managed=bool(mmmc_raw.get("managed", True)),
    )
