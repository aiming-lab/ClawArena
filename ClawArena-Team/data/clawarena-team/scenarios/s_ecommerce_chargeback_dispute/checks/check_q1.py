"""check_q1.py — wave3 s_ecommerce_chargeback_dispute q1 checker.

Verifies output/dispute_plan.md:
1. File exists
2. ≥ 5 section headings (##)
3. Mentions NorthWind Apparel (or NorthWind)
4. Mentions 1847.50 (or 1,847.50)
5. Mentions 48 (hours SLA)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def main(workspace: Path) -> int:
    out = workspace / "output" / "dispute_plan.md"
    if not out.exists():
        print("FAIL: output/dispute_plan.md not found")
        return 1

    text = out.read_text(encoding="utf-8", errors="ignore")

    # 1. ≥ 5 sections
    sections = re.findall(r"^#{1,3}\s+.+", text, re.MULTILINE)
    if len(sections) < 5:
        print(
            f"FAIL: dispute_plan.md has only {len(sections)} section heading(s) "
            f"(need ≥ 5). Add one section per work area."
        )
        return 1

    # 2. Merchant name
    if not re.search(r"NorthWind", text, re.IGNORECASE):
        print("FAIL: 'NorthWind' (merchant name) not found in dispute_plan.md")
        return 1

    # 3. Amount
    if not re.search(r"1[,.]?847[,.]?50|1847\.50", text):
        print("FAIL: chargeback amount 1847.50 not found in dispute_plan.md")
        return 1

    # 4. 48 hours SLA
    if not re.search(r"\b48\b", text):
        print("FAIL: 48-hour SLA reference not found in dispute_plan.md")
        return 1

    print(
        f"PASS: {len(sections)} sections, NorthWind, amount 1847.50, 48-hour SLA"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
