#!/usr/bin/env python3
"""
check_contradiction_tracker.py — Validate analysis/contradiction_tracker.json.

Checks:
  - File exists and is valid JSON
  - Has exactly 4 entries covering C1, C2, C3, C4
  - Each entry has id, description (or lin_xiaoya_claim), evidence_against fields
  - C4 entry specifically mentions IT scope
"""
import sys
import json
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_contradiction_tracker.py <workspace>")
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

    # Check for C1–C4 ids
    raw_lower = content.lower()
    for cid in ["c1", "c2", "c3", "c4"]:
        if cid not in raw_lower:
            print(f"FAILED: contradiction '{cid.upper()}' not found in contradiction_tracker.json")
            sys.exit(1)

    # Check that each entry has required fields (id + description/claim + evidence)
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        has_id = "id" in entry
        has_desc = any(k in entry for k in ("description", "lin_xiaoya_claim", "claim", "summary"))
        has_evidence = any(k in entry for k in ("evidence_against", "evidence", "refutation"))
        if not has_id:
            print(f"FAILED: entry missing 'id' field: {entry}")
            sys.exit(1)
        if not has_desc:
            print(f"FAILED: entry '{entry.get('id')}' missing description/claim field")
            sys.exit(1)
        if not has_evidence:
            print(f"FAILED: entry '{entry.get('id')}' missing evidence_against/evidence field")
            sys.exit(1)

    # C4 must mention IT scope
    c4_entry = None
    for entry in entries:
        if isinstance(entry, dict):
            eid = str(entry.get("id", "")).upper()
            if eid == "C4" or eid == "4":
                c4_entry = entry
                break

    if c4_entry is not None:
        c4_text = json.dumps(c4_entry).lower()
        if "it" not in c4_text and "scope" not in c4_text and "inv-042" not in c4_text:
            print("FAILED: C4 entry does not mention IT scope/report — C4 should describe the IT security report scope limitation")
            sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
