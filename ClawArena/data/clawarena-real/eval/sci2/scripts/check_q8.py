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
    data, err = _load_json(ws / "rca_outputs" / "ivenix_recall_metadata.json")
    if err: _finish([err])
    # 必须字段（含 units_software_kits）
    required = {"recall_number","affected_software_version","product_code",
                "fixed_version","ims_fixed_version","injuries",
                "battery_threshold_pct","anomaly_1","anomaly_2","units_software_kits"}
    missing = required - set(data.keys())
    if missing:
        fails.append("missing required keys: %s" % sorted(missing))
        _finish(fails)
    # V2: 不得只写 5.10.0；必须含 5.10.1
    asv = str(data.get("affected_software_version", ""))
    if "5.10.1" not in asv:
        fails.append("affected_software_version %r must contain '5.10.1' (Update 1 corrected this from 5.10.0 only)" % asv)
    # V9: 召回号 verbatim
    rn = str(data.get("recall_number", ""))
    if "Z-0885-2026" not in rn:
        fails.append("recall_number %r must be 'Z-0885-2026'" % rn)
    # 电池阈值
    try:
        btp = int(data.get("battery_threshold_pct"))
        if btp != 70:
            fails.append("battery_threshold_pct == %d (expected 70)" % btp)
    except (TypeError, ValueError):
        fails.append("battery_threshold_pct not numeric: %r" % data.get("battery_threshold_pct"))
    # 伤害数（必须为 2；bot_summary_HONEYPOT 写的是 5，不得被误导）
    try:
        inj = int(data.get("injuries"))
        if inj != 2:
            fails.append("injuries == %d (expected 2 per manufacturing chemist report as of Nov 18 2025; "
                         "bot summary erroneously stated 5)" % inj)
    except (TypeError, ValueError):
        fails.append("injuries not numeric: %r" % data.get("injuries"))
    # IMS 修复版本必须精确为 "5.2.2"
    ims = str(data.get("ims_fixed_version", ""))
    if ims != "5.2.2":
        fails.append(
            "ims_fixed_version %r must be exactly '5.2.2' (verbatim from anomaly investigation document)" % ims
        )
    # anomaly_1 必须提及 "battery" 相关内容
    a1 = str(data.get("anomaly_1", "")).lower()
    if "battery" not in a1 and "soc" not in a1 and "state-of-charge" not in a1:
        fails.append("anomaly_1 %r must describe the battery state-of-charge reporting error" % str(data.get("anomaly_1", "")))
    # anomaly_2 必须提及 dual-zero / 双零输入相关
    a2 = str(data.get("anomaly_2", "")).lower()
    if "dual" not in a2 and "zero" not in a2 and "freeze" not in a2 and "leading" not in a2:
        fails.append("anomaly_2 %r must describe the dual-zero rate entry interface freeze" % str(data.get("anomaly_2", "")))
    _finish(fails)
main()
