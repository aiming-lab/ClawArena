#!/usr/bin/env python3
"""check_metadata_analysis.py — Validates analysis/metadata_analysis.md for q18."""
import sys
import re
from pathlib import Path


def main():
    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "metadata_analysis.md"

    if not target.exists():
        print(f"FAILED: {target} not found")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    lower = content.lower()
    errors = []

    # Must contain the hash value (same as cryptographic_proof.md — cross-consistency check)
    if "a3f7b2c8e9d1" not in content:
        errors.append(
            "metadata_analysis.md must contain hash 'a3f7b2c8e9d1' "
            "(cross-consistency with cryptographic_proof.md)"
        )

    # Must contain the file size 2.3
    if "2.3" not in content:
        errors.append("metadata_analysis.md must contain '2.3' (file size in MB)")

    # Must reference salary-spreadsheet-metadata (the source document)
    if "salary-spreadsheet-metadata" not in lower:
        errors.append(
            "metadata_analysis.md must reference 'salary-spreadsheet-metadata' "
            "as the source document"
        )

    # Must reference salary-data-analysis.xlsx (the email attachment)
    if "salary-data-analysis" not in lower:
        errors.append(
            "metadata_analysis.md must reference 'salary-data-analysis.xlsx' "
            "(the email attachment confirmed by metadata)"
        )

    # Must have >= 2 ## headings
    headings = re.findall(r'^## .+', content, re.MULTILINE)
    if len(headings) < 2:
        errors.append(
            f"metadata_analysis.md must have >= 2 '## ' headings, found {len(headings)}"
        )

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
