#!/usr/bin/env python3
"""
check_q3.py — Verify docs/contradiction_map.json for hil_g4.

The agent must create docs/contradiction_map.json identifying at least 3 contradictions
in the Zhang Tao wrongful termination case:
  C1: PIP compliance timeline vs labor law requirement (30-day plan vs 60-day minimum)
  C2: HR 1-on-1 records vs what actually occurred (to be revealed by upd1)
  C3: Written warning count discrepancy (3 claimed vs 1 documented)

Schema: {"contradictions": [{"id": str, "c_type": str, "source_a": str,
         "source_b": str, "description": str}]}

Usage:
    python check_q3.py <workspace_path>
"""
import sys
import json
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    # Check file exists
    json_path = workspace / "docs" / "contradiction_map.json"
    if not json_path.exists():
        print(f"FAILED: docs/contradiction_map.json not found")
        sys.exit(1)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: cannot parse docs/contradiction_map.json: {e}")
        sys.exit(1)

    # Must have "contradictions" key
    if "contradictions" not in data:
        errors.append("FAILED: missing 'contradictions' key in JSON")
    else:
        contradictions = data["contradictions"]

        # Must be a list with >= 3 items
        if not isinstance(contradictions, list) or len(contradictions) < 3:
            errors.append(
                f"FAILED: 'contradictions' must be a list with >= 3 items, "
                f"got {len(contradictions) if isinstance(contradictions, list) else type(contradictions).__name__}"
            )
        else:
            # Each item must have required fields
            required_fields = {"id", "source_a", "source_b", "description"}
            for i, item in enumerate(contradictions):
                missing = required_fields - set(item.keys())
                if missing:
                    errors.append(
                        f"FAILED: contradiction[{i}] missing fields: {missing}"
                    )

            # Must reference actual workspace source files
            all_text = json.dumps(contradictions).lower()
            source_keywords = [
                "pip-email-chain", "labor-law-reference", "employee-hr-file",
                "calendar-1on1-history", "todo-pip-followups",
                "pip_email_chain", "labor_law_reference", "employee_hr_file",
                "calendar_1on1_history",
            ]
            found_sources = [kw for kw in source_keywords if kw in all_text]
            if len(found_sources) < 2:
                errors.append(
                    "FAILED: contradictions must reference at least 2 workspace source files "
                    "(e.g. pip-email-chain.md, labor-law-reference.md, employee-hr-file.md, "
                    "calendar-1on1-history.md). "
                    f"Found references to: {found_sources}"
                )

            # Must include a contradiction about PIP timeline or warning count
            pip_timeline_found = any(
                re.search(r'pip|60.{0,20}day|30.{0,20}day|timeline|期限|改进计划', str(item).lower())
                for item in contradictions
            )
            warning_count_found = any(
                re.search(r'warning|warn|警告|书面', str(item).lower())
                for item in contradictions
            )
            if not (pip_timeline_found or warning_count_found):
                errors.append(
                    "FAILED: contradictions must include at least one about PIP timeline "
                    "or written warning count discrepancy"
                )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
