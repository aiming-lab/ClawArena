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
    txt = _read(ws / "output" / "final_review_report.md")
    if txt is None:
        _finish(["file not found: output/final_review_report.md"])
    low = txt.lower()
    # 必须有三个固定章节（按序）
    h_exec = "## Executive Summary"
    h_risk = "## Risk Matrix"
    h_rec = "## Recommended Actions"
    for heading in (h_exec, h_risk, h_rec):
        if heading.lower() not in low:
            fails.append("report missing required heading: '%s'" % heading)
    # 章节顺序检查（P5）
    pos_exec = low.find("## executive summary")
    pos_risk = low.find("## risk matrix")
    pos_rec = low.find("## recommended actions")
    if not (pos_exec < pos_risk < pos_rec) and all(p >= 0 for p in (pos_exec, pos_risk, pos_rec)):
        fails.append("sections out of order: must be Executive Summary → Risk Matrix → Recommended Actions (P5)")
    # 必须引用 UCC § 2-316（含 § 符号，P1 格式）
    if "2-316" not in txt:
        fails.append("report must cite UCC § 2-316 (warranty disclaimer analysis)")
    if "ucc" in low and "2-316" in txt and "§" not in txt:
        fails.append("UCC citation must use § symbol: 'UCC § 2-316' (not 'UCC 2-316')")
    # 必须引用 Hadley [1854] EWHC J70（精确含方括号格式）
    if not re.search(r"\[1854\]\s*EWHC\s*J70", txt, re.IGNORECASE):
        fails.append(
            "report must cite Hadley v Baxendale with exact format '[1854] EWHC J70' "
            "(with square brackets — '(1854)' or '9 Exch 341' alone are insufficient)"
        )
    # 必须引用 GDPR 罚款金额
    if "10,000,000" not in txt and "10000000" not in txt and "€10" not in txt:
        if "2%" not in txt and "two percent" not in low:
            fails.append("report must reference GDPR Art.28 penalty (€10,000,000 or 2%)")
    # 必须精确引用 Everbridge MSA §10（含 §10 编号）作为市场基准
    if "everbridge" not in low:
        fails.append(
            "report must reference 'Everbridge MSA §10' by name as the market benchmark "
            "for the 12-month liability cap — generic '12 months' without source is insufficient"
        )
    elif "everbridge" in low and "§10" not in txt and "s10" not in low and "section 10" not in low:
        fails.append(
            "Everbridge reference must include the specific section: 'Everbridge MSA §10' "
            "(not just 'Everbridge MSA' without section number)"
        )
    # Recommended Actions 节下必须有 ≥ 3 条编号行动项（1. / 2. / 3.）
    pos_rec_end = pos_rec
    rec_section = txt[txt.lower().find("## recommended actions"):]
    numbered_items = re.findall(r"^\s*\d+\.", rec_section, re.MULTILINE)
    if len(numbered_items) < 3:
        fails.append(
            "## Recommended Actions section must contain at least 3 numbered action items "
            "(found %d); format each as '1. Action description'" % len(numbered_items)
        )
    # 报告总字数必须 ≥ 400 words（综合报告须有实质内容）
    word_count = len(txt.split())
    if word_count < 400:
        fails.append(
            "final_review_report.md is too brief (%d words); a comprehensive contract review report "
            "must contain at least 400 words of substantive analysis" % word_count
        )
    _finish(fails)
main()
