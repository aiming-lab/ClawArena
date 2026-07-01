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
    # Check analyze_plan.json (P1: must be in work/)
    data, err = _load_json(ws / "work" / "analyze_plan.json")
    if err: _finish([err])
    tables = data.get("tables_need_analyze") or []
    if not isinstance(tables, list) or len(tables) == 0:
        _finish(["tables_need_analyze must be a non-empty array"])
    # Must include notifications
    notif_entry = None
    for t in tables:
        if not isinstance(t, dict): continue
        tn = str(t.get("table_name") or "").lower()
        if "notification" in tn:
            notif_entry = t
            break
    if notif_entry is None:
        fails.append("tables_need_analyze must include 'notifications' table")
    else:
        reason = str(notif_entry.get("reason") or "").lower()
        # reason must mention stale statistics or bulk delete
        if not (re.search(r"stale|statistic|bulk|delete|autovacuum|dead", reason)):
            fails.append("notifications entry: reason must mention stale statistics or bulk delete, got %r" % reason[:80])
    # Check run_analyze.sh (P1: must be in work/)
    sh_txt = _read(ws / "work" / "run_analyze.sh")
    if sh_txt is None:
        fails.append("file not found: work/run_analyze.sh")
    else:
        low_sh = sh_txt.lower()
        if "analyze" not in low_sh:
            fails.append("run_analyze.sh must contain an ANALYZE command")
        if "notification" not in low_sh:
            fails.append("run_analyze.sh must reference the notifications table")
    _finish(fails)
main()
