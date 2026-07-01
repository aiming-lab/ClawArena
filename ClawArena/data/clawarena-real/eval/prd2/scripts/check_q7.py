#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re
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
    ws = Path(sys.argv[1])
    pe = ws / "policy_engine"
    fails = []
    data, err = _load_json(pe / "reports" / "deprecation_log.json")
    if err: _finish([err])

    entries = data.get("entries") or []
    if not isinstance(entries, list):
        _finish(["deprecation_log.json: 'entries' must be a list"])

    # Must have an entry for meta_strike_7 with deprecated=true
    meta_s7_entry = None
    for e in entries:
        key = str(e.get("field") or e.get("key") or e.get("id") or "").lower()
        if "meta" in key and ("strike_7" in key or "strike7" in key):
            meta_s7_entry = e
            break
    if meta_s7_entry is None:
        fails.append("deprecation_log: no entry found for meta strike_7 (e.g. field='meta_strike_7_duration')")
    elif meta_s7_entry.get("deprecated") is not True:
        fails.append("deprecation_log: meta strike_7 entry must have deprecated=true (got %r)" % meta_s7_entry.get("deprecated"))

    # Must have an entry for youtube appeal window with deprecated=true
    yt_appeal_entry = None
    for e in entries:
        key = str(e.get("field") or e.get("key") or e.get("id") or "").lower()
        if "youtube" in key and "appeal" in key:
            yt_appeal_entry = e
            break
    if yt_appeal_entry is None:
        fails.append("deprecation_log: no entry found for youtube appeal window (e.g. field='youtube_appeal_window_strike')")
    elif yt_appeal_entry.get("deprecated") is not True:
        fails.append("deprecation_log: youtube appeal window entry must have deprecated=true (got %r)" % yt_appeal_entry.get("deprecated"))

    _finish(fails)
main()
