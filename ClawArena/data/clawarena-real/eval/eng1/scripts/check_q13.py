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
    if "test_legitimate_url_returns_credentials" not in txt:
        fails.append("missing test method 'test_legitimate_url_returns_credentials'")
    if "test_empty_default_credentials_ignored" not in txt:
        fails.append("missing test method 'test_empty_default_credentials_ignored'")
    suite_txt = _read(ws / "test_results" / "q13_full_suite.txt")
    if suite_txt is None:
        _finish(["file not found: test_results/q13_full_suite.txt"])
    if "3 passed" not in suite_txt:
        fails.append("q13_full_suite.txt does not contain '3 passed' (expected all 3 tests to pass)")
    _finish(fails)
main()
