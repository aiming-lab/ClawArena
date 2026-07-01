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
    data, err = _load_json(ws / "final" / "compliance_summary_q16.json")
    if err: _finish([err])
    if not isinstance(data, dict):
        _finish(["compliance_summary_q16.json must be a JSON object"])
    # schema_version
    if str(data.get("schema_version")) != "1.0":
        fails.append("schema_version must be '1.0'")
    # total_violations_identified: positive integer
    tvi = data.get("total_violations_identified")
    if not isinstance(tvi, int) or tvi <= 0:
        fails.append("total_violations_identified must be a positive integer")
    # violations_resolved: non-negative integer
    vr = data.get("violations_resolved")
    if not isinstance(vr, int) or vr < 0:
        fails.append("violations_resolved must be a non-negative integer")
    # active_penalty_risk_usd: positive multiple of 51744
    apr = data.get("active_penalty_risk_usd")
    try:
        apr_f = float(apr)
        if apr_f <= 0:
            fails.append("active_penalty_risk_usd must be positive")
        # Must be a multiple of 51744 (within ±100)
        remainder = apr_f % 51744.0
        if remainder > 100 and (51744.0 - remainder) > 100:
            fails.append("active_penalty_risk_usd = %s must be a multiple of 51744 (per-violation rate; NOT 45000)" % apr_f)
    except (TypeError, ValueError):
        fails.append("active_penalty_risk_usd must be a number, got: %r" % apr)
    # governing_regulations: must contain "16 CFR Part 255" AND "16 CFR Part 465"
    gov = data.get("governing_regulations")
    if not isinstance(gov, list):
        fails.append("governing_regulations must be an array")
    else:
        gov_strs = [str(x) for x in gov]
        if not any("16 CFR Part 255" in s for s in gov_strs):
            fails.append("governing_regulations must include '16 CFR Part 255'")
        if not any("16 CFR Part 465" in s for s in gov_strs):
            fails.append("governing_regulations must include '16 CFR Part 465'")
    # review_date: ISO 8601
    rd = data.get("review_date", "")
    if not re.search(r"\d{4}-\d{2}-\d{2}", str(rd)):
        fails.append("review_date must be in ISO 8601 format (YYYY-MM-DD)")
    _finish(fails)
main()
