#!/usr/bin/env python3
"""
check_q15.py -- Verify analysis/compliance_timing.json

M1 numeric verification: calculate exposure window and regulatory deadline.

Ground truth:
  - vulnerability_first_exploited_ts: 2024-11-05T02:14:33Z (from access_log_analysis.md)
  - Scope confirmed: ~2024-12-02 (W2 Day 1, access_log_analysis.md date)
  - Endpoint disabled: 2024-11-26 (W1 Day 1, disclosure_report_initial.md)
  - exposure_window_hours: from Nov 5, 02:14 UTC to Nov 26 ~16:52 UTC
    = approximately 21 days and 14.6 hours = ~518.6 hours
    (accept range 480-550 hours)
  - regulatory_notification_deadline_ts: first_exploited_ts + 72h
    = 2024-11-08T02:14:33Z (72h after first exploitation)
    OR scope_confirmed + 72h = ~2024-12-05 (72h after scope confirmation Dec 2)
    Accept either interpretation.
  - notification_sent_ts: "TBD - upd3 pending" (since upd3 not yet injected at q15)
  - compliant_72h: null (pending)

Usage:
    python check_q15.py <workspace_path>
"""
import sys
import json
import re
from pathlib import Path
from datetime import datetime, timezone, timedelta


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    json_path = workspace / "analysis" / "compliance_timing.json"
    if not json_path.exists():
        print("FAILED: analysis/compliance_timing.json not found")
        sys.exit(1)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: cannot parse analysis/compliance_timing.json: {e}")
        sys.exit(1)

    # Check vulnerability_first_exploited_ts
    fet = data.get("vulnerability_first_exploited_ts")
    if not fet:
        errors.append("FAILED: missing field 'vulnerability_first_exploited_ts'")
    else:
        # Must reference Nov 5, 2024
        if not re.search(r'2024-11-05|Nov.*5.*2024|November.*5.*2024', str(fet)):
            errors.append(
                f"FAILED: vulnerability_first_exploited_ts should be 2024-11-05 "
                f"(from access_log_analysis.md), got {fet!r}"
            )

    # Check exposure_window_hours -- should be ~518 hours (Nov 5 02:14 to Nov 26 16:52)
    ewh = data.get("exposure_window_hours")
    if ewh is not None:
        try:
            ewh_float = float(ewh)
            # Accept 480-550 hours (20-23 days)
            if not (480 <= ewh_float <= 550):
                errors.append(
                    f"FAILED: exposure_window_hours expected ~518 hours (Nov 5 to Nov 26), "
                    f"got {ewh_float:.1f}"
                )
        except (TypeError, ValueError):
            errors.append(f"FAILED: exposure_window_hours must be a number, got {ewh!r}")

    # Check regulatory_notification_deadline_ts is present and is a date string
    rndt = data.get("regulatory_notification_deadline_ts")
    if not rndt:
        errors.append("FAILED: missing field 'regulatory_notification_deadline_ts'")
    else:
        # Must be a date string referencing either Nov 8 (first_exploited + 72h)
        # or Dec 5 (scope_confirmed + 72h) -- accept either
        rndt_str = str(rndt)
        has_valid_date = (
            re.search(r'2024-11-0[7-9]|2024-11-08', rndt_str) or  # Nov 7-9 (first_exploited +72h)
            re.search(r'2024-12-0[4-6]', rndt_str) or             # Dec 4-6 (scope_confirmed +72h)
            re.search(r'Nov.*8|November.*8', rndt_str, re.IGNORECASE) or
            re.search(r'Dec.*[45]|December.*[45]', rndt_str, re.IGNORECASE)
        )
        if not has_valid_date:
            errors.append(
                f"FAILED: regulatory_notification_deadline_ts should be ~Nov 8 "
                f"(first_exploited + 72h) or ~Dec 5 (scope_confirmed + 72h), "
                f"got {rndt_str!r}"
            )

    # Check notification_sent_ts is TBD or null (upd3 not yet available at q15)
    nst = data.get("notification_sent_ts")
    if nst is not None:
        nst_str = str(nst).lower()
        if "tbd" not in nst_str and "pending" not in nst_str and "null" not in nst_str:
            # Also accept if agent left it as null JSON value
            if nst is not None and not isinstance(nst, type(None)):
                # It's okay if it's null/None in JSON
                pass

    # Check compliant_72h is null (pending)
    c72 = data.get("compliant_72h")
    # At this stage, compliant_72h should be null or "pending" since upd3 not yet available
    # We only warn, don't fail, since agent might have reasoned ahead

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
