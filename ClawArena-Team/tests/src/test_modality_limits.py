"""per-modality 数量上限：配置解析、probe 校验、Read prompt 文案、context strip。

对应 C 增强：modalities 升级为带数量的 dict、probe 强制每个非 text effective 模态有正整数
上限、Read tool 描述注入上限、harness 按 per-modality context 上限剥离最旧附件（对齐
claude-code stripExcessMediaItems 的 oldest-first 语义）。
"""
from __future__ import annotations

import pytest

from clawarena_team.provider.base import ProviderError
from clawarena_team.provider.registry import (
    _check_modality_limits,
    _parse_modalities,
)
from clawarena_team.tools.basic import ReadTool
from clawarena_team.agent.harness import AgentHarness, HarnessTurn


# ---------------------------------------------------------------------------
# 配置解析：dict 形态 + list 向后兼容
# ---------------------------------------------------------------------------

def test_parse_modalities_dict_form():
    mods, limits = _parse_modalities({"text": True, "image": 4, "video": 1}, ctx="vlm")
    assert mods == ["text", "image", "video"]
    assert limits == {"image": 4, "video": 1}


def test_parse_modalities_list_form_backward_compatible():
    mods, limits = _parse_modalities(["text", "image"], ctx="vlm")
    assert mods == ["text", "image"]
    assert limits == {}  # 旧 list 无上限，留待 probe 报错要求补


def test_parse_modalities_text_always_implicit():
    mods, limits = _parse_modalities({"image": 4}, ctx="vlm")
    assert mods[0] == "text" and "image" in mods


@pytest.mark.parametrize("bad", [{"image": 0}, {"image": -1}, {"image": True}, {"image": "4"}])
def test_parse_modalities_rejects_non_positive_int(bad):
    with pytest.raises(ProviderError):
        _parse_modalities(bad, ctx="vlm")


# ---------------------------------------------------------------------------
# probe 校验：非 text effective 模态必须有正整数上限
# ---------------------------------------------------------------------------

def test_check_modality_limits_ok():
    errors: list[str] = []
    _check_modality_limits(["text", "image"], {"image": 4}, "pool[vlm]", errors)
    assert errors == []


def test_check_modality_limits_missing():
    errors: list[str] = []
    _check_modality_limits(["text", "image", "video"], {"image": 4}, "pool[vlm]", errors)
    assert len(errors) == 1 and "video" in errors[0]


def test_check_modality_limits_text_only_ok():
    errors: list[str] = []
    _check_modality_limits(["text"], {}, "main", errors)
    assert errors == []


# ---------------------------------------------------------------------------
# Read tool 描述注入上限文案
# ---------------------------------------------------------------------------

def test_read_schema_includes_budget_when_limits_given():
    desc = ReadTool.schema(
        modalities=["text", "image", "video"],
        modality_limits={"image": 4, "video": 1},
        notice_bytes=32768, hard_bytes=262144,
    )["description"]
    assert "Multimodal context budget" in desc
    assert "image=4" in desc and "video=1" in desc


def test_read_schema_omits_budget_for_text_only():
    desc = ReadTool.schema(
        modalities=["text"], modality_limits={}, notice_bytes=32768, hard_bytes=262144,
    )["description"]
    assert "Multimodal context budget" not in desc


# ---------------------------------------------------------------------------
# harness context 级 strip：保留最近 N、剥离最旧
# ---------------------------------------------------------------------------

def _harness_with_turns(modalities, limits, turns):
    h = AgentHarness.__new__(AgentHarness)  # 绕过重 __init__，仅测纯逻辑
    h.turns = turns
    h.agent_modalities = list(modalities)
    h.modality_limits = dict(limits)
    h._media_elided_notified = set()
    return h


def _img_turn(idx):
    return HarnessTurn(role="tool_result", content="", tool_call_id=f"t{idx}",
                       attachments=[(f"/w/img{idx}.png", "image")])


def test_media_elision_strips_oldest_keeps_recent():
    turns = [_img_turn(i) for i in range(5)]
    h = _harness_with_turns(["text", "image"], {"image": 2}, turns)
    elided, dropped = h._media_elision()
    # 5 张图、上限 2 → 剥离最旧 3 张（img0/1/2），保留最近 img3/img4
    assert sorted(p for p, _ in dropped) == ["/w/img0.png", "/w/img1.png", "/w/img2.png"]
    assert elided == {0: {0}, 1: {0}, 2: {0}}


def test_media_elision_per_modality_independent():
    turns = [
        HarnessTurn(role="tool_result", content="", tool_call_id="a",
                    attachments=[(f"/w/i{i}.png", "image") for i in range(3)]),
        HarnessTurn(role="tool_result", content="", tool_call_id="b",
                    attachments=[("/w/v0.mp4", "video")]),
    ]
    h = _harness_with_turns(["text", "image", "video"], {"image": 2, "video": 1}, turns)
    _, dropped = h._media_elision()
    # image 3→剥 1（最旧 i0）；video 1≤1→不剥
    assert dropped == [("/w/i0.png", "image")]


def test_media_elision_no_limit_no_strip():
    # 模态无配置上限（防御路径）→ 不剥离
    turns = [_img_turn(i) for i in range(5)]
    h = _harness_with_turns(["text", "image"], {}, turns)
    elided, dropped = h._media_elision()
    assert elided == {} and dropped == []


def test_media_elision_ignores_non_native_modality():
    # agent 不支持 video → 该模态附件不参与（也不会被发送）
    turns = [
        HarnessTurn(role="tool_result", content="", tool_call_id="a",
                    attachments=[("/w/v0.mp4", "video"), ("/w/v1.mp4", "video")]),
    ]
    h = _harness_with_turns(["text", "image"], {"image": 2}, turns)
    _, dropped = h._media_elision()
    assert dropped == []
