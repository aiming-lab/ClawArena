#!/usr/bin/env python3
"""
check_q14.py -- Verify docs/board_communication_analysis.md.

Usage:
    python check_q14.py <workspace_path>
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    md_path = workspace / "docs" / "board_communication_analysis.md"
    if not md_path.exists():
        errors.append(f"FAILED: {md_path} not found")
    else:
        try:
            content = md_path.read_text(encoding="utf-8")
        except Exception as e:
            errors.append(f"FAILED: cannot read {md_path}: {e}")
            content = ""

        if content:
            # Must reference David or Ochieng
            if not re.search(r"David|Ochieng", content, re.IGNORECASE):
                errors.append("FAILED: 'David' or 'Ochieng' not mentioned")

            # Must state 14-day deadline
            if not re.search(r"\b14\b.{0,20}(day|calendar)|14.calendar.day", content, re.IGNORECASE):
                errors.append(
                    "FAILED: 14-day waiver deadline not cited"
                )

            # Must mention waiver
            if not re.search(r"waiver", content, re.IGNORECASE):
                errors.append("FAILED: 'waiver' not mentioned")

            # Must distinguish personal note from formal Committee position
            if not re.search(
                r"personal.{0,30}(note|view|support|opinion)|"
                r"Committee.{0,30}(formal|position|require)|"
                r"formal.{0,30}position|institutional.{0,30}constraint",
                content,
                re.IGNORECASE,
            ):
                errors.append(
                    "FAILED: distinction between David's personal view and the "
                    "Committee's formal position not made"
                )

            # Must have >= 3 ## headings
            headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
            if len(headings) < 3:
                errors.append(
                    f"FAILED: file has only {len(headings)} ## headings (need >= 3)"
                )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
