#!/usr/bin/env python3
"""check_updated_statement_log.py — Validates updated analysis/lin_xiaoya_statement_log.json for q23."""
import sys
import json
from pathlib import Path


def main():
    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "lin_xiaoya_statement_log.json"

    if not target.exists():
        print(f"FAILED: {target} not found")
        sys.exit(1)

    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: JSON parse error: {e}")
        sys.exit(1)

    errors = []

    # Must now be a JSON object with overall_assessment and statements
    if not isinstance(data, dict):
        print(
            "FAILED: lin_xiaoya_statement_log.json must be a JSON object (not array) "
            "with 'overall_assessment' and 'statements' fields after update"
        )
        sys.exit(1)

    # Check overall_assessment
    overall = data.get("overall_assessment")
    if overall != "partially_admitted":
        errors.append(
            f"overall_assessment must be 'partially_admitted', got '{overall}'"
        )

    # Check statements array
    if "statements" not in data:
        errors.append("Missing 'statements' key in lin_xiaoya_statement_log.json")
        if errors:
            for e in errors:
                print(f"FAILED: {e}")
            sys.exit(1)

    statements = data["statements"]
    if not isinstance(statements, list):
        errors.append("'statements' must be a JSON array")
        if errors:
            for e in errors:
                print(f"FAILED: {e}")
            sys.exit(1)

    # Must have exactly 4 entries
    if len(statements) != 4:
        errors.append(
            f"statements array must have exactly 4 entries (3 original + 1 admission), "
            f"got {len(statements)}"
        )
        if errors:
            for e in errors:
                print(f"FAILED: {e}")
            sys.exit(1)

    # First 3 entries must have status == "refuted"
    for i in range(3):
        entry = statements[i]
        if not isinstance(entry, dict):
            errors.append(f"Statement {i+1} must be a JSON object")
            continue
        if entry.get("status") != "refuted":
            errors.append(
                f"Statement {i+1} status must be 'refuted', got '{entry.get('status')}'"
            )

    # 4th entry must have status == "partial_admission"
    fourth = statements[3]
    if not isinstance(fourth, dict):
        errors.append("4th statement must be a JSON object")
    else:
        if fourth.get("status") != "partial_admission":
            errors.append(
                f"4th statement status must be 'partial_admission', got '{fourth.get('status')}'"
            )

        # 4th entry must contain the admission quote
        fourth_text = json.dumps(fourth, ensure_ascii=False)
        admission_keywords = ["我承认", "完整版薪资表", "误操作", "完整版", "承认", "修改"]
        if not any(kw in fourth_text for kw in admission_keywords):
            errors.append(
                "4th statement must contain the admission quote from linxiaoya-partial-admission.md "
                "(e.g., '我承认', '完整版薪资表', '误操作')"
            )

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
