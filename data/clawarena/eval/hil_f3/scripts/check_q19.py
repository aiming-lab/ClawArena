#!/usr/bin/env python3
"""
check_q19.py -- Verify scripts/build_postmortem.py stdout JSON.

Usage (standalone):
    python check_q19.py <workspace_path>

The eval command for q19 is:
    cd ${workspace} && python scripts/build_postmortem.py
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
    script = workspace / "scripts" / "build_postmortem.py"

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
    if data.get("offset_minutes") != 60:
        errors.append(f"offset_minutes expected 60, got {data.get('offset_minutes')!r}")

    contributing_factors = data.get("contributing_factors", [])
    if not isinstance(contributing_factors, list) or len(contributing_factors) < 3:
        errors.append(f"contributing_factors must be a list with >= 3 items, got {contributing_factors!r}")

    if data.get("timeline_days_from_dst_switch_to_violation") != 8:
        errors.append(f"timeline_days_from_dst_switch_to_violation expected 8, got {data.get('timeline_days_from_dst_switch_to_violation')!r}")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
