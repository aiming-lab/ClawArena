#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, csv
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

VALID_METHODS = {"page", "dm", "alert"}

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q15_escalations.json")
    if err: _finish([err])
    # generated_at top-level
    if not data.get("generated_at"):
        fails.append("q15_escalations.json missing top-level 'generated_at' field (P5)")
    escs = data.get("escalations")
    if not isinstance(escs, list) or len(escs) < 3:
        _finish(["escalations must be an array with >= 3 entries (got %s)" % repr(escs)[:40]])
    # method valid
    for i, e in enumerate(escs):
        m = str(e.get("method", "")).lower()
        if m not in VALID_METHODS:
            fails.append("escalations[%d].method == %r (must be page/dm/alert)" % (i, e.get("method")))
    # at least 1 slack, 1 feishu
    channels = set(str(e.get("channel", "")).lower() for e in escs)
    if not any("slack" in c for c in channels):
        fails.append("escalations must include at least 1 entry from Slack channel")
    if not any("feishu" in c for c in channels):
        fails.append("escalations must include at least 1 entry from Feishu channel")
    _finish(fails)
main()
