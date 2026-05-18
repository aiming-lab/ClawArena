#!/usr/bin/env python3
"""
check_it_scope_gap.py — Validate docs/it_scope_gap_analysis.md.

Checks:
  - File exists in docs/
  - Contains "email"
  - Contains "attachment"
  - Contains "scope" or "limitation" or "not included"
  - Contains IT report number "IT-SEC-2026-INV-042" or "INV-042"
  - Has >= 3 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_it_scope_gap.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "docs" / "it_scope_gap_analysis.md"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    content_lower = content.lower()

    if "email" not in content_lower:
        print("FAILED: 'email' not found in it_scope_gap_analysis.md")
        sys.exit(1)

    if "attachment" not in content_lower:
        print("FAILED: 'attachment' not found in it_scope_gap_analysis.md")
        sys.exit(1)

    has_scope = (
        "scope" in content_lower
        or "limitation" in content_lower
        or "not included" in content_lower
    )
    if not has_scope:
        print("FAILED: 'scope', 'limitation', or 'not included' not found in it_scope_gap_analysis.md")
        sys.exit(1)

    has_report_num = (
        "IT-SEC-2026-INV-042" in content
        or "INV-042" in content
    )
    if not has_report_num:
        print("FAILED: IT report number 'IT-SEC-2026-INV-042' or 'INV-042' not found in it_scope_gap_analysis.md")
        sys.exit(1)

    heading_pattern = re.compile(r'^## .+', re.MULTILINE)
    headings = heading_pattern.findall(content)
    if len(headings) < 3:
        print(f"FAILED: expected >= 3 ## headings, found {len(headings)}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
