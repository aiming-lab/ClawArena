#!/usr/bin/env python3
"""
check_q15.py -- Verify docs/waiver_justification_framework.md.

Usage:
    python check_q15.py <workspace_path>
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

    md_path = workspace / "docs" / "waiver_justification_framework.md"
    if not md_path.exists():
        errors.append(f"FAILED: {md_path} not found")
    else:
        try:
            content = md_path.read_text(encoding="utf-8")
        except Exception as e:
            errors.append(f"FAILED: cannot read {md_path}: {e}")
            content = ""

        if content:
            # Must reference Section 6.1 or Section 6.3
            if not re.search(r"Section 6\.1|Section 6\.3|6\.1|6\.3", content):
                errors.append(
                    "FAILED: 'Section 6.1' or 'Section 6.3' not cited"
                )

            # Must state $37,000 overspend amount
            if not re.search(r"\$?37[,.]?000|37,000", content):
                errors.append(
                    "FAILED: $37,000 overspend amount not cited"
                )

            # Must reference 39% or 39.4% variance
            if not re.search(r"\b39\.4\b|\b39\b.{0,5}%", content):
                errors.append(
                    "FAILED: 39.4% or 39% overspend percentage not cited"
                )

            # Must mention waiver requirements (at least 2 of the 3 components)
            components_found = 0
            if re.search(r"operational.{0,30}justif|justif.{0,30}rationale", content, re.IGNORECASE):
                components_found += 1
            if re.search(r"enrollment.{0,30}impact|enrollment.{0,30}improvement|35%|Q4", content, re.IGNORECASE):
                components_found += 1
            if re.search(r"future.{0,30}compliance|written.{0,30}approval|prior.{0,30}approval", content, re.IGNORECASE):
                components_found += 1
            if components_found < 2:
                errors.append(
                    f"FAILED: only {components_found}/3 waiver components identified "
                    "(need >= 2): operational justification, enrollment impact, future compliance"
                )

            # Must have >= 3 ## headings
            headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
            if len(headings) < 3:
                errors.append(
                    f"FAILED: file has only {len(headings)} ## headings (need >= 3)"
                )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
