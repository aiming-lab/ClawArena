#!/usr/bin/env python3
"""
check_q26_evidence_strength.py — Verify q26: analysis/诉讼证据强度评估.md (M2)
  - File exists
  - Contains references to all four evidence types
  - Contains '承认' or '内部估算' (Liu Jie's admission — M2 authoritative source judgment)
  - Contains strength assessment / ranking language
  - >= 3 '##' headings
"""
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "诉讼证据强度评估.md"

    if not target.exists():
        print("FAILED: analysis/诉讼证据强度评估.md not found")
        sys.exit(1)

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read file: {e}")
        sys.exit(1)

    errors = []

    # Check four evidence types are covered
    evidence_keywords = [
        ["官方后台", "官方数据", "后台数据", "50,234", "50234"],    # official data
        ["API", "文档", "口径"],                                      # API documentation
        ["承认", "内部估算", "口头", "刘姐"],                         # admission
        ["合同", "条款", "违约", "截图"],                             # contract breach
    ]
    for i, keywords in enumerate(evidence_keywords):
        if not any(kw in content for kw in keywords):
            errors.append(
                f"evidence type {i+1} not found (expected one of: {keywords})"
            )

    # M2: must contain Liu Jie admission reference
    if "承认" not in content and "内部估算" not in content:
        errors.append("'承认' or '内部估算' (Liu Jie admission reference) not found")

    # Check strength assessment / ranking language
    strength_keywords = ["最关键", "最强", "强度", "评估", "排序", "重要", "关键", "核心"]
    if not any(kw in content for kw in strength_keywords):
        errors.append(
            f"strength assessment/ranking language not found (expected one of: {strength_keywords})"
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
