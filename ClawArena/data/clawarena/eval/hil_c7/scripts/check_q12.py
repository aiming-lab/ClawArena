#!/usr/bin/env python3
"""
check_q12.py -- Verify docs/checklist_audit_report.md

Expected content:
  - Audit of incident_response_checklist.md
  - Specific checklist items referenced by description (e.g., "cross-reference access logs",
    "72 hours", "GDPR", "rotate", "containment")
  - Completion status assessment for checklist items
  - At least one item identified as complete and at least one as incomplete/pending

Usage:
    python check_q12.py <workspace_path>
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

    md_path = workspace / "docs" / "checklist_audit_report.md"
    if not md_path.exists():
        print("FAILED: docs/checklist_audit_report.md not found")
        sys.exit(1)

    try:
        content = md_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read docs/checklist_audit_report.md: {e}")
        sys.exit(1)

    # Must reference incident_response_checklist.md
    if not re.search(r'incident_response_checklist|checklist', content, re.IGNORECASE):
        errors.append(
            "FAILED: must reference incident_response_checklist.md or the checklist"
        )

    # Must reference specific checklist items -- check for at least 2 specific items
    checklist_items = [
        re.compile(r'cross.{0,20}reference|access\s+log', re.IGNORECASE),
        re.compile(r'72.{0,10}hour|GDPR', re.IGNORECASE),
        re.compile(r'rotat|API\s+key.*rotat|key.*rotat', re.IGNORECASE),
        re.compile(r'disable|contain|endpoint.*disabl', re.IGNORECASE),
        re.compile(r'root\s+cause|PR|commit', re.IGNORECASE),
        re.compile(r'notification|notify|customer.*notif', re.IGNORECASE),
    ]
    found_items = [i for i, pattern in enumerate(checklist_items) if pattern.search(content)]
    if len(found_items) < 2:
        errors.append(
            "FAILED: must reference at least 2 specific checklist items by description "
            "(e.g., scope assessment, 72h GDPR window, API key rotation)"
        )

    # Must assess completion status
    if not re.search(
        r'complete|incomplete|done|pending|overdue|check|uncheck|in\s+progress|not\s+started',
        content, re.IGNORECASE
    ):
        errors.append(
            "FAILED: must assess completion status for checklist items "
            "(complete/incomplete/pending/overdue)"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
