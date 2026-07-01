#!/usr/bin/env python3
"""
check_q22.py -- Verify docs/narrative_exclusion_analysis.md (M6 explicit negative assertion).

Usage:
    python check_q22.py <workspace_path>
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

    md_path = workspace / "docs" / "narrative_exclusion_analysis.md"
    if not md_path.exists():
        errors.append(f"FAILED: {md_path} not found")
    else:
        try:
            content = md_path.read_text(encoding="utf-8")
        except Exception as e:
            errors.append(f"FAILED: cannot read {md_path}: {e}")
            content = ""

        if content:
            # Must reference 'narrative' with negative assertion (M6)
            if not re.search(
                r"(field narrative|nairobi_field_narrative|narrative).{0,80}"
                r"(not|cannot|should not|excluded|qualitative|approximate|cannot serve|"
                r"not authoritative|not the authoritative|insufficient)",
                content,
                re.IGNORECASE,
            ):
                errors.append(
                    "FAILED: M6 negative assertion missing — must explicitly state "
                    "the field narrative is NOT the authoritative quantitative source"
                )

            # Must reference 'financial' as the authoritative alternative
            if not re.search(r"financial", content, re.IGNORECASE):
                errors.append(
                    "FAILED: 'financial' records not identified as the appropriate "
                    "authoritative source"
                )

            # Must cite at least one specific qualitative language example from the narrative
            # Options: "approximately 200", "85-95%", "680-700", "approximately", "expect to reach"
            qualitative_examples = [
                r"approximately.{0,10}200",
                r"85.{0,3}95",
                r"680.{0,3}700",
                r"expect.{0,20}reach",
                r"approximately",
                r"informal.{0,30}workshop",
            ]
            found_qualitative = sum(
                1 for p in qualitative_examples if re.search(p, content, re.IGNORECASE)
            )
            if found_qualitative < 1:
                errors.append(
                    "FAILED: no specific qualitative/approximate language from "
                    "nairobi_field_narrative_Q2.md cited as an example "
                    "(e.g., 'approximately 200', '85-95%', '680-700', 'expect to reach')"
                )

            # Must have >= 2 ## headings
            headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
            if len(headings) < 2:
                errors.append(
                    f"FAILED: file has only {len(headings)} ## headings (need >= 2)"
                )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
