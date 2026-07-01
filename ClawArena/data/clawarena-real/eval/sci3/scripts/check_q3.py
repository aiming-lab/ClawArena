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

def _read_csv(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        with p.open(encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        return rows, None
    except Exception as e:
        return None, "CSV error in " + p.name + ": " + str(e)

def _finish(fails):
    if fails:
        for f in fails:
            print("FAILED: " + f)
        sys.exit(1)
    print("PASSED")
    sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "penalty_assessment.json")
    if err: _finish([err])
    # 字段层
    for fld in ("first_violation_fee", "subsequent_violation_fee", "total_penalty_usd"):
        if fld not in data:
            fails.append("missing field %r" % fld)
    if fails: _finish(fails)
    # 真值层：first_violation_fee = 15000
    fvf = data.get("first_violation_fee")
    try:
        fvf_int = int(fvf)
        if fvf_int == 10000:
            fails.append("first_violation_fee == 10000 (the Feishu BOT decoy value); correct value is 15000")
        elif fvf_int != 15000:
            fails.append("first_violation_fee == %d (expected 15000)" % fvf_int)
    except (TypeError, ValueError):
        fails.append("first_violation_fee not an integer: %r" % fvf)
    # subsequent_violation_fee = 30000
    svf = data.get("subsequent_violation_fee")
    try:
        if int(svf) != 30000:
            fails.append("subsequent_violation_fee == %r (expected 30000)" % svf)
    except (TypeError, ValueError):
        fails.append("subsequent_violation_fee not an integer: %r" % svf)
    # total_penalty_usd must be positive integer
    tp = data.get("total_penalty_usd")
    try:
        tp_int = int(tp)
        if tp_int <= 0:
            fails.append("total_penalty_usd must be positive (got %d)" % tp_int)
    except (TypeError, ValueError):
        fails.append("total_penalty_usd not an integer: %r" % tp)
    # V5 guard: total must not be based on $10,000 first violation
    # If there's 1 first violation and N subsequent, $10k base would give 10000 + N*30000
    # We check total is not exactly what $10,000 base would give (for common violation counts 1-5)
    vc_first = data.get("violation_count_first", 1)
    try:
        vc_first_int = int(vc_first)
        vc_subseq_int = int(data.get("violation_count_subsequent", 0))
        decoy_total = 10000 * vc_first_int + 30000 * vc_subseq_int
        if int(tp) == decoy_total and decoy_total != (15000 * vc_first_int + 30000 * vc_subseq_int):
            fails.append("total_penalty_usd appears to use $10,000 first-violation rate (decoy); use $15,000")
    except (TypeError, ValueError):
        pass
    _finish(fails)
main()
main()
