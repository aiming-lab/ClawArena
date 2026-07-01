"""分层配置（5 层优先级）覆盖测试。"""
from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from clawarena_team.config import (
    Config,
    PathsConfig,
    _deep_merge,
    _set_dotted,
    load_config,
    load_config_file,
    load_env_overrides,
)


def _write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data), encoding="utf-8")


def test_priority_cli_beats_config_beats_env_beats_yaml(monkeypatch, tmp_path):
    # yaml 在最低（除代码默认外）
    yaml_path = tmp_path / "y.yaml"
    _write_yaml(yaml_path, {"token_limits": {"main_agent": 1000}})
    # env 比 yaml 高
    monkeypatch.setenv("CATEAM_MAIN_TOKEN_LIMIT", "2000")
    # --config 比 env 高
    cfg_file = tmp_path / "c.yaml"
    _write_yaml(cfg_file, {"token_limits": {"main_agent": 3000}})

    # 不传 cli_overrides 时 --config 应胜出
    cfg = load_config(yaml_path=yaml_path, config_file=cfg_file)
    assert cfg.get("token_limits.main_agent") == 3000

    # CLI 显式时 CLI 胜出
    cfg = load_config(
        yaml_path=yaml_path,
        config_file=cfg_file,
        cli_overrides={"token_limits.main_agent": 4000},
    )
    assert cfg.get("token_limits.main_agent") == 4000


def test_load_config_file_json(tmp_path):
    p = tmp_path / "c.json"
    p.write_text(json.dumps({"logging": {"level": "DEBUG"}}), encoding="utf-8")
    cfg = load_config(config_file=p)
    assert cfg.get("logging.level") == "DEBUG"


def test_load_config_file_rejects_unknown_suffix(tmp_path):
    p = tmp_path / "c.txt"
    p.write_text("ignored", encoding="utf-8")
    with pytest.raises(ValueError):
        load_config_file(p)


def test_load_config_file_rejects_non_mapping(tmp_path):
    p = tmp_path / "c.json"
    p.write_text(json.dumps([1, 2]), encoding="utf-8")
    with pytest.raises(ValueError):
        load_config_file(p)


def test_env_overrides_modalities_split():
    import os
    os.environ["CATEAM_MODEL_VLM_MODALITIES"] = "text,image,video"
    try:
        overrides = load_env_overrides()
    finally:
        del os.environ["CATEAM_MODEL_VLM_MODALITIES"]
    assert overrides["model_pool"]["vlm"]["modalities"] == ["text", "image", "video"]


def test_env_overrides_main(monkeypatch):
    monkeypatch.setenv("CATEAM_MAIN_PROVIDER", "openai_compat")
    monkeypatch.setenv("CATEAM_MAIN_MODEL_ID", "gpt-5.4")
    monkeypatch.setenv("CATEAM_MAIN_MODALITIES", "text,image")
    cfg = load_config()
    assert cfg.get("main.provider") == "openai_compat"
    assert cfg.get("main.model_id") == "gpt-5.4"
    assert cfg.get("main.modalities") == ["text", "image"]


def test_nested_cli_override_does_not_drop_siblings(tmp_path):
    cfg = load_config(cli_overrides={"model_pool": {"vlm": {"api_key": "k2"}}})
    # 只覆盖了 vlm.api_key，其他池/字段不丢
    assert cfg.get("model_pool.vlm.api_key") == "k2"
    assert cfg.get("model_pool.llm.provider") == "openai_compat"
    assert cfg.get("model_pool.vlm.model_id") == "gemma-4-31b-it"


def test_paths_view_types(tmp_path):
    cfg = load_config(cli_overrides={
        "paths.data": str(tmp_path / "ds"),
        "paths.run_output": str(tmp_path / "out"),
        "paths.concurrency": 4,
        "paths.strict": True,
    })
    p: PathsConfig = cfg.paths()
    assert p.data is not None and p.data.is_absolute()
    assert p.run_output is not None and p.run_output.name == "out"
    assert p.concurrency == 4
    assert p.strict is True
    assert p.stats_output is None  # 未传


def test_deep_merge_preserves_unrelated_keys():
    base = {"a": {"x": 1, "y": 2}, "b": [1, 2]}
    out = _deep_merge(base, {"a": {"y": 99}})
    assert out == {"a": {"x": 1, "y": 99}, "b": [1, 2]}


def test_set_dotted_creates_intermediate():
    d: dict = {}
    _set_dotted(d, "a.b.c", 7)
    assert d == {"a": {"b": {"c": 7}}}
