"""wave4 多模态资产 helper 单元测试。

不联网 / 不实际跑 TTS（edge-tts 联网且不稳定）。仅测：
- 图像族 helper 落盘 + validate_image 通过
- 视频族 helper 落盘 + validate_video 通过（最小帧数）
- 校验函数对异常输入正确报错
"""
from __future__ import annotations

import shutil
from pathlib import Path

import pytest

# 资产 helper 需要 PIL / matplotlib / ffmpeg；缺一即跳过整组
PIL = pytest.importorskip("PIL")
plt = pytest.importorskip("matplotlib")

from dataset_lab._common import (
    MAX_ASSET_BYTES,
    render_algorithm_video_mp4,
    render_chart_png,
    render_data_animation_mp4,
    render_engineering_diagram,
    render_handheld_mp4,
    render_medical_image_annotated,
    render_remote_sensing_png,
    render_screen_screenshot,
    render_screencast_mp4,
    validate_image,
    validate_video,
    validate_wav,
)


@pytest.fixture(autouse=True)
def _skip_without_ffmpeg():
    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        pytest.skip("ffmpeg/ffprobe 不可用")


# ---------------------------------------------------------------------------
# Image helpers
# ---------------------------------------------------------------------------


def test_render_chart_png_line(tmp_path: Path):
    out = tmp_path / "chart.png"
    render_chart_png(
        {"x": [1, 2, 3, 4, 5], "y": [10, 20, 15, 30, 25], "label": "reward"},
        out,
        kind="line",
        title="reward curve",
        xlabel="step",
        ylabel="reward",
        annotations=[(3, 15, "dip")],
    )
    assert out.exists()
    validate_image(out)


def test_render_chart_png_multi_series_bar(tmp_path: Path):
    out = tmp_path / "bar.png"
    render_chart_png(
        {
            "Model A": {"x": ["a", "b", "c"], "y": [3, 5, 2]},
            "Model B": {"x": ["a", "b", "c"], "y": [4, 2, 6]},
        },
        out,
        kind="bar",
        title="Comparison",
    )
    validate_image(out)


def test_render_chart_png_heatmap(tmp_path: Path):
    out = tmp_path / "heat.png"
    render_chart_png(
        {
            "matrix": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            "xlabels": ["x1", "x2", "x3"],
            "ylabels": ["y1", "y2", "y3"],
        },
        out,
        kind="heatmap",
        title="hm",
    )
    validate_image(out)


def test_render_medical_image_annotated(tmp_path: Path):
    # 先合成一张灰度底图
    from PIL import Image, ImageDraw

    base = tmp_path / "base.png"
    img = Image.new("RGB", (640, 480), (80, 80, 80))
    d = ImageDraw.Draw(img)
    # 加点纹理避免被"纯色"判定打回
    for x in range(0, 640, 32):
        d.line([(x, 0), (x, 480)], fill=(100, 100, 100))
    img.save(base)

    out = tmp_path / "annotated.png"
    render_medical_image_annotated(
        base,
        out,
        arrows=[((100, 100), (300, 250), "lesion A")],
        masks=[((280, 230, 360, 290), (255, 0, 0, 80))],
        caption="CT 2026-05-24 — patient #4321",
    )
    validate_image(out)


def test_render_engineering_diagram(tmp_path: Path):
    out = tmp_path / "eng.png"
    render_engineering_diagram(
        out,
        nodes=[
            {"id": "A", "label": "Input", "xy": (0, 0), "shape": "rect", "color": "#4E79A7"},
            {"id": "B", "label": "Filter", "xy": (3, 0), "shape": "diamond", "color": "#F28E2B"},
            {"id": "C", "label": "Output", "xy": (6, 0), "shape": "circle", "color": "#59A14F"},
        ],
        edges=[("A", "B", "data"), ("B", "C", "ok")],
        title="Pipeline",
    )
    validate_image(out)


def test_render_screen_screenshot_ide_error(tmp_path: Path):
    out = tmp_path / "ide.png"
    render_screen_screenshot(
        out,
        content_type="ide_error",
        payload={
            "file": "src/main.py",
            "preview_lines": [
                "def divide(a, b):",
                "    return a / b",
                "",
                "divide(1, 0)",
            ],
            "stack": [
                "Traceback (most recent call last):",
                "  File 'src/main.py', line 4, in <module>",
                "    divide(1, 0)",
                "  File 'src/main.py', line 2, in divide",
                "    return a / b",
                "ZeroDivisionError: division by zero",
            ],
        },
    )
    validate_image(out)


def test_render_screen_screenshot_slack(tmp_path: Path):
    out = tmp_path / "slack.png"
    render_screen_screenshot(
        out,
        content_type="slack",
        payload={
            "channel": "#ops",
            "messages": [
                {"user": "alice", "ts": "10:32", "text": "anyone seeing 5xx on prod?"},
                {"user": "bob",   "ts": "10:33", "text": "yeah, looking now"},
            ],
        },
    )
    validate_image(out)


def test_render_screen_screenshot_web_dashboard(tmp_path: Path):
    out = tmp_path / "dash.png"
    render_screen_screenshot(
        out,
        content_type="web_dashboard",
        payload={
            "title": "Latency Dashboard",
            "metrics": [
                {"label": "p50 (ms)", "value": "42", "color": "#4E79A7", "note": "5m"},
                {"label": "p99 (ms)", "value": "320", "color": "#E15759", "note": "5m"},
                {"label": "error %", "value": "0.8%", "color": "#F28E2B"},
            ],
        },
    )
    validate_image(out)


def test_render_screen_screenshot_terminal(tmp_path: Path):
    out = tmp_path / "term.png"
    render_screen_screenshot(
        out,
        content_type="terminal",
        payload={"prompt": "$", "lines": ["$ pytest -k slow", "FAILED tests/test_x.py::test_slow", ">>> RuntimeError"]},
    )
    validate_image(out)


def test_render_remote_sensing_png(tmp_path: Path):
    from PIL import Image, ImageDraw

    base = tmp_path / "sat.png"
    img = Image.new("RGB", (800, 600), (40, 60, 30))
    d = ImageDraw.Draw(img)
    for i in range(0, 800, 20):
        d.line([(i, 0), (i, 600)], fill=(50, 75, 38))
    img.save(base)

    out = tmp_path / "sat_roi.png"
    render_remote_sensing_png(
        base,
        out,
        rois=[((100, 100, 320, 280), "field A", "#F28E2B"), ((400, 350, 700, 550), "field B", "#E15759")],
        caption="Sentinel-2 — 2026-05-12",
    )
    validate_image(out)


# ---------------------------------------------------------------------------
# Video helpers
# ---------------------------------------------------------------------------


def test_render_algorithm_video_mp4_short(tmp_path: Path):
    out = tmp_path / "anim.mp4"

    def frames(ax, i):
        ax.plot([0, 1, 2], [0, i % 5, (i * 2) % 7], color="#4E79A7", linewidth=2)
        ax.set_xlim(-0.5, 2.5)
        ax.set_ylim(-1, 8)
        ax.grid(True, alpha=0.3)

    render_algorithm_video_mp4(frames, out, n_frames=12, fps=6, title="demo")
    validate_video(out)


def test_render_screencast_mp4_short(tmp_path: Path):
    out = tmp_path / "screencast.mp4"
    events = [
        {"t": 0.0, "kind": "type", "payload": "$ pytest -k slow"},
        {"t": 0.5, "kind": "render", "payload": "running tests..."},
        {"t": 1.0, "kind": "type", "payload": "FAILED test_slow"},
        {"t": 1.5, "kind": "click", "payload": (400, 200)},
    ]
    render_screencast_mp4(events, out, fps=6, size=(640, 360))
    validate_video(out)


def test_render_handheld_mp4_short(tmp_path: Path):
    from PIL import Image, ImageDraw

    base = tmp_path / "panel.png"
    img = Image.new("RGB", (640, 480), (200, 50, 50))
    d = ImageDraw.Draw(img)
    d.rectangle([60, 60, 580, 420], outline=(255, 255, 255), width=4)
    d.text((80, 80), "ALARM", fill=(255, 255, 255))
    img.save(base)

    out = tmp_path / "handheld.mp4"
    render_handheld_mp4(base, out, duration_sec=1.0, fps=6, shake_amplitude_px=4)
    validate_video(out)


def test_render_data_animation_mp4_bar_race(tmp_path: Path):
    out = tmp_path / "race.mp4"
    frames = [
        {"labels": ["A", "B", "C"], "values": [1, 2, 3], "label_text": "2024"},
        {"labels": ["A", "B", "C"], "values": [3, 2, 1], "label_text": "2025"},
        {"labels": ["A", "B", "C"], "values": [2, 4, 2], "label_text": "2026"},
    ]
    render_data_animation_mp4(frames, out, kind="bar_race", fps=4, title="vol")
    validate_video(out)


# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------


def test_validate_image_rejects_solid(tmp_path: Path):
    from PIL import Image

    solid = tmp_path / "solid.png"
    Image.new("RGB", (300, 300), (255, 255, 255)).save(solid)
    with pytest.raises(RuntimeError, match="纯色"):
        validate_image(solid)


def test_validate_image_rejects_too_small(tmp_path: Path):
    from PIL import Image, ImageDraw

    small = tmp_path / "tiny.png"
    img = Image.new("RGB", (50, 50), (255, 255, 255))
    ImageDraw.Draw(img).line([(0, 0), (49, 49)], fill=(0, 0, 0))
    img.save(small)
    with pytest.raises(RuntimeError, match="分辨率"):
        validate_image(small)


def test_validate_wav_rejects_short(tmp_path: Path):
    import wave

    p = tmp_path / "tiny.wav"
    with wave.open(str(p), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(b"\x00\x00" * 800)  # 0.05s
    with pytest.raises(RuntimeError, match="时长"):
        validate_wav(p, min_duration_sec=1.0)


def test_validate_video_rejects_empty(tmp_path: Path):
    p = tmp_path / "fake.mp4"
    p.write_bytes(b"")
    with pytest.raises(RuntimeError):
        validate_video(p)


def test_max_asset_size_constant():
    assert MAX_ASSET_BYTES == 5 * 1024 * 1024
