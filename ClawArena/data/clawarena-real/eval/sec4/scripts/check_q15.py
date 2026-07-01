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

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "audit" / "penalty_mapping.json")
    if err: _finish([err])
    gaps = data.get("gaps") if isinstance(data, dict) else None
    if not isinstance(gaps, list):
        _finish(["penalty_mapping.json must have a 'gaps' list"])
    if len(gaps) < 7:
        fails.append(
            "gaps list has %d items (expected >= 7; include Art.30 RoPA gaps, DSAR deadline failures, "
            "DPIA absence, security documentation, AI register omission, Art.5 principle gaps)" % len(gaps)
        )
    tier2_count = 0
    for g in gaps:
        if not isinstance(g, dict): continue
        av = str(g.get("article_violated", ""))
        tier = g.get("tier")
        # V9: article_violated must use format "Art. X(Y)(Z)" or "Art. X(Y)"
        if not re.search(r"Art\.\s*\d+\(\d+\)", av):
            fails.append("gap %s: article_violated %r does not use format 'Art. X(Y)(Z)'" % (g.get("gap_id","?"), av))
        try:
            if int(tier) == 2:
                tier2_count += 1
        except (TypeError, ValueError):
            fails.append("gap %s: tier %r is not an int" % (g.get("gap_id","?"), tier))
    if tier2_count < 4:
        fails.append(
            "only %d tier-2 gaps (expected >= 4 substantive violations under Art. 83(5))" % tier2_count
        )
    _finish(fails)
main()
