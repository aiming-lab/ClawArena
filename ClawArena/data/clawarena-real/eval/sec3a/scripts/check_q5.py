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

def _csv_rows(p):
    """Read CSV and return (header, data_rows). Returns (None, []) if file missing."""
    p = Path(p)
    if not p.exists():
        return None, []
    with p.open(encoding="utf-8") as fh:
        rows = [r for r in fh if not r.strip().startswith("#")]
    if not rows:
        return None, []
    reader = csv.DictReader(iter(rows))
    data = list(reader)
    return reader.fieldnames, data

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "kcg_anchor_check.json")
    if err: _finish([err])
    # 结构层
    for req in ("financial_loss_usd", "penalty_usd", "rule_violated", "servers_count",
                "pre_market_emails", "shares_traded", "customer_orders", "incident_date"):
        if req not in data:
            fails.append("missing field: " + req)
    if fails: _finish(fails)
    # 真值层（带容差）
    try:
        loss = int(data.get("financial_loss_usd"))
    except (TypeError, ValueError):
        _finish(["financial_loss_usd not an int"])
    # 440M is the decoy from bot_summary/preliminary report — check strictly: must be >= 450M
    if loss < 450_000_000:
        fails.append("financial_loss_usd == %d (expected >= 460,000,000; $440M is the decoy)" % loss)
    try:
        penalty = int(data.get("penalty_usd"))
    except (TypeError, ValueError):
        _finish(["penalty_usd not an int"])
    if not (10_800_000 <= penalty <= 13_200_000):
        fails.append("penalty_usd == %d (expected ~12,000,000)" % penalty)
    rule = str(data.get("rule_violated", ""))
    if "15c3-5(b)" not in rule:
        fails.append("rule_violated == %r (must contain '15c3-5(b)', not just '15c3-5')" % rule)
    try:
        srv = int(data.get("servers_count"))
    except (TypeError, ValueError):
        _finish(["servers_count not an int"])
    if srv != 8:
        fails.append("servers_count == %d (expected 8)" % srv)
    try:
        emails = int(data.get("pre_market_emails"))
    except (TypeError, ValueError):
        _finish(["pre_market_emails not an int"])
    if emails != 97:
        fails.append("pre_market_emails == %d (expected 97)" % emails)
    try:
        shares = int(data.get("shares_traded"))
    except (TypeError, ValueError):
        _finish(["shares_traded not an int"])
    if shares != 397_000_000:
        fails.append(
            "shares_traded == %d (expected 397,000,000 per SEC-confirmed case study)" % shares
        )
    try:
        cust = int(data.get("customer_orders"))
    except (TypeError, ValueError):
        _finish(["customer_orders not an int"])
    if cust != 212:
        fails.append(
            "customer_orders == %d (expected 212: the exact number of customer orders "
            "received by Knight Capital on August 1, 2012)" % cust
        )
    _finish(fails)
main()
