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

def _csv_rows(p):
    """Read CSV and return (header, data_rows). Returns (None, []) if file missing."""
    p = Path(p)
    if not p.exists():
        return None, []
    with p.open(encoding="utf-8") as fh:
        rows = [r for r in fh if not r.strip().startswith("#")]
    if not rows:
        return None, []
    reader = csv.DictReader(iter(rows))
    data = list(reader)
    return reader.fieldnames, data

def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "output" / "regulatory_submission_summary.json")
    if txt is None:
        _finish(["file not found: output/regulatory_submission_summary.json"])
    try:
        data = json.loads(txt)
    except json.JSONDecodeError as e:
        _finish(["invalid JSON: " + str(e)])
    # P5: field order check (incident_date must come before rule_violated, before financial_impact, ...)
    required_order = ["incident_date", "rule_violated", "financial_impact", "remediation_count", "submission_date"]
    keys = [k for k in data.keys() if k in set(required_order)]
    order_idx = [required_order.index(k) for k in keys if k in required_order]
    if order_idx != sorted(order_idx):
        fails.append("P5 field order violated: required incident_date->rule_violated->financial_impact->remediation_count->submission_date (got %s)" % keys)
    # 真值层
    for req in required_order:
        if req not in data:
            fails.append("missing field: " + req)
    if fails: _finish(fails)
    rule = str(data.get("rule_violated", ""))
    if "15c3-5(b)" not in rule:
        fails.append("rule_violated must contain '15c3-5(b)' (got %r)" % rule)
    try:
        rc = int(data.get("remediation_count"))
    except (TypeError, ValueError):
        _finish(["remediation_count not an int"])
    if rc < 4:
        fails.append("remediation_count == %d (expected >= 4)" % rc)
    if data.get("incident_date") != "2024-11-03":
        fails.append("incident_date == %r (expected '2024-11-03')" % data.get("incident_date"))
    # V4 cross-round closure: financial_impact must reference the AROS audit log window count (39)
    fi = str(data.get("financial_impact", ""))
    if "39" not in fi:
        fails.append(
            "financial_impact must reference '39' (the AROS audit log window count from q3 — "
            "entries with timestamp_utc_reported in 14:00-15:00 UTC on 2024-11-03); "
            "do not use the position_delta_report.csv total (87) or bot_summary figure (63)"
        )
    _finish(fails)
main()
