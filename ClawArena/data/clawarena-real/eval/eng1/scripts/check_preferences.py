#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""eng1 preference checker (P1 snake_case / P2 changelog RST style /
P3 test file module docstring / P4 advisory ## Workaround after ## Fix)."""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """Every JSON output file uses snake_case field names (no camelCase)."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P1: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P1: target is not valid JSON"
    if not isinstance(data, dict):
        return True, "P1: top-level not a dict, skip"
    for k in data.keys():
        if re.search(r"[a-z][A-Z]", str(k)):
            return False, "P1: camelCase field name %r violates snake_case requirement" % k
    return True, "P1: PASSED"


def check_P2(ws, target):
    """Changelog entries follow HISTORY.md RST style with **Security** or **Bugfixes** headers."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    if "**Security**" not in txt and "**Bugfixes**" not in txt:
        return False, "P2: changelog missing RST-style header '**Security**' or '**Bugfixes**'"
    return True, "P2: PASSED"


def check_P3(ws, target):
    """Python test files must begin with a module-level docstring."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P3: target missing, skip"
    lines = txt.splitlines()
    first_content = next((l.strip() for l in lines if l.strip() and not l.strip().startswith("#")), "")
    if not (first_content.startswith(3 * chr(34)) or first_content.startswith(3 * chr(39))):
        return False, "P3: test file must begin with a module-level docstring (triple-quoted string)"
    return True, "P3: PASSED"


def check_P4(ws, target):
    """Security advisory must have ## Workaround section placed AFTER ## Fix."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    if "## Workaround" not in txt:
        return False, "P4: security advisory missing '## Workaround' section"
    fix_pos = txt.find("## Fix")
    wa_pos = txt.find("## Workaround")
    if fix_pos == -1:
        return False, "P4: security advisory missing '## Fix' section"
    if wa_pos < fix_pos:
        return False, "P4: '## Workaround' appears before '## Fix' (must be after)"
    return True, "P4: PASSED"


RULES = {"P1": check_P1, "P2": check_P2, "P3": check_P3, "P4": check_P4}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("--rules", default="P1,P2,P3,P4")
    ap.add_argument("--target", default="analysis/")
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
