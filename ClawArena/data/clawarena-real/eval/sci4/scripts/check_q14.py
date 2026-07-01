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
    data, err = _load_json(ws / "output" / "final_contract_summary.json")
    if err: _finish([err])
    # final_version 必须是 v2.5
    fv = str(data.get("final_version", "")).strip()
    if "2.5" not in fv:
        fails.append("final_version == %r (expected 'v2.5' — the final agreed version)" % fv)
    # final_cap_months 必须是 12（从 v2.4 的 6 个月恢复，须与 Q2/Q8 一致）
    fcm = data.get("final_cap_months")
    try:
        fcm = int(fcm)
    except (TypeError, ValueError):
        _finish(["final_cap_months not an int: %r" % fcm])
    if fcm != 12:
        fails.append("final_cap_months == %d (expected 12 — v2.5 restores TechCo's position; "
                     "v2.4's 6-month regression was rejected)" % fcm)
    # ip_remedy_options_count 必须是 4（含 procure rights）
    irc = data.get("ip_remedy_options_count")
    try:
        irc = int(irc)
    except (TypeError, ValueError):
        _finish(["ip_remedy_options_count not an int: %r" % irc])
    if irc != 4:
        fails.append("ip_remedy_options_count == %d (expected 4 — procure rights reinstated in v2.5)" % irc)
    # cross-round closure: final_cap_months must equal Q2 and Q8 positions
    q2, e2 = _load_json(ws / "output" / "liability_cap.json")
    if not e2 and q2 is not None:
        try:
            q2_cm = int(q2.get("cap_months"))
            if q2_cm != fcm:
                fails.append("cross-round drift: Q14 final_cap_months=%d != Q2 cap_months=%d" % (fcm, q2_cm))
        except (TypeError, ValueError):
            pass
    q8, e8 = _load_json(ws / "output" / "negotiation_position.json")
    if not e8 and q8 is not None:
        try:
            q8_op = int(q8.get("our_position_months"))
            if q8_op != fcm:
                fails.append("cross-round drift: Q14 final_cap_months=%d != Q8 our_position_months=%d" % (fcm, q8_op))
        except (TypeError, ValueError):
            pass
    _finish(fails)
main()
