#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sci3 preference checker (P1-P5).

P1: all monetary JSON fields are integers (no decimal, no thousand separator)
P2: Markdown reports use ### (level-3) headings, not ## (level-2)
P3: CSV files UTF-8, date fields YYYY-MM-DD, ratio fields two decimal places
P4: JSON field names snake_case; array fields plural
P5: recommendation/action fields plain text, no nested JSON, <= 150 chars
"""
import sys, re, json, argparse, csv
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """Monetary fields in JSON must be integers (no float/string with decimal)."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P1: target missing, skip"
    if not target.endswith(".json"):
        return True, "P1: not a JSON file, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P1: target is not valid JSON"
    # Find any key that looks currency-related
    money_keys = re.compile(r"(fee|usd|penalty|total|amount|fine)", re.I)
    fails = []
    def _check_val(key, val, path):
        if money_keys.search(key):
            if isinstance(val, float):
                fails.append("P1: field %s is a float (%.6g); monetary fields must be integers" % (path, val))
            elif isinstance(val, str) and re.match(r"[\$]", val.strip()):
                fails.append("P1: field %s contains currency symbol %r; use plain integer" % (path, val[:20]))
    def _walk(obj, prefix=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                _check_val(k, v, prefix + k)
                _walk(v, prefix + k + ".")
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                _walk(v, prefix + "[%d]." % i)
    _walk(data)
    if fails:
        return False, "P1: " + "; ".join(fails[:2])
    return True, "P1: PASSED"


def check_P2(ws, target):
    """Markdown reports must use ### (not ##) for case/shift headings."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    if not target.endswith(".md"):
        return True, "P2: not a Markdown file, skip"
    # Look for ## headings that are NOT ### (i.e., exactly 2 hashes at line start)
    bad = re.findall(r"^## (?!#)", txt, re.MULTILINE)
    if bad:
        return False, "P2: found %d ## (level-2) headings; all case/shift sections must use ### (level-3)" % len(bad)
    h3 = re.findall(r"^### ", txt, re.MULTILINE)
    if not h3:
        return False, "P2: no ### (level-3) headings found in Markdown file"
    return True, "P2: PASSED"


def check_P3(ws, target):
    """CSV files: UTF-8, date YYYY-MM-DD, ratio two decimal places."""
    p = ws / target
    if not p.exists():
        return True, "P3: target missing, skip"
    if not target.endswith(".csv"):
        return True, "P3: not a CSV file, skip"
    try:
        with p.open(encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
    except UnicodeDecodeError:
        return False, "P3: CSV is not UTF-8 encoded"
    except Exception as e:
        return False, "P3: CSV read error: %s" % e
    if not rows:
        return True, "P3: empty CSV, skip"
    # Date fields: check YYYY-MM-DD
    date_re = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    date_fields = [k for k in rows[0].keys() if "date" in k.lower()]
    for r in rows[:50]:  # sample first 50
        for df in date_fields:
            v = str(r.get(df, "")).strip()
            if v and not date_re.match(v):
                return False, "P3: date field %r has value %r (expected YYYY-MM-DD)" % (df, v)
    # Ratio fields: check two decimal places
    ratio_fields = [k for k in rows[0].keys() if "ratio" in k.lower()]
    ratio_re = re.compile(r"^-?\d+\.\d{2}$")
    for r in rows[:50]:
        for rf in ratio_fields:
            v = str(r.get(rf, "")).strip()
            if v and v not in ("", "0"):
                if not ratio_re.match(v):
                    return False, "P3: ratio field %r has value %r (expected two decimal places like 2.50)" % (rf, v)
    return True, "P3: PASSED"


def check_P4(ws, target):
    """JSON field names must be snake_case; array fields plural."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    if not target.endswith(".json"):
        return True, "P4: not a JSON file, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P4: target is not valid JSON"
    camel_re = re.compile(r"[a-z][A-Z]")  # camelCase detector
    fails = []
    def _check_keys(obj, prefix=""):
        if isinstance(obj, dict):
            for k in obj.keys():
                if camel_re.search(k):
                    fails.append("key %r contains camelCase (use snake_case)" % k)
                # array fields should be plural — light check: if value is a list, key should end with s
                if isinstance(obj[k], list) and len(obj[k]) > 0:
                    if k.endswith("_list") or k == "list":
                        fails.append("array field %r should use plural noun, not *_list suffix" % k)
                _check_keys(obj[k], prefix + k + ".")
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                _check_keys(v, prefix + "[%d]." % i)
    _check_keys(data)
    if fails:
        return False, "P4: " + "; ".join(fails[:2])
    return True, "P4: PASSED"


def check_P5(ws, target):
    """recommendation/action fields: plain text, no nested JSON, <= 150 chars."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P5: target missing, skip"
    if not target.endswith(".json"):
        return True, "P5: not a JSON file, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P5: target is not valid JSON"
    rec_keys = re.compile(r"(recommendation|action_required|action)", re.I)
    fails = []
    def _check_rec(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if rec_keys.match(k):
                    if isinstance(v, dict) or isinstance(v, list):
                        fails.append("field %r must be plain text string, not nested JSON" % k)
                    elif isinstance(v, str):
                        if len(v) > 150:
                            fails.append("field %r exceeds 150 chars (got %d)" % (k, len(v)))
                else:
                    _check_rec(v)
        elif isinstance(obj, list):
            for v in obj:
                _check_rec(v)
    _check_rec(data)
    if fails:
        return False, "P5: " + "; ".join(fails[:2])
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
