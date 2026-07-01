"""Provider 注册与构造。

ArcBench v1 仅 main 一个 agent，但 provider 层支持多家以便用户横评。
"""
from .anthropic import AnthropicProvider
from .base import BaseProvider, ProviderError
from .gemini import GeminiProvider
from .openai_compat import OpenAICompatProvider
from .registry import build_provider, parse_model_json
from .usage import (
    UsageRecord,
    extract_anthropic_usage,
    extract_gemini_usage,
    extract_openai_usage,
)

__all__ = [
    "BaseProvider",
    "ProviderError",
    "AnthropicProvider",
    "OpenAICompatProvider",
    "GeminiProvider",
    "build_provider",
    "parse_model_json",
    "UsageRecord",
    "extract_openai_usage",
    "extract_anthropic_usage",
    "extract_gemini_usage",
]
