#!/usr/bin/env python3
"""
check_accountability_matrix.py — 验证 docs/stakeholder_accountability_matrix.json。

用法：
    python check_accountability_matrix.py <workspace_path>
"""
import sys
import json
from pathlib import Path


REQUIRED_ENTRY_FIELDS = {
    "role_key",
    "role_title",
    "direct_contribution",
    "recommended_action",
}

REQUIRED_ROLE_KEYS = [
    "zhaolei_developer",
    "xiaozhou_reviewer",
    "zhaolei_rule_creator",
    "zhang_compliance",
]


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "docs" / "stakeholder_accountability_matrix.json"

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

    # 3. 数组长度 == 4
    if len(data) != 4:
        print(f"FAILED: expected exactly 4 stakeholder entries, got {len(data)}")
        sys.exit(1)

    # 4. 每个元素包含必需字段
    for i, entry in enumerate(data):
        missing = REQUIRED_ENTRY_FIELDS - set(entry.keys())
        if missing:
            print(f"FAILED: entry {i} missing fields: {sorted(missing)}")
            sys.exit(1)

    role_map = {e["role_key"]: e for e in data}

    # 5–8. 检查四个必需 role_key
    for rk in REQUIRED_ROLE_KEYS:
        if rk not in role_map:
            print(f"FAILED: no entry with role_key='{rk}'")
            sys.exit(1)

    # 9. zhaolei_developer 与 zhaolei_rule_creator 的 direct_contribution 不完全相同
    dev_contrib  = role_map["zhaolei_developer"]["direct_contribution"]
    rule_contrib = role_map["zhaolei_rule_creator"]["direct_contribution"]
    if dev_contrib == rule_contrib:
        print(
            "FAILED: zhaolei_developer and zhaolei_rule_creator have identical "
            "direct_contribution — they must be distinct"
        )
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
