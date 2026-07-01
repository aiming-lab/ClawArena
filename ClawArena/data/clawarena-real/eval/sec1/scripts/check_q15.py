#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, csv, os
from pathlib import Path

def _load_json(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        return json.loads(p.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, "invalid JSON in " + p.name + ": " + str(e)

def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None

def _finish(fails):
    if fails:
        for f in fails:
            print("FAILED: " + f)
        sys.exit(1)
    print("PASSED")
    sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "work" / "patch_diff_annotated.md")
    if txt is None:
        _finish(["file not found: work/patch_diff_annotated.md"])
    low = txt.lower()
    # V9: verbatim code identifier
    if "DO_LOG_SAFE_IN_SIGHAND" not in txt:
        fails.append("patch_diff_annotated.md missing DO_LOG_SAFE_IN_SIGHAND macro")
    # _exit(1) safe in signal handlers
    if "_exit(1)" not in txt and "_exit" not in txt:
        fails.append("patch_diff_annotated.md missing _exit(1) as async-signal-safe alternative")
    # V4: commit hash (consistent with Q4)
    if "752250c" not in txt:
        fails.append("patch_diff_annotated.md missing commit hash 752250c (must be consistent with Q4)")
    # D: must explain that syslog() calls malloc() — the specific mechanism of heap corruption
    if "malloc" not in low:
        fails.append("patch_diff_annotated.md must explain that syslog() internally calls malloc() (the heap corruption mechanism)")
    # D: must include actual code blocks (```c or similar) showing the diff
    if "```" not in txt:
        fails.append("patch_diff_annotated.md must include code blocks (```c or similar) showing the vulnerable vs patched code")
    # D: must have Chinese technical annotations (the task spec says 'Use Chinese technical annotations')
    # Check for presence of Chinese characters (basic CJK range)
    has_chinese = any(0x4e00 <= ord(c) <= 0x9fff for c in txt)
    if not has_chinese:
        fails.append("patch_diff_annotated.md must include Chinese technical annotations (as instructed in the task)")
    # D: must reference POSIX.1 standard for async-signal-safe functions
    # (signal_handler_analysis.md in assets/code_samples references POSIX.1-2008)
    if "posix" not in low and "POSIX" not in txt:
        fails.append("patch_diff_annotated.md must reference the POSIX standard for async-signal-safe functions (see assets/code_samples/signal_handler_analysis.md for POSIX.1-2008 signal safety requirements)")
    _finish(fails)
main()
