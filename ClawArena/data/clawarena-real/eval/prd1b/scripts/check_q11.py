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
    data, err = _load_json(ws / "reports" / "green_claims_q11.json")
    if err: _finish([err])
    claims = data.get("claims") or data.get("items") or []
    if not isinstance(claims, list) or len(claims) < 2:
        fails.append("claims array must have at least 2 entries (got %r)" % len(claims))
        _finish(fails)
    found_bio = found_recyclable = found_eco = False
    for c in claims:
        if not isinstance(c, dict): continue
        ct = str(c.get("claim_text","")).lower()
        cit = str(c.get("ftc_citation",""))
        comp = c.get("compliant")
        if "biodegradable" in ct or "biodegrad" in ct:
            found_bio = True
            if comp is not False:
                fails.append("'Biodegradable formula capsules' must have compliant=false (§260.8: no 1-year degradation)")
            if cit and "260.8" not in cit and "260" not in cit:
                fails.append("biodegradable entry should cite §260.8 (got %r)" % cit[:30])
        elif "recyclable" in ct or "recycle" in ct:
            found_recyclable = True
            if comp is not True:
                fails.append("'Recyclable PET bottle' must have compliant=true (78% coverage > 60% §260.12 threshold)")
            if cit and "260.12" not in cit and "260" not in cit:
                fails.append("recyclable entry should cite §260.12 (got %r)" % cit[:30])
        elif "eco-friendly" in ct or "eco friendly" in ct:
            found_eco = True
            if comp is not False:
                fails.append("'Eco-friendly packaging' must have compliant=false (unsupported general claim)")
    if not found_bio:
        fails.append("no entry found for 'biodegradable' claim")
    if not found_recyclable:
        fails.append("no entry found for 'recyclable' claim")
    _finish(fails)
main()
