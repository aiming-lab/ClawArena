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
    data, err = _load_json(ws / "output" / "negotiation_position.json")
    if err: _finish([err])
    # our_position_months 必须是 12（与 Q2 一致）
    op = data.get("our_position_months")
    try:
        op = int(op)
    except (TypeError, ValueError):
        _finish(["our_position_months not an int: %r" % op])
    if op != 12:
        fails.append("our_position_months == %d (expected 12 — must be consistent with Q2 cap_months and market standard)" % op)
    # vendor_position_months 必须是 6（来自 v2.4）
    vp = data.get("vendor_position_months")
    try:
        vp = int(vp)
    except (TypeError, ValueError):
        _finish(["vendor_position_months not an int: %r" % vp])
    if vp != 6:
        fails.append("vendor_position_months == %d (expected 6 — VendorX's v2.4 counter-proposal)" % vp)
    # market_standard_months 必须是 12
    ms = data.get("market_standard_months")
    try:
        ms = int(ms)
    except (TypeError, ValueError):
        _finish(["market_standard_months not an int: %r" % ms])
    if ms != 12:
        fails.append("market_standard_months == %d (expected 12 per Everbridge MSA §10 and AWS §9.2)" % ms)
    # supporting_sources 必须含 Everbridge 或 AWS 引用
    ss = [str(x).lower() for x in (data.get("supporting_sources") or [])]
    ss_str = " ".join(ss)
    if "everbridge" not in ss_str and "aws" not in ss_str:
        fails.append("supporting_sources must reference Everbridge MSA §10 or AWS §9.2 as market benchmark")
    # cross-round consistency: Q2 cap_months must equal our_position_months if Q2 exists
    q2, e2 = _load_json(ws / "output" / "liability_cap.json")
    if not e2 and q2 is not None:
        q2_cm = q2.get("cap_months")
        try:
            q2_cm = int(q2_cm)
            if q2_cm != op:
                fails.append("cross-round drift: Q8 our_position_months=%d != Q2 cap_months=%d" % (op, q2_cm))
        except (TypeError, ValueError):
            pass
    _finish(fails)
main()
