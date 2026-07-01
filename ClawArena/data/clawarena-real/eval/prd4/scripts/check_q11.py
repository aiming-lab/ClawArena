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
    data, err = _load_json(ws / "output" / "breach_tickets_Q4_v3.json")
    if err: _finish([err])
    tickets = data if isinstance(data, list) else data.get("tickets", [])
    # sla_policy_version=v3
    if isinstance(data, dict):
        ver = str(data.get("sla_policy_version") or "").lower()
        if "v3" not in ver:
            fails.append("sla_policy_version == %r (expected 'v3')" % data.get("sla_policy_version"))
    # supersede_notice must reference FEISHU-PRD4-L2-REVERT
    if isinstance(data, dict):
        notice = str(data.get("supersede_notice") or "").lower()
        if "feishu" not in notice and "revert" not in notice and "l2" not in notice:
            fails.append("supersede_notice == %r (must reference FEISHU-PRD4-L2-REVERT or L2 revert)" % data.get("supersede_notice"))
    # V10: L2 expected_response_min must be 120 (NOT 90 from v2)
    l2_v2_threshold = sum(
        1 for t in tickets
        if isinstance(t, dict) and t.get("severity") == "L2" and
        t.get("expected_response_min") is not None and int(t.get("expected_response_min", 0)) == 90
    )
    if l2_v2_threshold > 0:
        fails.append("%d L2 tickets still use expected_response_min=90 (must revert to 120)" % l2_v2_threshold)
    # patch: breach count should be LESS than v1's 28 (5 tickets corrected to compliant)
    n = len(tickets)
    if n >= 28:
        fails.append("v3 breach count %d >= 28 (patch should have corrected 5 breach→compliant tickets)" % n)
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
        fails.append("breach_delta_min arithmetic errors in %d v3 tickets" % arith_errors)
    _finish(fails)
main()
