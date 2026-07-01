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
    data, err = _load_json(ws / "output" / "update2_supersede_log.json")
    if err: _finish([err])
    # superseded_items 必须含 IP indemnification 相关内容
    si = [str(x).lower() for x in (data.get("superseded_items") or [])]
    si_str = " ".join(si)
    if "ip" not in si_str and "indemnif" not in si_str and "procure" not in si_str:
        fails.append("superseded_items must include the IP indemnification narrowing from v2.4 "
                     "(specifically the removal of procure rights and security patch exclusion)")
    # not_superseded_items 必须含 liability cap 相关内容（6 个月仍在谈判）
    nsi = [str(x).lower() for x in (data.get("not_superseded_items") or [])]
    nsi_str = " ".join(nsi)
    if "cap" not in nsi_str and "liability" not in nsi_str and "month" not in nsi_str:
        fails.append("not_superseded_items must include the liability cap (6-month VendorX position "
                     "from v2.4 is NOT superseded — still under active negotiation)")
    # not_superseded_items 还必须含 force majeure 相关内容（FM notice period 也未被撤销）
    if "force majeure" not in nsi_str and "fm" not in nsi_str and "notice period" not in nsi_str and "majeure" not in nsi_str:
        fails.append("not_superseded_items must also include the force majeure notice period "
                     "(per the supersede notice email, the FM notice period change from v2.4 is NOT superseded "
                     "and remains under review)")
    # effective_position_source 必须引用 external counsel 或 v2.4-revised 或 supersede notice
    # 且必须引用律所名称 Morrison（来自 email_supersede_notice.json cc: owen.park@morrisonclarke.com）
    eps = str(data.get("effective_position_source", "")).lower()
    if ("external" not in eps and "counsel" not in eps and
            "revised" not in eps and "supersede" not in eps and "morrison" not in eps):
        fails.append("effective_position_source must reference the external counsel redline (v2.4-revised) "
                     "and/or the supersede notice email")
    if "morrison" not in eps and "v2.4-revised" not in eps and "v2.4_revised" not in eps and "revised" not in eps:
        fails.append(
            "effective_position_source must specifically reference the Morrison & Clarke LLP external counsel "
            "redline (MSA_VendorX_v2.4_REVISED_external_counsel.md) — the supersede notice email "
            "cc'd owen.park@morrisonclarke.com establishing this as the effective source"
        )
    # supersede_date 必须精确等于 2026-01-27（来自 email_supersede_notice.json date 字段）
    sd = str(data.get("supersede_date", "")).strip()
    if sd != "2026-01-27":
        fails.append(
            "supersede_date == %r (must be exactly '2026-01-27' per the supersede notice email "
            "from Jessica Lin, GC, dated 2026-01-27 — not an approximation)" % sd
        )
    _finish(fails)
main()
