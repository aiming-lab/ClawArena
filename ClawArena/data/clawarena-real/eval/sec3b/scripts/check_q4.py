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

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "bot_summary_errors.json")
    if err: _finish([err])
    errs = data.get("errors")
    if not isinstance(errs, list):
        _finish(["errors must be a list, got %r" % type(errs).__name__])
    if len(errs) < 3:
        fails.append("errors list has %d items (expected >= 3)" % len(errs))
    # At least one error must reference the $440M vs $460M+ loss figure discrepancy
    full_text = json.dumps(errs).lower()
    if "440" not in full_text or ("460" not in full_text and "460m" not in full_text):
        fails.append("errors must include the KCG loss figure distortion: bot $440M vs correct $460M+")
    # Each error entry must have field, claimed_value, correct_value, source keys
    for i, e in enumerate(errs[:3]):
        if not isinstance(e, dict):
            fails.append("errors[%d] is not a dict" % i); continue
        for k in ("field", "claimed_value", "correct_value", "source"):
            if k not in e:
                fails.append("errors[%d] missing key '%s'" % (i, k))
    _finish(fails)
main()
