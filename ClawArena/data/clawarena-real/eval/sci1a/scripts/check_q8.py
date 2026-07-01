#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, csv
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

def _read_tsv(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        rows = []
        with p.open(encoding="utf-8") as fh:
            reader = csv.DictReader(fh, delimiter="\t")
            for row in reader:
                rows.append(row)
        return rows, None
    except Exception as e:
        return None, "error reading TSV " + p.name + ": " + str(e)

def _read_csv(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        rows = []
        with p.open(encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                rows.append(row)
        return rows, None
    except Exception as e:
        return None, "error reading CSV " + p.name + ": " + str(e)

def _finish(fails):
    if fails:
        for f in fails:
            print("FAILED: " + f)
        sys.exit(1)
    print("PASSED")
    sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "wip" / "nih_grants_summary.json")
    if err: _finish([err])
    # layer 1: structure
    for key in ("total_grants", "total_funding_usd", "pis_with_grants", "restitution_plausibility"):
        if key not in data:
            fails.append("missing key: " + key)
    if fails: _finish(fails)
    # layer 2: types
    try:
        tg = int(data["total_grants"])
        tf = int(data["total_funding_usd"])
    except (TypeError, ValueError) as e:
        _finish(["numeric field type error: " + str(e)])
    if not isinstance(data["pis_with_grants"], list):
        fails.append("pis_with_grants must be a list")
    if fails: _finish(fails)
    # layer 3: truth
    if tg <= 0:
        fails.append("total_grants == %d (must be > 0)" % tg)
    if tf <= 0:
        fails.append("total_funding_usd == %d (must be > 0)" % tf)
    if len(data["pis_with_grants"]) == 0:
        fails.append("pis_with_grants must be non-empty")
    rp = str(data.get("restitution_plausibility", "")).lower()
    if rp not in ("plausible", "implausible"):
        fails.append("restitution_plausibility must be 'plausible' or 'implausible' (got %r)" % rp)
    _finish(fails)
main()
