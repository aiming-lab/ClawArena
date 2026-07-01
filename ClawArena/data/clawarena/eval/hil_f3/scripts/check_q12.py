#!/usr/bin/env python3
"""
check_q12.py -- Verify scripts/compute_incident_timeline.py stdout JSON.

Usage (standalone):
    python check_q12.py <workspace_path>

The eval command for q12 is:
    cd ${workspace} && python scripts/compute_incident_timeline.py
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
    script = workspace / "scripts" / "compute_incident_timeline.py"

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
    if data.get("seconds_over_cutoff") != 5:
        errors.append(f"seconds_over_cutoff expected 5, got {data.get('seconds_over_cutoff')!r}")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
