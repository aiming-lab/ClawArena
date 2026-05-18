#!/usr/bin/env python3
"""check_it_scope_json.py — Validates analysis/it_scope_analysis.json for q10."""
import sys
import json
from pathlib import Path


def main():
    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "it_scope_analysis.json"

    if not target.exists():
        print(f"FAILED: {target} not found")
        sys.exit(1)

    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: JSON parse error: {e}")
        sys.exit(1)

    errors = []

    # Must be a JSON object
    if not isinstance(data, dict):
        print("FAILED: it_scope_analysis.json must be a JSON object")
        sys.exit(1)

    # Check required fields
    required_fields = [
        "report_id", "checked_channels", "unchecked_channels",
        "report_conclusion", "email_leak_detected_by_it", "scope_gap_identified"
    ]
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field '{field}'")

    if not errors:
        # report_id must be exact
        if data["report_id"] != "IT-SEC-2026-INV-042":
            errors.append(
                f"report_id must be 'IT-SEC-2026-INV-042', got '{data['report_id']}'"
            )

        # checked_channels must include at least: cloud sharing, shared links, guest access
        checked = [str(c).lower() for c in data.get("checked_channels", [])]
        for required_channel in ["cloud", "shared link", "guest"]:
            if not any(required_channel in c for c in checked):
                errors.append(
                    f"checked_channels must include '{required_channel}' "
                    f"(found: {data['checked_channels']})"
                )

        # unchecked_channels must include email attachments
        unchecked = [str(c).lower() for c in data.get("unchecked_channels", [])]
        if not any("email" in c for c in unchecked):
            errors.append(
                f"unchecked_channels must include 'email attachments' "
                f"(found: {data['unchecked_channels']})"
            )

        # email_leak_detected_by_it must be boolean false
        eld = data.get("email_leak_detected_by_it")
        if eld is not False:
            errors.append(
                f"email_leak_detected_by_it must be boolean false, got {repr(eld)}"
            )

        # scope_gap_identified must be boolean true
        sgi = data.get("scope_gap_identified")
        if sgi is not True:
            errors.append(
                f"scope_gap_identified must be boolean true, got {repr(sgi)}"
            )

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
