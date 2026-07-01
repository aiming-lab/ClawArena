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
    data, err = _load_json(ws / "reports" / "compliance_issues_q1.json")
    if err: _finish([err])
    issues = data.get("issues") or data.get("items") or []
    # Must identify at least 6 distinct compliance problems (as stated in the question)
    if not isinstance(issues, list) or len(issues) < 6:
        fails.append("issues array must have at least 6 entries — the draft contains at least six distinct compliance problems (got %r)" % len(issues))
        _finish(fails)
    # Structural check: each issue must have required keys including ftc_citation
    required_keys = {"issue_id", "claim_text", "violated_rule", "citable_section", "severity", "ftc_citation"}
    for i, iss in enumerate(issues):
        if not isinstance(iss, dict):
            fails.append("issue[%d] is not a JSON object" % i); continue
        missing = required_keys - set(iss.keys())
        if missing:
            fails.append("issue[%d] missing keys: %s" % (i, sorted(missing)))
        else:
            cit = str(iss.get("ftc_citation",""))
            if not re.match(r"16 CFR §\d", cit):
                fails.append("issue[%d] ftc_citation '%s' does not match '16 CFR §XXX.X' format" % (i, cit[:30]))
    # Truth layer: must flag 'clinically demonstrated' as a violation
    all_texts = " ".join(str(iss.get("claim_text","")) + " " + str(iss.get("violated_rule",""))
                         for iss in issues if isinstance(iss, dict)).lower()
    if "clinically demonstrated" not in all_texts and "clinically" not in all_texts:
        fails.append("issues must flag 'clinically demonstrated' claim (Health Products Guidance violation)")
    # must flag all FTC-prohibited qualifying terms present in the draft
    for term, label in [("may", "may help"), ("promis", "promising"), ("preliminary", "preliminary"),
                        ("initial", "initial"), ("pilot", "pilot")]:
        if term not in all_texts:
            fails.append("issues must flag FTC-prohibited qualifying term '%s' found in the draft" % label)
    # must flag employee review issue (§465.3)
    if "465.3" not in all_texts and "employee" not in all_texts and "insider" not in all_texts:
        fails.append("issues must flag the employee review without disclosure directive (§465.3)")
    # severity values must be valid
    valid_severity = {"high", "medium", "low"}
    for iss in issues:
        if isinstance(iss, dict):
            sev = str(iss.get("severity", "")).lower()
            if sev and sev not in valid_severity:
                fails.append("severity '%s' not in high/medium/low" % sev)
    _finish(fails)
main()
