"""Pluggable tokenizer (tiktoken first, transformers fallback)."""

from __future__ import annotations

from pathlib import Path


class TokenCounter:
    """Counts tokens in strings or text files via a configurable encoder."""

    def __init__(self, name: str = "cl100k_base") -> None:
        self.name = name
        self._encode = self._build_encoder(name)

    @staticmethod
    def _build_encoder(name: str):
        try:
            import tiktoken
            return tiktoken.get_encoding(name).encode
        except Exception:
            pass
        try:
            from transformers import AutoTokenizer
            return AutoTokenizer.from_pretrained(name).encode
        except Exception:
            pass
        raise RuntimeError(
            f"Cannot load tokenizer '{name}'. "
            f"Install tiktoken or transformers."
        )

    def count(self, text: str) -> int:
        if not text:
            return 0
        return len(self._encode(text))

    def count_with_special(self, text: str) -> int:
        """Count tokens allowing ChatML-style special tokens to encode.

        ``tiktoken`` raises by default when it sees sequences like
        ``<|im_start|>``; session-parser output embeds those on purpose
        to approximate the wire payload, so we explicitly allow them.
        Non-tiktoken backends simply fall back to :meth:`count`.
        """
        if not text:
            return 0
        try:
            return len(self._encode(text, allowed_special="all"))
        except TypeError:
            # transformers tokenizers etc. do not accept the kwarg.
            return len(self._encode(text))

    def count_file(self, path: Path) -> int:
        if not path.exists():
            return 0
        try:
            return self.count(path.read_text(encoding="utf-8"))
        except UnicodeDecodeError:
            return 0
