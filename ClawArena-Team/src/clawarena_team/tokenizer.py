"""Unified tokenizer and chat-template resolution.

The source field takes three forms:
1. A HuggingFace repo id (contains ``/``): ``Qwen/Qwen3.5-0.8B``
2. A short name: ``qwen3`` etc., mapped by ``SHORT_NAME_MAP`` to a local path under ``helper/``
3. A local path (relative to the yaml file, or absolute)

Template rendering goes through jinja2; token counting goes through the transformers
tokenizer. The two are decoupled.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .config import PROJECT_ROOT

HELPER_ROOT = PROJECT_ROOT / "helper"

SHORT_NAME_MAP_TOKENIZER = {
    "qwen3": HELPER_ROOT / "tokenizer" / "Qwen3.5-0.8B",
}

SHORT_NAME_MAP_TEMPLATE = {
    "qwen3": HELPER_ROOT / "chat_template" / "qwen3.jinja",
}


def resolve_tokenizer_source(source: str, base_dir: Path | None = None) -> str | Path:
    """Return an object that can be passed directly to ``AutoTokenizer.from_pretrained``."""
    if source in SHORT_NAME_MAP_TOKENIZER:
        return SHORT_NAME_MAP_TOKENIZER[source]
    p = Path(source)
    if not p.is_absolute() and base_dir is not None:
        p = (base_dir / p).resolve()
    if p.exists():
        return p
    return source  # treat as an HF repo id


def resolve_template_source(source: str, base_dir: Path | None = None) -> Path:
    if source in SHORT_NAME_MAP_TEMPLATE:
        return SHORT_NAME_MAP_TEMPLATE[source]
    p = Path(source)
    if not p.is_absolute() and base_dir is not None:
        p = (base_dir / p).resolve()
    return p


class UnifiedTokenizer:
    """Exposes the two core methods ``count(text)`` and ``render(messages)``."""

    def __init__(self, tokenizer_source: str, template_source: str, base_dir: Path | None = None):
        self._tok = None
        self._tok_source = resolve_tokenizer_source(tokenizer_source, base_dir)
        self._template_path = resolve_template_source(template_source, base_dir)
        self._template_str: str | None = None

    # lazy-init to reduce import cost
    def _ensure_tokenizer(self):
        if self._tok is None:
            from transformers import AutoTokenizer  # type: ignore

            self._tok = AutoTokenizer.from_pretrained(self._tok_source, trust_remote_code=False)
        return self._tok

    def _ensure_template(self) -> str:
        if self._template_str is None:
            if not self._template_path.exists():
                # Fallback: a minimal template
                self._template_str = (
                    "{% for m in messages %}<|im_start|>{{ m.role }}\n{{ m.content }}<|im_end|>\n{% endfor %}"
                )
            else:
                self._template_str = self._template_path.read_text(encoding="utf-8")
        return self._template_str

    def render(self, messages: list[dict[str, Any]]) -> str:
        from jinja2 import Template

        tpl = Template(self._ensure_template())
        return tpl.render(messages=messages)

    def count(self, text: str) -> int:
        tok = self._ensure_tokenizer()
        return len(tok.encode(text, add_special_tokens=False))

    def count_messages(self, messages: list[dict[str, Any]]) -> int:
        return self.count(self.render(messages))
