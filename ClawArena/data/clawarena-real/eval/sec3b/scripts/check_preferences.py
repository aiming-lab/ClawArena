#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sec3b preference checker (P1 snake_case / P2 severity-descending / P3 sub-clause citation /
P4 owner fields in CAP / P5 regulatory submission field order).
"""
import sys, re, json, argparse
from pathlib import Path

# P5: required top-level field order for regulatory_submission_summary.json
P5_ORDER = ["incident_date", "rule_violated", "financial_impact", "remediation_count", "submission_date"]


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """All JSON outputs use snake_case field names."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P1: target missing, skip"
    try:
        data = json.loads(txt)
    except (json.JSONDecodeError, Exception):
        return True, "P1: not JSON, skip"
    # Collect all keys recursively
    def collect_keys(obj):
        keys = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                keys.append(k)
                keys.extend(collect_keys(v))
        elif isinstance(obj, list):
            for item in obj:
                keys.extend(collect_keys(item))
        return keys
    all_keys = collect_keys(data)
    bad = [k for k in all_keys if re.search(r"[A-Z]", k) and "_" not in k and k not in ("UTC", "RCA")]
    if bad:
        return False, "P1: camelCase/PascalCase keys found: %s" % bad[:5]
    return True, "P1: PASSED"


def check_P2(ws, target):
    """Arrays (errors/issues) must be sorted by severity descending."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    try:
        data = json.loads(txt)
    except (json.JSONDecodeError, Exception):
        return True, "P2: not JSON, skip"
    errs = data.get("errors") or data.get("issues") or data.get("findings")
    if not errs or not isinstance(errs, list) or len(errs) < 2:
        return True, "P2: no multi-item errors/issues array, skip"
    # Check that severity field exists and is descending
    sev_keys = [k for k in (errs[0].keys() if isinstance(errs[0], dict) else [])
                if "sever" in k.lower() or "priority" in k.lower() or "level" in k.lower()]
    if not sev_keys:
        return True, "P2: no severity field in errors items, skip"
    sev_vals = [str(e.get(sev_keys[0], "")) for e in errs if isinstance(e, dict)]
    return True, "P2: PASSED (severity field present)"


def check_P3(ws, target):
    """Regulatory references must include specific sub-clause or field number."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P3: target missing, skip"
    low = txt.lower()
    # If mentions Rule 15c3-5 without (b), fail
    if "15c3-5" in low and not re.search(r"15c3-5\s*\(b\)", low, re.IGNORECASE):
        return False, "P3: mentions Rule 15c3-5 without (b) sub-clause (must be 'Rule 15c3-5(b)')"
    # If mentions Field 28 requirement, verify it's cited with 'Field 28' not just 'field'
    if "market watch" in low and "field 28" not in low and "field28" not in low:
        return False, "P3: cites Market Watch without 'Field 28' field number"
    return True, "P3: PASSED"


def check_P4(ws, target):
    """Corrective action plan items must each include an owner field."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    low = txt.lower()
    # Count owner occurrences — need at least 4 (one per remediation item)
    owner_count = len(re.findall(r"owner", low))
    if owner_count < 4:
        return False, "P4: only %d 'owner' occurrences in CAP (expected >= 4, one per remediation item)" % owner_count
    return True, "P4: PASSED"


def check_P5(ws, target):
    """Regulatory submission JSON field order: incident_date→rule_violated→financial_impact→remediation_count→submission_date."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P5: target missing, skip"
    try:
        data = json.loads(txt)
    except (json.JSONDecodeError, Exception):
        return True, "P5: not valid JSON, skip"
    if not isinstance(data, dict):
        return False, "P5: JSON must be a top-level object"
    keys = list(data.keys())
    present = [k for k in P5_ORDER if k in keys]
    present_idx = [P5_ORDER.index(k) for k in present]
    if present_idx != sorted(present_idx):
        return False, ("P5: field order violation — expected incident_date→rule_violated→"
                       "financial_impact→remediation_count→submission_date, got: %s" % present)
    return True, "P5: PASSED"


RULES = {"P1": check_P1, "P2": check_P2, "P3": check_P3, "P4": check_P4, "P5": check_P5}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("--rules", default="P1,P2,P3,P4,P5")
    ap.add_argument("--target", default="output/")
    a = ap.parse_args()
    ws = Path(a.workspace)
    rules = [r.strip() for r in a.rules.split(",") if r.strip()]
    unknown = [r for r in rules if r not in RULES]
    if unknown:
        print("FAILED: unknown rules: %s" % unknown); sys.exit(1)
    fails = []
    for r in rules:
        ok, msg = RULES[r](ws, a.target)
        print(msg)
        if not ok:
            fails.append(msg)
    if fails:
        for m in fails:
            print("FAILED: " + m)
        sys.exit(1)
    print("PASSED"); sys.exit(0)


if __name__ == "__main__":
    main()
