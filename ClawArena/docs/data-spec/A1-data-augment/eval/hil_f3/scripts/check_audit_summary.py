#!/usr/bin/env python3
"""
check_audit_summary.py — 验证 analysis/audit_summary.json。

用法：
    python check_audit_summary.py <workspace_path>
"""
import sys
import json
from pathlib import Path


REQUIRED_FIELDS = [
    "total_trades",
    "silenced_warnings",
    "near_miss_count",
    "violation_count",
    "max_delta_seconds",
    "first_anomaly_date",
]


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "audit_summary.json"

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

    # 5. violation_count == 1
    if data["violation_count"] != 1:
        print(f"FAILED: violation_count expected 1, got {data['violation_count']}")
        sys.exit(1)

    # 6. silenced_warnings == 5
    if data["silenced_warnings"] != 5:
        print(f"FAILED: silenced_warnings expected 5, got {data['silenced_warnings']}")
        sys.exit(1)

    # 7. first_anomaly_date 包含 "2026-03-10"
    if "2026-03-10" not in str(data["first_anomaly_date"]):
        print(
            f"FAILED: first_anomaly_date does not contain '2026-03-10', "
            f"got: {data['first_anomaly_date']}"
        )
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
