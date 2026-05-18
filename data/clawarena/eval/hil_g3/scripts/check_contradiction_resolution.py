#!/usr/bin/env python3
"""check_contradiction_resolution.py — Validates analysis/contradiction_resolution.md for q12."""
import sys
import re
from pathlib import Path


def main():
    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "contradiction_resolution.md"

    if not target.exists():
        print(f"FAILED: {target} not found")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    lower = content.lower()
    errors = []

    # Must contain IT report ID
    if "IT-SEC-2026-INV-042" not in content:
        errors.append("contradiction_resolution.md must contain 'IT-SEC-2026-INV-042'")

    # Must reference email attachment near scope context (within 200 chars)
    scope_pattern = re.search(
        r"email.{0,200}scope|scope.{0,200}email",
        lower
    )
    if not scope_pattern:
        errors.append(
            "contradiction_resolution.md must reference 'email attachment' near 'scope' "
            "(within ~200 characters of each other)"
        )

    # Must contain a resolution statement that both sources are compatible/accurate
    compat_patterns = [
        r"both.{0,100}(accurate|correct|valid|compatible)",
        r"(accurate|correct|valid|compatible).{0,100}both",
        r"not.{0,30}(genuine|real|actual).{0,30}contradiction",
        r"(no|not a).{0,30}contradiction",
        r"within.{0,50}scope",
        r"scope.{0,50}(limit|gap|boundary)",
    ]
    found_compat = any(re.search(pat, lower) for pat in compat_patterns)
    if not found_compat:
        errors.append(
            "contradiction_resolution.md must contain a resolution statement that both "
            "the IT report and email audit are compatible/accurate within their respective scopes"
        )

    # Must NOT conclude IT was "wrong" or "incorrect"
    wrong_patterns = [
        r"it.{0,50}report.{0,50}(wrong|incorrect|inaccurate|error|false)",
        r"(wrong|incorrect|inaccurate|error|false).{0,50}it.{0,50}report",
        r"it.{0,30}(was|is).{0,30}wrong",
    ]
    for pat in wrong_patterns:
        if re.search(pat, lower):
            errors.append(
                "contradiction_resolution.md must NOT conclude IT was 'wrong' or 'incorrect'. "
                f"Found: '{re.search(pat, lower).group()}'"
            )

    # Must reference the email exchange (chenjing or 陈静) as scope-gap source
    has_ref = (
        "chenjing" in lower
        or "陈静" in content
        or "chenjing_itsec_email" in lower
    )
    if not has_ref:
        errors.append(
            "contradiction_resolution.md must reference the email exchange with IT "
            "(chenjing, 陈静, or chenjing_itsec_email.md) as the scope-gap confirmation source"
        )

    # Must have >= 3 ## headings
    headings = re.findall(r'^## .+', content, re.MULTILINE)
    if len(headings) < 3:
        errors.append(
            f"contradiction_resolution.md must have >= 3 '## ' headings, found {len(headings)}"
        )

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
