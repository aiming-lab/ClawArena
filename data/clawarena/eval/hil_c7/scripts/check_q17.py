#!/usr/bin/env python3
"""
check_q17.py -- Verify docs/notification_comparison.md

Expected content:
  - Comparison between notification_draft_v1.md and required final notification
  - Must reference both documents by name
  - Must identify specific differences:
    * Draft v1 omits timeline (Nov 5-26) -- final must include it
    * Draft v1 omits scope (2340 records) -- final must include it
    * Draft v1 uses "security configuration issue" framing -- misleading
    * Draft v1 omits the external researcher disclosure
    * Draft v1 "precautionary" framing vs actual remedial rotation
  - Must cite at least 2 specific differences

Usage:
    python check_q17.py <workspace_path>
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

    md_path = workspace / "docs" / "notification_comparison.md"
    if not md_path.exists():
        print("FAILED: docs/notification_comparison.md not found")
        sys.exit(1)

    try:
        content = md_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read docs/notification_comparison.md: {e}")
        sys.exit(1)

    # Must reference notification_draft_v1.md (or "draft v1" or "v1")
    if not re.search(r'notification_draft_v1|draft\s*v1|v1\s*draft', content, re.IGNORECASE):
        errors.append(
            "FAILED: must reference notification_draft_v1.md or 'draft v1'"
        )

    # Must identify timeline omission
    if not re.search(
        r'Nov\s+5|November\s+5|Nov.*26|exposure\s+window|timeline|date',
        content, re.IGNORECASE
    ):
        errors.append(
            "FAILED: must identify that draft v1 omits the exposure timeline "
            "(Nov 5 - Nov 26)"
        )

    # Must identify scope omission OR framing issue
    if not re.search(
        r'scope|2,?340|record|number\s+of|missing|omit|left\s+out|'
        r'security\s+configuration|precautionary|minimal\s+disclosure|'
        r'GDPR|compliance',
        content, re.IGNORECASE
    ):
        errors.append(
            "FAILED: must identify what is missing in draft v1 "
            "(scope, timeline, GDPR compliance, or framing issues)"
        )

    # Must identify at least 2 specific differences (check count of difference markers)
    diff_markers = re.findall(
        r'(?:missing|omit|not\s+includ|left\s+out|differ|inadequat|insufficient|'
        r'precautionary|minimal|timeline|scope|GDPR|researcher|external)',
        content, re.IGNORECASE
    )
    if len(diff_markers) < 2:
        errors.append(
            "FAILED: must identify at least 2 specific differences between "
            "draft v1 and required notification content"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
