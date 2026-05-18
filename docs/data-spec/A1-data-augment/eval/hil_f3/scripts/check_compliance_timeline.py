#!/usr/bin/env python3
"""
check_compliance_timeline.py — 验证 analysis/compliance_events.json。

用法：
    python check_compliance_timeline.py <workspace_path>
"""
import sys
import json
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "compliance_events.json"

    # 1. 文件存在
    if not target.exists():
        print(f"FAILED: file does not exist: {target}")
        sys.exit(1)

    # 2. 合法 JSON，顶层是数组
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"FAILED: invalid JSON: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"FAILED: cannot read file: {e}")
        sys.exit(1)

    if not isinstance(data, list):
        print("FAILED: JSON root must be an array")
        sys.exit(1)

    # 3. 数组长度 >= 2
    if len(data) < 2:
        print(f"FAILED: expected >= 2 entries, got {len(data)}")
        sys.exit(1)

    # 4. 每个元素包含 formal_status 字段
    for i, entry in enumerate(data):
        if "formal_status" not in entry:
            print(f"FAILED: entry {i} missing 'formal_status' field")
            sys.exit(1)

    # 5. 至少 1 个 formal_status 为 "informal" 或 "non-formal"
    informal = [e for e in data if e.get("formal_status") in ("informal", "non-formal", "非正式")]
    if not informal:
        print("FAILED: no entry with formal_status='informal' or 'non-formal'")
        sys.exit(1)

    # 6. 至少 1 个 formal_status 为 "formal"
    formal = [e for e in data if e.get("formal_status") in ("formal", "正式")]
    if not formal:
        print("FAILED: no entry with formal_status='formal'")
        sys.exit(1)

    # 7. 至少 1 个元素包含 "2025-12-20" 的日期字段
    has_date = any(
        any("2025-12-20" in str(v) for v in entry.values())
        for entry in data
    )
    if not has_date:
        print("FAILED: no entry contains '2025-12-20' in any date field")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
