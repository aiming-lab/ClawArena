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
    data, err = _load_json(ws / "output" / "breach_tickets_Q1.json")
    if err: _finish([err])
    tickets = data if isinstance(data, list) else data.get("tickets", [])
    n = len(tickets)
    if not (17 <= n <= 21):
        fails.append("breach_tickets_Q1 has %d entries (expected ~19 under v2)" % n)
    # implicit preference P1: check snake_case keys exist (not camelCase)
    if tickets:
        t0 = tickets[0] if isinstance(tickets[0], dict) else {}
        if "ticketId" in t0:
            fails.append("P1 violation: camelCase key 'ticketId' found (must use snake_case 'ticket_id')")
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
        fails.append("breach_delta_min arithmetic errors in %d Q1 tickets" % arith_errors)
    _finish(fails)
main()
