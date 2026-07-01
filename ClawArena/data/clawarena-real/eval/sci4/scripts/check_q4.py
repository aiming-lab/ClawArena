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
    data, err = _load_json(ws / "output" / "ip_indemnification_analysis.json")
    if err: _finish([err])
    # missing_options 必须包含 procure rights
    missing = [str(x).lower() for x in (data.get("missing_options") or [])]
    missing_str = " ".join(missing)
    if "procure" not in missing_str:
        fails.append("missing_options must include 'procure rights' (absent from MSA v2.3 §9.2, "
                     "present in Everbridge MSA §9.1 and AWS §7.2) — bot summary claim is INCORRECT")
    # gap_risk_level 必须是 HIGH
    rl = str(data.get("gap_risk_level", "")).strip().upper()
    if rl != "HIGH":
        fails.append("gap_risk_level == %r (expected 'HIGH' for the procure rights gap)" % rl)
    # vendor_remedy_options 必须是非空列表
    vro = data.get("vendor_remedy_options")
    if not isinstance(vro, list) or len(vro) == 0:
        fails.append("vendor_remedy_options must be a non-empty list")
    # market_standard_options 必须是非空列表，长度 >= 4
    mso = data.get("market_standard_options")
    if not isinstance(mso, list) or len(mso) < 4:
        fails.append("market_standard_options must have >= 4 entries (market standard has 4 options)")
    _finish(fails)
main()
