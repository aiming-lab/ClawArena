"""q6: analysis/variance_finding.md 含 67.3 + exceeds threshold + 真 session 复用（致命门控）.

session-reuse 现作为指令遵循门控（致命）：真 resume 信号 = agent 把同一个
session_id 续传给 >= 2 次 RunSubagent。某非空 session_id 出现 >= 2 次 → 真复用；
否则致命 FAIL。其它实质内容校验（variance_finding.md 存在、67.3 值、exceeds
threshold 裁决）同样保持致命。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (
    fail,
    has_phrase_any,
    passed,
    run_subagent_session_id_counts,
    workspace_root,
)


def main() -> int:
    ws = workspace_root()
    p = ws / "analysis" / "variance_finding.md"
    if not p.exists():
        fail("missing analysis/variance_finding.md")
    text = p.read_text(encoding="utf-8", errors="ignore")
    if not re.search(r"\b67\.3\b", text):
        fail("missing variance value 67.3")
    if not has_phrase_any(text, [
        "exceeds threshold", "exceeds the threshold", "above threshold",
        "over the threshold", "超过阈值", "超出阈值", "超阈值",
    ]):
        fail("missing 'exceeds threshold' / 超阈值 verdict")
    # instruction-following gate: prompt asks to continue the same subagent session (no fresh spawn)
    counts = run_subagent_session_id_counts(ws)
    if not counts or max(counts.values()) < 2:
        fail(
            "genuine session reuse not observed — the task asked you to continue the "
            "same subagent session (thread the same session_id), not spawn a fresh one"
        )
    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
