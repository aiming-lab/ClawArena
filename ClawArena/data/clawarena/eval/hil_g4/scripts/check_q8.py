#!/usr/bin/env python3
"""
check_q8.py — Verify docs/1on1_discrepancy_analysis.md for hil_g4.

After upd1 (sunwei-1on1-notes.md) is injected, the agent must create
docs/1on1_discrepancy_analysis.md comparing the HR calendar records vs
Sun Wei's personal 1-on-1 notes, identifying specific discrepancies.

Requirements:
  1. File exists at docs/1on1_discrepancy_analysis.md (or similar name in docs/).
  2. Must reference both source files: calendar-1on1-history.md and sunwei-1on1-notes.md.
  3. Must mention specific meeting dates where records differ:
     - 2025-11-20: HR calendar says "Performance Discussion"; Sun Wei notes say "discussed" (not a warning)
     - 2025-12-18: HR calendar says "Performance Discussion"; Sun Wei notes say "follow up" (not a warning)
     - 2026-03-04: HR calendar says "PIP Review"; Sun Wei notes say "talked about termination"
  4. Must have >= 3 ## headings.
  5. Must identify the key discrepancy: 1-on-1 discussions labeled "Performance Discussion"
     are characterized differently by Sun Wei (informal discussion vs formal warning).

Ground truth:
  - Meetings in HR calendar: 2025-11-20 (Perf Discussion), 2025-12-18 (Perf Discussion),
    2026-01-08 (Regular), 2026-01-22 (Regular), 2026-02-05 (Regular),
    2026-02-15 (PIP Review), 2026-02-19 (Regular), 2026-03-04 (PIP Review), 2026-03-13 (Meeting)
  - Sun Wei notes cover: 2025-11-20, 2025-12-18, 2026-01-08, 2026-02-15, 2026-03-04
  - Key discrepancy: 2026-03-04 labeled "PIP Review" in calendar but Sun Wei notes
    describe it as a termination conversation

Usage:
    python check_q8.py <workspace_path>
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    docs_dir = workspace / "docs"
    errors = []

    if not docs_dir.exists():
        print("FAILED: docs/ directory not found")
        sys.exit(1)

    # Find the discrepancy analysis file (flexible name)
    candidates = list(docs_dir.glob("*1on1*discrepancy*.md")) + \
                 list(docs_dir.glob("*discrepancy*1on1*.md")) + \
                 list(docs_dir.glob("*1on1*analysis*.md")) + \
                 list(docs_dir.glob("*1on1*diff*.md")) + \
                 list(docs_dir.glob("*会议*差异*.md")) + \
                 list(docs_dir.glob("*差异*分析*.md"))

    if not candidates:
        # Fall back to any file containing both "1on1" concepts
        candidates = [f for f in docs_dir.glob("*.md")
                      if any(kw in f.name.lower() for kw in
                             ["1on1", "1:1", "discrepancy", "差异", "比较", "compare"])]

    if not candidates:
        print("FAILED: no 1-on-1 discrepancy analysis file found in docs/")
        sys.exit(1)

    # Use most recent
    target = sorted(candidates, key=lambda f: f.stat().st_mtime, reverse=True)[0]

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {target}: {e}")
        sys.exit(1)

    # Check for reference to both source files
    has_calendar = bool(re.search(
        r'calendar.1on1|calendar_1on1|日历|Calendar',
        content, re.IGNORECASE
    ))
    has_sunwei_notes = bool(re.search(
        r'sunwei.1on1|sunwei_1on1|孙伟.*笔记|孙伟.*记录|Sun Wei.*note|1on1.*note',
        content, re.IGNORECASE
    ))
    if not has_calendar:
        errors.append(
            "FAILED: file does not reference calendar-1on1-history.md source "
            "(expected: calendar-1on1, 日历, Calendar)"
        )
    if not has_sunwei_notes:
        errors.append(
            "FAILED: file does not reference sunwei-1on1-notes.md source "
            "(expected: sunwei-1on1, 孙伟笔记, Sun Wei note)"
        )

    # Check for specific conflict dates
    has_nov20 = "2025-11-20" in content or "11月20" in content or "November 20" in content
    has_dec18 = "2025-12-18" in content or "12月18" in content or "December 18" in content
    has_mar04 = "2026-03-04" in content or "3月4" in content or "March 4" in content

    if not has_nov20:
        errors.append("FAILED: file does not mention 2025-11-20 meeting date")
    if not has_dec18:
        errors.append("FAILED: file does not mention 2025-12-18 meeting date")
    if not (has_nov20 or has_dec18 or has_mar04):
        errors.append(
            "FAILED: file does not mention any of the specific conflict dates "
            "(2025-11-20, 2025-12-18, 2026-03-04)"
        )

    # Check for >= 3 ## headings
    headings = [ln for ln in content.splitlines() if re.match(r'^##+ ', ln.strip())]
    if len(headings) < 3:
        errors.append(
            f"FAILED: file has only {len(headings)} ## headings (expected >= 3)"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
