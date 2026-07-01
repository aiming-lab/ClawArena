#!/usr/bin/env python3
"""
check_near_miss_report.py — 验证 docs/near_miss_risk_report.md。

用法：
    python check_near_miss_report.py <workspace_path>
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "docs" / "near_miss_risk_report.md"

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

    # 2. 包含 "13" 和 "2026-03-10"
    if "13" not in content or "2026-03-10" not in content:
        print("FAILED: file does not contain both '13' and '2026-03-10' (Mar 10 13-sec entry)")
        sys.exit(1)

    # 3. 包含 "7" 和 "2026-03-11"
    if not re.search(r'\b7\b', content) or "2026-03-11" not in content:
        print("FAILED: file does not contain both '7' and '2026-03-11' (Mar 11 7-sec entry)")
        sys.exit(1)

    # 4. 包含 "5" 和 "2026-03-16"
    if not re.search(r'\b5\b', content) or "2026-03-16" not in content:
        print("FAILED: file does not contain both '5' and '2026-03-16' (Mar 16 5-sec violation)")
        sys.exit(1)

    # 5. 至少 3 个 "##" 开头的标题
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 3:
        print(f"FAILED: expected >= 3 '##' headings, found {len(headings)}")
        sys.exit(1)

    # 6. 提及 7 天延误
    if not re.search(r'7\s*天|7\s*day|seven\s*day', content, re.IGNORECASE):
        print("FAILED: file does not reference '7天' or '7 days' delay")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
