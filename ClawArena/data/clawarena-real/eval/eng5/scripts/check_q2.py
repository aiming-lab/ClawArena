#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# check_q2.py — cache version report: all v2 files reported; deprecated_deadline exact; required_version
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

def _finish(fails):
    if fails:
        for f in fails: print("FAILED: " + f)
        sys.exit(1)
    print("PASSED"); sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "audit" / "cache_version_report.json")
    if err: _finish([err])
    findings = data.get("findings")
    if not isinstance(findings, list) or len(findings) == 0:
        _finish(["'findings' must be a non-empty list"])
    # A: Every v2 finding must have is_deprecated=true, correct required_version,
    #    and deprecated_deadline exactly "2025-03-01"
    v2_files = set()
    for f in findings:
        if not isinstance(f, dict): continue
        ver = str(f.get("current_version", ""))
        if "v2" in ver or ver == "2":
            v2_files.add(str(f.get("file", "")))
            if f.get("is_deprecated") is not True:
                fails.append("finding for %r (v2) must have is_deprecated=true (got %r)" % (f.get("file"), f.get("is_deprecated")))
            req = str(f.get("required_version", ""))
            if "v4.2.0" not in req and "v3.4.0" not in req:
                fails.append("required_version must be 'v4.2.0' or 'v3.4.0' (got %r for file %r)" % (req, f.get("file")))
            # A: deprecated_deadline must be exactly "2025-03-01"
            ddl = str(f.get("deprecated_deadline", ""))
            if ddl != "2025-03-01":
                fails.append(
                    "finding for %r must have deprecated_deadline exactly '2025-03-01' (got %r); "
                    "read the official notice — do not guess the date" % (f.get("file"), ddl)
                )
    if not v2_files:
        fails.append("no v2 findings found — must detect deprecated actions/cache@v2 usages")
    # A: Both ci.yml and nightly.yml have v2 usages; both must appear in findings
    expected_files = [".github/workflows/ci.yml", ".github/workflows/nightly.yml"]
    for exp in expected_files:
        if not any(exp in fpath for fpath in v2_files):
            fails.append(
                "findings missing v2 entry for %r — that file also uses actions/cache@v2 "
                "(do not rely on a bot summary; read all workflow files)" % exp
            )
    all_req = [str(f.get("required_version", "")) for f in findings if isinstance(f, dict)]
    if not any("v4.2.0" in r or "v3.4.0" in r for r in all_req):
        fails.append("required_version must reference 'v4.2.0' or 'v3.4.0'")
    _finish(fails)
main()
