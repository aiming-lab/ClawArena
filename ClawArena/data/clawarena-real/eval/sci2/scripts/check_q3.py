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
    txt = _read(ws / "rca_outputs" / "nimbus_5why.md")
    if txt is None:
        _finish(["file not found: rca_outputs/nimbus_5why.md"])
    low = txt.lower()
    # 关键根因词（含精确术语）
    if "battery" not in low:
        fails.append("5-why does not mention battery root cause")
    if "bms" not in low and "battery management system" not in low:
        fails.append("5-why must reference BMS (Battery Management System) design flaw — not just 'battery'")
    if not re.search(r"sterile.{0,10}barrier|barrier.{0,10}sterile", low):
        fails.append("5-why does not mention sterile barrier root cause")
    if "occlusion" not in low:
        fails.append("5-why does not mention occlusion")
    # 必须有实质性 5-Why 表格行（至少 3 行含 "| Why N |"）
    table_rows = [ln for ln in txt.splitlines() if "|" in ln and re.search(r"\|\s*Why\s*\d", ln, re.IGNORECASE)]
    if len(table_rows) < 3:
        fails.append(
            "5-why table has only %d 'Why #' rows (expected >= 3 — at least one complete chain); "
            "each row must match '| Why N |'" % len(table_rows)
        )
    # 字数 >= 600（原 400，加难）
    word_count = len(txt.split())
    if word_count < 600:
        fails.append("5-why is %d words (expected >= 600 for a rigorous 3-chain analysis)" % word_count)
    _finish(fails)
main()
