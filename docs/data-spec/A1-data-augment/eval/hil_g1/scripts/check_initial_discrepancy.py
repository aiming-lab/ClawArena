#!/usr/bin/env python3
"""
check_initial_discrepancy.py — Validates analysis/initial_discrepancy_summary.md.

Checks:
- "12" AND "4" present (team size discrepancy values)
- First ## heading contains "Summary", "Executive", or "Finding"
- "3x" or "three times" or "ratio" present (discrepancy ratio)
- >= 3 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_initial_discrepancy.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "initial_discrepancy_summary.md"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # Check "12" and "4" present (word boundaries to avoid false positives)
    if not re.search(r'\b12\b', content):
        failures.append("Missing '12' (resume team size claim)")
    if not re.search(r'\b4\b', content):
        failures.append("Missing '4' (reference check team size)")

    # Check executive summary / finding heading appears first
    headings = re.findall(r'^## (.+)$', content, re.MULTILINE)
    if not headings:
        failures.append("No ## headings found")
    else:
        first = headings[0]
        if not re.search(r'summary|executive|finding|conclusion', first, re.IGNORECASE):
            failures.append(
                f"First ## heading '{first}' does not contain "
                "Summary/Executive/Finding/Conclusion — lead with the answer"
            )

    # Check 3x ratio language
    if not re.search(r'3x|three times|3-fold|ratio|three.fold', content, re.IGNORECASE):
        failures.append("Missing discrepancy ratio language ('3x', 'three times', or 'ratio')")

    # Check >= 3 headings
    if len(headings) < 3:
        failures.append(f"Only {len(headings)} ## headings (expected >= 3)")

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
