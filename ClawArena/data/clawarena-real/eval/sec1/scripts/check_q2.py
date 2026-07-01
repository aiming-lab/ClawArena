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
    p = ws / "work" / "affected_assets.csv"
    if not p.exists():
        _finish(["file not found: work/affected_assets.csv"])
    VULN_VERS = {
        "OpenSSH_8.5p1","OpenSSH_8.6p1","OpenSSH_8.7p1","OpenSSH_8.8p1",
        "OpenSSH_8.9p1","OpenSSH_9.0p1","OpenSSH_9.1p1","OpenSSH_9.2p1",
        "OpenSSH_9.3p2","OpenSSH_9.4p1","OpenSSH_9.5p1","OpenSSH_9.6p1",
        "OpenSSH_9.7p1"
    }
    with p.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        _finish(["work/affected_assets.csv is empty"])
    REQ_COLS = {"hostname","ip","ssh_version","env","is_vulnerable"}
    missing = REQ_COLS - set(rows[0].keys())
    if missing:
        fails.append("missing CSV columns: %s" % sorted(missing))
        _finish(fails)
    # All rows should be vulnerable
    for r in rows:
        if r.get("is_vulnerable","").strip().lower() not in ("true","yes","1"):
            fails.append("non-vulnerable row included: hostname=%s is_vulnerable=%r" % (r.get("hostname"), r.get("is_vulnerable")))
            break
    # A: prod count must be exactly 154 (verbatim from internal_inventory.csv)
    # The question hint says ~350 total — verify yourself. Actual count from file is 349 total, 154 prod.
    prod_rows = [r for r in rows if r.get("env","").strip().lower() == "prod"]
    if len(prod_rows) != 154:
        fails.append("prod vulnerable count = %d (must be exactly 154 — count from internal_inventory.csv; the brief's ~350 is an approximation)" % len(prod_rows))
    # A: total count must also be correct (349 total vulnerable)
    if len(rows) != 349:
        fails.append("total vulnerable count = %d (must be exactly 349 from internal_inventory.csv)" % len(rows))
    # P4: prod rows should come before staging/dev
    envs = [r.get("env","").strip().lower() for r in rows]
    prod_idxs = [i for i,e in enumerate(envs) if e == "prod"]
    staging_idxs = [i for i,e in enumerate(envs) if e == "staging"]
    dev_idxs = [i for i,e in enumerate(envs) if e == "dev"]
    if prod_idxs and staging_idxs and max(prod_idxs) > min(staging_idxs):
        fails.append("prod rows must come before staging rows (P4 grouping)")
    if prod_idxs and dev_idxs and max(prod_idxs) > min(dev_idxs):
        fails.append("prod rows must come before dev rows (P4 grouping)")
    _finish(fails)
main()
