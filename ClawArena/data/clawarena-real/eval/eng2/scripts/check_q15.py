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

def _field_entry(data, name):
    """从 quality report 取某字段 entry，兼容 fields 为 list 或 dict。"""
    fields = data.get("fields")
    if isinstance(fields, list):
        for e in fields:
            if isinstance(e, dict) and e.get("field_name") == name:
                return e
    elif isinstance(fields, dict):
        e = fields.get(name)
        if isinstance(e, dict):
            return e
        if e is not None:
            return {"field_name": name, "null_count": e}
    return None

def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "output" / "q15_migration_checklist.md")
    if txt is None:
        _finish(["file not found: output/q15_migration_checklist.md"])
    low = txt.lower()
    # require >= 10 checked items
    x_count = len(re.findall(r"\[x\]", low))
    if x_count < 10:
        fails.append("only %d '[x]' checklist items (expected >= 10; include all major pipeline steps)" % x_count)
    if len(re.findall(r"^## ", txt, re.MULTILINE)) < 2:
        fails.append("fewer than 2 '## ' section headings")
    if not (re.search(r"vendorid", low) and "6" in txt and re.search(r"exclu|remov|drop", low)):
        fails.append("no explicit VendorID=6 exclusion item")
    if "supersede" not in low and "supersed" not in low:
        fails.append("checklist does not record that the exclusion SUPERSEDES the earlier audit_only Slack guidance")
    # must explicitly cite the Slack thread reference being superseded
    if "slack-a20-vendor6-keep" not in low and "slack_a20" not in low:
        fails.append("checklist must explicitly cite the superseded Slack reference 'SLACK-A20-VENDOR6-KEEP' (from vendor_registry.json)")
    # must explicitly record audit_only label being superseded
    if "audit_only" not in low and "audit only" not in low:
        fails.append("checklist must explicitly mention the superseded 'audit_only' Slack rule")
    _finish(fails)
main()
