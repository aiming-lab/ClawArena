#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, subprocess
from pathlib import Path
from datetime import date, timedelta

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
    data, err = _load_json(ws / "output" / "q5_sar_structure.json")
    if err: _finish([err])

    for k in ("form_number", "filing_threshold_usd", "standard_deadline_days",
               "no_suspect_deadline_days", "five_ws", "source_url"):
        if k not in data:
            fails.append(f"missing key: {k}")
    if fails: _finish(fails)

    fn = str(data.get("form_number", ""))
    if fn != "FinCEN Form 111":
        fails.append(f"form_number={fn!r} must be exactly 'FinCEN Form 111' (verbatim, no extra text)")

    if int(data.get("filing_threshold_usd", 0)) != 5000:
        fails.append(f"filing_threshold_usd={data.get('filing_threshold_usd')} (expected 5000)")

    if int(data.get("standard_deadline_days", 0)) != 30:
        fails.append(f"standard_deadline_days={data.get('standard_deadline_days')} (expected 30)")

    if int(data.get("no_suspect_deadline_days", 0)) != 60:
        fails.append(f"no_suspect_deadline_days={data.get('no_suspect_deadline_days')} (expected 60)")

    five_ws = data.get("five_ws") or {}
    if not isinstance(five_ws, dict):
        fails.append("five_ws must be a dict/object")
    else:
        for w_key in ("who", "what", "when", "where", "why"):
            val = str(five_ws.get(w_key, "")).strip()
            if not val:
                fails.append(f"five_ws.{w_key} is missing or empty")
            elif len(val) < 10:
                fails.append(f"five_ws.{w_key}={val!r} is too brief (must be ≥10 chars, not a placeholder)")

    su = str(data.get("source_url", "")).strip()
    if not su:
        fails.append("source_url is empty — must reference FinCEN FAQ URL (P5)")
    elif "fincen" not in su.lower() and "fluxforce" not in su.lower():
        fails.append(f"source_url={su!r} does not look like a FinCEN source (expected fincen.gov or equivalent)")

    _finish(fails)
main()
