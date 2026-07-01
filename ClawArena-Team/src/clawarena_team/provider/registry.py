"""Provider registry + ``--model`` JSON parsing + pool rule validation.

``--model`` JSON form::

    {
      "main":  {"provider": "...", "model_id": "...", "modalities": ["text","image"]},
      "llm":   {... "modalities": ["text"]},
      "vlm":   {... "modalities": ["text","image","video"]},
      "omni":  {... "modalities": ["text","audio","image"]}
    }

The ``api_key_env`` field is also supported, reading the key from an environment
variable.

Pool-type validation (enforced at init; see :data:`POOL_REQUIRED_MODALITIES` /
:data:`POOL_USABLE_MODALITIES`):

- ``llm``: must contain text; other declared modalities are warned and stripped,
  keeping only text;
- ``vlm``: must contain text+image; a declared audio is warned and stripped; a missing
  video is warned but the effective set keeps the usable items;
- ``omni``: must contain text+audio; image/video are optional and **not** warned; if
  declared, they take effect.
- ``main``: whatever is passed takes effect; audio/video are only warned, not stripped.

`build_pool_from_config`/`parse_model_json` only perform static rule pruning; actual
runtime modality availability is pruned again by :func:`probe_and_apply` via
:mod:`.probe` after live testing.
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
from typing import Any

from ..types import (
    ALLOWED_MODALITY_NAMES,
    ModelBundle,
    ModelConfig,
    ModelPoolEntry,
    Modality,
    POOL_REQUIRED_MODALITIES,
    POOL_USABLE_MODALITIES,
)
from .anthropic import AnthropicProvider
from .base import BaseProvider, ProviderError
from .gemini import GeminiProvider
from .openai_compat import OpenAICompatProvider
from .probe import ProbeOutcome, probe_model

log = logging.getLogger(__name__)

_REGISTRY: dict[str, type[BaseProvider]] = {
    "openai": OpenAICompatProvider,
    "openai_compat": OpenAICompatProvider,
    "vllm": OpenAICompatProvider,
    "ollama": OpenAICompatProvider,
    "openrouter": OpenAICompatProvider,
    "anthropic": AnthropicProvider,
    "gemini": GeminiProvider,
    "google": GeminiProvider,
}


def register_provider(name: str, cls: type[BaseProvider]) -> None:
    _REGISTRY[name] = cls


def build_provider(config: ModelConfig) -> BaseProvider:
    cls = _REGISTRY.get(config.provider)
    if cls is None:
        raise ProviderError(f"unknown provider: {config.provider!r}")
    return cls(config)


# ---------------------------------------------------------------------------
# dict → ModelConfig
# ---------------------------------------------------------------------------


_KNOWN_KEYS = {"provider", "model_id", "api_base", "api_key", "api_key_env", "name", "modalities"}


def _resolve_api_key(d: dict[str, Any]) -> str | None:
    if d.get("api_key"):
        return d["api_key"]
    env_name = d.get("api_key_env")
    if env_name:
        return os.environ.get(env_name)
    return None


def _parse_modalities(raw: Any, *, ctx: str) -> tuple[list[str], dict[str, int]]:
    """Parse modalities, supporting two forms, returning (modalities_list, modality_limits):

    - **dict (recommended)**: ``{text: true, image: 4, video: 1}`` — keys are modalities,
      and a non-``text`` value is the upper bound on the number of most-recent
      attachments of that modality kept in context (a positive integer).
    - **list (legacy / backward-compatible)**: ``["text", "image"]`` — no count limit
      (limits is empty; the probe stage will error on the missing limit, requiring an
      explicit dict form).
    """
    if raw is None:
        return ["text"], {}
    limits: dict[str, int] = {}
    if isinstance(raw, dict):
        mods = list(raw.keys())
        for m, v in raw.items():
            if m == "text":
                continue
            if isinstance(v, bool) or not isinstance(v, int) or v < 1:
                raise ProviderError(
                    f"{ctx}: modality '{m}' must map to a positive integer count "
                    f"(e.g. {{{m}: 4}}); got {v!r}"
                )
            limits[m] = int(v)
    elif isinstance(raw, list) and all(isinstance(x, str) for x in raw):
        mods = list(raw)
    else:
        raise ProviderError(
            f"{ctx}: modalities must be a list of strings or a dict of "
            f"{{modality: count}}; got {raw!r}"
        )
    mods = list(dict.fromkeys(mods))  # deduplicate while preserving order
    if "text" not in mods:
        mods.insert(0, "text")
    unknown = [m for m in mods if m not in ALLOWED_MODALITY_NAMES]
    if unknown:
        raise ProviderError(
            f"{ctx}: unknown modalities {unknown}; allowed: {sorted(ALLOWED_MODALITY_NAMES)}"
        )
    return mods, limits


def _model_config_from_dict(d: dict[str, Any], *, ctx: str) -> tuple[ModelConfig, list[str]]:
    if not d.get("provider") or not d.get("model_id"):
        raise ProviderError(f"{ctx}: provider and model_id are required")
    declared, limits = _parse_modalities(d.get("modalities"), ctx=ctx)
    extra = {k: v for k, v in d.items() if k not in _KNOWN_KEYS}
    cfg = ModelConfig(
        provider=d["provider"],
        model_id=d["model_id"],
        api_base=d.get("api_base"),
        api_key=_resolve_api_key(d),
        modalities=list(declared),
        modality_limits=dict(limits),
        extra=extra,
    )
    return cfg, declared


# ---------------------------------------------------------------------------
# Pool rules: prune declared modalities → static effective set
# ---------------------------------------------------------------------------


def _apply_pool_rules(
    key: Modality,
    declared: list[str],
    *,
    warnings: list[str],
    errors: list[str],
) -> list[str]:
    """Prune the declared modality set according to the pool type, returning the static
    effective set."""
    required = POOL_REQUIRED_MODALITIES[key]
    usable = POOL_USABLE_MODALITIES[key]

    declared_set = set(declared)
    extras = declared_set - usable
    if extras:
        warnings.append(
            f"pool[{key.value}]: modalities {sorted(extras)} are not usable for this pool "
            f"(usable: {sorted(usable)}); dropping"
        )

    effective = [m for m in declared if m in usable]
    effective_set = set(effective)

    missing_required = required - effective_set
    if missing_required:
        errors.append(
            f"pool[{key.value}]: missing required modalities {sorted(missing_required)}; "
            f"required: {sorted(required)}"
        )

    # vlm-only warning: a missing video gives a hint but does not fail
    if key is Modality.VLM and "video" not in effective_set:
        warnings.append("pool[vlm]: 'video' not declared — vlm subagents will not be able to read video files")

    return effective


def _apply_main_warnings(declared: list[str], *, warnings: list[str]) -> list[str]:
    """Pruning for main is very lenient: whatever is passed takes effect; audio/video are
    only warned, not stripped."""
    flagged = [m for m in declared if m in {"audio", "video"}]
    if flagged:
        warnings.append(
            f"main: declared modalities include {flagged}; main agents are typically text or text+image — "
            f"keep these only if you really intend main to consume {flagged} natively"
        )
    return list(declared)


# ---------------------------------------------------------------------------
# yaml → ModelPoolEntry
# ---------------------------------------------------------------------------


def build_pool_from_config(
    model_pool_cfg: dict[str, Any],
    *,
    warnings: list[str] | None = None,
    errors: list[str] | None = None,
) -> dict[Modality, ModelPoolEntry]:
    """Build pool entries from the ``model_pool`` dict merged from yaml/env and apply
    static rules.

    If ``warnings`` / ``errors`` are given, diagnostics are appended to them; otherwise
    they are accumulated internally and emitted via the log. On validation failure this
    function still returns a partially constructed pool (effective_modalities may not
    satisfy the required set), and ``probe_and_apply`` or the caller ultimately decides
    whether to abort.
    """
    own_warnings = warnings if warnings is not None else []
    own_errors = errors if errors is not None else []

    pool: dict[Modality, ModelPoolEntry] = {}
    for key_str in ("llm", "vlm", "omni"):
        entry = model_pool_cfg.get(key_str)
        if entry is None:
            continue
        modality = Modality(key_str)
        cfg, declared = _model_config_from_dict(entry, ctx=f"pool[{key_str}]")
        effective = _apply_pool_rules(
            modality, declared, warnings=own_warnings, errors=own_errors
        )
        cfg.modalities = list(effective)
        name = entry.get("name") or cfg.model_id
        pool[modality] = ModelPoolEntry(
            key=modality,
            name=name,
            config=cfg,
            declared_modalities=list(declared),
            effective_modalities=list(effective),
        )

    if warnings is None:
        for w in own_warnings:
            log.warning("%s", w)
    if errors is None:
        for e in own_errors:
            log.error("%s", e)
    return pool


# ---------------------------------------------------------------------------
# CLI ``--model`` JSON merge
# ---------------------------------------------------------------------------


def parse_model_json(
    raw: str | dict[str, Any],
    *,
    defaults_pool: dict[Modality, ModelPoolEntry] | None = None,
    main_defaults: dict[str, Any] | None = None,
    warnings: list[str] | None = None,
    errors: list[str] | None = None,
) -> ModelBundle:
    """Parse the CLI ``--model`` argument and merge it with the default pool/main into a
    :class:`ModelBundle`.

    Priority: explicitly given in ``raw`` > defaults. ``raw`` must provide a ``main``
    field, or defaults must supply it.
    """
    own_warnings = warnings if warnings is not None else []
    own_errors = errors if errors is not None else []

    if isinstance(raw, str):
        data = json.loads(raw)
    else:
        data = raw
    if not isinstance(data, dict):
        raise ProviderError("--model JSON root must be an object")

    # main: raw explicit > defaults
    main_raw = data.get("main")
    if main_raw is None:
        if not main_defaults or not main_defaults.get("provider"):
            raise ProviderError("--model JSON must contain 'main' (or set main.* in config)")
        main_raw = main_defaults
    main_cfg, main_declared = _model_config_from_dict(main_raw, ctx="main")
    main_effective = _apply_main_warnings(main_declared, warnings=own_warnings)
    main_cfg.modalities = list(main_effective)

    # pool: entries given in raw override defaults
    pool: dict[Modality, ModelPoolEntry] = dict(defaults_pool or {})
    for key_str in ("llm", "vlm", "omni"):
        if key_str not in data:
            continue
        modality = Modality(key_str)
        cfg, declared = _model_config_from_dict(data[key_str], ctx=f"pool[{key_str}]")
        effective = _apply_pool_rules(
            modality, declared, warnings=own_warnings, errors=own_errors
        )
        cfg.modalities = list(effective)
        name = data[key_str].get("name", cfg.model_id)
        pool[modality] = ModelPoolEntry(
            key=modality,
            name=name,
            config=cfg,
            declared_modalities=list(declared),
            effective_modalities=list(effective),
        )

    if warnings is None:
        for w in own_warnings:
            log.warning("%s", w)
    if errors is None:
        for e in own_errors:
            log.error("%s", e)
    return ModelBundle(main=main_cfg, pool=pool)


# ---------------------------------------------------------------------------
# Runtime probing: live-test each declared non-text modality by actually calling the
# provider
# ---------------------------------------------------------------------------


async def _probe_entry(
    entry: ModelPoolEntry,
    *,
    timeout_sec: float,
    max_tokens: int,
) -> tuple[list[str], list[ProbeOutcome]]:
    outcomes = await probe_model(
        entry.config, entry.effective_modalities,
        timeout_sec=timeout_sec, max_tokens=max_tokens,
    )
    survived = [o.modality for o in outcomes if o.ok]
    return survived, outcomes


def _check_modality_limits(
    modalities: list[str], limits: dict[str, int], ctx: str, errors: list[str]
) -> None:
    """Every effective non-text modality must have a positive-integer count limit
    (the modalities dict form).

    The limit = the number of most-recent attachments of that modality kept in context
    (the oldest are stripped beyond it). A missing limit errors out, forcing the config
    author to declare it explicitly, to avoid unbounded historical multimodal
    accumulation hitting vLLM's ``--limit-mm-per-prompt``.
    """
    for m in modalities:
        if m == "text":
            continue
        v = limits.get(m)
        if isinstance(v, bool) or not isinstance(v, int) or v < 1:
            errors.append(
                f"{ctx}: modality '{m}' is supported but has no positive per-modality "
                f"count limit; declare it as modalities: {{{m}: N}} (N = max recent "
                f"attachments kept in context, must be ≤ serving --limit-mm-per-prompt)"
            )


async def probe_and_apply(
    bundle: ModelBundle,
    *,
    timeout_sec: float = 20.0,
    max_tokens: int = 4,
    warnings: list[str] | None = None,
    errors: list[str] | None = None,
) -> ModelBundle:
    """Validate all declared non-text modalities by actually calling the provider.

    - if any pool entry loses an item from its :data:`POOL_REQUIRED_MODALITIES` →
      add to ``errors``;
    - if it only loses optional items → add to ``warnings`` and strip them from
      effective;
    - because main's rules are lenient, it only warns and does not affect the
      required-set validation.
    """
    own_warnings = warnings if warnings is not None else []
    own_errors = errors if errors is not None else []

    # pool: concurrent probing
    pool_items = list(bundle.pool.items())
    pool_results = await asyncio.gather(
        *[
            _probe_entry(entry, timeout_sec=timeout_sec, max_tokens=max_tokens)
            for _, entry in pool_items
        ]
    )
    for (key, entry), (survived, outcomes) in zip(pool_items, pool_results):
        lost = [o for o in outcomes if not o.ok]
        for o in lost:
            own_warnings.append(
                f"pool[{key.value}]: probe failed for modality {o.modality!r}: {o.detail}"
            )
        required = POOL_REQUIRED_MODALITIES[key]
        missing = required - set(survived)
        if missing:
            own_errors.append(
                f"pool[{key.value}]: required modalities {sorted(missing)} failed probe; "
                f"check provider/api_base/model_id"
            )
        entry.effective_modalities = list(survived)
        entry.config.modalities = list(survived)

    # main
    main_outcomes = await probe_model(
        bundle.main, bundle.main.modalities,
        timeout_sec=timeout_sec, max_tokens=max_tokens,
    )
    main_survived = [o.modality for o in main_outcomes if o.ok]
    for o in main_outcomes:
        if not o.ok:
            own_warnings.append(f"main: probe failed for modality {o.modality!r}: {o.detail}")
    if "text" not in main_survived:
        own_errors.append("main: text probe failed; main agent cannot proceed")
    bundle.main.modalities = list(main_survived)

    # Count-limit validation: after probe pruning, every still-effective non-text
    # modality must have a positive-integer limit.
    for key, entry in bundle.pool.items():
        _check_modality_limits(
            entry.effective_modalities, entry.config.modality_limits,
            f"pool[{key.value}]", own_errors,
        )
    _check_modality_limits(
        bundle.main.modalities, bundle.main.modality_limits, "main", own_errors,
    )

    if warnings is None:
        for w in own_warnings:
            log.warning("%s", w)
    if errors is None:
        for e in own_errors:
            log.error("%s", e)
    return bundle
