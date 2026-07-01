#!/usr/bin/env python3
"""
check_diagnostic_interp.py — 验证 docs/server_diagnostic_interpretation.md。

用法：
    python check_diagnostic_interp.py <workspace_path>
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "docs" / "server_diagnostic_interpretation.md"

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

    # 2. 包含票单号
    if not re.search(r'#?TK-20260317-4521', content):
        print("FAILED: file does not contain 'TK-20260317-4521'")
        sys.exit(1)

    # 3. 包含 "50ms" / "50 ms" / "50毫秒"
    if not re.search(r'50\s*ms|50毫秒', content, re.IGNORECASE):
        print("FAILED: file does not mention '50ms' (NTP drift threshold)")
        sys.exit(1)

    # 4. 包含 "127" 或 "line 127"
    if not re.search(r'127', content):
        print("FAILED: file does not contain '127' (code line reference)")
        sys.exit(1)

    # 5. 包含应用层结论关键词
    if not re.search(r'应用|application|代码层', content, re.IGNORECASE):
        print("FAILED: file does not contain application-layer conclusion keywords")
        sys.exit(1)

    # 6. 包含环境/基础设施相关词（否定环境差异假设的讨论）
    if not re.search(r'环境|environment', content, re.IGNORECASE):
        print("FAILED: file does not contain environment-related discussion")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
