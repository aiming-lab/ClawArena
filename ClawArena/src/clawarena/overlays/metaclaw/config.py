"""MetaClaw configuration — YAML loading and trigger config parsing."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path

_ENV_VAR_RE = re.compile(r"\$\{([^}:]+?)(?::-([^}]*))?\}")


def _expand_env(value: str) -> str:
    """Expand ${VAR} and ${VAR:-default} in a string."""
    def _repl(m: re.Match) -> str:
        return os.environ.get(m.group(1), m.group(2) if m.group(2) is not None else "")
    return _ENV_VAR_RE.sub(_repl, value)


def _expand_dict(d: dict) -> dict:
    """Recursively expand env vars in all string values of a dict."""
    out: dict = {}
    for k, v in d.items():
        if isinstance(v, str):
            out[k] = _expand_env(v)
        elif isinstance(v, dict):
            out[k] = _expand_dict(v)
        elif isinstance(v, list):
            out[k] = [_expand_env(i) if isinstance(i, str) else i for i in v]
        else:
            out[k] = v
    return out


# ---------------------------------------------------------------------------
# Structured config dataclasses
# ---------------------------------------------------------------------------


@dataclass
class MemoryCfg:
    enabled: bool = False
    scope: str = "default"
    retrieval_mode: str = "hybrid"
    embedding_mode: str = "semantic"
    max_injected_units: int = 10
    max_injected_tokens: int = 1500
    manual_trigger: bool = True
    ignore_turn_type: bool = True


@dataclass
class SkillsCfg:
    enabled: bool = False
    dir: str | None = None
    auto_evolve: bool = True
    top_k: int = 6


@dataclass
class RLCfg:
    enabled: bool = False
    scene_per_train: int = 5
    manual_train_trigger: bool = True
    batch_size: int = 4
    lora_rank: int = 32
    model: str = ""


@dataclass
class MetaClawConfig:
    raw_yaml: dict = field(default_factory=dict)
    memory: MemoryCfg = field(default_factory=MemoryCfg)
    skills: SkillsCfg = field(default_factory=SkillsCfg)
    rl: RLCfg = field(default_factory=RLCfg)
    proxy_host: str = "127.0.0.1"
    proxy_port: int | None = None
    served_model_name: str = "metaclaw"
    upstream_model_id: str = ""
    max_context_tokens: int = 50000


def load_config(config_path: Path) -> MetaClawConfig:
    """Load a MetaClaw YAML config, expanding ${VAR} env vars."""
    try:
        import yaml
    except ImportError:
        raise ImportError("PyYAML is required for MetaClaw config: pip install pyyaml")

    raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    expanded = _expand_dict(raw)

    mem_raw = expanded.get("memory", {})
    memory = MemoryCfg(
        enabled=bool(mem_raw.get("enabled", False)),
        scope=str(mem_raw.get("scope", "default")),
        retrieval_mode=str(mem_raw.get("retrieval_mode", "hybrid")),
        embedding_mode=str(mem_raw.get("embedding_mode", "semantic")),
        max_injected_units=int(mem_raw.get("max_injected_units", 10)),
        max_injected_tokens=int(mem_raw.get("max_injected_tokens", 1500)),
        manual_trigger=bool(mem_raw.get("manual_trigger", True)),
        ignore_turn_type=bool(mem_raw.get("ignore_turn_type", True)),
    )

    sk_raw = expanded.get("skills", {})
    skills = SkillsCfg(
        enabled=bool(sk_raw.get("enabled", False)),
        dir=sk_raw.get("dir"),
        auto_evolve=bool(sk_raw.get("auto_evolve", True)),
        top_k=int(sk_raw.get("top_k", 6)),
    )

    rl_raw = expanded.get("rl", {})
    rl = RLCfg(
        enabled=bool(rl_raw.get("enabled", False)),
        scene_per_train=int(rl_raw.get("scene_per_train", 5)),
        manual_train_trigger=bool(rl_raw.get("manual_train_trigger", True)),
        batch_size=int(rl_raw.get("batch_size", 4)),
        lora_rank=int(rl_raw.get("lora_rank", 32)),
        model=str(rl_raw.get("model", "")),
    )

    proxy_raw = expanded.get("proxy", {})
    llm_raw = expanded.get("llm", {})
    return MetaClawConfig(
        raw_yaml=expanded,
        memory=memory,
        skills=skills,
        rl=rl,
        proxy_host=str(proxy_raw.get("host", expanded.get("proxy_host", "127.0.0.1"))),
        proxy_port=proxy_raw.get("port", expanded.get("proxy_port")),
        served_model_name=str(
            proxy_raw.get("served_model_name", expanded.get("served_model_name", "metaclaw"))
        ),
        upstream_model_id=str(llm_raw.get("model_id", "")),
        max_context_tokens=int(expanded.get("max_context_tokens", 50000)),
    )


# ---------------------------------------------------------------------------
# Trigger config (from tests.json, not YAML)
# ---------------------------------------------------------------------------


@dataclass
class TriggerCfg:
    every_n_rounds: int = 0
    every_n_scenes: int = 0
    on_last_round: bool = False


def parse_trigger_config(mc_raw: dict) -> tuple[TriggerCfg, TriggerCfg]:
    """Parse tests.json metaclaw.memory_trigger / rl_trigger."""
    def _parse_one(raw: dict) -> TriggerCfg:
        return TriggerCfg(
            every_n_rounds=int(_expand_env(str(raw.get("every_n_rounds", 0)))),
            every_n_scenes=int(_expand_env(str(raw.get("every_n_scenes", 0)))),
            on_last_round=bool(raw.get("on_last_round", False)),
        )

    mem_raw = mc_raw.get("memory_trigger", {})
    rl_raw = mc_raw.get("rl_trigger", {})
    return _parse_one(mem_raw), _parse_one(rl_raw)
