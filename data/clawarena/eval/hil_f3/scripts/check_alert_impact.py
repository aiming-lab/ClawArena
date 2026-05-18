#!/usr/bin/env python3
"""
check_alert_impact.py — 验证 docs/alert_silence_impact_report.md。

用法：
    python check_alert_impact.py <workspace_path>
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "docs" / "alert_silence_impact_report.md"

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

    errors = []

    # 2. 必须包含 "rule_007"（规则名称，而非仅 "rule" 和 "silence"）
    if "rule_007" not in content:
        errors.append("FAILED: file does not contain 'rule_007'")

    # 3. 必须含独立数字 7（7 天静默期，word-boundary 检查）
    if not re.search(r'\b7\b', content):
        errors.append("FAILED: file does not contain standalone number '7' (7-day silence period)")

    # 4. 必须含独立数字 5（被静默的 5 条告警，word-boundary 检查）
    if not re.search(r'\b5\b', content):
        errors.append("FAILED: file does not contain standalone number '5' (5 silenced alerts count)")

    # 5. 必须说明 expires=null / 从未过期
    if not re.search(r'null|never\s+expired|no\s+expir|expires.*null|expires.*never', content, re.IGNORECASE):
        errors.append("FAILED: file does not state 'expires=null' or 'never expired'")

    # 6. 必须包含 "2026-03-10"（near-miss 起始日期）
    if "2026-03-10" not in content:
        errors.append("FAILED: file does not contain '2026-03-10'")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
