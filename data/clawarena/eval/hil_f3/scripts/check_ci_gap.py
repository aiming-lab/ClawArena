#!/usr/bin/env python3
"""
check_ci_gap.py — 验证 docs/ci_test_gap_analysis.md。

用法：
    python check_ci_gap.py <workspace_path>
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "docs" / "ci_test_gap_analysis.md"

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

    # 2. 包含 "2026-01-15"
    if "2026-01-15" not in content:
        print("FAILED: file does not contain '2026-01-15'")
        sys.exit(1)

    # 3. 包含 "DST" 或 "夏令时"
    if "DST" not in content and "夏令时" not in content:
        print("FAILED: file does not contain 'DST' or '夏令时'")
        sys.exit(1)

    # 4. 包含 "55" 或 "55%"
    if "55" not in content:
        print("FAILED: file does not contain '55' (branch coverage reference)")
        sys.exit(1)

    # 5. 至少 2 个 "##" 开头的标题行
    heading_lines = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(heading_lines) < 2:
        print(f"FAILED: expected >= 2 '##' headings, found {len(heading_lines)}")
        sys.exit(1)

    # 6. 至少两类缺口关键词
    gap_categories = [
        bool(re.search(r'边界|boundary|DST边界', content)),
        bool(re.search(r'休市|market|11:30', content)),
        bool(re.search(r'累积|多日|consecutive', content)),
    ]
    if sum(gap_categories) < 2:
        print(
            "FAILED: file must contain keywords from at least 2 of the 3 gap "
            "categories (boundary/market-close/consecutive)"
        )
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
