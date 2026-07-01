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
    if not (ws / ".gitlab" / "ci" / "build.yml.bak").exists():
        fails.append("backup not found: .gitlab/ci/build.yml.bak")
    txt = _read(ws / ".gitlab" / "ci" / "build.yml")
    if txt is None:
        _finish(["file not found: .gitlab/ci/build.yml"])
    # Extract lines inside files: block (under key: under cache:)
    in_files = False
    file_entries = []
    for line in txt.splitlines():
        stripped = line.strip()
        if stripped == "files:":
            in_files = True
            continue
        if in_files:
            if stripped.startswith("- "):
                file_entries.append(stripped[2:].strip())
            elif stripped and not stripped.startswith("#"):
                break
    if len(file_entries) == 0:
        fails.append("no 'files:' block found in .gitlab/ci/build.yml")
    elif len(file_entries) != 2:
        fails.append(
            "cache:key:files has %d entries (must be exactly 2: Gemfile.lock and yarn.lock)"
            % len(file_entries)
        )
    if "Gemfile.lock" not in txt:
        fails.append("cache:key:files must retain Gemfile.lock")
    if "yarn.lock" not in txt:
        fails.append("cache:key:files must retain yarn.lock")
    # Verify package-lock.json is NOT in the files block entries
    if any("package-lock.json" in e for e in file_entries):
        fails.append("cache:key:files must NOT include package-lock.json (only 2 entries allowed)")
    md = _read(ws / "audit" / "gitlab_cache_fix.md")
    if md is None:
        fails.append("file not found: audit/gitlab_cache_fix.md")
    _finish(fails)
main()
