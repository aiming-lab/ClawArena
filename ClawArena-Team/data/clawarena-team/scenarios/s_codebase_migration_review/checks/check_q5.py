"""check_q5.py — findings/regression_finding.md 含真实 pytest 失败的测试名 + 行号 78。

通过条件（全部满足，exit 0）：
  1. findings/regression_finding.md 存在
  2. 文件含 'test_payment_idempotency_after_split'（精确测试名）
  3. 文件含行号 78（严格，±0）
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root


def main() -> int:
    ws = workspace_root()
    finding = ws / "findings" / "regression_finding.md"
    if not finding.exists():
        fail("missing findings/regression_finding.md")
    text = finding.read_text(encoding="utf-8", errors="ignore")

    # 精确测试名
    if "test_payment_idempotency_after_split" not in text:
        fail("missing failing test name 'test_payment_idempotency_after_split'")

    # 行号 78（严格匹配，容 'line 78' / ':78' / 'line=78' 等形态）
    if not re.search(r"\bline\s*78\b|:78\b|line\s*=\s*78\b", text, flags=re.IGNORECASE):
        fail("missing assertion line number 78 (need 'line 78' or ':78' or equivalent)")

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
