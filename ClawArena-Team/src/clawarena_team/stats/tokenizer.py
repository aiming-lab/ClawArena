"""TokenCounter: a thin wrapper that uniformly exposes ``count`` and ``count_file`` to upper layers.

By default it uses the ClawArena-Team ``UnifiedTokenizer`` (helper/tokenizer/Qwen3.5-0.8B).
It also accepts tokenizers from other sources, such as a tiktoken short name or a
HuggingFace repo id: the resolution path is the same as ``UnifiedTokenizer``
(short-name mapping → local → HF).

Non-text attachments (image / audio / video) are estimated by ``MultimodalConfig``
anchors; the authoritative defaults live in
``clawarena_team.provider.multimodal.DEFAULT_MULTIMODAL_CONFIG``. The offline stats
view keeps the same convention as ``AgentHarness._count_prompt_tokens``, avoiding
the discrepancy where the local view is 0 while the provider actually bills.
``mm_cfg`` may be passed explicitly at construction to stay in sync with the
runtime yaml; if omitted, fallback constants are used.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from ..provider.multimodal import MultimodalConfig, estimate_attachment_tokens
from ..tokenizer import UnifiedTokenizer


# Non-text suffixes are estimated via ``clawarena_team.multimodal.estimate_attachment_tokens``
# (image=280, video=2240, audio≤750). Consistent with the Read tool grouping in
# ``clawarena_team.tools.basic``: the full text-like set + the three office types
# (the latter are accounted after being parsed to text).
_TEXT_EXT = {
    # docs
    ".md", ".markdown", ".txt", ".rst", ".rtf",
    # data / config
    ".csv", ".tsv", ".json", ".jsonl", ".ndjson",
    ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".env",
    ".xml", ".html", ".htm", ".svg", ".css", ".scss",
    # logs
    ".log", ".eml", ".ics",
    # code
    ".py", ".pyi", ".ipynb",
    ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx",
    ".go", ".rs", ".java", ".kt", ".scala", ".swift",
    ".rb", ".php", ".pl", ".lua",
    ".c", ".cc", ".cpp", ".cxx", ".h", ".hpp", ".cs",
    ".sh", ".bash", ".zsh", ".fish",
    ".sql", ".graphql", ".proto", ".tf", ".hcl",
    ".vue", ".svelte",
    ".dockerfile", ".mk", ".makefile",
    ".patch", ".diff",
    # legacy / misc
    ".jinja", ".j2", ".tex", ".bib", ".lock",
}

# Office files are parsed to text via ``clawarena_team.tools.basic._parse_office`` and
# then counted for tokens, consistent with the view the runtime Read tool sees.
_OFFICE_EXT = {".xlsx", ".docx", ".pdf"}

# Non-text attachment suffixes are looked up by modality, corresponding to ``clawarena_team.tools.basic``'s IMAGE/AUDIO/VIDEO_EXTS.
_MM_EXT_TO_MODALITY: dict[str, str] = {
    # image
    ".png": "image", ".jpg": "image", ".jpeg": "image", ".gif": "image",
    ".bmp": "image", ".webp": "image", ".tiff": "image",
    # audio
    ".wav": "audio", ".mp3": "audio", ".flac": "audio", ".ogg": "audio",
    ".m4a": "audio", ".aac": "audio",
    # video
    ".mp4": "video", ".mov": "video", ".avi": "video", ".mkv": "video", ".webm": "video",
}


class TokenCounter:
    """Unified token counter."""

    def __init__(self, source: str = "qwen3", *, mm_cfg: Optional[MultimodalConfig] = None):
        self.name = source
        self._tok = UnifiedTokenizer(tokenizer_source=source, template_source="qwen3")
        self._mm_cfg = mm_cfg or MultimodalConfig.default()

    @classmethod
    def is_textual(cls, path: Path) -> bool:
        ext = path.suffix.lower()
        return ext in _TEXT_EXT or ext in _OFFICE_EXT

    @classmethod
    def modality_of(cls, path: Path) -> str:
        """Return ``image`` / ``audio`` / ``video`` / ``text`` (office maps to text, consistent with the Read tool)."""
        ext = path.suffix.lower()
        return _MM_EXT_TO_MODALITY.get(ext, "text")

    def count(self, text: str) -> int:
        if not text:
            return 0
        try:
            return self._tok.count(text)
        except Exception:
            return max(1, len(text) // 4)

    def count_file(self, path: Path) -> int:
        if not path.exists() or not path.is_file():
            return 0
        ext = path.suffix.lower()
        if ext in _OFFICE_EXT:
            try:
                from ..tools.basic import _parse_office

                text, err = _parse_office(path)
                if err:
                    return 0
                return self.count(text)
            except Exception:
                return 0
        mm = _MM_EXT_TO_MODALITY.get(ext)
        if mm is not None:
            return estimate_attachment_tokens(path, mm, self._mm_cfg)
        if ext not in _TEXT_EXT:
            return 0
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return 0
        return self.count(text)
