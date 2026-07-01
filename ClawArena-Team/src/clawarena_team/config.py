"""Config loading and five-layer priority merge.

Priority (highest to lowest)::

    1. Explicit CLI flags (only items explicitly passed; not passed → no override)
    2. The override file pointed to by ``--config /path/to/{yaml,json}``
    3. Environment variables (``CATEAM_*``)
    4. ``configs/default.yaml``
    5. In-code ``CODE_DEFAULTS`` (fallback)

``configs/default.yaml`` is the example of the "full set of effective parameters":
every configurable key appears once, and those left empty are CLI/env-only. Copy
this file to use as a starting point for ``--config``.

Parameters are flattened by **semantics** rather than by command: keys with the
same semantics are shared (e.g. ``paths.data`` is shared by run/resume/check/stats/
clean), while different semantics are distinguished by prefix (``paths.run_output``
vs ``paths.stats_output``).
"""
from __future__ import annotations

import json
import os
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import yaml

from .provider.multimodal import DEFAULT_MULTIMODAL_CONFIG

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_ROOT = Path(__file__).resolve().parent
DEFAULT_YAML = PACKAGE_ROOT / "configs" / "default.yaml"

# In-code fallback; default.yaml is the authoritative source for the official parameters.
CODE_DEFAULTS: dict[str, Any] = {
    "paths": {
        "data": None,
        "scenario_filter": None,
        "run_output": None,
        "resume_old": None,
        "resume_output": None,
        "stats_output": None,
        "clean_output": None,
        "compare_output": None,
        "tokenizer_override": None,
        "strict": False,
        "concurrency": 1,
        "clean_targets": "work",
    },
    "main": {
        "provider": None,
        "model_id": None,
        "api_base": None,
        "api_key": None,
        "api_key_env": None,
        "modalities": ["text"],
    },
    "model_pool": {
        "llm": {
            "provider": "openai_compat",
            "model_id": "gemma-4-31b-it",
            "api_base": "http://127.0.0.1:8900/v1",
            "api_key": "EMPTY",
            "api_key_env": None,
            "name": "gemma-4-31b-it-text",
            "modalities": ["text"],
        },
        "vlm": {
            "provider": "openai_compat",
            "model_id": "gemma-4-31b-it",
            "api_base": "http://127.0.0.1:8900/v1",
            "api_key": "EMPTY",
            "api_key_env": None,
            "name": "gemma-4-31b-it-vl",
            "modalities": {"text": True, "image": 48, "video": 8},
        },
        "omni": {
            "provider": "openai_compat",
            "model_id": "gemma-4-e4b-it",
            "api_base": "http://127.0.0.1:8902/v1",
            "api_key": "EMPTY",
            "api_key_env": None,
            "name": "gemma-4-e4b-it",
            "modalities": {"text": True, "image": 24, "video": 4, "audio": 4},
        },
    },
    "probe": {
        "enabled": True,
        "timeout_sec": 20,
        "max_tokens": 4,
    },
    "tokenizer": {"source": "qwen3"},
    "chat_template": {"source": "qwen3"},
    "token_limits": {"main_agent": 200000, "subagent": 100000},
    "usage_hint": {
        "always_on_real_user": True,
        "thresholds_pct": [50, 60, 70, 80, 85, 90, 95],
    },
    "agent_loop": {"max_iterations": 80, "tool_call_parallel": True},
    "bash": {"default_timeout_sec": 60, "max_output_bytes": 65536},
    "grep": {"default_max_results": 200, "context_lines": 0},
    "read": {
        "notice_bytes": 32768,
        "hard_bytes": 262144,
        "max_text_bytes": 524288,
        "multimodal_summary_length": 512,
    },
    # The authoritative defaults for the multimodal section live in
    # ``provider/multimodal.py:DEFAULT_MULTIMODAL_CONFIG``; here we just reference
    # the same dict to avoid two-source drift. yaml overrides and the from_dict
    # factory work as usual.
    "multimodal": DEFAULT_MULTIMODAL_CONFIG,
    "scenario": {"final_feedback_mode": "skip", "concurrency_default": 1, "retry": 3},
    "subagent_creation": {"forbid_subagent_tools_in_subagent": True},
    "tools": {
        "enabled": [
            "Read",
            "Write",
            "Edit",
            "Bash",
            "Grep",
            "Glob",
            "CreateSubagent",
            "RunSubagent",
            "ListSubagents",
        ],
    },
    "logging": {"level": "INFO"},
}

_MODEL_POOL_KEYS = ("llm", "vlm", "omni")
_MODEL_POOL_FIELDS = (
    "provider", "model_id", "api_base", "api_key", "api_key_env", "name", "modalities",
)

# Single-field env overrides: env name -> (dotted path, cast)
_FLAT_ENV_OVERRIDES: dict[str, tuple[str, Any]] = {
    "CATEAM_MAIN_TOKEN_LIMIT": ("token_limits.main_agent", int),
    "CATEAM_SUB_TOKEN_LIMIT": ("token_limits.subagent", int),
    "CATEAM_BASH_TIMEOUT": ("bash.default_timeout_sec", int),
    "CATEAM_LOG_LEVEL": ("logging.level", str),
    "CATEAM_TOKENIZER": ("tokenizer.source", str),
    "CATEAM_CHAT_TEMPLATE": ("chat_template.source", str),
    "CATEAM_FINAL_FEEDBACK_MODE": ("scenario.final_feedback_mode", str),
    "CATEAM_SCENARIO_RETRY": ("scenario.retry", int),
    "CATEAM_PROBE_ENABLED": ("probe.enabled", lambda v: v.lower() in {"1", "true", "yes", "on"}),
    "CATEAM_PROBE_TIMEOUT": ("probe.timeout_sec", int),
}


# ---------------------------------------------------------------------------
# Helpers: deep merge + dotted-path set/get
# ---------------------------------------------------------------------------


def _deep_merge(base: dict[str, Any], over: dict[str, Any]) -> dict[str, Any]:
    out = deepcopy(base)
    for k, v in over.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = deepcopy(v)
    return out


def _set_dotted(d: dict[str, Any], dotted: str, value: Any) -> None:
    keys = dotted.split(".")
    cur = d
    for k in keys[:-1]:
        cur = cur.setdefault(k, {})
    cur[keys[-1]] = value


def _get_dotted(d: dict[str, Any], dotted: str, default: Any = None) -> Any:
    cur: Any = d
    for k in dotted.split("."):
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


# ---------------------------------------------------------------------------
# Single-layer source loaders
# ---------------------------------------------------------------------------


def _load_yaml_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f"config file root must be a mapping, got {type(data).__name__}: {path}")
    return data


def _load_json_file(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"config file root must be a mapping, got {type(data).__name__}: {path}")
    return data


def load_config_file(path: Path | None) -> dict[str, Any]:
    """Detect yaml/json by suffix and return a dict (an empty file returns ``{}``)."""
    if path is None:
        return {}
    suffix = path.suffix.lower()
    if suffix in {".yaml", ".yml"}:
        return _load_yaml_file(path)
    if suffix == ".json":
        return _load_json_file(path)
    raise ValueError(f"unsupported config suffix {suffix!r}; expected .yaml/.yml/.json")


def load_env_overrides() -> dict[str, Any]:
    out: dict[str, Any] = {}
    for env_name, (dotted, cast) in _FLAT_ENV_OVERRIDES.items():
        raw = os.environ.get(env_name)
        if raw is None:
            continue
        try:
            _set_dotted(out, dotted, cast(raw))
        except (TypeError, ValueError):
            continue
    # Nested model_pool: CATEAM_MODEL_<KEY>_<FIELD>
    for key in _MODEL_POOL_KEYS:
        for field in _MODEL_POOL_FIELDS:
            env_name = f"CATEAM_MODEL_{key.upper()}_{field.upper()}"
            raw = os.environ.get(env_name)
            if raw is None:
                continue
            value: Any = raw
            if field == "modalities":
                value = [m.strip() for m in raw.split(",") if m.strip()]
            _set_dotted(out, f"model_pool.{key}.{field}", value)
    # main likewise supports CATEAM_MAIN_<FIELD>
    for field in ("provider", "model_id", "api_base", "api_key", "api_key_env", "modalities"):
        env_name = f"CATEAM_MAIN_{field.upper()}"
        raw = os.environ.get(env_name)
        if raw is None:
            continue
        value: Any = raw
        if field == "modalities":
            value = [m.strip() for m in raw.split(",") if m.strip()]
        _set_dotted(out, f"main.{field}", value)
    return out


# ---------------------------------------------------------------------------
# Config body
# ---------------------------------------------------------------------------


@dataclass
class PathsConfig:
    """A strongly-typed view of the ``paths.*`` section. CLI subcommands read just this."""

    data: Optional[Path] = None
    scenario_filter: Optional[str] = None
    tests_ref: str = "tests.json"
    run_output: Optional[Path] = None
    resume_old: Optional[Path] = None
    resume_output: Optional[Path] = None
    stats_output: Optional[Path] = None
    clean_output: Optional[Path] = None
    compare_output: Optional[Path] = None
    tokenizer_override: Optional[str] = None
    strict: bool = False
    concurrency: int = 1
    clean_targets: str = "work"

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "PathsConfig":
        def _path(v: Any) -> Optional[Path]:
            return Path(v).resolve() if v else None

        return cls(
            data=_path(d.get("data")),
            scenario_filter=d.get("scenario_filter"),
            tests_ref=str(d.get("tests_ref", "tests.json") or "tests.json"),
            run_output=_path(d.get("run_output")),
            resume_old=_path(d.get("resume_old")),
            resume_output=_path(d.get("resume_output")),
            stats_output=_path(d.get("stats_output")),
            clean_output=_path(d.get("clean_output")),
            compare_output=_path(d.get("compare_output")),
            tokenizer_override=d.get("tokenizer_override"),
            strict=bool(d.get("strict", False)),
            concurrency=int(d.get("concurrency", 1) or 1),
            clean_targets=str(d.get("clean_targets", "work")),
        )


class Config:
    def __init__(self, data: dict[str, Any], yaml_path: Optional[Path] = None):
        self._data = data
        self.yaml_path = yaml_path

    def get(self, dotted: str, default: Any = None) -> Any:
        return _get_dotted(self._data, dotted, default)

    def as_dict(self) -> dict[str, Any]:
        return deepcopy(self._data)

    def paths(self) -> PathsConfig:
        return PathsConfig.from_dict(self._data.get("paths", {}))


def _prune_none(d: dict[str, Any]) -> dict[str, Any]:
    """Recursively drop keys whose value is None, so empty overrides don't clobber existing values with None."""
    out: dict[str, Any] = {}
    for k, v in d.items():
        if v is None:
            continue
        if isinstance(v, dict):
            cleaned = _prune_none(v)
            if cleaned:
                out[k] = cleaned
        else:
            out[k] = v
    return out


def load_config(
    *,
    yaml_path: Optional[Path] = None,
    config_file: Optional[Path] = None,
    cli_overrides: Optional[dict[str, Any]] = None,
) -> Config:
    """Merge config according to the five-layer priority.

    Args:
        yaml_path: Path overriding the default ``configs/default.yaml``; usually not passed, for testing only.
        config_file: The override file (yaml or json) the user passes via ``-c/--config``.
        cli_overrides: Only the items **explicitly** passed on the CLI (a dict keyed by dotted path).

    The returned :class:`Config` is already the final merged state.
    """
    data: dict[str, Any] = deepcopy(CODE_DEFAULTS)

    # Layer 4: default.yaml
    yp = yaml_path if yaml_path is not None else DEFAULT_YAML
    data = _deep_merge(data, _load_yaml_file(yp))

    # Layer 3: env
    data = _deep_merge(data, load_env_overrides())

    # Layer 2: --config file
    if config_file is not None:
        data = _deep_merge(data, load_config_file(config_file))

    # Layer 1: explicit CLI (accepts both flat-dotted and nested-dict forms)
    if cli_overrides:
        nested: dict[str, Any] = {}
        for k, v in cli_overrides.items():
            if v is None:
                continue
            if "." in k:
                _set_dotted(nested, k, v)
            elif isinstance(v, dict):
                nested[k] = _deep_merge(nested.get(k, {}) if isinstance(nested.get(k), dict) else {}, v)
            else:
                nested[k] = v
        data = _deep_merge(data, _prune_none(nested))

    return Config(data, yaml_path=yp)
