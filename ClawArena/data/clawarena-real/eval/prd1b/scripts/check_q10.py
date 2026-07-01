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
    data, err = _load_json(ws / "reports" / "audit_integration_q10.json")
    if err: _finish([err])
    # superseded_recommendations must exist and be non-empty
    sup = data.get("superseded_recommendations") or []
    if not isinstance(sup, list) or len(sup) == 0:
        fails.append("superseded_recommendations must be a non-empty array")
        _finish(fails)
    sup_txt = " ".join(str(s) for s in sup).lower()
    # 'results not typical' safe harbor must be in superseded
    if not re.search(r"results not typical|safe harbor|1980|2009|abolish|abolit", sup_txt):
        fails.append("superseded_recommendations must include the 'Results Not Typical' safe harbor recommendation (abolished 2009)")
    # valid_recommendations must not reference the 1980/1998 guides as current
    valid = data.get("valid_recommendations") or []
    valid_txt = " ".join(str(v) for v in valid).lower()
    if "1980" in valid_txt and "supersed" not in valid_txt:
        fails.append("valid_recommendations must not cite 1980 Guides as current law")
    if "1998" in valid_txt and "supersed" not in valid_txt:
        fails.append("valid_recommendations must not cite 1998 Dietary Supplements Guide as current (replaced by Dec 2022 guidance)")
    # reason_superseded must exist and be non-empty
    rs = data.get("reason_superseded") or []
    if not isinstance(rs, list) or len(rs) == 0:
        fails.append("reason_superseded must be a non-empty array")
    _finish(fails)
main()
