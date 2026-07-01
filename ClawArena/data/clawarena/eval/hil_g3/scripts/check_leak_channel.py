#!/usr/bin/env python3
"""
check_leak_channel.py — Validate analysis/leak_channel_comparison.json.

Checks:
  - File exists and is valid JSON
  - Has >= 2 entries (channels)
  - One entry has is_leak_vector=true and covered=false (email channel)
  - One entry has covered=true and is_leak_vector=false (cloud sharing)
"""
import sys
import json
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_leak_channel.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "leak_channel_comparison.json"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    try:
        content = target.read_text(encoding="utf-8")
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"FAILED: invalid JSON in {target}: {e}")
        sys.exit(1)

    # Accept array or object with array inside
    if isinstance(data, list):
        entries = data
    elif isinstance(data, dict):
        entries = []
        for v in data.values():
            if isinstance(v, list):
                entries.extend(v)
    else:
        print(f"FAILED: unexpected JSON structure: {type(data).__name__}")
        sys.exit(1)

    if len(entries) < 2:
        print(f"FAILED: expected >= 2 channel entries, found {len(entries)}")
        sys.exit(1)

    # Check for email channel: is_leak_vector=true and covered=false
    has_uncovered_leak = any(
        isinstance(e, dict)
        and e.get("is_leak_vector") is True
        and e.get("covered") is False
        for e in entries
    )
    if not has_uncovered_leak:
        print("FAILED: no entry with is_leak_vector=true and covered=false found — email attachment channel should be uncovered leak vector")
        sys.exit(1)

    # Check for cloud sharing: covered=true and is_leak_vector=false
    has_covered_non_leak = any(
        isinstance(e, dict)
        and e.get("covered") is True
        and e.get("is_leak_vector") is False
        for e in entries
    )
    if not has_covered_non_leak:
        print("FAILED: no entry with covered=true and is_leak_vector=false found — cloud sharing channel should be covered but not the leak vector")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
