"""check_q1.py — wave3 s_hospital_safety_event_review q1 checker.

Verifies output/rca_plan.md:
  - File exists
  - ≥ 5 section headings
  - Mentions Mercator Vitals M-7
  - Mentions ICU or MICU
  - Mentions 23:48
  - Mentions MedWatch
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def main(workspace: Path) -> int:
    out = workspace / "output" / "rca_plan.md"
    if not out.exists():
        print("FAIL: output/rca_plan.md not found")
        return 1

    text = out.read_text(encoding="utf-8", errors="ignore")

    # 1. ≥ 5 section headings (accept #, **, numbered N. or N))
    headings = re.findall(
        r"(?m)^(?:#{1,4}\s+.+|(?:\*{1,2}|\d+[\.\)])\s+\S.{3,})",
        text,
    )
    if len(headings) < 5:
        print(f"FAIL: found {len(headings)} section headings, need ≥ 5")
        return 1

    # 2. Mentions Mercator Vitals M-7
    if not re.search(r"Mercator\s+Vitals\s+M-?7", text, re.IGNORECASE):
        print("FAIL: 'Mercator Vitals M-7' not mentioned in rca_plan.md")
        return 1

    # 3. Mentions ICU or MICU
    if not re.search(r"\b(?:ICU|MICU)\b", text, re.IGNORECASE):
        print("FAIL: ICU or MICU not mentioned in rca_plan.md")
        return 1

    # 4. Mentions 23:48
    if not re.search(r"23:48", text):
        print("FAIL: event time 23:48 not mentioned in rca_plan.md")
        return 1

    # 5. Mentions MedWatch
    if not re.search(r"MedWatch", text, re.IGNORECASE):
        print("FAIL: FDA MedWatch not mentioned in rca_plan.md")
        return 1

    print(
        f"PASS: rca_plan.md has {len(headings)} headings, "
        "Mercator Vitals M-7, ICU/MICU, 23:48, MedWatch"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
