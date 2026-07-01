#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, csv
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
    data, err = _load_json(ws / "legal" / "eeoc_complaint_draft.json")
    if err: _finish([err])
    # bases_of_discrimination must include age AND FMLA retaliation
    bases = [str(x).lower() for x in (data.get("bases_of_discrimination") or [])]
    bases_text = " ".join(bases)
    if not re.search(r"age|adea", bases_text):
        fails.append("bases_of_discrimination must include age discrimination / ADEA")
    if not re.search(r"fmla.retaliat|retaliat.*fmla", bases_text):
        fails.append("bases_of_discrimination must include FMLA retaliation")
    # C: complainant must identify Marcus Webb with employee ID EMP-0042
    complainant = str(data.get("complainant") or "")
    if not re.search(r"marcus.webb", complainant, re.I):
        fails.append("complainant must reference \'Marcus Webb\' (got %r)" % complainant)
    if "EMP-0042" not in complainant:
        fails.append("complainant must include employee ID \'EMP-0042\' (required for record identification; got %r)" % complainant)
    # filing_deadline must match Q9 output (2026-07-08) — V4 cross-round closure
    fd = str(data.get("filing_deadline") or "")
    # also check Q9 output for cross-round consistency
    q9, e9 = _load_json(ws / "reports" / "eeoc_deadline.json")
    if not e9 and q9 is not None:
        q9_dd = str(q9.get("deadline_date") or "")
        if fd and q9_dd and fd != q9_dd:
            fails.append("filing_deadline %r does not match Q9 eeoc_deadline.deadline_date %r (cross-round consistency required)" % (fd, q9_dd))
    if "2026-07-08" not in fd:
        fails.append("filing_deadline must contain 2026-07-08 (300 days from 2025-09-12; got %r)" % fd)
    # C: date_of_harm must match termination_date from Q3 fmla_timeline.json
    doh = str(data.get("date_of_harm") or "")
    q3, e3 = _load_json(ws / "reports" / "fmla_timeline.json")
    if not e3 and q3 is not None:
        q3_term = str(q3.get("termination_date") or "")
        if doh and q3_term and doh != q3_term:
            fails.append("date_of_harm %r does not match Q3 fmla_timeline.termination_date %r (cross-round consistency: use the personnel file date, not the Slack DM date)" % (doh, q3_term))
    if "2025-09-12" not in doh:
        fails.append("date_of_harm must be 2025-09-12 (Marcus Webb\'s termination date per personnel file; got %r)" % doh)
    _finish(fails)
main()
