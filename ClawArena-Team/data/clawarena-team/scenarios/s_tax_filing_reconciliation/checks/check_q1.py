#!/usr/bin/env python3
"""check_q1.py — wave3 s_tax_filing_reconciliation q1 checker.

Verifies output/filing_plan.md:
1. File exists and has ≥ 300 chars.
2. ≥ 5 level-2 Markdown headings (## ...).
3. Contains "Liu Wei" (client name).
4. Contains dual-citizenship reference ("dual citi" / "dual-citi" / "双国籍" / "US.*DE" / "DE.*US").
5. Contains "2026".
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def main(workspace: Path) -> int:
    out = workspace / "output" / "filing_plan.md"
    if not out.exists():
        print("FAIL: output/filing_plan.md not found")
        return 1

    text = out.read_text(encoding="utf-8", errors="ignore")

    if len(text.strip()) < 300:
        print(f"FAIL: filing_plan.md too short ({len(text)} chars)")
        return 1

    # ≥ 5 section headings
    headings = re.findall(r"^#{1,3}\s+.+", text, re.MULTILINE)
    if len(headings) < 5:
        print(f"FAIL: found only {len(headings)} headings, need ≥ 5")
        return 1

    # Client name
    if not re.search(r"Liu\s+Wei", text, re.IGNORECASE):
        print("FAIL: 'Liu Wei' not found in filing_plan.md")
        return 1

    # Dual citizenship
    dual_pattern = re.compile(
        r"dual.citi|dual.national|双国籍|US.*DE|DE.*US|"
        r"United States.*German|German.*United States|"
        r"cross.border|cross-border",
        re.IGNORECASE
    )
    if not dual_pattern.search(text):
        print("FAIL: dual-citizenship / cross-border reference not found in filing_plan.md")
        return 1

    # Year 2026
    if not re.search(r"2026", text):
        print("FAIL: '2026' not found in filing_plan.md")
        return 1

    print("PASS: filing_plan.md has ≥ 5 headings, Liu Wei, dual-citizenship, 2026")
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
