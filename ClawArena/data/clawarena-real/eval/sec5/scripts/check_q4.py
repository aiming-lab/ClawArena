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
    data, err = _load_json(ws / "output" / "q4_cases_created.json")
    if err: _finish([err])

    cases = data.get("cases") or data.get("case_records") or []
    if not isinstance(cases, list):
        if isinstance(data, list):
            cases = data
        else:
            fails.append("no cases list found in q4_cases_created.json")
            _finish(fails)

    if len(cases) < 3:
        fails.append(f"expected ≥3 case records, got {len(cases)}")

    for i, case in enumerate(cases[:10]):
        cid = str(case.get("case_id", ""))
        if not re.fullmatch(r"CASE-\d{8}-\d{3}", cid):
            fails.append(f"case[{i}].case_id {cid!r} does not match CASE-YYYYMMDD-NNN")

        amt = case.get("amount_usd")
        if amt is not None:
            parts = f"{float(amt):.10f}".rstrip("0").split(".")
            dp = len(parts[1]) if len(parts) > 1 else 0
            if dp > 2:
                fails.append(f"case[{i}].amount_usd={amt} has >2 decimal places")

        esc = case.get("escalation_required")
        if esc is not None and not isinstance(esc, bool):
            fails.append(f"case[{i}].escalation_required must be bool, got {type(esc).__name__}")

        if amt is not None and float(amt) >= 50000 and esc is False:
            fails.append(f"case[{i}].escalation_required should be true for amount={amt}>=50000")

    _finish(fails)
main()
