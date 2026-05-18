#!/usr/bin/env python3
"""
check_q17.py -- Verify docs/pemberton_formal_response_draft.md.

Usage:
    python check_q17.py <workspace_path>
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

    md_path = workspace / "docs" / "pemberton_formal_response_draft.md"
    if not md_path.exists():
        errors.append(f"FAILED: {md_path} not found")
    else:
        try:
            content = md_path.read_text(encoding="utf-8")
        except Exception as e:
            errors.append(f"FAILED: cannot read {md_path}: {e}")
            content = ""

        if content:
            # Must reference Annex C or PEM activity codes
            if not re.search(
                r"Annex C|PEM-EDT-01|PEM-INF-01|PEM-GOV-01|PEM-EDU-01",
                content,
                re.IGNORECASE,
            ):
                errors.append(
                    "FAILED: 'Annex C' or PEM activity code not referenced"
                )

            # Must cite $37,000 overspend or 39.4% variance
            if not re.search(r"\$?37[,.]?000|37,000|39\.4|39\.4%", content):
                errors.append(
                    "FAILED: $37,000 overspend amount or 39.4% variance not cited"
                )

            # Must reference Petrova's 58% or 63% figure
            if not re.search(r"\b58\b|\b63\b", content):
                errors.append(
                    "FAILED: Petrova's verified completion figure (58% or 63%) not cited"
                )

            # Must mention waiver
            if not re.search(r"waiver", content, re.IGNORECASE):
                errors.append("FAILED: 'waiver' not mentioned")

            # Must mention documentation improvement
            if not re.search(r"documentation.{0,30}(improvement|plan)|improvement.{0,30}plan", content, re.IGNORECASE):
                errors.append(
                    "FAILED: 'documentation improvement' or 'improvement plan' not mentioned"
                )

            # Must have >= 4 ## headings
            headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
            if len(headings) < 4:
                errors.append(
                    f"FAILED: file has only {len(headings)} ## headings (need >= 4)"
                )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
