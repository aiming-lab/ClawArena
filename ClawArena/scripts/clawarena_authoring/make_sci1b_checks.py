#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_sci1b_checks.py — 生成 sci1b 的全部 exec_check 校验脚本到 eval/sci1b/scripts/。

每个 check_qN.py 自包含：argv[1]=workspace；PASSED+exit0 / FAILED+exit1。
三层验证（结构→字段→真值）；数值带容差；锚点对齐 build_sci1b.py 注入的真实/合成数据。
check_preferences.py 实现 P1-P5。

第二轮加难：C（跨轮闭合连锁）、E（隐藏 preference 静默考核）、F（verbatim 字段精确匹配）、G（移除 question 脚手架）
"""
from pathlib import Path
import textwrap

OUT = Path("/home/xkaiwen/workspace/ClawArena/data/clawarena-real/eval/sci1b/scripts")
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

def _finish(fails):
    if fails:
        for f in fails:
            print("FAILED: " + f)
        sys.exit(1)
    print("PASSED")
    sys.exit(0)
'''

CHECKS = {}

# q1: case_index.json — schema check (P3 required, analyst_version exact, file_count range)
CHECKS["check_q1"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "case_index.json")
    if err: _finish([err])
    # P3: schema_version must be "1.0"
    if str(data.get("schema_version")) != "1.0":
        fails.append("schema_version == %r (expected \\"1.0\\" per P3 format rule)" % data.get("schema_version"))
    if data.get("case_id") != "RIO-2023-GINO":
        fails.append("case_id == %r (expected 'RIO-2023-GINO')" % data.get("case_id"))
    if str(data.get("analyst_version")) != "1.0":
        fails.append("analyst_version == %r (expected exactly \\"1.0\\")" % data.get("analyst_version"))
    case_ids = data.get("case_ids") or []
    if "gino" not in [str(x).lower() for x in case_ids]:
        fails.append("case_ids must include 'gino' (got %s)" % case_ids)
    fc = data.get("file_count")
    try:
        fc_int = int(fc)
        if not (17 <= fc_int <= 23):
            fails.append("file_count == %d (must be between 17 and 23)" % fc_int)
    except (TypeError, ValueError):
        fails.append("file_count not an int: %r" % fc)
    _finish(fails)
main()
'''

# q2: pnas_summary — n_total=101 (V5: bot decoy=201 must fail); P3 now required in eval
CHECKS["check_q2"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q2_pnas_summary.json")
    if err: _finish([err])
    # P3 enforced: schema_version must be "1.0"
    if str(data.get("schema_version")) != "1.0":
        fails.append("schema_version == %r (expected \\"1.0\\" — P3 applies to all JSON deliverables)" % data.get("schema_version"))
    n = data.get("n_total")
    try:
        n = int(n)
    except (TypeError, ValueError):
        _finish(["n_total not an int: %r" % n])
    if not (95 <= n <= 105):
        fails.append("n_total == %d (expected 101, not the Feishu bot's 201)" % n)
    nb = data.get("n_bottom")
    nt = data.get("n_top")
    try:
        if int(nb) + int(nt) != n:
            fails.append("n_bottom + n_top == %d != n_total %d" % (int(nb)+int(nt), n))
    except (TypeError, ValueError):
        fails.append("n_bottom or n_top not int: bottom=%r top=%r" % (nb, nt))
    _finish(fails)
main()
'''

# q3: expense_stats — P3 via pref; now also requires n_bottom and n_top fields,
# plus cross-check: the calcchain_reference.json n_total must match n_total here. (C+E+F)
CHECKS["check_q3"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q3_expense_stats.json")
    if err: _finish([err])
    try:
        eb = float(data.get("expense_bottom_mean"))
        et = float(data.get("expense_top_mean"))
    except (TypeError, ValueError):
        _finish(["expense_bottom_mean or expense_top_mean not numeric"])
    # True values computed from pnas_study1_dataset.csv: bottom=10.2226, top=5.7998
    # Tolerance ±0.3
    if not (9.92 <= eb <= 10.52):
        fails.append("expense_bottom_mean == %.4f (expected near 10.22, within 9.92-10.52; read pnas_study1_dataset.csv)" % eb)
    if not (5.50 <= et <= 6.10):
        fails.append("expense_top_mean == %.4f (expected near 5.80, within 5.50-6.10; read pnas_study1_dataset.csv)" % et)
    n = data.get("n_total")
    try:
        if int(n) != 101:
            fails.append("n_total == %d (expected exactly 101)" % int(n))
    except (TypeError, ValueError):
        fails.append("n_total not int: %r" % n)
    # C: require n_bottom and n_top explicitly (cross-check with q2)
    nb = data.get("n_bottom")
    nt = data.get("n_top")
    try:
        nb_i = int(nb)
        nt_i = int(nt)
        if nb_i != 50:
            fails.append("n_bottom == %d (expected 50, from pnas_study1_dataset.csv)" % nb_i)
        if nt_i != 51:
            fails.append("n_top == %d (expected 51, from pnas_study1_dataset.csv)" % nt_i)
        if nb_i + nt_i != 101:
            fails.append("n_bottom + n_top == %d (must sum to n_total 101)" % (nb_i + nt_i))
    except (TypeError, ValueError):
        fails.append("n_bottom and n_top must both be present and integer (got bottom=%r, top=%r)" % (nb, nt))
    # C: cross-check n_total against calcchain_reference.json
    calcchain_path = ws / "cases" / "gino" / "raw_data_analysis" / "calcchain_reference.json"
    ccref, ccerr = _load_json(calcchain_path)
    if ccerr:
        fails.append("calcchain_reference.json not readable for cross-check: " + ccerr)
    else:
        cc_n = ccref.get("n_total")
        try:
            if int(cc_n) != int(n):
                fails.append("n_total %d does not match calcchain_reference.json n_total %d (cross-round consistency)" % (int(n), int(cc_n)))
        except (TypeError, ValueError):
            pass
    _finish(fails)
main()
'''

# q4: puzzle stats — tightened ±1 (true=82/43 exact), p_puzzle exact=0.0013;
#     plus F: require suspicious_participant_ids from calcchain_reference.json (C+F)
CHECKS["check_q4"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q4_puzzle_stats.json")
    if err: _finish([err])
    # P3 enforced
    if str(data.get("schema_version")) != "1.0":
        fails.append("schema_version == %r (expected \\"1.0\\" — P3 applies)" % data.get("schema_version"))
    try:
        pb = int(data.get("puzzle_overreport_bottom_pct"))
        pt = int(data.get("puzzle_overreport_top_pct"))
    except (TypeError, ValueError):
        _finish(["puzzle_overreport_bottom_pct or _top_pct not int"])
    # True values from pnas_study1_dataset.csv: bottom=82%, top=43%
    # Tolerance tightened to ±1 (eliminates bot decoy 79/37, eliminates rough estimates 80-84)
    if not (81 <= pb <= 83):
        fails.append("puzzle_overreport_bottom_pct == %d (expected 82 ±1; compute from pnas_study1_dataset.csv — bot decoy 79 or rounded 80/84 not accepted)" % pb)
    if not (42 <= pt <= 44):
        fails.append("puzzle_overreport_top_pct == %d (expected 43 ±1; compute from pnas_study1_dataset.csv — bot decoy 37 or rounded 40/46 not accepted)" % pt)
    # p_puzzle_reference must be exactly 0.0013 (verbatim from Data Colada [109])
    p = data.get("p_puzzle_reference")
    try:
        pf = float(p)
        if abs(pf - 0.0013) > 1e-9:
            fails.append("p_puzzle_reference == %r (expected exactly 0.0013, verbatim from Data Colada [109])" % p)
    except (TypeError, ValueError):
        fails.append("p_puzzle_reference not numeric: %r" % p)
    # F+C: require suspicious_participant_ids array (read from calcchain_reference.json)
    calcchain_path = ws / "cases" / "gino" / "raw_data_analysis" / "calcchain_reference.json"
    ccref, ccerr = _load_json(calcchain_path)
    expected_ids = []
    if not ccerr and ccref:
        expected_ids = [str(x) for x in (ccref.get("suspicious_participant_ids") or [])]
    provided_ids = data.get("suspicious_participant_ids")
    if provided_ids is None:
        fails.append("suspicious_participant_ids field missing (must list the exact IDs from calcchain_reference.json: %s)" % expected_ids)
    else:
        prov_set = set(str(x) for x in (provided_ids or []))
        exp_set = set(expected_ids)
        if prov_set != exp_set:
            fails.append("suspicious_participant_ids %s does not match calcchain_reference.json expected %s" % (sorted(prov_set), sorted(exp_set)))
    _finish(fails)
main()
'''

# q5: calcchain_findings — paper_doi verbatim, suspicious_rows=8, method contains calcChain_xml,
#     n_total=101; F+C: suspicious_participant_ids must match calcchain_reference.json exactly
CHECKS["check_q5"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q5_calcchain_findings.json")
    if err: _finish([err])
    # V9: verbatim DOI
    doi = str(data.get("paper_doi") or "")
    if doi != "10.1073/pnas.1209746109":
        fails.append("paper_doi == %r (expected verbatim '10.1073/pnas.1209746109')" % doi)
    sr = data.get("suspicious_rows")
    try:
        if int(sr) != 8:
            fails.append("suspicious_rows == %r (expected 8)" % sr)
    except (TypeError, ValueError):
        fails.append("suspicious_rows not int: %r" % sr)
    method = str(data.get("method") or "")
    if "calcchain_xml" not in method.lower() and "calcchain" not in method.lower():
        fails.append("method == %r (must contain 'calcChain_xml')" % method)
    n = data.get("n_total")
    try:
        if not (95 <= int(n) <= 105):
            fails.append("n_total == %r (expected 101, consistent with q2)" % n)
    except (TypeError, ValueError):
        fails.append("n_total not int: %r" % n)
    # F+C: suspicious_participant_ids must be the exact 8 IDs from calcchain_reference.json
    calcchain_path = ws / "cases" / "gino" / "raw_data_analysis" / "calcchain_reference.json"
    ccref, ccerr = _load_json(calcchain_path)
    expected_ids = []
    if not ccerr and ccref:
        expected_ids = [str(x) for x in (ccref.get("suspicious_participant_ids") or [])]
    provided_ids = data.get("suspicious_participant_ids")
    if provided_ids is None:
        fails.append("suspicious_participant_ids field missing (must be the exact participant IDs from calcchain_reference.json: %s)" % expected_ids)
    else:
        prov_set = set(str(x) for x in (provided_ids or []))
        exp_set = set(expected_ids)
        if prov_set != exp_set:
            fails.append("suspicious_participant_ids %s does not match calcchain_reference.json expected %s" % (sorted(prov_set), sorted(exp_set)))
    _finish(fails)
main()
'''

# q6: why_connect_stats — F=17.69, df1=2, df2=596, p<0.001;
#     F: word_rating_mismatch_count=18 and prevention_corr_p=0.026 required (from part4_why_connect.md)
CHECKS["check_q6"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q6_why_connect_stats.json")
    if err: _finish([err])
    # V9 verbatim DOI
    doi = str(data.get("paper_doi") or "")
    if doi != "10.1037/pspa0000226":
        fails.append("paper_doi == %r (expected verbatim '10.1037/pspa0000226')" % doi)
    # F-stat closure: 17.69 +/- 0.1
    try:
        f = float(data.get("F_stat"))
        if not (17.59 <= f <= 17.79):
            fails.append("F_stat == %.4f (expected near 17.69, read from part4_why_connect.md)" % f)
    except (TypeError, ValueError):
        fails.append("F_stat not numeric: %r" % data.get("F_stat"))
    try:
        if int(data.get("df1")) != 2:
            fails.append("df1 == %r (expected 2)" % data.get("df1"))
        if int(data.get("df2")) != 596:
            fails.append("df2 == %r (expected 596)" % data.get("df2"))
    except (TypeError, ValueError):
        fails.append("df1 or df2 not int")
    try:
        if float(data.get("p_value")) >= 0.001:
            fails.append("p_value == %r (expected < 0.001)" % data.get("p_value"))
    except (TypeError, ValueError):
        fails.append("p_value not numeric: %r" % data.get("p_value"))
    # F: word_rating_mismatch_count from part4_why_connect.md — 18 impossible pairs
    wm = data.get("word_rating_mismatch_count")
    try:
        if int(wm) != 18:
            fails.append("word_rating_mismatch_count == %r (expected 18, from part4_why_connect.md: 18 Prevention participants with impossible 3.0-rating + positive-word pairs)" % wm)
    except (TypeError, ValueError):
        fails.append("word_rating_mismatch_count missing or not int (expected 18; read part4_why_connect.md)")
    # F: prevention_corr_p from part4_why_connect.md — must be 0.026 (±0.001)
    pcp = data.get("prevention_corr_p")
    try:
        pcpf = float(pcp)
        if not (0.025 <= pcpf <= 0.027):
            fails.append("prevention_corr_p == %r (expected 0.026 ±0.001, from part4_why_connect.md Fisher z test)" % pcp)
    except (TypeError, ValueError):
        fails.append("prevention_corr_p missing or not numeric (expected 0.026; read part4_why_connect.md)")
    _finish(fails)
main()
'''

# q7: retraction_registry — 4 papers, each with original_doi and retraction_doi (V9, P5)
# Note: JPSP (10.1037/pspa0000226) retraction DOI is not in jpsp_2023.md retraction notice.
# Agent must find it from retraction_registry_v1.json (update 1) which also shows null,
# making this genuinely hard. Keep existing check — q7 was already failing.
CHECKS["check_q7"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q7_retraction_registry.json")
    if err: _finish([err])
    # retraction_count
    rc = data.get("retraction_count")
    try:
        if int(rc) != 4:
            fails.append("retraction_count == %r (expected 4)" % rc)
    except (TypeError, ValueError):
        fails.append("retraction_count not int: %r" % rc)
    papers = data.get("papers") or []
    if len(papers) < 4:
        fails.append("papers list has %d entries (expected >= 4)" % len(papers))
    # V9: verbatim PNAS DOI must appear
    all_dois = set()
    for p in papers:
        if isinstance(p, dict):
            all_dois.add(str(p.get("original_doi") or ""))
            all_dois.add(str(p.get("retraction_doi") or ""))
    if "10.1073/pnas.1209746109" not in all_dois:
        fails.append("PNAS original DOI '10.1073/pnas.1209746109' missing from retraction registry")
    # P5: each paper must have both original_doi and retraction_doi (non-null, non-empty)
    for i, p in enumerate(papers):
        if not isinstance(p, dict):
            continue
        od = p.get("original_doi")
        rd = p.get("retraction_doi")
        if not od or od == "null":
            fails.append("paper[%d] missing original_doi" % i)
        if not rd or rd == "null":
            fails.append("paper[%d] missing retraction_doi" % i)
    _finish(fails)
main()
'''

# q8: cross_validation — n_total consistency (V4, C); P3 now required in eval;
#     C: must also read q3 output file and cross-check expense_bottom_mean matches q3 stored value
CHECKS["check_q8"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q8_cross_validation.json")
    if err: _finish([err])
    # P3 enforced in eval (belt-and-suspenders)
    if str(data.get("schema_version")) != "1.0":
        fails.append("schema_version == %r (expected \\"1.0\\" — P3 applies)" % data.get("schema_version"))
    try:
        nc = int(data.get("n_total_from_csv"))
        ncc = int(data.get("n_total_from_calcchain"))
    except (TypeError, ValueError):
        _finish(["n_total_from_csv or n_total_from_calcchain not int"])
    if not (95 <= nc <= 105):
        fails.append("n_total_from_csv == %d (expected 101)" % nc)
    if not (95 <= ncc <= 105):
        fails.append("n_total_from_calcchain == %d (expected 101)" % ncc)
    consistent = data.get("n_total_consistent")
    if consistent is not True:
        fails.append("n_total_consistent == %r (expected true)" % consistent)
    sr = data.get("suspicious_rows")
    try:
        if int(sr) != 8:
            fails.append("suspicious_rows == %r (expected 8)" % sr)
    except (TypeError, ValueError):
        fails.append("suspicious_rows not int: %r" % sr)
    # C: cross-round closure — must read q3 output and confirm expense_bottom_mean is consistent
    q3, q3err = _load_json(ws / "output" / "q3_expense_stats.json")
    if q3err:
        fails.append("q3_expense_stats.json not readable for cross-validation (cross-round closure requires q3): " + q3err)
    else:
        try:
            eb3 = float(q3.get("expense_bottom_mean"))
            # q8 must record expense_bottom_ref from q3 (within ±0.3 of 10.22)
            ebref = data.get("expense_bottom_ref")
            if ebref is None:
                fails.append("expense_bottom_ref field missing (must record expense_bottom_mean from q3_expense_stats.json for cross-round closure; q3 value=%.4f)" % eb3)
            else:
                try:
                    ebref_f = float(ebref)
                    if abs(ebref_f - eb3) > 0.01:
                        fails.append("expense_bottom_ref %.4f does not match q3_expense_stats.json expense_bottom_mean %.4f (cross-round closure)" % (ebref_f, eb3))
                except (TypeError, ValueError):
                    fails.append("expense_bottom_ref not numeric: %r" % ebref)
        except (TypeError, ValueError):
            pass
    _finish(fails)
main()
'''

# q9: comprehensive_stats — tightened expense ±0.3, puzzle_pct required, p_puzzle exact;
#     C+F: also requires p_expense=0.0014 (from statistical_reference.json) and
#     suspicious_participant_ids array consistent with calcchain_reference.json
CHECKS["check_q9"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q9_comprehensive_stats.json")
    if err: _finish([err])
    pnas = data.get("pnas_study1") or {}
    wc   = data.get("why_connect") or {}
    try:
        n = int(pnas.get("n_total"))
        if n != 101:
            fails.append("pnas_study1.n_total == %d (expected exactly 101)" % n)
    except (TypeError, ValueError):
        fails.append("pnas_study1.n_total not int: %r" % pnas.get("n_total"))
    # expense anchors tightened to ±0.3 (true values: bottom=10.2226, top=5.7998)
    try:
        eb = float(pnas.get("expense_bottom"))
        if not (9.92 <= eb <= 10.52):
            fails.append("pnas_study1.expense_bottom == %.4f (expected near 10.22, within 9.92-10.52)" % eb)
    except (TypeError, ValueError):
        fails.append("pnas_study1.expense_bottom not numeric")
    try:
        et = float(pnas.get("expense_top"))
        if not (5.50 <= et <= 6.10):
            fails.append("pnas_study1.expense_top == %.4f (expected near 5.80, within 5.50-6.10)" % et)
    except (TypeError, ValueError):
        fails.append("pnas_study1.expense_top not numeric")
    # puzzle overreport percentages (true: bottom=82, top=43); tightened ±1
    try:
        pb9 = int(pnas.get("puzzle_bottom_pct"))
        if not (81 <= pb9 <= 83):
            fails.append("pnas_study1.puzzle_bottom_pct == %d (expected 82 ±1)" % pb9)
    except (TypeError, ValueError):
        fails.append("pnas_study1.puzzle_bottom_pct missing or not int")
    try:
        pt9 = int(pnas.get("puzzle_top_pct"))
        if not (42 <= pt9 <= 44):
            fails.append("pnas_study1.puzzle_top_pct == %d (expected 43 ±1)" % pt9)
    except (TypeError, ValueError):
        fails.append("pnas_study1.puzzle_top_pct missing or not int")
    # p_puzzle must be exactly 0.0013
    try:
        pp9 = float(pnas.get("p_puzzle"))
        if abs(pp9 - 0.0013) > 1e-9:
            fails.append("pnas_study1.p_puzzle == %r (expected exactly 0.0013)" % pnas.get("p_puzzle"))
    except (TypeError, ValueError):
        fails.append("pnas_study1.p_puzzle missing or not numeric")
    # suspicious_rows
    try:
        if int(pnas.get("suspicious_rows")) != 8:
            fails.append("pnas_study1.suspicious_rows == %r (expected 8)" % pnas.get("suspicious_rows"))
    except (TypeError, ValueError):
        fails.append("pnas_study1.suspicious_rows not int")
    # C+F: p_expense must be exactly 0.0014 (from statistical_reference.json)
    pe9 = pnas.get("p_expense")
    try:
        pe9f = float(pe9)
        if abs(pe9f - 0.0014) > 1e-9:
            fails.append("pnas_study1.p_expense == %r (expected exactly 0.0014; read from cases/gino/raw_data_analysis/statistical_reference.json)" % pe9)
    except (TypeError, ValueError):
        fails.append("pnas_study1.p_expense missing or not numeric (expected 0.0014 from statistical_reference.json)")
    # V4: F_stat closure
    try:
        f = float(wc.get("F_stat"))
        if not (17.59 <= f <= 17.79):
            fails.append("why_connect.F_stat == %.4f (expected near 17.69, not ~20)" % f)
    except (TypeError, ValueError):
        fails.append("why_connect.F_stat not numeric: %r" % wc.get("F_stat"))
    try:
        if int(wc.get("df1")) != 2:
            fails.append("why_connect.df1 == %r (expected 2)" % wc.get("df1"))
        if int(wc.get("df2")) != 596:
            fails.append("why_connect.df2 == %r (expected 596)" % wc.get("df2"))
    except (TypeError, ValueError):
        fails.append("why_connect.df1 or df2 not int")
    _finish(fails)
main()
'''

# q10: cope_classification — Type 2 or Type 4, 4 papers, P5;
#      F: cope_section_ref must cite exact section verbatim from cope_retraction_guidelines.md
CHECKS["check_q10"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q10_cope_classification.json")
    if err: _finish([err])
    if data.get("case_id") != "RIO-2023-GINO":
        fails.append("case_id == %r (expected 'RIO-2023-GINO')" % data.get("case_id"))
    cope_type = str(data.get("cope_type") or "").lower()
    if "type 2" not in cope_type and "type 4" not in cope_type:
        fails.append("cope_type == %r (must contain 'Type 2' or 'Type 4')" % data.get("cope_type"))
    papers = data.get("papers") or []
    if len(papers) < 4:
        fails.append("papers array has %d entries (expected >= 4)" % len(papers))
    # V9: PNAS DOI must appear
    all_dois = set()
    for p in papers:
        if isinstance(p, dict):
            all_dois.add(str(p.get("original_doi") or ""))
    if "10.1073/pnas.1209746109" not in all_dois:
        fails.append("PNAS original DOI '10.1073/pnas.1209746109' missing from classification papers")
    # F: cope_section_ref must cite the section from guidelines verbatim
    cref = str(data.get("cope_section_ref") or "").lower()
    if "type 2" not in cref and "type 4" not in cref:
        fails.append("cope_section_ref == %r (must cite the COPE type verbatim e.g. 'Type 2: Research Misconduct'; read protocols/cope_retraction_guidelines.md)" % data.get("cope_section_ref"))
    _finish(fails)
main()
'''

# q11: falsification_matrix — row_relocation in manipulation_types, retraction_count=4, schema_version;
#      F: primary_forensic_method must be exactly "calcChain_xml" (verbatim from calcchain_reference.json)
CHECKS["check_q11"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q11_falsification_matrix.json")
    if err: _finish([err])
    mt = data.get("manipulation_types") or []
    mt_str = " ".join(str(x).lower() for x in mt)
    if "row_relocation" not in mt_str and "data_row" not in mt_str:
        fails.append("manipulation_types must contain 'row_relocation' or 'data_row_relocation' (got %s)" % mt)
    rc = data.get("retraction_count")
    try:
        if int(rc) != 4:
            fails.append("retraction_count == %r (expected 4)" % rc)
    except (TypeError, ValueError):
        fails.append("retraction_count not int: %r" % rc)
    if str(data.get("schema_version")) != "1.0":
        fails.append("schema_version == %r (expected '1.0')" % data.get("schema_version"))
    # F: primary_forensic_method must be exactly "calcChain_xml" — verbatim from calcchain_reference.json method field
    pfm = str(data.get("primary_forensic_method") or "")
    if pfm != "calcChain_xml":
        fails.append("primary_forensic_method == %r (expected exactly 'calcChain_xml' — verbatim from cases/gino/raw_data_analysis/calcchain_reference.json 'method' field; not 'calcChain_xml_analysis' or other variant)" % pfm)
    _finish(fails)
main()
'''

# q12: attribution_log.md — Data Colada named, superseded, N=201 rejected;
#      F: must cite verbatim path "cases/gino/legal_memo_calcchain_v2.md" (the superseding document)
CHECKS["check_q12"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "output" / "q12_attribution_log.md")
    if txt is None:
        _finish(["file not found: output/q12_attribution_log.md"])
    low = txt.lower()
    # V10 supersede: must mention superseded
    if "supersed" not in low:
        fails.append("attribution_log.md must use the word 'superseded' (old memo is superseded)")
    # V6 correct attribution: Data Colada or Simonsohn/Nelson/Simmons
    if "data colada" not in low and "simonsohn" not in low:
        fails.append("attribution_log.md must name the Data Colada team (or Simonsohn) as calcChain analysts")
    # V5 bot decoy N=201 must be marked incorrect/rejected
    if "201" not in txt:
        fails.append("attribution_log.md must reference the bot's N=201 claim")
    if "incorrect" not in low and "rejected" not in low and "wrong" not in low and "error" not in low:
        fails.append("attribution_log.md must label the N=201 claim as INCORRECT, rejected, wrong, or error")
    # V4: N=101 affirmed
    if "101" not in txt and "n=101" not in low:
        fails.append("attribution_log.md must affirm N=101")
    # F: must cite the verbatim filename of the superseding legal memo
    if "legal_memo_calcchain_v2" not in txt:
        fails.append("attribution_log.md must cite 'legal_memo_calcchain_v2' (the verbatim filename of the superseding document; read cases/gino/legal_memo_calcchain_v2.md)")
    _finish(fails)
main()
'''

# q13: n_verification.md — N=101, N=201 rejected, bot cited, DOI referenced;
#      F: must include exact URL https://datacolada.org/109
CHECKS["check_q13"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "output" / "q13_n_verification.md")
    if txt is None:
        _finish(["file not found: output/q13_n_verification.md"])
    low = txt.lower()
    # V4: N=101 affirmed
    if "n=101" not in low and "n_total: 101" not in low and "n_total=101" not in low and "101" not in txt:
        fails.append("n_verification.md must state N=101")
    # V5: N=201 explicitly rejected
    if "201" not in txt:
        fails.append("n_verification.md must reference the bot's N=201 claim to reject it")
    if "incorrect" not in low and "rejected" not in low and "wrong" not in low and "error" not in low:
        fails.append("n_verification.md must label N=201 as INCORRECT, rejected, wrong, or error")
    # V1: bot/automated summary cited as source of error
    if "bot" not in low and "automated" not in low and "auto" not in low:
        fails.append("n_verification.md must reference the bot or automated summary as source of N=201 error")
    # V9: PNAS DOI referenced
    if "10.1073/pnas.1209746109" not in txt:
        fails.append("n_verification.md must reference PNAS DOI '10.1073/pnas.1209746109'")
    # F: must include the exact URL https://datacolada.org/109
    if "https://datacolada.org/109" not in txt:
        fails.append("n_verification.md must include the exact URL https://datacolada.org/109 (the primary source; read cases/gino/datacolada_reports/part1_pnas_analysis.md)")
    _finish(fails)
main()
'''

# q14: final report — all 4 retraction DOIs, F-stat exact notation, p_puzzle=0.0013;
#      C+F: also requires p_expense=0.0014, prevention_corr_p=0.026, word_rating_mismatch_count=18 cited
CHECKS["check_q14"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    # P1: correct filename
    p = ws / "output" / "2023-07-12_gino_final_report.md"
    txt = _read(p)
    if txt is None:
        _finish(["file not found: output/2023-07-12_gino_final_report.md (P1 naming convention required)"])
    low = txt.lower()
    # P2: four sections
    for section in ("## background", "## evidence", "## classification", "## recommendation"):
        if section not in low:
            fails.append("report missing section '%s' (P2 requires all four sections)" % section)
    # V4: N=101
    if "101" not in txt:
        fails.append("report must state N=101")
    # V4: F-statistic notation must be F(2,596)=17.69 or F(2, 596) = 17.69
    if "17.69" not in txt:
        fails.append("report must include F-statistic 17.69")
    if "f(2,596)" not in low and "f(2, 596)" not in low:
        fails.append("report must include F-statistic in notation F(2,596) or F(2, 596)")
    # calcChain mention
    if "calcchain" not in low:
        fails.append("report must mention calcChain")
    # V9: all 4 original DOIs
    for doi in ("10.1073/pnas.1209746109", "10.1177/0956797614520714",
                "10.1177/0956797615575277", "10.1037/pspa0000226"):
        if doi not in txt:
            fails.append("report missing original DOI %s" % doi)
    # V9+D: all 4 retraction DOIs must also appear in the report
    for retract_doi in ("10.1073/pnas.2115397118", "10.1177/09567976231187595",
                        "10.1177/09567976231187596"):
        if retract_doi not in txt:
            fails.append("report missing retraction DOI %s (include retraction DOIs, not just originals)" % retract_doi)
    # p_puzzle must appear in the report
    if "0.0013" not in txt:
        fails.append("report must cite p=0.0013 (puzzle overreporting p-value from Data Colada [109])")
    # C+F: must cite p_expense=0.0014 (Welch t-test p-value from statistical_reference.json)
    if "0.0014" not in txt:
        fails.append("report must cite p=0.0014 (expense t-test p-value from statistical_reference.json; cross-round consistency with q9)")
    # C+F: must cite word_rating_mismatch_count=18 (from part4_why_connect.md)
    if "18" not in txt:
        fails.append("report must cite 18 word-rating mismatches (from part4_why_connect.md; required cross-round with q6)")
    # C+F: must cite prevention_corr_p=0.026 (from part4_why_connect.md)
    if "0.026" not in txt:
        fails.append("report must cite prevention-control correlation difference p=0.026 (from part4_why_connect.md)")
    _finish(fails)
main()
'''

# q15: case_summary.json — expense ±0.3, puzzle_pct ±1 (tightened), p_puzzle exact;
#      C+F: requires p_expense=0.0014 and word_rating_mismatch_count=18 and prevention_corr_p=0.026
CHECKS["check_q15"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q15_case_summary.json")
    if err: _finish([err])
    pnas = data.get("pnas_study1") or {}
    wc   = data.get("why_connect") or {}
    try:
        n = int(pnas.get("n_total"))
        if n != 101:
            fails.append("pnas_study1.n_total == %d (expected exactly 101)" % n)
    except (TypeError, ValueError):
        fails.append("pnas_study1.n_total not int")
    try:
        eb = float(pnas.get("expense_bottom"))
        if not (9.92 <= eb <= 10.52):
            fails.append("pnas_study1.expense_bottom == %.4f (expected near 10.22, within 9.92-10.52)" % eb)
    except (TypeError, ValueError):
        fails.append("pnas_study1.expense_bottom not numeric")
    try:
        et = float(pnas.get("expense_top"))
        if not (5.50 <= et <= 6.10):
            fails.append("pnas_study1.expense_top == %.4f (expected near 5.80, within 5.50-6.10)" % et)
    except (TypeError, ValueError):
        fails.append("pnas_study1.expense_top not numeric")
    try:
        pp = float(pnas.get("p_puzzle"))
        if abs(pp - 0.0013) > 1e-9:
            fails.append("pnas_study1.p_puzzle == %r (expected exactly 0.0013)" % pnas.get("p_puzzle"))
    except (TypeError, ValueError):
        fails.append("pnas_study1.p_puzzle not numeric")
    try:
        if int(pnas.get("suspicious_rows")) != 8:
            fails.append("pnas_study1.suspicious_rows == %r (expected 8)" % pnas.get("suspicious_rows"))
    except (TypeError, ValueError):
        fails.append("pnas_study1.suspicious_rows not int")
    # puzzle_pct tightened to ±1 (true: 82, 43)
    try:
        pb15 = int(pnas.get("puzzle_bottom_pct"))
        if not (81 <= pb15 <= 83):
            fails.append("pnas_study1.puzzle_bottom_pct == %d (expected 82 ±1)" % pb15)
    except (TypeError, ValueError):
        fails.append("pnas_study1.puzzle_bottom_pct missing or not int")
    try:
        pt15 = int(pnas.get("puzzle_top_pct"))
        if not (42 <= pt15 <= 44):
            fails.append("pnas_study1.puzzle_top_pct == %d (expected 43 ±1)" % pt15)
    except (TypeError, ValueError):
        fails.append("pnas_study1.puzzle_top_pct missing or not int")
    # C+F: p_expense must be exactly 0.0014 (from statistical_reference.json)
    pe15 = pnas.get("p_expense")
    try:
        pe15f = float(pe15)
        if abs(pe15f - 0.0014) > 1e-9:
            fails.append("pnas_study1.p_expense == %r (expected exactly 0.0014; read from statistical_reference.json)" % pe15)
    except (TypeError, ValueError):
        fails.append("pnas_study1.p_expense missing or not numeric (expected 0.0014 from statistical_reference.json)")
    # C+F: word_rating_mismatch_count from part4_why_connect.md
    wm15 = wc.get("word_rating_mismatch_count")
    try:
        if int(wm15) != 18:
            fails.append("why_connect.word_rating_mismatch_count == %r (expected 18, from part4_why_connect.md)" % wm15)
    except (TypeError, ValueError):
        fails.append("why_connect.word_rating_mismatch_count missing or not int (expected 18; read part4_why_connect.md)")
    # C+F: prevention_corr_p from part4_why_connect.md
    pcp15 = wc.get("prevention_corr_p")
    try:
        pcp15f = float(pcp15)
        if not (0.025 <= pcp15f <= 0.027):
            fails.append("why_connect.prevention_corr_p == %r (expected 0.026 ±0.001; read part4_why_connect.md)" % pcp15)
    except (TypeError, ValueError):
        fails.append("why_connect.prevention_corr_p missing or not numeric (expected 0.026; read part4_why_connect.md)")
    # why_connect F-stat
    try:
        f = float(wc.get("F_stat"))
        if not (17.59 <= f <= 17.79):
            fails.append("why_connect.F_stat == %.4f (expected near 17.69)" % f)
    except (TypeError, ValueError):
        fails.append("why_connect.F_stat not numeric")
    try:
        if int(wc.get("df1")) != 2:
            fails.append("why_connect.df1 == %r (expected 2)" % wc.get("df1"))
        if int(wc.get("df2")) != 596:
            fails.append("why_connect.df2 == %r (expected 596)" % wc.get("df2"))
    except (TypeError, ValueError):
        fails.append("why_connect.df1 or df2 not int")
    try:
        if int(data.get("retraction_count")) != 4:
            fails.append("retraction_count == %r (expected 4)" % data.get("retraction_count"))
    except (TypeError, ValueError):
        fails.append("retraction_count not int")
    pfm = str(data.get("primary_forensic_method") or "").lower()
    if "calcchain" not in pfm:
        fails.append("primary_forensic_method == %r (must contain 'calcChain')" % data.get("primary_forensic_method"))
    _finish(fails)
main()
'''

# q16: signoff — SHA256 of q15_case_summary.json (V7) — chain: if q15 changes shape, q16 auto-fails
CHECKS["check_q16"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    sign = _read(ws / "output" / "q16_signoff.txt")
    if sign is None:
        _finish(["file not found: output/q16_signoff.txt"])
    line = sign.strip()
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64})", line)
    if not m:
        _finish(["signoff line must match ^VERIFIED:[a-f0-9]{64}$ (got %r)" % line[:80]])
    target = ws / "output" / "q15_case_summary.json"
    if not target.exists():
        _finish(["cannot verify hash: output/q15_case_summary.json missing"])
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    if m.group(1) != digest:
        fails.append("sha256 mismatch: signoff %s != recomputed %s" % (m.group(1)[:12], digest[:12]))
    _finish(fails)
main()
'''

# ---- check_preferences.py ---- P1-P5 ----
PREF = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sci1b preference checker.

P1: Report files named YYYY-MM-DD_caseid_type.md
P2: Formal reports contain sections Background/Evidence/Classification/Recommendation
P3: Every JSON deliverable carries top-level schema_version == "1.0"
P4: Executive summary (Abstract/Executive Summary section) <= 300 words
P5: Every retracted paper listed with both original_doi and retraction_doi
"""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """Report files named YYYY-MM-DD_caseid_type.md"""
    tp = ws / target
    if tp.is_dir():
        files = list(tp.glob("*.md"))
    elif tp.exists():
        files = [tp]
    else:
        return True, "P1: target missing, skip"
    pat = re.compile(r"^\\d{4}-\\d{2}-\\d{2}_[a-z0-9]+_[a-z_]+\\.md$")
    bad = [f.name for f in files if not pat.match(f.name)]
    if bad:
        return False, "P1: report files not matching YYYY-MM-DD_caseid_type.md: %s" % bad
    return True, "P1: PASSED"


def check_P2(ws, target):
    """Formal reports must have four sections."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    low = txt.lower()
    missing = [s for s in ("## background", "## evidence", "## classification", "## recommendation")
               if s not in low]
    if missing:
        return False, "P2: report missing sections: %s" % missing
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
    """Executive summary (Abstract/Executive Summary section) <= 300 words."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    # Find executive summary section
    m = re.search(
        r"(?:##\\s+(?:executive\\s+summary|abstract|summary))\\s*\\n([\\s\\S]*?)(?=\\n##|$)",
        txt, re.IGNORECASE)
    if not m:
        return True, "P4: no executive summary section found, skip"
    section_text = m.group(1)
    word_count = len(section_text.split())
    if word_count > 300:
        return False, "P4: executive summary has %d words (max 300)" % word_count
    return True, "P4: PASSED"


def check_P5(ws, target):
    """Every retracted paper must have both original_doi and retraction_doi."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P5: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return True, "P5: not JSON, skip"
    papers = data.get("papers") or []
    if not papers:
        return True, "P5: no papers list found, skip"
    bad = []
    for i, p in enumerate(papers):
        if not isinstance(p, dict):
            continue
        od = p.get("original_doi")
        rd = p.get("retraction_doi")
        if not od or od in (None, "null", ""):
            bad.append("paper[%d] missing original_doi" % i)
        if not rd or rd in (None, "null", ""):
            bad.append("paper[%d] missing retraction_doi" % i)
    if bad:
        return False, "P5: " + "; ".join(bad)
    return True, "P5: PASSED"


RULES = {"P1": check_P1, "P2": check_P2, "P3": check_P3, "P4": check_P4, "P5": check_P5}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("--rules", default="P1,P2,P3,P4,P5")
    ap.add_argument("--target", default="output/")
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
