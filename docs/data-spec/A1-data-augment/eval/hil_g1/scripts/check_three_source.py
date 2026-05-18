#!/usr/bin/env python3
"""
check_three_source.py — Validates analysis/three_source_corroboration.md.

Checks:
- "Liu Wei" present (reference check source)
- "hesitat" or "self-correct" present (interview observation source)
- "three" or "3" sources mentioned
- >= 2 ## headings
- Corroboration/convergence language present
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_three_source.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "three_source_corroboration.md"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # Liu Wei reference
    if not re.search(r'Liu Wei', content):
        failures.append("Missing source 'Liu Wei' (reference check)")

    # Interview hesitation / self-correction
    if not re.search(r'hesitat|self.correct', content, re.IGNORECASE):
        failures.append("Missing interview behavioral signal ('hesitat' or 'self-correct')")

    # Three sources mentioned
    if not re.search(r'\bthree\b|\b3\b', content, re.IGNORECASE):
        failures.append("Missing mention of three/3 sources")

    # Corroboration / convergence language
    if not re.search(r'corrobor|converge|consistent|independent|confirm', content, re.IGNORECASE):
        failures.append("Missing corroboration/convergence language")

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
