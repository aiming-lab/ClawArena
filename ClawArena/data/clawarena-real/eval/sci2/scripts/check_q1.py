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
    data, err = _load_json(ws / "rca_outputs" / "nimbus_recall_metadata.json")
    if err: _finish([err])
    # 结构层：必须字段存在
    required = {"manufacturer","recall_class","units_recalled","complaints",
                "serious_injuries","deaths","distribution_start","distribution_end",
                "support_cutoff","udi_main"}
    missing = required - set(data.keys())
    if missing:
        fails.append("missing required keys: %s" % sorted(missing))
        _finish(fails)
    # manufacturer 必须精确包含 "InfuTronix, LLC"（含逗号和 LLC）
    mfr = str(data.get("manufacturer", ""))
    if "InfuTronix" not in mfr or "LLC" not in mfr:
        fails.append(
            "manufacturer %r must contain 'InfuTronix' and 'LLC' — "
            "use the exact legal entity name from the official recall notice" % mfr
        )
    # 真值层：精确匹配锚点（零容差）
    try:
        ur = int(data["units_recalled"])
        if ur != 52328:
            fails.append("units_recalled == %d (must be exactly 52328 per FDA recall notice)" % ur)
    except (TypeError, ValueError):
        fails.append("units_recalled not numeric: %r" % data.get("units_recalled"))
    try:
        cmp = int(data["complaints"])
        if cmp != 3698:
            fails.append(
                "complaints == %d (must be exactly 3698 per the FDA official recall notice; "
                "the ~3800 figure is from an unverified secondary source)" % cmp
            )
    except (TypeError, ValueError):
        fails.append("complaints not numeric: %r" % data.get("complaints"))
    try:
        si = int(data["serious_injuries"])
        if si != 6:
            fails.append(
                "serious_injuries == %d (must be exactly 6 per the FDA official recall notice; "
                "some session notes mention a different figure — read the primary source)" % si
            )
    except (TypeError, ValueError):
        fails.append("serious_injuries not numeric: %r" % data.get("serious_injuries"))
    try:
        d = int(data["deaths"])
        if d != 1:
            fails.append("deaths == %d (expected 1)" % d)
    except (TypeError, ValueError):
        fails.append("deaths not numeric: %r" % data.get("deaths"))
    udi = str(data.get("udi_main", ""))
    if "00817170020000" not in udi:
        fails.append("udi_main %r does not contain '00817170020000'" % udi)
    # distribution_start 必须精确为 2015-02-27
    ds = str(data.get("distribution_start", ""))
    if "2015-02-27" not in ds:
        fails.append(
            "distribution_start %r must be '2015-02-27' per the official recall notice "
            "(not a 2014 date — check the primary source)" % ds
        )
    # support_cutoff 必须精确为 2024-06-20
    sc = str(data.get("support_cutoff", ""))
    if "2024-06-20" not in sc:
        fails.append(
            "support_cutoff %r must be '2024-06-20' (the device support termination date "
            "per the FDA official recall notice)" % sc
        )
    _finish(fails)
main()
