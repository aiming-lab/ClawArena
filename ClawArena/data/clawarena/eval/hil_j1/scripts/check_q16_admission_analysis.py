#!/usr/bin/env python3
"""
check_q16_admission_analysis.py — Verify q16: analysis/承认记录分析.md
  - File exists
  - Contains exact string '内部估算' (exact match, M2 requirement)
  - Contains '刘姐'
  - Contains contradiction/admission analysis keywords
  - >= 3 '##' headings
"""
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "承认记录分析.md"

    if not target.exists():
        print("FAILED: analysis/承认记录分析.md not found")
        sys.exit(1)

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read file: {e}")
        sys.exit(1)

    errors = []

    # Must contain exact '内部估算' (M2: MCN self-admission)
    if "内部估算" not in content:
        errors.append("exact string '内部估算' not found (required for M2 admission check)")

    # Must mention 刘姐
    if "刘姐" not in content:
        errors.append("'刘姐' not found")

    # Must contain contradiction/admission analysis
    analysis_keywords = ["矛盾", "承认", "推翻", "不一致", "前后", "口径"]
    if not any(kw in content for kw in analysis_keywords):
        errors.append(
            f"contradiction/admission analysis keyword not found (expected one of: {analysis_keywords})"
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
