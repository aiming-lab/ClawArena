"""多模态附件投递与 token 估算 unit tests（不依赖外部 vLLM endpoint）。

覆盖：
- ``clawarena_team.provider.multimodal``：``MultimodalConfig.from_dict`` 默认值与覆盖；
  ``estimate_attachment_tokens`` 三模态分支（含视频按 cv2 帧数精算、音频 WAV 时长精算、
  非 WAV / 取不到帧数时的 fallback）；
- ``attachment_to_content_part`` 三类 part 结构；
- ``attachments_to_parts`` 的 modality 过滤与 size 限制；
- ``stats.tokenizer.TokenCounter``：PNG/MP4/WAV 不再返回 0；mm_cfg 可外注；
- ``agent.harness.AgentHarness._build_mm_followup`` / ``_multimodal_token_overhead``：
  attachment 真的被打包；非 agent 原生模态被剔除。
"""
from __future__ import annotations

import math
import wave
from pathlib import Path

import numpy as np
import pytest

from clawarena_team.provider.multimodal import (
    DEFAULT_MULTIMODAL_CONFIG,
    MultimodalConfig,
    attachment_to_content_part,
    attachments_to_parts,
    build_followup_user_message,
    estimate_attachment_tokens,
)
from clawarena_team.stats.tokenizer import TokenCounter


# -----------------------------------------------------------------------------
# Helpers: 合成最小测试资产
# -----------------------------------------------------------------------------


def _png(p: Path) -> Path:
    p.write_bytes(b"\x89PNG\r\n\x1a\nzzz")
    return p


def _mp4_stub(p: Path) -> Path:
    """伪 mp4 头——cv2 解不出帧数，触发 fallback_tokens 分支。"""
    p.write_bytes(b"\x00\x00\x00\x20ftypisom" + b"\x00" * 64)
    return p


def _mp4_real(p: Path, *, fps: int, n_frames: int) -> Path:
    """用 imageio 合成真实 mp4（cv2 能读出帧数）。

    fix/audit-top10 #9:imageio + cv2 不在 dev 依赖里,原裸 import 让默认装包跑
    pytest 出 3 个 fail;同仓库 tests/test_multimodal_e2e.py:76-79 对同一 import
    已做 pytest.skip,这里一并对齐。要真跑视频测试,装 `imageio` 与 `opencv-python`
    或参考 pyproject 的 [video] extras: `pip install -e .[dev,video]`。
    """
    try:
        import imageio.v2 as imageio  # type: ignore
    except ImportError:
        import pytest
        pytest.skip("imageio not available; install `imageio` to synthesize real mp4")
    writer = imageio.get_writer(str(p), fps=fps, codec="libx264",
                                quality=8, macro_block_size=8)
    for _ in range(n_frames):
        writer.append_data(np.full((64, 64, 3), 128, dtype=np.uint8))
    writer.close()
    return p


def _wav(p: Path, *, seconds: float, sr: int = 16000) -> Path:
    n = int(seconds * sr)
    samples = np.zeros(n, dtype=np.int16)
    with wave.open(str(p), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(samples.tobytes())
    return p


# -----------------------------------------------------------------------------
# MultimodalConfig
# -----------------------------------------------------------------------------


def test_mm_config_default_matches_dict():
    c = MultimodalConfig.default()
    D = DEFAULT_MULTIMODAL_CONFIG
    assert c.image_tokens_per_file == D["image"]["tokens_per_file"]
    assert c.video_tokens_per_frame == D["video"]["tokens_per_frame"]
    assert c.video_max_frames == D["video"]["max_frames"]
    assert c.audio_tokens_per_second == D["audio"]["tokens_per_second"]
    assert c.audio_max_tokens == D["audio"]["max_tokens"]
    assert c.attachment_max_bytes == D["attachment_max_bytes"]


def test_mm_config_overrides_partial():
    c = MultimodalConfig.from_dict({"image": {"tokens_per_file": 999},
                                    "attachment_max_bytes": 42})
    # 显式覆盖
    assert c.image_tokens_per_file == 999
    assert c.attachment_max_bytes == 42
    # 未覆盖的字段保持默认
    assert c.video_tokens_per_frame == DEFAULT_MULTIMODAL_CONFIG["video"]["tokens_per_frame"]


# -----------------------------------------------------------------------------
# estimate_attachment_tokens
# -----------------------------------------------------------------------------


def test_estimate_image_constant(tmp_path: Path):
    cfg = MultimodalConfig.default()
    p = _png(tmp_path / "x.png")
    assert estimate_attachment_tokens(p, "image", cfg) == cfg.image_tokens_per_file


def test_estimate_video_real_frames_short(tmp_path: Path):
    """视频 actual_frames < max_frames：按实际帧计。"""
    cfg = MultimodalConfig.default()
    p = _mp4_real(tmp_path / "v.mp4", fps=10, n_frames=8)  # 8 帧
    tokens = estimate_attachment_tokens(p, "video", cfg)
    assert tokens == 8 * cfg.video_tokens_per_frame


def test_estimate_video_real_frames_capped(tmp_path: Path):
    """视频 actual_frames > max_frames：clip 到 max_frames。"""
    cfg = MultimodalConfig.default()
    p = _mp4_real(tmp_path / "v.mp4", fps=10, n_frames=50)  # 50 帧 > 32
    tokens = estimate_attachment_tokens(p, "video", cfg)
    assert tokens == cfg.video_max_frames * cfg.video_tokens_per_frame


def test_estimate_video_unreadable_fallback(tmp_path: Path):
    """无法解析的伪 mp4：回退到 fallback_tokens。"""
    cfg = MultimodalConfig.default()
    p = _mp4_stub(tmp_path / "bad.mp4")
    assert estimate_attachment_tokens(p, "video", cfg) == cfg.video_fallback_tokens


def test_estimate_audio_wav_precise(tmp_path: Path):
    cfg = MultimodalConfig.default()
    p = _wav(tmp_path / "a.wav", seconds=2.0)
    expected = math.ceil(2.0 * cfg.audio_tokens_per_second)
    assert estimate_attachment_tokens(p, "audio", cfg) == expected


def test_estimate_audio_wav_capped(tmp_path: Path):
    cfg = MultimodalConfig.default()
    p = _wav(tmp_path / "long.wav", seconds=60.0)  # 60 > max_seconds=30
    assert estimate_attachment_tokens(p, "audio", cfg) == cfg.audio_max_tokens


def test_estimate_audio_nonwav_fallback(tmp_path: Path):
    cfg = MultimodalConfig.default()
    p = tmp_path / "x.mp3"
    p.write_bytes(b"ID3" + b"\x00" * 100)
    assert estimate_attachment_tokens(p, "audio", cfg) == cfg.audio_max_tokens


def test_estimate_unknown_modality_returns_zero(tmp_path: Path):
    cfg = MultimodalConfig.default()
    p = _png(tmp_path / "x.png")
    assert estimate_attachment_tokens(p, "text", cfg) == 0


# -----------------------------------------------------------------------------
# attachment_to_content_part
# -----------------------------------------------------------------------------


def test_part_image_data_url(tmp_path: Path):
    p = _png(tmp_path / "x.png")
    part = attachment_to_content_part(p, "image")
    assert part is not None
    assert part["type"] == "image_url"
    assert part["image_url"]["url"].startswith("data:image/png;base64,")


def test_part_video_data_url(tmp_path: Path):
    p = _mp4_stub(tmp_path / "x.mp4")
    part = attachment_to_content_part(p, "video")
    assert part is not None
    assert part["type"] == "video_url"
    assert part["video_url"]["url"].startswith("data:video/mp4;base64,")


def test_part_audio_input_audio_format(tmp_path: Path):
    p = _wav(tmp_path / "a.wav", seconds=0.1)
    part = attachment_to_content_part(p, "audio")
    assert part is not None
    assert part["type"] == "input_audio"
    assert part["input_audio"]["format"] == "wav"
    assert part["input_audio"]["data"]


def test_part_unknown_modality_returns_none(tmp_path: Path):
    p = tmp_path / "x.png"
    p.write_bytes(b"")
    assert attachment_to_content_part(p, "text") is None


def test_followup_message_has_parts_and_note(tmp_path: Path):
    p = _png(tmp_path / "x.png")
    part = attachment_to_content_part(p, "image")
    msg = build_followup_user_message(parts=[part], note_text="hello")
    assert msg is not None
    assert msg["role"] == "user"
    assert isinstance(msg["content"], list)
    assert msg["content"][-1] == {"type": "text", "text": "hello"}


def test_followup_message_empty_parts_returns_none():
    assert build_followup_user_message(parts=[], note_text="x") is None


# -----------------------------------------------------------------------------
# attachments_to_parts
# -----------------------------------------------------------------------------


def test_attachments_to_parts_filters_non_native(tmp_path: Path):
    cfg = MultimodalConfig.default()
    img = _png(tmp_path / "x.png")
    aud = _wav(tmp_path / "a.wav", seconds=0.5)
    parts, paths = attachments_to_parts(
        [(str(img), "image"), (str(aud), "audio")],
        agent_modalities=["text", "image"],
        cfg=cfg,
    )
    types = {p["type"] for p in parts}
    assert "image_url" in types and "input_audio" not in types
    assert str(img) in paths and str(aud) not in paths


def test_attachments_to_parts_drops_oversized(tmp_path: Path):
    cfg = MultimodalConfig.from_dict({"attachment_max_bytes": 4})
    img = _png(tmp_path / "x.png")  # 12 bytes > 4
    parts, paths = attachments_to_parts(
        [(str(img), "image")],
        agent_modalities=["text", "image"],
        cfg=cfg,
    )
    assert parts == [] and paths == []


# -----------------------------------------------------------------------------
# TokenCounter integration
# -----------------------------------------------------------------------------


class _FakeCounter(TokenCounter):
    """避开真实 tokenizer，仅校验 count_file 对多模态的分支接通。"""

    def __init__(self, *, mm_cfg=None):  # noqa: D401
        self.name = "fake"
        self._mm_cfg = mm_cfg or MultimodalConfig.default()

    def count(self, text: str) -> int:
        return max(1, len(text) // 4) if text else 0


def test_token_counter_image_nonzero(tmp_path: Path):
    p = _png(tmp_path / "x.png")
    c = _FakeCounter()
    assert c.count_file(p) == MultimodalConfig.default().image_tokens_per_file


def test_token_counter_video_real(tmp_path: Path):
    p = _mp4_real(tmp_path / "v.mp4", fps=10, n_frames=8)
    c = _FakeCounter()
    cfg = MultimodalConfig.default()
    assert c.count_file(p) == 8 * cfg.video_tokens_per_frame


def test_token_counter_audio_wav_precise(tmp_path: Path):
    p = _wav(tmp_path / "a.wav", seconds=1.0)
    c = _FakeCounter()
    cfg = MultimodalConfig.default()
    assert c.count_file(p) == math.ceil(1.0 * cfg.audio_tokens_per_second)


def test_token_counter_accepts_external_mm_cfg(tmp_path: Path):
    custom = MultimodalConfig.from_dict({"image": {"tokens_per_file": 1000}})
    c = _FakeCounter(mm_cfg=custom)
    p = _png(tmp_path / "x.png")
    assert c.count_file(p) == 1000


def test_token_counter_modality_of():
    assert TokenCounter.modality_of(Path("a.png")) == "image"
    assert TokenCounter.modality_of(Path("a.mp4")) == "video"
    assert TokenCounter.modality_of(Path("a.wav")) == "audio"
    assert TokenCounter.modality_of(Path("a.md")) == "text"


# -----------------------------------------------------------------------------
# AgentHarness wiring
# -----------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_harness_followup_only_native_modality(tmp_path: Path):
    from clawarena_team.agent.harness import AgentHarness, HarnessConfig, HarnessTurn
    from clawarena_team.sandbox import AccessibleScope, ReadTracker
    from clawarena_team.tokenizer import UnifiedTokenizer

    img = _png(tmp_path / "x.png")
    aud = _wav(tmp_path / "a.wav", seconds=0.5)

    class _FakeTok(UnifiedTokenizer):
        def __init__(self): pass
        def count(self, text: str) -> int: return max(1, len(text) // 4)
        def count_messages(self, messages) -> int:
            return sum(self.count(m.get("content", "")) for m in messages)

    h = AgentHarness(
        agent_id="main", system_prompt="sys", provider=None, tools={}, tool_schemas=[],
        scope=AccessibleScope([tmp_path], scenario_root=tmp_path),
        read_tracker=ReadTracker(), cwd=tmp_path, tokenizer=_FakeTok(),
        cfg=HarnessConfig(token_limit=10_000_000, usage_thresholds_pct=[],
                          always_hint_on_real_user=False, max_iterations=1),
        config_dict={}, agent_modalities=["text", "image"],
    )
    h.turns.append(HarnessTurn(
        role="tool_result", content="[image file ...]", tool_call_id="t1",
        attachments=[(str(img), "image"), (str(aud), "audio")],
    ))
    msgs = h._provider_messages()
    tool_idx = next(i for i, m in enumerate(msgs) if m.get("role") == "tool")
    followup = msgs[tool_idx + 1]
    assert followup["role"] == "user"
    types = {p["type"] for p in followup["content"] if isinstance(p, dict)}
    assert "image_url" in types
    assert "input_audio" not in types


@pytest.mark.asyncio
async def test_harness_mm_overhead_added_to_count(tmp_path: Path):
    from clawarena_team.agent.harness import AgentHarness, HarnessConfig, HarnessTurn
    from clawarena_team.sandbox import AccessibleScope, ReadTracker
    from clawarena_team.tokenizer import UnifiedTokenizer

    img = _png(tmp_path / "x.png")

    class _FakeTok(UnifiedTokenizer):
        def __init__(self): pass
        def count(self, text: str) -> int: return 1
        def count_messages(self, messages) -> int: return len(messages)

    h = AgentHarness(
        agent_id="main", system_prompt="sys", provider=None, tools={}, tool_schemas=[],
        scope=AccessibleScope([tmp_path], scenario_root=tmp_path),
        read_tracker=ReadTracker(), cwd=tmp_path, tokenizer=_FakeTok(),
        cfg=HarnessConfig(token_limit=10_000_000, usage_thresholds_pct=[],
                          always_hint_on_real_user=False, max_iterations=1),
        config_dict={}, agent_modalities=["text", "image"],
    )
    base = h._count_prompt_tokens()
    h.turns.append(HarnessTurn(
        role="tool_result", content="...", tool_call_id="t1",
        attachments=[(str(img), "image")],
    ))
    after = h._count_prompt_tokens()
    assert after - base >= MultimodalConfig.default().image_tokens_per_file


@pytest.mark.asyncio
async def test_harness_respects_yaml_mm_config(tmp_path: Path):
    """覆盖 config_dict.multimodal 后，attachment_max_bytes 与 token 估算同步刷新。"""
    from clawarena_team.agent.harness import AgentHarness, HarnessConfig, HarnessTurn
    from clawarena_team.sandbox import AccessibleScope, ReadTracker
    from clawarena_team.tokenizer import UnifiedTokenizer

    img = _png(tmp_path / "x.png")  # 12 字节

    class _FakeTok(UnifiedTokenizer):
        def __init__(self): pass
        def count(self, text: str) -> int: return 1
        def count_messages(self, messages) -> int: return len(messages)

    h = AgentHarness(
        agent_id="main", system_prompt="sys", provider=None, tools={}, tool_schemas=[],
        scope=AccessibleScope([tmp_path], scenario_root=tmp_path),
        read_tracker=ReadTracker(), cwd=tmp_path, tokenizer=_FakeTok(),
        cfg=HarnessConfig(token_limit=10_000_000, usage_thresholds_pct=[],
                          always_hint_on_real_user=False, max_iterations=1),
        config_dict={"multimodal": {
            "attachment_max_bytes": 4,  # 极小，过滤掉 png
            "image": {"tokens_per_file": 9999},
        }},
        agent_modalities=["text", "image"],
    )
    h.turns.append(HarnessTurn(
        role="tool_result", content="...", tool_call_id="t1",
        attachments=[(str(img), "image")],
    ))
    # 因 size > max_bytes 被过滤，followup user 应为 None / 不存在
    msgs = h._provider_messages()
    has_user_after_tool = any(
        msgs[i].get("role") == "tool" and i + 1 < len(msgs)
        and msgs[i + 1].get("role") == "user"
        for i in range(len(msgs))
    )
    assert not has_user_after_tool
    # 但 token 估算仍按 cfg 计入（image_tokens_per_file=9999）
    assert h._multimodal_token_overhead() == 9999
