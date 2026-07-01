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

def _find_val(obj, needle):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str) and needle in v: return True
            if _find_val(v, needle): return True
    elif isinstance(obj, list):
        for item in obj:
            if _find_val(item, needle): return True
    return False

def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / ".github" / "workflows" / "deploy.yml")
    if txt is None:
        _finish(["file not found: .github/workflows/deploy.yml"])
    if not re.search(r"deployments\s*:\s*write", txt):
        fails.append("deploy.yml does not have 'deployments: write' (required after April 1, 2025)")
    if not re.search(r"id-token\s*:\s*write", txt):
        fails.append("deploy.yml lost 'id-token: write' permission (must be preserved from Q7)")
    data, err = _load_json(ws / "audit" / "permissions_changelog.json")
    if err: _finish([err])
    if not _find_val(data, "2025-04-01"):
        fails.append("permissions_changelog.json does not contain deadline '2025-04-01'")
    _finish(fails)
main()
