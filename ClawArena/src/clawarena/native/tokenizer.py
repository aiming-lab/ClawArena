"""统一 tokenizer 与 chat template 解析。

source 字段三种形式：
1. HuggingFace repo id（包含 ``/``）：``Qwen/Qwen3.5-0.8B``
2. 短名：``qwen3`` 等，由 ``SHORT_NAME_MAP`` 映射到 ``helper/`` 下本地路径
3. 本地路径（相对 yaml 文件或绝对路径）

模板渲染走 jinja2；token 计数走 transformers tokenizer。两者解耦。

ArcBench 跨 provider 的 token 计数走该统一 tokenizer——provider 返回的 raw_usage
仅落 jsonl 作统计来源，**不**用于 harness 内部决策（与 SMbench 同口径）。
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
    """返回可直接传给 ``AutoTokenizer.from_pretrained`` 的对象。"""
    if source in SHORT_NAME_MAP_TOKENIZER:
        return SHORT_NAME_MAP_TOKENIZER[source]
    p = Path(source)
    if not p.is_absolute() and base_dir is not None:
        p = (base_dir / p).resolve()
    if p.exists():
        return p
    return source


def resolve_template_source(source: str, base_dir: Path | None = None) -> Path:
    if source in SHORT_NAME_MAP_TEMPLATE:
        return SHORT_NAME_MAP_TEMPLATE[source]
    p = Path(source)
    if not p.is_absolute() and base_dir is not None:
        p = (base_dir / p).resolve()
    return p


class UnifiedTokenizer:
    """对外暴露 ``count(text)`` / ``count_messages(messages)`` / ``render(messages)``。"""

    def __init__(
        self,
        tokenizer_source: str,
        template_source: str,
        base_dir: Path | None = None,
    ):
        self._tok = None
        self._tok_failed = False
        self._tiktoken = None
        self._tok_source = resolve_tokenizer_source(tokenizer_source, base_dir)
        self._template_path = resolve_template_source(template_source, base_dir)
        self._template_str: str | None = None

    def _ensure_tokenizer(self):
        if self._tok is None and not self._tok_failed:
            try:
                from transformers import AutoTokenizer  # type: ignore

                self._tok = AutoTokenizer.from_pretrained(self._tok_source, trust_remote_code=False)
            except Exception:
                # HF tokenizer 不可用（如 qwen3 未 vendor 到 helper/、或 source 是本地
                # vllm 模型名非 HF repo id）。降级 tiktoken cl100k 近似计数——token 数仅
                # 用于 compaction 触发/体量估算，近似口径足够，避免 from_pretrained 崩。
                self._tok_failed = True
        return self._tok

    def _ensure_tiktoken(self):
        if self._tiktoken is None:
            import tiktoken

            self._tiktoken = tiktoken.get_encoding("cl100k_base")
        return self._tiktoken

    def _ensure_template(self) -> str:
        if self._template_str is None:
            if not self._template_path.exists():
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
        if tok is not None:
            return len(tok.encode(text, add_special_tokens=False))
        return len(self._ensure_tiktoken().encode(text))

    def count_messages(self, messages: list[dict[str, Any]]) -> int:
        return self.count(self.render(messages))
