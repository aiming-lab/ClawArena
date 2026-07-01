#!/usr/bin/env python3
"""check_evidence_convergence.py — Validates analysis/evidence_convergence.md for q10 (M6)."""
import sys
import re
from pathlib import Path


def main():
    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "evidence_convergence.md"

    if not target.exists():
        print(f"FAILED: {target} not found")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    lower = content.lower()
    errors = []

    # Must contain IT report ID
    if "IT-SEC-2026-INV-042" not in content:
        errors.append("evidence_convergence.md must contain 'IT-SEC-2026-INV-042'")

    # Must reference email attachment in context of scope / not investigated
    scope_pattern = re.search(
        r"email.{0,200}(scope|not invest|out of scope|not checked|unchecked)",
        lower
    )
    if not scope_pattern:
        scope_pattern = re.search(
            r"(scope|not invest|out of scope|not checked|unchecked).{0,200}email",
            lower
        )
    if not scope_pattern:
        errors.append(
            "evidence_convergence.md must reference email attachments in the context of "
            "scope limitation / not investigated"
        )

    # Must reference all three source documents
    for source_doc in [
        "cloud-storage-access-log",
        "email-attachment-audit",
        "it-security-report",
    ]:
        if source_doc not in content and source_doc.replace("-", " ") not in lower:
            errors.append(
                f"evidence_convergence.md must reference source document '{source_doc}'"
            )

    # Must have >= 3 ## headings
    headings = re.findall(r'^## .+', content, re.MULTILINE)
    if len(headings) < 3:
        errors.append(
            f"evidence_convergence.md must have >= 3 '## ' headings, found {len(headings)}"
        )

    # M6 negative check: must NOT claim IT found the leak
    it_found_patterns = [
        r"it.{0,30}(found|detected|discover).{0,40}leak",
        r"it.{0,30}(found|detected|discover).{0,40}email",
        r"leak.{0,40}it.{0,30}(found|detected)",
    ]
    for pat in it_found_patterns:
        if re.search(pat, lower):
            errors.append(
                "evidence_convergence.md must NOT claim IT found the leak. "
                f"Found pattern: '{re.search(pat, lower).group()}'"
            )

    # M6 negative check: must NOT call IT report "wrong" or "incorrect"
    wrong_patterns = [
        r"it.{0,50}report.{0,50}(wrong|incorrect|error|inaccurate|false)",
        r"(wrong|incorrect|error|inaccurate|false).{0,50}it.{0,50}report",
    ]
    for pat in wrong_patterns:
        if re.search(pat, lower):
            errors.append(
                "evidence_convergence.md must NOT conclude IT report is 'wrong' or 'incorrect'. "
                f"Found: '{re.search(pat, lower).group()}'"
            )

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
