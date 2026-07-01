#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, csv, hashlib
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

VALID_OVERALL = {"COMPLIANT", "PARTIALLY_COMPLIANT", "NON_COMPLIANT"}
BOOL_FIELDS = ["article_30_compliant", "article_33_compliant", "article_37_compliant"]
REQUIRED_KEYS = [
    "audit_date", "company_id", "dpo_name", "overall_status",
    "article_30_compliant", "article_33_compliant", "article_37_compliant",
    "article_83_max_exposure_eur", "signoff"
]

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "audit" / "gdpr_audit_certificate.json")
    if err: _finish([err])
    # All required keys present
    for k in REQUIRED_KEYS:
        if k not in data:
            fails.append("missing required key: %s" % k)
    # Boolean fields must be string "TRUE" or "FALSE" (P4)
    for f in BOOL_FIELDS:
        v = data.get(f)
        if v not in ("TRUE", "FALSE"):
            fails.append("%s == %r (must be string \"TRUE\" or \"FALSE\")" % (f, v))
    # overall_status must be valid enum (P5)
    os_ = data.get("overall_status")
    if os_ not in VALID_OVERALL:
        fails.append("overall_status == %r (must be COMPLIANT/PARTIALLY_COMPLIANT/NON_COMPLIANT)" % os_)
    # article_83_max_exposure_eur must be 20,000,000 (tier2_max from Q11)
    try:
        exp = int(data.get("article_83_max_exposure_eur", 0))
        if not (19_000_000 <= exp <= 21_000_000):
            fails.append("article_83_max_exposure_eur == %d (expected 20,000,000 from Q11 tier2_max)" % exp)
    except (TypeError, ValueError):
        fails.append("article_83_max_exposure_eur not an int")
    # signoff must match VERIFIED:<sha256> and cross-check with Q16
    signoff = str(data.get("signoff", ""))
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64})", signoff)
    if not m:
        fails.append("signoff must match VERIFIED:[a-f0-9]{64} (got %r)" % signoff[:80])
    else:
        # Cross-round closure: verify against compliance_summary.json
        target = ws / "audit" / "compliance_summary.json"
        if target.exists():
            actual = hashlib.sha256(target.read_bytes()).hexdigest()
            if m.group(1) != actual:
                fails.append("signoff sha256 mismatch with compliance_summary.json (cross-round closure violation)")
    # company_id must reference VeritasCloud
    cid = str(data.get("company_id", ""))
    if "veritascloud" not in cid.lower() and "veritas" not in cid.lower():
        fails.append("company_id %r does not reference VeritasCloud GmbH" % cid)
    # dpo_name must be non-empty
    if not data.get("dpo_name") or str(data.get("dpo_name","")).strip() == "":
        fails.append("dpo_name must be non-empty")
    _finish(fails)
main()
