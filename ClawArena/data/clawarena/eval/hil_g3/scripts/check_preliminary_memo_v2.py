#!/usr/bin/env python3
"""check_preliminary_memo_v2.py — Validates docs/YYYY-MM-DD_preliminary_investigation_memo.md for q14."""
import sys
import re
from pathlib import Path


def main():
    workspace = Path(sys.argv[1])
    docs_dir = workspace / "docs"

    if not docs_dir.exists():
        print("FAILED: docs/ directory not found")
        sys.exit(1)

    # Find a file matching the date-prefix pattern for preliminary memo
    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    memo_files = [
        f for f in docs_dir.glob("*.md")
        if date_prefix.match(f.name) and "preliminary" in f.name.lower()
    ]

    if not memo_files:
        # Try any date-prefixed md file (more lenient)
        memo_files = [
            f for f in docs_dir.glob("*.md")
            if date_prefix.match(f.name) and "memo" in f.name.lower()
        ]

    if not memo_files:
        print("FAILED: No date-prefixed preliminary investigation memo found in docs/")
        sys.exit(1)

    # Use the most recently modified one
    target = sorted(memo_files, key=lambda p: p.stat().st_mtime, reverse=True)[0]
    content = target.read_text(encoding="utf-8")
    lower = content.lower()
    errors = []

    # 1. First ## heading must contain 'Summary' or 'Executive' (within first 800 chars)
    first_800 = content[:800]
    first_heading_match = re.search(r'^## .+', first_800, re.MULTILINE)
    if not first_heading_match:
        errors.append(
            f"First '## ' heading not found within first 800 chars of {target.name}"
        )
    else:
        first_heading = first_heading_match.group().lower()
        if not any(kw in first_heading for kw in ["summary", "executive", "finding"]):
            errors.append(
                f"First '## ' heading must contain 'Summary', 'Executive', or 'Finding', "
                f"got: '{first_heading_match.group()}'"
            )

    # 2. Must contain IT report ID
    if "IT-SEC-2026-INV-042" not in content:
        errors.append("Memo must contain 'IT-SEC-2026-INV-042'")

    # 3. Must contain download timestamp
    if "14:22:17" not in content:
        errors.append("Memo must contain download timestamp '14:22:17'")

    # 4. Must contain email send timestamp
    if "15:03:44" not in content:
        errors.append("Memo must contain email timestamp '15:03:44'")

    # 5. Must have >= 4 ## headings
    headings = re.findall(r'^## .+', content, re.MULTILINE)
    if len(headings) < 4:
        errors.append(
            f"Memo must have >= 4 '## ' headings, found {len(headings)}"
        )

    # 6. M6 negative check: must NOT claim 2.3 MB is the anonymized version
    # or that 林小雅 sent the 0.8 MB file
    bad_patterns = [
        r"0\.8.{0,50}(sent|forward|email|attach)",
        r"(sent|forward|email|attach).{0,50}0\.8",
        r"2\.3.{0,60}anonymi[sz]ed",
        r"anonymi[sz]ed.{0,60}2\.3",
    ]
    for pat in bad_patterns:
        if re.search(pat, lower):
            errors.append(
                "Memo must NOT claim 2.3 MB is the anonymized version or that "
                f"林小雅 sent the 0.8 MB file. Found: '{re.search(pat, lower).group()}'"
            )

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
