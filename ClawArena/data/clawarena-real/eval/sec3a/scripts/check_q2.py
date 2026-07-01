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
    txt = _read(ws / "output" / "timezone_bug_report.md")
    if txt is None:
        _finish(["file not found: output/timezone_bug_report.md"])
    low = txt.lower()
    # 真值层：必须包含正确值和错误值（case-insensitive）
    if "utc-4" not in low and "utc_offset = -4" not in low and "utc_offset=-4" not in low:
        fails.append("report must mention UTC-4 (the wrong value)")
    if "utc-5" not in low and "utc_offset = -5" not in low and "utc_offset=-5" not in low:
        fails.append("report must mention UTC-5 (the correct EST value)")
    # 必须引用行号
    if not re.search(r"line \d+", low):
        fails.append("report must reference a line number (e.g., 'line 47')")
    # V6 guard: 不得引用 deprecated legacy 文件作为来源
    if re.search(r"aros_v3_1_router_deprecated|timezone_config_v3_archive", low):
        fails.append("report must not cite deprecated legacy files as the bug source")
    _finish(fails)
main()
