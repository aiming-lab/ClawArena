"""Provider 注册、构造、以及三 role 模型配置解析。

ArcBench 支持三 role 模型：

- ``main``：主 agent loop
- ``subagent``：``Agent`` 工具 spawn 的子代理
- ``compaction``：主 agent 自压缩

``--model`` JSON 接受两种顶层形式，二者**等价**——任一字段均可缺省：

1. 扁平形式（向后兼容，等价于只配 ``main``）::

       {"provider": "anthropic", "model_id": "claude-opus-4-7"}

2. 三 role 显式分配::

       {
         "main":       {"provider": "anthropic", "model_id": "claude-opus-4-7"},
         "subagent":   {"provider": "openai_compat", "model_id": "gpt-4o-mini"},
         "compaction": {"provider": "anthropic", "model_id": "claude-haiku-4-5"}
       }

任何 role / 任何字段可缺；缺失的字段按 ``CLI JSON > env > yaml > default`` 优先级
回落，最后 ``subagent`` / ``compaction`` **field-by-field** 从已解析好的 ``main``
继承未填的字段。仅当 ``main.provider`` 或 ``main.model_id`` 全链路均缺时报错。
"""
from __future__ import annotations

import json
import os
from typing import Any

from ..types import ModelBundle, ModelConfig
from .anthropic import AnthropicProvider
from .base import BaseProvider
from .gemini import GeminiProvider
from .openai_compat import OpenAICompatProvider

_REGISTRY: dict[str, type[BaseProvider]] = {
    "anthropic": AnthropicProvider,
    "openai_compat": OpenAICompatProvider,
    "openai": OpenAICompatProvider,
    "gemini": GeminiProvider,
}

_ROLES = ("main", "subagent", "compaction")
_FIELDS = ("provider", "model_id", "api_base", "api_key", "api_key_env", "modalities")


def build_provider(config: ModelConfig) -> BaseProvider:
    """按 :class:`ModelConfig` 构造 :class:`BaseProvider` 实例（role-agnostic）。"""
    cls = _REGISTRY.get(config.provider)
    if cls is None:
        raise ValueError(
            f"unknown provider {config.provider!r}; supported: {sorted(_REGISTRY)}"
        )
    return cls(config)


def _resolve_api_key(d: dict[str, Any]) -> str | None:
    api_key = d.get("api_key")
    if api_key:
        return api_key
    env_name = d.get("api_key_env")
    if env_name:
        return os.environ.get(env_name)
    return None


def _normalize_modalities(
    raw: Any, *, role: str, warnings: list[str]
) -> list[str]:
    if raw is None:
        return ["text"]
    if not isinstance(raw, list):
        warnings.append(f"{role}.modalities must be a list; coercing to ['text']")
        return ["text"]
    out = list(raw)
    if "text" not in out:
        warnings.append(f"{role}.modalities did not include 'text'; prepending it")
        out = ["text"] + out
    return out


def _split_known_extra(d: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """把一个 role 的字典拆为 (known_fields, extra)。"""
    known = {k: d[k] for k in _FIELDS if k in d}
    extra = {k: v for k, v in d.items() if k not in _FIELDS}
    return known, extra


def _build_role_config(
    role: str,
    role_dict: dict[str, Any],
    *,
    warnings: list[str],
    extra_passthrough: dict[str, Any] | None = None,
) -> ModelConfig:
    modalities = _normalize_modalities(role_dict.get("modalities"), role=role, warnings=warnings)
    if role == "compaction":
        # claude-code 同款：summary 不携带 image 块，compaction provider 强制 text-only
        modalities = ["text"]
    api_key = _resolve_api_key(role_dict)
    extra = dict(extra_passthrough or {})
    return ModelConfig(
        provider=str(role_dict.get("provider") or ""),
        model_id=str(role_dict.get("model_id") or ""),
        api_base=role_dict.get("api_base"),
        api_key=api_key,
        modalities=modalities,
        declared_modalities=list(modalities),
        effective_modalities=list(modalities),
        extra=extra,
    )


def _inherit_from_main(
    role: str, role_dict: dict[str, Any], main_dict: dict[str, Any]
) -> dict[str, Any]:
    """``subagent`` / ``compaction`` field-by-field 继承 ``main`` 已合并好的值。"""
    merged = dict(main_dict)
    merged.update({k: v for k, v in role_dict.items() if v not in (None, "", [])})
    return merged


def parse_model_json(
    raw: str | dict[str, Any],
    *,
    models_defaults: dict[str, Any],
    warnings: list[str] | None = None,
    errors: list[str] | None = None,
) -> ModelBundle:
    """把 ``--model`` 的 JSON 与 ``models.*`` yaml/env 默认值合并为三 role :class:`ModelBundle`。

    Args:
        raw: ``--model`` 的 JSON 字符串或 dict；空串 / None 视为未传
        models_defaults: 已合并好的 ``models`` 段（yaml + env 已就位），形如
            ``{"main": {...}, "subagent": {...}, "compaction": {...}}``。每个 role 的
            dict 内字段：``provider / model_id / api_base / api_key / api_key_env /
            modalities``
    """
    warnings = warnings if warnings is not None else []
    errors = errors if errors is not None else []
    if isinstance(raw, str) and raw.strip():
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as e:
            errors.append(f"--model JSON is not valid: {e}")
            obj = {}
    elif isinstance(raw, dict):
        obj = raw
    else:
        obj = {}

    # 形式判别：若顶层带任意 role key，按 role-keyed 解；否则视为 main 的扁平别名
    is_role_keyed = isinstance(obj, dict) and any(r in obj for r in _ROLES)
    json_per_role: dict[str, dict[str, Any]] = {r: {} for r in _ROLES}
    if is_role_keyed:
        for r in _ROLES:
            v = obj.get(r)
            if isinstance(v, dict):
                json_per_role[r] = v
    elif isinstance(obj, dict) and obj:
        json_per_role["main"] = obj

    # 合并：yaml/env defaults  ⨁  JSON 同 role，再处理继承
    merged: dict[str, dict[str, Any]] = {}
    for r in _ROLES:
        base = dict(models_defaults.get(r) or {})
        base.update({k: v for k, v in json_per_role[r].items() if v is not None})
        merged[r] = base

    # subagent / compaction 缺字段从 main 继承
    main_merged = merged["main"]
    for r in ("subagent", "compaction"):
        merged[r] = _inherit_from_main(r, merged[r], main_merged)

    # 校验：main 的两个必填字段全链路是否齐
    if not main_merged.get("provider"):
        errors.append("main.provider is required (set via --model JSON, env, or yaml)")
    if not main_merged.get("model_id"):
        errors.append("main.model_id is required (set via --model JSON, env, or yaml)")

    # 构造 ModelConfig；extra 字段（非 _FIELDS 之内的项）只在 main 上保留以便 provider 扩展
    main_extra = {k: v for k, v in json_per_role["main"].items() if k not in _FIELDS}
    return ModelBundle(
        main=_build_role_config("main", merged["main"], warnings=warnings, extra_passthrough=main_extra),
        subagent=_build_role_config("subagent", merged["subagent"], warnings=warnings),
        compaction=_build_role_config("compaction", merged["compaction"], warnings=warnings),
    )
