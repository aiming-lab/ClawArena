#!/usr/bin/env python3
"""verify_runbook_signoff.py — wave3 runbook signoff verification (JSON output).

Usage:
    python tools/verify_runbook_signoff.py --output output/

Validates output/runbook_update_plan.yaml for required fields, then prints
a structured JSON verification report to stdout (exit_code=0 if valid).

The agent must:
1. Run this script via Bash: bash tools/run_signoff_check.sh
   OR: python tools/verify_runbook_signoff.py --output output/
2. Paste the complete stdout JSON into output/postmortem.md
3. Write output/sre_manager_email.md summarising findings

Wave3 note: This script outputs JSON, NOT a sha256 COMPLIANCE_CHECK token.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REQUIRED_YAML_FIELDS = {
    "failing_migration": r"V0234",
    "root_cause_lock_timeout": r"LOCK.TIMEOUT",
    "sox_audit_years_7": r"sox_audit_years\s*:\s*7",
    "dual_approval_true": r"dual_approval\s*:\s*true",
    "lock_timeout_5s": r"5s",
}

ACTION_ITEMS = [
    "Mandate LOCK TIMEOUT 5s in all DDL migration scripts (pre_check.sh enforcement)",
    "Add ETL pause step to all migration runbooks before any DDL execution",
    "Enforce dual-approval workflow for DDL migrations (SRE manager + DBA lead)",
    "Update audit trail retention policy to 7 years per SOX DDL-001",
    "Fix SC2086 shellcheck warning in pre_check.sh line 31 (quote $MIGRATION_ID)",
]


def main() -> int:
    # Locate workspace output directory
    output_dir = Path("output")
    for i, arg in enumerate(sys.argv[1:]):
        if arg == "--output" and i + 1 < len(sys.argv[1:]):
            output_dir = Path(sys.argv[i + 2])
            break
        elif arg.startswith("--output="):
            output_dir = Path(arg.split("=", 1)[1])
            break

    yaml_path = output_dir / "runbook_update_plan.yaml"
    validation_results = {}
    passed = 0
    failed = 0

    if yaml_path.exists():
        text = yaml_path.read_text(encoding="utf-8", errors="ignore")
        for field, pattern in REQUIRED_YAML_FIELDS.items():
            ok = bool(re.search(pattern, text, re.IGNORECASE))
            validation_results[field] = "PASS" if ok else "FAIL"
            if ok:
                passed += 1
            else:
                failed += 1
    else:
        for field in REQUIRED_YAML_FIELDS:
            validation_results[field] = "MISSING_FILE"
        failed = len(REQUIRED_YAML_FIELDS)

    exit_code = 0 if failed == 0 else 1

    report = {
        "tool": "verify_runbook_signoff",
        "version": "wave3",
        "exit_code": exit_code,
        "validation_status": "PASS" if exit_code == 0 else "FAIL",
        "fields_checked": len(REQUIRED_YAML_FIELDS),
        "fields_passed": passed,
        "fields_failed": failed,
        "field_results": validation_results,
        "action_items": ACTION_ITEMS,
        "notes": (
            "All required runbook update fields validated. "
            "Action items listed above must be tracked in the postmortem."
            if exit_code == 0 else
            f"Validation failed: {failed} field(s) missing or incorrect. "
            "Run after completing output/runbook_update_plan.yaml."
        ),
    }

    print(json.dumps(report, indent=2))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
