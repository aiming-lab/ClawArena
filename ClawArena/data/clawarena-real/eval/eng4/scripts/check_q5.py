#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib
from pathlib import Path

def _load_json(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        return json.loads(p.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, "invalid JSON in " + p.name + ": " + str(e)

def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None

def _finish(fails):
    if fails:
        for f in fails:
            print("FAILED: " + f)
        sys.exit(1)
    print("PASSED")
    sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "work" / "archive_review.json")
    if err: _finish([err])
    # is_outdated must be True
    if data.get("is_outdated") is not True:
        fails.append("is_outdated == %r (expected true)" % data.get("is_outdated"))
    # outdated_recommendations must be a non-empty array with at least 2 entries
    # (archive has 2 Hash index recommendations and the work_mem recommendation)
    orecs = data.get("outdated_recommendations") or []
    if not isinstance(orecs, list) or len(orecs) == 0:
        fails.append("outdated_recommendations must be a non-empty array")
    else:
        # HARDENED: at least one entry's original_text must contain "HASH" (case-insensitive)
        # and reference an actual DDL/recommendation from the archive file
        found_hash_original = False
        found_hash_reason_complete = False
        for rec in orecs:
            if not isinstance(rec, dict):
                continue
            reason = str(rec.get("reason_outdated") or "").lower()
            orig = str(rec.get("original_text") or "").lower()
            # HARDENED: original_text must contain "hash" to show it came from the archive
            if "hash" in orig:
                found_hash_original = True
                # HARDENED: reason_outdated must mention BOTH "equality" AND "range"
                # (the archive itself explains this limitation explicitly)
                if ("equality" in reason or "only =" in reason or "= operator" in reason or "only equality" in reason) and (
                    "range" in reason
                ):
                    found_hash_reason_complete = True
        if not found_hash_original:
            fails.append(
                "outdated_recommendations: at least one entry\'s original_text must quote the Hash index DDL "
                "from the archive (must contain \'HASH\' — read archive/old_optimization_plan_v0.md literally)"
            )
        elif not found_hash_reason_complete:
            fails.append(
                "outdated_recommendations: reason_outdated for the Hash index entry must explicitly mention "
                "BOTH \'equality\' (what Hash supports) AND \'range\' (what it cannot support)"
            )
    # valid_recommendations must be an array (can be empty if nothing is valid)
    vrecs = data.get("valid_recommendations")
    if vrecs is not None and not isinstance(vrecs, list):
        fails.append("valid_recommendations must be an array")
    _finish(fails)
main()
