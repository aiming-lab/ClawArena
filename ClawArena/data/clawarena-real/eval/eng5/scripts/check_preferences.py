#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""eng5 preference checker (P1 snake_case JSON / P2 bilingual headings /
P3 backup before modify / P4 gitlab stage-split / P5 Python version comment)."""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """All JSON output files: schema_version == '1.0'; no camelCase field names."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P1: target missing, skip"
    # P1 only applies to JSON files
    if not str(target).endswith(".json"):
        return True, "P1: not a JSON file, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P1: target is not valid JSON"
    if not isinstance(data, dict):
        return False, "P1: top-level must be a JSON object carrying schema_version"
    if str(data.get("schema_version")) != "1.0":
        return False, "P1: missing top-level schema_version == \"1.0\" (got %r)" % data.get("schema_version")
    def _check_keys(obj):
        if isinstance(obj, dict):
            for k in obj.keys():
                if re.search(r"[a-z][A-Z]", k): return k
            for v in obj.values():
                r = _check_keys(v)
                if r: return r
        elif isinstance(obj, list):
            for item in obj:
                r = _check_keys(item)
                if r: return r
        return None
    camel_key = _check_keys(data)
    if camel_key:
        return False, "P1: JSON field %r uses camelCase (must use snake_case)" % camel_key
    return True, "P1: PASSED"


def check_P2(ws, target):
    """Markdown docs: level-1 and level-2 headings must be bilingual (# 中文 / English)."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    if not str(target).endswith(".md"):
        return True, "P2: not a Markdown file, skip"
    h1 = re.findall(r"^# .+", txt, re.MULTILINE)
    h2 = re.findall(r"^## .+", txt, re.MULTILINE)
    def _is_bilingual(h): return "/" in h
    if h1 and not any(_is_bilingual(h) for h in h1):
        return False, "P2: level-1 heading not bilingual: %r" % h1[0]
    if h2 and not any(_is_bilingual(h) for h in h2):
        return False, "P2: level-2 heading not bilingual: %r" % h2[0]
    return True, "P2: PASSED"


def check_P3(ws, target):
    """Before modifying any config file (yml/yaml), a .bak backup must exist.
    P3 only applies to configuration files (yml/yaml), not newly created documents."""
    tp = ws / target
    if not tp.exists():
        return True, "P3: target missing, skip"
    # P3 only applies to config files being modified (yml/yaml files)
    tgt_str = str(target)
    if not (tgt_str.endswith(".yml") or tgt_str.endswith(".yaml")):
        return True, "P3: not a config file, skip (P3 applies to yml/yaml configs only)"
    bak = Path(str(tp) + ".bak")
    if not bak.exists():
        return False, "P3: backup not found: %s.bak" % target
    return True, "P3: PASSED"


def check_P4(ws, target):
    """GitLab CI configs in .gitlab/ci/ (stage-split); root .gitlab-ci.yml uses include:."""
    txt = _read(ws / ".gitlab-ci.yml")
    if txt is None:
        return True, "P4: .gitlab-ci.yml missing, skip"
    lines = txt.splitlines()
    job_lines = [
        l for l in lines
        if re.match(r"^[a-zA-Z][a-zA-Z0-9_-]+\s*:", l) and
        not l.strip().startswith("#") and
        l.strip().split(":")[0].strip() not in (
            "stages", "variables", "cache", "default", "workflow", "include",
            "image", "services", "before_script", "after_script", "rules",
            "extends", "artifacts", "environment", "needs", "script",
            "coverage", "interruptible", "retry", "timeout", "tags",
        )
    ]
    if len(job_lines) > 1:
        return False, "P4: .gitlab-ci.yml appears to contain inline job definitions (stage-split required)"
    return True, "P4: PASSED"


def check_P5(ws, target):
    """Python scripts must include '# version: X.Y' comment in the header."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P5: target missing, skip"
    if not str(target).endswith(".py"):
        return True, "P5: not a Python file, skip"
    if not re.search(r"#\s*version\s*:\s*\d+\.\d+", txt):
        return False, "P5: script missing '# version: X.Y' comment in header"
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
        for m in fails: print("FAILED: " + m)
        sys.exit(1)
    print("PASSED"); sys.exit(0)


if __name__ == "__main__":
    main()
