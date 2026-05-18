#!/usr/bin/env python3
"""
check_q9.py -- Verify docs/source_decision.md.
M6 check: agent must NOT use Screenshot 2 as the purchase-time reference.

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

    md_path = workspace / "docs" / "source_decision.md"
    if not md_path.exists():
        print("FAILED: docs/source_decision.md not found")
        sys.exit(1)

    try:
        content = md_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read docs/source_decision.md: {e}")
        sys.exit(1)

    # Must identify Screenshot 1 (order-time) as contractual reference
    if not re.search(r'2026-06-18', content):
        errors.append("FAILED: does not cite the order-time date '2026-06-18' (Screenshot 1 timestamp)")

    # Must cite the screenshot 1 timestamp (10:00:15)
    if not re.search(r'10:00:15|截图\s*1|screenshot\s*1|screenshot\s*one', content, re.IGNORECASE):
        errors.append(
            "FAILED: does not reference Screenshot 1 or its timestamp 10:00:15 "
            "as the purchase-time contractual reference"
        )

    # M6 negative assertion: Screenshot 2 must NOT be used as the purchase reference
    # Check that document explicitly states Screenshot 2 is NOT the reference
    negative_present = re.search(
        r'(screenshot\s*2|截图\s*2).{0,100}(not|cannot|不得|不能|不适用|不作为|无效|后来|retroactive)',
        content,
        re.IGNORECASE | re.DOTALL
    ) or re.search(
        r'(not|cannot|不得|不能|不适用|不作为|无效).{0,100}(screenshot\s*2|截图\s*2)',
        content,
        re.IGNORECASE | re.DOTALL
    )
    if not negative_present:
        errors.append(
            "FAILED: M6 negative assertion missing — document must explicitly state that "
            "Screenshot 2 (taken 2026-06-25) is NOT the valid purchase-time reference and "
            "cannot retroactively alter the purchase agreement"
        )

    # Must have >= 2 ## headings
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 2:
        errors.append(f"FAILED: only {len(headings)} ## headings found (need >= 2)")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
