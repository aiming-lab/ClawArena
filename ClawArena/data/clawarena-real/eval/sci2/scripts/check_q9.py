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
    data, err = _load_json(ws / "rca_outputs" / "capa_comparison.json")
    if err: _finish([err])
    # case_A root_cause_category
    case_a = data.get("case_A") or data.get("case_a") or {}
    if not isinstance(case_a, dict):
        _finish(["case_A must be a JSON object"])
    rcc_a = str(case_a.get("root_cause_category", "")).lower()
    if "hardware" not in rcc_a:
        fails.append("case_A.root_cause_category %r must contain 'hardware'" % rcc_a)
    # case_B root_cause_category
    case_b = data.get("case_B") or data.get("case_b") or {}
    if not isinstance(case_b, dict):
        _finish(["case_B must be a JSON object"])
    rcc_b = str(case_b.get("root_cause_category", "")).lower()
    if "software" not in rcc_b:
        fails.append("case_B.root_cause_category %r must contain 'software'" % rcc_b)
    # case_B CAPA 行动须含 5.10.2
    capa_b = case_b.get("capa_actions") or []
    capa_txt = json.dumps(capa_b, ensure_ascii=False)
    if "5.10.2" not in capa_txt:
        fails.append("case_B.capa_actions must reference updating to v5.10.2")
    # C★ 跨轮闭合：与 Q8 产物 ivenix_recall_metadata.json 交叉验证 fixed_version 一致性
    meta8_path = ws / "rca_outputs" / "ivenix_recall_metadata.json"
    if meta8_path.exists():
        try:
            meta8 = json.loads(meta8_path.read_text(encoding="utf-8"))
            q8_fixed = str(meta8.get("fixed_version", ""))
            if q8_fixed and q8_fixed not in capa_txt:
                fails.append(
                    "cross-round consistency failure: case_B.capa_actions must reference version '%s' "
                    "(the fixed_version recorded in ivenix_recall_metadata.json from Q8) — "
                    "Q9 CAPA actions must be consistent with the corrective version identified in Q8" % q8_fixed
                )
            q8_ims = str(meta8.get("ims_fixed_version", ""))
            if q8_ims and q8_ims not in capa_txt:
                fails.append(
                    "cross-round consistency failure: case_B.capa_actions should reference IMS version '%s' "
                    "(from ivenix_recall_metadata.json ims_fixed_version in Q8) — "
                    "complete CAPA must address both LVP and IMS updates" % q8_ims
                )
        except Exception as e:
            fails.append("could not cross-check with ivenix_recall_metadata.json: %s" % e)
    else:
        fails.append(
            "ivenix_recall_metadata.json not found — Q9 requires Q8 output for cross-round "
            "consistency verification of CAPA software versions"
        )
    _finish(fails)
main()
