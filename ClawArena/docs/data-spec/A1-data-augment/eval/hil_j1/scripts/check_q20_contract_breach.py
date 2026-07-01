#!/usr/bin/env python3
"""
check_q20_contract_breach.py — Verify q20: analysis/合同违约分析.md
  - File exists
  - Contains '7.3' (completion rate >= 7.3% clause)
  - Contains '9.1' (engagement rate >= 9.1% clause)
  - Contains '4.2' (conversion rate >= 4.2% clause)
  - Contains contract vs actual comparison keywords
  - >= 3 '##' headings
"""
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "合同违约分析.md"

    if not target.exists():
        print("FAILED: analysis/合同违约分析.md not found")
        sys.exit(1)

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read file: {e}")
        sys.exit(1)

    errors = []

    # Check 完播率 clause
    if "7.3" not in content:
        errors.append("contract clause '7.3' (completion rate >= 7.3%) not found")

    # Check 互动率 clause
    if "9.1" not in content:
        errors.append("contract clause '9.1' (engagement rate >= 9.1%) not found")

    # Check 转化率 clause
    if "4.2" not in content:
        errors.append("contract clause '4.2' (conversion rate >= 4.2%) not found")

    # Check contract vs actual comparison keywords
    comparison_keywords = ["合同", "实际", "官方", "对比", "差距"]
    if not any(kw in content for kw in comparison_keywords):
        errors.append(
            f"contract vs actual comparison not found (expected one of: {comparison_keywords})"
        )

    # Check heading count >= 3
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 3:
        errors.append(f"'##' headings: {len(headings)} (expected >= 3)")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
