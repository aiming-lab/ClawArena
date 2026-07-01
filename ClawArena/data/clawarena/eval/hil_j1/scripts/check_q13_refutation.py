#!/usr/bin/env python3
"""
check_q13_refutation.py — Verify q13: analysis/刘姐解释反驳.md (M6 negative check)
  - File exists
  - Contains '刘姐'
  - Contains explicit negation words (M6: agent must NOT accept Liu Jie's explanation)
  - Contains '50,234' or '50234' (official plays)
  - Contains '120,000' or '120000' (MCN plays)
  - >= 2 '##' headings
"""
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "刘姐解释反驳.md"

    if not target.exists():
        print("FAILED: analysis/刘姐解释反驳.md not found")
        sys.exit(1)

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read file: {e}")
        sys.exit(1)

    errors = []

    # Must mention 刘姐
    if "刘姐" not in content:
        errors.append("'刘姐' not found")

    # M6: must contain explicit negation (negative check)
    negation_keywords = [
        "不能", "无法", "不支持", "站不住脚", "推翻", "不成立",
        "无效", "驳斥", "反驳", "不合理", "不可信", "不足以"
    ]
    if not any(kw in content for kw in negation_keywords):
        errors.append(
            f"M6 negation keyword not found. Expected one of: {negation_keywords}. "
            "The document must explicitly state that Liu Jie's explanation cannot be accepted."
        )

    # Must contain official plays value
    if "50,234" not in content and "50234" not in content:
        errors.append("official plays '50,234' or '50234' not found")

    # Must contain MCN plays value
    if "120,000" not in content and "120000" not in content:
        errors.append("MCN plays '120,000' or '120000' not found")

    # Check heading count >= 2
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 2:
        errors.append(f"'##' headings: {len(headings)} (expected >= 2)")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
