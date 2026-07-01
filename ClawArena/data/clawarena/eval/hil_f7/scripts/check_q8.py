#!/usr/bin/env python3
"""
check_q8.py -- Verify docs/spec_comparison.md.

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
    errors = []

    md_path = workspace / "docs" / "spec_comparison.md"
    if not md_path.exists():
        print("FAILED: docs/spec_comparison.md not found")
        sys.exit(1)

    try:
        content = md_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read docs/spec_comparison.md: {e}")
        sys.exit(1)

    # Must contain both prices
    if not re.search(r'72[,.]?999', content):
        errors.append("FAILED: does not contain Screenshot 1 price '72,999' (618 promotional price)")

    if not re.search(r'74[,.]?999', content):
        errors.append("FAILED: does not contain Screenshot 2 price '74,999' (post-618 price)")

    # Must contain markdown table
    if not re.search(r'^\|.+\|', content, re.MULTILINE):
        errors.append("FAILED: no markdown table found (lines starting with |)")

    # Must mention stock status
    if not re.search(r'有货|in.stock|库存', content, re.IGNORECASE):
        errors.append("FAILED: does not mention stock status ('有货' or 'in stock')")

    # Must have >= 2 ## headings
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 2:
        errors.append(f"FAILED: only {len(headings)} ## headings found (need >= 2)")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
