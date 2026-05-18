#!/usr/bin/env python3
"""
check_q15_admission_script.py — Verify q15: scripts/analyze_admission_evidence.py
  - Script exists and runs without error
  - Output JSON liu_jie_admitted_estimate == true
  - Output JSON quote_found == true
  - Output JSON key_quote contains '内部估算'
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
    script = workspace / "scripts" / "analyze_admission_evidence.py"

    if not script.exists():
        print("FAILED: scripts/analyze_admission_evidence.py not found")
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

    if data.get("liu_jie_admitted_estimate") is not True:
        errors.append(
            f"liu_jie_admitted_estimate expected true, got {data.get('liu_jie_admitted_estimate')!r}"
        )

    if data.get("quote_found") is not True:
        errors.append(f"quote_found expected true, got {data.get('quote_found')!r}")

    key_quote = data.get("key_quote", "")
    if "内部估算" not in str(key_quote):
        errors.append(
            f"key_quote must contain '内部估算', got: {key_quote!r}"
        )

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
