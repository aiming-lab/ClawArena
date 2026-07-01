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
    data, err = _load_json(ws / "work" / "q010_join_analysis.json")
    if err: _finish([err])
    # has_disk_spill must be True
    hds = data.get("has_disk_spill")
    if hds is not True:
        fails.append("has_disk_spill == %r (expected true; EXPLAIN shows Hash Batches=8 and Sort Method=external merge Disk)" % hds)
    # hash_batches must be > 1
    try:
        hb = int(data.get("hash_batches") or 0)
        if hb <= 1:
            fails.append("hash_batches == %d (expected > 1 — indicates disk spill)" % hb)
    except (TypeError, ValueError):
        fails.append("hash_batches not an int: %r" % data.get("hash_batches"))
    # recommendation must be a valid value
    valid_recs = {"increase_work_mem", "rewrite_query", "add_index", "create_statistics"}
    rec = str(data.get("recommendation") or "")
    if rec not in valid_recs:
        fails.append("recommendation %r not in valid set %s" % (rec, sorted(valid_recs)))
    # At this point (Q8, before Update 2), recommendation should be increase_work_mem
    # but we accept any valid value since agent may read Update 2 early
    # join_type must be present and non-empty
    if not data.get("join_type"):
        fails.append("join_type field missing or empty")
    _finish(fails)
main()
