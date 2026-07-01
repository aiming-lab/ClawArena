#!/usr/bin/env python3
"""
check_remediation_schema.py — 验证 docs/remediation_plan.json。

用法：
    python check_remediation_schema.py <workspace_path>
"""
import sys
import json
import re
from pathlib import Path


REQUIRED_ENTRY_FIELDS = {
    "action_id",
    "title",
    "owner",
    "deadline",
    "acceptance_criteria",
}


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "docs" / "remediation_plan.json"

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

    # 3. 数组长度 == 6
    if len(data) != 6:
        print(f"FAILED: expected exactly 6 action items, got {len(data)}")
        sys.exit(1)

    # 4. 每个元素包含必需字段
    for i, entry in enumerate(data):
        missing = REQUIRED_ENTRY_FIELDS - set(entry.keys())
        if missing:
            print(f"FAILED: entry {i} missing fields: {sorted(missing)}")
            sys.exit(1)

    criteria_texts = [str(e.get("acceptance_criteria", "")) for e in data]
    title_texts    = [str(e.get("title", "")) for e in data]

    # 5. acceptance_criteria 含 "rule_007" 或 "告警规则"
    has_rule007 = any(
        re.search(r'rule_007|告警规则', c) for c in criteria_texts
    )
    if not has_rule007:
        print("FAILED: no acceptance_criteria contains 'rule_007' or '告警规则'")
        sys.exit(1)

    # 6. acceptance_criteria 含 "12" 或 "十二"
    has_12 = any(re.search(r'\b12\b|十二', c) for c in criteria_texts)
    if not has_12:
        print("FAILED: no acceptance_criteria contains '12' or '十二' (DST test cases)")
        sys.exit(1)

    # 7. title 或 acceptance_criteria 含 "合规" / "入档" / "追踪"
    all_texts = title_texts + criteria_texts
    has_compliance = any(re.search(r'合规|入档|追踪', t) for t in all_texts)
    if not has_compliance:
        print(
            "FAILED: no title or acceptance_criteria contains "
            "'合规' / '入档' / '追踪'"
        )
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
