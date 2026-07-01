#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""eng2 preference checker (P1 schema_version / P2 script header / P3 sample naming /
P4 quality-report field order / P5 verbatim column names)."""
import sys, re, json, argparse
from pathlib import Path

ORDER = ["field_name", "null_count", "null_pct", "invalid_count", "invalid_pct", "notes"]


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """Every output JSON file carries a top-level schema_version == "1.0"."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P1: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P1: target is not valid JSON"
    if not isinstance(data, dict):
        return False, "P1: top-level must be a JSON object carrying schema_version"
    if str(data.get("schema_version")) != "1.0":
        return False, "P1: missing top-level schema_version == \"1.0\" (got %r)" % data.get("schema_version")
    return True, "P1: PASSED"


def check_P2(ws, target):
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    head = "\n".join(txt.splitlines()[:3])
    if "#!/usr/bin/env python3" not in head:
        return False, "P2: missing '#!/usr/bin/env python3' shebang on line 1-2"
    if "# -*- coding: utf-8 -*-" not in head:
        return False, "P2: missing '# -*- coding: utf-8 -*-' encoding header"
    return True, "P2: PASSED"


def check_P3(ws, target):
    """Sample files named {type}_{year}{month:02d}_sample.csv."""
    tp = ws / target
    files = [tp] if tp.is_file() else list(tp.glob("*_sample.csv")) if tp.exists() else []
    if not files:
        return True, "P3: no sample files, skip"
    pat = re.compile(r"^[a-z]+_\d{6}_sample\.(csv|parquet)$")
    bad = [f.name for f in files if not pat.match(f.name)]
    if bad:
        return False, "P3: sample files not matching {type}_{YYYYMM}_sample: %s" % bad
    return True, "P3: PASSED"


def check_P4(ws, target):
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P4: target is not valid JSON"
    fields = data.get("fields")
    entries = fields if isinstance(fields, list) else (list(fields.values()) if isinstance(fields, dict) else [])
    for e in entries:
        if not isinstance(e, dict):
            continue
        idx = [ORDER.index(k) for k in e.keys() if k in ORDER]
        if idx != sorted(idx):
            return False, "P4: field-object key order violates field_name/null_count/null_pct/invalid_count/invalid_pct/notes"
    return True, "P4: PASSED"


def check_P5(ws, target):
    txt = _read(ws / target)
    if txt is None:
        return True, "P5: target missing, skip"
    if re.search(r"(?<!tpep_)pickup_datetime", txt):
        return False, "P5: uses abbreviated 'pickup_datetime' instead of verbatim 'tpep_pickup_datetime'"
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
