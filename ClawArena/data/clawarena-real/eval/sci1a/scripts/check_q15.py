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
    # P1: filename check
    fpath = ws / "reports" / "final" / "2024-01-02_dfci_final_report.md"
    txt = _read(fpath)
    if txt is None:
        _finish(["file not found: reports/final/2024-01-02_dfci_final_report.md "
                 "(P1: must use YYYY-MM-DD_caseid_type.md naming)"])
    low = txt.lower()
    # layer 2: structure (P2 four sections)
    for section in ("background", "evidence", "classification", "recommendation"):
        if section not in low:
            fails.append("missing mandatory section '%s' (P2)" % section)
    # layer 3: truth (A+D: more anchors; V4 numerical closure)
    if "6 retractions" not in low and "6 retraction" not in low:
        fails.append("final report must contain '6 retractions'")
    if "31 corrections" not in low and "31 correction" not in low:
        fails.append("final report must contain '31 corrections'")
    if "15,000,000" not in txt and "15000000" not in txt:
        fails.append("final report must contain '$15,000,000' settlement figure")
    if "10.1126/science.1123480" not in txt:
        fails.append("final report must reference DOI '10.1126/science.1123480' (Glimcher Science 2006)")
    # A: retraction DOI must also be present
    if "10.1126/science.adp1104" not in txt:
        fails.append("final report must include retraction DOI '10.1126/science.adp1104' (Glimcher retraction notice DOI)")
    if "95" not in txt:
        fails.append("final report must contain '95' (updated paper count per Update 1)")
    if "cope" not in low:
        fails.append("final report must reference COPE classification")
    # D: whistleblower figure must be cited
    if "2,630,000" not in txt and "2630000" not in txt:
        fails.append("final report must cite whistleblower share '$2,630,000' (from settlement_summary.md)")
    # D: independent blog count 47 must appear
    if "47" not in txt:
        fails.append("final report must reference the independent blog analysis figure '47' (image-pair anomalies)")
    # Glimcher figures: both Fig. 1A and Fig. 6A must be explicitly cited (verbatim from retraction notice)
    if "Fig. 1A" not in txt and "fig. 1a" not in low:
        fails.append(
            "final report must explicitly cite 'Fig. 1A' (one of the two flagged panels in "
            "the Glimcher Science 2006 retraction — both Fig. 1A and Fig. 6A were flagged)"
        )
    if "Fig. 6A" not in txt and "fig. 6a" not in low:
        fails.append(
            "final report must explicitly cite 'Fig. 6A' (the second flagged panel in "
            "the Glimcher Science 2006 retraction notice)"
        )
    _finish(fails)
main()
