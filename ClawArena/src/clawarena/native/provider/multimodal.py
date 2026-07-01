"""多模态附件投递与 token 估算 —— provider 协议层的语义。

职责（与 claude-code 的 ``mapToolResultToToolResultBlockParam`` 对位）：

1. 把 ``ToolResultMessage.attachments`` 中的本地路径转为 OpenAI list-content 部件
   （``image_url`` / ``video_url`` / ``input_audio``）。
2. 按当前模型 processor 锚点估算每个附件占多少 token（让 harness 的本地 token 视图与
   远端真实计费同口径）。
3. 决定 mp4 等容器在 omni 模型上是否抽音轨——见 ``mp4_extract_audio_track``。

锚点默认值（Gemma-4 31B / E4B 一致；切到其它模型时在 yaml 覆盖即可）：

- ``image.tokens_per_file = 280``       —— ``vision_soft_tokens_per_image``
- ``video.tokens_per_frame = 70``       —— ``max_soft_tokens``
- ``video.max_frames = 32``             —— ``num_frames``
- ``audio.tokens_per_second = 25``      —— ``audio_ms_per_token=40`` → 1/0.04
- ``audio.max_tokens = 750``            —— ``audio_seq_length``

视频时长精算：实际帧数 + 上限 ``min(actual_frames, max_frames) × tokens_per_frame``。
cv2 拿不到帧数时回退 ``video.fallback_tokens``（保守上限）。

mp4 dual-track 实测发现 vLLM gemma-4 omni 当前在同一请求中只能识别一种非文本模态——
video+audio 混搭时 audio 永远丢失。因此 ``mp4_extract_audio_track`` 默认 ``False``，
留作未来兼容；开启亦不会从 mp4 抽音轨，仅记录到日志。
"""
from __future__ import annotations

import base64
import math
import mimetypes
import wave
from dataclasses import dataclass
from pathlib import Path
from typing import Any


# -----------------------------------------------------------------------------
# 默认值（与 default.yaml multimodal: 节、CODE_DEFAULTS 同步；唯一权威源在此）
# -----------------------------------------------------------------------------

DEFAULT_MULTIMODAL_CONFIG: dict[str, Any] = {
    "attachment_max_bytes": 10 * 1024 * 1024,  # 10 MB
    "image": {
        "tokens_per_file": 280,
    },
    "video": {
        "tokens_per_frame": 70,
        "max_frames": 32,
        "fallback_tokens": 2240,  # max_frames × tokens_per_frame 上限
    },
    "audio": {
        "tokens_per_second": 25.0,
        "max_tokens": 750,
        "max_seconds": 30.0,
    },
    # vLLM gemma-4 omni 当前同消息混搭 video+audio 时 audio 丢失（与 SMbench 同结论）。
    # 默认关闭；未来 vLLM 修复后改 true 即可启用 mp4 抽音轨双轨投递。
    "mp4_extract_audio_track": False,
}


@dataclass(frozen=True)
class MultimodalConfig:
    """``multimodal:`` 节的强类型视图。``from_dict`` 自动套用缺省值。"""

    attachment_max_bytes: int
    image_tokens_per_file: int
    video_tokens_per_frame: int
    video_max_frames: int
    video_fallback_tokens: int
    audio_tokens_per_second: float
    audio_max_tokens: int
    audio_max_seconds: float
    mp4_extract_audio_track: bool

    @classmethod
    def from_dict(cls, d: dict[str, Any] | None) -> "MultimodalConfig":
        d = d or {}
        D = DEFAULT_MULTIMODAL_CONFIG
        img = (d.get("image") or {})
        vid = (d.get("video") or {})
        aud = (d.get("audio") or {})
        return cls(
            attachment_max_bytes=int(d.get("attachment_max_bytes", D["attachment_max_bytes"])),
            image_tokens_per_file=int(img.get("tokens_per_file", D["image"]["tokens_per_file"])),
            video_tokens_per_frame=int(vid.get("tokens_per_frame", D["video"]["tokens_per_frame"])),
            video_max_frames=int(vid.get("max_frames", D["video"]["max_frames"])),
            video_fallback_tokens=int(vid.get("fallback_tokens", D["video"]["fallback_tokens"])),
            audio_tokens_per_second=float(aud.get("tokens_per_second", D["audio"]["tokens_per_second"])),
            audio_max_tokens=int(aud.get("max_tokens", D["audio"]["max_tokens"])),
            audio_max_seconds=float(aud.get("max_seconds", D["audio"]["max_seconds"])),
            mp4_extract_audio_track=bool(d.get("mp4_extract_audio_track", D["mp4_extract_audio_track"])),
        )

    @classmethod
    def default(cls) -> "MultimodalConfig":
        return cls.from_dict(DEFAULT_MULTIMODAL_CONFIG)


# -----------------------------------------------------------------------------
# Token 估算：image 固定；video 按 (actual_frames ∧ max_frames) × per_frame；
# audio WAV 走 stdlib wave 精算时长，否则上限保守。
# -----------------------------------------------------------------------------


def _audio_duration_sec(path: Path) -> float | None:
    """仅对 ``.wav`` 走 stdlib ``wave``；其他格式返回 None 由调用方走上限 fallback。"""
    if path.suffix.lower() != ".wav":
        return None
    try:
        with wave.open(str(path), "rb") as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            if rate <= 0:
                return None
            return frames / float(rate)
    except (wave.Error, OSError, EOFError):
        return None


def _video_frame_count(path: Path) -> int | None:
    """用 cv2 拿 ``CAP_PROP_FRAME_COUNT``；模块缺失或读不到返回 None。"""
    try:
        import cv2  # type: ignore
    except ImportError:
        return None
    cap = cv2.VideoCapture(str(path))
    try:
        if not cap.isOpened():
            return None
        n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        return n if n > 0 else None
    finally:
        cap.release()


def estimate_attachment_tokens(
    path: Path, modality: str, cfg: MultimodalConfig
) -> int:
    """对单个附件返回 token 估算。

    - image：恒定 ``cfg.image_tokens_per_file``（Gemma-4 vision_soft_tokens_per_image
      与分辨率无关）。
    - video：``min(actual_frames, cfg.video_max_frames) × cfg.video_tokens_per_frame``；
      帧数读不到时回退 ``cfg.video_fallback_tokens``。
    - audio：WAV 走 ``ceil(duration_sec × tokens_per_second)`` 并被 ``max_tokens`` clip；
      非 WAV 回退 ``cfg.audio_max_tokens``。
    - 其他 modality：0。
    """
    if modality == "image":
        return cfg.image_tokens_per_file
    if modality == "video":
        n = _video_frame_count(path)
        if n is None:
            return cfg.video_fallback_tokens
        sampled = min(cfg.video_max_frames, n)
        return max(1, sampled) * cfg.video_tokens_per_frame
    if modality == "audio":
        sec = _audio_duration_sec(path)
        if sec is None:
            return cfg.audio_max_tokens
        approx = math.ceil(sec * cfg.audio_tokens_per_second)
        return min(cfg.audio_max_tokens, max(1, approx))
    return 0


# -----------------------------------------------------------------------------
# Wire format：附件 → OpenAI list-content part（base64 data URL / input_audio）
# -----------------------------------------------------------------------------

MMPart = dict[str, Any]


def attachment_to_content_part(path: Path, modality: str) -> MMPart | None:
    """把附件路径转 OpenAI list-content part。

    - image  → ``{"type":"image_url","image_url":{"url":"data:<mime>;base64,..."}}``
    - video  → ``{"type":"video_url","video_url":{"url":"data:<mime>;base64,..."}}``
    - audio  → ``{"type":"input_audio","input_audio":{"data":"<b64>","format":"wav|mp3|..."}}``

    读不到文件或 modality 非三类原生时返回 ``None``（调用方应略过）。
    """
    if modality not in {"image", "video", "audio"}:
        return None
    try:
        data = path.read_bytes()
    except OSError:
        return None
    b64 = base64.b64encode(data).decode("ascii")
    mime, _ = mimetypes.guess_type(str(path))
    if modality == "image":
        return {
            "type": "image_url",
            "image_url": {"url": f"data:{mime or 'image/png'};base64,{b64}"},
        }
    if modality == "video":
        return {
            "type": "video_url",
            "video_url": {"url": f"data:{mime or 'video/mp4'};base64,{b64}"},
        }
    fmt = path.suffix.lstrip(".").lower() or "wav"
    return {"type": "input_audio", "input_audio": {"data": b64, "format": fmt}}


def build_followup_user_message(
    *, parts: list[MMPart], note_text: str
) -> dict[str, Any] | None:
    """合成 user 消息（方案 C）：tool_result 后紧跟一条 user 携带 base64 部件。

    vLLM gemma-4 chat-template 在 tool role 上展开 ``<image>`` 占位符会 500；改让 tool
    消息保留文字 stub，紧跟一条 user 消息携带真正的二进制部件。
    """
    if not parts:
        return None
    content: list[MMPart] = list(parts)
    if note_text:
        content.append({"type": "text", "text": note_text})
    return {"role": "user", "content": content}


# -----------------------------------------------------------------------------
# 附件 → 部件序列：过滤非该 agent 原生模态、超大文件、不可读文件
# -----------------------------------------------------------------------------


def attachments_to_parts(
    attachments: list[tuple[str, str]],
    *,
    agent_modalities: list[str] | tuple[str, ...],
    cfg: MultimodalConfig,
) -> tuple[list[MMPart], list[str]]:
    """决定哪些附件下发，构造部件列表。

    返回 ``(parts, dispatched_paths)``：

    - 仅 agent 原生模态在 ``agent_modalities`` 中的附件被打包；
    - 超过 ``cfg.attachment_max_bytes`` 的文件被丢弃（不投递二进制，模型仍可见 tool
      消息里的文字摘要，里面已有 size 字段）；
    - 当前 mp4 dual-track 因 vLLM 限制只发 video，不抽音轨——后续 vLLM 修复或换模型后
      在此分支扩展即可。
    """
    parts: list[MMPart] = []
    dispatched: list[str] = []
    for raw_path, modality in attachments:
        if modality not in {"image", "audio", "video"}:
            continue
        if modality not in agent_modalities:
            continue
        p = Path(raw_path)
        try:
            size = p.stat().st_size
        except OSError:
            continue
        if size > cfg.attachment_max_bytes:
            continue
        part = attachment_to_content_part(p, modality)
        if part is None:
            continue
        parts.append(part)
        dispatched.append(raw_path)
    return parts, dispatched
