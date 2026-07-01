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
    data, err = _load_json(ws / "output" / "q7_model_comparison.json")
    if err: _finish([err])

    # E-rule: schema_version silently checked (no reminder in question)
    if data.get("schema_version") != "1.0":
        fails.append(f"schema_version={data.get('schema_version')!r} must be '1.0'")

    for k in ("v1_auc", "v2_auc", "v1_threshold", "v2_summary_threshold",
               "v2_authoritative_threshold", "identified_discrepancy",
               "authoritative_source", "source_url"):
        if k not in data:
            fails.append(f"missing key: {k}")
    if fails: _finish(fails)

    # v1_threshold must be exactly 0.5 (from models/fraud_model_v1_config.json)
    v1_t = float(data.get("v1_threshold", 0))
    if abs(v1_t - 0.5) > 0.01:
        fails.append(f"v1_threshold={v1_t} (expected 0.5 from fraud_model_v1_config.json)")

    # Auto-summary says 0.3, authoritative says 0.5
    v2_sum = float(data.get("v2_summary_threshold", 0))
    if abs(v2_sum - 0.3) > 0.01:
        fails.append(f"v2_summary_threshold={v2_sum} (expected 0.3 — the distorted bot summary value)")

    v2_auth = float(data.get("v2_authoritative_threshold", 0))
    if abs(v2_auth - 0.5) > 0.01:
        fails.append(f"v2_authoritative_threshold={v2_auth} (expected 0.5 from Detailed Findings)")

    disc = str(data.get("identified_discrepancy", "")).strip()
    if not disc:
        fails.append("identified_discrepancy is empty — must explain the 0.3 vs 0.5 contradiction")
    elif len(disc) < 20:
        fails.append(f"identified_discrepancy too brief ({len(disc)} chars) — must substantively explain contradiction")

    if not str(data.get("authoritative_source", "")).strip():
        fails.append("authoritative_source is empty")

    # F-rule: source_url must be non-empty (P5 extended silently to this round)
    su = str(data.get("source_url", "")).strip()
    if not su:
        fails.append("source_url is missing — regulatory analysis must cite sources")

    _finish(fails)
main()
