#!/usr/bin/env python3
"""
check_q21.py -- Verify scripts/generate_breach_summary.py produces correct JSON output.

The script must read all 3 update files and output JSON:
  - breach_summary.exploit_ts: str (2024-11-05T02:14:33Z)
  - breach_summary.fix_ts: str (2024-11-26 endpoint disabled)
  - breach_summary.notify_ts: str (2024-12-07 from notification_final.md)
  - breach_summary.exposure_hours: float (~518.6, accept 480-550)
  - breach_summary.notification_hours: float (hours from breach to notification)
  - breach_summary.compliant_72h: bool
  - breach_summary.affected_endpoints: int (1 vulnerable endpoint)
  - breach_summary.cvss_score: float (7.5)

Usage:
    python check_q21.py <workspace_path>
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

    script_path = workspace / "scripts" / "generate_breach_summary.py"
    if not script_path.exists():
        print("FAILED: scripts/generate_breach_summary.py not found")
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
        print("FAILED: scripts/generate_breach_summary.py timed out after 60s")
        sys.exit(1)
    except Exception as e:
        print(f"FAILED: error running scripts/generate_breach_summary.py: {e}")
        sys.exit(1)

    if result.returncode != 0:
        print(f"FAILED: scripts/generate_breach_summary.py exited {result.returncode}")
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

    # Navigate to breach_summary
    bs = data.get("breach_summary") if isinstance(data, dict) else None
    if bs is None:
        # Try top-level fields directly
        bs = data

    # Check exploit_ts references Nov 5
    exploit_ts = bs.get("exploit_ts", "")
    if not re.search(r'2024-11-05|Nov.*5.*2024', str(exploit_ts)):
        errors.append(
            f"FAILED: breach_summary.exploit_ts should reference 2024-11-05, "
            f"got {exploit_ts!r}"
        )

    # Check notify_ts references Dec 7
    notify_ts = bs.get("notify_ts", "")
    if not re.search(r'2024-12-07|Dec.*7.*2024', str(notify_ts), re.IGNORECASE):
        errors.append(
            f"FAILED: breach_summary.notify_ts should reference 2024-12-07, "
            f"got {notify_ts!r}"
        )

    # Check exposure_hours (480-550)
    eh = bs.get("exposure_hours")
    if eh is None:
        errors.append("FAILED: missing field 'breach_summary.exposure_hours'")
    else:
        try:
            eh_float = float(eh)
            if not (480 <= eh_float <= 550):
                errors.append(
                    f"FAILED: exposure_hours expected ~518 (Nov 5 to Nov 26), "
                    f"got {eh_float:.1f}"
                )
        except (TypeError, ValueError):
            errors.append(f"FAILED: exposure_hours must be a number, got {eh!r}")

    # Check compliant_72h is a boolean
    c72 = bs.get("compliant_72h")
    if c72 is None:
        errors.append("FAILED: missing field 'breach_summary.compliant_72h'")
    elif not isinstance(c72, bool):
        errors.append(f"FAILED: compliant_72h must be a boolean, got {c72!r}")

    # Check affected_endpoints is a positive integer
    ae = bs.get("affected_endpoints")
    if ae is None:
        errors.append("FAILED: missing field 'breach_summary.affected_endpoints'")
    elif not isinstance(ae, int) or ae < 1:
        errors.append(
            f"FAILED: affected_endpoints must be a positive integer, got {ae!r}"
        )

    # Check cvss_score = 7.5
    cvss = bs.get("cvss_score")
    if cvss is None:
        errors.append("FAILED: missing field 'breach_summary.cvss_score'")
    else:
        try:
            if abs(float(cvss) - 7.5) > 0.05:
                errors.append(
                    f"FAILED: cvss_score expected 7.5, got {cvss!r}"
                )
        except (TypeError, ValueError):
            errors.append(f"FAILED: cvss_score must be a number, got {cvss!r}")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
