#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, csv, hashlib
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

PRINCIPLES = [
    "lawfulness_fairness_transparency", "purpose_limitation", "data_minimisation",
    "accuracy", "storage_limitation", "integrity_and_confidentiality"
]
VALID_STATUS = {"COMPLIANT", "PARTIAL", "MISSING"}

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "audit" / "art5_compliance_map.json")
    if err: _finish([err])
    activities = data.get("activities") if isinstance(data, dict) else None
    if not isinstance(activities, list):
        _finish(["art5_compliance_map.json must have an 'activities' list"])
    if len(activities) != 30:
        fails.append("activities count == %d (expected 30)" % len(activities))
    bad_principles = []
    for act in activities:
        if not isinstance(act, dict): continue
        aid = act.get("activity_id", "?")
        p = act.get("principles")
        if not isinstance(p, dict):
            bad_principles.append("%s: missing 'principles' object" % aid)
            continue
        for prin in PRINCIPLES:
            if prin not in p:
                bad_principles.append("%s: missing principle key %r" % (aid, prin))
            else:
                entry = p[prin]
                status = entry.get("status") if isinstance(entry, dict) else entry
                if str(status) not in VALID_STATUS:
                    bad_principles.append("%s: %s status %r not in COMPLIANT/PARTIAL/MISSING" % (aid, prin, status))
    for b in bad_principles[:6]:
        fails.append(b)
    if len(bad_principles) > 6:
        fails.append("... and %d more principle issues" % (len(bad_principles) - 6))
    # Exact-state anchors: ACT-002 is missing security_measures in the draft v1 RoPA,
    # therefore its integrity_and_confidentiality principle MUST be MISSING (not PARTIAL/COMPLIANT).
    act_map2 = {a.get("activity_id"): a for a in activities if isinstance(a, dict)}
    act002_q3 = act_map2.get("ACT-002")
    if act002_q3:
        p002 = act002_q3.get("principles", {})
        ic002 = p002.get("integrity_and_confidentiality")
        status002 = ic002.get("status") if isinstance(ic002, dict) else ic002
        if str(status002) != "MISSING":
            fails.append(
                "ACT-002 integrity_and_confidentiality status == %r "
                "(must be 'MISSING' — ACT-002 has no security_measures in ropa_controller_draft_v1.json; "
                "read the source file directly, do not assume)" % status002
            )
    # ACT-001 has security_measures in the source RoPA, so integrity_and_confidentiality must NOT be MISSING
    act001_q3 = act_map2.get("ACT-001")
    if act001_q3:
        p001 = act001_q3.get("principles", {})
        ic001 = p001.get("integrity_and_confidentiality")
        status001 = ic001.get("status") if isinstance(ic001, dict) else ic001
        if str(status001) == "MISSING":
            fails.append(
                "ACT-001 integrity_and_confidentiality status == 'MISSING' "
                "(should be COMPLIANT or PARTIAL — ACT-001 has security_measures documented in the draft v1)"
            )
    _finish(fails)
main()
