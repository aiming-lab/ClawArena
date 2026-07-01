#!/usr/bin/env python3
"""
check_q26.py -- Verify docs/remediation_plan.json

M4 strict schema check.

Required schema:
  {
    "remediation_actions": [
      {
        "action_id": str (non-empty),
        "description": str (non-empty),
        "owner": str (non-empty),
        "deadline": str (non-empty),
        "acceptance_criteria": str (non-empty)
      },
      ... (minimum 5 actions)
    ],
    "estimated_completion_days": int (positive)
  }

Usage:
    python check_q26.py <workspace_path>
"""
import sys
import json
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    json_path = workspace / "docs" / "remediation_plan.json"
    if not json_path.exists():
        print("FAILED: docs/remediation_plan.json not found")
        sys.exit(1)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: cannot parse docs/remediation_plan.json: {e}")
        sys.exit(1)

    # Check top-level structure
    if not isinstance(data, dict):
        print(f"FAILED: expected a JSON object, got {type(data).__name__}")
        sys.exit(1)

    # Check remediation_actions is a list with >= 5 items
    actions = data.get("remediation_actions")
    if not isinstance(actions, list):
        errors.append("FAILED: 'remediation_actions' must be a list")
    elif len(actions) < 5:
        errors.append(
            f"FAILED: 'remediation_actions' must have >= 5 items, got {len(actions)}"
        )
    else:
        # Check each action has all required fields
        required_fields = ["action_id", "description", "owner", "deadline", "acceptance_criteria"]
        for i, action in enumerate(actions):
            if not isinstance(action, dict):
                errors.append(f"FAILED: action[{i}] must be a dict, got {type(action).__name__}")
                continue
            for field in required_fields:
                val = action.get(field)
                if val is None or (isinstance(val, str) and not val.strip()):
                    errors.append(
                        f"FAILED: action[{i}] missing or empty field '{field}'"
                    )

    # Check estimated_completion_days is a positive integer
    ecd = data.get("estimated_completion_days")
    if ecd is None:
        errors.append("FAILED: missing field 'estimated_completion_days'")
    elif not isinstance(ecd, int) or ecd < 1:
        errors.append(
            f"FAILED: 'estimated_completion_days' must be a positive integer, got {ecd!r}"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
