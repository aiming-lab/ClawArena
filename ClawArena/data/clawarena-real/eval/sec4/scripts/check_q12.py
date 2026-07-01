#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, csv, hashlib
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
    data, err = _load_json(ws / "audit" / "ropa_version_decision.json")
    if err: _finish([err])
    sv = data.get("selected_version")
    if str(sv).strip().lower() not in ("v1", "ropa_controller_draft_v1", "draft_v1"):
        fails.append("selected_version == %r (expected \"v1\")" % sv)
    rv = data.get("rejected_version")
    if str(rv).strip().lower() not in ("v0", "ropa_controller_legacy_v0", "legacy_v0"):
        fails.append("rejected_version == %r (expected \"v0\")" % rv)
    reason = str(data.get("reason", "")).lower()
    # Keyword check: must include 'legacy' or 'supersed' (covers superseded/supersedes)
    if "legacy" not in reason and "supersed" not in reason:
        fails.append("reason must include 'legacy' or 'superseded' (got: %r)" % data.get("reason",""))
    sf = data.get("source_file", "")
    if not sf or "v1" not in str(sf).lower():
        fails.append("source_file must reference the v1 RoPA file (got %r)" % sf)
    _finish(fails)
main()
