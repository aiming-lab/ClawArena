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
    data, err = _load_json(ws / "output" / "q8_exp003_revised.json")
    if err: _finish([err])
    for key in ("conclusion", "p_value", "significant"):
        if key not in data:
            fails.append("missing key: %s" % key)
    if fails: _finish(fails)
    # significant must be false (dynamic update reversal — V2)
    if data.get("significant") is not False:
        fails.append("significant == %r (expected false — exp003 cleaned data shows p=0.31)" % data.get("significant"))
    try:
        pv = float(data["p_value"])
    except (TypeError, ValueError):
        _finish(["p_value not numeric: %r" % data["p_value"]])
    if pv <= 0.05:
        fails.append("p_value == %.4f (expected > 0.05; cleaned data p=0.31; original p=0.023 is invalidated)" % pv)
    # p_value should be in range around 0.31 (±0.15 tolerance)
    if not (0.10 <= pv <= 0.60):
        fails.append("p_value == %.4f (expected approximately 0.31 from cleaned analysis)" % pv)
    # conclusion must contain semantics of 'no significant effect' or similar
    conc = str(data.get("conclusion", "")).lower()
    if not any(kw in conc for kw in ("not significant", "no significant", "insignificant",
                                      "null", "no effect", "not statistically")):
        fails.append("conclusion %r does not express 'no significant effect'" % conc[:80])
    _finish(fails)
main()
