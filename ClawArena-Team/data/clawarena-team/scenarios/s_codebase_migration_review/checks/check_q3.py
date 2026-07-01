"""check_q3.py — notes/svc_summary_ledger_reports.md 存在 + session 复用 >= 2 + 含 ledger/reports。

通过条件（全部满足，exit 0）：
  1. notes/svc_summary_ledger_reports.md 存在
  2. 文件含 'ledger' 和 'reports' 关键词
  3. 致命：题面要求在同一 subagent session 内续接（不要重新开），故须观测到
     某个非空 session_id 在 RunSubagent 调用里出现 >= 2 次（真 resume 信号）。
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, run_subagent_session_id_counts, workspace_root


def main() -> int:
    ws = workspace_root()
    summary = ws / "notes" / "svc_summary_ledger_reports.md"
    if not summary.exists():
        fail("missing notes/svc_summary_ledger_reports.md")
    text = summary.read_text(encoding="utf-8", errors="ignore").lower()

    for svc in ("ledger", "reports"):
        if svc not in text:
            fail(f"svc_summary_ledger_reports.md missing service reference: {svc!r}")

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
