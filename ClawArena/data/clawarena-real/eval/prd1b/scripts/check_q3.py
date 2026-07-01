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
    data, err = _load_json(ws / "reports" / "evidence_assessment_q3.json")
    if err: _finish([err])
    claims = data.get("claims") or data.get("items") or []
    if not isinstance(claims, list) or len(claims) < 3:
        fails.append("claims array must have at least 3 entries (got %r)" % len(claims))
        _finish(fails)
    found_blongum = False
    found_lacidophilus = False
    for c in claims:
        if not isinstance(c, dict): continue
        ingredient = str(c.get("ingredient","")).lower() + str(c.get("claim_text","")).lower()
        mfs = c.get("meets_ftc_standard")
        if "longum" in ingredient or "digestive comfort" in ingredient:
            found_blongum = True
            if mfs is not False:
                fails.append("B. longum digestive comfort claim must have meets_ftc_standard=false (in vitro + animal only)")
            ev = str(c.get("evidence_type","")).lower()
            if "rct" in ev and "vitro" not in ev and "animal" not in ev:
                fails.append("B. longum evidence_type must reflect in vitro/animal, not RCT")
        if "acidophilus" in ingredient or "ncfm" in ingredient or "immune support" in ingredient.lower():
            if "longum" not in ingredient:
                found_lacidophilus = True
                if mfs is not True:
                    fails.append("L. acidophilus NCFM immune support must have meets_ftc_standard=true (2 RCTs)")
    if not found_blongum:
        fails.append("no entry found for B. longum / digestive comfort claim")
    _finish(fails)
main()
