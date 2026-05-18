#!/usr/bin/env python3
"""
check_denial_timeline.py — Validate analysis/denial_refutation_timeline.md.

Checks:
  - File exists
  - 3 denials documented (Denial 1/First, Denial 2/Second, Denial 3/Third)
  - Third denial mentions hash
  - Has >= 4 ## headings OR table with >= 3 rows
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_denial_timeline.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "denial_refutation_timeline.md"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    content_lower = content.lower()

    # Check for three denials/statements
    has_denial1 = (
        "denial 1" in content_lower
        or "statement 1" in content_lower
        or "first denial" in content_lower
        or "first statement" in content_lower
        or "denial #1" in content_lower
    )
    has_denial2 = (
        "denial 2" in content_lower
        or "statement 2" in content_lower
        or "second denial" in content_lower
        or "second statement" in content_lower
        or "denial #2" in content_lower
    )
    has_denial3 = (
        "denial 3" in content_lower
        or "statement 3" in content_lower
        or "third denial" in content_lower
        or "third statement" in content_lower
        or "denial #3" in content_lower
    )

    if not has_denial1:
        print("FAILED: Denial 1 / Statement 1 / First denial not found in denial_refutation_timeline.md")
        sys.exit(1)

    if not has_denial2:
        print("FAILED: Denial 2 / Statement 2 / Second denial not found in denial_refutation_timeline.md")
        sys.exit(1)

    if not has_denial3:
        print("FAILED: Denial 3 / Statement 3 / Third denial not found in denial_refutation_timeline.md")
        sys.exit(1)

    # Check that third denial section mentions hash
    # Find the region around "denial 3" or "third"
    third_denial_patterns = [
        r'denial\s+3.{0,500}',
        r'statement\s+3.{0,500}',
        r'third.{0,500}',
        r'denial\s+#3.{0,500}',
    ]
    third_section = ""
    for pattern in third_denial_patterns:
        m = re.search(pattern, content_lower)
        if m:
            third_section += m.group(0)

    has_hash_in_third = (
        "hash" in third_section
        or "sha" in third_section
        or "a3f7b2c8e9d1" in third_section
        or "checksum" in third_section
    )
    if not has_hash_in_third:
        # Also accept hash anywhere in file if the document is structured as a table
        if "hash" not in content_lower and "sha" not in content_lower:
            print("FAILED: hash evidence not mentioned for third denial in denial_refutation_timeline.md")
            sys.exit(1)

    # Check structure: >= 4 ## headings OR Markdown table with >= 3 data rows
    heading_pattern = re.compile(r'^## .+', re.MULTILINE)
    headings = heading_pattern.findall(content)

    table_row_pattern = re.compile(r'^\|.+\|', re.MULTILINE)
    table_rows = table_row_pattern.findall(content)
    # Subtract header separator row (|---|---|)
    data_rows = [r for r in table_rows if not re.match(r'^\|[\s\-|]+\|$', r.strip())]

    if len(headings) < 4 and len(data_rows) < 3:
        print(
            f"FAILED: expected >= 4 ## headings OR >= 3 table data rows; "
            f"found {len(headings)} headings and {len(data_rows)} table rows"
        )
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
