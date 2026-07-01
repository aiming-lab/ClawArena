#!/usr/bin/env python3
"""
check_closure_memo.py — Validates docs/YYYY-MM-DD_case_closure_memo.md.

Checks:
  1. ≥1 date-prefixed .md file in docs/
  2. 4 allegations/contradictions addressed
  3. "corrigendum" present
  4. "lesson" or "future" improvement present
  5. ≥5 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_closure_memo.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    docs_dir = workspace / "docs"

    if not docs_dir.exists():
        print("FAILED: docs/ directory does not exist")
        sys.exit(1)

    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    candidates = [f for f in docs_dir.glob("*.md") if date_prefix.match(f.name)]

    if not candidates:
        print("FAILED: no date-prefixed .md file found in docs/")
        sys.exit(1)

    target = sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)[0]
    content = target.read_text(encoding="utf-8")
    failures = []

    # 4 allegations / contradictions addressed
    # Count C1-C4 or Allegation 1-4 or the 4 complaint themes
    c_count = len(set(re.findall(r'C[1-4]\b', content)))
    allegation_count = len(set(re.findall(r'Allegation\s+[1-4]', content, re.IGNORECASE)))
    # Also count key allegation themes
    theme_count = sum(1 for pat in (
        r'selective\s+exclusion',
        r'duplicate\s+publication',
        r'data\s+manipulat',
        r'tiebreaker|ID.only',
    ) if re.search(pat, content, re.IGNORECASE))

    if max(c_count, allegation_count, theme_count) < 4:
        # Accept if at least 4 of the specific allegation types are covered
        specific = sum(1 for pat in (
            r'HIS\s+migration',
            r'selective\s+exclusion',
            r'duplicate',
            r'tiebreaker',
            r'Wang\s+Yisheng',
            r'2022.2023',
        ) if re.search(pat, content, re.IGNORECASE))
        if specific < 4:
            failures.append(
                "FAILED: fewer than 4 allegations/contradictions addressed "
                "(expected C1–C4 or 4 complaint themes covered)"
            )

    # Corrigendum
    if not re.search(r'\bcorrigendum\b', content, re.IGNORECASE):
        failures.append("FAILED: 'corrigendum' not mentioned")

    # Lessons learned / future improvement
    if not re.search(r'\b(lesson|future|prevent|improve|recommendation)\b',
                     content, re.IGNORECASE):
        failures.append(
            "FAILED: 'lesson', 'future', or improvement recommendation not found"
        )

    # Minimum heading count
    headings = re.findall(r'^##\s+', content, re.MULTILINE)
    if len(headings) < 5:
        failures.append(
            f"FAILED: only {len(headings)} ## headings found (expected ≥5)"
        )

    if failures:
        for f in failures:
            print(f)
        sys.exit(1)

    print(f"PASSED (checked {target.name})")
    sys.exit(0)


if __name__ == "__main__":
    main()
