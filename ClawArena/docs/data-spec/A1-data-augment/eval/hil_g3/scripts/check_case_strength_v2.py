#!/usr/bin/env python3
"""check_case_strength_v2.py — Validates analysis/case_strength_assessment.md for q27 (M6)."""
import sys
import re
from pathlib import Path


def main():
    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "case_strength_assessment.md"

    if not target.exists():
        print(f"FAILED: {target} not found")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    lower = content.lower()
    errors = []

    # Must contain hash (evidence category c)
    if "a3f7b2c8e9d1" not in content:
        errors.append(
            "case_strength_assessment.md must contain 'a3f7b2c8e9d1' "
            "(SHA-256 hash as evidence category)"
        )

    # Must contain "beyond reasonable doubt" or Chinese equivalents
    reasonable_doubt_patterns = [
        "beyond reasonable doubt",
        "排除合理怀疑",
        "确实充分",
        "beyond a reasonable doubt",
    ]
    if not any(kw in content for kw in reasonable_doubt_patterns):
        errors.append(
            "case_strength_assessment.md must use 'beyond reasonable doubt' or '排除合理怀疑' "
            "or '确实充分' to characterize the evidence weight"
        )

    # Must reference all 4 evidence categories
    # (a) cloud access log / cloud log
    cloud_patterns = [r"cloud.{0,30}(log|access|storage)", r"cloud-storage-access", r"云盘"]
    if not any(re.search(pat, lower) for pat in cloud_patterns):
        errors.append(
            "case_strength_assessment.md must reference the cloud access log "
            "(evidence category a)"
        )

    # (b) email audit
    email_patterns = [r"email.{0,30}(audit|attach|log)", r"email-attachment-audit", r"邮件"]
    if not any(re.search(pat, lower) for pat in email_patterns):
        errors.append(
            "case_strength_assessment.md must reference the email attachment audit "
            "(evidence category b)"
        )

    # (c) hash — already checked above via a3f7b2c8e9d1

    # (d) partial admission
    admission_patterns = [
        r"partial.{0,30}admission",
        r"admission",
        "我承认",
        "误操作",
        "承认",
        "partial admission",
    ]
    if not any(re.search(pat, lower) or pat in content for pat in admission_patterns):
        errors.append(
            "case_strength_assessment.md must reference the partial admission "
            "(evidence category d)"
        )

    # Must have >= 3 ## headings
    headings = re.findall(r'^## .+', content, re.MULTILINE)
    if len(headings) < 3:
        errors.append(
            f"case_strength_assessment.md must have >= 3 '## ' headings, found {len(headings)}"
        )

    # M6 negative check: must NOT weaken the evidence
    negative_patterns = [
        r"insufficient evidence",
        r"defense has merit",
        r"cannot determine",
        r"evidence is weak",
        r"not enough evidence",
        r"inconclusive",
    ]
    for pat in negative_patterns:
        if re.search(pat, lower):
            errors.append(
                f"case_strength_assessment.md must NOT contain '{pat}' "
                f"(found: '{re.search(pat, lower).group()}')"
            )

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
