#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""eng4 preference checker (P1 work/ dir / P2 snake_case / P3 rationale URL /
P4 CONCURRENTLY / P5 q{N}_ prefix)."""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """All work products must be in the work/ directory."""
    tp = Path(ws) / target
    if not tp.exists():
        return True, "P1: target missing, skip"
    # Verify the target path is under work/
    try:
        tp.relative_to(Path(ws) / "work")
        return True, "P1: PASSED (target is under work/)"
    except ValueError:
        return False, "P1: deliverable %s must be inside work/ directory" % target


def check_P2(ws, target):
    """JSON field names must use snake_case (no camelCase or PascalCase)."""
    txt = _read(Path(ws) / target)
    if txt is None:
        return True, "P2: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return True, "P2: target not JSON, skip"
    # Check all keys at all levels recursively
    def collect_keys(obj):
        if isinstance(obj, dict):
            for k in obj.keys():
                yield k
                yield from collect_keys(obj[k])
        elif isinstance(obj, list):
            for item in obj:
                yield from collect_keys(item)
    camel_pat = re.compile(r"[a-z][A-Z]")  # camelCase indicator
    pascal_pat = re.compile(r"^[A-Z]")     # PascalCase indicator
    bad_keys = []
    for key in collect_keys(data):
        if isinstance(key, str):
            if camel_pat.search(key) or pascal_pat.match(key):
                bad_keys.append(key)
    if bad_keys:
        return False, "P2: non-snake_case JSON keys found: %s" % bad_keys[:5]
    return True, "P2: PASSED"


def check_P3(ws, target):
    """rationale field in index recommendation JSON must cite a documentation URL."""
    txt = _read(Path(ws) / target)
    if txt is None:
        return True, "P3: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return True, "P3: target not JSON, skip"
    # Look for rationale field at any level
    def find_rationale(obj):
        if isinstance(obj, dict):
            if "rationale" in obj:
                yield obj["rationale"]
            for v in obj.values():
                yield from find_rationale(v)
        elif isinstance(obj, list):
            for item in obj:
                yield from find_rationale(item)
    rationales = list(find_rationale(data))
    if not rationales:
        return True, "P3: no rationale field found, skip"
    for rat in rationales:
        if "http" not in str(rat) and "postgresql.org" not in str(rat):
            return False, "P3: rationale must cite a documentation URL, got %r" % str(rat)[:80]
    return True, "P3: PASSED"


def check_P4(ws, target):
    """All CREATE INDEX statements must use CONCURRENTLY."""
    txt = _read(Path(ws) / target)
    if txt is None:
        return True, "P4: target missing, skip"
    low = txt.lower()
    # Check if file contains any CREATE INDEX
    if "create index" not in low:
        return True, "P4: no CREATE INDEX found, skip"
    # Every CREATE INDEX must have CONCURRENTLY
    lines = txt.splitlines()
    for line in lines:
        ll = line.lower().strip()
        if "create index" in ll and "concurrently" not in ll:
            # Allow lines that are just comments
            if not ll.startswith("--") and not ll.startswith("#"):
                return False, "P4: CREATE INDEX without CONCURRENTLY: %r" % line[:80]
    return True, "P4: PASSED"


def check_P5(ws, target):
    """SQL files must use q{N}_ prefix naming convention."""
    tp = Path(ws) / target
    if not tp.exists():
        return True, "P5: target missing, skip"
    fname = tp.name
    if fname.endswith(".sql"):
        pat = re.compile(r"^q\d+_")
        if not pat.match(fname):
            return False, "P5: SQL file name %r does not use q{N}_ prefix (e.g. q011_partial_index.sql)" % fname
    return True, "P5: PASSED"


RULES = {"P1": check_P1, "P2": check_P2, "P3": check_P3, "P4": check_P4, "P5": check_P5}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("--rules", default="P1,P2,P3,P4,P5")
    ap.add_argument("--target", default="work/")
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
