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

def _finish(fails):
    if fails:
        for f in fails:
            print("FAILED: " + f)
        sys.exit(1)
    print("PASSED")
    sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    # P1: correct filename
    p = ws / "output" / "2023-07-12_gino_final_report.md"
    txt = _read(p)
    if txt is None:
        _finish(["file not found: output/2023-07-12_gino_final_report.md (P1 naming convention required)"])
    low = txt.lower()
    # P2: four sections
    for section in ("## background", "## evidence", "## classification", "## recommendation"):
        if section not in low:
            fails.append("report missing section '%s' (P2 requires all four sections)" % section)
    # V4: N=101
    if "101" not in txt:
        fails.append("report must state N=101")
    # V4: F-statistic notation must be F(2,596)=17.69 or F(2, 596) = 17.69
    if "17.69" not in txt:
        fails.append("report must include F-statistic 17.69")
    if "f(2,596)" not in low and "f(2, 596)" not in low:
        fails.append("report must include F-statistic in notation F(2,596) or F(2, 596)")
    # calcChain mention
    if "calcchain" not in low:
        fails.append("report must mention calcChain")
    # V9: all 4 original DOIs
    for doi in ("10.1073/pnas.1209746109", "10.1177/0956797614520714",
                "10.1177/0956797615575277", "10.1037/pspa0000226"):
        if doi not in txt:
            fails.append("report missing original DOI %s" % doi)
    # V9+D: all 4 retraction DOIs must also appear in the report
    for retract_doi in ("10.1073/pnas.2115397118", "10.1177/09567976231187595",
                        "10.1177/09567976231187596"):
        if retract_doi not in txt:
            fails.append("report missing retraction DOI %s (include retraction DOIs, not just originals)" % retract_doi)
    # p_puzzle must appear in the report
    if "0.0013" not in txt:
        fails.append("report must cite p=0.0013 (puzzle overreporting p-value from Data Colada [109])")
    # C+F: must cite p_expense=0.0014 (Welch t-test p-value from statistical_reference.json)
    if "0.0014" not in txt:
        fails.append("report must cite p=0.0014 (expense t-test p-value from statistical_reference.json; cross-round consistency with q9)")
    # C+F: must cite word_rating_mismatch_count=18 (from part4_why_connect.md)
    if "18" not in txt:
        fails.append("report must cite 18 word-rating mismatches (from part4_why_connect.md; required cross-round with q6)")
    # C+F: must cite prevention_corr_p=0.026 (from part4_why_connect.md)
    if "0.026" not in txt:
        fails.append("report must cite prevention-control correlation difference p=0.026 (from part4_why_connect.md)")
    _finish(fails)
main()
