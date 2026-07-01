"""check_q1.py — review_plan.md 含 6 个 section + 引用 4 个服务名 + project 名。

通过条件（全部满足，exit 0）：
  1. output/review_plan.md 存在
  2. 含 >= 6 个 '## ' 二级标题
  3. 覆盖 6 个审查领域：architecture / shared_deps / risk_sql / coverage / rpc_compat / rollout
  4. 提及 4 个服务（payments / billing / ledger / reports）
  5. 提及 project 名 payments-split
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root


def main() -> int:
    ws = workspace_root()
    plan = ws / "output" / "review_plan.md"
    if not plan.exists():
        fail("missing output/review_plan.md")
    text = plan.read_text(encoding="utf-8", errors="ignore")
    low = text.lower()

    # 结构层：6 个 ## section
    sections = re.findall(r"^##\s+\S.*$", text, flags=re.MULTILINE)
    if len(sections) < 6:
        fail(f"need >= 6 '## ' sections, got {len(sections)}: {sections}")

    # 字段层：6 个审查领域（关键词匹配，容下划线/斜杠/空格变体）
    required_domains = [
        (r"architect", "architecture"),
        (r"shared.dep", "shared_deps"),
        (r"risk.sql|pii.sql|sql.risk|0042|migration.*sql", "risk_sql"),
        (r"coverage", "coverage"),
        (r"rpc.compat|rpc.diff|schema.diff|proto.*diff|cross.service", "rpc_compat"),
        (r"rollout|staged|block.merge|decision", "rollout"),
    ]
    for pattern, label in required_domains:
        if not re.search(pattern, low):
            fail(f"review_plan.md missing domain: {label!r} (pattern: {pattern!r})")

    # 真值层：4 个服务名
    for svc in ("payments", "billing", "ledger", "reports"):
        if svc not in low:
            fail(f"review_plan.md missing service reference: {svc!r}")

    # 真值层：project 名
    if "payments-split" not in low:
        fail("review_plan.md missing project reference: 'payments-split'")

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
