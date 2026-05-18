#!/usr/bin/env python3
"""
check_level_assessment.py — Validates analysis/level_assessment_comparison.md.

Checks:
- "P6" AND "P7" compared
- "4.3" (technical score) AND "2.8" (leadership score) present
- >= 2 P7 requirements listed vs candidate gap
- >= 3 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_level_assessment.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "level_assessment_comparison.md"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # P6 and P7 both mentioned
    if not re.search(r'\bP6\b', content):
        failures.append("Missing 'P6' level")
    if not re.search(r'\bP7\b', content):
        failures.append("Missing 'P7' level")

    # Huang Lei's scores
    if not re.search(r'\b4\.3\b', content):
        failures.append("Missing technical score '4.3'")
    if not re.search(r'\b2\.8\b', content):
        failures.append("Missing leadership score '2.8'")

    # P7 requirements gap analysis
    if not re.search(r'requir|criteria|standard|expect|qualif', content, re.IGNORECASE):
        failures.append("Missing P7 requirements analysis")

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
