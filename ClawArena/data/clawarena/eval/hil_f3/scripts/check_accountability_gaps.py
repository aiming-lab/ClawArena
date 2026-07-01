#!/usr/bin/env python3
"""
check_accountability_gaps.py — 验证 docs/system_accountability_gaps.md。

用法：
    python check_accountability_gaps.py <workspace_path>
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "docs" / "system_accountability_gaps.md"

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

    # 2. 至少 2 个 "##" 开头的标题
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 2:
        print(f"FAILED: expected >= 2 '##' headings, found {len(headings)}")
        sys.exit(1)

    # 3. 漏洞一：rule_007 / 静默规则 / silence
    if not re.search(r'rule_007|静默规则|silence', content, re.IGNORECASE):
        print("FAILED: file does not reference rule_007 or silence-related gap")
        sys.exit(1)

    # 4. 漏洞二：非正式 / informal / 入档
    if not re.search(r'非正式|informal|入档', content, re.IGNORECASE):
        print("FAILED: file does not reference informal/undocumented gap")
        sys.exit(1)

    # 5. 改进建议
    if not re.search(r'改进|建议|recommendation', content, re.IGNORECASE):
        print("FAILED: file does not contain improvement recommendations")
        sys.exit(1)

    # 6. 根因分析
    if not re.search(r'根因|原因|cause', content, re.IGNORECASE):
        print("FAILED: file does not contain root-cause analysis")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
