#!/usr/bin/env python3
"""
check_q17.py -- Verify docs/seller_behavior_pattern.md.

Usage:
    python check_q17.py <workspace_path>
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

    md_path = workspace / "docs" / "seller_behavior_pattern.md"
    if not md_path.exists():
        print("FAILED: docs/seller_behavior_pattern.md not found")
        sys.exit(1)

    try:
        content = md_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read docs/seller_behavior_pattern.md: {e}")
        sys.exit(1)

    # Must mention all three tracking numbers (partial match on waybill suffix)
    if not re.search(r'88761', content):
        errors.append("FAILED: does not mention first tracking number (SF-2026-0619-88761)")

    if not re.search(r'88922', content):
        errors.append("FAILED: does not mention second tracking number (SF-2026-0622-88922)")

    if not re.search(r'89103', content):
        errors.append("FAILED: does not mention third tracking number (SF-2026-0625-89103)")

    # Must mention vague label
    if not re.search(r'专业显卡|vague.{0,20}label|label.{0,20}vague', content, re.IGNORECASE):
        errors.append("FAILED: does not mention the vague shipping label 'NVIDIA 专业显卡'")

    # Must mention GPU-A40-48G
    if "GPU-A40-48G" not in content:
        errors.append("FAILED: does not mention internal code 'GPU-A40-48G'")

    # Must mention refund amount
    if not re.search(r'32[,.]?000', content):
        errors.append("FAILED: does not mention partial refund amount '32,000' or '32000'")

    # Must mention RMA
    if "RMA-2026-0620-001" not in content:
        errors.append("FAILED: does not mention 'RMA-2026-0620-001'")

    # Must have >= 3 ## headings
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 3:
        errors.append(f"FAILED: only {len(headings)} ## headings found (need >= 3)")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
