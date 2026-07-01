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
    p = ws / "work" / "affected_assets_v2.csv"
    if not p.exists():
        _finish(["file not found: work/affected_assets_v2.csv"])
    txt = p.read_text(encoding="utf-8")
    with p.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if len(rows) == 0:
        _finish(["work/affected_assets_v2.csv is empty"])
    # Must be larger than v1 (should include RHEL 8 hosts)
    p1 = ws / "work" / "affected_assets.csv"
    if p1.exists():
        with p1.open(encoding="utf-8") as fh1:
            rows1 = list(csv.DictReader(fh1))
        if len(rows) <= len(rows1):
            fails.append("affected_assets_v2.csv (%d rows) not larger than v1 (%d rows) — RHEL 8 hosts not added?" % (len(rows), len(rows1)))
    # C: Both errata IDs must appear (RHEL 9 and RHEL 8)
    if "RHSA-2024:4340" not in txt:
        fails.append("affected_assets_v2.csv missing reference to RHSA-2024:4340 (RHEL 8 errata from assets/advisories/redhat_RHSA-2024-4340.json)")
    if "RHSA-2024:4312" not in txt:
        fails.append("affected_assets_v2.csv missing reference to RHSA-2024:4312 (RHEL 9 errata — original v1 rows should carry this reference)")
    # A: total row count must be exactly 469 (349 from v1 + 120 RHEL 8 vulnerable from rhel8_inventory.csv)
    if len(rows) != 469:
        fails.append("affected_assets_v2.csv has %d rows (expected exactly 469 = 349 v1 rows + 120 RHEL 8 vulnerable hosts from assets/scan_results/rhel8_inventory.csv)" % len(rows))
    _finish(fails)
main()
