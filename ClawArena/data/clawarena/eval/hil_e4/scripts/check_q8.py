#!/usr/bin/env python3
"""
check_q8.py -- Verify docs/petrova_assessment_analysis.md.

Usage:
    python check_q8.py <workspace_path>
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

    md_path = workspace / "docs" / "petrova_assessment_analysis.md"
    if not md_path.exists():
        errors.append(f"FAILED: {md_path} not found")
    else:
        try:
            content = md_path.read_text(encoding="utf-8")
        except Exception as e:
            errors.append(f"FAILED: cannot read {md_path}: {e}")
            content = ""

        if content:
            # Must cite 39 verified workshops
            if not re.search(r"\b39\b", content):
                errors.append(
                    "FAILED: file does not cite '39' (Petrova's verified workshop count)"
                )

            # Must cite 58% conservative estimate
            if not re.search(r"\b58\b", content):
                errors.append(
                    "FAILED: file does not cite '58' (Petrova's conservative completion estimate)"
                )

            # Must cite 63% inclusive estimate
            if not re.search(r"\b63\b", content):
                errors.append(
                    "FAILED: file does not cite '63' (Petrova's inclusive completion estimate)"
                )

            # Must reference Petrova by name
            if not re.search(r"Petrova", content, re.IGNORECASE):
                errors.append("FAILED: 'Petrova' not mentioned")

            # Must distinguish from Sophie's estimate or explain the gap
            if not re.search(
                r"Sophie|68|72|verified|estimated|reconcil",
                content,
                re.IGNORECASE,
            ):
                errors.append(
                    "FAILED: file does not distinguish Petrova's figure from the 68-72% "
                    "internal estimate (no reference to Sophie, 68%, 72%, or verification gap)"
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
