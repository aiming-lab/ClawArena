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
    data, err = _load_json(ws / "analysis" / "version_impact.json")
    if err: _finish([err])
    ab = str(data.get("affected_below") or "")
    if ab != "2.32.4":
        fails.append("affected_below == %r (expected '2.32.4', not '2.32.3' from Slack/bot confusion)" % ab)
    fv = str(data.get("fixed_version") or "")
    if fv != "2.32.4":
        fails.append("fixed_version == %r (expected '2.32.4')" % fv)
    # source must identify NVD as the authoritative source (not just Slack/bot)
    src = str(data.get("source") or "")
    if "NVD" not in src:
        fails.append(
            "source == %r: must explicitly reference 'NVD' as the authoritative source "
            "(Slack and email are conflicting; only NVD / PR#6965 are authoritative)" % src[:120])
    # snake_case guard
    for k in data.keys():
        if re.search(r"[a-z][A-Z]", k):
            fails.append("camelCase field name %r violates P1" % k)
    _finish(fails)
main()
