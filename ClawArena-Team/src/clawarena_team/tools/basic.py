"""Basic tools: Read / Write / Edit / Bash / Grep / Glob.

Names and parameters are kept as close as possible to the real claude-code versions
(see ``docs/claude_code_reference.md``):

- Tool names: CapitalCase (``Read``/``Write``/...).
- Path parameters: ``file_path`` (Read/Write/Edit) or ``path`` (the Grep/Glob search
  root), which must be absolute; a non-absolute path returns an error directly, with no
  cwd-resolve.
- Bash: ``description`` is required, ``timeout`` is in milliseconds (max 600000).
- Grep: the full parameter set ``output_mode``/``-A``/``-B``/``-C``/``head_limit``/``offset``/``multiline``/``type``.
- Glob: returns a path list sorted by modification time, newest first.

Any out-of-scope path or unread file returns ``ToolExecResult(is_error=True)`` and
**does not raise**, so the agent can self-recover and the violation is counted.
"""
from __future__ import annotations

import asyncio
import mimetypes
import shutil
from pathlib import Path
from typing import Any

from ..prompts import (
    ABSOLUTE_PATH_REQUIRED_MESSAGE,
    BASH_BACKGROUND_RESULT,
    FORBIDDEN_PATH_MESSAGE,
    READ_BEFORE_EDIT_MESSAGE,
    TOOL_DESCRIPTIONS,
    TOOL_PARAM_DESCRIPTIONS,
)


def _params(tool: str) -> dict[str, str]:
    return TOOL_PARAM_DESCRIPTIONS[tool]
from ..sandbox import ForbiddenPathError
from .base import BaseTool, ToolContext, ToolExecResult

# ---------------------------------------------------------------------------
# Modality / extension detection
# ---------------------------------------------------------------------------
# Text extensions are grouped into four buckets -- "work files / data / logs / code" --
# for the Read schema hint; any extension not listed is still read in as plain text (an
# "everything else" fallback). The three office formats (xlsx/docx/pdf) are parsed to text
# via openpyxl / python-docx / pypdf and then follow the text path, transparently to the agent.

DOC_EXTS = {".md", ".markdown", ".txt", ".rst", ".rtf"}
DATA_EXTS = {
    ".csv", ".tsv", ".json", ".jsonl", ".ndjson",
    ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".env",
    ".xml", ".html", ".htm", ".svg",
}
LOG_EXTS = {".log"}
CODE_EXTS = {
    ".py", ".pyi", ".ipynb",
    ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx",
    ".go", ".rs", ".java", ".kt", ".scala", ".swift",
    ".rb", ".php", ".pl", ".lua",
    ".c", ".cc", ".cpp", ".cxx", ".h", ".hpp", ".cs",
    ".sh", ".bash", ".zsh", ".fish",
    ".sql", ".graphql", ".proto",
    ".tf", ".hcl",
    ".vue", ".svelte",
    ".dockerfile", ".mk", ".makefile",
    ".patch", ".diff",
}
OFFICE_EXTS = {".xlsx", ".docx", ".pdf"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".tiff"}
AUDIO_EXTS = {".wav", ".mp3", ".flac", ".ogg", ".m4a", ".aac"}
VIDEO_EXTS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}


def detect_modality(path: Path) -> str:
    """Return the file's internal Read-tool classification: image/audio/video/office/text.

    "office" is only an internal branch marker; from the agent's perspective office and
    text are both "readable text-like" content.
    """
    ext = path.suffix.lower()
    if ext in IMAGE_EXTS:
        return "image"
    if ext in AUDIO_EXTS:
        return "audio"
    if ext in VIDEO_EXTS:
        return "video"
    if ext in OFFICE_EXTS:
        return "office"
    return "text"


def _parse_office(path: Path) -> tuple[str, str | None]:
    """Parse .xlsx / .docx / .pdf into plain text. Returns (text, error_message).

    When a dependency is missing, returns (empty, a friendly error message) and leaves it
    to the caller to decide whether to raise.
    """
    ext = path.suffix.lower()
    try:
        if ext == ".xlsx":
            import openpyxl  # type: ignore

            wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
            parts: list[str] = []
            for sheet in wb.worksheets:
                parts.append(f"# Sheet: {sheet.title}")
                for row in sheet.iter_rows(values_only=True):
                    parts.append("\t".join("" if v is None else str(v) for v in row))
                parts.append("")
            wb.close()
            return "\n".join(parts), None
        if ext == ".docx":
            from docx import Document  # type: ignore

            doc = Document(str(path))
            parts = []
            for para in doc.paragraphs:
                if para.text:
                    parts.append(para.text)
            for table in doc.tables:
                for row in table.rows:
                    cells = [cell.text.replace("\n", " ").strip() for cell in row.cells]
                    parts.append("\t".join(cells))
            return "\n".join(parts), None
        if ext == ".pdf":
            from pypdf import PdfReader  # type: ignore

            reader = PdfReader(str(path))
            parts = []
            for i, page in enumerate(reader.pages):
                parts.append(f"--- Page {i + 1} ---")
                parts.append(page.extract_text() or "")
            return "\n".join(parts), None
    except ImportError as e:
        return "", (
            f"office parser dependency missing for {ext}: {e.name or e}. "
            f"Install one of: openpyxl (.xlsx) / python-docx (.docx) / pypdf (.pdf)."
        )
    except Exception as e:  # noqa: BLE001 -- parse-layer fallback
        return "", f"office parse error for {path.name}: {type(e).__name__}: {e}"
    return "", f"unsupported office extension: {ext}"


def _require_absolute(p: str) -> Path | ToolExecResult:
    pp = Path(p)
    if not pp.is_absolute():
        return ToolExecResult(
            ABSOLUTE_PATH_REQUIRED_MESSAGE.format(path=p), is_error=True
        )
    return pp.resolve(strict=False)


def _forbidden(path: str) -> ToolExecResult:
    return ToolExecResult(FORBIDDEN_PATH_MESSAGE.format(path=path), is_error=True)


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------


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
                "  Not natively supported by this agent (delegate to a subagent "
                "whose model declares the matching modality):"
            )
            for m, exts in unsupported:
                listing_lines.append(f"    - {m}: {' '.join(sorted(exts))}")
        extension_listing = "\n" + "\n".join(listing_lines)
        # Large-file soft/hard thresholds follow the read.notice_bytes / read.hard_bytes config, so the prompt stays consistent with runtime.
        notice_kib = int(format_kwargs.get("notice_bytes", 32768)) // 1024
        hard_kib = int(format_kwargs.get("hard_bytes", 262144)) // 1024
        # Multimodal context budget: for each native non-text modality, keep at most the N
        # most recent attachments and strip the oldest beyond that. For a text-only agent
        # (no limits) this bullet is omitted entirely.
        limits = format_kwargs.get("modality_limits") or {}
        budget_pairs = [
            (m, limits[m]) for m in ("image", "audio", "video")
            if m in modalities and isinstance(limits.get(m), int) and limits[m] > 0
        ]
        if budget_pairs:
            pretty = ", ".join(f"{m}={n}" for m, n in budget_pairs)
            multimodal_budget = (
                f"- Multimodal context budget: at most the most recent of each native "
                f"non-text modality is retained in this agent's context ({pretty}). "
                f"When a modality exceeds its limit (e.g. many images read across parallel "
                f"calls), the OLDEST attachments are auto-elided to a text placeholder and a "
                f"<system-reminder> lists what was dropped — re-Read a file to bring it back "
                f"as the most recent. Keep parallel multimodal reads within these limits.\n"
            )
        else:
            multimodal_budget = ""
        desc = TOOL_DESCRIPTIONS["Read"].format(
            modalities=", ".join(modalities),
            extension_listing=extension_listing,
            notice_kib=notice_kib,
            hard_kib=hard_kib,
            multimodal_budget=multimodal_budget,
        )
        p = _params("Read")
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
        resolved = _require_absolute(raw)
        if isinstance(resolved, ToolExecResult):
            return resolved
        try:
            real = ctx.scope.check(resolved)
        except ForbiddenPathError:
            return _forbidden(raw)
        if not real.exists():
            return ToolExecResult(f"file not found: {raw}", is_error=True)
        if not real.is_file():
            return ToolExecResult(f"not a file: {raw}", is_error=True)
        modality = detect_modality(real)
        # office counts as text for counters and attachments (it is text once parsed)
        counter_key = "text" if modality == "office" else modality
        ctx.modality_counter[counter_key] = ctx.modality_counter.get(counter_key, 0) + 1
        ctx.tools_used.add(self.name)
        ctx.read_tracker.record_read(real)

        if modality in {"image", "audio", "video"} and modality not in ctx.agent_modalities:
            # This agent does not natively support this modality: return a text hint and
            # **no attachment** -- once attached, the harness would actually base64-deliver
            # it to a model that cannot read it, wasting tokens; instead, the attachment is
            # only seen once the main agent explicitly delegates to a subagent.
            mime, _ = mimetypes.guess_type(str(real))
            size = real.stat().st_size
            return ToolExecResult(
                f"[{modality} file | not natively supported by this agent | "
                f"path={raw} mime={mime or 'unknown'} size={size} bytes] "
                f"This agent supports modalities: {ctx.agent_modalities}. "
                f"Delegate to a subagent whose model natively supports the "
                f"`{modality}` modality (use CreateSubagent + RunSubagent)."
            )

        if modality in {"text", "office"}:
            if modality == "office":
                text, err = _parse_office(real)
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
                    f"{hard_bytes}-byte hard cap. Either pass `offset` + `limit` to page "
                    f"through a specific slice, or delegate the full read to an `llm` "
                    f"subagent (CreateSubagent + RunSubagent) and have it return a summary.",
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
                    f"for a precise slice, or delegate the full read to an `llm` subagent "
                    f"to keep your context budget free.]"
                )
                numbered = f"{notice}\n{numbered}" if numbered else notice
            return ToolExecResult(numbered, attachments=[(str(real), "text")])

        # Natively-supported non-text: the attachment is handed to the provider over the
        # multimodal channel, and content keeps a summary description.
        # harness._provider_messages appends a user message after this tool_result carrying
        # the base64 part (approach C; see multimodal.py and /tmp/mm_wire.md).
        mime, _ = mimetypes.guess_type(str(real))
        size = real.stat().st_size
        max_bytes = int(ctx.config.get("multimodal.attachment_max_bytes", 10 * 1024 * 1024))
        if size > max_bytes:
            return ToolExecResult(
                f"[{modality} file | path={raw} mime={mime or 'unknown'} size={size} bytes] "
                f"too large to inline ({size} > {max_bytes}-byte attachment cap). "
                f"Use a smaller file or raise read.attachment_max_bytes."
            )
        summary = (
            f"[{modality} file | natively supported | path={raw} "
            f"mime={mime or 'unknown'} size={size} bytes]"
        )
        return ToolExecResult(summary, attachments=[(str(real), modality)])


# ---------------------------------------------------------------------------
# Write
# ---------------------------------------------------------------------------


class WriteTool(BaseTool):
    name = "Write"
    description = TOOL_DESCRIPTIONS["Write"]

    @classmethod
    def schema(cls, **_: Any) -> dict[str, Any]:
        p = _params("Write")
        return {
            "name": cls.name,
            "description": cls.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": p["file_path"]},
                    "content": {"type": "string", "description": p["content"]},
                },
                "required": ["file_path", "content"],
            },
        }

    async def run(self, args: dict[str, Any], ctx: ToolContext) -> ToolExecResult:
        raw = args.get("file_path", "")
        content = args.get("content", "")
        resolved = _require_absolute(raw)
        if isinstance(resolved, ToolExecResult):
            return resolved
        try:
            real = ctx.scope.check(resolved)
        except ForbiddenPathError:
            return _forbidden(raw)
        if real.exists() and not ctx.read_tracker.can_modify(real):
            return ToolExecResult(READ_BEFORE_EDIT_MESSAGE.format(path=raw), is_error=True)
        real.parent.mkdir(parents=True, exist_ok=True)
        try:
            real.write_text(content, encoding="utf-8")
        except OSError as e:
            return ToolExecResult(f"write error: {e}", is_error=True)
        ctx.tools_used.add(self.name)
        ctx.read_tracker.record_read(real)
        return ToolExecResult(f"wrote {len(content)} chars to {raw}")


# ---------------------------------------------------------------------------
# Edit
# ---------------------------------------------------------------------------


class EditTool(BaseTool):
    name = "Edit"
    description = TOOL_DESCRIPTIONS["Edit"]

    @classmethod
    def schema(cls, **_: Any) -> dict[str, Any]:
        p = _params("Edit")
        return {
            "name": cls.name,
            "description": cls.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": p["file_path"]},
                    "old_string": {"type": "string", "description": p["old_string"]},
                    "new_string": {"type": "string", "description": p["new_string"]},
                    "replace_all": {
                        "type": "boolean",
                        "default": False,
                        "description": p["replace_all"],
                    },
                },
                "required": ["file_path", "old_string", "new_string"],
            },
        }

    async def run(self, args: dict[str, Any], ctx: ToolContext) -> ToolExecResult:
        raw = args.get("file_path", "")
        old_s = args.get("old_string", "")
        new_s = args.get("new_string", "")
        replace_all = bool(args.get("replace_all", False))
        resolved = _require_absolute(raw)
        if isinstance(resolved, ToolExecResult):
            return resolved
        try:
            real = ctx.scope.check(resolved)
        except ForbiddenPathError:
            return _forbidden(raw)
        if not real.exists():
            return ToolExecResult(f"file not found: {raw}", is_error=True)
        if not ctx.read_tracker.can_modify(real):
            return ToolExecResult(READ_BEFORE_EDIT_MESSAGE.format(path=raw), is_error=True)
        text = real.read_text(encoding="utf-8", errors="replace")
        if old_s not in text:
            return ToolExecResult(f"edit error: old_string not found in {raw}", is_error=True)
        if not replace_all and text.count(old_s) > 1:
            return ToolExecResult(
                f"edit error: old_string is ambiguous ({text.count(old_s)} matches) in {raw}; "
                "provide more surrounding context or set replace_all=true.",
                is_error=True,
            )
        new_text = text.replace(old_s, new_s) if replace_all else text.replace(old_s, new_s, 1)
        real.write_text(new_text, encoding="utf-8")
        ctx.tools_used.add(self.name)
        ctx.read_tracker.record_read(real)
        return ToolExecResult(f"edited {raw}")


# ---------------------------------------------------------------------------
# Bash
# ---------------------------------------------------------------------------


class BashTool(BaseTool):
    name = "Bash"
    description = TOOL_DESCRIPTIONS["Bash"]

    @classmethod
    def schema(cls, **format_kwargs: Any) -> dict[str, Any]:
        p = _params("Bash")
        # The default timeout follows bash.default_timeout_ms (same source as the harness ToolContext).
        default_ms = int(format_kwargs.get("default_timeout_ms", 120000))
        m = default_ms / 60000
        default_min = str(int(m)) if m == int(m) else f"{m:.1f}"
        desc = TOOL_DESCRIPTIONS["Bash"].format(default_ms=default_ms, default_min=default_min)
        return {
            "name": cls.name,
            "description": desc,
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": p["command"]},
                    "description": {"type": "string", "description": p["description"]},
                    "timeout": {"type": "number", "description": p["timeout"].format(default_ms=default_ms)},
                    "run_in_background": {
                        "type": "boolean",
                        "default": False,
                        "description": p["run_in_background"],
                    },
                },
                "required": ["command", "description"],
            },
        }

    async def _run_command(
        self, command: str, cwd: str, timeout_sec: float, max_bytes: int
    ) -> tuple[int | None, str]:
        proc = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd,
        )
        try:
            stdout_b, stderr_b = await asyncio.wait_for(proc.communicate(), timeout=timeout_sec)
        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
            return None, f"bash timeout after {int(timeout_sec * 1000)}ms"
        stdout = stdout_b[:max_bytes].decode("utf-8", errors="replace")
        stderr = stderr_b[:max_bytes].decode("utf-8", errors="replace")
        rc = proc.returncode if proc.returncode is not None else -1
        return rc, f"exit={rc}\n--- stdout ---\n{stdout}\n--- stderr ---\n{stderr}"

    async def run(self, args: dict[str, Any], ctx: ToolContext) -> ToolExecResult:
        command = args.get("command", "")
        # Default 120000ms = 120s; cap 600000ms = 10min.
        default_ms = int(ctx.config.get("bash.default_timeout_ms", 120000))
        timeout_ms = int(args.get("timeout", default_ms))
        timeout_ms = max(1, min(timeout_ms, 600000))
        timeout_sec = timeout_ms / 1000.0
        max_bytes = int(ctx.config.get("bash.max_output_bytes", 65536))
        ctx.tools_used.add(self.name)

        # Background execution: mirrors claude-code's native run_in_background. Takes effect
        # only when this agent holds the unified background registry (i.e. the main agent);
        # a subagent has no registry -> it degrades to synchronous execution (a subagent must
        # finish before returning to main anyway).
        background = bool(args.get("run_in_background", False))
        if background and ctx.background is not None:
            ctx.bash_mode_counter["background"] = ctx.bash_mode_counter.get("background", 0) + 1
            cwd = str(ctx.cwd)
            task_id = ctx.background.new_task_id("bash")

            async def _bg_body() -> str:
                _rc, payload = await self._run_command(command, cwd, timeout_sec, max_bytes)
                return BASH_BACKGROUND_RESULT.format(
                    task_id=task_id, command=command, result=payload
                )

            ctx.background.spawn("bash", _bg_body(), task_id=task_id)
            return ToolExecResult(
                f"background bash started, task_id={task_id}. "
                f"You'll receive a <task-notification> when it completes; "
                f"do not poll — continue with other work."
            )

        ctx.bash_mode_counter["runtime"] = ctx.bash_mode_counter.get("runtime", 0) + 1
        rc, payload = await self._run_command(command, str(ctx.cwd), timeout_sec, max_bytes)
        if rc is None:
            return ToolExecResult(payload, is_error=True)
        return ToolExecResult(payload, is_error=rc != 0)


# ---------------------------------------------------------------------------
# Grep
# ---------------------------------------------------------------------------


class GrepTool(BaseTool):
    name = "Grep"
    description = TOOL_DESCRIPTIONS["Grep"]

    @classmethod
    def schema(cls, **_: Any) -> dict[str, Any]:
        p = _params("Grep")
        return {
            "name": cls.name,
            "description": cls.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": p["pattern"]},
                    "path": {"type": "string", "description": p["path"]},
                    "glob": {"type": "string", "description": p["glob"]},
                    "type": {"type": "string", "description": p["type"]},
                    "output_mode": {
                        "type": "string",
                        "enum": ["content", "files_with_matches", "count"],
                        "description": p["output_mode"],
                    },
                    "-i": {"type": "boolean", "description": p["-i"]},
                    "-n": {"type": "boolean", "description": p["-n"]},
                    "-A": {"type": "number", "description": p["-A"]},
                    "-B": {"type": "number", "description": p["-B"]},
                    "-C": {"type": "number", "description": p["-C"]},
                    "head_limit": {"type": "number", "description": p["head_limit"]},
                    "offset": {"type": "number", "description": p["offset"]},
                    "multiline": {"type": "boolean", "description": p["multiline"]},
                },
                "required": ["pattern"],
            },
        }

    async def run(self, args: dict[str, Any], ctx: ToolContext) -> ToolExecResult:
        pattern = args.get("pattern", "")
        raw_path = args.get("path")
        if raw_path is None:
            real = ctx.cwd
        else:
            resolved = _require_absolute(raw_path)
            if isinstance(resolved, ToolExecResult):
                return resolved
            try:
                real = ctx.scope.check(resolved)
            except ForbiddenPathError:
                return _forbidden(raw_path)

        rg = shutil.which("rg")
        if rg is None:
            return ToolExecResult("grep error: ripgrep (rg) is not installed", is_error=True)

        output_mode = args.get("output_mode", "files_with_matches")
        cmd = [rg, "--no-heading"]
        if output_mode == "content":
            show_n = args.get("-n", True)
            cmd.append("--with-filename")
            if show_n:
                cmd.append("-n")
            for flag, key in (("-A", "-A"), ("-B", "-B"), ("-C", "-C")):
                v = args.get(key)
                if v is not None:
                    cmd.extend([flag, str(int(v))])
        elif output_mode == "files_with_matches":
            cmd.append("-l")
        elif output_mode == "count":
            cmd.append("-c")
        else:
            return ToolExecResult(f"grep error: unknown output_mode {output_mode!r}", is_error=True)

        if args.get("-i"):
            cmd.append("-i")
        if args.get("multiline"):
            cmd.extend(["-U", "--multiline-dotall"])
        if args.get("glob"):
            cmd.extend(["--glob", args["glob"]])
        if args.get("type"):
            cmd.extend(["--type", args["type"]])

        cmd.append(pattern)
        cmd.append(str(real))

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(ctx.cwd),
        )
        stdout_b, stderr_b = await proc.communicate()
        ctx.tools_used.add(self.name)
        out = stdout_b.decode("utf-8", errors="replace")
        if not out and proc.returncode not in (0, 1) and stderr_b:
            return ToolExecResult(stderr_b.decode("utf-8", errors="replace"), is_error=True)

        lines = out.splitlines()
        offset = int(args.get("offset", 0) or 0)
        head = args.get("head_limit")
        if head is not None:
            lines = lines[offset : offset + int(head)]
        elif offset:
            lines = lines[offset:]
        if not lines:
            return ToolExecResult("(no matches)")
        return ToolExecResult("\n".join(lines))


# ---------------------------------------------------------------------------
# Glob
# ---------------------------------------------------------------------------


class GlobTool(BaseTool):
    name = "Glob"
    description = TOOL_DESCRIPTIONS["Glob"]

    @classmethod
    def schema(cls, **_: Any) -> dict[str, Any]:
        p = _params("Glob")
        return {
            "name": cls.name,
            "description": cls.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": p["pattern"]},
                    "path": {"type": "string", "description": p["path"]},
                },
                "required": ["pattern"],
            },
        }

    async def run(self, args: dict[str, Any], ctx: ToolContext) -> ToolExecResult:
        pattern = args.get("pattern", "")
        raw_path = args.get("path")
        if raw_path is None:
            real = ctx.cwd
        else:
            resolved = _require_absolute(raw_path)
            if isinstance(resolved, ToolExecResult):
                return resolved
            try:
                real = ctx.scope.check(resolved)
            except ForbiddenPathError:
                return _forbidden(raw_path)
        if not real.exists():
            return ToolExecResult("(no matches)")

        candidates = [p for p in real.glob(pattern) if ctx.scope.is_allowed(p)]
        candidates.sort(key=lambda p: p.stat().st_mtime if p.exists() else 0.0, reverse=True)
        ctx.tools_used.add(self.name)
        if not candidates:
            return ToolExecResult("(no matches)")
        return ToolExecResult("\n".join(str(p) for p in candidates[:1000]))
