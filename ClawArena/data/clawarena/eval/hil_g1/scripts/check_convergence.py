#!/usr/bin/env python3
"""
check_convergence.py — Validates analysis/evidence_convergence_summary.md.

Checks:
- >= 4 independent sources listed (Liu Wei, Huang Lei, GitHub, LinkedIn)
- "converge" or "consistent" or "independent" confirmation language
- >= 3 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_convergence.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "evidence_convergence_summary.md"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # Check for >= 4 independent sources
    sources_found = 0
    if re.search(r'Liu Wei', content):
        sources_found += 1
    if re.search(r'Huang Lei', content):
        sources_found += 1
    if re.search(r'GitHub', content, re.IGNORECASE):
        sources_found += 1
    if re.search(r'LinkedIn', content, re.IGNORECASE):
        sources_found += 1

    if sources_found < 4:
        failures.append(
            f"Only {sources_found}/4 required sources mentioned "
            "(need: Liu Wei, Huang Lei, GitHub, LinkedIn)"
        )

    # Convergence language
    if not re.search(r'converge|consistent|independent|corrobor|align', content, re.IGNORECASE):
        failures.append("Missing convergence/consistency language")

    # >= 3 headings
    headings = re.findall(r'^## ', content, re.MULTILINE)
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
