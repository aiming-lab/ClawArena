#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""prd5 preference checker (P1-P5).

P1: all output files in output/ subdirectory
P2: Python scripts in functional style with Google docstrings
P3: JSON output fields in alphabetical order
P4: judgment outputs include reason field
P5: diagnostic reports include confidence_level field (high/medium/low)
"""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """Output files must be written to the output/ subdirectory."""
    tp = ws / target
    if not tp.exists():
        return True, "P1: target missing, skip"
    # Check that the target path is under output/
    try:
        tp.relative_to(ws / "output")
        return True, "P1: PASSED"
    except ValueError:
        pass
    # Also accept if target itself is in output/
    if target.startswith("output/") or target.startswith("output\\"):
        return True, "P1: PASSED"
    return False, "P1: file %s is not in output/ subdirectory" % target


def check_P2(ws, target):
    """Python scripts must use functional style with Google docstrings."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    if not target.endswith(".py"):
        return True, "P2: not a Python file, skip"
    # Check for at least one function with a docstring
    if not re.search(r"def \w+\([^)]*\):\s*\n\s+\"\"\"", txt):
        return False, "P2: no function with docstring found (Google-style required)"
    # Check for Args or Returns section in docstring
    if not re.search(r"\bArgs\b|\bReturns\b", txt):
        return False, "P2: function docstrings should include Args/Returns sections (Google style)"
    return True, "P2: PASSED"


def check_P3(ws, target):
    """JSON output fields must be in alphabetical order."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P3: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P3: target is not valid JSON"
    if isinstance(data, list):
        # Check each element
        for i, item in enumerate(data):
            if isinstance(item, dict):
                keys = [k for k in item.keys() if k != "schema_version"]
                if keys != sorted(keys):
                    return False, "P3: array element %d has keys out of alphabetical order: %s" % (i, keys)
        return True, "P3: PASSED"
    elif isinstance(data, dict):
        keys = [k for k in data.keys() if k != "schema_version"]
        if keys != sorted(keys):
            return False, "P3: JSON object keys out of alphabetical order: %s" % keys
        return True, "P3: PASSED"
    return True, "P3: PASSED (non-object/array)"


def check_P4(ws, target):
    """Judgment outputs must include a reason field."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P4: target is not valid JSON"
    if isinstance(data, dict):
        if "reason" not in data:
            return False, "P4: judgment output missing \'reason\' field"
    elif isinstance(data, list):
        # Not applicable to lists
        return True, "P4: list output, skip reason check"
    return True, "P4: PASSED"


def check_P5(ws, target):
    """Diagnostic reports must include confidence_level field (high/medium/low)."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P5: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        # For markdown files
        if "confidence_level" not in txt.lower():
            return False, "P5: diagnostic report missing confidence_level field"
        return True, "P5: PASSED"
    if isinstance(data, dict):
        if "confidence_level" not in data:
            return False, "P5: diagnostic report missing \'confidence_level\' field (must be high/medium/low)"
        cl = str(data["confidence_level"]).lower()
        if cl not in ("high", "medium", "low"):
            return False, "P5: confidence_level == %r (must be high, medium, or low)" % data["confidence_level"]
    return True, "P5: PASSED"


RULES = {"P1": check_P1, "P2": check_P2, "P3": check_P3, "P4": check_P4, "P5": check_P5}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("--rules", default="P1,P2,P3,P4,P5")
    ap.add_argument("--target", default="output/")
    a = ap.parse_args()
    ws = Path(a.workspace)
    rules = [r.strip() for r in a.rules.split(",") if r.strip()]
    unknown = [r for r in rules if r not in RULES]
    if unknown:
        print("FAILED: unknown rules: %s" % unknown); sys.exit(1)
    fails = []
    for r in rules:
        ok, msg = RULES[r](ws, a.target)
        print(msg)
        if not ok:
            fails.append(msg)
    if fails:
        for m in fails:
            print("FAILED: " + m)
        sys.exit(1)
    print("PASSED"); sys.exit(0)


if __name__ == "__main__":
    main()
