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
    data, err = _load_json(ws / "output" / "kcg_anchor_check.json")
    if err: _finish([err])
    # financial_loss_usd: must be EXACTLY 460000000 (SEC Release 34-70694)
    # 440000000 is the media preliminary figure — must not be used
    loss = data.get("financial_loss_usd")
    try:
        loss = int(loss)
    except (TypeError, ValueError):
        _finish(["financial_loss_usd not an int: %r" % loss])
    if loss == 440000000:
        fails.append("financial_loss_usd == 440000000 is the preliminary media figure; "
                     "SEC Release 34-70694 confirms the authoritative figure is 460000000")
    if loss != 460000000:
        fails.append("financial_loss_usd == %d (must be exactly 460000000 per SEC Release 34-70694; "
                     "not approximate — read the source document)" % loss)
    # penalty_usd: exactly 12000000
    pen = data.get("penalty_usd")
    try:
        pen = int(pen)
    except (TypeError, ValueError):
        _finish(["penalty_usd not an int: %r" % pen])
    if pen != 12000000:
        fails.append("penalty_usd == %d (expected exactly 12,000,000)" % pen)
    # rule_violated: must contain 15c3-5 and the (b) sub-clause
    rule = str(data.get("rule_violated") or "")
    if "15c3-5" not in rule:
        fails.append("rule_violated %r does not reference Rule 15c3-5" % rule)
    if "(b)" not in rule and "(B)" not in rule:
        fails.append("rule_violated %r must include sub-clause (b) per P3" % rule)
    # servers_count: exactly 8
    svc = data.get("servers_count")
    try:
        svc = int(svc)
    except (TypeError, ValueError):
        _finish(["servers_count not an int: %r" % svc])
    if svc != 8:
        fails.append("servers_count == %d (expected 8)" % svc)
    # pre_market_emails: exactly 97
    ems = data.get("pre_market_emails")
    try:
        ems = int(ems)
    except (TypeError, ValueError):
        _finish(["pre_market_emails not an int: %r" % ems])
    if ems != 97:
        fails.append("pre_market_emails == %d (expected 97)" % ems)
    # shares_traded_millions: must be exactly 397.0 +/- 0.5 (tightened from +/-1)
    stm = data.get("shares_traded_millions")
    if stm is None:
        fails.append("shares_traded_millions field missing (required key)")
    else:
        try:
            stm = float(stm)
        except (TypeError, ValueError):
            _finish(["shares_traded_millions not a number: %r" % stm])
        if not (396.5 <= stm <= 397.5):
            fails.append(
                "shares_traded_millions == %.3f (expected 397.0 ± 0.5 per SEC Release 34-70694; "
                "read the primary source document for the exact figure)" % stm
            )
    # case_number: must include the exact Admin Proc file number from SEC Release 34-70694
    # Verbatim: "Admin. Proc. File No. 3-15570" (the official docket identifier)
    cn = str(data.get("case_number") or "")
    if not cn:
        fails.append(
            "case_number field missing — must be the verbatim Admin. Proc. File No. from "
            "SEC Release 34-70694 (e.g. 'Admin. Proc. File No. 3-15570')"
        )
    elif "3-15570" not in cn:
        fails.append(
            "case_number == %r does not contain '3-15570' "
            "(must be verbatim docket number from SEC Release 34-70694)" % cn[:60]
        )
    _finish(fails)
main()
