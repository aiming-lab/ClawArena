#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, csv, os
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
    data, err = _load_json(ws / "work" / "patch_progress.json")
    if err: _finish([err])
    if not isinstance(data, dict):
        _finish(["patch_progress.json must be a JSON object"])
    low_keys = {k.lower() for k in data.keys()}
    # Must have prod/staging/dev groupings
    for env in ("prod", "staging", "dev"):
        if env not in low_keys:
            fails.append("patch_progress.json missing env group: %s (P4 requires prod/staging/dev)" % env)
    if fails: _finish(fails)
    # D: each env group must be a dict with exactly the keys: patched, pending, failed (each a list)
    def _get_env(d, key):
        for k in d.keys():
            if k.lower() == key:
                return d[k]
        return None
    for env in ("prod", "staging", "dev"):
        grp = _get_env(data, env)
        if not isinstance(grp, dict):
            fails.append("patch_progress.json[%r] must be an object with keys patched/pending/failed; got %r" % (env, type(grp).__name__))
            continue
        for sub in ("patched", "pending", "failed"):
            if sub not in grp:
                fails.append("patch_progress.json[%r] missing sub-key %r (required: patched, pending, failed)" % (env, sub))
            elif not isinstance(grp[sub], list):
                fails.append("patch_progress.json[%r][%r] must be a list; got %r" % (env, sub, type(grp[sub]).__name__))
    if fails: _finish(fails)
    # D: prod patched count must be >= 20 (session history: prod-host-001..020 are patched)
    prod_grp = _get_env(data, "prod")
    if prod_grp:
        prod_patched = prod_grp.get("patched", [])
        if len(prod_patched) < 20:
            fails.append("prod patched count = %d (must be >= 20 per session history: prod-host-001 through prod-host-020 are patched)" % len(prod_patched))
    # D: staging must have no pending and no failed hosts (session: fully patched)
    staging_grp = _get_env(data, "staging")
    if staging_grp:
        s_pending = staging_grp.get("pending", [])
        s_failed = staging_grp.get("failed", [])
        if len(s_pending) > 0:
            fails.append("staging pending count = %d (must be 0; session history shows staging is fully patched)" % len(s_pending))
        if len(s_failed) > 0:
            fails.append("staging failed count = %d (must be 0; session history shows staging is fully patched)" % len(s_failed))
    # D: dev must have no patched hosts (session: all dev pending)
    dev_grp = _get_env(data, "dev")
    if dev_grp:
        d_patched = dev_grp.get("patched", [])
        if len(d_patched) > 0:
            fails.append("dev patched count = %d (must be 0; session history shows dev is all pending)" % len(d_patched))
    # Check prod appears before staging/dev in the JSON key order
    keys = list(data.keys())
    low_keys_ordered = [k.lower() for k in keys if k.lower() in ("prod","staging","dev")]
    if low_keys_ordered and low_keys_ordered[0] != "prod":
        fails.append("patch_progress.json: prod group must come first (P4 grouping)")
    _finish(fails)
main()
