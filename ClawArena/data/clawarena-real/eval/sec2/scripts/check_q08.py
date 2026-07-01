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
    data, err = _load_json(ws / "output" / "q08_aws_remediation.json")
    if err: _finish([err])
    # rule_name verbatim
    rn = str(data.get("rule_name", ""))
    if rn != "ACCESS_KEYS_ROTATED":
        fails.append("rule_name == %r (expected verbatim 'ACCESS_KEYS_ROTATED')" % rn)
    # compliance_type 枚举值
    ct = str(data.get("compliance_type", "")).upper()
    if ct not in ("COMPLIANT", "NON_COMPLIANT"):
        fails.append("compliance_type == %r (expected 'COMPLIANT' or 'NON_COMPLIANT')" % data.get("compliance_type"))
    # max_key_age_days == 90
    mkad = data.get("max_key_age_days")
    try:
        mkad = int(mkad)
    except (TypeError, ValueError):
        _finish(["max_key_age_days not an int: %r" % mkad])
    if mkad != 90:
        fails.append("max_key_age_days == %d (expected 90 — AWS Config access-keys-rotated default parameter)" % mkad)
    _finish(fails)
main()
