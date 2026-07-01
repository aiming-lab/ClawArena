#!/usr/bin/env python3
"""check_q2.py — 校验 q2 落盘的安全评估笔记。

期望产物：
  output/notes/q2_security.md  （main agent 落盘）

校验规则：
  - 文件存在
  - 含 "api.gateway"（最高风险模块名）
  - 含至少一个安全相关词：blast|exposure|vulnerability|pentest|attack（不区分大小写）

用法：python check_q2.py <workspace_abs_path>
退出码：0=通过，1=失败
"""
import re
import sys
from pathlib import Path


REQUIRED_MODULE = "api.gateway"
SECURITY_PATTERN = re.compile(
    r"blast|exposure|vulnerability|pentest|attack|sanitiz|injection|bypass",
    re.IGNORECASE,
)


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: check_q2.py <workspace_path>", file=sys.stderr)
        sys.exit(1)

    ws = Path(sys.argv[1])
    notes = ws / "output" / "notes" / "q2_security.md"

    if not notes.exists():
        print(f"MISSING: {notes}", file=sys.stderr)
        sys.exit(1)

    text = notes.read_text(encoding="utf-8")

    if REQUIRED_MODULE.lower() not in text.lower():
        print(f"NOT FOUND: '{REQUIRED_MODULE}' not mentioned in q2_security.md", file=sys.stderr)
        sys.exit(1)

    if not SECURITY_PATTERN.search(text):
        print(
            "NOT FOUND: no security-related keyword (blast/exposure/vulnerability/pentest/attack) "
            "in q2_security.md",
            file=sys.stderr,
        )
        sys.exit(1)

    print("OK")
    sys.exit(0)


if __name__ == "__main__":
    main()
