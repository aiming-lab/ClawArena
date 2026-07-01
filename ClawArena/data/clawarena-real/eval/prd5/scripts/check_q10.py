#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, math
from pathlib import Path

def _load_json(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        return json.loads(p.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, "invalid JSON: " + str(e)

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
    data, err = _load_json(ws / "output" / "q10_runbook_diff.json")
    if err: _finish([err])
    for key in ("is_deprecated", "discrepancy_list"):
        if key not in data:
            fails.append("missing key: %s" % key)
    if fails: _finish(fails)
    if data.get("is_deprecated") is not True:
        fails.append("is_deprecated == %r (expected true)" % data.get("is_deprecated"))
    dl = data.get("discrepancy_list")
    if not isinstance(dl, list) or len(dl) < 2:
        fails.append("discrepancy_list must have >= 2 entries (got %r)" % dl)
    else:
        dl_text = " ".join(str(x) for x in dl).lower()
        # Must identify z-value discrepancy (2.33 vs 1.96)
        if not (("2.33" in dl_text or "z_alpha" in dl_text or "z-alpha" in dl_text or
                 "z alpha" in dl_text) and ("1.96" in dl_text or "alpha" in dl_text)):
            fails.append("discrepancy_list must mention z_alpha/2 discrepancy (old: 2.33, correct: 1.96)")
    _finish(fails)
main()
