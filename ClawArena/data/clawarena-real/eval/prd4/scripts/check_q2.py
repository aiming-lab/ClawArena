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
    data, err = _load_json(ws / "output" / "archive_audit.json")
    if err: _finish([err])
    # is_superseded must be true
    if data.get("is_superseded") is not True:
        fails.append("is_superseded == %r (expected true)" % data.get("is_superseded"))
    # incorrect_fields must include L1 response_minutes error
    fields = data.get("incorrect_fields") or []
    l1_found = False
    for f in fields:
        if not isinstance(f, dict):
            continue
        path = str(f.get("field_path") or "")
        archived = f.get("archived_value")
        correct = f.get("correct_value")
        if "L1" in path or "l1" in path.lower():
            try:
                arch_int = int(archived)
                corr_int = int(correct)
                if arch_int == 60 and corr_int == 30:
                    l1_found = True
                elif arch_int == 60 or "60" in str(archived):
                    # also accept string "60" vs "30"
                    l1_found = True
            except (TypeError, ValueError):
                # accept string values
                if str(archived) in ("60", "1h", "1 hour") and str(correct) in ("30", "30min", "30 minutes"):
                    l1_found = True
    if not l1_found:
        fails.append("incorrect_fields must include L1 response_minutes: archived_value=60 (or 1h), correct_value=30 (or 30min)")
    # superseded_date must be present and valid ISO 8601 format
    sd = str(data.get("superseded_date") or "")
    if not sd:
        fails.append("superseded_date field missing (must be an ISO 8601 date/datetime string)")
    else:
        import re
        if not re.match(r"^\d{4}-\d{2}-\d{2}", sd):
            fails.append("superseded_date == %r (must match YYYY-MM-DD ISO 8601 format)" % sd)
    # reviewer_signature must exist (P5)
    if "reviewer_signature" not in data:
        fails.append("reviewer_signature field missing (P5 requires this field in every report)")
    # incorrect_fields must have field_path, archived_value, correct_value in each entry
    for i, f in enumerate(data.get("incorrect_fields") or []):
        if not isinstance(f, dict):
            continue
        for req_field in ("field_path", "archived_value", "correct_value"):
            if req_field not in f:
                fails.append("incorrect_fields[%d] missing required field: %r" % (i, req_field))
                break
    _finish(fails)
main()
