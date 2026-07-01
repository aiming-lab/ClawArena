"""模型池模态规则与（mock）探测的单元测试。"""
from __future__ import annotations

import json
from unittest.mock import AsyncMock, patch

import pytest

from clawarena_team.provider import (
    build_pool_from_config,
    parse_model_json,
    probe_and_apply,
)
from clawarena_team.provider.probe import ProbeOutcome
from clawarena_team.types import (
    Modality,
    POOL_REQUIRED_MODALITIES,
    POOL_USABLE_MODALITIES,
)


# ---------------------------------------------------------------------------
# 静态规则：build_pool_from_config / parse_model_json
# ---------------------------------------------------------------------------


def _base_entry(provider="openai_compat", model_id="m", api_base="http://x"):
    return {
        "provider": provider,
        "model_id": model_id,
        "api_base": api_base,
        "api_key": "EMPTY",
        "name": model_id,
    }


def test_llm_drops_extras_with_warning():
    warnings: list[str] = []
    errors: list[str] = []
    cfg = {"llm": dict(_base_entry(), modalities=["text", "image", "audio"])}
    pool = build_pool_from_config(cfg, warnings=warnings, errors=errors)
    entry = pool[Modality.LLM]
    assert entry.effective_modalities == ["text"]
    assert entry.declared_modalities == ["text", "image", "audio"]
    assert any("not usable" in w for w in warnings)
    assert not errors


def test_vlm_drops_audio_warns_missing_video():
    warnings: list[str] = []
    errors: list[str] = []
    cfg = {"vlm": dict(_base_entry(), modalities=["text", "image", "audio"])}
    pool = build_pool_from_config(cfg, warnings=warnings, errors=errors)
    entry = pool[Modality.VLM]
    assert "audio" not in entry.effective_modalities
    assert "image" in entry.effective_modalities
    assert any("not usable" in w and "audio" in w for w in warnings)
    assert any("video" in w and "not declared" in w for w in warnings)
    assert not errors


def test_vlm_missing_image_errors():
    warnings: list[str] = []
    errors: list[str] = []
    cfg = {"vlm": dict(_base_entry(), modalities=["text"])}
    build_pool_from_config(cfg, warnings=warnings, errors=errors)
    assert any("missing required modalities" in e and "image" in e for e in errors)


def test_omni_accepts_all_declared_without_warn():
    warnings: list[str] = []
    errors: list[str] = []
    cfg = {"omni": dict(_base_entry(), modalities=["text", "audio", "image", "video"])}
    pool = build_pool_from_config(cfg, warnings=warnings, errors=errors)
    entry = pool[Modality.OMNI]
    assert entry.effective_modalities == ["text", "audio", "image", "video"]
    assert not warnings
    assert not errors


def test_omni_missing_audio_errors():
    warnings: list[str] = []
    errors: list[str] = []
    cfg = {"omni": dict(_base_entry(), modalities=["text", "image"])}
    build_pool_from_config(cfg, warnings=warnings, errors=errors)
    assert any("missing required modalities" in e and "audio" in e for e in errors)


def test_parse_model_json_main_warns_on_audio_video():
    warnings: list[str] = []
    raw = json.dumps({
        "main": dict(_base_entry(model_id="gpt-5.4"), modalities=["text", "audio"]),
    })
    bundle = parse_model_json(raw, warnings=warnings)
    # audio 仍保留（main 不剔除），但 warn
    assert "audio" in bundle.main.modalities
    assert any("audio" in w for w in warnings)


def test_parse_model_json_text_always_implicit():
    warnings: list[str] = []
    raw = json.dumps({"main": dict(_base_entry(), modalities=["image"])})
    bundle = parse_model_json(raw, warnings=warnings)
    assert bundle.main.modalities[0] == "text"
    assert "image" in bundle.main.modalities


def test_parse_model_json_requires_provider_model_id():
    with pytest.raises(Exception) as exc:
        parse_model_json(json.dumps({"main": {"provider": "openai"}}))
    assert "model_id" in str(exc.value).lower()


def test_required_and_usable_tables_consistent():
    for key in (Modality.LLM, Modality.VLM, Modality.OMNI):
        assert POOL_REQUIRED_MODALITIES[key] <= POOL_USABLE_MODALITIES[key]


# ---------------------------------------------------------------------------
# probe_and_apply：mock httpx 后验证生效集合更新
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_probe_drops_optional_warns():
    raw = json.dumps({
        # dict 形态：非 text 模态须带正整数数量上限（probe 阶段强制校验）
        "main": dict(_base_entry(model_id="gpt-5.4"), modalities={"text": True, "image": 4}),
        "vlm": dict(_base_entry(model_id="vlm"), modalities={"text": True, "image": 4, "video": 1}),
    })
    bundle = parse_model_json(raw)

    async def fake_probe(config, modalities, **kw):
        # video 失败、其余成功
        return [
            ProbeOutcome(m, ok=(m != "video"), detail="" if m != "video" else "HTTP 400")
            for m in modalities
        ]

    warnings: list[str] = []
    errors: list[str] = []
    with patch("clawarena_team.provider.registry.probe_model", side_effect=fake_probe):
        await probe_and_apply(bundle, warnings=warnings, errors=errors)

    assert "video" not in bundle.pool[Modality.VLM].effective_modalities
    assert any("video" in w and "probe failed" in w for w in warnings)
    assert not errors


@pytest.mark.asyncio
async def test_probe_missing_required_errors():
    raw = json.dumps({
        "main": dict(_base_entry(model_id="gpt-5.4"), modalities=["text"]),
        "omni": dict(_base_entry(model_id="omni"), modalities=["text", "audio"]),
    })
    bundle = parse_model_json(raw)

    async def fake_probe(config, modalities, **kw):
        # 全失败
        return [ProbeOutcome(m, ok=False, detail="boom") for m in modalities if m != "text"] + \
            ([ProbeOutcome("text", ok=True)] if "text" in modalities else [])

    async def fake_probe_simple(config, modalities, **kw):
        return [
            ProbeOutcome(m, ok=(m == "text"), detail="boom" if m != "text" else "")
            for m in modalities
        ]

    warnings: list[str] = []
    errors: list[str] = []
    with patch("clawarena_team.provider.registry.probe_model", side_effect=fake_probe_simple):
        await probe_and_apply(bundle, warnings=warnings, errors=errors)

    assert any("audio" in e and "failed probe" in e for e in errors)
