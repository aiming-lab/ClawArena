#!/usr/bin/env python3
"""
check_compliance_response.py — 验证 docs/compliance_response_draft.md。

用法：
    python check_compliance_response.py <workspace_path>
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "docs" / "compliance_response_draft.md"

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

    # 2. 至少 4 个 "##" 开头的标题
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 4:
        print(f"FAILED: expected >= 4 '##' headings, found {len(headings)}")
        sys.exit(1)

    # 3. 包含 "12" 或 "十二"
    if not re.search(r'\b12\b|十二', content):
        print("FAILED: file does not contain '12' (12 test cases)")
        sys.exit(1)

    # 4. 包含 "rule_007"
    if "rule_007" not in content:
        print("FAILED: file does not contain 'rule_007'")
        sys.exit(1)

    # 5. 包含 "127" 或 "scheduler"
    if not re.search(r'127|scheduler', content, re.IGNORECASE):
        print("FAILED: file does not contain '127' or 'scheduler' (code fix reference)")
        sys.exit(1)

    # 6. 包含报告核心内容关键词
    if not re.search(r'根因|时间线|整改', content):
        print("FAILED: file does not contain core report keywords (根因/时间线/整改)")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
