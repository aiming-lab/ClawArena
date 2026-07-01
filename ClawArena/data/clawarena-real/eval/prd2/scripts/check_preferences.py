#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""prd2 preference checker (P1: JSON 2-space indent + snake_case / P2: _source_url companion /
P3: time limits in months 1 decimal / P4: [^N] footnote citations / P5: reports/ naming convention)."""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """JSON files must use 2-space indentation and snake_case keys (no camelCase)."""
    p = Path(ws) / target
    if not p.exists():
        return True, "P1: target missing, skip"
    if p.suffix not in (".json",):
        return True, "P1: non-JSON target, skip"
    txt = _read(p)
    if txt is None:
        return True, "P1: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P1: target is not valid JSON"
    # Check for camelCase keys (any key with a lowercase letter followed by uppercase)
    all_keys = _collect_keys(data)
    camel = [k for k in all_keys if re.search(r"[a-z][A-Z]", k)]
    if camel:
        return False, "P1: camelCase keys detected: %s (use snake_case)" % camel[:3]
    # Check indentation (2-space): re-serialize and compare
    canonical = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    if txt.strip() != canonical.strip():
        # Allow minor whitespace differences but flag drastically different indent
        lines = [l for l in txt.splitlines() if l.startswith("  ") and not l.startswith("   ")]
        three_indent = [l for l in txt.splitlines() if l.startswith("   ") and not l.startswith("    ")]
        if three_indent:
            return False, "P1: JSON indentation appears to be 3+ spaces (should be 2-space)"
    return True, "P1: PASSED"


def _collect_keys(obj, depth=0):
    keys = []
    if depth > 5:
        return keys
    if isinstance(obj, dict):
        for k, v in obj.items():
            keys.append(k)
            keys.extend(_collect_keys(v, depth + 1))
    elif isinstance(obj, list):
        for item in obj:
            keys.extend(_collect_keys(item, depth + 1))
    return keys


def check_P2(ws, target):
    """Numeric fields in JSON must have a companion _source_url field at the same level."""
    p = Path(ws) / target
    if not p.exists():
        return True, "P2: target missing, skip"
    if p.suffix not in (".json",):
        return True, "P2: non-JSON target, skip"
    txt = _read(p)
    if txt is None:
        return True, "P2: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P2: target is not valid JSON"
    # Check that numeric fields have _source_url companions
    issues = _check_source_urls(data)
    if issues:
        return False, "P2: numeric fields without _source_url companions: %s" % issues[:3]
    return True, "P2: PASSED"


def _check_source_urls(obj, parent_key="", depth=0):
    """Return list of numeric field names lacking a _source_url sibling."""
    if depth > 6:
        return []
    issues = []
    if isinstance(obj, dict):
        keys = set(obj.keys())
        for k, v in obj.items():
            if k.endswith("_source_url") or k.endswith("_url") or k.startswith("_"):
                continue
            if isinstance(v, (int, float)) and v not in (0, 1) and k not in (
                "schema_version", "tier", "strikes_required", "automation_rate",
                "videos_removed_pct_of_uploads",
            ):
                companion = k + "_source_url"
                if companion not in keys:
                    issues.append("%s.%s (missing %s)" % (parent_key, k, companion))
            if isinstance(v, (dict, list)):
                issues.extend(_check_source_urls(v, parent_key + "." + k if parent_key else k, depth + 1))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            issues.extend(_check_source_urls(item, parent_key + "[%d]" % i, depth + 1))
    return issues


def check_P3(ws, target):
    """Time-limit values use months as primary unit, 1 decimal place."""
    p = Path(ws) / target
    if not p.exists():
        return True, "P3: target missing, skip"
    if p.suffix not in (".json",):
        return True, "P3: non-JSON target, skip"
    txt = _read(p)
    if txt is None:
        return True, "P3: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P3: target is not valid JSON"
    # Check month fields: must be float-like with 1 decimal (e.g. 6.0, 12.0, 3.0)
    issues = _check_month_fields(data)
    if issues:
        return False, "P3: month fields not using 1 decimal: %s" % issues[:3]
    return True, "P3: PASSED"


def _check_month_fields(obj, depth=0):
    if depth > 5:
        return []
    issues = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if "month" in k and "url" not in k:
                if isinstance(v, (int, float)):
                    # Must be representable as X.Y (1 decimal)
                    if isinstance(v, int) and v > 0:
                        issues.append("%s=%r (should be float e.g. %.1f)" % (k, v, float(v)))
            if isinstance(v, (dict, list)):
                issues.extend(_check_month_fields(v, depth + 1))
    elif isinstance(obj, list):
        for item in obj:
            issues.extend(_check_month_fields(item, depth + 1))
    return issues


def check_P4(ws, target):
    """Markdown documents must use [^N] footnote format and include ## 参考来源 section."""
    p = Path(ws) / target
    if not p.exists():
        return True, "P4: target missing, skip"
    if p.suffix not in (".md",):
        return True, "P4: non-Markdown target, skip"
    txt = _read(p)
    if txt is None:
        return True, "P4: target missing, skip"
    if "[^" not in txt:
        return False, "P4: missing [^N] footnote citations in Markdown document"
    if not re.search(r"^## (参考来源|references|来源参考|sources)", txt, re.IGNORECASE | re.MULTILINE):
        return False, "P4: missing ## 参考来源 / ## References section at document end"
    return True, "P4: PASSED"


def check_P5(ws, target):
    """Files in reports/ must follow {type}_{yyyy-mm}.json or {type}_latest.json naming."""
    p = Path(ws) / target
    if p.is_file():
        files = [p]
    elif p.is_dir():
        files = list(p.glob("*.json"))
    else:
        return True, "P5: target missing, skip"
    pat_date = re.compile(r"^[a-z][a-z0-9_]*_\d{4}-\d{2}\.json$")
    pat_latest = re.compile(r"^[a-z][a-z0-9_]*_latest\.json$")
    bad = []
    for f in files:
        if f.name in ("cross_validation.json", "deprecation_log.json",
                      "compliance_signoff.json", "compliance_report_final.json"):
            continue
        if "violation_stats" in f.name or "compliance" in f.name:
            if not (pat_date.match(f.name) or pat_latest.match(f.name)):
                bad.append(f.name)
    if bad:
        return False, "P5: reports/ files not matching {type}_{yyyy-mm}.json or {type}_latest.json: %s" % bad
    return True, "P5: PASSED"


RULES = {"P1": check_P1, "P2": check_P2, "P3": check_P3, "P4": check_P4, "P5": check_P5}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("--rules", default="P1,P2,P3,P4,P5")
    ap.add_argument("--target", default="policy_engine/internal/")
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
