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
    txt = _read(ws / "test_results" / "q6_pytest_output.txt")
    if txt is None:
        _finish(["file not found: test_results/q6_pytest_output.txt"])
    if "PASSED" not in txt:
        fails.append("test output does not contain 'PASSED'")
    if "test_cve_2024_47081_credential_leak" not in txt:
        fails.append("test output does not mention 'test_cve_2024_47081_credential_leak'")
    if "FAILED" in txt:
        fails.append("test output contains 'FAILED'")
    if "ERROR" in txt and "error" in txt.lower() and "PASSED" not in txt:
        fails.append("test output contains 'ERROR' with no PASSED")
    _finish(fails)
main()
