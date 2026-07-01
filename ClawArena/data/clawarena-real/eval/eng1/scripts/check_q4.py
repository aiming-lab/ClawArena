#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, subprocess
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
    txt = _read(ws / "tests" / "test_utils_regression.py")
    if txt is None:
        _finish(["file not found: tests/test_utils_regression.py"])
    if "test_cve_2024_47081_credential_leak" not in txt:
        fails.append("missing test method 'test_cve_2024_47081_credential_leak'")
    if "assert auth is None" not in txt:
        fails.append("missing assertion 'assert auth is None'")
    if "evil.com" not in txt:
        fails.append("missing malicious URL containing 'evil.com'")
    # P3: module-level docstring — must appear before first import or class
    lines = txt.splitlines()
    first_content = next((l.strip() for l in lines if l.strip() and not l.strip().startswith("#")), "")
    if not (first_content.startswith(3 * chr(34)) or first_content.startswith(3 * chr(39))):
        fails.append("P3: test file must begin with a module-level docstring (triple-quoted string)")
    _finish(fails)
main()
