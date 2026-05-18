#!/usr/bin/env python3
"""
check_sender_recipient.py — Validate analysis/sender_recipient_analysis.md.

Checks:
  - File exists
  - Contains "headhunter-corp.com" or "headhunter"
  - Contains exact timestamp "15:03:44" or "15:03"
  - Contains "external"
  - Has >= 2 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_sender_recipient.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "sender_recipient_analysis.md"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    content_lower = content.lower()

    if "headhunter-corp.com" not in content_lower and "headhunter" not in content_lower:
        print("FAILED: external recipient domain 'headhunter-corp.com' or 'headhunter' not found in sender_recipient_analysis.md")
        sys.exit(1)

    if "15:03:44" not in content and "15:03" not in content:
        print("FAILED: email send timestamp '15:03:44' or '15:03' not found in sender_recipient_analysis.md")
        sys.exit(1)

    if "external" not in content_lower:
        print("FAILED: 'external' not found in sender_recipient_analysis.md")
        sys.exit(1)

    heading_pattern = re.compile(r'^## .+', re.MULTILINE)
    headings = heading_pattern.findall(content)
    if len(headings) < 2:
        print(f"FAILED: expected >= 2 ## headings, found {len(headings)}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
