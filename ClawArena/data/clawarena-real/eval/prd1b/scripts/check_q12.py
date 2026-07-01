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
    data, err = _load_json(ws / "reports" / "final_compliance_q12.json")
    if err: _finish([err])
    # update_source must be exactly "email_revised_audit_v2"
    us = str(data.get("update_source",""))
    if us != "email_revised_audit_v2":
        fails.append("update_source must be exactly 'email_revised_audit_v2' (got %r)" % us)
    # doctor_formulated_requires_substantiation must be True
    dfrs = data.get("doctor_formulated_requires_substantiation")
    if dfrs is not True:
        fails.append("doctor_formulated_requires_substantiation must be true (revised audit letter changed the position)")
    # superseded_items must be non-empty
    sup = data.get("superseded_items") or []
    if not isinstance(sup, list) or len(sup) == 0:
        fails.append("superseded_items must be a non-empty array")
    # active_items must be non-empty
    act = data.get("active_items") or []
    if not isinstance(act, list) or len(act) == 0:
        fails.append("active_items must be a non-empty array")
    # At least some entries must have ftc_citation
    all_items = (sup if isinstance(sup, list) else []) + (act if isinstance(act, list) else [])
    has_citation = any(
        isinstance(it, dict) and re.match(r"16 CFR §\d", str(it.get("ftc_citation","")))
        for it in all_items
    )
    if not has_citation and len(all_items) > 0:
        fails.append("items in superseded_items or active_items must include ftc_citation in '16 CFR §XXX.X' format")
    # superseded_items must reference Doctor-Formulated conditional permission
    sup_txt = " ".join(str(s) for s in sup).lower()
    if "doctor" not in sup_txt and "physician" not in sup_txt and "formulated" not in sup_txt:
        fails.append("superseded_items must include the March 7 conditional permission for 'Doctor-Formulated' claim")
    _finish(fails)
main()
