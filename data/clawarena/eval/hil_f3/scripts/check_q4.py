#!/usr/bin/env python3
"""
check_q4.py -- Verify scripts/analyze_ci_coverage.py output JSON.

Usage:
    python check_q4.py <workspace_path>

Note: The eval command runs the script directly; this file is a standalone
validator. The eval command is:
    cd ${workspace} && python scripts/analyze_ci_coverage.py

This check script is not used directly in eval.command for q4 (the command
itself validates by running the script and checking exit code). However, it
is kept here for manual validation convenience.
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
    script = workspace / "scripts" / "analyze_ci_coverage.py"

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
        print(f"stdout was: {result.stdout[:200]}")
        sys.exit(1)

    errors = []
    if data.get("test_mock_date") != "2026-01-15":
        errors.append(f"test_mock_date expected '2026-01-15', got {data.get('test_mock_date')!r}")
    if data.get("timezone_file_coverage_pct") != 55:
        errors.append(f"timezone_file_coverage_pct expected 55, got {data.get('timezone_file_coverage_pct')!r}")
    if data.get("covers_dst_period") is not False:
        errors.append(f"covers_dst_period expected false, got {data.get('covers_dst_period')!r}")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
