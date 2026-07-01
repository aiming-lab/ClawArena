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
    data, err = _load_json(ws / "output" / "breach_tickets_Q4.json")
    if err: _finish([err])
    tickets = data if isinstance(data, list) else data.get("tickets", [])
    n = len(tickets)
    # 真值层：28 breaches under v1, allow +/-2 tolerance for edge cases
    if not (26 <= n <= 30):
        fails.append("breach_tickets_Q4 has %d entries (expected ~28 under v1 L1=30/L2=120/L3=480/L4=1440)" % n)
    # 字段层 + 算术闭合
    arith_errors = 0
    for t in tickets:
        if not isinstance(t, dict):
            continue
        exp = t.get("expected_response_min")
        act = t.get("actual_response_min")
        delta = t.get("breach_delta_min")
        try:
            exp_i = int(exp); act_i = int(act); delta_i = int(delta)
            if delta_i != act_i - exp_i:
                arith_errors += 1
        except (TypeError, ValueError):
            arith_errors += 1
    if arith_errors > 0:
        fails.append("breach_delta_min arithmetic error in %d tickets (must equal actual - expected)" % arith_errors)
    _finish(fails)
main()
