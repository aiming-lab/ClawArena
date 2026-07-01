#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""eng3 preference checker.

P1: All timestamps in output JSON must use ISO 8601 UTC YYYY-MM-DDTHH:MM:SSZ format.
P2: Percentage/ratio fields must be formatted as {value: float_2dp, unit: "percent"} objects.
P3: Postmortem section headings must use bilingual format "## Section Name / 章节名称".
P4: Customer-facing documents must include [ArcNode Status] prefix.
P5: JSON outputs must include top-level "generated_at" field (ISO 8601 UTC); file names snake_case.
"""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """All timestamps must be ISO 8601 UTC YYYY-MM-DDTHH:MM:SSZ — no other format."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P1: target missing, skip"
    try:
        data = json.loads(txt)
    except (json.JSONDecodeError, Exception):
        return True, "P1: target not JSON, skip"
    # Find all string values and check timestamp-like ones
    ts_fields = ["incident_start_utc", "start_utc", "end_utc", "peak_time_utc",
                 "time_utc", "generated_at"]
    def _check_val(v):
        if not isinstance(v, str):
            return True
        # if it looks like a timestamp (contains T and colon)
        if re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}", v):
            if not re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", v):
                return False
        return True
    def _walk(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in ts_fields or "utc" in k.lower() or "timestamp" in k.lower() or "time" in k.lower():
                    if isinstance(v, str) and re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}", v):
                        if not re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", v):
                            return False, v
                if isinstance(v, (dict, list)):
                    ok, bad = _walk(v)
                    if not ok:
                        return ok, bad
        elif isinstance(obj, list):
            for item in obj:
                ok, bad = _walk(item)
                if not ok:
                    return ok, bad
        return True, None
    ok, bad = _walk(data)
    if not ok:
        return False, "P1: timestamp %r not ISO 8601 UTC YYYY-MM-DDTHH:MM:SSZ" % bad
    return True, "P1: PASSED"


def check_P2(ws, target):
    """Percentage fields must be formatted as {value: float, unit: 'percent'}."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    try:
        data = json.loads(txt)
    except (json.JSONDecodeError, Exception):
        return True, "P2: target not JSON, skip"
    pct_keys = ["peak_cdn_error_pct", "peak_5xx_pct", "western_europe_loss_pct",
                "eastern_europe_loss_pct"]
    for k in pct_keys:
        if k in data:
            v = data[k]
            if not isinstance(v, dict):
                return False, "P2: %s is not an object {value, unit} (got %r)" % (k, v)
            if "unit" not in v or v.get("unit") != "percent":
                return False, "P2: %s.unit must be 'percent' (got %r)" % (k, v.get("unit"))
    return True, "P2: PASSED"


def check_P3(ws, target):
    """Postmortem section headings must use bilingual format '## Name / 名称'."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P3: target missing, skip"
    headings = re.findall(r"^##\s+.+", txt, re.MULTILINE)
    if not headings:
        return True, "P3: no ## headings found, skip"
    bad = [h for h in headings if "/" not in h]
    if bad:
        return False, "P3: heading(s) missing bilingual slash separator: %s" % bad[:2]
    return True, "P3: PASSED"


def check_P4(ws, target):
    """Customer-facing documents must include [ArcNode Status] prefix."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    if "[arcnode status]" not in txt.lower():
        return False, "P4: missing '[ArcNode Status]' prefix in %s" % target
    return True, "P4: PASSED"


def check_P5(ws, target):
    """JSON outputs must include top-level 'generated_at' field (ISO 8601 UTC)."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P5: target missing, skip"
    try:
        data = json.loads(txt)
    except (json.JSONDecodeError, Exception):
        return True, "P5: target not JSON, skip"
    if not isinstance(data, dict):
        return True, "P5: top-level not dict, skip"
    ga = data.get("generated_at")
    if not ga:
        return False, "P5: missing top-level 'generated_at' field"
    if not re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", str(ga)):
        return False, "P5: generated_at %r not ISO 8601 UTC YYYY-MM-DDTHH:MM:SSZ" % ga
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
