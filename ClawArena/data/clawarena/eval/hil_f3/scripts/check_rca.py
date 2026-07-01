#!/usr/bin/env python3
"""
check_rca.py — 验证 docs/root_cause_analysis.md。

用法：
    python check_rca.py <workspace_path>
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "docs" / "root_cause_analysis.md"

    # 1. 文件存在且非空
    if not target.exists():
        print(f"FAILED: file does not exist: {target}")
        sys.exit(1)
    try:
        content = target.read_text(encoding="utf-8").strip()
    except Exception as e:
        print(f"FAILED: cannot read file: {e}")
        sys.exit(1)
    if not content:
        print("FAILED: file is empty")
        sys.exit(1)

    # 2. 至少 6 个 "##" 开头的标题
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 6:
        print(f"FAILED: expected >= 6 '##' headings, found {len(headings)}")
        sys.exit(1)

    # 3. 包含 "127"
    if "127" not in content:
        print("FAILED: file does not contain '127' (code line reference)")
        sys.exit(1)

    # 4. 包含 "2026-01-15"
    if "2026-01-15" not in content:
        print("FAILED: file does not contain '2026-01-15' (mock date reference)")
        sys.exit(1)

    # 5. 包含 "rule_007"
    if "rule_007" not in content:
        print("FAILED: file does not contain 'rule_007'")
        sys.exit(1)

    # 6. 包含 "7" 或 "七"
    if not re.search(r'\b7\b|七', content):
        print("FAILED: file does not contain '7' (7-day delay reference)")
        sys.exit(1)

    # 7. 包含 "60" 或 "60分钟"
    if not re.search(r'\b60\b', content):
        print("FAILED: file does not contain '60' (offset reference)")
        sys.exit(1)

    # 8. 至少包含两个维度关键词组合
    dimensions = [
        bool(re.search(r'代码|bug', content, re.IGNORECASE)),
        bool(re.search(r'测试|覆盖', content)),
        bool(re.search(r'静默|silence', content, re.IGNORECASE)),
        bool(re.search(r'审查|review', content, re.IGNORECASE)),
        bool(re.search(r'合规|compliance', content, re.IGNORECASE)),
        bool(re.search(r'递进|near.miss', content, re.IGNORECASE)),
    ]
    matched = sum(dimensions)
    if matched < 2:
        print(
            f"FAILED: expected >= 2 dimension keywords, found {matched}. "
            "Required: (代码/bug) + (测试/覆盖) + (静默/silence) + "
            "(审查/review) + (合规/compliance) + (递进/near-miss)"
        )
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
