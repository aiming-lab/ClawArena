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
    txt = _read(ws / "rca_outputs" / "nimbus_mdr_summary.md")
    if txt is None:
        _finish(["file not found: rca_outputs/nimbus_mdr_summary.md"])
    low = txt.lower()
    # V9: verbatim Form 3500A 引用
    if "3500a" not in low:
        fails.append("nimbus_mdr_summary.md does not reference Form 3500A")
    # Section B3（事件严重程度）
    if not re.search(r"section\s+b|b3", low):
        fails.append("nimbus_mdr_summary.md does not reference Section B or B3 (event description)")
    # 30 calendar days
    if "30 calendar" not in low and "30-calendar" not in low:
        fails.append("nimbus_mdr_summary.md does not mention '30 calendar days' MDR requirement")
    # 字数 >= 600
    word_count = len(txt.split())
    if word_count < 600:
        fails.append("nimbus_mdr_summary.md is %d words (expected >= 600)" % word_count)
    # F: 必须明确提及 serious_injuries 精确数字 6
    si_match = re.search(r"serious\s+injur\w*[^0-9]*(\d+)", low)
    if si_match:
        si_num = int(si_match.group(1))
        if si_num != 6:
            fails.append(
                "nimbus_mdr_summary.md reports serious_injuries as %d — "
                "must be exactly 6 per the FDA official recall notice "
                "(some session notes and bot summary contain incorrect figures)" % si_num
            )
    # C★ 跨轮闭合：从 Q1 产物读 deaths 做一致性核验
    meta1_path = ws / "rca_outputs" / "nimbus_recall_metadata.json"
    if meta1_path.exists():
        try:
            meta1 = json.loads(meta1_path.read_text(encoding="utf-8"))
            q1_deaths = str(meta1.get("deaths", ""))
            if q1_deaths and q1_deaths not in txt:
                fails.append(
                    "cross-round consistency: nimbus_mdr_summary.md must reflect the deaths count "
                    "from nimbus_recall_metadata.json (Q1 output) — found %r in Q1 but not referenced in MDR" % q1_deaths
                )
        except Exception as e:
            fails.append("could not cross-check with nimbus_recall_metadata.json: %s" % e)
    _finish(fails)
main()
