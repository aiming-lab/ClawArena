#!/usr/bin/env python3
"""
check_q20.py -- Verify docs/deployment_vs_financial.md (M3 multi-source cross-check).

Usage:
    python check_q20.py <workspace_path>
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

    md_path = workspace / "docs" / "deployment_vs_financial.md"
    if not md_path.exists():
        errors.append(f"FAILED: {md_path} not found")
    else:
        try:
            content = md_path.read_text(encoding="utf-8")
        except Exception as e:
            errors.append(f"FAILED: cannot read {md_path}: {e}")
            content = ""

        if content:
            # Must cite 14 staff
            if not re.search(r"\b14\b.{0,30}(staff|person|employee)|"
                             r"(staff|person|employee).{0,30}\b14\b", content, re.IGNORECASE):
                errors.append(
                    "FAILED: '14' (total staff count) not cited in context of staff/personnel"
                )

            # Must cite $409,000 or 409,000 labor cost
            if not re.search(r"\$?409[,.]?000|409,000|409000", content):
                errors.append(
                    "FAILED: Personnel labor cost '$409,000' not cited"
                )

            # Must show cost-per-person calculation or result
            if not re.search(
                r"29[,.]?214|29214|per.{0,20}staff|per.{0,20}person|per.{0,20}member|"
                r"cost.{0,30}per|implied.{0,30}cost",
                content,
                re.IGNORECASE,
            ):
                errors.append(
                    "FAILED: cost-per-person calculation or result not present"
                )

            # Must reference plausibility calculation (0.98 workshops or similar)
            if not re.search(
                r"0\.98|plausib|workshop.{0,30}per.{0,30}month|per.{0,30}officer.{0,30}month",
                content,
                re.IGNORECASE,
            ):
                errors.append(
                    "FAILED: plausibility calculation (0.98 workshops/officer/month) "
                    "not referenced"
                )

            # Must state Annex C caveat
            if not re.search(
                r"Annex C|documentation.{0,30}(not|cannot|does not)|"
                r"does not.{0,30}(substitute|replace|prove)",
                content,
                re.IGNORECASE,
            ):
                errors.append(
                    "FAILED: Annex C documentation caveat not stated "
                    "(deployment consistency does not substitute for documentation requirements)"
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
