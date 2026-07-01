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
    cspath = ws / "final" / "compliance_summary_final_20260309.json"
    if not cspath.exists():
        candidates = list((ws / "final").glob("compliance_summary_final_*.json")) if (ws / "final").exists() else []
        if candidates:
            cspath = candidates[0]
        else:
            _finish(["file not found: final/compliance_summary_final_20260309.json"])
    data, err = _load_json(cspath)
    if err: _finish([err])
    # governing_regulations must include both Part 255 and Part 465
    gr = data.get("governing_regulations") or []
    gr_txt = " ".join(str(g) for g in gr)
    if "16 CFR Part 255" not in gr_txt and "Part 255" not in gr_txt:
        fails.append("governing_regulations must include '16 CFR Part 255'")
    if "16 CFR Part 465" not in gr_txt and "Part 465" not in gr_txt:
        fails.append("governing_regulations must include '16 CFR Part 465'")
    # active_penalty_risk_usd must be a multiple of 51744 and > 0
    apr = data.get("active_penalty_risk_usd")
    try:
        apr = float(apr)
        if apr <= 0:
            fails.append("active_penalty_risk_usd must be > 0 (got %g)" % apr)
        elif round(apr) % 51744 != 0:
            fails.append("active_penalty_risk_usd must be a multiple of 51744 (got %g)" % apr)
    except (TypeError, ValueError):
        fails.append("active_penalty_risk_usd not numeric: %r" % apr)
    # b_longum_claim_status must be "insufficient_evidence"
    bls = str(data.get("b_longum_claim_status",""))
    if "insufficient" not in bls.lower():
        fails.append("b_longum_claim_status must be 'insufficient_evidence' (carry forward Q3 finding; got %r)" % bls)
    # total_violations_identified must be > 0
    tvi = data.get("total_violations_identified")
    try:
        tvi = int(tvi)
        if tvi < 3:
            fails.append("total_violations_identified must be >= 3 (got %d)" % tvi)
    except (TypeError, ValueError):
        fails.append("total_violations_identified not numeric: %r" % tvi)
    _finish(fails)
main()
