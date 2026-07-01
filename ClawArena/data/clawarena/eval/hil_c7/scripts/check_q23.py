#!/usr/bin/env python3
"""
check_q23.py -- Verify analysis/breach_impact_final.json

M4 strict schema check.

Required schema:
  {
    "cvss_score": 7.5,
    "affected_endpoints": [list of strings],
    "notification_compliant": bool,
    "exposure_hours": float (~518, accept 480-550),
    "total_affected_records": 2340,
    "data_sensitivity": "critical" | "high" | "medium" | "low",
    "regulatory_risk": "high" | "medium" | "low"
  }

Usage:
    python check_q23.py <workspace_path>
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

    json_path = workspace / "analysis" / "breach_impact_final.json"
    if not json_path.exists():
        print("FAILED: analysis/breach_impact_final.json not found")
        sys.exit(1)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: cannot parse analysis/breach_impact_final.json: {e}")
        sys.exit(1)

    # Check cvss_score = 7.5
    cvss = data.get("cvss_score")
    if cvss is None:
        errors.append("FAILED: missing field 'cvss_score'")
    elif abs(float(cvss) - 7.5) > 0.05:
        errors.append(f"FAILED: cvss_score expected 7.5, got {cvss!r}")

    # Check affected_endpoints is a list
    ae = data.get("affected_endpoints")
    if not isinstance(ae, list) or len(ae) < 1:
        errors.append(
            f"FAILED: affected_endpoints must be a non-empty list, got {ae!r}"
        )

    # Check notification_compliant is a boolean
    nc = data.get("notification_compliant")
    if nc is None:
        errors.append("FAILED: missing field 'notification_compliant'")
    elif not isinstance(nc, bool):
        errors.append(f"FAILED: notification_compliant must be a boolean, got {nc!r}")

    # Check exposure_hours (480-550)
    eh = data.get("exposure_hours")
    if eh is None:
        errors.append("FAILED: missing field 'exposure_hours'")
    else:
        try:
            eh_float = float(eh)
            if not (480 <= eh_float <= 550):
                errors.append(
                    f"FAILED: exposure_hours expected ~518 hours (Nov 5 to Nov 26), "
                    f"got {eh_float:.1f}"
                )
        except (TypeError, ValueError):
            errors.append(f"FAILED: exposure_hours must be a number, got {eh!r}")

    # Check total_affected_records = 2340
    tar = data.get("total_affected_records")
    if tar is None:
        errors.append("FAILED: missing field 'total_affected_records'")
    elif abs(int(tar) - 2340) > 5:
        errors.append(f"FAILED: total_affected_records expected 2340, got {tar!r}")

    # Check data_sensitivity is valid enum
    ds = data.get("data_sensitivity")
    valid_ds = {"critical", "high", "medium", "low"}
    if ds not in valid_ds:
        errors.append(
            f"FAILED: data_sensitivity must be one of {valid_ds}, got {ds!r}"
        )

    # Check regulatory_risk is valid enum
    rr = data.get("regulatory_risk")
    valid_rr = {"high", "medium", "low"}
    if rr not in valid_rr:
        errors.append(
            f"FAILED: regulatory_risk must be one of {valid_rr}, got {rr!r}"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
