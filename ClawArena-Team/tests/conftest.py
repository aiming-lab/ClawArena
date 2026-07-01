"""共享 fixture 与简易 stub。"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


class StubTokenizer:
    """无需 transformers 即可使用的 tokenizer 替身，按 4 字符一个 token 估算。"""

    def count(self, text: str) -> int:
        return max(1, len(text) // 4)

    def count_messages(self, messages: list[dict[str, Any]]) -> int:
        total = 0
        for m in messages:
            total += self.count(m.get("content", ""))
        return total

    def render(self, messages: list[dict[str, Any]]) -> str:
        return "\n".join(f"{m['role']}:{m.get('content', '')}" for m in messages)


@pytest.fixture
def stub_tokenizer() -> StubTokenizer:
    return StubTokenizer()


@pytest.fixture
def tmp_workspace(tmp_path: Path) -> Path:
    ws = tmp_path / "workspace"
    ws.mkdir()
    (ws / "inbox").mkdir()
    (ws / "notes").mkdir()
    (ws / "restricted").mkdir()
    (ws / "inbox" / "hello.txt").write_text("hello world", encoding="utf-8")
    (ws / "restricted" / "secret.txt").write_text("top secret", encoding="utf-8")
    return ws
