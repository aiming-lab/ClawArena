#!/usr/bin/env python3
"""
check_ci_remediation.py — 验证 docs/ci_remediation_tests.md。

用法：
    python check_ci_remediation.py <workspace_path>
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "docs" / "ci_remediation_tests.md"

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

    # 3. 包含 "2026-03-10"
    if "2026-03-10" not in content:
        print("FAILED: file does not contain '2026-03-10' (DST mock date)")
        sys.exit(1)

    # 4. 包含 "11:30" 或 "休市"
    if not re.search(r'11:30|休市', content):
        print("FAILED: file does not contain '11:30' or '休市' (market-close test)")
        sys.exit(1)

    # 5. 包含 mock 关键词
    if not re.search(r'mock|Mock|@mock\.patch', content):
        print("FAILED: file does not contain mock-related keywords")
        sys.exit(1)

    # 6. 包含参数化测试关键词
    if not re.search(r'parametrize|参数|pytest\.mark', content, re.IGNORECASE):
        print("FAILED: file does not contain parametrize/pytest reference")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
