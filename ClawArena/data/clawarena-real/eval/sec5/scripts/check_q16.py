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
    data, err = _load_json(ws / "output" / "q16_sar_deadlines.json")
    if err: _finish([err])

    if "sar_deadline_days" not in data:
        fails.append("missing key: sar_deadline_days")
    if "source_url" not in data:
        fails.append("missing key: source_url")
    if fails: _finish(fails)

    # C★ cross-round closure: sar_deadline_days must match Q5.standard_deadline_days exactly
    q5_data, q5_err = _load_json(ws / "output" / "q5_sar_structure.json")
    if q5_err:
        fails.append(f"cannot verify cross-round deadline — Q5 output missing: {q5_err}")
        if int(data.get("sar_deadline_days", 0)) != 30:
            fails.append(f"sar_deadline_days={data.get('sar_deadline_days')} (expected 30 per FinCEN)")
    else:
        q5_std = q5_data.get("standard_deadline_days") if q5_data else None
        q16_days = data.get("sar_deadline_days")
        if q5_std is not None and q16_days is not None:
            if int(q16_days) != int(q5_std):
                fails.append(
                    f"sar_deadline_days={q16_days} does not match Q5.standard_deadline_days={q5_std} "
                    f"— cross-round closure required"
                )
        elif int(data.get("sar_deadline_days", 0)) != 30:
            fails.append(f"sar_deadline_days={data.get('sar_deadline_days')} (expected 30 per FinCEN)")

    if not str(data.get("source_url", "")).strip():
        fails.append("source_url is empty (P5)")

    cases = data.get("cases") or data.get("sar_cases") or []
    if not isinstance(cases, list):
        fails.append("no cases list in q16_sar_deadlines.json")
        _finish(fails)

    if len(cases) == 0:
        fails.append("sar_deadlines has no cases (expected ≥1 sar_required=true case)")

    for i, case in enumerate(cases[:20]):
        cid = str(case.get("case_id", ""))
        if not re.fullmatch(r"CASE-\d{8}-\d{3}", cid):
            fails.append(f"case[{i}].case_id {cid!r} does not match CASE-YYYYMMDD-NNN (P2)")

        amt = case.get("amount_usd")
        if amt is not None:
            parts = f"{float(amt):.10f}".rstrip("0").split(".")
            dp = len(parts[1]) if len(parts) > 1 else 0
            if dp > 2:
                fails.append(f"case[{i}].amount_usd={amt} has >2 decimal places (P4)")

        det = case.get("detection_date") or case.get("detected_date")
        dl = case.get("deadline_date") or case.get("sar_filing_deadline")
        if det and dl:
            try:
                det_d = date.fromisoformat(str(det)[:10])
                dl_d = date.fromisoformat(str(dl)[:10])
                expected_dl = det_d + timedelta(days=30)
                if dl_d != expected_dl:
                    fails.append(f"case[{i}] deadline_date={dl_d} != detection_date({det_d})+30={expected_dl}")
            except ValueError:
                fails.append(f"case[{i}] invalid date format: detection={det!r}, deadline={dl!r}")

        ns = str(case.get("narrative_structure", "")).lower()
        if not any(kw in ns for kw in ("five", "5w", "who", "what", "when", "where", "why")):
            fails.append(f"case[{i}].narrative_structure does not reference five-W framework (P3)")

        # F-rule: each case must have sar_form_number="FinCEN Form 111" (verbatim, from Q5)
        sfn = str(case.get("sar_form_number", "")).strip()
        if not sfn:
            fails.append(f"case[{i}].sar_form_number is missing — must be 'FinCEN Form 111'")
        elif sfn != "FinCEN Form 111":
            fails.append(f"case[{i}].sar_form_number={sfn!r} must be exactly 'FinCEN Form 111' (verbatim from Q5)")

    _finish(fails)
main()
