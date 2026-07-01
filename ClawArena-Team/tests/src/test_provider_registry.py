from __future__ import annotations

import json

import pytest

from clawarena_team.provider import build_pool_from_config, build_provider, parse_model_json
from clawarena_team.provider.base import ProviderError
from clawarena_team.types import Modality


def test_parse_model_json_main_only():
    raw = json.dumps({"main": {"provider": "openai", "model_id": "gpt-x"}})
    b = parse_model_json(raw)
    assert b.main.provider == "openai"
    assert b.main.model_id == "gpt-x"
    assert b.pool == {}


def test_parse_model_json_with_pool():
    raw = {
        "main": {"provider": "openai", "model_id": "m"},
        "llm": {"provider": "openai", "model_id": "qwen", "name": "qwen"},
    }
    b = parse_model_json(raw)
    assert Modality.LLM in b.pool
    assert b.pool[Modality.LLM].name == "qwen"


def test_parse_model_json_missing_main():
    with pytest.raises(ProviderError):
        parse_model_json("{}")


def test_defaults_pool_merged_with_cli():
    from clawarena_team.types import ModelConfig, ModelPoolEntry

    pool = {Modality.LLM: ModelPoolEntry(Modality.LLM, "from_yaml", ModelConfig("openai", "x"))}
    raw = {"main": {"provider": "openai", "model_id": "m"}}
    b = parse_model_json(raw, defaults_pool=pool)
    assert b.pool[Modality.LLM].name == "from_yaml"


def test_cli_overrides_yaml_pool_entry():
    from clawarena_team.types import ModelConfig, ModelPoolEntry

    pool = {Modality.LLM: ModelPoolEntry(Modality.LLM, "from_yaml", ModelConfig("openai", "x"))}
    raw = {
        "main": {"provider": "openai", "model_id": "m"},
        "llm": {"provider": "openai", "model_id": "y", "name": "from_cli"},
    }
    b = parse_model_json(raw, defaults_pool=pool)
    assert b.pool[Modality.LLM].name == "from_cli"
    assert b.pool[Modality.LLM].config.model_id == "y"


def test_build_pool_from_config_basic():
    cfg = {
        "llm": {"provider": "openai", "model_id": "x", "name": "n1"},
        "vlm": {"provider": "openai", "model_id": "y"},
    }
    pool = build_pool_from_config(cfg)
    assert pool[Modality.LLM].name == "n1"
    assert pool[Modality.VLM].name == "y"  # 缺省 name 取 model_id
    assert Modality.OMNI not in pool


def test_unknown_provider_raises():
    from clawarena_team.types import ModelConfig

    with pytest.raises(ProviderError):
        build_provider(ModelConfig(provider="nope", model_id="x"))
