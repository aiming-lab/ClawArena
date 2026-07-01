#!/usr/bin/env python3
"""
check_org_dynamics.py — Validates analysis/organizational_dynamics_analysis.md.

Checks:
- "CTO" AND ("Zhang Wei" or "HR VP") with opposing positions
- Precedent/risk of minimization argued
- >= 3 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_org_dynamics.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "organizational_dynamics_analysis.md"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # CTO present
    if not re.search(r'\bCTO\b', content):
        failures.append("Missing 'CTO'")

    # Zhang Wei / HR VP opposing position
    if not re.search(r'Zhang Wei|HR VP', content, re.IGNORECASE):
        failures.append("Missing 'Zhang Wei' or 'HR VP' opposing position")

    # Opposing positions (divergence language)
    if not re.search(r'diverge|oppos|disagree|conflict|tension|vs\.?|versus', content, re.IGNORECASE):
        failures.append("Missing opposing positions / divergence language")

    # Precedent / risk of minimization
    if not re.search(r'precedent|risk|minimiz|endorse|normalize|endorsing misrepresent', content, re.IGNORECASE):
        failures.append("Missing precedent/risk of CTO minimization argument")

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
