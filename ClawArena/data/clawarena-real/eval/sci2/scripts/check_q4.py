#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib
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
    data, err = _load_json(ws / "rca_outputs" / "regulatory_obligations.json")
    if err: _finish([err])
    # 必须字段完整
    required = {"mdr_30day_cfr", "mdr_5day_cfr", "recall_report_cfr", "recall_report_deadline_days"}
    missing = required - set(data.keys())
    if missing:
        fails.append("missing required keys: %s" % sorted(missing))
        _finish(fails)
    # verbatim 精确匹配
    mdr30 = str(data.get("mdr_30day_cfr", ""))
    if "803.50(a)(1)" not in mdr30 or "21 CFR" not in mdr30:
        fails.append("mdr_30day_cfr %r must contain '21 CFR 803.50(a)(1)'" % mdr30)
    mdr5 = str(data.get("mdr_5day_cfr", ""))
    if "803.53" not in mdr5 or "21 CFR" not in mdr5:
        fails.append("mdr_5day_cfr %r must contain '21 CFR 803.53'" % mdr5)
    rrcfr = str(data.get("recall_report_cfr", ""))
    if "806.10" not in rrcfr or "21 CFR" not in rrcfr:
        fails.append("recall_report_cfr %r must contain '21 CFR 806.10'" % rrcfr)
    deadline = data.get("recall_report_deadline_days")
    try:
        d = int(deadline)
        if d != 10:
            fails.append("recall_report_deadline_days == %d (expected 10 working days per 21 CFR 806.10)" % d)
    except (TypeError, ValueError):
        fails.append("recall_report_deadline_days not numeric: %r" % deadline)
    _finish(fails)
main()
