"""模态探测。

启动 run / resume 时以最小请求实调 provider，验证每个声明的非文本模态确实可用。
失败的模态从 ``effective_modalities`` 中剔除（``text`` 永远保留）。

四个模态各以一份**轻量级合法二进制**做实测（base64 内联，无需文件系统）：

- ``image``：32×32 灰色 PNG（~98B；1×1 部分云端拒收 "unsupported image"，故升至 32×32）
- ``audio``：8000Hz mono 16-bit 静音 WAV（~46B）
- ``video``：64×64 mp4v 4 帧（~980B；16×16 被 Qwen3VLProcessor "patch size too small" 拒收）

资产源自 SMbench ``src/smbench/provider/probe.py``，已在多家 provider 上验证可用。
"""
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any

from ..types import ModelConfig
from .base import BaseProvider, ProviderError


# ---------------------------------------------------------------------------
# 资产：极小的合法二进制，base64 内联
# ---------------------------------------------------------------------------

# 32×32 灰色 PNG (~98B)
_PNG_BASE64 = (
    "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAAKUlEQVR4nO3NMQEAAAjDMED5pGMCvlRA00nqs3m9AwAAAAAAAAAAgMMWvj0BwDVKG0sAAAAASUVORK5CYII="
)

# 8000Hz mono 16-bit 单静音采样 WAV (~46B)
_WAV_BASE64 = (
    "UklGRiYAAABXQVZFZm10IBAAAAABAAEAQB8AAIA+AAACABAAZGF0YQIAAAAAAA=="
)

# 64×64 mp4v 4 帧 (~980B)，由 opencv VideoWriter 生成
_MP4_BASE64 = (
    "AAAAHGZ0eXBpc29tAAACAGlzb21pc28ybXA0MQAAAAhmcmVlAAAAXW1kYXQAAAGzABAHAAABthYHHDbkjbb+Ntv422/jbb+Ntv422/jbb+Ntv422/jbb+Ntv422/jbb+Ntv422/fAAABtmuBn//3AAABtmsBn//3AAABtmuBn//3AAADVG1vb3YAAABsbXZoZAAAAAAAAAAAAAAAAAAAA+gAAA+gAAEAAAEAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAJ/dHJhawAAAFx0a2hkAAAAAwAAAAAAAAAAAAAAAQAAAAAAAA+gAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAQAAAAABAAAAAQAAAAAAAJGVkdHMAAAAcZWxzdAAAAAAAAAABAAAPoAAAAAAAAQAAAAAB921kaWEAAAAgbWRoZAAAAAAAAAAAAAAAAAAAQAAAAQAAVcQAAAAAAC1oZGxyAAAAAAAAAAB2aWRlAAAAAAAAAAAAAAAAVmlkZW9IYW5kbGVyAAAAAaJtaW5mAAAAFHZtaGQAAAABAAAAAAAAAAAAAAAkZGluZgAAABxkcmVmAAAAAAAAAAEAAAAMdXJsIAAAAAEAAAFic3RibAAAANpzdHNkAAAAAAAAAAEAAADKbXA0dgAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAABAAEAASAAAAEgAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABj//wAAAGBlc2RzAAAAAAOAgIBPAAEABICAgEEgEQAAAAAAIAAAAACqBYCAgC8AAAGwAQAAAbWJEwAAAQAAAAEgAMSNiAANAgQIFGMAAAGyTGF2YzYyLjExLjEwMAaAgIABAgAAABRidHJ0AAAAAAAAIAAAAACqAAAAGHN0dHMAAAAAAAAAAQAAAAQAAEAAAAAAFHN0c3MAAAAAAAAAAQAAAAEAAAAcc3RzYwAAAAAAAAABAAAAAQAAAAQAAAABAAAAJHN0c3oAAAAAAAAAAAAAAAQAAAA6AAAACQAAAAkAAAAJAAAAFHN0Y28AAAAAAAAAAQAAACwAAABhdWR0YQAAAFltZXRhAAAAAAAAACFoZGxyAAAAAAAAAABtZGlyYXBwbAAAAAAAAAAAAAAAACxpbHN0AAAAJKl0b28AAAAcZGF0YQAAAAEAAAAATGF2ZjYyLjMuMTAw"
)


@dataclass
class ProbeResult:
    modality: str
    ok: bool
    error: str = ""


def _content_part(modality: str) -> dict[str, Any]:
    if modality == "image":
        return {
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{_PNG_BASE64}"},
        }
    if modality == "audio":
        return {
            "type": "input_audio",
            "input_audio": {"data": _WAV_BASE64, "format": "wav"},
        }
    if modality == "video":
        return {
            "type": "video_url",
            "video_url": {"url": f"data:video/mp4;base64,{_MP4_BASE64}"},
        }
    raise ValueError(f"unknown probe modality: {modality!r}")


def _probe_messages(modality: str) -> list[dict[str, Any]]:
    return [
        {
            "role": "user",
            "content": [_content_part(modality), {"type": "text", "text": "ping"}],
        }
    ]


async def _probe_text(provider: BaseProvider, timeout: float, max_tokens: int) -> ProbeResult:
    try:
        await asyncio.wait_for(
            provider.chat(
                messages=[{"role": "user", "content": "hi"}],
                tools=None,
                max_tokens=max_tokens,
            ),
            timeout=timeout,
        )
        return ProbeResult("text", True)
    except (ProviderError, asyncio.TimeoutError, Exception) as e:  # noqa: BLE001
        return ProbeResult("text", False, str(e))


async def _probe_modal(
    provider: BaseProvider, modality: str, timeout: float, max_tokens: int
) -> ProbeResult:
    """image / audio / video 共用：发一份内联资产 + "ping" 文本。"""
    try:
        await asyncio.wait_for(
            provider.chat(
                messages=_probe_messages(modality), tools=None, max_tokens=max_tokens
            ),
            timeout=timeout,
        )
        return ProbeResult(modality, True)
    except Exception as e:  # noqa: BLE001
        return ProbeResult(modality, False, str(e))


async def probe_modalities(
    provider: BaseProvider, config: ModelConfig, *, timeout: float = 20.0, max_tokens: int = 4
) -> list[ProbeResult]:
    """对 ``config.declared_modalities`` 逐项实测。

    text 必探；image / audio / video 各发一份轻量 base64 资产，2xx 视为可用，任何
    错误（包括 4xx 拒收 / 网络异常 / 超时）视为不可用，回到调用方汇总 warning。
    """
    results: list[ProbeResult] = []
    for m in config.declared_modalities:
        if m == "text":
            results.append(await _probe_text(provider, timeout, max_tokens))
        elif m in {"image", "audio", "video"}:
            results.append(await _probe_modal(provider, m, timeout, max_tokens))
        else:
            results.append(ProbeResult(m, False, f"unknown modality {m}"))
    return results


def apply_probe_results(config: ModelConfig, results: list[ProbeResult]) -> list[str]:
    """把 probe 结果应用到 ``config.effective_modalities``；返回 warning list。"""
    warnings: list[str] = []
    effective = []
    for r in results:
        if r.ok:
            effective.append(r.modality)
        else:
            warnings.append(f"modality {r.modality} probe failed: {r.error}")
    if "text" not in effective:
        effective.insert(0, "text")
    config.effective_modalities = effective
    return warnings
