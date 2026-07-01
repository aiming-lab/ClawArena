#!/usr/bin/env python3
"""
check_incident_timeline.py — Validate analysis/incident_timeline.json.

Checks:
  - File exists and is valid JSON
  - Array with >= 5 entries
  - Contains "14:22:17" (Lin Xiaoya download timestamp)
  - Contains "15:03:44" (email send timestamp)
  - Contains "2.3" or 2.3 as float (full file size)
  - At least one entry references external recipient / headhunter
"""
import sys
import json
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_incident_timeline.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "incident_timeline.json"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    try:
        content = target.read_text(encoding="utf-8")
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"FAILED: invalid JSON in {target}: {e}")
        sys.exit(1)

    if not isinstance(data, list):
        print(f"FAILED: expected a JSON array, got {type(data).__name__}")
        sys.exit(1)

    if len(data) < 5:
        print(f"FAILED: expected >= 5 events, found {len(data)}")
        sys.exit(1)

    # Serialize entire content for string-level checks
    raw = content

    if "14:22:17" not in raw:
        print("FAILED: download timestamp '14:22:17' not found in incident_timeline.json")
        sys.exit(1)

    if "15:03:44" not in raw:
        print("FAILED: email send timestamp '15:03:44' not found in incident_timeline.json")
        sys.exit(1)

    # Check for full file size: "2.3" as string or 2.3 as float value
    has_size = "2.3" in raw
    if not has_size:
        # Check numeric float values in entries
        has_size = any(
            isinstance(entry.get("size_mb"), float) and abs(entry["size_mb"] - 2.3) < 0.05
            for entry in data if isinstance(entry, dict)
        )
    if not has_size:
        print("FAILED: full file size '2.3' (MB) not found in incident_timeline.json")
        sys.exit(1)

    raw_lower = raw.lower()
    if "headhunter" not in raw_lower:
        print("FAILED: external recipient reference ('headhunter') not found in incident_timeline.json")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
