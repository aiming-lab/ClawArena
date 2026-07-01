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
    data, err = _load_json(ws / "reports" / "revised_compliance_q8.json")
    if err: _finish([err])
    items = data.get("claims") if isinstance(data, dict) else None
    if items is None and isinstance(data, list):
        items = data
    if not isinstance(items, list) or len(items) == 0:
        _finish(["revised_compliance_q8.json claims array missing or empty"])
    # V2: "clinically demonstrated" must still be flagged as violation
    all_text = json.dumps(data).lower()
    if "clinically demonstrated" in all_text:
        # find the entry
        for entry in items:
            if not isinstance(entry, dict): continue
            if "clinically demonstrated" in str(entry.get("claim_text", "")).lower() or                "clinically demonstrated" in str(entry.get("claim_id", "")).lower():
                revised = str(entry.get("revised_status", "")).lower()
                if re.search(r"compliant|approved|acceptable|valid|permitted", revised):
                    fails.append("'clinically demonstrated' must remain a violation after Update 1 (CEO withdrawal doesn't change FTC standards)")
    # V4: consistency with Q3 — in vitro/animal claims must still be non-compliant
    for entry in items:
        if not isinstance(entry, dict): continue
        ev = str(entry.get("evidence_type", "")).lower()
        rev_status = str(entry.get("revised_status", "")).lower()
        if any(x in ev for x in ("in vitro", "animal", "pilot")):
            if re.search(r"compliant|accepted|standard.?met", rev_status):
                fails.append("in vitro/animal/pilot claims must remain non-compliant after Update 1 (consistent with Q3)")
    # P2: ftc_citation format
    for entry in items:
        if not isinstance(entry, dict): continue
        cit = str(entry.get("ftc_citation", ""))
        if cit and not re.search(r"16 CFR §\d", cit):
            fails.append("ftc_citation '%s' does not match '16 CFR §XXX.X' format" % cit[:40])
    _finish(fails)
main()
