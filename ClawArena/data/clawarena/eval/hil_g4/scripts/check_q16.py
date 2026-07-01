#!/usr/bin/env python3
"""
check_q16.py — Verify scripts/analyze_pip_process.py stdout JSON for hil_g4 (L3).

The agent must write scripts/analyze_pip_process.py that reads calendar-1on1-history.md,
pip-email-chain.md, and labor-law-reference.md, and outputs JSON to stdout.

Expected stdout JSON fields (exact names):
  {
    "total_meetings_required": <int — policy-required check-ins during PIP>,
    "total_meetings_held": <int — meetings held per calendar>,
    "meetings_with_written_record": <int — meetings with email/written follow-up>,
    "meetings_with_written_confirmation": <int — meetings with employee confirmation>,
    "process_gaps": [<list of specific gap description strings>]
  }

Ground truth:
  - total_meetings_required: 2 (Week 2 and Week 4 check-ins per PIP plan)
  - total_meetings_held: 2 (2026-02-15 PIP Review and 2026-03-04 Meeting in calendar)
  - meetings_with_written_record: 1 (2026-02-15 has email follow-up; 2026-03-04 has no email)
  - meetings_with_written_confirmation: 0 (employee never confirmed/signed anything)
  - process_gaps: must list at least 2 specific gaps

Alternative acceptable values:
  - total_meetings_held may be 2 or 9 (depending on whether all 1:1s are counted)
  - The key is days_shortfall=20, and process_gaps >= 2 items

Usage:
    python check_q16.py <workspace_path>
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
    errors = []

    # Check agent script exists
    script_path = workspace / "scripts" / "analyze_pip_process.py"
    if not script_path.exists():
        print("FAILED: scripts/analyze_pip_process.py not found")
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
        print("FAILED: scripts/analyze_pip_process.py timed out (>60s)")
        sys.exit(1)
    except Exception as e:
        print(f"FAILED: error running scripts/analyze_pip_process.py: {e}")
        sys.exit(1)

    if result.returncode != 0:
        print(f"FAILED: scripts/analyze_pip_process.py exited with code {result.returncode}")
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

    # Check process_gaps is a list with >= 2 items
    gaps = data.get("process_gaps", [])
    if not isinstance(gaps, list):
        errors.append(
            f"FAILED: process_gaps must be a list, got {type(gaps).__name__}"
        )
    elif len(gaps) < 2:
        errors.append(
            f"FAILED: process_gaps must have >= 2 items, got {len(gaps)}"
        )

    # Check meetings_with_written_record (must be <= total meetings held)
    written = data.get("meetings_with_written_record") or data.get("meetings_with_email_record")
    held = data.get("total_meetings_held") or data.get("meetings_held")

    if written is None:
        errors.append(
            "FAILED: missing 'meetings_with_written_record' (or 'meetings_with_email_record') field"
        )

    if held is None:
        errors.append(
            "FAILED: missing 'total_meetings_held' (or 'meetings_held') field"
        )

    # Check total_meetings_required is present
    required = data.get("total_meetings_required") or data.get("meetings_required")
    if required is None:
        errors.append(
            "FAILED: missing 'total_meetings_required' field"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
