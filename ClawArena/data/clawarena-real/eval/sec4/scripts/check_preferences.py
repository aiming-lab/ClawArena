#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sec4 preference checker (P1-P5).

P1: All structured JSON outputs must be valid JSON with snake_case field names.
P2: Article references must use format "Art. X(Y)(Z)" (dot + parentheses).
P3: DSAR response/deadline files must carry case_id, request_date, response_deadline, status.
P4: Boolean conclusion fields must use uppercase string "TRUE"/"FALSE", not JSON true/false.
P5: overall_status must be one of COMPLIANT / PARTIALLY_COMPLIANT / NON_COMPLIANT.
"""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """Valid JSON with snake_case keys."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P1: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError as e:
        return False, "P1: target is not valid JSON: %s" % e
    # Walk keys and check snake_case (allow all-lowercase + underscores + digits)
    def _walk(obj):
        if isinstance(obj, dict):
            for k in obj.keys():
                if re.search(r"[A-Z]", k) and k not in ("DPO_contact", "DRAFT_NOTE"):
                    # Allow DPO_contact as it is part of a required field name in GDPR spec
                    if not k.startswith("DPO"):
                        return "P1: key %r is not snake_case" % k
            for v in obj.values():
                r = _walk(v)
                if r: return r
        elif isinstance(obj, list):
            for item in obj:
                r = _walk(item)
                if r: return r
        return None
    err = _walk(data)
    if err:
        return False, err
    return True, "P1: PASSED"


def check_P2(ws, target):
    """Article references must use format 'Art. X(Y)(Z)'."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    # Look for bad patterns: "Article X" or "#X" that reference GDPR articles
    bad = re.findall(r"Article\s+\d+", txt)
    if bad:
        return False, "P2: found non-standard article reference format: %s (use 'Art. X(Y)(Z)')" % bad[:3]
    # Check for hash-style references like "#33" when followed by a parenthetical
    bad2 = re.findall(r"#\d+\(\d+\)", txt)
    if bad2:
        return False, "P2: found hash-style article reference: %s (use 'Art. X(Y)(Z)')" % bad2[:3]
    return True, "P2: PASSED"


def check_P3(ws, target):
    """DSAR response/deadline files must carry four metadata fields."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P3: target missing, skip"
    low = txt.lower()
    missing = []
    for field in ("case_id", "request_date", "response_deadline", "status"):
        if field not in low:
            missing.append(field)
    if missing:
        return False, "P3: DSAR file missing metadata fields: %s" % missing
    return True, "P3: PASSED"


def check_P4(ws, target):
    """Boolean conclusion fields must be uppercase string TRUE/FALSE."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P4: target is not valid JSON"
    # Check specific boolean-conclusion fields that should be strings
    BOOL_KEYS = {
        "mandatory", "dpo_mandatory", "article_30_compliant",
        "article_33_compliant", "article_37_compliant",
    }
    def _walk(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in BOOL_KEYS and isinstance(v, bool):
                    return "P4: field %r uses JSON bool %r (must be string \"TRUE\" or \"FALSE\")" % (k, v)
            for v in obj.values():
                r = _walk(v)
                if r: return r
        elif isinstance(obj, list):
            for item in obj:
                r = _walk(item)
                if r: return r
        return None
    err = _walk(data)
    if err:
        return False, err
    return True, "P4: PASSED"


def check_P5(ws, target):
    """overall_status must be one of three valid enum values."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P5: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P5: target is not valid JSON"
    if not isinstance(data, dict):
        return True, "P5: not a JSON object, skip"
    if "overall_status" not in data:
        return True, "P5: no overall_status field, skip"
    VALID = {"COMPLIANT", "PARTIALLY_COMPLIANT", "NON_COMPLIANT"}
    os_ = data.get("overall_status")
    if os_ not in VALID:
        return False, "P5: overall_status == %r (must be COMPLIANT / PARTIALLY_COMPLIANT / NON_COMPLIANT)" % os_
    return True, "P5: PASSED"


RULES = {"P1": check_P1, "P2": check_P2, "P3": check_P3, "P4": check_P4, "P5": check_P5}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("--rules", default="P1,P2,P3,P4,P5")
    ap.add_argument("--target", default="audit/")
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
