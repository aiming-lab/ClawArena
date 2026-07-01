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
    data, err = _load_json(ws / "output" / "q2_pnas_summary.json")
    if err: _finish([err])
    # P3 enforced: schema_version must be "1.0"
    if str(data.get("schema_version")) != "1.0":
        fails.append("schema_version == %r (expected \"1.0\" — P3 applies to all JSON deliverables)" % data.get("schema_version"))
    n = data.get("n_total")
    try:
        n = int(n)
    except (TypeError, ValueError):
        _finish(["n_total not an int: %r" % n])
    if not (95 <= n <= 105):
        fails.append("n_total == %d (expected 101, not the Feishu bot's 201)" % n)
    nb = data.get("n_bottom")
    nt = data.get("n_top")
    try:
        if int(nb) + int(nt) != n:
            fails.append("n_bottom + n_top == %d != n_total %d" % (int(nb)+int(nt), n))
    except (TypeError, ValueError):
        fails.append("n_bottom or n_top not int: bottom=%r top=%r" % (nb, nt))
    _finish(fails)
main()
