#!/usr/bin/env python3
"""
check_q16.py -- Verify scripts/analyze_timeline.py produces correct JSON output.

The script must read access_log_analysis.md and deployment_timeline.md and output JSON:
  - exploit_first_ts: str (2024-11-05T02:14:33Z or similar)
  - vulnerability_introduced_ts: str (2024-10-14T14:32:18Z or similar)
  - fix_deployed_ts: str (2024-11-26 endpoint disabled date, or Oct 14 deploy)
  - exposure_hours: float (Nov 5 02:14 to Nov 26 ~16:52 = ~518.6 hours)
  - regulatory_window_hours: 72
  - regulatory_deadline_ts: str (exploit_first_ts + 72h = 2024-11-08T02:14:33Z)

Ground truth:
  - exploit_first_ts: 2024-11-05T02:14:33Z
  - vulnerability_introduced_ts: 2024-10-14T14:32:18Z
  - exposure_hours: ~518.6 hours (Nov 5 02:14 UTC to Nov 26 16:52 UTC)
    accept 480-550 hours
  - regulatory_deadline_ts: exploit_first_ts + 72h = 2024-11-08T02:14:33Z

Usage:
    python check_q16.py <workspace_path>
"""
import sys
import json
import re
import subprocess
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    script_path = workspace / "scripts" / "analyze_timeline.py"
    if not script_path.exists():
        print("FAILED: scripts/analyze_timeline.py not found")
        sys.exit(1)

    # Run the script
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(workspace),
        )
    except subprocess.TimeoutExpired:
        print("FAILED: scripts/analyze_timeline.py timed out after 60s")
        sys.exit(1)
    except Exception as e:
        print(f"FAILED: error running scripts/analyze_timeline.py: {e}")
        sys.exit(1)

    if result.returncode != 0:
        print(f"FAILED: scripts/analyze_timeline.py exited {result.returncode}")
        if result.stderr:
            print(result.stderr[:500])
        sys.exit(1)

    # Parse stdout as JSON
    try:
        data = json.loads(result.stdout.strip())
    except Exception as e:
        print(f"FAILED: stdout is not valid JSON: {e}")
        print(f"stdout was: {result.stdout[:300]}")
        sys.exit(1)

    # Check exploit_first_ts references Nov 5, 2024
    eft = data.get("exploit_first_ts", "")
    if not re.search(r'2024-11-05|Nov.*5.*2024', str(eft)):
        errors.append(
            f"FAILED: exploit_first_ts should reference 2024-11-05, got {eft!r}"
        )

    # Check vulnerability_introduced_ts references Oct 14, 2024
    vit = data.get("vulnerability_introduced_ts", "")
    if not re.search(r'2024-10-14|Oct.*14.*2024', str(vit)):
        errors.append(
            f"FAILED: vulnerability_introduced_ts should reference 2024-10-14, got {vit!r}"
        )

    # Check exposure_hours (480-550 hours)
    eh = data.get("exposure_hours")
    if eh is None:
        errors.append("FAILED: missing field 'exposure_hours'")
    else:
        try:
            eh_float = float(eh)
            if not (480 <= eh_float <= 550):
                errors.append(
                    f"FAILED: exposure_hours expected ~518 hours (Nov 5 to Nov 26 endpoint disabled), "
                    f"got {eh_float:.1f}"
                )
        except (TypeError, ValueError):
            errors.append(f"FAILED: exposure_hours must be a number, got {eh!r}")

    # Check regulatory_window_hours = 72
    rwh = data.get("regulatory_window_hours")
    if rwh is None:
        errors.append("FAILED: missing field 'regulatory_window_hours'")
    elif abs(float(rwh) - 72.0) > 0.5:
        errors.append(f"FAILED: regulatory_window_hours expected 72, got {rwh!r}")

    # Check regulatory_deadline_ts references Nov 8, 2024 (exploit + 72h)
    rdt = data.get("regulatory_deadline_ts", "")
    if not re.search(r'2024-11-0[78]|Nov.*8.*2024|Nov.*7.*2024', str(rdt)):
        errors.append(
            f"FAILED: regulatory_deadline_ts should be ~2024-11-08 "
            f"(exploit_first_ts + 72h), got {rdt!r}"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
