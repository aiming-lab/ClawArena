#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sci2 preference checker (P1-P5).

P1: 5-Why analyses must use Markdown table format (| Why # | Question | Finding |)
P2: Fishbone JSON must use exactly Six-M categories as keys under 'categories'
P3: MDR documents must contain Section A through Section G headings
P4: Executive Summary must contain YAML frontmatter with date/author/recall_cases/classification
P5: Final report files must match naming pattern final_rca_report_YYYYMMDD.md
"""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """5-Why must use Markdown table format."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P1: target missing, skip"
    # Check for Markdown table pattern: | Why | or | Why # |
    if not re.search(r"\|\s*Why", txt, re.IGNORECASE):
        return False, "P1: 5-Why analysis must use Markdown table format (| Why # | Question | Finding |) — prose format not accepted"
    return True, "P1: PASSED"


def check_P2(ws, target):
    """Fishbone JSON must use Six-M categories."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P2: target is not valid JSON"
    cats = data.get("categories")
    if not isinstance(cats, dict):
        return False, "P2: 'categories' must be a JSON object with Six-M keys"
    cat_keys_lower = {str(k).strip().lower() for k in cats.keys()}
    six_m = {"man", "machine", "material", "method", "environment", "measurement"}
    missing = six_m - cat_keys_lower
    if missing:
        return False, "P2: fishbone categories missing Six-M keys: %s" % sorted(missing)
    return True, "P2: PASSED"


def check_P3(ws, target):
    """MDR document must follow Form 3500A Section A-G structure."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P3: target missing, skip"
    low = txt.lower()
    # Must have section headings A through G (at least 4 of them)
    sections_found = sum(
        1 for letter in "abcdefg"
        if re.search(r"section\s+" + letter + r"\b", low)
    )
    if sections_found < 4:
        return False, "P3: MDR document must follow Form 3500A structure with Section A through Section G headings (found only %d section labels)" % sections_found
    return True, "P3: PASSED"


def check_P4(ws, target):
    """Executive Summary must have YAML frontmatter."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    # YAML frontmatter: --- at start, then --- closing
    if not txt.startswith("---"):
        return False, "P4: Executive Summary must start with YAML frontmatter (---)"
    fm_match = re.match(r"---\s*\n(.*?)\n---", txt, re.DOTALL)
    if not fm_match:
        return False, "P4: YAML frontmatter not properly closed with ---"
    fm_body = fm_match.group(1).lower()
    required = ["date", "author", "recall_cases", "classification"]
    missing = [f for f in required if f not in fm_body]
    if missing:
        return False, "P4: YAML frontmatter missing fields: %s" % missing
    return True, "P4: PASSED"


def check_P5(ws, target):
    """Final report file naming: final_rca_report_YYYYMMDD.md"""
    # target should be the directory or a specific file
    tp = ws / target
    if tp.is_file():
        files = [tp]
    elif tp.is_dir():
        files = list(tp.glob("final_rca_report_*.md"))
    else:
        return True, "P5: target not found, skip"
    if not files:
        return False, "P5: no file matching final_rca_report_YYYYMMDD.md found"
    pattern = re.compile(r"^final_rca_report_\d{8}\.md$")
    bad = [f.name for f in files if not pattern.match(f.name)]
    if bad:
        return False, "P5: file names not matching final_rca_report_YYYYMMDD.md: %s" % bad
    return True, "P5: PASSED"


RULES = {"P1": check_P1, "P2": check_P2, "P3": check_P3, "P4": check_P4, "P5": check_P5}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("--rules", default="P1,P2,P3,P4,P5")
    ap.add_argument("--target", default="rca_outputs/")
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
