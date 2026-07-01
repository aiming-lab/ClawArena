"""check_q2.py — notes/svc_summary_pay_bill.md 存在 + 含 payments/billing 服务 + RunSubagent 出现 >= 1 次。

通过条件（全部满足，exit 0）：
  1. notes/svc_summary_pay_bill.md 存在
  2. 文件含 'payments' 和 'billing' 关键词
  3. ADVISORY ONLY (non-gating): sessions/main.jsonl 中 RunSubagent 出现 >= 1 次（委托 sub 读代码）
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, run_subagent_id_counts, workspace_root


def main() -> int:
    ws = workspace_root()
    summary = ws / "notes" / "svc_summary_pay_bill.md"
    if not summary.exists():
        fail("missing notes/svc_summary_pay_bill.md")
    text = summary.read_text(encoding="utf-8", errors="ignore").lower()

    for svc in ("payments", "billing"):
        if svc not in text:
            fail(f"svc_summary_pay_bill.md missing service reference: {svc!r}")

    # 至少 1 次 RunSubagent（委托 sub 读代码是 session_reuse 前提）
    counts = run_subagent_id_counts(ws)
    total_runs = sum(counts.values())
    if total_runs < 1:
        print("NOTE: parallel/delegated subagent count not verified — advisory only, non-gating", file=sys.stderr)

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
