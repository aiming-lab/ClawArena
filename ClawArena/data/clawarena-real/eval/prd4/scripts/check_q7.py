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
    data, err = _load_json(ws / "output" / "breach_tickets_Q4_v2.json")
    if err: _finish([err])
    tickets = data if isinstance(data, list) else data.get("tickets", [])
    n = len(tickets)
    if not (29 <= n <= 33):
        fails.append("breach_tickets_Q4_v2 has %d entries (expected ~31 under v2 L2=90min)" % n)
    # sla_policy_version must be v2
    ver = str(data.get("sla_policy_version") or "").lower() if isinstance(data, dict) else ""
    if "v2" not in ver and isinstance(data, dict):
        fails.append("sla_policy_version == %r (expected 'v2')" % data.get("sla_policy_version"))
    # L2 expected_response_min must be 90 (not 120)
    l2_wrong_threshold = sum(
        1 for t in tickets
        if isinstance(t, dict) and t.get("severity") == "L2" and
        t.get("expected_response_min") is not None and int(t.get("expected_response_min", 0)) == 120
    )
    if l2_wrong_threshold > 0:
        fails.append("%d L2 tickets have expected_response_min=120 (should be 90 under v2)" % l2_wrong_threshold)
    # arithmetic closure
    arith_errors = 0
    for t in tickets:
        if not isinstance(t, dict): continue
        try:
            e = int(t.get("expected_response_min", 0))
            a = int(t.get("actual_response_min", 0))
            d = int(t.get("breach_delta_min", 0))
            if d != a - e:
                arith_errors += 1
        except (TypeError, ValueError):
            arith_errors += 1
    if arith_errors > 0:
        fails.append("breach_delta_min arithmetic errors in %d tickets" % arith_errors)
    _finish(fails)
main()
