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
    txt = _read(ws / "rca_outputs" / "executive_summary.md")
    if txt is None:
        _finish(["file not found: rca_outputs/executive_summary.md"])
    # 关键数字必须出现
    if not (re.search(r"52[,.]?328", txt) or "52328" in txt):
        fails.append("executive_summary.md does not contain Nimbus unit count 52,328 or 52328")
    if not (re.search(r"3[,.]?698", txt) or "3698" in txt):
        fails.append("executive_summary.md does not contain complaints count 3,698 or 3698")
    if "Z-0885-2026" not in txt:
        fails.append("executive_summary.md does not contain Ivenix recall number Z-0885-2026")
    if "2015-02-27" not in txt:
        fails.append("executive_summary.md does not contain Nimbus distribution start 2015-02-27")
    if "2024-06-20" not in txt:
        fails.append("executive_summary.md does not contain Nimbus support cutoff 2024-06-20")
    # 必须含 IMS 修复版本 5.2.2
    if "5.2.2" not in txt:
        fails.append(
            "executive_summary.md does not reference IMS fixed version 5.2.2 — "
            "executive summary must include the complete corrective action (LVP + IMS versions)"
        )
    # Class I 必须出现至少 2 次（两个 recall 均为 Class I）
    class1_count = len(re.findall(r"Class\s+I(?!\s*I)", txt))
    if class1_count < 2:
        fails.append(
            "executive_summary.md mentions 'Class I' only %d time(s) — "
            "must appear >= 2 times (both Case A and Case B are Class I recalls)" % class1_count
        )
    # 必须明确提及 Case C 排除在当前范围之外
    low = txt.lower()
    if not (
        re.search(r"case\s+c", low) and
        re.search(r"archived|legacy|not in scope|out of scope|excluded", low)
    ):
        fails.append(
            "executive_summary.md must explicitly address Case C (SynchroMed II) as archived/legacy "
            "and out of current RCA scope"
        )
    # C★ 跨轮闭合：与 Q1/Q8/Q13 产物交叉核验数值一致性
    meta1_path = ws / "rca_outputs" / "nimbus_recall_metadata.json"
    if meta1_path.exists():
        try:
            meta1 = json.loads(meta1_path.read_text(encoding="utf-8"))
            q1_ds = str(meta1.get("distribution_start", ""))
            if q1_ds and q1_ds not in txt:
                fails.append(
                    "cross-round consistency: executive_summary.md distribution_start must match "
                    "nimbus_recall_metadata.json (Q1) value '%s'" % q1_ds
                )
            q1_sc = str(meta1.get("support_cutoff", ""))
            if q1_sc and q1_sc not in txt:
                fails.append(
                    "cross-round consistency: executive_summary.md support_cutoff must match "
                    "nimbus_recall_metadata.json (Q1) value '%s'" % q1_sc
                )
            q1_units = str(meta1.get("units_recalled", ""))
            if q1_units and q1_units not in txt.replace(",", ""):
                fails.append(
                    "cross-round consistency: executive_summary.md units_recalled must match "
                    "nimbus_recall_metadata.json (Q1) value '%s'" % q1_units
                )
        except Exception as e:
            fails.append("could not cross-check with nimbus_recall_metadata.json: %s" % e)
    else:
        fails.append(
            "nimbus_recall_metadata.json (Q1 output) not found — Q14 executive summary "
            "must be consistent with Q1 recall metadata"
        )
    meta8_path = ws / "rca_outputs" / "ivenix_recall_metadata.json"
    if meta8_path.exists():
        try:
            meta8 = json.loads(meta8_path.read_text(encoding="utf-8"))
            q8_rn = str(meta8.get("recall_number", ""))
            if q8_rn and q8_rn not in txt:
                fails.append(
                    "cross-round consistency: executive_summary.md recall_number must match "
                    "ivenix_recall_metadata.json (Q8) value '%s'" % q8_rn
                )
        except Exception as e:
            fails.append("could not cross-check with ivenix_recall_metadata.json: %s" % e)
    meta13_path = ws / "rca_outputs" / "distribution_timeline.json"
    if meta13_path.exists():
        try:
            meta13 = json.loads(meta13_path.read_text(encoding="utf-8"))
            q13_ds = str(meta13.get("distribution_start", ""))
            if q13_ds and q13_ds not in txt:
                fails.append(
                    "cross-round consistency: executive_summary.md distribution_start must match "
                    "distribution_timeline.json (Q13) value '%s'" % q13_ds
                )
            q13_sc = str(meta13.get("support_cutoff", ""))
            if q13_sc and q13_sc not in txt:
                fails.append(
                    "cross-round consistency: executive_summary.md support_cutoff must match "
                    "distribution_timeline.json (Q13) value '%s'" % q13_sc
                )
        except Exception as e:
            fails.append("could not cross-check with distribution_timeline.json: %s" % e)
    _finish(fails)
main()
