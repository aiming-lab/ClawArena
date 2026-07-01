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
    data, err = _load_json(ws / "output" / "q9_legacy_assessment.json")
    if err: _finish([err])

    # E-rule: schema_version silently checked
    if data.get("schema_version") != "1.0":
        fails.append(f"schema_version={data.get('schema_version')!r} must be '1.0'")

    for k in ("document_name", "document_status", "reason", "correct_threshold_bps",
               "authoritative_source_file"):
        if k not in data:
            fails.append(f"missing key: {k}")
    if fails: _finish(fails)

    dname = str(data.get("document_name", ""))
    if dname != "LEGACY_visa_vdmp_old_thresholds.md":
        fails.append(f"document_name={dname!r} (expected 'LEGACY_visa_vdmp_old_thresholds.md')")

    status = str(data.get("document_status", ""))
    if status != "LEGACY_DO_NOT_USE":
        fails.append(f"document_status={status!r} (must be exactly 'LEGACY_DO_NOT_USE')")

    thr = data.get("correct_threshold_bps")
    try:
        thr_int = int(thr)
    except (TypeError, ValueError):
        thr_int = -1
    if thr_int != 150:
        fails.append(f"correct_threshold_bps={thr} (expected 150 — the 2026-04-01 authoritative threshold)")

    # F-rule: reason must explicitly contain "2026-04-01" (not just "2026") and "220"
    reason = str(data.get("reason", "")).strip()
    if not reason:
        fails.append("reason is empty — must explain why the LEGACY document is deprecated")
    else:
        if "220" not in reason:
            fails.append(f"reason must mention the superseded 220 bps threshold; got: {reason[:120]!r}")
        if "2026-04-01" not in reason:
            fails.append(f"reason must state the exact effective date '2026-04-01' of the new threshold; got: {reason[:120]!r}")

    VALID_SOURCES = {
        "visa_vamp_thresholds_2026.json",
        "visa_vamp_fact_sheet_summary.md",
    }
    src = str(data.get("authoritative_source_file", "")).strip()
    if not src:
        fails.append("authoritative_source_file is empty")
    elif src not in VALID_SOURCES:
        fails.append(f"authoritative_source_file={src!r} must be one of {sorted(VALID_SOURCES)}")

    _finish(fails)
main()
