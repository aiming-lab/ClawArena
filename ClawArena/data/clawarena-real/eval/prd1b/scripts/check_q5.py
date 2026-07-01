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
    data, err = _load_json(ws / "reports" / "influencer_audit_summary_q5.json")
    if err: _finish([err])
    # total_posts_audited
    total = data.get("total_posts_audited")
    try:
        total = int(total)
        if not (900 <= total <= 1400):
            fails.append("total_posts_audited == %d (expected ~1200)" % total)
    except (TypeError, ValueError):
        fails.append("total_posts_audited not numeric: %r" % total)
    # non_compliant_posts must be around 830
    nc = data.get("non_compliant_posts")
    try:
        nc = int(nc)
        if not (750 <= nc <= 900):
            fails.append("non_compliant_posts == %d (expected ~830)" % nc)
    except (TypeError, ValueError):
        fails.append("non_compliant_posts not numeric: %r" % nc)
    # penalty_per_violation must be 51744 (not 45000 DECOY)
    ppv = data.get("penalty_per_violation")
    try:
        ppv = int(float(ppv))
        if ppv == 45000:
            fails.append("penalty_per_violation == 45000 (DECOY figure — correct 2024 rate is 51744)")
        elif ppv != 51744:
            fails.append("penalty_per_violation == %d (expected 51744 per 16 CFR Part 465)" % ppv)
    except (TypeError, ValueError):
        fails.append("penalty_per_violation not numeric: %r" % ppv)
    # total_penalty_exposure_usd must be 830 * 51744 = 42947520 (±10%)
    tpe = data.get("total_penalty_exposure_usd")
    try:
        tpe = int(float(tpe))
        expected = 830 * 51744
        if not (expected * 0.9 <= tpe <= expected * 1.1):
            fails.append("total_penalty_exposure_usd == %d (expected ~%d)" % (tpe, expected))
    except (TypeError, ValueError):
        fails.append("total_penalty_exposure_usd not numeric: %r" % tpe)
    # ftc_citation must be present
    cit = str(data.get("ftc_citation",""))
    if not cit or not re.match(r"16 CFR §\d", cit):
        fails.append("top-level ftc_citation must be '16 CFR §255.5' or similar (got %r)" % cit[:30])
    _finish(fails)
main()
