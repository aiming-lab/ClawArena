#!/usr/bin/env python3
"""
check_q24.py -- Verify docs/stakeholder_action_timeline.md

Expected content:
  - Multiple stakeholders mentioned with specific actions and timestamps
  - Key stakeholders: Alex Rivera, Jake Morrison, Diego Santos, Sana Mehta,
    Jordan Park (at minimum 3 of these)
  - Specific actions with timestamps (Nov 26 key events at minimum)
  - Nov 26 disclosure and endpoint disabling must be referenced

Usage:
    python check_q24.py <workspace_path>
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

    md_path = workspace / "docs" / "stakeholder_action_timeline.md"
    if not md_path.exists():
        print("FAILED: docs/stakeholder_action_timeline.md not found")
        sys.exit(1)

    try:
        content = md_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read docs/stakeholder_action_timeline.md: {e}")
        sys.exit(1)

    # Must mention at least 3 stakeholders
    stakeholders = [
        ("Alex Rivera", re.compile(r'Alex\s+Rivera|Alex\b', re.IGNORECASE)),
        ("Jake Morrison", re.compile(r'Jake\s+Morrison|Jake\b', re.IGNORECASE)),
        ("Diego Santos", re.compile(r'Diego\s+Santos|Diego\b', re.IGNORECASE)),
        ("Sana Mehta", re.compile(r'Sana\s+Mehta|Sana\b', re.IGNORECASE)),
        ("Jordan Park", re.compile(r'Jordan\s+Park|Jordan\b', re.IGNORECASE)),
    ]
    found_stakeholders = [name for name, pattern in stakeholders if pattern.search(content)]
    if len(found_stakeholders) < 3:
        errors.append(
            f"FAILED: must mention at least 3 stakeholders, found: {found_stakeholders}"
        )

    # Must reference Nov 26 (breach disclosure day)
    if not re.search(
        r'Nov\s+26|November\s+26|2024-11-26',
        content, re.IGNORECASE
    ):
        errors.append(
            "FAILED: must reference November 26, 2024 (researcher disclosure date)"
        )

    # Must reference specific actions (not just names)
    action_keywords = re.compile(
        r'disabl|notifi|engag|analys|rotati|disclos|receiv|assess|confirm',
        re.IGNORECASE
    )
    action_matches = action_keywords.findall(content)
    if len(action_matches) < 3:
        errors.append(
            "FAILED: must describe at least 3 specific actions "
            "(disabled, notified, engaged, rotated, etc.)"
        )

    # Must have timestamps or dates
    if not re.search(r'\d{4}-\d{2}-\d{2}|\bNov\b|\bDec\b', content, re.IGNORECASE):
        errors.append(
            "FAILED: must include timestamps or dates for stakeholder actions"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
