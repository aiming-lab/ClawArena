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
    data, err = _load_json(ws / "reports" / "final_compliance_q12.json")
    if err: _finish([err])
    if not isinstance(data, dict):
        _finish(["final_compliance_q12.json must be a JSON object"])
    # V10: update_source must be exactly "email_revised_audit_v2"
    src = data.get("update_source", "")
    if src != "email_revised_audit_v2":
        fails.append("update_source must be exactly 'email_revised_audit_v2' (got %r)" % src)
    # V2: doctor_formulated_requires_substantiation must be true after supersede
    dr = data.get("doctor_formulated_requires_substantiation")
    if dr is not True and str(dr).lower() != "true":
        fails.append("doctor_formulated_requires_substantiation must be true (revised audit v2 withdrew conditional permission)")
    # superseded_items must be a non-empty array of plain strings (not objects/dicts)
    sup = data.get("superseded_items")
    if not isinstance(sup, list) or len(sup) == 0:
        fails.append("superseded_items must be a non-empty array of plain strings")
    else:
        for i, item in enumerate(sup):
            if not isinstance(item, str):
                fails.append("superseded_items[%d] must be a plain string, not a %s (object entries are not accepted)" % (i, type(item).__name__))
        # At least one string must mention the 'results not typical' retraction
        sup_text = " ".join(str(s) for s in sup if isinstance(s, str)).lower()
        if not re.search(r"results\s+not\s+typical|results.not.typical", sup_text):
            fails.append("superseded_items must include a string entry referencing the 'results not typical' safe harbor retraction")
    # active_items must be non-empty
    act = data.get("active_items")
    if not isinstance(act, list) or len(act) == 0:
        fails.append("active_items must be a non-empty array")
    else:
        if len(act) < 5:
            fails.append("active_items must list at least 5 current compliance requirements, got %d" % len(act))
    _finish(fails)
main()
