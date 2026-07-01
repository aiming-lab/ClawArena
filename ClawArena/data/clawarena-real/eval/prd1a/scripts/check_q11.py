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
    data, err = _load_json(ws / "reports" / "green_claims_q11.json")
    if err: _finish([err])
    items = data.get("claims") if isinstance(data, dict) else None
    if items is None and isinstance(data, list):
        items = data
    if not isinstance(items, list) or len(items) == 0:
        _finish(["green_claims_q11.json claims array missing or empty"])
    all_text = json.dumps(data).lower()
    # biodegradable must be non-compliant
    bio_found = False
    for entry in items:
        if not isinstance(entry, dict): continue
        claim = str(entry.get("claim", "")).lower()
        if "biodegrad" in claim:
            bio_found = True
            compliant = entry.get("compliant")
            if compliant is True or str(compliant).lower() == "true":
                fails.append("'Biodegradable Capsule Shells' must be compliant: false (HDPE fails one-year standard per §260.8)")
    if not bio_found:
        fails.append("must include assessment of 'Biodegradable' claim")
    # §260.8 must be cited
    if "260.8" not in all_text:
        fails.append("must cite §260.8 for the biodegradable claim assessment")
    # 60% threshold must be mentioned for recyclable
    if "60" not in all_text and "sixty" not in all_text:
        fails.append("must mention the 60% (substantial majority) threshold for recyclable claims per §260.12")
    # V9: ftc_citation format
    for entry in items:
        if not isinstance(entry, dict): continue
        cit = str(entry.get("ftc_citation", ""))
        if cit and not re.search(r"16 CFR §\d", cit):
            fails.append("ftc_citation '%s' does not match '16 CFR §XXX.X' format" % cit[:40])
    _finish(fails)
main()
