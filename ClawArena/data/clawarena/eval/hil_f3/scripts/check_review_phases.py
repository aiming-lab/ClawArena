#!/usr/bin/env python3
"""
check_review_phases.py — 验证 docs/two_phase_review_analysis.md。

用法：
    python check_review_phases.py <workspace_path>
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "docs" / "two_phase_review_analysis.md"

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

    # 2. 至少 3 个 "##" 开头的标题
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 3:
        print(f"FAILED: expected >= 3 '##' headings, found {len(headings)}")
        sys.exit(1)

    # 3. 阶段一：范围限定描述
    if not re.search(r'范围|scope|逐行', content, re.IGNORECASE):
        print("FAILED: file does not contain phase-1 scope description keywords")
        sys.exit(1)

    # 4. 阶段二：知识缺失描述
    if not re.search(r'盲点|知识|不知道|DST', content):
        print("FAILED: file does not contain phase-2 knowledge-gap keywords")
        sys.exit(1)

    # 5. 责任性质差异分析
    if not re.search(r'责任|accountability|差异', content, re.IGNORECASE):
        print("FAILED: file does not contain accountability/difference analysis keywords")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
