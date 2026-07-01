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
    data, err = _load_json(ws / "output" / "escalation_report_2024_11.json")
    if err: _finish([err])
    # sla_policy_version must be v1 (November 2024 predates both updates)
    ver = str(data.get("sla_policy_version") or "").lower()
    if "v1" not in ver:
        fails.append("sla_policy_version == %r (must be 'v1' — November 2024 predates v2 and v3)" % data.get("sla_policy_version"))
    # credit_recommendations: source_url must reference atlassian.com/legal/sla
    recs = data.get("credit_recommendations") or []
    if not recs:
        fails.append("credit_recommendations is empty or missing")
    for rec in recs:
        if not isinstance(rec, dict): continue
        src = str(rec.get("source_url") or "")
        if "atlassian.com/legal/sla" not in src:
            fails.append("credit_recommendations[].source_url == %r (expected https://www.atlassian.com/legal/sla)" % src)
            break
    # metadata block required (P2)
    meta = data.get("metadata")
    if not isinstance(meta, dict):
        fails.append("metadata block missing or not an object (P2)")
    else:
        for req in ("generated_at", "agent_id", "schema_version"):
            if req not in meta:
                fails.append("metadata.%s missing" % req)
    # reviewer_signature must exist (P5)
    if "reviewer_signature" not in data:
        fails.append("reviewer_signature field missing (P5)")
    # report_period
    period = str(data.get("report_period") or "")
    if "2024-11" not in period:
        fails.append("report_period == %r (expected '2024-11')" % period)
    _finish(fails)
main()
