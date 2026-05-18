#!/usr/bin/env python3
"""
check_q9.py -- Verify docs/source_reliability_decision.md (M2 + M6).

Usage:
    python check_q9.py <workspace_path>
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

    md_path = workspace / "docs" / "source_reliability_decision.md"
    if not md_path.exists():
        errors.append(f"FAILED: {md_path} not found")
    else:
        try:
            content = md_path.read_text(encoding="utf-8")
        except Exception as e:
            errors.append(f"FAILED: cannot read {md_path}: {e}")
            content = ""

        if content:
            # Must explicitly choose financial records as more reliable
            if not re.search(
                r"financial.{0,30}(more reliable|reliable|authoritative|primary)|"
                r"(more reliable|reliable|authoritative|primary).{0,30}financial",
                content,
                re.IGNORECASE,
            ):
                errors.append(
                    "FAILED: file does not explicitly state financial records "
                    "are the more reliable source for compliance verification"
                )

            # M6 negative assertion: field narrative is NOT authoritative
            if not re.search(
                r"(field narrative|nairobi_field_narrative).{0,60}"
                r"(not|cannot|should not|excluded|qualitative|approximate)",
                content,
                re.IGNORECASE,
            ):
                errors.append(
                    "FAILED: M6 negative assertion missing — file must explicitly "
                    "state the field narrative is NOT the authoritative quantitative source"
                )

            # Must cite specific qualitative/approximate language from narrative
            if not re.search(
                r"approximately|approximately 200|85.95|680.700|about|roughly|expect",
                content,
                re.IGNORECASE,
            ):
                errors.append(
                    "FAILED: no specific qualitative or approximate language from "
                    "nairobi_field_narrative_Q2.md cited as an example"
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
