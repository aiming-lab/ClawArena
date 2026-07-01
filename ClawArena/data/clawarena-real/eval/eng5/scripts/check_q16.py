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
    txt = _read(ws / "audit" / "compliance_statement.md")
    if txt is None:
        _finish(["file not found: audit/compliance_statement.md"])
    # V9: verbatim required strings
    for s, desc in [
        ("v4.2.0", "minimum cache version"),
        ("2025-03-01", "cache deprecation deadline"),
        ("id-token: write", "OIDC permission"),
        ("optional: true", "needs optional syntax"),
    ]:
        if s not in txt:
            fails.append("compliance_statement.md missing %r (%s)" % (s, desc))
    # V4 cross-round closure: VERIFIED hash must match signoff.txt
    sign = _read(ws / "audit" / "signoff.txt")
    if sign is not None:
        sig_line = sign.strip()
        if sig_line and sig_line not in txt:
            fails.append("compliance_statement.md must include the VERIFIED:<sha256> token from signoff.txt")
    else:
        fails.append("cannot verify sha256: audit/signoff.txt missing")
    # P2: bilingual headings check
    h1 = re.findall(r"^# .+", txt, re.MULTILINE)
    h2 = re.findall(r"^## .+", txt, re.MULTILINE)
    def _is_bilingual(h):
        return "/" in h
    if h1 and not any(_is_bilingual(h) for h in h1):
        fails.append("level-1 headings must be bilingual (# 中文 / English): %r" % h1[0])
    if h2 and not any(_is_bilingual(h) for h in h2):
        fails.append("level-2 headings must be bilingual (## 中文 / English): %r" % h2[0])
    _finish(fails)
main()
