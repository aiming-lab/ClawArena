#!/usr/bin/env python3
"""
check_q13_self_correction.py — Validates analysis/self_correction_significance.md.

Checks:
  - Hesitation/self-correction documented
  - Implicit acknowledgment of resume inflation stated
  - Liu Wei and two-source corroboration mentioned
  - >= 2 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_q13_self_correction.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "self_correction_significance.md"

    if not target.exists():
        print("FAILED: file not found: analysis/self_correction_significance.md")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # Hesitation/self-correction documented
    if not re.search(r'hesitat|self.correct|self.correc', content, re.IGNORECASE):
        failures.append("Missing hesitation/self-correction documentation")

    # Implicit acknowledgment
    if not re.search(
        r'implicit|acknowledg|admit|concede|indicat|suggest|aware',
        content, re.IGNORECASE
    ):
        failures.append(
            "Missing implicit acknowledgment language "
            "('implicit', 'acknowledges', 'admits', 'indicates', 'suggests')"
        )

    # Liu Wei corroboration
    if not re.search(r'Liu Wei|reference', content, re.IGNORECASE):
        failures.append("Missing Liu Wei reference as corroborating source")

    # Two-source language
    if not re.search(
        r'two.source|second.source|corrobor|independent|both',
        content, re.IGNORECASE
    ):
        failures.append(
            "Missing two-source corroboration language "
            "('two sources', 'second source', 'corroborates')"
        )

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
