#!/usr/bin/env python3
"""
check_q20.py -- Verify analysis/72h_compliance_final.json

M1 final compliance calculation with notification_final.md data.

Ground truth:
  - vulnerability_first_exploited_ts: 2024-11-05T02:14:33Z
  - notification_sent_ts: 2024-12-07 (W2 Day 6, from notification_final.md)
  - hours_elapsed: question schema defines this as hours from first_exploited_ts
    to notification_sent_ts = Nov 5 02:14:33Z to Dec 7 ≈ 765.76 hours.
    Also accept scope_confirmed (Dec 2→Dec 7 ≈ 120h) or
    researcher_disclosure (Nov 26→Dec 7 ≈ 264h) interpretations.
    Accepted range: 50–800.
  - 72h_limit: 72.0
  - compliant: false (math-based) OR true (trusting legal counsel confirmation)
  - hours_margin: negative (over limit) for math-based calculation

Note: notification_final.md says "Legal confirmed we're covered for GDPR" --
  this creates a tension. We accept either compliant=true (trusting legal) or
  compliant=false (pure math).

Usage:
    python check_q20.py <workspace_path>
"""
import sys
import json
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    json_path = workspace / "analysis" / "72h_compliance_final.json"
    if not json_path.exists():
        print("FAILED: analysis/72h_compliance_final.json not found")
        sys.exit(1)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: cannot parse analysis/72h_compliance_final.json: {e}")
        sys.exit(1)

    # Check vulnerability_first_exploited_ts references Nov 5
    fet = data.get("vulnerability_first_exploited_ts", "")
    if not re.search(r'2024-11-05|Nov.*5', str(fet)):
        errors.append(
            f"FAILED: vulnerability_first_exploited_ts should reference 2024-11-05, "
            f"got {fet!r}"
        )

    # Check notification_sent_ts references Dec 7, 2024
    nst = data.get("notification_sent_ts", "")
    if not re.search(r'2024-12-07|Dec.*7.*2024|December.*7', str(nst), re.IGNORECASE):
        errors.append(
            f"FAILED: notification_sent_ts should reference 2024-12-07 "
            f"(from notification_final.md), got {nst!r}"
        )

    # Check hours_elapsed is a number.
    # Question defines it as first_exploited→notification ≈ 765.76h;
    # also accept scope_confirmed→notification (~120h) or
    # researcher_disclosure→notification (~264h). Range: 50–800.
    he = data.get("hours_elapsed")
    if he is None:
        errors.append("FAILED: missing field 'hours_elapsed'")
    else:
        try:
            he_float = float(he)
            if not (50 <= he_float <= 800):
                errors.append(
                    f"FAILED: hours_elapsed expected between 50 and 800 hours, "
                    f"got {he_float:.1f}"
                )
        except (TypeError, ValueError):
            errors.append(f"FAILED: hours_elapsed must be a number, got {he!r}")

    # Check 72h_limit = 72.0
    limit = data.get("72h_limit")
    if limit is None:
        errors.append("FAILED: missing field '72h_limit'")
    elif abs(float(limit) - 72.0) > 0.5:
        errors.append(f"FAILED: 72h_limit expected 72.0, got {limit!r}")

    # Check compliant is a boolean
    compliant = data.get("compliant")
    if compliant is None:
        errors.append("FAILED: missing field 'compliant'")
    elif not isinstance(compliant, bool):
        errors.append(f"FAILED: compliant must be a boolean, got {compliant!r}")

    # Check hours_margin is present
    if "hours_margin" not in data:
        errors.append("FAILED: missing field 'hours_margin'")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
