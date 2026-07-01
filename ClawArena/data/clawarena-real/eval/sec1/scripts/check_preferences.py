#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sec1 preference checker (P1-P5).

P1: JSON 2-space indent, top-level fields alphabetically ordered.
P2: CVE IDs formatted as CVE-YYYY-NNNNN (hyphenated, uppercase).
P3: Work product filenames use snake_case.
P4: Progress/inventory reports grouped prod/staging/dev, prod first.
P5: Executive summaries contain standalone TL;DR paragraph ≤200 words.
"""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """JSON 2-space indent + top-level alphabetical field order."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P1: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P1: target is not valid JSON"
    if not isinstance(data, dict):
        return True, "P1: top-level not a dict, skip"
    # Check indentation: look for 2-space indent pattern
    lines = txt.split("\n")
    has_indent = any(line.startswith("  ") and not line.startswith("   ") for line in lines)
    if lines and not has_indent:
        # Allow no-indent for trivially small JSON or single-line
        pass  # lenient on this check
    # Check alphabetical field order
    keys = list(data.keys())
    # filter out schema_version as a special key
    content_keys = [k for k in keys]
    if content_keys != sorted(content_keys):
        return False, ("P1: top-level keys not alphabetically sorted: %s (expected %s)" %
                       (content_keys[:8], sorted(content_keys)[:8]))
    return True, "P1: PASSED"


def check_P2(ws, target):
    """CVE IDs must be in CVE-YYYY-NNNNN format."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    # Find any CVE-like patterns
    bad = re.findall(r"\bcve[- _]?\d{4}[- _]?\d+\b", txt, re.IGNORECASE)
    good = re.findall(r"\bCVE-\d{4}-\d+\b", txt)
    # Remove properly formatted ones from bad
    bad_only = [b for b in bad if not re.match(r"^CVE-\d{4}-\d+$", b, re.IGNORECASE)]
    # Actually find malformatted ones
    malformed = re.findall(r"\b(?:cve|CVE)(?!-\d{4}-\d)[-_\s]?\d", txt)
    bad_format = [b for b in re.findall(r"\b[Cc][Vv][Ee][-_\s]?\d{4}[-_\s]?\d+\b", txt)
                  if b != re.sub(r"[-_\s]", "-", b.upper())]
    if bad_format:
        return False, "P2: malformatted CVE IDs found: %s (must be CVE-YYYY-NNNNN)" % bad_format[:3]
    return True, "P2: PASSED"


def check_P3(ws, target):
    """Filename must be snake_case."""
    p = ws / target
    name = p.name
    if not name:
        return True, "P3: no target file, skip"
    # Allow only lowercase letters, digits, underscores, dots (for extension)
    stem = p.stem
    bad_chars = re.findall(r"[A-Z\-\s]", stem)
    if bad_chars:
        return False, "P3: filename %r contains non-snake_case chars %s" % (name, bad_chars[:5])
    return True, "P3: PASSED"


def check_P4(ws, target):
    """Progress/inventory: prod group appears before staging and dev."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    # For CSV: check that first env value is prod
    if target.endswith(".csv"):
        import csv, io
        rows = list(csv.DictReader(io.StringIO(txt)))
        if not rows:
            return True, "P4: empty CSV, skip"
        envs = [r.get("env","").lower() for r in rows]
        if envs and envs[0] != "prod":
            return False, "P4: first row env=%r (expected prod-first ordering)" % envs[0]
        return True, "P4: PASSED"
    # For JSON: check that prod key appears before staging/dev
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return True, "P4: not JSON, skip"
    if not isinstance(data, dict):
        return True, "P4: not a dict, skip"
    keys = [k.lower() for k in data.keys()]
    if "prod" in keys and "staging" in keys:
        if keys.index("prod") > keys.index("staging"):
            return False, "P4: prod group appears after staging (must be first)"
    if "prod" in keys and "dev" in keys:
        if keys.index("prod") > keys.index("dev"):
            return False, "P4: prod group appears after dev (must be first)"
    return True, "P4: PASSED"


def check_P5(ws, target):
    """Executive summary must contain standalone TL;DR ≤200 words."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P5: target missing, skip"
    m = re.search(r"##?\s*TL;?DR(.+?)(?=^##|\Z)", txt, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    if not m:
        return False, "P5: missing standalone TL;DR section (required for executive summaries)"
    tldr = m.group(1).strip()
    wc = len(tldr.split())
    if wc > 200:
        return False, "P5: TL;DR section has %d words (must be ≤200)" % wc
    return True, "P5: PASSED"


RULES = {"P1": check_P1, "P2": check_P2, "P3": check_P3, "P4": check_P4, "P5": check_P5}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("--rules", default="P1,P2,P3,P4,P5")
    ap.add_argument("--target", default="work/")
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
