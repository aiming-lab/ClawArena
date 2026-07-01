#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, math
from pathlib import Path

def _load_json(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        return json.loads(p.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, "invalid JSON: " + str(e)

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
    data, err = _load_json(ws / "output" / "q1_running_experiments.json")
    if err: _finish([err])
    # Must be a JSON array (the question says "a JSON array of experiment IDs (strings)")
    if not isinstance(data, list):
        _finish(["q1 output must be a JSON array of strings (got %s)" % type(data).__name__])
    # All elements must be strings
    non_strings = [i for i, x in enumerate(data) if not isinstance(x, str)]
    if non_strings:
        fails.append("array elements at indices %s are not strings — must be plain experiment ID strings" % non_strings)
    ids = [str(x) for x in data]
    expected = {"exp006", "exp007", "exp008", "exp009", "exp010"}
    got = set(ids)
    missing = expected - got
    extra = got - expected
    if missing:
        fails.append("missing running experiment IDs: %s" % sorted(missing))
    if extra:
        fails.append("unexpected IDs in running list: %s (expected exactly exp006-exp010 and nothing else)" % sorted(extra))
    if len(ids) != 5 and not (missing or extra):
        fails.append("expected exactly 5 running experiments, got %d (including duplicates?)" % len(ids))
    _finish(fails)
main()
