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
    data, err = _load_json(ws / "output" / "sla_comparison.json")
    if err: _finish([err])
    # extract comparison_items array
    if isinstance(data, dict):
        items = data.get("comparison_items") or data.get("items") or []
    elif isinstance(data, list):
        items = data
    else:
        _finish(["sla_comparison.json must be object with comparison_items or array"])
    # check 4 required entries with exact source_url values
    required = [
        ("99.90", "https://www.atlassian.com/legal/sla", "Atlassian Premium 99.90%"),
        ("99.95", "https://www.atlassian.com/legal/sla", "Atlassian Enterprise 99.95%"),
        ("99.99", "https://aws.amazon.com/ec2/sla/", "AWS EC2 Region 99.99%"),
        ("99.95", "https://aws.amazon.com/lambda/sla/", "AWS Lambda 99.95%"),
    ]
    for val, exact_url, label in required:
        found = False
        for item in items:
            if not isinstance(item, dict): continue
            v = str(item.get("value") or "")
            src = str(item.get("source_url") or "")
            if val in v and src == exact_url:
                found = True
                break
        if not found:
            fails.append("Missing %s entry: value containing %r with source_url exactly %r" % (label, val, exact_url))
    # each item must have vendor, metric_name, value, source_url fields
    for i, item in enumerate(items):
        if not isinstance(item, dict): continue
        for req_field in ("vendor", "metric_name", "value", "source_url"):
            if req_field not in item:
                fails.append("comparison_items[%d] missing required field: %r" % (i, req_field))
                break
    # reviewer_signature in outer object (P5)
    if isinstance(data, dict) and "reviewer_signature" not in data:
        fails.append("reviewer_signature field missing in top-level object (P5)")
    # schema_version must be present in metadata (P2)
    if isinstance(data, dict):
        meta = data.get("metadata")
        if not isinstance(meta, dict):
            fails.append("metadata block missing (P2 requires metadata with generated_at, agent_id, schema_version)")
        else:
            for req in ("generated_at", "agent_id", "schema_version"):
                if req not in meta:
                    fails.append("metadata.%s missing (P2)" % req)
    _finish(fails)
main()
