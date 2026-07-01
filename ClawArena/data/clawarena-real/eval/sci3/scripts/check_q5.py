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

def _read_csv(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        with p.open(encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        return rows, None
    except Exception as e:
        return None, "CSV error in " + p.name + ": " + str(e)

def _finish(fails):
    if fails:
        for f in fails:
            print("FAILED: " + f)
        sys.exit(1)
    print("PASSED")
    sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "output" / "exemption_analysis.md")
    if txt is None:
        _finish(["file not found: output/exemption_analysis.md"])
    low = txt.lower()
    # 真值层 1: seasonal flu NOT auto-exempt
    if not (re.search(r"flu|influenza", low) and re.search(r"not.{0,30}(auto|exempt)|cannot.{0,30}exempt", low)):
        # alternate phrasing
        if not re.search(r"(seasonal|influenza|flu).{0,60}not.{0,30}(automatically|auto).{0,30}(exempt|qualify|qualif)", low):
            fails.append("must state seasonal flu/influenza does NOT automatically qualify as exempt (AFL-23-27)")
    # 真值层 2: Prong 3 failure (on-call list not exhausted)
    if not re.search(r"prong.{0,5}3|on.call.{0,15}list.{0,30}(not|exhaust|fail)", low):
        fails.append("must identify Prong 3 failure: on-call list was not fully exhausted for Med/Surg")
    # 真值层 3: verbatim AFL-23-27 language (near-verbatim)
    afl_phrase = "immediately used and subsequently exhausted"
    if afl_phrase not in low:
        # relax: accept paraphrase with key words
        if not (re.search(r"exhaust.{0,20}on.call", low) and re.search(r"immedi", low)):
            fails.append("must include AFL-23-27 language: 'immediately used and subsequently exhausted the ... on-call list'")
    # 结构层: at least 2 sections (one per violation group)
    h3_count = len(re.findall(r"^### ", txt, re.MULTILINE))
    if h3_count < 2:
        fails.append("fewer than 2 ### headings (expected one per violation group)")
    _finish(fails)
main()
main()
