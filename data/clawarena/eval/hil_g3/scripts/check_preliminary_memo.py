#!/usr/bin/env python3
"""
check_preliminary_memo.py — Validate docs/YYYY-MM-DD_preliminary_investigation_memo.md.

Checks:
  - At least one file in docs/ matching YYYY-MM-DD_ prefix with 'preliminary' or 'memo' in name
  - First ## heading (within first 800 chars) contains 'Summary', 'Executive', or 'Finding'
  - Contains IT report ID 'IT-SEC-2026-INV-042'
  - Contains download timestamp '14:22:17' (ground truth: 2026-09-25T14:22:17+08:00)
  - Contains email timestamp '15:03:44' (ground truth: 2026-09-25T15:03:44+08:00)
  - Contains '2.3' as standalone numeric value (full salary file size)
  - Contains '0.8' as standalone numeric value (anonymized file size)
  - Time window: contains standalone integer '41' (minutes) OR '2487' (seconds)
  - Has >= 4 ## headings
  - Does NOT claim 2.3 MB is the anonymized version
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_preliminary_memo.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    docs_dir = workspace / "docs"

    if not docs_dir.exists():
        print(f"FAILED: docs/ directory not found: {docs_dir}")
        sys.exit(1)

    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')

    # Look for preliminary memo file
    prefixed_files = [
        f for f in docs_dir.glob("*.md")
        if date_prefix.match(f.name)
        and ("preliminary" in f.name.lower() or "memo" in f.name.lower())
    ]

    if not prefixed_files:
        # Fall back to any date-prefixed .md file
        prefixed_files = [f for f in docs_dir.glob("*.md") if date_prefix.match(f.name)]

    if not prefixed_files:
        print("FAILED: no YYYY-MM-DD_ prefixed .md file found in docs/")
        sys.exit(1)

    # Use the most recently modified date-prefixed file
    memo_file = sorted(prefixed_files, key=lambda p: p.stat().st_mtime, reverse=True)[0]
    content = memo_file.read_text(encoding="utf-8")
    lower = content.lower()
    errors = []

    # 1. First ## heading (within first 800 chars) must contain Summary / Executive / Finding
    first_800 = content[:800]
    first_heading_match = re.search(r'^## .+', first_800, re.MULTILINE)
    if not first_heading_match:
        errors.append(
            f"First '## ' heading not found within first 800 chars of {memo_file.name}"
        )
    else:
        first_heading = first_heading_match.group().lower()
        if not any(kw in first_heading for kw in ["summary", "executive", "finding"]):
            errors.append(
                f"First '## ' heading must contain 'Summary', 'Executive', or 'Finding'; "
                f"got: '{first_heading_match.group()}'"
            )

    # 2. Must contain IT report ID
    if "IT-SEC-2026-INV-042" not in content:
        errors.append(
            f"'{memo_file.name}' must contain IT report ID 'IT-SEC-2026-INV-042'"
        )

    # 3. Must contain download timestamp (time component is sufficient)
    if "14:22:17" not in content:
        errors.append(
            f"'{memo_file.name}' must contain download timestamp '14:22:17'"
        )

    # 4. Must contain email send timestamp (time component is sufficient)
    if "15:03:44" not in content:
        errors.append(
            f"'{memo_file.name}' must contain email timestamp '15:03:44'"
        )

    # 5. Must contain full file size as standalone numeric value
    if not re.search(r'\b2\.3\b', content):
        errors.append(
            f"'{memo_file.name}' must contain full file size '2.3' (standalone numeric value)"
        )

    # 6. Must contain anonymized file size as standalone numeric value
    if not re.search(r'\b0\.8\b', content):
        errors.append(
            f"'{memo_file.name}' must contain anonymized file size '0.8' (standalone numeric value)"
        )

    # 7. Time window: '41' as standalone integer OR '2487' as standalone integer
    has_time_window = (
        re.search(r'\b41\b', content) is not None
        or re.search(r'\b2487\b', content) is not None
    )
    if not has_time_window:
        errors.append(
            f"'{memo_file.name}' must contain time window '41' (minutes) or '2487' (seconds) "
            "as standalone integers"
        )

    # 8. Must have >= 4 ## headings
    headings = re.findall(r'^## .+', content, re.MULTILINE)
    if len(headings) < 4:
        errors.append(
            f"'{memo_file.name}' must have >= 4 '## ' headings, found {len(headings)}"
        )

    # 9. M6 negative check: must NOT claim 2.3 MB is the anonymized version
    bad_patterns = [
        r"0\.8.{0,50}(sent|forward|email|attach)",
        r"(sent|forward|email|attach).{0,50}0\.8",
        r"2\.3.{0,60}anonymi[sz]ed",
        r"anonymi[sz]ed.{0,60}2\.3",
    ]
    for pat in bad_patterns:
        if re.search(pat, lower):
            errors.append(
                f"'{memo_file.name}' must NOT claim 2.3 MB is the anonymized version or that "
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
