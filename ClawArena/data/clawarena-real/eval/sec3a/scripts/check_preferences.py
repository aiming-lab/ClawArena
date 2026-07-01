#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sec3a preference checker:
P1 — all JSON output uses snake_case field names (no camelCase/PascalCase)
P2 — all JSON deliverables carry top-level schema_version == "1.0"
P3 — regulatory citations include specific sub-paragraph (e.g., 'Rule 15c3-5(b)')
P4 — CAP items each include an owner field
P5 — regulatory submission JSON field order: incident_date → rule_violated → financial_impact → remediation_count → submission_date
"""
import sys, re, json, argparse
from pathlib import Path

P5_ORDER = ["incident_date", "rule_violated", "financial_impact", "remediation_count", "submission_date"]


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """All JSON outputs must carry top-level schema_version == '1.0'."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P1: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P1: target is not valid JSON"
    if not isinstance(data, dict):
        return True, "P1: top-level is not object, skip"
    if str(data.get("schema_version")) != "1.0":
        return False, "P1: missing top-level schema_version == \"1.0\" (got %r)" % data.get("schema_version")
    return True, "P1: PASSED"


def check_P2(ws, target):
    """All JSON field names must be snake_case (no camelCase or PascalCase)."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    if not target.endswith(".json"):
        return True, "P2: not a JSON file, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P2: target is not valid JSON"
    # Flatten all keys recursively
    def all_keys(obj):
        if isinstance(obj, dict):
            for k in obj.keys():
                yield k
                yield from all_keys(obj[k])
        elif isinstance(obj, list):
            for item in obj:
                yield from all_keys(item)
    bad = []
    for k in all_keys(data):
        if k in ("schema_version",):
            continue
        # camelCase: starts with lowercase, has uppercase letter inside
        if re.match(r"[a-z][a-z0-9]*[A-Z]", k):
            bad.append(k)
        # PascalCase: starts with uppercase
        if re.match(r"[A-Z]", k):
            bad.append(k)
    if bad:
        return False, "P2: non-snake_case field names found: %s" % bad[:5]
    return True, "P2: PASSED"


def check_P3(ws, target):
    """Regulatory citations must include sub-paragraph (e.g., '15c3-5(b)' not '15c3-5' alone)."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P3: target missing, skip"
    # If the file mentions 15c3-5 at all, it must include the sub-paragraph (b)
    if re.search(r"15c3-5", txt):
        if not re.search(r"15c3-5\([a-z]\)", txt) and not re.search(r"15c3-5\(b\)", txt):
            return False, "P3: found '15c3-5' without sub-paragraph; must cite '15c3-5(b)'"
    return True, "P3: PASSED"


def check_P4(ws, target):
    """CAP items each must include an 'owner' field."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    # For markdown CAP files: at least 4 'owner' mentions
    low = txt.lower()
    count = len(re.findall(r"\bowner\b", low))
    if count < 4:
        return False, "P4: fewer than 4 'owner' mentions in CAP (found %d); each item must have an owner" % count
    return True, "P4: PASSED"


def check_P5(ws, target):
    """Regulatory submission JSON must have top-level fields in fixed order."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P5: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P5: target is not valid JSON"
    if not isinstance(data, dict):
        return True, "P5: not a JSON object, skip"
    present = [k for k in data.keys() if k in set(P5_ORDER)]
    idx = [P5_ORDER.index(k) for k in present]
    if idx != sorted(idx):
        return False, "P5: field order wrong: required incident_date→rule_violated→financial_impact→remediation_count→submission_date (got %s)" % present
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
