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
    data, err = _load_json(ws / "reports" / "compliance_issues_q1.json")
    if err: _finish([err])
    # P1: schema_version at top level
    if not isinstance(data, dict) or str(data.get("schema_version")) != "1.0":
        fails.append("top-level schema_version must be '1.0'")
    # Issues array
    issues = data.get("issues") if isinstance(data, dict) else None
    if issues is None and isinstance(data, list):
        issues = data
    if not isinstance(issues, list) or len(issues) == 0:
        _finish(["issues array is missing or empty"])
    # Must have at least 4 entries (6 prohibited qualifiers + at least some other violations)
    if len(issues) < 4:
        fails.append("expected at least 4 compliance issues, got %d" % len(issues))
    # Each entry must have required fields
    for i, entry in enumerate(issues):
        if not isinstance(entry, dict):
            fails.append("issue[%d] is not a dict" % i); continue
        for req in ("issue_id", "claim_text", "violated_rule", "ftc_citation", "severity"):
            if not entry.get(req):
                fails.append("issue[%d] missing or empty field '%s'" % (i, req))
    # Check that prohibited qualifiers are flagged — look for at least 'promis' or 'preliminar' or 'may' or 'initial'
    all_text = json.dumps(issues).lower()
    found_qualifiers = sum(1 for q in ("may", "promis", "preliminar", "initial", "pilot", "helps")
                          if q in all_text)
    if found_qualifiers < 3:
        fails.append("expected at least 3 of the prohibited qualifiers (may/promising/preliminary/initial/pilot/helps) to be flagged, found markers for %d" % found_qualifiers)
    _finish(fails)
main()
