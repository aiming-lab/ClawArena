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
    data, err = _load_json(ws / "output" / "ratios_baseline.json")
    if err: _finish([err])
    # 结构层：units 数组
    units = data.get("units") or data.get("ratios") or []
    if not isinstance(units, list) or len(units) < 6:
        fails.append("units array must have at least 6 entries (got %r)" % len(units))
        _finish(fails)
    # 建立 unit -> entry 索引（支持多种 unit 名写法）
    def norm(s):
        s = str(s).lower().replace("-", "").replace("/", "").replace(" ", "")
        return s
    by_unit = {}
    for e in units:
        if isinstance(e, dict):
            u = norm(e.get("unit", ""))
            by_unit[u] = e
    # 真值层：每个科室最大患者数
    EXPECTED = {
        "icu": 2, "intensivecareunit": 2, "criticalcare": 2,
        "medsurg": 5, "medicalsurgical": 5, "medicalsurg": 5,
        "stepdown": 3, "intermediatecareunit": 3, "progressivecare": 3,
        "telemetry": 4,
        "ed": 4, "emergencydepartment": 4, "emergency": 4,
        "psychiatric": 6, "psych": 6, "psychiatricunit": 6,
    }
    UNIT_ALIASES = {
        "icu": ["icu", "intensivecareunit", "criticalcare"],
        "medsurg": ["medsurg", "medicalsurgical", "medicalsurg"],
        "stepdown": ["stepdown", "intermediatecareunit", "progressivecare", "stepdownunit"],
        "telemetry": ["telemetry"],
        "ed": ["ed", "emergencydepartment", "emergency"],
        "psych": ["psychiatric", "psych", "psychiatricunit"],
    }
    for canonical, aliases in UNIT_ALIASES.items():
        entry = None
        for a in aliases:
            if a in by_unit:
                entry = by_unit[a]
                break
        if entry is None:
            fails.append("no entry found for unit group %r" % canonical)
            continue
        max_p = None
        for k in ("legal_ratio_max_patients", "max_patients", "ratio_max_patients", "max"):
            if k in entry:
                try:
                    max_p = int(entry[k])
                except (ValueError, TypeError):
                    pass
                break
        expected = EXPECTED[aliases[0]]
        if max_p is None:
            fails.append("%s: could not find legal_ratio_max_patients field" % canonical)
        elif max_p != expected:
            fails.append("%s: legal_ratio_max_patients == %r (expected %d)" % (canonical, max_p, expected))
        # regulation_ref must contain "§ 70217"
        ref = str(entry.get("regulation_ref", ""))
        if "70217" not in ref:
            fails.append("%s: regulation_ref %r does not contain '§ 70217' or '70217'" % (canonical, ref[:50]))
    # effective_date checks
    for e in units:
        if not isinstance(e, dict):
            continue
        u = norm(e.get("unit", ""))
        ed = str(e.get("effective_date", ""))
        if u in ("icu", "intensivecareunit", "criticalcare"):
            if ed and ed != "2004-01-01":
                fails.append("ICU effective_date == %r (expected 2004-01-01)" % ed)
        if u in ("stepdown", "stepdownunit", "intermediatecareunit"):
            if ed and ed != "2008-01-01":
                fails.append("Step-Down effective_date == %r (expected 2008-01-01)" % ed)
        if u in ("telemetry",):
            if ed and ed != "2008-01-01":
                fails.append("Telemetry effective_date == %r (expected 2008-01-01)" % ed)
    _finish(fails)
main()
main()
