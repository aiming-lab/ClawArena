#!/usr/bin/env python3
"""
check_compliance_comparison.py — 验证 docs/compliance_history_comparison.md。

用法：
    python check_compliance_comparison.py <workspace_path>
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "docs" / "compliance_history_comparison.md"

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

    # 2. 包含 "2025-12-20"
    if "2025-12-20" not in content:
        print("FAILED: file does not contain '2025-12-20'")
        sys.exit(1)

    # 3. 包含 "非正式" 或 "informal"
    if not re.search(r'非正式|informal', content, re.IGNORECASE):
        print("FAILED: file does not contain '非正式' or 'informal'")
        sys.exit(1)

    # 4. 包含 "|"（Markdown 表格）
    if "|" not in content:
        print("FAILED: file does not contain '|' (Markdown table expected)")
        sys.exit(1)

    # 5. 包含追踪漏洞分析关键词
    if not re.search(r'关联|追踪|漏洞|断层', content):
        print("FAILED: file does not contain tracking-gap analysis keywords")
        sys.exit(1)

    # 6. 至少 2 个 "##" 开头的标题
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 2:
        print(f"FAILED: expected >= 2 '##' headings, found {len(headings)}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
