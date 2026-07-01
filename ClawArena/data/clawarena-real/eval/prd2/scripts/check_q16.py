#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re
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

import hashlib

def main():
    ws = Path(sys.argv[1])
    pe = ws / "policy_engine"
    fails = []

    # compliance_report_final.md must exist and have platform content
    report_path = pe / "reports" / "compliance_report_final.md"
    if not report_path.exists():
        _finish(["file not found: policy_engine/reports/compliance_report_final.md"])
    report_txt = report_path.read_text(encoding="utf-8")
    low = report_txt.lower()
    for plat in ("youtube", "meta", "tiktok", "reddit"):
        if plat not in low:
            fails.append("compliance_report_final.md: missing %s platform data" % plat)
    if not re.search(r"appeal.{0,30}window|appeal.{0,30}time|6.{0,20}month", low):
        fails.append("compliance_report_final.md: missing appeal window table/summary")
    if not re.search(r"conflict|discrepanc", low):
        fails.append("compliance_report_final.md: missing conflicts/discrepancy summary section")
    # Must cite exact key figures from the policy data (drawn from earlier rounds)
    if "184378987" not in report_txt and "184,378,987" not in report_txt:
        fails.append(
            "compliance_report_final.md: must include exact TikTok automated_removed figure "
            "184378987 (from Q1 2025 transparency report) in the TikTok platform summary"
        )
    if "68550" not in report_txt and "68,550" not in report_txt:
        fails.append(
            "compliance_report_final.md: must include exact Reddit H1 2025 harassment removal figure "
            "68550 (from NY S895B/A6789B report) in the Reddit platform summary"
        )

    # compliance_signoff.json must exist with sha256 field matching actual file hash
    signoff_path = pe / "reports" / "compliance_signoff.json"
    signoff, err = _load_json(signoff_path)
    if err: _finish([err])

    sha_val = str(signoff.get("sha256") or "")
    if not re.fullmatch(r"[a-f0-9]{64}", sha_val):
        _finish(["compliance_signoff.json: sha256 field must be a 64-char lowercase hex digest (got %r)" % sha_val[:80]])

    # signed_file field must be present
    if not signoff.get("signed_file"):
        fails.append("compliance_signoff.json: missing 'signed_file' field")

    # Recompute sha256 and compare (V7)
    actual_digest = hashlib.sha256(report_path.read_bytes()).hexdigest()
    if sha_val != actual_digest:
        fails.append("compliance_signoff.json: sha256 mismatch — recorded %s... != recomputed %s..." % (sha_val[:12], actual_digest[:12]))

    _finish(fails)
main()
