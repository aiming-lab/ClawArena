"""三家 provider 的 usage 提取器单元测试。

覆盖关键 schema 差异：
- OpenAI ``prompt_tokens_details.cached_tokens`` / ``completion_tokens_details.reasoning_tokens``
- Anthropic ``cache_read_input_tokens`` / ``cache_creation_input_tokens``
- Gemini 外层字段名 ``usageMetadata`` 与 ``cachedContentTokenCount`` 等
"""
from __future__ import annotations

from clawarena_team.provider.usage import (
    UsageRecord,
    extract_anthropic_usage,
    extract_gemini_usage,
    extract_openai_usage,
)


def test_openai_usage_full_fields():
    data = {
        "usage": {
            "prompt_tokens": 1000,
            "completion_tokens": 200,
            "total_tokens": 1200,
            "prompt_tokens_details": {"cached_tokens": 800, "audio_tokens": 0},
            "completion_tokens_details": {
                "reasoning_tokens": 50,
                "accepted_prediction_tokens": 0,
                "rejected_prediction_tokens": 0,
                "audio_tokens": 0,
            },
        }
    }
    raw, rec = extract_openai_usage(data)
    assert raw == data["usage"]
    # input = prompt - cached = 1000 - 800 = 200
    assert rec.input_tokens == 200
    assert rec.output_tokens == 200
    assert rec.cache_read_tokens == 800
    assert rec.cache_write_tokens == 0
    assert rec.reasoning_tokens == 50
    assert rec.total_tokens == 1200
    assert rec.provider == "openai_compat"
    # raw 字段须包含原始 audio_tokens 等 OpenAI 子项
    assert rec.raw["prompt_tokens_details"]["audio_tokens"] == 0


def test_openai_usage_missing_details():
    """无 cache、无 reasoning 时只剩 prompt/completion/total。"""
    data = {"usage": {"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150}}
    _, rec = extract_openai_usage(data)
    assert rec.input_tokens == 100
    assert rec.cache_read_tokens == 0
    assert rec.reasoning_tokens == 0


def test_openai_usage_empty():
    """完全缺 usage 时所有字段安全归零。"""
    _, rec = extract_openai_usage({})
    assert rec.input_tokens == 0
    assert rec.output_tokens == 0
    assert rec.cache_read_tokens == 0
    assert rec.total_tokens == 0


def test_anthropic_usage_with_cache():
    data = {
        "usage": {
            "input_tokens": 120,
            "output_tokens": 300,
            "cache_read_input_tokens": 5000,
            "cache_creation_input_tokens": 700,
        }
    }
    raw, rec = extract_anthropic_usage(data)
    assert raw == data["usage"]
    assert rec.input_tokens == 120
    assert rec.output_tokens == 300
    assert rec.cache_read_tokens == 5000
    assert rec.cache_write_tokens == 700
    assert rec.reasoning_tokens == 0
    # total = 全部加总
    assert rec.total_tokens == 120 + 300 + 5000 + 700
    assert rec.provider == "anthropic"


def test_anthropic_usage_no_cache_fields():
    """旧响应没有 cache_* 字段也不应崩。"""
    data = {"usage": {"input_tokens": 50, "output_tokens": 20}}
    _, rec = extract_anthropic_usage(data)
    assert rec.input_tokens == 50
    assert rec.output_tokens == 20
    assert rec.cache_read_tokens == 0
    assert rec.cache_write_tokens == 0
    assert rec.total_tokens == 70


def test_gemini_usage_outer_field_name():
    """外层字段名是 usageMetadata，不是 usage。"""
    data = {
        "usageMetadata": {
            "promptTokenCount": 800,
            "candidatesTokenCount": 200,
            "cachedContentTokenCount": 600,
            "thoughtsTokenCount": 40,
            "toolUsePromptTokenCount": 30,
            "totalTokenCount": 1070,
        }
    }
    raw, rec = extract_gemini_usage(data)
    assert raw == data["usageMetadata"]
    # input = prompt - cached = 800 - 600 = 200
    assert rec.input_tokens == 200
    assert rec.output_tokens == 200
    assert rec.cache_read_tokens == 600
    assert rec.cache_write_tokens == 0
    assert rec.reasoning_tokens == 40
    assert rec.total_tokens == 1070
    assert rec.provider == "gemini"


def test_gemini_usage_missing_optional_fields():
    """无 cache / thinking 时 cachedContentTokenCount / thoughtsTokenCount 可能缺。"""
    data = {
        "usageMetadata": {
            "promptTokenCount": 100,
            "candidatesTokenCount": 50,
            "totalTokenCount": 150,
        }
    }
    _, rec = extract_gemini_usage(data)
    assert rec.input_tokens == 100
    assert rec.cache_read_tokens == 0
    assert rec.reasoning_tokens == 0
    assert rec.total_tokens == 150


def test_gemini_usage_using_wrong_outer_key_returns_zeros():
    """误用 'usage' 而非 'usageMetadata' 时不会捡到任何数据（避免静默错读）。"""
    data = {"usage": {"prompt_tokens": 999}}
    _, rec = extract_gemini_usage(data)
    assert rec.input_tokens == 0
    assert rec.output_tokens == 0


def test_usage_record_to_dict_roundtrip():
    rec = UsageRecord(
        input_tokens=1, output_tokens=2, cache_read_tokens=3,
        cache_write_tokens=4, reasoning_tokens=5, total_tokens=15,
        provider="openai_compat", raw={"prompt_tokens": 4},
    )
    d = rec.to_dict()
    assert d["input_tokens"] == 1
    assert d["raw"]["prompt_tokens"] == 4
    assert d["provider"] == "openai_compat"
