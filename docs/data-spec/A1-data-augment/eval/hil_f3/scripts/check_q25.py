#!/usr/bin/env python3
"""
check_q25.py -- Verify scripts/validate_fix_readiness.py stdout JSON.

The eval command for q25 is:
    cd ${workspace} && python scripts/validate_fix_readiness.py

Usage (standalone):
    python check_q25.py <workspace_path>
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
    script = workspace / "scripts" / "validate_fix_readiness.py"

    if not script.exists():
        print(f"FAILED: {script} not found")
        sys.exit(1)

    try:
        result = subprocess.run(
            ["python", str(script)],
            cwd=str(workspace),
            capture_output=True,
            text=True,
            timeout=30
        )
    except Exception as e:
        print(f"FAILED: error running script: {e}")
        sys.exit(1)

    if result.returncode != 0:
        print(f"FAILED: script exited with code {result.returncode}")
        if result.stderr:
            print(result.stderr[:500])
        sys.exit(1)

    try:
        data = json.loads(result.stdout)
    except Exception as e:
        print(f"FAILED: stdout is not valid JSON: {e}")
        sys.exit(1)

    errors = []

    # fix_ready must be false (fixes not yet applied)
    if data.get("fix_ready") is not False:
        errors.append(f"fix_ready expected false (fixes not yet applied to workspace), got {data.get('fix_ready')!r}")

    # All individual checks should also be false
    for field in ["rule_007_deleted", "line_127_fixed", "dst_test_added", "coverage_improved"]:
        if field not in data:
            errors.append(f"missing field: '{field}'")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
