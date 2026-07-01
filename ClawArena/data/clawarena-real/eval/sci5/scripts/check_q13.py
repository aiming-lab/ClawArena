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
    p = ws / "reports" / "risk_matrix_final.csv"
    if not p.exists():
        _finish(["file not found: reports/risk_matrix_final.csv"])
    # P5: UTF-8 with BOM
    raw = p.read_bytes()
    if not raw.startswith(b"\xef\xbb\xbf"):
        fails.append("risk_matrix_final.csv must begin with UTF-8 BOM bytes (\xef\xbb\xbf) per P5")
    # parse CSV
    try:
        text = raw[3:].decode("utf-8") if raw.startswith(b"\xef\xbb\xbf") else raw.decode("utf-8")
        rows = list(csv.DictReader(text.splitlines()))
    except Exception as e:
        _finish(["CSV parse error: " + str(e)])
    # A: >= 8 data rows (expanded from 6 — covers all major risk areas in this scenario)
    if len(rows) < 8:
        fails.append("risk_matrix_final.csv must have >= 8 data rows covering all major risk areas (got %d)" % len(rows))
    # severity values
    valid_sev = {"HIGH", "MEDIUM", "LOW"}
    for r in rows:
        sev = str(r.get("severity") or "").strip().upper()
        if sev not in valid_sev:
            fails.append("row %r has invalid severity %r (must be HIGH, MEDIUM, or LOW)" % (r.get("risk_id"), sev))
        # D: recommended_action must not be empty
        ra = str(r.get("recommended_action") or "").strip()
        if not ra:
            fails.append("row %r has empty recommended_action (every risk row must include a concrete action)" % r.get("risk_id"))
    # FMLA row must be HIGH
    fmla_rows = [r for r in rows if re.search(r"fmla", str(r.get("law") or "") + str(r.get("risk_description") or ""), re.I)]
    if not fmla_rows:
        fails.append("no FMLA risk row found in risk_matrix_final.csv")
    else:
        for r in fmla_rows:
            if str(r.get("severity") or "").strip().upper() != "HIGH":
                fails.append("FMLA risk row must have severity HIGH (got %r)" % r.get("severity"))
    # Cal-WARN row must be HIGH
    cal_rows = [r for r in rows if re.search(r"cal.warn|california.warn|cal_warn", str(r.get("law") or "") + str(r.get("risk_description") or ""), re.I)]
    if not cal_rows:
        fails.append("no Cal-WARN risk row found in risk_matrix_final.csv")
    else:
        for r in cal_rows:
            if str(r.get("severity") or "").strip().upper() != "HIGH":
                fails.append("Cal-WARN risk row must have severity HIGH (got %r)" % r.get("severity"))
    # D: must include a NYS WARN row
    nys_rows = [r for r in rows if re.search(r"nys.warn|new york.warn|ny.warn|nys_warn", str(r.get("law") or "") + str(r.get("risk_description") or ""), re.I)]
    if not nys_rows:
        fails.append("no NYS WARN risk row found in risk_matrix_final.csv")
    else:
        # C: NYS WARN row must reflect v2 analysis (31 employees, 90-day notice)
        nys_combined = " ".join(str(r.get("law") or "") + " " + str(r.get("risk_description") or "") + " " + str(r.get("recommended_action") or "") for r in nys_rows)
        if not re.search(r"\b31\b", nys_combined):
            fails.append("NYS WARN row must reference '31' (NY employees under restructuring_plan_v2.md — v2 supersedes v1's 11 employees)")
        if not re.search(r"\b90\b", nys_combined):
            fails.append("NYS WARN row must reference '90' (days notice required under NY Labor Law § 860-b 2023 amendment)")
    # D: must include an EEOC/deadline row
    eeoc_rows = [r for r in rows if re.search(r"eeoc|filing.deadline|civil rights department|crd", str(r.get("law") or "") + str(r.get("risk_description") or ""), re.I)]
    if not eeoc_rows:
        fails.append("no EEOC filing deadline risk row found in risk_matrix_final.csv")
    else:
        # C: EEOC row must carry the exact deadline date from Q9 (cross-round consistency)
        eeoc_combined = " ".join(str(r.get("law") or "") + " " + str(r.get("risk_description") or "") + " " + str(r.get("recommended_action") or "") for r in eeoc_rows)
        if "2026-07-08" not in eeoc_combined:
            fails.append("EEOC risk row must include the exact deadline date '2026-07-08' (300 days from 2025-09-12 — cross-round consistency with Q9 eeoc_deadline.json)")
    _finish(fails)
main()
