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

def _csv_rows(p):
    """Read CSV and return (header, data_rows). Returns (None, []) if file missing."""
    p = Path(p)
    if not p.exists():
        return None, []
    with p.open(encoding="utf-8") as fh:
        rows = [r for r in fh if not r.strip().startswith("#")]
    if not rows:
        return None, []
    reader = csv.DictReader(iter(rows))
    data = list(reader)
    return reader.fieldnames, data

def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "output" / "mifir_field28_correction.md")
    if txt is None:
        _finish(["file not found: output/mifir_field28_correction.md"])
    # 真值层
    if "Field 28" not in txt:
        fails.append("report must contain 'Field 28' (verbatim MiFIR field name)")
    if "UTC" not in txt:
        fails.append("report must contain 'UTC'")
    if "Market Watch 59" not in txt:
        fails.append("report must reference 'Market Watch 59' (FCA publication)")
    low = txt.lower()
    if not re.search(r"dst|daylight|summer time|bst|winter|clock|clocks", low):
        fails.append("report must mention DST / daylight saving time transition")
    # 精确时区值：必须同时注明错误值 UTC-4 和正确值 UTC-5
    if "UTC-4" not in txt and "UTC\u22124" not in txt:
        fails.append(
            "report must explicitly state the incorrect offset 'UTC-4' "
            "(the value AROS used in Field 28 timestamps)"
        )
    if "UTC-5" not in txt and "UTC\u22125" not in txt:
        fails.append(
            "report must explicitly state the correct offset 'UTC-5' "
            "(EST, the value that should have been used)"
        )
    # 必须引用 FCA 全机构名
    if "FCA" not in txt and "Financial Conduct Authority" not in txt:
        fails.append(
            "report must reference 'FCA' or 'Financial Conduct Authority' as the issuing regulator"
        )
    # V9 verbatim: 必须引用技术标准名称 RTS 22（从 fca_market_watch_59_summary.md 可查）
    if "RTS 22" not in txt and "Regulatory Technical Standard 22" not in txt and "RTS22" not in txt:
        fails.append(
            "report must cite 'RTS 22' or 'Regulatory Technical Standard 22' "
            "(the technical standard underlying the Field 28 requirement, "
            "per FCA Market Watch 59 and regulatory/fca_market_watch_59_summary.md)"
        )
    _finish(fails)
main()
