#!/usr/bin/env python3
"""
check_q23.py -- Verify docs/remediation_action_plan.md.

Usage:
    python check_q23.py <workspace_path>
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

    md_path = workspace / "docs" / "remediation_action_plan.md"
    if not md_path.exists():
        errors.append(f"FAILED: {md_path} not found")
    else:
        try:
            content = md_path.read_text(encoding="utf-8")
        except Exception as e:
            errors.append(f"FAILED: cannot read {md_path}: {e}")
            content = ""

        if content:
            # Must reference grant agreement or Annex C
            if not re.search(
                r"Section 6|Annex C|grant agreement|grant_agreement",
                content,
                re.IGNORECASE,
            ):
                errors.append(
                    "FAILED: 'Section 6', 'Annex C', or 'grant agreement' not referenced"
                )

            # Must name at least one responsible party
            responsible_parties = [
                "Fatima", "James", "Sophie", "Rachel", "Mwangi", "Laurent", "Wu",
                "Al-Hassan", "Program Director", "Field Director", "Finance Director",
            ]
            found_responsible = [p for p in responsible_parties if p in content]
            if not found_responsible:
                errors.append(
                    "FAILED: no responsible party named "
                    "(expected one of: Fatima, James, Sophie, Rachel, or their titles)"
                )

            # Must include timeline references
            if not re.search(
                r"\b14\b.{0,20}(day|calendar)|30.{0,20}(day|calendar)|"
                r"calendar.{0,20}day|deadline|Year 3",
                content,
                re.IGNORECASE,
            ):
                errors.append(
                    "FAILED: no timeline mentioned (14 calendar days, 30 days, or Year 3)"
                )

            # Must have >= 3 ## headings (one per compliance gap)
            headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
            if len(headings) < 3:
                errors.append(
                    f"FAILED: file has only {len(headings)} ## headings (need >= 3)"
                )

            # Must address multiple compliance gaps: count headings or gap-related keywords
            gap_keywords = [
                r"mobilization|budget.{0,20}waiver|waiver",
                r"educator.{0,20}training|documentation.{0,20}gap|retroactive",
                r"infrastructure|government.{0,20}co.signature|co-signature",
            ]
            gaps_found = sum(
                1 for p in gap_keywords if re.search(p, content, re.IGNORECASE)
            )
            if gaps_found < 2:
                errors.append(
                    f"FAILED: only {gaps_found}/3 compliance gaps addressed "
                    "(need >= 2 of: mobilization waiver, educator training documentation, "
                    "infrastructure co-signatures)"
                )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
