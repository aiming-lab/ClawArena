#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib
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
    data, err = _load_json(ws / "output" / "contract_metadata.json")
    if err: _finish([err])
    # 版本必须是 v2.3（非 v2.1 旧版）
    ver = str(data.get("version", "")).strip()
    if "2.3" not in ver:
        fails.append("version == %r (expected 'v2.3', not the superseded v2.1)" % ver)
    # 状态必须是 ACTIVE
    status = str(data.get("status", "")).strip().upper()
    if status != "ACTIVE":
        fails.append("status == %r (expected 'ACTIVE')" % status)
    # effective_date 必须精确等于 2026-01-15（ISO 8601，来自 MSA v2.3 DRAFT Date 字段）
    ed = str(data.get("effective_date", "")).strip()
    if ed != "2026-01-15":
        fails.append(
            "effective_date == %r (must be exactly '2026-01-15' per MSA v2.3 DRAFT header — "
            "not the superseded v2.1 date 2025-11-20, not today's date)" % ed
        )
    # superseded_version 必须引用 v2.1
    sup = str(data.get("superseded_version", "")).strip()
    if "2.1" not in sup:
        fails.append("superseded_version == %r (expected to reference 'v2.1')" % sup)
    # parties 必须包含 TechCo, Inc. 和 VendorX Solutions Ltd.（verbatim 精确名称）
    parties = data.get("parties")
    if not isinstance(parties, list) or len(parties) < 2:
        fails.append("parties must be a list with at least 2 party names, got: %r" % parties)
    else:
        parties_str = " | ".join(str(p) for p in parties)
        if "TechCo" not in parties_str:
            fails.append(
                "parties must include 'TechCo, Inc.' (exact party name from MSA v2.3 header), "
                "got: %r" % parties
            )
        if "VendorX" not in parties_str:
            fails.append(
                "parties must include 'VendorX Solutions Ltd.' (exact party name from MSA v2.3 header), "
                "got: %r" % parties
            )
    _finish(fails)
main()
