from __future__ import annotations

import os
from pathlib import Path

import pytest

from clawarena_team.config import CODE_DEFAULTS, load_config


def test_load_default_yaml_overrides_code_defaults():
    cfg = load_config()
    # default.yaml 中 token_limits.main_agent = 200000，与代码默认相同；可以验证存在
    assert cfg.get("token_limits.main_agent") == 200000
    assert cfg.get("tokenizer.source") == "qwen3"


def test_env_overrides_yaml(monkeypatch):
    monkeypatch.setenv("CATEAM_MAIN_TOKEN_LIMIT", "12345")
    cfg = load_config()
    assert cfg.get("token_limits.main_agent") == 12345


def test_cli_overrides_env(monkeypatch):
    monkeypatch.setenv("CATEAM_MAIN_TOKEN_LIMIT", "1")
    cfg = load_config(cli_overrides={"token_limits.main_agent": 999})
    assert cfg.get("token_limits.main_agent") == 999


def test_code_defaults_complete():
    # 关键键不可缺
    for key in ("model_pool", "token_limits", "usage_hint", "agent_loop", "bash", "scenario"):
        assert key in CODE_DEFAULTS


def test_model_pool_env_overrides(monkeypatch):
    monkeypatch.setenv("CATEAM_MODEL_LLM_API_KEY", "sk-from-env")
    monkeypatch.setenv("CATEAM_MODEL_OMNI_MODEL_ID", "omni-override")
    cfg = load_config()
    assert cfg.get("model_pool.llm.api_key") == "sk-from-env"
    assert cfg.get("model_pool.omni.model_id") == "omni-override"
    # 未覆写字段仍来自 yaml
    assert cfg.get("model_pool.vlm.provider") == "openai_compat"


def test_model_pool_yaml_loaded():
    cfg = load_config()
    assert cfg.get("model_pool.llm.provider") == "openai_compat"
    assert cfg.get("model_pool.vlm.model_id") == "gemma-4-31b-it"
    assert cfg.get("model_pool.omni.name") == "gemma-4-e4b-it"
