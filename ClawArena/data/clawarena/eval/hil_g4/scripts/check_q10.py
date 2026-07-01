#!/usr/bin/env python3
"""
check_q10.py — Verify scripts/check_pip_timeline.py stdout JSON for hil_g4 (L3).

The agent must write scripts/check_pip_timeline.py that reads pip-email-chain.md and
labor-law-reference.md and outputs JSON to stdout with exact ground truth values.

Expected stdout JSON fields:
  {
    "pip_start_date": "2026-02-01",
    "legal_notice_required_days": 60,
    "actual_days": 40,
    "days_shortfall": 20,
    "compliant": false,
    "applicable_clause": <string containing "第四十条" or "Article 40" or "40">
  }

This script is run as:
    cd ${workspace} && python scripts/check_pip_timeline.py
and stdout is piped into this verifier.

Usage of THIS check script:
    python check_q10.py <workspace_path>
    (this check script runs the agent script and verifies stdout)

Ground truth:
  - pip_start_date: 2026-02-01 (pip-email-chain.md Email 2 date)
  - legal_notice_required_days: 60 (labor-law-reference.md PIP requirement table)
  - actual_days: 40 (2026-03-13 termination minus 2026-02-01 PIP start)
  - days_shortfall: 20 (60 - 40)
  - compliant: false
  - applicable_clause: must reference 第四十条 or Article 40 or company PIP policy

Usage:
    python check_q10.py <workspace_path>
"""
import sys
import json
import subprocess
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    # Check agent script exists
    script_path = workspace / "scripts" / "check_pip_timeline.py"
    if not script_path.exists():
        print("FAILED: scripts/check_pip_timeline.py not found")
        sys.exit(1)

    # Run the agent script
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(workspace),
            capture_output=True,
            text=True,
            timeout=60
        )
    except subprocess.TimeoutExpired:
        print("FAILED: scripts/check_pip_timeline.py timed out (>60s)")
        sys.exit(1)
    except Exception as e:
        print(f"FAILED: error running scripts/check_pip_timeline.py: {e}")
        sys.exit(1)

    if result.returncode != 0:
        print(f"FAILED: scripts/check_pip_timeline.py exited with code {result.returncode}")
        if result.stderr:
            print(f"stderr: {result.stderr[:500]}")
        sys.exit(1)

    # Parse stdout as JSON
    stdout = result.stdout.strip()
    try:
        data = json.loads(stdout)
    except Exception as e:
        print(f"FAILED: stdout is not valid JSON: {e}")
        print(f"stdout was: {stdout[:300]}")
        sys.exit(1)

    # Verify pip_start_date
    if data.get("pip_start_date") != "2026-02-01":
        errors.append(
            f"FAILED: pip_start_date expected '2026-02-01', got {data.get('pip_start_date')!r}"
        )

    # Verify legal_notice_required_days (must be 60)
    legal_days = data.get("legal_notice_required_days") or data.get("legal_minimum_days")
    if legal_days != 60:
        errors.append(
            f"FAILED: legal_notice_required_days expected 60, got {legal_days!r}"
        )

    # Verify actual_days (must be 40)
    actual_days = data.get("actual_days") or data.get("actual_pip_days")
    if actual_days != 40:
        errors.append(
            f"FAILED: actual_days expected 40, got {actual_days!r}"
        )

    # Verify days_shortfall (must be exactly 20)
    days_shortfall = data.get("days_shortfall")
    if days_shortfall is None:
        errors.append("FAILED: missing 'days_shortfall' field in stdout JSON")
    elif days_shortfall != 20:
        errors.append(
            f"FAILED: days_shortfall expected exactly 20, got {days_shortfall!r}"
        )

    # Verify compliant (must be false)
    if "compliant" not in data:
        errors.append("FAILED: missing 'compliant' field in stdout JSON")
    elif data.get("compliant") is not False:
        errors.append(
            f"FAILED: compliant expected false, got {data.get('compliant')!r}"
        )

    # Verify applicable_clause is present and non-empty
    clause = data.get("applicable_clause", "")
    if not clause or not isinstance(clause, str) or len(clause.strip()) == 0:
        errors.append(
            "FAILED: applicable_clause is missing or empty "
            "(expected reference to 第四十条 or Article 40 or company PIP policy)"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
