#!/usr/bin/env python3
"""
check_q24.py -- Verify docs/legal_complaint_draft.md.

Usage:
    python check_q24.py <workspace_path>
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

    md_path = workspace / "docs" / "legal_complaint_draft.md"
    if not md_path.exists():
        print("FAILED: docs/legal_complaint_draft.md not found")
        sys.exit(1)

    try:
        content = md_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read docs/legal_complaint_draft.md: {e}")
        sys.exit(1)

    # Must cite consumer protection law
    if not re.search(r'消费者权益|Consumer.{0,10}Rights|Consumer.{0,10}Protection|消费者保护', content, re.IGNORECASE):
        errors.append(
            "FAILED: does not cite consumer protection law (消费者权益保护法 or equivalent)"
        )

    # Must state the paid amount
    if not re.search(r'72[,.]?999', content):
        errors.append("FAILED: does not mention paid amount '72,999' or '72999'")

    # Must mention ordered product (A100)
    if not re.search(r'GPU-A100-80G|A100\s*80GB|A100', content, re.IGNORECASE):
        errors.append("FAILED: does not mention ordered product GPU-A100-80G or A100")

    # Must mention received product (A40)
    if not re.search(r'GPU-A40-48G|A40\s*48GB|A40', content, re.IGNORECASE):
        errors.append("FAILED: does not mention received product GPU-A40-48G or A40")

    # Must cite return policy section 4.2
    if not re.search(r'4\.2', content):
        errors.append("FAILED: does not cite return policy Section 4.2")

    # Must mention 12315 consumer hotline
    if "12315" not in content:
        errors.append("FAILED: does not mention '12315' consumer complaint hotline")

    # Must have >= 4 ## headings
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 4:
        errors.append(f"FAILED: only {len(headings)} ## headings found (need >= 4)")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
