"""check_q1.py — Wave3 s_partnership_term_sheet q1 checker.

Verifies output/audit_plan.md:
- File exists
- ≥ 5 section headings
- Contains JV TS-2026-009
- Names Mercator Robotics
- Names Helios Energy
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def main(workspace: Path) -> int:
    out = workspace / "output" / "audit_plan.md"
    if not out.exists():
        print("FAIL: output/audit_plan.md not found")
        return 1

    text = out.read_text(encoding="utf-8", errors="ignore")

    # 1. ≥ 5 section headings (accept #, **, numbered N., or 中文序号)
    headings = re.findall(
        r"(?m)^(?:#{1,4}\s+.+|(?:\*{1,2}|\d+[\.\)])\s+\S.{3,})",
        text,
    )
    if len(headings) < 5:
        print(f"FAIL: found {len(headings)} section headings, need ≥ 5")
        return 1

    # 2. JV TS-2026-009
    if not re.search(r"TS-2026-009", text):
        print("FAIL: JV reference TS-2026-009 not mentioned")
        return 1

    # 3. Mercator Robotics
    if not re.search(r"Mercator\s+Robotics|Mercator", text, re.IGNORECASE):
        print("FAIL: Mercator Robotics not mentioned")
        return 1

    # 4. Helios Energy
    if not re.search(r"Helios\s+Energy|Helios", text, re.IGNORECASE):
        print("FAIL: Helios Energy not mentioned")
        return 1

    print(
        f"PASS: audit_plan.md has {len(headings)} headings, "
        f"TS-2026-009, Mercator Robotics, Helios Energy"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
