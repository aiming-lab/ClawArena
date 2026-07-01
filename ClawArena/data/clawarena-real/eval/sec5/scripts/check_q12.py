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
    data, err = _load_json(ws / "output" / "q12_sar_draft.json")
    if err: _finish([err])

    for k in ("case_id", "form_number", "filing_deadline_days", "amount_reported",
               "narrative", "source_url"):
        if k not in data:
            fails.append(f"missing key: {k}")
    if fails: _finish(fails)

    # Verbatim form number
    fn = str(data.get("form_number", ""))
    if "FinCEN Form 111" not in fn:
        fails.append(f"form_number={fn!r} must contain 'FinCEN Form 111' verbatim")

    # C-rule: filing_deadline_days must match Q5 standard_deadline_days (cross-round closure)
    q5_data, q5_err = _load_json(ws / "output" / "q5_sar_structure.json")
    if q5_err:
        fails.append(f"cannot verify cross-round deadline — Q5 output missing: {q5_err}")
    else:
        q5_deadline = q5_data.get("standard_deadline_days") if q5_data else None
        q12_deadline = data.get("filing_deadline_days")
        if q5_deadline is not None and q12_deadline is not None:
            if int(q12_deadline) != int(q5_deadline):
                fails.append(
                    f"filing_deadline_days={q12_deadline} does not match Q5.standard_deadline_days={q5_deadline} "
                    f"— cross-round consistency required"
                )
        elif int(data.get("filing_deadline_days", 0)) != 30:
            fails.append(f"filing_deadline_days={data.get('filing_deadline_days')} (expected 30)")

    # C-rule: case_id must exactly match the highest-amount case in open_cases.json
    oc_data, oc_err = _load_json(ws / "cases" / "open_cases.json")
    if oc_err:
        fails.append(f"cannot verify case_id — open_cases.json missing: {oc_err}")
    else:
        oc_cases = oc_data.get("cases", []) if oc_data else []
        eligible = [c for c in oc_cases if float(c.get("amount_usd", 0)) >= 5000]
        if eligible:
            top_case = max(eligible, key=lambda c: float(c.get("amount_usd", 0)))
            expected_cid = top_case.get("case_id")
            got_cid = str(data.get("case_id", ""))
            if expected_cid and got_cid != expected_cid:
                fails.append(
                    f"case_id={got_cid!r} — must be exactly {expected_cid!r} (highest-amount case "
                    f"${float(top_case.get('amount_usd',0)):,.2f} from open_cases.json)"
                )

    # amount_reported >= 5000, exactly 2dp
    amt = data.get("amount_reported")
    if amt is None:
        fails.append("amount_reported is missing")
    else:
        try:
            amt_f = float(amt)
        except (TypeError, ValueError):
            fails.append(f"amount_reported={amt!r} is not a number")
            amt_f = 0
        if amt_f < 5000:
            fails.append(f"amount_reported={amt_f} must be >= 5000 (SAR threshold)")
        parts = f"{amt_f:.10f}".rstrip("0").split(".")
        dp = len(parts[1]) if len(parts) > 1 else 0
        if dp > 2:
            fails.append(f"amount_reported={amt_f} has >2 decimal places (P4)")

    # Narrative five-W structure
    narrative = data.get("narrative") or {}
    if not isinstance(narrative, dict):
        fails.append("narrative must be an object with who/what/when/where/why keys")
    else:
        for w_key in ("who", "what", "when", "where", "why"):
            val = narrative.get(w_key)
            if not val or not str(val).strip():
                fails.append(f"narrative.{w_key} is missing or empty (P3: five-W structure required)")

    if not str(data.get("source_url", "")).strip():
        fails.append("source_url is empty (P5)")

    _finish(fails)
main()
