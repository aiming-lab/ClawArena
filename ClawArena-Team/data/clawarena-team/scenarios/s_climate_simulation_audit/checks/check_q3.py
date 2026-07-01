"""q3: analysis/quarterly_summary.md 存在 + 4 季度全引用（致命）+ session 复用（advisory）。

通过条件（exit 0）：
  1. analysis/quarterly_summary.md 存在，长度 >= 200 字符（致命）
  2. 4 个季度文件均被引用（q1/q2/q3/q4 或 w12_q* 等标识）（致命）

Session reuse（真 resume 信号）—— 致命门控：
  题面要求在同一 subagent session 内追加读取（建议复用同一 session 以省 context），
  故须观测到某个非空 session_id 在 RunSubagent 调用里出现 >= 2 次。只传 subagent_id
  而不传 session_id 会让 harness 每次新建会话，不算真复用，故只认 session_id 信号。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, has_phrase_any, passed, run_subagent_session_id_counts, workspace_root


_QUARTER_PATTERNS = [
    r"\bq1\b",
    r"\bq2\b",
    r"\bq3\b",
    r"\bq4\b",
]
_QUARTER_LABELS = [
    ["q1", "quarter 1", "w12_q1", "2027q1", "2027 q1"],
    ["q2", "quarter 2", "w12_q2", "2027q2", "2027 q2"],
    ["q3", "quarter 3", "w12_q3", "2027q3", "2027 q3"],
    ["q4", "quarter 4", "w12_q4", "2027q4", "2027 q4"],
]


def main() -> int:
    ws = workspace_root()
    summary = ws / "analysis" / "quarterly_summary.md"
    if not summary.exists():
        fail("missing analysis/quarterly_summary.md")

    text = summary.read_text(encoding="utf-8", errors="ignore")
    if len(text.strip()) < 200:
        fail(f"quarterly_summary.md too short: {len(text.strip())} chars < 200")

    low = text.lower()
    for i, labels in enumerate(_QUARTER_LABELS, 1):
        if not any(lbl in low for lbl in labels):
            fail(f"Q{i} not referenced in quarterly_summary.md (tried: {labels[:3]})")

    # instruction-following gate: prompt asks to continue the same subagent session (no fresh spawn)
    sess_counts = run_subagent_session_id_counts(ws)
    if not sess_counts or max(sess_counts.values()) < 2:
        fail(
            "genuine session reuse not observed — the task asked you to continue the same "
            "subagent session (thread the same session_id), not spawn a fresh one each round"
        )

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
