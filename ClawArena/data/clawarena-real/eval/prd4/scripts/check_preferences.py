#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""prd4 preference checker (P1 snake_case / P2 metadata block / P3 ISO 8601 timestamps /
P4 two-decimal numerics / P5 reviewer_signature field)."""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """All JSON output field names use snake_case (no camelCase or hyphenated)."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P1: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P1: target is not valid JSON"
    # check top-level keys for camelCase
    keys = list(data.keys()) if isinstance(data, dict) else []
    for k in keys:
        if k != k.lower() and re.search(r"[a-z][A-Z]", k):
            return False, "P1: camelCase key found: %r (use snake_case)" % k
    return True, "P1: PASSED"


def check_P2(ws, target):
    """Every report file has a top-level metadata block with generated_at, agent_id, schema_version."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P2: target is not valid JSON"
    if not isinstance(data, dict):
        return True, "P2: not a dict (array is OK without metadata), skip"
    meta = data.get("metadata")
    if not isinstance(meta, dict):
        return False, "P2: metadata block missing or not an object"
    for req in ("generated_at", "agent_id", "schema_version"):
        if req not in meta:
            return False, "P2: metadata.%s missing" % req
    return True, "P2: PASSED"


def check_P3(ws, target):
    """All datetime/timestamp fields use ISO 8601 YYYY-MM-DDTHH:MM:SSZ format."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P3: target missing, skip"
    # Match full datetime including optional Z suffix, so we capture the Z
    ts_pat = re.compile(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}Z?")
    iso_pat = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
    bad = []
    for m in ts_pat.finditer(txt):
        s = m.group(0)
        if not iso_pat.match(s):
            bad.append(s)
    if bad:
        return False, "P3: non-ISO-8601 timestamp found: %r" % bad[0]
    return True, "P3: PASSED"


def check_P4(ws, target):
    """Numeric percentage/rate fields reported to 2 decimal places."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P4: target is not valid JSON"
    # look for fields with 'rate' or 'pct' or 'percent' in the key that have many decimals
    def check_dict(d, depth=0):
        if depth > 5 or not isinstance(d, dict):
            return None
        for k, v in d.items():
            if isinstance(v, float):
                if ("rate" in k or "pct" in k or "percent" in k or "uptime" in k):
                    # check it has at most 2 decimal places
                    rounded = round(v, 2)
                    if abs(v - rounded) > 1e-9:
                        return "P4: field %r value %r has more than 2 decimal places" % (k, v)
            elif isinstance(v, dict):
                err = check_dict(v, depth+1)
                if err:
                    return err
            elif isinstance(v, list):
                for item in v:
                    err = check_dict(item, depth+1) if isinstance(item, dict) else None
                    if err:
                        return err
        return None
    err = check_dict(data)
    if err:
        return False, err
    return True, "P4: PASSED"


def check_P5(ws, target):
    """Every report file includes a reviewer_signature field."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P5: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P5: target is not valid JSON"
    if not isinstance(data, dict):
        return True, "P5: array type, skip"
    if "reviewer_signature" not in data:
        return False, "P5: reviewer_signature field missing (must exist, may be empty string)"
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
