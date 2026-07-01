#!/usr/bin/env python3
"""
check_bias_risk.py — Validates analysis/b2_bias_risk.md.

Checks:
  1. File exists at analysis/b2_bias_risk.md
  2. Anchoring bias / complaint-framing bias explained
  3. Correct reframe stated: difference with valid explanation ≠ problem
  4. ≥2 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_bias_risk.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "b2_bias_risk.md"

    if not target.exists():
        print(f"FAILED: {target} does not exist")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # Anchoring / complaint framing bias
    has_bias = re.search(
        r'\b(anchor\w*|bias|complaint.framing|framing|presupposition|assumption)\b',
        content, re.IGNORECASE
    )
    if not has_bias:
        failures.append(
            "FAILED: anchoring bias or complaint framing not described "
            "('anchoring', 'bias', 'complaint-framing', etc. expected)"
        )

    # Correct reframe: difference with explanation is not automatically a problem
    has_reframe = re.search(
        r'(valid\s+explanation|explained\s+difference|not\s+(necessarily\s+)?a\s+problem|'
        r'does\s+not\s+indicate|correct\s+question|reframe)',
        content, re.IGNORECASE
    )
    if not has_reframe:
        failures.append(
            "FAILED: correct reframe not stated "
            "(should clarify that a difference with valid explanation is not a problem)"
        )

    # Minimum heading count
    headings = re.findall(r'^##\s+', content, re.MULTILINE)
    if len(headings) < 2:
        failures.append(
            f"FAILED: only {len(headings)} ## headings found (expected ≥2)"
        )

    if failures:
        for f in failures:
            print(f)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
