"""Unified ModelConfig for LLM provider configuration across all frameworks."""

from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

VALID_PROVIDERS = frozenset({
    # Core providers (supported by most frameworks)
    "openai", "anthropic", "claude", "bedrock", "google", "ollama", "azure",
    "codex",
    "ccr", "claude-code-router",
    # Extended providers (zeroclaw-native, passed through to config)
    "openrouter", "groq", "mistral", "xai",
    "qwen", "moonshot", "glm", "minimax",
    "copilot", "telnyx",
})

DEFAULT_API_BASE: dict[str, str] = {
    "openai": "https://api.openai.com/v1",
    "anthropic": "https://api.anthropic.com",
    "google": "https://generativelanguage.googleapis.com/v1beta",
    "ollama": "http://localhost:11434/v1",
    "azure": "",
    "bedrock": "",
    "claude": "",
    "codex": "",
    "ccr": "",
    "claude-code-router": "",
    # Extended providers
    "openrouter": "https://openrouter.ai/api/v1",
    "groq": "https://api.groq.com/openai/v1",
    "mistral": "https://api.mistral.ai/v1",
    "xai": "https://api.x.ai/v1",
    "qwen": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "moonshot": "https://api.moonshot.cn/v1",
    "glm": "https://open.bigmodel.cn/api/paas/v4",
    "minimax": "https://api.minimax.chat/v1",
    "copilot": "",
    "telnyx": "https://api.telnyx.com/v2/ai",
}

_ENV_VAR_RE = re.compile(r"\$\{([^}:]+?)(?::-([^}]*))?\}")
_CLAUDE_4_ALIAS_RE = re.compile(r"^(claude-(?:opus|sonnet|haiku)-4)-(\d+)$")


def expand_env_vars(value: str) -> str:
    """Expand ${VAR} and ${VAR:-default} patterns in a string."""
    def _replace(m: re.Match) -> str:
        var_name = m.group(1)
        default = m.group(2) if m.group(2) is not None else ""
        return os.environ.get(var_name, default)
    return _ENV_VAR_RE.sub(_replace, value)


def mask_api_key(key: str) -> str:
    """Mask an API key for safe logging: first 6 chars + ***."""
    if len(key) <= 6:
        return "***"
    return key[:6] + "***"


class ConfigError(Exception):
    """Raised when a framework does not support a given provider configuration."""


def normalize_model_id(model_id: str) -> str:
    """Normalize legacy model aliases into canonical ids."""
    if not model_id:
        return model_id
    return _CLAUDE_4_ALIAS_RE.sub(r"\1.\2", model_id)


@dataclass
class ModelConfig:
    """Universal model configuration for LLM provider redirection.

    Attributes:
        model_id: Model name, e.g. "gpt-4o", "claude-opus-4.6".
        api_base: API endpoint URL. Empty means use provider default.
        provider: Provider type determining API format and auth.
        api_key: Auth credential. Supports ${VAR} interpolation. None = no change.
        extra: Framework-specific override fields.
    """

    model_id: str
    api_base: str = ""
    provider: str = "openai"
    api_key: str | None = None
    extra: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.model_id = normalize_model_id(self.model_id)

    @classmethod
    def from_env(cls) -> ModelConfig | None:
        """Build from CLAWARENA_MODEL_ID / CLAWARENA_API_BASE / CLAWARENA_API_KEY / CLAWARENA_PROVIDER."""
        model_id = os.environ.get("CLAWARENA_MODEL_ID", "")
        if not model_id:
            return None
        return cls(
            model_id=model_id,
            api_base=os.environ.get("CLAWARENA_API_BASE", ""),
            provider=os.environ.get("CLAWARENA_PROVIDER", "openai"),
            api_key=os.environ.get("CLAWARENA_API_KEY"),
        )

    @classmethod
    def from_dict(cls, d: dict) -> ModelConfig:
        """Build from a tests.json model field dict. Supports ${VAR} interpolation."""
        model_id = expand_env_vars(str(d.get("model_id", "")))
        api_base = expand_env_vars(str(d.get("api_base", "")))
        provider = expand_env_vars(str(d.get("provider", "openai")))
        raw_key = d.get("api_key")
        api_key: str | None = None
        if raw_key is not None:
            key_str = str(raw_key)
            if key_str and not _ENV_VAR_RE.search(key_str):
                logger.warning(
                    "[warn] api_key is plaintext in config — "
                    "consider using ${ENV_VAR} reference instead"
                )
            api_key = expand_env_vars(key_str) if key_str else None

        extra = {k: v for k, v in d.items()
                 if k not in ("model_id", "api_base", "provider", "api_key")}

        return cls(
            model_id=model_id,
            api_base=api_base,
            provider=provider,
            api_key=api_key,
            extra=extra,
        )

    @classmethod
    def from_cli(
        cls,
        provider: str | None,
        model_id: str | None,
        api_base: str | None,
        api_key: str | None,
        model_config_json: str | None = None,
    ) -> ModelConfig | None:
        """Build from CLI arguments. Returns None if no --model-id given."""
        if not model_id:
            return None
        extra: dict = {}
        if model_config_json:
            import json as _json

            try:
                parsed = _json.loads(model_config_json)
                if not isinstance(parsed, dict):
                    raise ValueError("--model-config must be a JSON object")
                extra = parsed
            except Exception as exc:
                raise ValueError(f"--model-config: invalid JSON — {exc}") from exc
        return cls(
            model_id=model_id,
            api_base=api_base or "",
            provider=provider or "openai",
            api_key=api_key,
            extra=extra,
        )

    def resolved_api_base(self) -> str:
        """Return api_base, falling back to provider default if empty."""
        if self.api_base:
            return self.api_base
        return DEFAULT_API_BASE.get(self.provider, "")


def resolve_model_config(
    tests_cfg: dict,
    framework: str,
    cli_model: ModelConfig | None = None,
) -> ModelConfig | None:
    """Resolve ModelConfig from the priority chain:

    CLI args > env vars > framework-level model > top-level model > None
    """
    if cli_model:
        return cli_model

    env_model = ModelConfig.from_env()
    if env_model:
        return env_model

    fw_cfg = tests_cfg.get("frameworks", {}).get(framework, {})
    fw_model_raw = fw_cfg.get("model")
    if fw_model_raw:
        return ModelConfig.from_dict(fw_model_raw)

    top_model_raw = tests_cfg.get("model")
    if top_model_raw:
        return ModelConfig.from_dict(top_model_raw)

    return None
