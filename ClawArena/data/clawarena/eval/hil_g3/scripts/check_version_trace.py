#!/usr/bin/env python3
"""check_version_trace.py — Validates analysis/version_trace.md for q6."""
import sys
import re
from pathlib import Path


def main():
    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "version_trace.md"

    if not target.exists():
        print(f"FAILED: {target} not found")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    errors = []

    # Must contain version sizes
    if "2.1" not in content:
        errors.append("version_trace.md must contain '2.1' (v1.0 size)")
    if "2.3" not in content:
        errors.append("version_trace.md must contain '2.3' (v1.1 size)")

    # Must have >= 2 ## headings
    headings = re.findall(r'^## .+', content, re.MULTILINE)
    if len(headings) < 2:
        errors.append(f"version_trace.md must have >= 2 '## ' headings, found {len(headings)}")

    # Must explicitly exclude v1.0
    lower = content.lower()
    exclusion_patterns = [
        r"2\.1\s*(mb)?.{0,60}(not match|does not match|mismatch|ruled out|exclud|reject|refut)",
        r"(not match|does not match|mismatch|ruled out|exclud|reject|refut).{0,60}2\.1",
        r"v1\.0.{0,80}(ruled out|exclud|not match|refut|reject|eliminate)",
        r"(ruled out|exclud|not match|refut|reject|eliminate).{0,80}v1\.0",
        r"2\.1.{0,60}≠.{0,60}2\.3",
        r"2\.3.{0,60}≠.{0,60}2\.1",
    ]
    found_exclusion = any(
        re.search(pat, lower) for pat in exclusion_patterns
    )
    if not found_exclusion:
        errors.append(
            "version_trace.md must explicitly exclude v1.0 (e.g., 'v1.0 ruled out', "
            "'2.1 MB does not match', 'excludes v1.0', '2.1 ≠ 2.3')"
        )

    # Must NOT conclude v1.0 was downloaded
    bad_patterns = [
        r"v1\.0.{0,40}(was|is).{0,40}download",
        r"download.{0,40}v1\.0",
        r"林小雅.{0,80}v1\.0",
    ]
    for pat in bad_patterns:
        if re.search(pat, lower):
            errors.append(
                "version_trace.md must NOT conclude v1.0 was downloaded. "
                f"Found suspicious pattern: '{re.search(pat, lower).group()}'"
            )

    # Cross-consistency: must reference v1.1 as the downloaded version
    if "v1.1" not in content:
        errors.append("version_trace.md must reference 'v1.1' as the downloaded version")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
