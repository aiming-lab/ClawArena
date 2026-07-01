"""端到端：真实 vLLM gemma-4 端点 + 完整 AgentHarness + 真实 ReadTool。

跳过条件：endpoint 不可达。这是 long-running 集成测试，本地存在两个 serve 时跑。
固定锚点：
- 8900 main: gemma-4-31b-it，modalities=text+image+video
- 8902 omni: gemma-4-e4b-it ，modalities=text+image+video+audio

测试资产由 fixture 现场合成，不依赖外部数据集：
- PNG 红底中央 'STAR' 64pt 白字
- MP4 256x256 30 帧 15fps 绿色方块从左到右
- WAV 16kHz 单声道 2s 440Hz 正弦
"""
from __future__ import annotations

import math
import socket
import wave
from pathlib import Path

import numpy as np
import pytest
from PIL import Image, ImageDraw, ImageFont

from clawarena_team.agent.harness import AgentHarness, HarnessConfig
from clawarena_team.provider.openai_compat import OpenAICompatProvider
from clawarena_team.sandbox import AccessibleScope, ReadTracker
from clawarena_team.tokenizer import UnifiedTokenizer
from clawarena_team.tools.basic import ReadTool
from clawarena_team.types import ModelConfig


# ---------------------------------------------------------------------------
# Skip helpers
# ---------------------------------------------------------------------------


def _endpoint_alive(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=1.0):
            return True
    except OSError:
        return False


def _require(host: str, port: int) -> None:
    if not _endpoint_alive(host, port):
        pytest.skip(f"vLLM endpoint {host}:{port} not reachable")


# ---------------------------------------------------------------------------
# Asset fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def img_path(tmp_path_factory) -> Path:
    p = tmp_path_factory.mktemp("mm_e2e") / "star.png"
    img = Image.new("RGB", (256, 256), color=(220, 30, 30))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64
        )
    except OSError:
        font = ImageFont.load_default()
    text = "STAR"
    bbox = d.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(((256 - w) / 2, (256 - h) / 2 - 10), text, fill=(255, 255, 255), font=font)
    img.save(p, format="PNG")
    return p


@pytest.fixture(scope="module")
def vid_path(tmp_path_factory) -> Path:
    try:
        import imageio.v2 as imageio  # type: ignore
    except ImportError:
        pytest.skip("imageio not available; cannot synthesize MP4 for e2e")
    p = tmp_path_factory.mktemp("mm_e2e") / "slide.mp4"
    w, h, fps, n = 256, 256, 15, 30
    writer = imageio.get_writer(str(p), fps=fps, codec="libx264",
                                quality=8, macro_block_size=8)
    for i in range(n):
        frame = np.full((h, w, 3), 240, dtype=np.uint8)
        x0 = int(20 + (w - 80) * i / max(n - 1, 1))
        frame[80:160, x0:x0 + 40, :] = (20, 180, 60)
        writer.append_data(frame)
    writer.close()
    return p


@pytest.fixture(scope="module")
def aud_path(tmp_path_factory) -> Path:
    p = tmp_path_factory.mktemp("mm_e2e") / "tone.wav"
    sr, dur, freq = 16000, 2.0, 440.0
    n = int(sr * dur)
    samples = (0.6 * np.sin(2 * math.pi * freq * np.arange(n) / sr) * 32767).astype(np.int16)
    with wave.open(str(p), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(samples.tobytes())
    return p


# ---------------------------------------------------------------------------
# Harness factory
# ---------------------------------------------------------------------------


class _Provider(OpenAICompatProvider):
    async def chat(self, *, messages, tools=None, **kwargs):
        kwargs.setdefault("max_tokens", 120)
        kwargs.setdefault("temperature", 0.0)
        return await super().chat(messages=messages, tools=tools, **kwargs)


def _make_harness(*, endpoint: str, model_id: str, modalities: list[str], cwd: Path):
    cfg = ModelConfig(provider="openai_compat", model_id=model_id,
                      api_base=endpoint, modalities=modalities)
    provider = _Provider(cfg)
    scope = AccessibleScope([cwd], scenario_root=cwd)
    return AgentHarness(
        agent_id="main",
        system_prompt=(
            "You are a careful assistant. To answer questions about files, "
            "use the Read tool with the absolute path. After Read, respond with "
            "ONE short sentence describing the file content."
        ),
        provider=provider,
        tools={"Read": ReadTool()},
        tool_schemas=[ReadTool.schema(modalities=modalities)],
        scope=scope,
        read_tracker=ReadTracker(),
        cwd=cwd,
        tokenizer=UnifiedTokenizer(tokenizer_source="qwen3", template_source="qwen3"),
        cfg=HarnessConfig(token_limit=200_000, usage_thresholds_pct=[],
                          always_hint_on_real_user=False, max_iterations=4),
        config_dict={},
        agent_modalities=modalities,
    )


# ---------------------------------------------------------------------------
# Cases
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_e2e_image_31b(img_path: Path):
    _require("127.0.0.1", 8900)
    h = _make_harness(endpoint="http://127.0.0.1:8900/v1",
                      model_id="gemma-4-31b-it",
                      modalities=["text", "image", "video"],
                      cwd=img_path.parent)
    answer = await h.send_user(
        f"What is the single word visible on this image? Reply with that word only. The file is at {img_path}.",
        is_real_question=True,
    )
    assert "star" in answer.lower()
    assert h.modality_counter.get("image", 0) == 1
    # context_size_max 应含 image overhead (>= 280)
    assert h.context_size_max >= 280


@pytest.mark.asyncio
async def test_e2e_video_31b(vid_path: Path):
    _require("127.0.0.1", 8900)
    h = _make_harness(endpoint="http://127.0.0.1:8900/v1",
                      model_id="gemma-4-31b-it",
                      modalities=["text", "image", "video"],
                      cwd=vid_path.parent)
    answer = await h.send_user(
        f"What color is the moving square in this video? Reply with one word. The file is at {vid_path}.",
        is_real_question=True,
    )
    assert "green" in answer.lower()
    assert h.modality_counter.get("video", 0) == 1
    assert h.context_size_max >= 2240


@pytest.mark.asyncio
async def test_e2e_audio_e4b(aud_path: Path):
    _require("127.0.0.1", 8902)
    h = _make_harness(endpoint="http://127.0.0.1:8902/v1",
                      model_id="gemma-4-e4b-it",
                      modalities=["text", "image", "video", "audio"],
                      cwd=aud_path.parent)
    answer = await h.send_user(
        f"Briefly describe the audio. Is it speech, music, or a pure tone? The file is at {aud_path}.",
        is_real_question=True,
    )
    keywords = ["tone", "sine", "beep", "buzz", "hum", "frequency", "pitch"]
    assert any(k in answer.lower() for k in keywords), f"unexpected: {answer!r}"
    assert h.modality_counter.get("audio", 0) == 1
