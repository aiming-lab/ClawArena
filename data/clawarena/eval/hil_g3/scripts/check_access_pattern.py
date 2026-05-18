#!/usr/bin/env python3
"""
check_access_pattern.py — Validate analysis/access_pattern_analysis.json.

Checks:
  - File exists and is valid JSON
  - Has at least one entry for Lin Xiaoya with event_type=DOWNLOAD and is_anomalous=true
  - Has a reference to full version (v1.1 or "full" or "2.3")
"""
import sys
import json
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_access_pattern.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "access_pattern_analysis.json"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    try:
        content = target.read_text(encoding="utf-8")
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"FAILED: invalid JSON in {target}: {e}")
        sys.exit(1)

    # Accept either a list or an object with an array inside
    if isinstance(data, dict):
        entries = []
        for v in data.values():
            if isinstance(v, list):
                entries.extend(v)
            elif isinstance(v, dict):
                entries.append(v)
    elif isinstance(data, list):
        entries = data
    else:
        print(f"FAILED: unexpected JSON structure: {type(data).__name__}")
        sys.exit(1)

    # Check for Lin Xiaoya entry with DOWNLOAD and anomalous flag
    raw_lower = content.lower()

    has_lin = "lin xiaoya" in raw_lower or "linxiaoya" in raw_lower or "lin_xiaoya" in raw_lower
    if not has_lin:
        print("FAILED: Lin Xiaoya entry not found in access_pattern_analysis.json")
        sys.exit(1)

    has_download = "download" in raw_lower
    if not has_download:
        print("FAILED: DOWNLOAD event_type not found in access_pattern_analysis.json")
        sys.exit(1)

    # Check anomalous marker
    has_anomalous = (
        '"is_anomalous": true' in content
        or "'is_anomalous': True" in content
        or "anomalous" in raw_lower
    )
    if not has_anomalous:
        print("FAILED: anomalous marker not found in access_pattern_analysis.json — expected is_anomalous=true for Lin Xiaoya's download event")
        sys.exit(1)

    # Check full version reference
    has_full = (
        "v1.1" in content
        or '"full"' in raw_lower
        or "'full'" in raw_lower
        or "full version" in raw_lower
        or "2.3" in content
    )
    if not has_full:
        print("FAILED: full version reference (v1.1 / 'full' / 2.3) not found in access_pattern_analysis.json")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
