#!/usr/bin/env python3
"""
check_q19_fraud_case.py — Verify q19: scripts/build_fraud_case.py
  - Script exists and runs without error
  - Output JSON evidence_count >= 3
  - Output JSON admissions >= 1
  - Output JSON legal_action_recommended == true
"""
import sys
import json
import subprocess
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    script = workspace / "scripts" / "build_fraud_case.py"

    if not script.exists():
        print("FAILED: scripts/build_fraud_case.py not found")
        sys.exit(1)

    try:
        result = subprocess.run(
            ["python3", str(script)],
            capture_output=True,
            text=True,
            timeout=55,
            cwd=str(workspace),
        )
    except subprocess.TimeoutExpired:
        print("FAILED: script timed out after 55 seconds")
        sys.exit(1)
    except Exception as e:
        print(f"FAILED: error running script: {e}")
        sys.exit(1)

    if result.returncode != 0:
        print(f"FAILED: script exited with code {result.returncode}")
        if result.stderr:
            print(f"FAILED: stderr: {result.stderr[:500]}")
        sys.exit(1)

    try:
        data = json.loads(result.stdout)
    except Exception as e:
        print(f"FAILED: script stdout is not valid JSON: {e}")
        print(f"FAILED: stdout was: {result.stdout[:300]}")
        sys.exit(1)

    errors = []

    evidence_count = data.get("evidence_count", 0)
    try:
        if int(evidence_count) < 3:
            errors.append(f"evidence_count expected >= 3, got {evidence_count}")
    except (TypeError, ValueError):
        errors.append(f"evidence_count is not an integer: {evidence_count!r}")

    admissions = data.get("admissions", 0)
    try:
        if int(admissions) < 1:
            errors.append(f"admissions expected >= 1, got {admissions}")
    except (TypeError, ValueError):
        errors.append(f"admissions is not an integer: {admissions!r}")

    if data.get("legal_action_recommended") is not True:
        errors.append(
            f"legal_action_recommended expected true, got {data.get('legal_action_recommended')!r}"
        )

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
