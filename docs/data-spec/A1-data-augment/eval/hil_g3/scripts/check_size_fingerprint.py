#!/usr/bin/env python3
"""check_size_fingerprint.py — Validates analysis/size_fingerprint.md for q3."""
import sys
import re
from pathlib import Path


def main():
    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "size_fingerprint.md"

    if not target.exists():
        print(f"FAILED: {target} not found")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    errors = []

    # Must contain the ratio 2.875
    if "2.875" not in content:
        errors.append("size_fingerprint.md must contain the computed ratio '2.875' (= 2.3 / 0.8)")

    # Must contain both sizes
    if "0.8" not in content:
        errors.append("size_fingerprint.md must contain '0.8' (anonymized file size)")
    if "2.3" not in content:
        errors.append("size_fingerprint.md must contain '2.3' (full salary file size)")

    # Must have >= 2 ## headings
    headings = re.findall(r'^## .+', content, re.MULTILINE)
    if len(headings) < 2:
        errors.append(f"size_fingerprint.md must have >= 2 '## ' headings, found {len(headings)}")

    # Must NOT conclude that the email attachment matches the anonymized version
    # (i.e., must not say 0.8 MB matches the email attachment)
    lower = content.lower()
    bad_patterns = [
        r"email.{0,40}0\.8",
        r"0\.8.{0,40}email",
        r"attachment.{0,40}0\.8",
        r"0\.8.{0,40}attachment",
        r"anonymized.{0,40}match.{0,40}email",
        r"email.{0,40}match.{0,40}anonymized",
    ]
    for pat in bad_patterns:
        if re.search(pat, lower):
            errors.append(
                f"size_fingerprint.md must NOT conclude the email attachment matches the "
                f"anonymized (0.8 MB) version. Found suspicious pattern near: "
                f"'{re.search(pat, lower).group()}'"
            )

    # Cross-consistency: must reference "14:22" (download time)
    if "14:22" not in content:
        errors.append(
            "size_fingerprint.md should reference '14:22' (download time) to cross-validate "
            "with access_timeline.json"
        )

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
