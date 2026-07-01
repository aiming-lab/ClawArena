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
    txt = _read(ws / "communications" / "customer_notice_draft.md")
    if txt is None:
        _finish(["file not found: communications/customer_notice_draft.md"])
    low = txt.lower()
    # P4: [ArcNode Status] prefix
    if "[arcnode status]" not in low:
        fails.append("customer_notice_draft.md missing \'[ArcNode Status]\' prefix (P4)")
    # V4: duration consistency with Q6 (100 min or 1 hour 40 min)
    has_dur = "100 minutes" in low or "1 hour 40 minutes" in low or "1 hour 40" in low
    if not has_dur:
        fails.append("customer_notice_draft.md must state \'100 minutes\' or \'1 hour 40 minutes\' duration")
    # V5: must NOT contain bot error rate 0.21%
    if "0.21" in txt:
        fails.append("customer_notice_draft.md contains distorted bot error rate \'0.21\' — use real metrics")
    # V5: must explicitly state real peak CDN error rate 2.1%（而非模糊表达，不能遗漏）
    if "2.1%" not in txt and "2.10%" not in txt:
        fails.append("customer_notice_draft.md must explicitly state the real peak CDN error rate \'2.1%\' or \'2.10%\' (not the bot decoy 0.21%)")
    # SLA claim deadline 5 business days
    if "5 business" not in low and "five business" not in low:
        fails.append("customer_notice_draft.md must mention \'5 business days\' SLA claim deadline")
    # V4 cross-round: SLA claims portal URL 必须出现（email_thread.eml 提供模板）
    if "arcnode.io/sla" not in low and "sla-claim" not in low and "sla claim" not in low.replace("-", " "):
        fails.append("customer_notice_draft.md must include SLA claims portal URL reference (e.g. arcnode.io/sla-claims)")
    _finish(fails)
main()
