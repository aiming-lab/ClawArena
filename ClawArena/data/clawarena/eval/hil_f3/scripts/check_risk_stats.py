#!/usr/bin/env python3
"""
check_risk_stats.py — 验证 analysis/risk_window_stats.json。

用法：
    python check_risk_stats.py <workspace_path>
"""
import sys
import json
from pathlib import Path


REQUIRED_FIELDS = [
    "period_start",
    "period_end",
    "total_trades",
    "filled_anomalous",
    "near_miss_count",
    "rejected_count",
    "min_margin_to_close_secs",
]


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "risk_window_stats.json"

    # 1. 文件存在
    if not target.exists():
        print(f"FAILED: file does not exist: {target}")
        sys.exit(1)

    # 2. 合法 JSON，顶层是对象
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"FAILED: invalid JSON: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"FAILED: cannot read file: {e}")
        sys.exit(1)

    if not isinstance(data, dict):
        print("FAILED: JSON root must be an object")
        sys.exit(1)

    # 3. 包含所有必需字段
    missing = [f for f in REQUIRED_FIELDS if f not in data]
    if missing:
        print(f"FAILED: missing required fields: {missing}")
        sys.exit(1)

    # 4. near_miss_count == 2
    if data["near_miss_count"] != 2:
        print(f"FAILED: near_miss_count expected 2, got {data['near_miss_count']}")
        sys.exit(1)

    # 5. rejected_count == 1
    if data["rejected_count"] != 1:
        print(f"FAILED: rejected_count expected 1, got {data['rejected_count']}")
        sys.exit(1)

    # 6. min_margin_to_close_secs == 7 或 -7
    margin = data["min_margin_to_close_secs"]
    if abs(margin) != 7:
        print(
            f"FAILED: min_margin_to_close_secs expected 7 or -7, got {margin}"
        )
        sys.exit(1)

    # 7. period_start 包含 "2026-03-10"
    if "2026-03-10" not in str(data["period_start"]):
        print(
            f"FAILED: period_start does not contain '2026-03-10', "
            f"got: {data['period_start']}"
        )
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
