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
    data, err = _load_json(ws / "reports" / "revised_compliance_q8.json")
    if err: _finish([err])
    claims = data.get("claims") or data.get("items") or []
    if not isinstance(claims, list) or len(claims) < 1:
        fails.append("claims array must have at least 1 entry")
        _finish(fails)
    all_txt = " ".join(str(c) for c in claims).lower()
    # "clinically demonstrated" must be flagged as violation in revised_status
    found_clinically = False
    for c in claims:
        if not isinstance(c, dict): continue
        ct = str(c.get("claim_text","")).lower()
        if "clinically" in ct or "demonstrated" in ct:
            found_clinically = True
            if str(c.get("revised_status","")).lower() != "violation":
                fails.append("'clinically demonstrated' claim must have revised_status='violation' after CEO retraction")
    if not found_clinically:
        # check if it appears in original_status items
        if "clinically" not in all_txt:
            fails.append("revised compliance must include assessment of 'clinically demonstrated' claim")
    # B. longum consistency: if Q3 exists and said false, Q8 must also reflect that
    q3, e3 = _load_json(ws / "reports" / "evidence_assessment_q3.json")
    if not e3 and q3 is not None:
        q3_claims = q3.get("claims") or []
        for c3 in q3_claims:
            if not isinstance(c3, dict): continue
            if "longum" in str(c3.get("ingredient","")).lower():
                if c3.get("meets_ftc_standard") is False:
                    # Q8 must not suddenly say B. longum is now compliant
                    for c8 in claims:
                        if not isinstance(c8, dict): continue
                        if "longum" in str(c8.get("claim_text","")).lower():
                            if str(c8.get("revised_status","")).lower() == "compliant":
                                fails.append("V4 cross-round drift: Q8 marks B. longum compliant but Q3 said meets_ftc_standard=false")
    _finish(fails)
main()
