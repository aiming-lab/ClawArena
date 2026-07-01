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
    data, err = _load_json(ws / "reports" / "wip" / "discrepancy_conflict_record.json")
    if err: _finish([err])
    # layer 1: structure
    for key in ("institutional_discrepancy_count", "independent_discrepancy_count",
                "source_blog", "conflict_explanation"):
        if key not in data:
            fails.append("missing key: " + key)
    if fails: _finish(fails)
    # layer 2: types
    try:
        inst_count = int(data["institutional_discrepancy_count"])
        indep_count = int(data["independent_discrepancy_count"])
    except (TypeError, ValueError) as e:
        _finish(["numeric field type error: " + str(e)])
    conflict_exp = str(data.get("conflict_explanation", ""))
    if fails: _finish(fails)
    # layer 3: truth (A exact values; V1 multi-source conflict; V9 verbatim URL; V5 ResearchBot artefact rejection)
    if inst_count != 12:
        fails.append("institutional_discrepancy_count == %d (expected exactly 12 from imagetwin_report.json)" % inst_count)
    # independent_discrepancy_count: must be exactly 47 (from blog analysis)
    if indep_count != 47:
        fails.append("independent_discrepancy_count == %d (expected exactly 47 from independent blog analysis, not 89 ResearchBot artefact)" % indep_count)
    # V9 verbatim URL check
    expected_url = "https://forbetterscience.com/2024/01/02/dana-farberications-at-harvard-university/"
    if str(data.get("source_blog")) != expected_url:
        fails.append("source_blog == %r (expected exact URL '%s')" % (str(data.get("source_blog"))[:60], expected_url))
    if len(conflict_exp) < 20:
        fails.append("conflict_explanation too short (must be >= 20 chars explaining why counts differ)")
    # V5: ResearchBot 89 must not appear as either authoritative count
    if inst_count == 89 or indep_count == 89:
        fails.append("discrepancy count == 89 is the ResearchBot artefact; do not use it as authoritative")
    _finish(fails)
main()
