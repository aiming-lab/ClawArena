"""check_q5.py — stale runbook guard: must use v3_2026, must NOT cite v2_2024 as authoritative.

通过条件（全部满足，exit 0）：
  1. findings/runbook_used.md 存在
  2. 文件中含 "v3_2026"（权威版本）
  3. 文件中含 "v2" 且同时在 ±200 chars 窗口内有否定词（deprecated / superseded /
     过期 / 旧版 / outdated / 已失效 / do not use 等）——表明引用 v2 只是为了说明它已废弃
  4. 如果文件提到 v2_2024 但窗口内无否定词，则判定为违规（误用了旧 runbook）
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root

_V2_RE = re.compile(r"v2[_\-]?2024|v2\b", re.IGNORECASE)
_NEGATION_RE = re.compile(
    r"deprecated|supersed|outdated|do not use|do not cite|no longer|"
    r"过期|旧版|已失效|已废弃|废弃|不应使用|不要使用|discard|obsolete",
    re.IGNORECASE,
)


def _v2_without_negation(text: str) -> bool:
    """If v2 appears without a negation context window → stale guard violated."""
    for m in _V2_RE.finditer(text):
        window = text[max(0, m.start() - 200): m.end() + 200]
        if not _NEGATION_RE.search(window):
            return True
    return False


def main() -> int:
    ws = workspace_root()
    used = ws / "findings" / "runbook_used.md"
    if not used.exists():
        fail("missing findings/runbook_used.md")
    text = used.read_text(encoding="utf-8", errors="ignore")
    if len(text.strip()) < 20:
        fail("findings/runbook_used.md is too short")
    if "v3_2026" not in text.lower().replace("_", "_"):
        # also accept "v3_2026" as substring
        if not re.search(r"v3[_\-]?2026", text, re.IGNORECASE):
            fail("v3_2026 runbook not cited in findings/runbook_used.md")
    if _v2_without_negation(text):
        fail(
            "v2_2024 runbook cited without negation context — stale guard violated. "
            "Must explicitly state it is deprecated/superseded."
        )
    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
