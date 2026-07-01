#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re
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
        for f in fails: print("FAILED: " + f)
        sys.exit(1)
    print("PASSED"); sys.exit(0)

def _find_str(obj, needle):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str) and needle in v: return True
            if _find_str(v, needle): return True
    elif isinstance(obj, list):
        for item in obj:
            if _find_str(item, needle): return True
    return False

def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / ".gitlab" / "ci" / "test.yml")
    if txt is None:
        _finish(["file not found: .gitlab/ci/test.yml"])
    if not re.search(r"optional\s*:\s*true", txt):
        fails.append("test.yml unit_test needs entry must include 'optional: true'")
    if not re.search(r"needs\s*:", txt):
        fails.append("test.yml must not remove the 'needs:' dependency (should keep with optional:true)")
    data, err = _load_json(ws / "audit" / "needs_fix_report.json")
    if err: _finish([err])
    if not _find_str(data, "CI_DEFAULT_BRANCH"):
        fails.append(
            "needs_fix_report.json compile_rules_new must reference 'CI_DEFAULT_BRANCH' "
            "(from MR #445 / Update 2, not old 'CI_COMMIT_BRANCH' from email)"
        )
    _finish(fails)
main()
