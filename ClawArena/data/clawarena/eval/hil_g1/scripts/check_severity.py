#!/usr/bin/env python3
"""
check_severity.py — Validates analysis/discrepancy_severity_assessment.md.

Checks:
- "3x" or "300%" or ("12" vs "4" ratio) present
- "P7" requirements vs leadership score gap mentioned
- "inflat" or "exaggerat" present
- >= 2 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_severity.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "discrepancy_severity_assessment.md"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # 3x ratio / 300% / 12 vs 4
    has_ratio = bool(
        re.search(r'3x|3-fold|three.fold|300%', content, re.IGNORECASE)
        or (re.search(r'\b12\b', content) and re.search(r'\b4\b', content))
    )
    if not has_ratio:
        failures.append("Missing 3x ratio language ('3x', '300%', or '12' vs '4')")

    # P7 requirements gap
    if not re.search(r'\bP7\b', content):
        failures.append("Missing 'P7' level reference")

    # Inflation / exaggeration language
    if not re.search(r'inflat|exaggerat|overstat', content, re.IGNORECASE):
        failures.append("Missing inflation/exaggeration language ('inflat', 'exaggerat')")

    # >= 2 headings
    headings = re.findall(r'^## ', content, re.MULTILINE)
    if len(headings) < 2:
        failures.append(f"Only {len(headings)} ## headings (expected >= 2)")

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
