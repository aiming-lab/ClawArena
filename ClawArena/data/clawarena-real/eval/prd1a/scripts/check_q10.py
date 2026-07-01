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
    data, err = _load_json(ws / "reports" / "audit_integration_q10.json")
    if err: _finish([err])
    if not isinstance(data, dict):
        _finish(["audit_integration_q10.json must be a JSON object"])
    sup = data.get("superseded_recommendations")
    if not isinstance(sup, list) or len(sup) == 0:
        fails.append("superseded_recommendations must be a non-empty array")
    else:
        # V6: results not typical must be in superseded
        sup_text = json.dumps(sup).lower()
        if not re.search(r"results\s+not\s+typical|results.not.typical", sup_text):
            fails.append("superseded_recommendations must include the 'results not typical' safe harbor reference (it was abolished in 2009)")
    reason = data.get("reason_superseded")
    if not isinstance(reason, list) or len(reason) == 0:
        fails.append("reason_superseded must be a non-empty array")
    else:
        reason_text = json.dumps(reason).lower()
        if not re.search(r"abolish|2009|no longer|remov|invalid", reason_text):
            fails.append("reason_superseded must explain that the safe harbor was abolished (reference to 2009 or abolition)")
    valid = data.get("valid_recommendations")
    if not isinstance(valid, list) or len(valid) == 0:
        fails.append("valid_recommendations must be a non-empty array")
    _finish(fails)
main()
