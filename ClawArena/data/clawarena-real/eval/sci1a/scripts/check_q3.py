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
    data, err = _load_json(ws / "reports" / "wip" / "glimcher_retraction_record.json")
    if err: _finish([err])
    # layer 1: structure
    for key in ("original_doi", "retraction_doi", "publication_year", "figures_with_issues"):
        if key not in data:
            fails.append("missing key: " + key)
    if fails: _finish(fails)
    # layer 2: types
    if not isinstance(data["publication_year"], int):
        try:
            data["publication_year"] = int(data["publication_year"])
        except (TypeError, ValueError):
            fails.append("publication_year must be an integer")
    if not isinstance(data["figures_with_issues"], list):
        fails.append("figures_with_issues must be a list")
    if fails: _finish(fails)
    # layer 3: verbatim truth (V9)
    if str(data.get("original_doi")) != "10.1126/science.1123480":
        fails.append("original_doi == %r (expected '10.1126/science.1123480')" % data.get("original_doi"))
    if str(data.get("retraction_doi")) != "10.1126/science.adp1104":
        fails.append("retraction_doi == %r (expected '10.1126/science.adp1104')" % data.get("retraction_doi"))
    if int(data.get("publication_year", 0)) != 2006:
        fails.append("publication_year == %r (expected 2006)" % data.get("publication_year"))
    figs_str = [str(f).strip() for f in data["figures_with_issues"]]
    # verbatim figure labels: both "Fig. 1A" and "Fig. 6A" must appear exactly
    if not any(f == "Fig. 1A" or f == "Fig. 1A." for f in figs_str):
        fails.append(
            "figures_with_issues must include 'Fig. 1A' (verbatim from retraction notice — "
            "not 'Fig. 3B' or 'Fig. 6A only'; both panels were flagged)"
        )
    if not any(f == "Fig. 6A" or f == "Fig. 6A." for f in figs_str):
        fails.append(
            "figures_with_issues must include 'Fig. 6A' (verbatim from retraction notice — "
            "controls discrepancy confirmed for this panel)"
        )
    _finish(fails)
main()
