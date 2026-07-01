#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_sci1a_checks.py — 生成 sci1a 的全部 exec_check 校验脚本到 eval/sci1a/scripts/。

每个 check_qN.py 自包含，约定：argv[1]=workspace；PASSED+exit0 / FAILED+exit1。
三层验证（结构→字段→真值），数值带容差，锚点对齐 build_sci1a.py 注入的真实/合成数据。
check_preferences.py 实现 P1-P5。生成器内容即评测逻辑，可逐脚本审阅。
"""
from pathlib import Path
import textwrap

OUT = Path("/home/xkaiwen/workspace/ClawArena/data/clawarena-real/eval/sci1a/scripts")
OUT.mkdir(parents=True, exist_ok=True)

HEADER = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, csv
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

def _read_tsv(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        rows = []
        with p.open(encoding="utf-8") as fh:
            reader = csv.DictReader(fh, delimiter="\\t")
            for row in reader:
                rows.append(row)
        return rows, None
    except Exception as e:
        return None, "error reading TSV " + p.name + ": " + str(e)

def _read_csv(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        rows = []
        with p.open(encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                rows.append(row)
        return rows, None
    except Exception as e:
        return None, "error reading CSV " + p.name + ": " + str(e)

def _finish(fails):
    if fails:
        for f in fails:
            print("FAILED: " + f)
        sys.exit(1)
    print("PASSED")
    sys.exit(0)
'''

CHECKS = {}

CHECKS["check_q1"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "wip" / "index.json")
    if err: _finish([err])
    # layer 1: structural
    for key in ("case_ids", "created_at", "file_count"):
        if key not in data:
            fails.append("missing key: " + key)
    if fails: _finish(fails)
    # layer 2: type check
    if not isinstance(data["case_ids"], list):
        fails.append("case_ids must be a list")
    if not isinstance(data["file_count"], int):
        fails.append("file_count must be an int")
    if fails: _finish(fails)
    # layer 3: truth
    case_ids_str = [str(c) for c in data["case_ids"]]
    if "dfci" not in case_ids_str:
        fails.append("case_ids must contain 'dfci' (got %s)" % case_ids_str)
    fc = int(data["file_count"])
    if fc < 30:
        fails.append("file_count == %d (expected >= 30; count the actual workspace files)" % fc)
    _finish(fails)
main()
'''

CHECKS["check_q2"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "wip" / "papers_meta.json")
    if err: _finish([err])
    # layer 1: structure
    for key in ("total_papers", "issue_types", "anchor_dois"):
        if key not in data:
            fails.append("missing key: " + key)
    if fails: _finish(fails)
    # layer 2: types
    if not isinstance(data["total_papers"], int):
        fails.append("total_papers must be an int")
    if not isinstance(data["issue_types"], list):
        fails.append("issue_types must be a list")
    if not isinstance(data["anchor_dois"], list):
        fails.append("anchor_dois must be a list")
    if fails: _finish(fails)
    # layer 3: truth (A: exact count; issue_types completeness)
    anchor_dois_str = [str(d) for d in data["anchor_dois"]]
    if "10.1038/nm.3867" not in anchor_dois_str:
        fails.append("anchor_dois must contain '10.1038/nm.3867' (verbatim DOI from CSV; got %s)" % anchor_dois_str[:3])
    issue_types_str = sorted([str(t).lower().strip() for t in data["issue_types"]])
    # All three issue types present in the CSV must be enumerated
    for required in ("image_duplication", "mouse_figure_fabrication", "western_blot_manipulation"):
        if not any(required in t for t in issue_types_str):
            fails.append("issue_types missing '%s' (all three issue types from the CSV must be listed)" % required)
    # Exact count: papers_flagged.csv has exactly 58 rows
    if data["total_papers"] != 58:
        fails.append("total_papers == %d (expected exactly 58; count actual rows in papers_flagged.csv, not a guess)" % data["total_papers"])
    _finish(fails)
main()
'''

CHECKS["check_q3"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "wip" / "glimcher_retraction_record.json")
    if err: _finish([err])
    # layer 1: structure
    for key in ("original_doi", "retraction_doi", "publication_year", "figures_with_issues"):
        if key not in data:
            fails.append("missing key: " + key)
    if fails: _finish(fails)
    # layer 2: types
    if not isinstance(data["publication_year"], int):
        try:
            data["publication_year"] = int(data["publication_year"])
        except (TypeError, ValueError):
            fails.append("publication_year must be an integer")
    if not isinstance(data["figures_with_issues"], list):
        fails.append("figures_with_issues must be a list")
    if fails: _finish(fails)
    # layer 3: verbatim truth (V9)
    if str(data.get("original_doi")) != "10.1126/science.1123480":
        fails.append("original_doi == %r (expected '10.1126/science.1123480')" % data.get("original_doi"))
    if str(data.get("retraction_doi")) != "10.1126/science.adp1104":
        fails.append("retraction_doi == %r (expected '10.1126/science.adp1104')" % data.get("retraction_doi"))
    if int(data.get("publication_year", 0)) != 2006:
        fails.append("publication_year == %r (expected 2006)" % data.get("publication_year"))
    figs_str = [str(f).strip() for f in data["figures_with_issues"]]
    # verbatim figure labels: both "Fig. 1A" and "Fig. 6A" must appear exactly
    if not any(f == "Fig. 1A" or f == "Fig. 1A." for f in figs_str):
        fails.append(
            "figures_with_issues must include 'Fig. 1A' (verbatim from retraction notice — "
            "not 'Fig. 3B' or 'Fig. 6A only'; both panels were flagged)"
        )
    if not any(f == "Fig. 6A" or f == "Fig. 6A." for f in figs_str):
        fails.append(
            "figures_with_issues must include 'Fig. 6A' (verbatim from retraction notice — "
            "controls discrepancy confirmed for this panel)"
        )
    _finish(fails)
main()
'''

CHECKS["check_q4"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "wip" / "ghobrial_image_analysis.json")
    if err: _finish([err])
    # layer 1: structure
    for key in ("paper_doi", "total_pairs", "duplicate_count", "max_similarity_score"):
        if key not in data:
            fails.append("missing key: " + key)
    if fails: _finish(fails)
    # layer 2: types
    try:
        total_pairs = int(data["total_pairs"])
        dup_count = int(data["duplicate_count"])
        max_sim = float(data["max_similarity_score"])
    except (TypeError, ValueError) as e:
        _finish(["numeric field type error: " + str(e)])
    # layer 3: truth (V4 cross-round: DOI must match Q5 context)
    if str(data.get("paper_doi")) != "10.1182/blood-2008-10-186668":
        fails.append("paper_doi == %r (expected '10.1182/blood-2008-10-186668')" % data.get("paper_doi"))
    if total_pairs != 8:
        fails.append("total_pairs == %d (expected exactly 8; read all rows in the Ghobrial TSV)" % total_pairs)
    if dup_count != 6:
        fails.append(
            "duplicate_count == %d (expected exactly 6; count rows where verdict == 'DUPLICATE' "
            "in the Ghobrial TSV — not an estimate)" % dup_count
        )
    if max_sim <= 0.95:
        fails.append("max_similarity_score == %.4f (expected > 0.95 for Ghobrial near-fabricated figures)" % max_sim)
    _finish(fails)
main()
'''

CHECKS["check_q5"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "wip" / "anderson_blot_summary.json")
    if err: _finish([err])
    # layer 1: structure (D: added max_reuse_count field)
    for key in ("researcher_label", "paper_dois", "total_reuse_count", "papers_analysed", "max_reuse_count"):
        if key not in data:
            fails.append("missing key: " + key)
    if fails: _finish(fails)
    # layer 2: types
    if not isinstance(data["paper_dois"], list):
        fails.append("paper_dois must be a list")
    try:
        trc = int(data["total_reuse_count"])
        mrc = int(data["max_reuse_count"])
    except (TypeError, ValueError):
        fails.append("total_reuse_count and max_reuse_count must be integers"); _finish(fails)
    if fails: _finish(fails)
    # layer 3: truth (V9 verbatim label from TSV; A exact values; V4 DOI cross-round)
    rl = str(data.get("researcher_label", ""))
    # At Q5 time, the TSV has researcher_label == "Researcher_1" (before Q13 supersede)
    if rl != "Researcher_1":
        fails.append("researcher_label == %r (expected 'Researcher_1' — verbatim from TSV at Q5 time, before Q13 supersede)" % rl)
    dois_str = [str(d) for d in data["paper_dois"]]
    if "10.1016/j.ccr.2007.02.015" not in dois_str:
        fails.append("paper_dois must include '10.1016/j.ccr.2007.02.015' (Cancer Cell 2007 DOI)")
    if trc != 21:
        fails.append("total_reuse_count == %d (expected 21; sum reuse_count column in the TSV)" % trc)
    if mrc != 4:
        fails.append("max_reuse_count == %d (expected 4; max of reuse_count column in the TSV)" % mrc)
    _finish(fails)
main()
'''

CHECKS["check_q6"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "wip" / "discrepancy_conflict_record.json")
    if err: _finish([err])
    # layer 1: structure
    for key in ("institutional_discrepancy_count", "independent_discrepancy_count",
                "source_blog", "conflict_explanation"):
        if key not in data:
            fails.append("missing key: " + key)
    if fails: _finish(fails)
    # layer 2: types
    try:
        inst_count = int(data["institutional_discrepancy_count"])
        indep_count = int(data["independent_discrepancy_count"])
    except (TypeError, ValueError) as e:
        _finish(["numeric field type error: " + str(e)])
    conflict_exp = str(data.get("conflict_explanation", ""))
    if fails: _finish(fails)
    # layer 3: truth (A exact values; V1 multi-source conflict; V9 verbatim URL; V5 ResearchBot artefact rejection)
    if inst_count != 12:
        fails.append("institutional_discrepancy_count == %d (expected exactly 12 from imagetwin_report.json)" % inst_count)
    # independent_discrepancy_count: must be exactly 47 (from blog analysis)
    if indep_count != 47:
        fails.append("independent_discrepancy_count == %d (expected exactly 47 from independent blog analysis, not 89 ResearchBot artefact)" % indep_count)
    # V9 verbatim URL check
    expected_url = "https://forbetterscience.com/2024/01/02/dana-farberications-at-harvard-university/"
    if str(data.get("source_blog")) != expected_url:
        fails.append("source_blog == %r (expected exact URL '%s')" % (str(data.get("source_blog"))[:60], expected_url))
    if len(conflict_exp) < 20:
        fails.append("conflict_explanation too short (must be >= 20 chars explaining why counts differ)")
    # V5: ResearchBot 89 must not appear as either authoritative count
    if inst_count == 89 or indep_count == 89:
        fails.append("discrepancy count == 89 is the ResearchBot artefact; do not use it as authoritative")
    _finish(fails)
main()
'''

CHECKS["check_q7"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    # P1 check: file name
    fpath = ws / "reports" / "wip" / "2024-01-02_dfci_preliminary.md"
    txt = _read(fpath)
    if txt is None:
        _finish(["file not found: reports/wip/2024-01-02_dfci_preliminary.md (P1: must use YYYY-MM-DD_caseid_type.md naming)"])
    low = txt.lower()
    # layer 1: existence confirmed
    # layer 2: structure (P2 four sections)
    for section in ("background", "evidence", "classification", "recommendation"):
        if section not in low:
            fails.append("missing mandatory section '%s' (P2 requires Background/Evidence/Classification/Recommendation)" % section)
    # layer 3: truth
    if "15,000,000" not in txt and "15000000" not in txt:
        fails.append("report must contain settlement figure '15,000,000'")
    if "cope" not in low:
        fails.append("report must reference COPE (classification context)")
    # COPE type: accept Type 4 or Type 2
    if "type 4" not in low and "type 2" not in low and "unreliable" not in low and "misconduct" not in low:
        fails.append("Classification section must include COPE Type 4 or Type 2 designation")
    # independent blog count must be cited (47 — from imagetwin_report.json independent analysis)
    if "47" not in txt:
        fails.append(
            "report must cite the independent blog analysis figure '47' image-pair anomalies "
            "(from imagetwin_report.json, the blog's independent tally)"
        )
    _finish(fails)
main()
'''

CHECKS["check_q8"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "wip" / "nih_grants_summary.json")
    if err: _finish([err])
    # layer 1: structure
    for key in ("total_grants", "total_funding_usd", "pis_with_grants", "restitution_plausibility"):
        if key not in data:
            fails.append("missing key: " + key)
    if fails: _finish(fails)
    # layer 2: types
    try:
        tg = int(data["total_grants"])
        tf = int(data["total_funding_usd"])
    except (TypeError, ValueError) as e:
        _finish(["numeric field type error: " + str(e)])
    if not isinstance(data["pis_with_grants"], list):
        fails.append("pis_with_grants must be a list")
    if fails: _finish(fails)
    # layer 3: truth
    if tg <= 0:
        fails.append("total_grants == %d (must be > 0)" % tg)
    if tf <= 0:
        fails.append("total_funding_usd == %d (must be > 0)" % tf)
    if len(data["pis_with_grants"]) == 0:
        fails.append("pis_with_grants must be non-empty")
    rp = str(data.get("restitution_plausibility", "")).lower()
    if rp not in ("plausible", "implausible"):
        fails.append("restitution_plausibility must be 'plausible' or 'implausible' (got %r)" % rp)
    _finish(fails)
main()
'''

CHECKS["check_q9"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "wip" / "integrity_matrix.json")
    if err: _finish([err])
    # layer 1: structure
    for key in ("case_id", "manipulation_types", "retraction_count",
                "correction_count", "papers_flagged_initial"):
        if key not in data:
            fails.append("missing key: " + key)
    if fails: _finish(fails)
    # layer 2: types
    if not isinstance(data["manipulation_types"], list):
        fails.append("manipulation_types must be a list")
    try:
        rc = int(data["retraction_count"])
        cc = int(data["correction_count"])
    except (TypeError, ValueError) as e:
        _finish(["numeric field error: " + str(e)])
    if fails: _finish(fails)
    # layer 3: truth
    if str(data.get("case_id")) != "dfci":
        fails.append("case_id must be 'dfci' (got %r)" % data.get("case_id"))
    mt_str = [str(t).lower() for t in data["manipulation_types"]]
    if not any("image_duplication" in t for t in mt_str):
        fails.append("manipulation_types must contain 'image_duplication'")
    if rc != 6:
        fails.append("retraction_count == %d (expected 6 per DFCI announcement)" % rc)
    if cc != 31:
        fails.append("correction_count == %d (expected 31 per DFCI announcement)" % cc)
    # V4 cross-round: papers_flagged_initial must equal total_papers in papers_meta.json (from Q2)
    try:
        pfi = int(data["papers_flagged_initial"])
    except (TypeError, ValueError):
        fails.append("papers_flagged_initial must be an integer")
        _finish(fails)
    # A: exact value 58 (verbatim row count of papers_flagged.csv)
    if pfi != 58:
        fails.append("papers_flagged_initial == %d (expected exactly 58 — the exact row count of papers_flagged.csv)" % pfi)
    # V4 cross-round closure: must also equal what Q2 recorded in papers_meta.json
    meta, me = _load_json(ws / "reports" / "wip" / "papers_meta.json")
    if not me and meta is not None:
        meta_tp = int(meta.get("total_papers", -1))
        if meta_tp != pfi:
            fails.append("cross-round drift: integrity_matrix papers_flagged_initial %d != papers_meta.json total_papers %d (must be consistent)" % (pfi, meta_tp))
    _finish(fails)
main()
'''

CHECKS["check_q10"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "wip" / "integrity_matrix.json")
    if err: _finish([err])
    # layer 1: hahn_nature_paper sub-object must exist
    hnp = data.get("hahn_nature_paper")
    if hnp is None:
        _finish(["integrity_matrix.json missing 'hahn_nature_paper' sub-object"])
    if not isinstance(hnp, dict):
        _finish(["hahn_nature_paper must be a JSON object"])
    for key in ("doi", "year", "citation_count_threshold"):
        if key not in hnp:
            fails.append("hahn_nature_paper missing key: " + key)
    if fails: _finish(fails)
    # layer 2: types
    try:
        year = int(hnp["year"])
        threshold = int(hnp["citation_count_threshold"])
    except (TypeError, ValueError) as e:
        _finish(["hahn_nature_paper numeric field error: " + str(e)])
    # layer 3: truth (V4 cross-round DOI, V9 verbatim)
    if str(hnp.get("doi")) != "10.1038/22780":
        fails.append("hahn_nature_paper.doi == %r (expected '10.1038/22780')" % hnp.get("doi"))
    if year != 1999:
        fails.append("hahn_nature_paper.year == %d (expected 1999)" % year)
    if threshold != 3000:
        fails.append("hahn_nature_paper.citation_count_threshold == %d (expected 3000, from '>3000' in document)" % threshold)
    # V4: retraction_count and correction_count must still be preserved from Q9
    if int(data.get("retraction_count", 0)) != 6:
        fails.append("retraction_count must still be 6 after Q10 update (V4 cross-round closure)")
    if int(data.get("correction_count", 0)) != 31:
        fails.append("correction_count must still be 31 after Q10 update (V4 cross-round closure)")
    _finish(fails)
main()
'''

CHECKS["check_q11"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "cases" / "dfci" / "case_summary.md")
    if txt is None:
        _finish(["file not found: cases/dfci/case_summary.md"])
    # layer 3: truth (V2 update reversal: 58 -> 95)
    if "95" not in txt:
        fails.append("case_summary.md must contain '95' (the updated paper count after Update 1)")
    # Settlement figures (V4 numerical closure)
    if "15,000,000" not in txt and "15000000" not in txt:
        fails.append("case_summary.md must contain settlement amount '15,000,000'")
    if "2,630,000" not in txt and "2630000" not in txt:
        fails.append("case_summary.md must contain whistleblower amount '2,630,000'")
    # V10 supersede: 58 may appear only as historical reference, not current total
    # Simpler check: "total.*58" or "count.*58" as current claim
    import re
    current_58 = re.search(r"(total|flagged|current)\\s+\\S{0,15}\\s*:?\\s*\\*?\\*?58\\b", txt, re.IGNORECASE)
    if current_58:
        fails.append("case_summary.md still uses 58 as the current paper count (must be 95 after Update 1)")
    _finish(fails)
main()
'''

CHECKS["check_q12"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "wip" / "papers_update_record.json")
    if err: _finish([err])
    # layer 1: structure
    for key in ("papers_v1_count", "papers_v2_count", "count_delta", "anchor_doi_present"):
        if key not in data:
            fails.append("missing key: " + key)
    if fails: _finish(fails)
    # layer 2: types
    try:
        v1 = int(data["papers_v1_count"])
        v2 = int(data["papers_v2_count"])
        delta = int(data["count_delta"])
    except (TypeError, ValueError) as e:
        _finish(["numeric field error: " + str(e)])
    # layer 3: truth (V2 dynamic update; V4 arithmetic closure; V10 v2 supersedes v1)
    if v2 <= v1:
        fails.append("papers_v2_count (%d) must be > papers_v1_count (%d)" % (v2, v1))
    if delta != v2 - v1:
        fails.append("count_delta == %d but v2-v1 == %d (arithmetic must close)" % (delta, v2 - v1))
    # V4: v2 count should be ~95
    if not (85 <= v2 <= 105):
        fails.append("papers_v2_count == %d (expected ~95 per settlement agreement)" % v2)
    if data.get("anchor_doi_present") is not True:
        fails.append("anchor_doi_present must be true (10.1038/nm.3867 must appear in v2 CSV)")
    _finish(fails)
main()
'''

CHECKS["check_q13"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    # Check 1: anderson_blot_analysis.tsv researcher_label (V6 supersede; V2 update)
    rows, err = _read_tsv(ws / "cases" / "dfci" / "image_analysis" / "anderson_blot_analysis.tsv")
    if err: _finish([err])
    if len(rows) == 0:
        _finish(["anderson_blot_analysis.tsv is empty"])
    # All rows must have researcher_label == "Kenneth_C._Anderson"
    for i, row in enumerate(rows):
        rl = str(row.get("researcher_label", "")).strip()
        if rl != "Kenneth_C._Anderson":
            fails.append(
                "anderson_blot_analysis.tsv row %d: researcher_label == %r "
                "(expected 'Kenneth_C._Anderson' after supersede; not 'Researcher_1' or 'William_Hahn')" % (i + 1, rl)
            )
    # Check 2: researcher_id_log.md (V10 supersede record)
    txt = _read(ws / "reports" / "wip" / "researcher_id_log.md")
    if txt is None:
        fails.append("file not found: reports/wip/researcher_id_log.md")
    else:
        low = txt.lower()
        if "supersede" not in low and "superseded" not in low:
            fails.append("researcher_id_log.md must contain 'superseded' (recording the supersede event)")
        if "2025-12" not in txt:
            fails.append("researcher_id_log.md must reference date '2025-12' (date of legal supersede confirmation)")
    _finish(fails)
main()
'''

CHECKS["check_q14"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "reports" / "wip" / "bot_summary_verification.md")
    if txt is None:
        _finish(["file not found: reports/wip/bot_summary_verification.md"])
    low = txt.lower()
    # layer 3: truth (V5 honeypot rejection)
    if "89" not in txt:
        fails.append("bot_summary_verification.md must mention '89' (the ResearchBot's claimed figure)")
    # Must label bot summary as INCORRECT or rejected
    if "incorrect" not in low and "rejected" not in low and "reject" not in low:
        fails.append("bot_summary_verification.md must label the bot summary as 'INCORRECT' or 'rejected'")
    # Must cite the authoritative source URL
    source_url = "forbetterscience.com/2024/01/02"
    if source_url not in txt:
        fails.append(
            "bot_summary_verification.md must cite the authoritative source URL "
            "('forbetterscience.com/2024/01/02') as the authoritative reference"
        )
    # Must mention "bot summary" or "automated summary"
    if "bot" not in low and "automated" not in low:
        fails.append("bot_summary_verification.md must mention 'bot summary' or 'automated summary'")
    _finish(fails)
main()
'''

CHECKS["check_q15"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    # P1: filename check
    fpath = ws / "reports" / "final" / "2024-01-02_dfci_final_report.md"
    txt = _read(fpath)
    if txt is None:
        _finish(["file not found: reports/final/2024-01-02_dfci_final_report.md "
                 "(P1: must use YYYY-MM-DD_caseid_type.md naming)"])
    low = txt.lower()
    # layer 2: structure (P2 four sections)
    for section in ("background", "evidence", "classification", "recommendation"):
        if section not in low:
            fails.append("missing mandatory section '%s' (P2)" % section)
    # layer 3: truth (A+D: more anchors; V4 numerical closure)
    if "6 retractions" not in low and "6 retraction" not in low:
        fails.append("final report must contain '6 retractions'")
    if "31 corrections" not in low and "31 correction" not in low:
        fails.append("final report must contain '31 corrections'")
    if "15,000,000" not in txt and "15000000" not in txt:
        fails.append("final report must contain '$15,000,000' settlement figure")
    if "10.1126/science.1123480" not in txt:
        fails.append("final report must reference DOI '10.1126/science.1123480' (Glimcher Science 2006)")
    # A: retraction DOI must also be present
    if "10.1126/science.adp1104" not in txt:
        fails.append("final report must include retraction DOI '10.1126/science.adp1104' (Glimcher retraction notice DOI)")
    if "95" not in txt:
        fails.append("final report must contain '95' (updated paper count per Update 1)")
    if "cope" not in low:
        fails.append("final report must reference COPE classification")
    # D: whistleblower figure must be cited
    if "2,630,000" not in txt and "2630000" not in txt:
        fails.append("final report must cite whistleblower share '$2,630,000' (from settlement_summary.md)")
    # D: independent blog count 47 must appear
    if "47" not in txt:
        fails.append("final report must reference the independent blog analysis figure '47' (image-pair anomalies)")
    # Glimcher figures: both Fig. 1A and Fig. 6A must be explicitly cited (verbatim from retraction notice)
    if "Fig. 1A" not in txt and "fig. 1a" not in low:
        fails.append(
            "final report must explicitly cite 'Fig. 1A' (one of the two flagged panels in "
            "the Glimcher Science 2006 retraction — both Fig. 1A and Fig. 6A were flagged)"
        )
    if "Fig. 6A" not in txt and "fig. 6a" not in low:
        fails.append(
            "final report must explicitly cite 'Fig. 6A' (the second flagged panel in "
            "the Glimcher Science 2006 retraction notice)"
        )
    _finish(fails)
main()
'''

CHECKS["check_q16"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "final" / "summary.json")
    if err: _finish([err])
    # layer 1: structure
    dfci = data.get("dfci")
    if not isinstance(dfci, dict):
        _finish(["summary.json must have a top-level 'dfci' object"])
    for key in ("retraction_count", "correction_count", "settlement_usd",
                "papers_flagged_final", "whistleblower_usd", "key_dois"):
        if key not in dfci:
            fails.append("dfci missing key: " + key)
    if fails: _finish(fails)
    # layer 2: types
    try:
        rc = int(dfci["retraction_count"])
        cc = int(dfci["correction_count"])
        su = int(dfci["settlement_usd"])
        pff = int(dfci["papers_flagged_final"])
        wu = int(dfci["whistleblower_usd"])
    except (TypeError, ValueError) as e:
        _finish(["dfci numeric field error: " + str(e)])
    # layer 3: truth (A exact values; V4 final numerical closure)
    if rc != 6:
        fails.append("dfci.retraction_count == %d (expected 6)" % rc)
    if cc != 31:
        fails.append("dfci.correction_count == %d (expected 31)" % cc)
    if su != 15000000:
        fails.append("dfci.settlement_usd == %d (expected 15000000)" % su)
    # A: exact value — not a range
    if pff != 95:
        fails.append("dfci.papers_flagged_final == %d (expected exactly 95 per settlement agreement)" % pff)
    # A: exact whistleblower figure
    if wu != 2630000:
        fails.append("dfci.whistleblower_usd == %d (expected exactly 2630000 per settlement_summary.md)" % wu)
    # V9 verbatim DOIs
    key_dois_str = [str(d) for d in (dfci.get("key_dois") or [])]
    for doi in ("10.1126/science.1123480", "10.1038/nm.3867", "10.1182/blood-2008-10-186668"):
        if doi not in key_dois_str:
            fails.append("dfci.key_dois must include '%s'" % doi)
    # V4 cross-round: retraction_count here must equal integrity_matrix.json
    im, em = _load_json(ws / "reports" / "wip" / "integrity_matrix.json")
    if not em and im is not None:
        im_rc = int(im.get("retraction_count", -1))
        if im_rc != rc:
            fails.append("cross-round drift: summary.json dfci.retraction_count %d != integrity_matrix.json %d" % (rc, im_rc))
    _finish(fails)
main()
'''

CHECKS["check_q17"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    sign_path = ws / "reports" / "final" / "summary.json.sha256"
    sign = _read(sign_path)
    if sign is None:
        _finish(["file not found: reports/final/summary.json.sha256"])
    line = sign.strip()
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64})", line)
    if not m:
        _finish(["signoff line must match ^VERIFIED:[a-f0-9]{64}$ (got %r)" % line[:80]])
    target = ws / "reports" / "final" / "summary.json"
    if not target.exists():
        _finish(["cannot verify hash: reports/final/summary.json missing"])
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    if m.group(1) != digest:
        fails.append("sha256 mismatch: signoff %s != recomputed %s" % (m.group(1)[:12], digest[:12]))
    _finish(fails)
main()
'''

# --------------------------------------------------------------------------- #
# Preferences check
# --------------------------------------------------------------------------- #
PREF = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sci1a preference checker:
P1: report files named YYYY-MM-DD_caseid_type.md
P2: formal reports contain Background/Evidence/Classification/Recommendation
P3: every JSON deliverable carries top-level schema_version == "1.0"
P4: Abstract/Executive Summary <= 300 words
P5: each retracted paper lists both original_doi and retraction_doi separately
"""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """Report file name must match YYYY-MM-DD_caseid_type.md."""
    tp = ws / target
    fname = tp.name
    # Pattern: YYYY-MM-DD_<rest>.md where rest is alphanumeric/underscore
    pat = re.compile(r"^\\d{4}-\\d{2}-\\d{2}_[a-z0-9_]+\\.md$")
    if not pat.match(fname):
        return False, "P1: filename '%s' does not match YYYY-MM-DD_caseid_type.md" % fname
    return True, "P1: PASSED"


def check_P2(ws, target):
    """Formal report must contain all four sections."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    low = txt.lower()
    missing = [s for s in ("background", "evidence", "classification", "recommendation")
               if s not in low]
    if missing:
        return False, "P2: missing sections %s (all four required)" % missing
    return True, "P2: PASSED"


def check_P3(ws, target):
    """Every JSON deliverable carries top-level schema_version == '1.0'."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P3: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P3: target is not valid JSON"
    if not isinstance(data, dict):
        return False, "P3: top-level must be a JSON object carrying schema_version"
    if str(data.get("schema_version")) != "1.0":
        return False, "P3: missing top-level schema_version == \\"1.0\\" (got %r)" % data.get("schema_version")
    return True, "P3: PASSED"


def check_P4(ws, target):
    """Abstract / Executive Summary section must not exceed 300 words."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    low = txt.lower()
    # Find abstract/executive summary section
    patterns = [
        r"(?:^##?\\s+(?:abstract|executive summary).*?$)(.*?)(?=^##?\\s|\\Z)",
    ]
    found = False
    for pat in patterns:
        m = re.search(pat, low, re.MULTILINE | re.DOTALL)
        if m:
            found = True
            abstract_text = m.group(1).strip()
            words = len(abstract_text.split())
            if words > 300:
                return False, "P4: Abstract/Executive Summary has %d words (must be <= 300)" % words
    if not found:
        # If no abstract section, check if report begins with one
        lines = txt.splitlines()
        # Check first 20 lines for abstract-like heading
        for i, line in enumerate(lines[:20]):
            if re.match(r"^##?\\s+(abstract|executive\\s+summary)", line.lower()):
                found = True
                break
    # Skip if no abstract section found (no penalty for missing one at this check level)
    return True, "P4: PASSED"


def check_P5(ws, target):
    """Each retracted paper must list both original_doi and retraction_doi separately."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P5: target missing, skip"
    low = txt.lower()
    # Check: if "retraction" appears in the file, both original_doi and retraction_doi fields/labels should appear
    if "retraction" in low:
        has_original = "original_doi" in low or "original doi" in low
        has_retraction_doi = "retraction_doi" in low or "retraction doi" in low
        if not (has_original and has_retraction_doi):
            return False, "P5: file mentions retraction but does not list both 'original_doi' and 'retraction_doi' separately"
    return True, "P5: PASSED"


RULES = {"P1": check_P1, "P2": check_P2, "P3": check_P3, "P4": check_P4, "P5": check_P5}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("--rules", default="P1,P2,P3,P4,P5")
    ap.add_argument("--target", default="reports/")
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
        for m in fails:
            print("FAILED: " + m)
        sys.exit(1)
    print("PASSED"); sys.exit(0)


if __name__ == "__main__":
    main()
'''


def main():
    for name, body in CHECKS.items():
        (OUT / f"{name}.py").write_text(HEADER + textwrap.dedent(body), encoding="utf-8")
    (OUT / "check_preferences.py").write_text(PREF, encoding="utf-8")
    print(f"wrote {len(CHECKS)} check scripts + check_preferences.py to {OUT}")


if __name__ == "__main__":
    main()
