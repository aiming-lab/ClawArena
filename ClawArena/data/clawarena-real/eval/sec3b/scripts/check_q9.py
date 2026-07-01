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

def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "output" / "root_cause_analysis.md")
    if txt is None:
        _finish(["file not found: output/root_cause_analysis.md"])
    low = txt.lower()
    # Must contain incident date
    if "2024-11-03" not in txt:
        fails.append("RCA does not contain incident date '2024-11-03'")
    # Must mention both UTC-4 and UTC-5
    if "utc-4" not in txt and "utc -4" not in txt and "-4" not in txt:
        fails.append("RCA does not mention UTC-4 (the error offset)")
    if "utc-5" not in txt and "utc -5" not in txt and "-5" not in txt:
        fails.append("RCA does not mention UTC-5 (the correct offset)")
    # Must cite Rule 15c3-5 (P3: with sub-clause)
    if "15c3-5" not in txt:
        fails.append("RCA does not reference Rule 15c3-5")
    if not re.search(r"15c3-5\(b\)|15c3-5\s*\(b\)", txt, re.IGNORECASE):
        fails.append("RCA cites Rule 15c3-5 but not the (b) sub-clause (P3 requires sub-clause)")
    # Must cite Rule 15c6-1 (T+1 settlement) with its effective date
    if "15c6-1" not in txt:
        fails.append("RCA does not reference Rule 15c6-1 (T+1 settlement rule)")
    if "2024-05-28" not in txt:
        fails.append(
            "RCA does not cite Rule 15c6-1 effective date '2024-05-28' "
            "(cross-round closure: the exact effective date must appear in the regulatory violations section)"
        )
    # Must include BOTH the incorrect CME time (20:00 UTC) AND correct time (21:00 UTC)
    if "20:00" not in txt and "2000" not in txt:
        fails.append("RCA does not reference 20:00 UTC (the incorrect CME settlement time the system computed)")
    if "21:00" not in txt and "2100" not in txt:
        fails.append("RCA does not reference 21:00 UTC (the correct CME settlement time after DST switch)")
    # Must reference the total_affected order count from Round 3 (V4 cross-round closure)
    q3, e3 = _load_json(ws / "output" / "affected_orders_count.json")
    if not e3 and q3 is not None:
        ta = q3.get("total_affected")
        try:
            ta = int(ta)
            if ta > 0 and str(ta) not in txt:
                fails.append(
                    "RCA does not reference total_affected order count (%d) from Round 3 output "
                    "(V4 cross-round closure: the financial impact section must cite this figure)" % ta
                )
        except (TypeError, ValueError):
            pass
        # C★ Cross-round closure: must also cite audit_log_total_scanned from q3
        tsc = q3.get("audit_log_total_scanned")
        try:
            tsc = int(tsc)
            if tsc > 0 and str(tsc) not in txt:
                fails.append(
                    "RCA does not reference audit_log_total_scanned (%d) from Round 3 output "
                    "(C★ cross-round closure: the audit scope section must cite total lines scanned "
                    "from output/affected_orders_count.json — cross-check your Round 3 result)" % tsc
                )
        except (TypeError, ValueError):
            pass
    # C★ Cross-round closure: must cite exact KCG financial_loss_usd from Round 5
    q5, e5 = _load_json(ws / "output" / "kcg_anchor_check.json")
    if not e5 and q5 is not None:
        kcg_loss = q5.get("financial_loss_usd")
        try:
            kcg_loss = int(kcg_loss)
            if kcg_loss > 0 and str(kcg_loss) not in txt:
                fails.append(
                    "RCA does not cite the exact KCG financial_loss_usd (%d) from Round 5 output "
                    "(C★ cross-round closure: the KCG comparison section must quote the exact integer "
                    "from output/kcg_anchor_check.json — both the string '%d' must appear)" % (kcg_loss, kcg_loss)
                )
        except (TypeError, ValueError):
            pass
    # Must NOT contain $440M as an authoritative figure (only as a decoy reference)
    if "440" in txt and "440m" in txt.lower():
        if "460" not in txt:
            fails.append("RCA mentions '$440M' without the correct '$460M+' figure (use SEC-verified number)")
    _finish(fails)
main()
