#!/usr/bin/env python3
"""
check_q11.py -- Verify analysis/incident_timeline.md and analysis/timeline_data.json (M3 cross-validation).

Usage:
    python check_q11.py <workspace_path>
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

    # --- File 1: analysis/incident_timeline.md ---
    md_path = workspace / "analysis" / "incident_timeline.md"
    if not md_path.exists():
        errors.append(f"FAILED: {md_path} not found")
    else:
        try:
            md_content = md_path.read_text(encoding="utf-8")
        except Exception as e:
            errors.append(f"FAILED: cannot read {md_path}: {e}")
            md_content = ""

        if md_content:
            # Must mention 7 days silence
            if not re.search(r'\b7\b.{0,20}day|day.{0,20}\b7\b|7-day', md_content, re.IGNORECASE):
                errors.append("FAILED: incident_timeline.md does not contain '7 days' or '7-day'")

            # Must mention 60 minutes offset
            if not re.search(r'\b60\b.{0,20}min|60-min|\+60', md_content, re.IGNORECASE):
                errors.append("FAILED: incident_timeline.md does not contain '60 minutes' or '+60' offset")

            # Must mention 5 seconds violation
            if not re.search(r'\b5\b.{0,20}sec|sec.{0,20}\b5\b|5-sec', md_content, re.IGNORECASE):
                errors.append("FAILED: incident_timeline.md does not contain '5 seconds'")

            # Must have >= 3 ## headings
            headings = [ln for ln in md_content.splitlines() if ln.strip().startswith("##")]
            if len(headings) < 3:
                errors.append(f"FAILED: incident_timeline.md has only {len(headings)} ## headings (need >= 3)")

    # --- File 2: analysis/timeline_data.json ---
    json_path = workspace / "analysis" / "timeline_data.json"
    if not json_path.exists():
        errors.append(f"FAILED: {json_path} not found")
    else:
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except Exception as e:
            errors.append(f"FAILED: cannot parse {json_path}: {e}")
            data = {}

        if data:
            if data.get("silence_days") != 7:
                errors.append(f"FAILED: timeline_data.json silence_days expected 7, got {data.get('silence_days')!r}")
            if data.get("offset_minutes") != 60:
                errors.append(f"FAILED: timeline_data.json offset_minutes expected 60, got {data.get('offset_minutes')!r}")
            if data.get("seconds_over_cutoff") != 5:
                errors.append(f"FAILED: timeline_data.json seconds_over_cutoff expected 5, got {data.get('seconds_over_cutoff')!r}")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
