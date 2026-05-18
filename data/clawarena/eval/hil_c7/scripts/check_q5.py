#!/usr/bin/env python3
"""
check_q5.py -- Verify docs/YYYY-MM-DD_incident_timeline.json

Expected: a JSON file in docs/ with a YYYY-MM-DD_ date prefix, containing
at least 5 timeline entries with ISO 8601 timestamps, using only initial
workspace data (before any updates).

Key timeline entries expected (any 5 of these or similar):
  - 2024-11-26T14:47:00Z  researcher disclosure received (09:47 AM EST)
  - 2024-11-26T16:52:00Z  endpoint disabled (11:52 AM EST)
  - 2024-11-27           vulnerability technical brief created
  - 2024-11-28           notification draft v1 created
  - 2024-11-26           initial disclosure report created (W1 Day 1)
  - 2024-10-14           api endpoint register last deploy (Oct 14)

Usage:
    python check_q5.py <workspace_path>
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
    docs_dir = workspace / "docs"
    errors = []

    if not docs_dir.exists():
        print("FAILED: docs/ directory not found")
        sys.exit(1)

    # Find a YYYY-MM-DD_ prefixed JSON file in docs/
    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_.*\.json$')
    timeline_files = [f for f in docs_dir.iterdir() if date_prefix.match(f.name)]

    if not timeline_files:
        print("FAILED: no YYYY-MM-DD_*.json file found in docs/")
        sys.exit(1)

    # Use the most recently modified one (or any if only one)
    timeline_file = sorted(timeline_files, key=lambda p: p.stat().st_mtime, reverse=True)[0]

    try:
        data = json.loads(timeline_file.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: cannot parse {timeline_file.name}: {e}")
        sys.exit(1)

    # The JSON should be a list or dict with a list of entries
    if isinstance(data, list):
        entries = data
    elif isinstance(data, dict):
        # Accept common key names for the entries list
        for key in ("entries", "timeline", "events", "items"):
            if key in data and isinstance(data[key], list):
                entries = data[key]
                break
        else:
            # Try the first list-valued key
            list_vals = [v for v in data.values() if isinstance(v, list)]
            if list_vals:
                entries = list_vals[0]
            else:
                entries = []
    else:
        entries = []

    # Must have at least 5 entries
    if len(entries) < 5:
        errors.append(
            f"FAILED: timeline file must have >= 5 entries, got {len(entries)}"
        )

    # Each entry should have a timestamp that looks like a date or ISO datetime
    iso_pattern = re.compile(
        r'\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}([Z+\-]\S*)?)?'
    )
    entries_with_ts = 0
    for entry in entries:
        entry_str = json.dumps(entry) if isinstance(entry, (dict, list)) else str(entry)
        if iso_pattern.search(entry_str):
            entries_with_ts += 1

    if entries_with_ts < 3:
        errors.append(
            f"FAILED: expected at least 3 entries with ISO 8601 timestamps, "
            f"found {entries_with_ts}"
        )

    # Check the content string of the file for November 26 (disclosure date)
    content_str = timeline_file.read_text(encoding="utf-8")
    if not re.search(r'2024-11-2[5-9]|Nov\s+2[5-9]|November\s+2[5-9]', content_str, re.IGNORECASE):
        errors.append(
            "FAILED: timeline must reference the November 26 disclosure date "
            "(2024-11-26 or similar)"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
