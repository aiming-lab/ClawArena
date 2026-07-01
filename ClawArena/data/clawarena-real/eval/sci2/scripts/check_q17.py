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
    data, err = _load_json(ws / "rca_outputs" / "compliance_checklist.json")
    if err: _finish([err])
    items = data.get("items")
    if not isinstance(items, list) or len(items) < 10:
        _finish(["items must be a list with >= 10 entries (got %r)" % (len(items) if isinstance(items, list) else type(items))])
    # 索引
    items_by_id = {str(it.get("id","")): it for it in items if isinstance(it, dict)}
    # 必须含 required_ids 中全部五个 id
    required_ids = {"MDR-30DAY", "RECALL-REPORT", "IVENIX-SOFTWARE", "NIMBUS-CAPA", "HONEYPOT-FLAGS"}
    missing_ids = required_ids - set(items_by_id.keys())
    if missing_ids:
        fails.append("compliance_checklist.json missing required item ids: %s" % sorted(missing_ids))
    # MDR-30DAY: cfr_citation 必须含 "21 CFR 803.50(a)(1)"
    mdr30 = items_by_id.get("MDR-30DAY")
    if mdr30 is not None:
        cit = str(mdr30.get("cfr_citation",""))
        if "803.50(a)(1)" not in cit or "21 CFR" not in cit:
            fails.append("MDR-30DAY cfr_citation %r must be '21 CFR 803.50(a)(1)'" % cit)
    # RECALL-REPORT: cfr_citation 必须含 "21 CFR 806.10"
    rr = items_by_id.get("RECALL-REPORT")
    if rr is not None:
        cit = str(rr.get("cfr_citation",""))
        if "806.10" not in cit or "21 CFR" not in cit:
            fails.append("RECALL-REPORT cfr_citation %r must contain '21 CFR 806.10'" % cit)
    # IVENIX-SOFTWARE: evidence_file 须含 ivenix_recall_metadata_v2（不得只有 v1）
    iv = items_by_id.get("IVENIX-SOFTWARE")
    if iv is not None:
        ef = str(iv.get("evidence_file","")).lower()
        if "ivenix_recall_metadata_v2" not in ef and "metadata_v2" not in ef:
            fails.append("IVENIX-SOFTWARE evidence_file %r must reference ivenix_recall_metadata_v2.json (v2, not v1)" % ef)
    # NIMBUS-CAPA: evidence_file 须含 capa; cfr_citation 必须精确含 "21 CFR 820.100"（不接受仅 "21 CFR 820"）
    nc = items_by_id.get("NIMBUS-CAPA")
    if nc is not None:
        ef = str(nc.get("evidence_file","")).lower()
        if "capa" not in ef:
            fails.append("NIMBUS-CAPA evidence_file %r must reference a CAPA-related output file" % ef)
        cfr = str(nc.get("cfr_citation",""))
        if "820.100" not in cfr or "21 CFR" not in cfr:
            fails.append(
                "NIMBUS-CAPA cfr_citation %r must be exactly '21 CFR 820.100' "
                "(the CAPA-specific subsection — not just '21 CFR 820')" % cfr
            )
    # HONEYPOT-FLAGS: evidence_file 须含 honeypot
    hf = items_by_id.get("HONEYPOT-FLAGS")
    if hf is not None:
        ef = str(hf.get("evidence_file","")).lower()
        if "honeypot" not in ef:
            fails.append("HONEYPOT-FLAGS evidence_file %r must reference the honeypot_flags.json output" % ef)
    # C★ 跨轮闭合：MDR-30DAY 引用的 evidence_file 必须实际存在于 rca_outputs/
    mdr30 = items_by_id.get("MDR-30DAY")
    if mdr30 is not None:
        ef = str(mdr30.get("evidence_file",""))
        if ef:
            ef_path = ws / "rca_outputs" / Path(ef).name
            if not ef_path.exists():
                fails.append(
                    "MDR-30DAY evidence_file '%s' does not exist in rca_outputs/ — "
                    "checklist evidence files must reference actual produced outputs" % ef
                )
    # C★ 跨轮闭合：IVENIX-SOFTWARE evidence_file 引用的 v2 文件必须存在
    iv = items_by_id.get("IVENIX-SOFTWARE")
    if iv is not None:
        ef = str(iv.get("evidence_file",""))
        if ef:
            ef_path = ws / "rca_outputs" / Path(ef).name
            if not ef_path.exists():
                fails.append(
                    "IVENIX-SOFTWARE evidence_file '%s' does not exist in rca_outputs/ — "
                    "must reference the actual Q12 output file" % ef
                )
    _finish(fails)
main()
