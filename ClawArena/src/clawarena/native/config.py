"""配置加载与六层优先级合并。

优先级（自高至低）::

    1. CLI 显式 flag（仅显式传入的项，未传 → 不参与覆盖）
    2. ``--config-overrides '<json>'`` 内联 JSON 覆盖（所有子命令通用）
    3. ``--config /path/to/{yaml,json}`` 指向的覆盖文件
    4. 环境变量（``ARCBENCH_*``）
    5. ``configs/default.yaml``
    6. 代码内 ``CODE_DEFAULTS``（兜底）

``configs/default.yaml`` 即「有效参数全集」示例：每个可配置键均出现一次，仅留空者表示
CLI/env-only。复制此文件即可作为 ``--config`` 起点。

参数按**语义**铺平而非按命令：相同语义共用一个键（如 ``paths.data`` 被 run/resume/
check/stats/clean 共用），异义则前缀区分（``paths.run_output`` vs ``paths.stats_output``）。
"""
from __future__ import annotations

import json
import os
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_ROOT = Path(__file__).resolve().parent
DEFAULT_YAML = PACKAGE_ROOT / "configs" / "default.yaml"

# 代码内兜底；正式参数以 default.yaml 为权威。
CODE_DEFAULTS: dict[str, Any] = {
    "paths": {
        "data": None,
        "arc_filter": None,
        "run_output": None,
        "resume_old": None,
        "resume_output": None,
        "stats_output": None,
        "clean_output": None,
        "tokenizer_override": None,
        "strict": False,
        "concurrency": 1,
        "clean_targets": "work",
    },
    # 三 role 模型配置。``main`` 必须最终有 provider + model_id；``subagent`` /
    # ``compaction`` 任一字段缺省时从 main 继承（详见
    # ``arcbench.provider.registry.parse_model_json``）。``compaction.modalities``
    # 由代码强制 ["text"]，配置不可改动。
    "models": {
        "main": {
            "provider": None,
            "model_id": None,
            "api_base": None,
            "api_key": None,
            "api_key_env": None,
            "modalities": ["text"],
        },
        "subagent": {
            "provider": None,
            "model_id": None,
            "api_base": None,
            "api_key": None,
            "api_key_env": None,
            "modalities": None,
        },
        "compaction": {
            "provider": None,
            "model_id": None,
            "api_base": None,
            "api_key": None,
            "api_key_env": None,
        },
    },
    "probe": {"enabled": True, "timeout_sec": 20, "max_tokens": 4},
    "tokenizer": {"source": "qwen3"},
    "chat_template": {"source": "qwen3"},
    "token_limits": {"main_agent": 200000},
    "usage_hint": {
        "always_on_real_user": True,
        "thresholds_pct": [50, 60, 70, 80, 85, 90, 95],
    },
    "memory": {
        "notification_enabled": True,
        # 须为 usage_hint.thresholds_pct 的子集；越界项启动时剔除并 warn。
        "persist_reminder_thresholds_pct": [80, 90],
    },
    "compaction": {
        # 动态阈值三参，对齐 claude-code autoCompact.ts
        "auto_compact_buffer_tokens": 13000,
        "reserved_summary_output_tokens": 20000,
        "force_pct": 92,
        "max_consecutive_failures": 3,
        "summarizer_max_output_tokens": 20000,
    },
    "microcompact": {
        "enabled": True,
        "stale_after_messages": 30,
        "size_threshold_tokens": 800,
        "max_redactions_per_event": 8,
    },
    "post_compact_reinjection": {
        "enabled": True,
        "token_budget": 50000,
        "max_files": 5,
        "max_tokens_per_file": 5000,
    },
    "agent_loop": {"max_iterations": 80, "tool_call_parallel": True},
    "bash": {
        "default_timeout_sec": 60,
        "max_output_bytes": 65536,
        "forbidden_prefixes": ["git"],
    },
    "grep": {"default_max_results": 200, "context_lines": 0},
    "read": {
        "notice_bytes": 32768,
        "hard_bytes": 262144,
        "max_text_bytes": 524288,
        "multimodal_summary_length": 512,
    },
    "multimodal": {
        "attachment_max_bytes": 10 * 1024 * 1024,
        "image": {"tokens_per_file": 280},
        "video": {
            "tokens_per_frame": 70,
            "max_frames": 32,
            "fallback_tokens": 2240,
        },
        "audio": {
            "tokens_per_second": 25.0,
            "max_tokens": 750,
            "max_seconds": 30.0,
        },
        "mp4_extract_audio_track": False,
    },
    "preferences": {
        "mode": "fixed",                          # "fixed" 或 "ema"
        "explicit_exposures": 2,                  # fixed: 前 N 次显式期
        "silent_penalty_factor": 0.7,             # fixed/ema: 静默期违反扣分系数
        "ema_alpha": 0.3,                         # ema: EMA 追踪速率
        "ema_initial": 0.5,                       # ema: 初始 EMA 值
        "ema_threshold_low": 0.4,                 # ema: low/mid band 分界
        "ema_threshold_high": 0.8,                # ema: mid/high band 分界
        "silent_penalty_mid": 0.85,               # ema: mid band 违反扣分系数
        "user_override_enabled": True,
    },
    "update_engine": {
        "hidden_workspace_subdir": "workspace",
        "conflict_strategy": "theirs",
        "reminder_summary_max_chars": 2048,
    },
    "arc_scheduler": {
        # 选弧模式（实验旋钮）：fixed（可比基线）| rule（规则自动）| agent_choice（被测 agent 主动选）
        "selection_mode": "fixed",
        # selection_mode=rule 的子策略：branching（if-else 启发式）| continuous（state_score 软调节）
        "rule_strategy": "branching",
        # agent_choice 解析失败/越界后重发 reminder 的次数；仍失败则回落候选集首项（不依赖 seed）
        "agent_choice_max_retries": 1,
        "base_priority": {},
        # continuous strategy 的 state_score 三路融合权重（之和需 > 0）
        "state_w_tcr": 0.5,
        "state_w_adh": 0.3,
        "state_w_sil": 0.2,
        "state_recent_window": 3,
        "state_initial": 0.5,
    },
    "scoring": {
        "enabled": {
            "streak": True,
            "adherence": True,
            "adaptation": True,
            "callback": True,
            "compaction_profile": True,
        },
        "weights": {
            "tcr": 0.4,
            "streak_robustness": 0.2,
            "adherence": 0.2,
            "adaptation": 0.1,
            "callback": 0.1,
        },
    },
    "oracle": {"mode": "cascade"},
    "subagent": {
        "explore_enabled": True,
        "general_purpose_enabled": True,
        "token_limit": 100000,
        "max_iterations": 30,
    },
    "ls": {"max_entries": 1000},
    "tools": {
        "enabled": ["Read", "Write", "Edit", "Bash", "Grep", "Glob", "LS", "Agent"],
    },
    "logging": {"level": "INFO"},
}


# 单字段 env 覆盖：env name -> (dotted path, cast)
_FLAT_ENV_OVERRIDES: dict[str, tuple[str, Any]] = {
    "ARCBENCH_TOKEN_LIMIT_MAIN_AGENT": ("token_limits.main_agent", int),
    "ARCBENCH_BASH_TIMEOUT": ("bash.default_timeout_sec", int),
    "ARCBENCH_LOG_LEVEL": ("logging.level", str),
    "ARCBENCH_TOKENIZER": ("tokenizer.source", str),
    "ARCBENCH_CHAT_TEMPLATE": ("chat_template.source", str),
    "ARCBENCH_PROBE_ENABLED": (
        "probe.enabled",
        lambda v: v.lower() in {"1", "true", "yes", "on"},
    ),
    "ARCBENCH_PROBE_TIMEOUT": ("probe.timeout_sec", int),
    "ARCBENCH_COMPACTION_AUTO_BUFFER_TOKENS": (
        "compaction.auto_compact_buffer_tokens", int,
    ),
    "ARCBENCH_COMPACTION_RESERVED_OUTPUT_TOKENS": (
        "compaction.reserved_summary_output_tokens", int,
    ),
    "ARCBENCH_COMPACTION_FORCE_PCT": ("compaction.force_pct", int),
    "ARCBENCH_COMPACTION_MAX_CONSEC_FAILURES": (
        "compaction.max_consecutive_failures", int,
    ),
    "ARCBENCH_ORACLE_MODE": ("oracle.mode", str),
    "ARCBENCH_ARC_SELECTION_MODE": ("arc_scheduler.selection_mode", str),
}

# 三 role 模型配置的 env 命名：ARCBENCH_{MAIN,SUBAGENT,COMPACT}_<FIELD>
_MODEL_ENV_ROLES: dict[str, str] = {
    "MAIN": "main",
    "SUBAGENT": "subagent",
    "COMPACT": "compaction",
}
_MODEL_ENV_FIELDS: tuple[str, ...] = (
    "provider",
    "model_id",
    "api_base",
    "api_key",
    "api_key_env",
    "modalities",
)


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
    # 三 role 模型配置的单字段 env 覆盖：ARCBENCH_{MAIN,SUBAGENT,COMPACT}_<FIELD>
    for env_role, cfg_role in _MODEL_ENV_ROLES.items():
        for field in _MODEL_ENV_FIELDS:
            env_name = f"ARCBENCH_{env_role}_{field.upper()}"
            raw = os.environ.get(env_name)
            if raw is None:
                continue
            value: Any = raw
            if field == "modalities":
                value = [m.strip() for m in raw.split(",") if m.strip()]
            _set_dotted(out, f"models.{cfg_role}.{field}", value)
    return out


@dataclass
class PathsConfig:
    """``paths.*`` 节的强类型视图。CLI 子命令读这一份即可。"""

    data: Optional[Path] = None
    arc_filter: Optional[str] = None
    run_output: Optional[Path] = None
    resume_old: Optional[Path] = None
    resume_output: Optional[Path] = None
    stats_output: Optional[Path] = None
    clean_output: Optional[Path] = None
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
            arc_filter=d.get("arc_filter"),
            run_output=_path(d.get("run_output")),
            resume_old=_path(d.get("resume_old")),
            resume_output=_path(d.get("resume_output")),
            stats_output=_path(d.get("stats_output")),
            clean_output=_path(d.get("clean_output")),
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
    """递归剔除值为 None 的键，避免空覆盖把已有值打成 None。"""
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
    cli_config_overrides: Optional[dict[str, Any]] = None,
    cli_overrides: Optional[dict[str, Any]] = None,
) -> Config:
    """按六层优先级合并配置。

    ``cli_config_overrides`` 对应所有子命令通用的 ``--config-overrides '<json>'``，
    其优先级介于 ``--config`` 文件（低）与 CLI 显式 flag（高）之间。
    """
    data: dict[str, Any] = deepcopy(CODE_DEFAULTS)

    # 第 5 层：default.yaml
    yp = yaml_path if yaml_path is not None else DEFAULT_YAML
    data = _deep_merge(data, _load_yaml_file(yp))

    # 第 4 层：env
    data = _deep_merge(data, load_env_overrides())

    # 第 3 层：--config 文件
    if config_file is not None:
        data = _deep_merge(data, load_config_file(config_file))

    # 第 2 层：--config-overrides 内联 JSON
    if cli_config_overrides:
        data = _deep_merge(data, cli_config_overrides)

    # 第 1 层：CLI 显式
    if cli_overrides:
        nested: dict[str, Any] = {}
        for k, v in cli_overrides.items():
            if v is None:
                continue
            if "." in k:
                _set_dotted(nested, k, v)
            elif isinstance(v, dict):
                nested[k] = _deep_merge(
                    nested.get(k, {}) if isinstance(nested.get(k), dict) else {}, v
                )
            else:
                nested[k] = v
        data = _deep_merge(data, _prune_none(nested))

    return Config(data, yaml_path=yp)
