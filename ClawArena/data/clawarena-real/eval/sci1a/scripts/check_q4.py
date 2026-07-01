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
    data, err = _load_json(ws / "reports" / "wip" / "ghobrial_image_analysis.json")
    if err: _finish([err])
    # layer 1: structure
    for key in ("paper_doi", "total_pairs", "duplicate_count", "max_similarity_score"):
        if key not in data:
            fails.append("missing key: " + key)
    if fails: _finish(fails)
    # layer 2: types
    try:
        total_pairs = int(data["total_pairs"])
        dup_count = int(data["duplicate_count"])
        max_sim = float(data["max_similarity_score"])
    except (TypeError, ValueError) as e:
        _finish(["numeric field type error: " + str(e)])
    # layer 3: truth (V4 cross-round: DOI must match Q5 context)
    if str(data.get("paper_doi")) != "10.1182/blood-2008-10-186668":
        fails.append("paper_doi == %r (expected '10.1182/blood-2008-10-186668')" % data.get("paper_doi"))
    if total_pairs != 8:
        fails.append("total_pairs == %d (expected exactly 8; read all rows in the Ghobrial TSV)" % total_pairs)
    if dup_count != 6:
        fails.append(
            "duplicate_count == %d (expected exactly 6; count rows where verdict == 'DUPLICATE' "
            "in the Ghobrial TSV — not an estimate)" % dup_count
        )
    if max_sim <= 0.95:
        fails.append("max_similarity_score == %.4f (expected > 0.95 for Ghobrial near-fabricated figures)" % max_sim)
    _finish(fails)
main()
