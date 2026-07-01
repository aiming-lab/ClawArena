#!/usr/bin/env python3
"""
check_q20.py -- Verify docs/courier_investigation_analysis.md.

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

    md_path = workspace / "docs" / "courier_investigation_analysis.md"
    if not md_path.exists():
        print("FAILED: docs/courier_investigation_analysis.md not found")
        sys.exit(1)

    try:
        content = md_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read docs/courier_investigation_analysis.md: {e}")
        sys.exit(1)

    # Must contain GPU-A40-48G
    if "GPU-A40-48G" not in content:
        errors.append("FAILED: does not mention internal product code 'GPU-A40-48G'")

    # Must mention A100 inventory / shortage
    if not re.search(r'A100.{0,20}(缺货|库存|inventory|zero|没有|stock)', content, re.IGNORECASE) and \
       not re.search(r'(缺货|库存为0|zero.{0,10}inventory)', content, re.IGNORECASE):
        errors.append("FAILED: does not mention A100 inventory shortage or zero inventory")

    # Must mention oral/verbal (not formal written) authorization
    if not re.search(r'口头|oral|verbal|not.{0,20}written|非书面|非正式', content, re.IGNORECASE):
        errors.append(
            "FAILED: does not distinguish oral/verbal supervisor approval from a formal written policy"
        )

    # Must mention courier evidence date
    if "2026-06-29" not in content:
        errors.append("FAILED: does not mention courier evidence date '2026-06-29'")

    # Must mention all three tracking numbers
    if not re.search(r'88761', content):
        errors.append("FAILED: does not mention first waybill number (88761)")
    if not re.search(r'88922', content):
        errors.append("FAILED: does not mention second waybill number (88922)")
    if not re.search(r'89103', content):
        errors.append("FAILED: does not mention third waybill number (89103)")

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
