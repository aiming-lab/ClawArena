#!/usr/bin/env python3
"""
check_timeline_json.py — 验证 docs/incident_timeline.json。

用法：
    python check_timeline_json.py <workspace_path>
"""
import sys
import json
from pathlib import Path


REQUIRED_FIELDS = [
    "pr_merged",
    "rule_007_created",
    "dst_switched",
    "first_warn_silenced",
    "violation_occurred",
]


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "docs" / "incident_timeline.json"

    # 1. 文件存在
    if not target.exists():
        print(f"FAILED: file does not exist: {target}")
        sys.exit(1)

    # 2. 合法 JSON
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

    # 3. 包含全部 5 个必需字段
    missing = [f for f in REQUIRED_FIELDS if f not in data]
    if missing:
        print(f"FAILED: missing required fields: {missing}")
        sys.exit(1)

    # 4. pr_merged 包含 "2026-03-10"
    if "2026-03-10" not in str(data["pr_merged"]):
        print(f"FAILED: pr_merged does not contain '2026-03-10', got: {data['pr_merged']}")
        sys.exit(1)

    # 5. rule_007_created 包含 "2025-12-15"
    if "2025-12-15" not in str(data["rule_007_created"]):
        print(
            f"FAILED: rule_007_created does not contain '2025-12-15', "
            f"got: {data['rule_007_created']}"
        )
        sys.exit(1)

    # 6. dst_switched 包含 "2026-03-08"
    if "2026-03-08" not in str(data["dst_switched"]):
        print(
            f"FAILED: dst_switched does not contain '2026-03-08', "
            f"got: {data['dst_switched']}"
        )
        sys.exit(1)

    # 7. violation_occurred 包含 "2026-03-16"
    if "2026-03-16" not in str(data["violation_occurred"]):
        print(
            f"FAILED: violation_occurred does not contain '2026-03-16', "
            f"got: {data['violation_occurred']}"
        )
        sys.exit(1)

    # 8. 至少 3 个字段的值含 "+" 或 "+08:00"（ISO 8601 时区）
    tz_count = sum(
        1 for f in REQUIRED_FIELDS if "+" in str(data.get(f, ""))
    )
    if tz_count < 3:
        print(
            f"FAILED: expected >= 3 fields with ISO 8601 timezone ('+'), "
            f"found {tz_count}"
        )
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
