#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sec2 preference checker (P1 extracted_at / P2 operator / P3 file naming /
P4 Slack three-section / P5 Rationale section)."""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """Every JSON deliverable must include a top-level extracted_at field (ISO-8601 UTC)."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P1: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P1: target is not valid JSON"
    if not isinstance(data, dict):
        return False, "P1: top-level must be a JSON object"
    ea = data.get("extracted_at")
    if not ea:
        return False, "P1: missing top-level extracted_at field (must be ISO-8601 UTC timestamp)"
    if not re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", str(ea)):
        return False, "P1: extracted_at %r does not look like ISO-8601 datetime" % str(ea)
    return True, "P1: PASSED"


def check_P2(ws, target):
    """Every JSON deliverable must include a top-level operator field."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P2: target is not valid JSON"
    if not isinstance(data, dict):
        return False, "P2: top-level must be a JSON object"
    op = data.get("operator")
    if not op:
        return False, "P2: missing top-level operator field (must identify executing person/system)"
    return True, "P2: PASSED"


def check_P3(ws, target):
    """Deliverable file naming: q{NN}_{descriptor}.{ext}, descriptor lowercase+underscore."""
    tp = ws / target
    if tp.is_file():
        files = [tp]
    elif tp.is_dir():
        files = list(tp.glob("q[0-9][0-9]_*.json")) + list(tp.glob("q[0-9][0-9]_*.md")) + list(tp.glob("q[0-9][0-9]_*.txt"))
    else:
        return True, "P3: target not found, skip"
    if not files:
        return True, "P3: no q-prefixed output files, skip"
    pat = re.compile(r"^q\d{2}_[a-z0-9_]+\.(json|md|txt)$")
    bad = [f.name for f in files if not pat.match(f.name)]
    if bad:
        return False, "P3: file names not matching q{NN}_{lowercase_underscore}.{ext}: %s" % bad
    return True, "P3: PASSED"


def check_P4(ws, target):
    """Slack summaries must use three H2 sections: ## Impact / ## Actions Taken / ## Next Steps."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    missing = []
    for heading in ("## Impact", "## Actions Taken", "## Next Steps"):
        if heading not in txt and heading.lower() not in txt.lower():
            missing.append(heading)
    if missing:
        return False, "P4: Slack summary missing H2 sections: %s" % missing
    return True, "P4: PASSED"


def check_P5(ws, target):
    """Technical documents must include a standalone ## Rationale section."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P5: target missing, skip"
    if "## Rationale" not in txt and "## rationale" not in txt.lower():
        return False, "P5: document missing '## Rationale' section (required by CTO Zhang — Feishu group)"
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
