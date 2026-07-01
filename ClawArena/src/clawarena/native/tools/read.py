"""Read tool: 透明吞下文本 + office；对非声明的多模态降级为占位符。"""
from __future__ import annotations

import mimetypes
from typing import Any

from ..prompts import TOOL_DESCRIPTIONS
from ..sandbox import ForbiddenPathError
from ._helpers import (
    AUDIO_EXTS,
    CODE_EXTS,
    DATA_EXTS,
    DOC_EXTS,
    IMAGE_EXTS,
    LOG_EXTS,
    OFFICE_EXTS,
    VIDEO_EXTS,
    detect_modality,
    forbidden,
    params,
    parse_office,
    require_absolute,
)
from .base import BaseTool, ToolContext, ToolExecResult


class ReadTool(BaseTool):
    name = "Read"

    @classmethod
    def schema(cls, **format_kwargs: Any) -> dict[str, Any]:
        modalities = format_kwargs.get("modalities", ["text"])
        groups: list[tuple[str, list[str]]] = [
            ("docs", sorted(DOC_EXTS)),
            ("data / config", sorted(DATA_EXTS)),
            ("logs", sorted(LOG_EXTS)),
            ("code", sorted(CODE_EXTS)),
            (
                "office (auto-parsed to text via openpyxl / python-docx / pypdf)",
                sorted(OFFICE_EXTS),
            ),
        ]
        if "image" in modalities:
            groups.append(("image (native)", sorted(IMAGE_EXTS)))
        if "audio" in modalities:
            groups.append(("audio (native)", sorted(AUDIO_EXTS)))
        if "video" in modalities:
            groups.append(("video (native)", sorted(VIDEO_EXTS)))
        listing_lines = [f"    - {label}: {' '.join(exts)}" for label, exts in groups]

        unsupported = [
            (m, exts)
            for m, exts in (
                ("image", IMAGE_EXTS),
                ("audio", AUDIO_EXTS),
                ("video", VIDEO_EXTS),
            )
            if m not in modalities
        ]
        if unsupported:
            listing_lines.append(
                "  Not natively supported by this agent (returned as a textual placeholder):"
            )
            for m, exts in unsupported:
                listing_lines.append(f"    - {m}: {' '.join(sorted(exts))}")
        extension_listing = "\n" + "\n".join(listing_lines)
        notice_bytes = int(format_kwargs.get("notice_bytes", 32768))
        hard_bytes = int(format_kwargs.get("hard_bytes", 262144))
        desc = TOOL_DESCRIPTIONS["Read"].format(
            modalities=", ".join(modalities),
            extension_listing=extension_listing,
            notice_threshold=f"{notice_bytes // 1024} KiB",
            hard_threshold=f"{hard_bytes // 1024} KiB",
        )
        p = params("Read")
        return {
            "name": cls.name,
            "description": desc,
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": p["file_path"]},
                    "offset": {"type": "integer", "description": p["offset"]},
                    "limit": {"type": "integer", "description": p["limit"]},
                },
                "required": ["file_path"],
            },
        }

    async def run(self, args: dict[str, Any], ctx: ToolContext) -> ToolExecResult:
        raw = args.get("file_path", "")
        resolved = require_absolute(raw)
        if isinstance(resolved, ToolExecResult):
            return resolved
        try:
            real = ctx.scope.check(resolved)
        except ForbiddenPathError:
            return forbidden(raw)
        if not real.exists():
            return ToolExecResult(f"file not found: {raw}", is_error=True)
        if not real.is_file():
            return ToolExecResult(f"not a file: {raw}", is_error=True)
        modality = detect_modality(real)
        counter_key = "text" if modality == "office" else modality
        ctx.modality_counter[counter_key] = ctx.modality_counter.get(counter_key, 0) + 1
        ctx.tools_used.add(self.name)
        ctx.read_tracker.record_read(real)

        if modality in {"image", "audio", "video"} and modality not in ctx.agent_modalities:
            mime, _ = mimetypes.guess_type(str(real))
            size = real.stat().st_size
            # 不挂 attachment：该模态非本 agent 原生，二进制下发也会在 wire 层被
            # agent_modalities 过滤掉，徒增一个会被丢弃的引用。仅回文字占位符。
            return ToolExecResult(
                f"[{modality} file | not natively supported by this agent | "
                f"path={raw} mime={mime or 'unknown'} size={size} bytes] "
                f"This agent supports modalities: {ctx.agent_modalities}."
            )

        if modality in {"text", "office"}:
            if modality == "office":
                text, err = parse_office(real)
                if err:
                    return ToolExecResult(f"read error: {err}", is_error=True)
            else:
                try:
                    text = real.read_text(encoding="utf-8", errors="replace")
                except (OSError, UnicodeError) as e:
                    return ToolExecResult(f"read error: {e}", is_error=True)
            raw_bytes = len(text.encode("utf-8"))
            hard_bytes = int(ctx.config.get("read.hard_bytes", 262144))
            notice_bytes = int(ctx.config.get("read.notice_bytes", 32768))
            max_bytes = int(ctx.config.get("read.max_text_bytes", 524288))
            offset = int(args.get("offset", 0))
            limit = int(args.get("limit", 2000))
            paged = "offset" in args or "limit" in args
            size_label = "parsed text" if modality == "office" else "file"
            if raw_bytes >= hard_bytes and not paged:
                return ToolExecResult(
                    f"{size_label} too large for a single Read: {raw_bytes} bytes >= "
                    f"{hard_bytes}-byte hard cap. Pass `offset` + `limit` to page "
                    f"through a specific slice.",
                    is_error=True,
                )
            data = text.encode("utf-8")
            if len(data) > max_bytes:
                text = data[:max_bytes].decode("utf-8", errors="replace")
            lines = text.splitlines()
            chunk = lines[offset : offset + limit]
            numbered = "\n".join(f"{i + offset + 1}\t{l}" for i, l in enumerate(chunk))
            if raw_bytes >= notice_bytes and not paged:
                notice = (
                    f"[notice: {size_label} is {raw_bytes} bytes (>= {notice_bytes}-byte "
                    f"soft threshold). Showing first {len(chunk)} lines. Pass `offset`+`limit` "
                    f"for a precise slice.]"
                )
                numbered = f"{notice}\n{numbered}" if numbered else notice
            return ToolExecResult(numbered, attachments=[(str(real), "text")])

        mime, _ = mimetypes.guess_type(str(real))
        size = real.stat().st_size
        summary = (
            f"[{modality} file | natively supported | path={raw} "
            f"mime={mime or 'unknown'} size={size} bytes]"
        )
        # 超过内联上限的文件，wire 层不会投递二进制（attachments_to_parts 丢弃）；
        # 在文字摘要里明确告知 agent，避免它以为"已看到"该文件。
        max_bytes = int(ctx.config.get("multimodal.attachment_max_bytes", 10 * 1024 * 1024))
        if size > max_bytes:
            summary += (
                f" [notice: {size} bytes exceeds the {max_bytes}-byte inline cap; "
                f"its binary content will NOT be delivered — rely on this metadata "
                f"or obtain a smaller/representative file]"
            )
        return ToolExecResult(summary, attachments=[(str(real), modality)])
