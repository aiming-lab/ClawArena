"""check_q1.py — triage plan: 5 sections + patient ID + chief complaint.

Pass conditions (all required):
  1. output/triage_plan.md exists
  2. >= 5 markdown section headings (## or #)
  3. Patient ID P-2026-0884 appears in the file
  4. Chief complaint keyword: 'cough' OR '咳嗽' (case-insensitive)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root

PATIENT_ID = "P-2026-0884"


def main() -> int:
    ws = workspace_root()
    target = ws / "output" / "triage_plan.md"
    if not target.exists():
        fail("missing output/triage_plan.md")
    text = target.read_text(encoding="utf-8", errors="ignore")
    if len(text.strip()) < 80:
        fail("triage_plan.md is too short (< 80 chars)")

    # 5 sections
    sections = re.findall(r"^#{1,3}\s+\S", text, flags=re.MULTILINE)
    if len(sections) < 5:
        fail(f"need >= 5 section headings, found {len(sections)}")

    # Patient ID
    if PATIENT_ID not in text:
        fail(f"patient ID {PATIENT_ID!r} not found in triage_plan.md")

    # Chief complaint
    if not re.search(r"cough|咳嗽", text, flags=re.IGNORECASE):
        fail("chief complaint keyword ('cough' / '咳嗽') not found")

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
