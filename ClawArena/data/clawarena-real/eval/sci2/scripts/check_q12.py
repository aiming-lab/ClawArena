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
    data, err = _load_json(ws / "rca_outputs" / "ivenix_recall_metadata_v2.json")
    if err: _finish([err])
    # units_software_kits 必须为 "undisclosed"（不能保留 "30"）
    usk = str(data.get("units_software_kits", "")).lower().strip()
    if usk == "30" or usk == 30:
        fails.append("units_software_kits == '30' — Update 2 superseded this; must be 'undisclosed'")
    if "undisclosed" not in usk:
        fails.append("units_software_kits %r must be 'undisclosed' per Update 2 supersede" % usk)
    # 仍须含正确软件版本
    asv = str(data.get("affected_software_version", ""))
    if "5.10.1" not in asv:
        fails.append("affected_software_version must still contain '5.10.1' in v2 output")
    # 召回号
    rn = str(data.get("recall_number", ""))
    if "Z-0885-2026" not in rn:
        fails.append("recall_number must be 'Z-0885-2026'")
    # C★ 跨轮闭合：与 Q8 产物 ivenix_recall_metadata.json 交叉验证关键字段
    meta8_path = ws / "rca_outputs" / "ivenix_recall_metadata.json"
    if meta8_path.exists():
        try:
            meta8 = json.loads(meta8_path.read_text(encoding="utf-8"))
            v2_btp = data.get("battery_threshold_pct")
            q8_btp = meta8.get("battery_threshold_pct")
            if v2_btp is not None and q8_btp is not None:
                try:
                    if int(v2_btp) != int(q8_btp):
                        fails.append(
                            "cross-round consistency failure: ivenix_recall_metadata_v2.json "
                            "battery_threshold_pct (%s) must match ivenix_recall_metadata.json "
                            "battery_threshold_pct (%s) from Q8 — v2 must carry forward Q8 values" % (v2_btp, q8_btp)
                        )
                except (TypeError, ValueError):
                    pass
            elif v2_btp is None:
                fails.append(
                    "ivenix_recall_metadata_v2.json missing battery_threshold_pct — "
                    "v2 must carry forward all fields from Q8 (only units_software_kits changes)"
                )
            v2_inj = data.get("injuries")
            q8_inj = meta8.get("injuries")
            if v2_inj is not None and q8_inj is not None:
                try:
                    if int(v2_inj) != int(q8_inj):
                        fails.append(
                            "cross-round consistency failure: injuries (%s in v2) must match Q8 value (%s)" % (v2_inj, q8_inj)
                        )
                except (TypeError, ValueError):
                    pass
        except Exception as e:
            fails.append("could not cross-check with ivenix_recall_metadata.json: %s" % e)
    else:
        fails.append(
            "ivenix_recall_metadata.json (Q8 output) not found — Q12 v2 update requires Q8 "
            "as its source for carry-forward fields"
        )
    _finish(fails)
main()
