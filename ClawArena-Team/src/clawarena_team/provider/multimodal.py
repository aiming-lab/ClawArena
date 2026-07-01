"""Multimodal attachment delivery and token estimation — semantics of the provider
protocol layer.

Responsibilities (mirroring claude-code's ``mapToolResultToToolResultBlockParam``):

1. Convert local paths in ``ToolResult.attachments`` into OpenAI list-content parts
   (``image_url`` / ``video_url`` / ``input_audio``).
2. Estimate how many tokens each attachment consumes against the current model's
   processor anchors (so the harness's ``context_size_max`` is measured on the same
   basis as the real remote billing).
3. Decide whether to extract the audio track from containers like mp4 on omni models —
   see ``mp4_extract_audio_track``.

Default anchor values (consistent for Gemma-4 31B / E4B; override in yaml when
switching to another model):

- ``image.tokens_per_file = 280``       — ``vision_soft_tokens_per_image``
- ``video.tokens_per_frame = 70``       — ``max_soft_tokens``
- ``video.max_frames = 32``             — ``num_frames``
- ``audio.tokens_per_second = 25``      — ``audio_ms_per_token=40`` → 1/0.04
- ``audio.max_tokens = 750``            — ``audio_seq_length``

Video duration calculation: actual frame count, capped at
``min(actual_frames, max_frames) × tokens_per_frame``. When cv2 cannot obtain the
frame count, it falls back to ``video.fallback_tokens`` (a conservative upper bound).

mp4 dual-track testing (``/tmp/mm_dual_track*.py``) found that vLLM gemma-4 omni can
currently only recognize one non-text modality per request — when video+audio are
mixed, audio is always lost (even when splitting the user message or inserting an
assistant reply in between). Therefore ``mp4_extract_audio_track`` defaults to
``False``, kept for future compatibility; enabling it still does not extract the audio
track from mp4 and only logs the event.
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
# Default values (kept in sync with the default.yaml multimodal: section and
# CODE_DEFAULTS; this is the single source of truth)
# -----------------------------------------------------------------------------

DEFAULT_MULTIMODAL_CONFIG: dict[str, Any] = {
    "attachment_max_bytes": 10 * 1024 * 1024,  # 10 MB
    "image": {
        "tokens_per_file": 280,
    },
    "video": {
        "tokens_per_frame": 70,
        "max_frames": 32,
        "fallback_tokens": 2240,  # max_frames × tokens_per_frame upper bound
    },
    "audio": {
        "tokens_per_second": 25.0,
        "max_tokens": 750,
        "max_seconds": 30.0,
    },
    # On vLLM gemma-4 omni, mixing video+audio in the same message currently loses the
    # audio (see mm_dual_track*.py for the measurement). Off by default; once vLLM fixes
    # this in the future, set true to enable dual-track mp4 audio-extraction delivery.
    "mp4_extract_audio_track": False,
}


@dataclass(frozen=True)
class MultimodalConfig:
    """A strongly-typed view of the ``multimodal:`` section. ``from_dict`` automatically
    applies default values."""

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
# Token estimation: image is fixed; video is (actual_frames ∧ max_frames) × per_frame;
# audio WAV computes duration precisely via stdlib wave, otherwise a conservative
# upper bound.
# -----------------------------------------------------------------------------


def _audio_duration_sec(path: Path) -> float | None:
    """Use stdlib ``wave`` only for ``.wav``; other formats return None so the caller
    uses the upper-bound fallback."""
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
    """Use cv2 to get ``CAP_PROP_FRAME_COUNT``; returns None if the module is missing or
    the value cannot be read."""
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
    """Return a token estimate for a single attachment.

    - image: a constant ``cfg.image_tokens_per_file`` (Gemma-4
      vision_soft_tokens_per_image is independent of resolution).
    - video: ``min(actual_frames, cfg.video_max_frames) × cfg.video_tokens_per_frame``;
      falls back to ``cfg.video_fallback_tokens`` when the frame count cannot be read.
    - audio: WAV uses ``ceil(duration_sec × tokens_per_second)`` clipped by
      ``max_tokens``; non-WAV falls back to ``cfg.audio_max_tokens``.
    - other modalities: 0.
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
# Wire format: attachment → OpenAI list-content part (base64 data URL / input_audio)
# -----------------------------------------------------------------------------

MMPart = dict[str, Any]


def attachment_to_content_part(path: Path, modality: str) -> MMPart | None:
    """Convert an attachment path into an OpenAI list-content part.

    - image  → ``{"type":"image_url","image_url":{"url":"data:<mime>;base64,..."}}``
    - video  → ``{"type":"video_url","video_url":{"url":"data:<mime>;base64,..."}}``
    - audio  → ``{"type":"input_audio","input_audio":{"data":"<b64>","format":"wav|mp3|..."}}``

    Returns ``None`` when the file cannot be read or the modality is not one of the
    three native types (the caller should skip it).
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
    """Synthesize a user message (approach C): a tool_result followed immediately by a
    user message carrying the base64 parts.

    The vLLM gemma-4 chat-template returns 500 when expanding the ``<image>`` placeholder
    on a tool role; instead, the tool message keeps a text stub, followed immediately by
    a user message carrying the actual binary parts, see ``/tmp/mm_wire.md``.
    """
    if not parts:
        return None
    content: list[MMPart] = list(parts)
    if note_text:
        content.append({"type": "text", "text": note_text})
    return {"role": "user", "content": content}


# -----------------------------------------------------------------------------
# Attachments → part sequence: filter out modalities not native to the agent,
# oversized files, and unreadable files
# -----------------------------------------------------------------------------


def attachments_to_parts(
    attachments: list[tuple[str, str]],
    *,
    agent_modalities: list[str] | tuple[str, ...],
    cfg: MultimodalConfig,
) -> tuple[list[MMPart], list[str]]:
    """Decide which attachments to deliver and build the part list.

    Returns ``(parts, dispatched_paths)``:

    - only attachments whose native modality is in ``agent_modalities`` are packaged;
    - files exceeding ``cfg.attachment_max_bytes`` are dropped (the binary is not
      delivered, but the model can still see the text summary in the tool message,
      which already includes a size field);
    - mp4 dual-track currently sends only video due to the vLLM limitation, without
      extracting the audio track — extend this branch once vLLM is fixed or the model
      is changed.
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
