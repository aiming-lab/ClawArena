#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re
from pathlib import Path

def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None

def _finish(fails):
    if fails:
        for f in fails: print("FAILED: " + f)
        sys.exit(1)
    print("PASSED"); sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    if not (ws / ".github" / "workflows" / "release.yml.bak").exists():
        fails.append("backup not found: .github/workflows/release.yml.bak")
    txt = _read(ws / ".github" / "workflows" / "release.yml")
    if txt is None:
        _finish(["file not found: .github/workflows/release.yml"])
    if "windows-latest" not in txt:
        fails.append("release.yml does not reference windows-latest in exclude block")
    # Collect lines inside the exclude: block (by indentation)
    in_exclude = False
    excl_lines = []
    for line in txt.splitlines():
        stripped = line.strip()
        if re.match(r"exclude\s*:", stripped):
            in_exclude = True
            continue
        if in_exclude:
            # End of exclude block: non-empty line at same or lower indent
            if stripped and not stripped.startswith("-") and not stripped.startswith("#"):
                # Check if it looks like a sibling key (not deeper indented)
                indent = len(line) - len(line.lstrip())
                if indent <= 8:  # approximate: strategy items indented > 8
                    break
            excl_lines.append(stripped)
    excl_text = " ".join(excl_lines)
    version_count = len(re.findall(r"version\s*:", excl_text))
    os_count = len(re.findall(r"\bos\s*:", excl_text))
    if version_count < 2:
        fails.append(
            "exclude block must have >= 2 entries with version field "
            "(found %d, need >= 2)" % version_count
        )
    if os_count < 2:
        fails.append(
            "exclude block must have >= 2 os entries (found %d, need >= 2)" % os_count
        )
    _finish(fails)
main()
