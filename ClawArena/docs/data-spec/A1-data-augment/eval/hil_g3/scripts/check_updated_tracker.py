#!/usr/bin/env python3
"""
check_updated_tracker.py — Validate updated analysis/contradiction_tracker.json (post-upd4).

Checks:
  - File exists and is valid JSON
  - All 4 Cs (C1–C4) present
  - Each entry has a status field
  - C3 entry references hash verification AND partial admission
"""
import sys
import json
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_updated_tracker.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "contradiction_tracker.json"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    try:
        content = target.read_text(encoding="utf-8")
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"FAILED: invalid JSON in {target}: {e}")
        sys.exit(1)

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

    if len(entries) < 4:
        print(f"FAILED: expected 4 contradiction entries (C1–C4), found {len(entries)}")
        sys.exit(1)

    raw_lower = content.lower()

    # All 4 Cs present
    for cid in ["c1", "c2", "c3", "c4"]:
        if cid not in raw_lower:
            print(f"FAILED: contradiction '{cid.upper()}' not found in contradiction_tracker.json")
            sys.exit(1)

    # Each entry should have status field
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        if "status" not in entry:
            print(f"FAILED: entry '{entry.get('id')}' missing 'status' field — entries should have a status like 'refuted' or 'confirmed_false'")
            sys.exit(1)

    # C3 entry must reference hash AND partial admission
    c3_entry = None
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        eid = str(entry.get("id", "")).upper()
        if eid == "C3" or eid == "3":
            c3_entry = entry
            break
    if c3_entry is None and len(entries) >= 3:
        c3_entry = entries[2]

    if c3_entry is not None:
        c3_text = json.dumps(c3_entry).lower()
        has_hash = "hash" in c3_text or "sha" in c3_text or "a3f7b2c8e9d1" in c3_text
        has_admission = "admission" in c3_text or "admitted" in c3_text or "partial" in c3_text or "deny" in c3_text or "claim" in c3_text
        if not has_hash:
            print("FAILED: C3 entry does not reference hash verification — C3 refutation requires hash evidence")
            sys.exit(1)
        if not has_admission:
            print("FAILED: C3 entry does not reference partial admission — C3 should document Lin Xiaoya's third denial claim")
            sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
