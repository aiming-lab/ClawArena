#!/usr/bin/env python3
"""
check_window_violations.py — 验证 analysis/trade_window_violations.json。

用法：
    python check_window_violations.py <workspace_path>
"""
import sys
import json
from pathlib import Path


REQUIRED_ENTRY_FIELDS = {
    "order_id",
    "actual_time",
    "delta_to_close_secs",
    "status",
    "near_miss",
}


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "trade_window_violations.json"

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

    # 3. 数组长度 >= 3
    if len(data) < 3:
        print(f"FAILED: expected >= 3 entries, got {len(data)}")
        sys.exit(1)

    # 4. 每个元素包含必需字段
    for i, entry in enumerate(data):
        missing = REQUIRED_ENTRY_FIELDS - set(entry.keys())
        if missing:
            print(f"FAILED: entry {i} missing fields: {sorted(missing)}")
            sys.exit(1)

    # 5. 至少 2 个元素的 near_miss 为 True
    near_miss_entries = [e for e in data if e.get("near_miss") is True]
    if len(near_miss_entries) < 2:
        print(
            f"FAILED: expected >= 2 entries with near_miss=True, "
            f"got {len(near_miss_entries)}"
        )
        sys.exit(1)

    # 6. 至少 1 个元素的 status 为 "REJECTED"
    rejected = [e for e in data if e.get("status") == "REJECTED"]
    if not rejected:
        print("FAILED: no entry with status='REJECTED' found")
        sys.exit(1)

    # 7. 有元素的 delta_to_close_secs 接近 -13 或 -7
    deltas = []
    for e in data:
        try:
            deltas.append(float(e["delta_to_close_secs"]))
        except (TypeError, ValueError):
            pass

    has_near_13 = any(abs(d - (-13)) <= 2 for d in deltas)
    has_near_7  = any(abs(d - (-7))  <= 2 for d in deltas)
    if not (has_near_13 or has_near_7):
        print(
            f"FAILED: no entry with delta_to_close_secs near -13 or -7. "
            f"Actual deltas: {deltas}"
        )
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
