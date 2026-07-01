"""check_q4.py — findings/shared_deps_finding.md 存在 + 含 7 个 shared deps + 标记 PII SQL 文件。

通过条件（全部满足，exit 0）：
  1. findings/shared_deps_finding.md 存在
  2. 文件含数字 7（shared deps 总数）
  3. 文件提及 '0042_pii_columns.sql'（break-glass SQL 文件名精确引用）
  4. 文件含 'break-glass' 或等价标记（high-risk / pii / dangerous / critical）
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, has_phrase_any, passed, workspace_root


def main() -> int:
    ws = workspace_root()
    finding = ws / "findings" / "shared_deps_finding.md"
    if not finding.exists():
        fail("missing findings/shared_deps_finding.md")
    text = finding.read_text(encoding="utf-8", errors="ignore")
    low = text.lower()

    # 数字 7
    if not re.search(r"\b7\b", text):
        fail("shared_deps_finding.md does not mention the count 7 (expected 7 shared deps)")

    # 精确文件名
    if "0042_pii_columns.sql" not in text:
        fail("shared_deps_finding.md missing exact reference: '0042_pii_columns.sql'")

    # break-glass 标记（容多种等价词）
    if not has_phrase_any(text, [
        "break-glass", "break glass", "pii", "high.risk", "high risk",
        "dangerous", "critical", "sensitive", "高风险", "敏感",
    ]):
        fail(
            "shared_deps_finding.md does not mark the SQL file as break-glass / high-risk / PII; "
            "expected explicit risk label for 0042_pii_columns.sql"
        )

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
