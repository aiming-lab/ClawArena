#!/usr/bin/env python3
"""
check_q11_caliber_report.py — Verify q11: analysis/口径辨析报告.md (M2 check)
  - File exists
  - Contains '刘姐' (MCN source reference)
  - Contains 'API' or '官方' (official source reference)
  - Contains '口径' (caliber/standard discussion)
  - Contains '50,234' or '50234' (official plays value)
  - Contains '120,000' or '120000' (MCN plays value for comparison)
  - Contains judgment/conclusion language
  - >= 3 '##' headings
"""
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "口径辨析报告.md"

    if not target.exists():
        print("FAILED: analysis/口径辨析报告.md not found")
        sys.exit(1)

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read file: {e}")
        sys.exit(1)

    errors = []

    # M2 check: must cite 刘姐 (MCN source)
    if "刘姐" not in content:
        errors.append("'刘姐' (MCN explanation source) not found")

    # M2 check: must cite API or official source
    if "API" not in content and "官方" not in content:
        errors.append("'API' or '官方' (official source) not found")

    # Must discuss 口径
    if "口径" not in content:
        errors.append("'口径' (statistical caliber) not found")

    # Must contain official plays value
    if "50,234" not in content and "50234" not in content:
        errors.append("official plays '50,234' or '50234' not found")

    # Must contain MCN plays value (for the comparison)
    if "120,000" not in content and "120000" not in content:
        errors.append("MCN plays '120,000' or '120000' not found")

    # Must contain judgment/conclusion language
    judgment_keywords = [
        "不成立", "推翻", "不可信", "更权威", "判断", "结论",
        "无效", "驳斥", "反驳", "证伪", "不符合", "矛盾"
    ]
    if not any(kw in content for kw in judgment_keywords):
        errors.append(
            f"judgment/conclusion language not found (expected one of: {judgment_keywords})"
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
