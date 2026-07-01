#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gold_solve_sci1b.py — sci1b 可解性审计（金标自检）。

在 workspace 的临时副本上模拟 update 生效后的状态，写出每一轮的正确产物，
然后运行全部 check_qN.py + 对应 preference，断言正解全部 PASS。
再做 ≥4 个反例（错误产物），断言 check 能 FAIL（不过松）。

运行：python scripts/clawarena_authoring/gold_solve_sci1b.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DS = REPO / "data" / "clawarena-real"
WS_SRC = DS / "openclaw" / "workspaces" / "sci1b"
UPD = DS / "openclaw" / "updates" / "sci1b"
SCRIPTS = DS / "eval" / "sci1b" / "scripts"
GOLD = Path("/home/xkaiwen/.claude/jobs/579de28f/tmp/sci1b_gold_ws")

# Ground-truth anchors (must match build_sci1b.py exactly)
GINO_PNAS_DOI     = "10.1073/pnas.1209746109"
GINO_PNAS_RETRACT = "10.1073/pnas.2115397118"
GINO_EVIL_DOI     = "10.1177/0956797614520714"
GINO_EVIL_RETRACT = "10.1177/09567976231187595"
GINO_AUTH_DOI     = "10.1177/0956797615575277"
GINO_AUTH_RETRACT = "10.1177/09567976231187596"
GINO_WHY_DOI      = "10.1037/pspa0000226"

PNAS_N               = 101
PNAS_SUSPICIOUS_ROWS = 8
# True CSV values (computed from pnas_study1_dataset.csv):
PUZZLE_BOTTOM        = 82   # overreport percentage from CSV (not the Data Colada reference 79)
PUZZLE_TOP           = 43   # overreport percentage from CSV (not the Data Colada reference 37)
EXPENSE_BOTTOM       = 10.2226   # from CSV (not the Data Colada reference 9.62)
EXPENSE_TOP          = 5.7998    # from CSV (not the Data Colada reference 5.27)
P_PUZZLE             = 0.0013
P_EXPENSE            = 0.0014    # from statistical_reference.json
WHY_F                = 17.69
WHY_DF1              = 2
WHY_DF2              = 596
WORD_RATING_MISMATCH = 18        # from part4_why_connect.md
PREVENTION_CORR_P    = 0.026     # from part4_why_connect.md

# Exact suspicious participant IDs from calcchain_reference.json
SUSPICIOUS_IDS = ["P012", "P013", "P014", "P015", "P016", "P017", "P018", "P019"]
# Verbatim method from calcchain_reference.json
CALCCHAIN_METHOD = "calcChain_xml"


def prep_workspace() -> Path:
    if GOLD.exists():
        shutil.rmtree(GOLD)
    shutil.copytree(WS_SRC, GOLD)
    # Apply update 1 workspace files
    for fname, target in [
        ("why_connect_extended_dataset.csv",
         "cases/gino/raw_data_analysis/why_connect_extended_dataset.csv"),
        ("retraction_registry_v1.json", "cases/gino/retraction_registry_v1.json"),
        ("extended_commentary.md", "cases/gino/extended_commentary.md"),
    ]:
        src = UPD / "upd1_workspace" / fname
        dst = GOLD / target
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dst)
    # Apply update 2 workspace files
    for fname, target in [
        ("legal_memo_calcchain_v2.md", "cases/gino/legal_memo_calcchain_v2.md"),
        ("pnas_extended_reanalysis.csv",
         "cases/gino/raw_data_analysis/pnas_extended_reanalysis.csv"),
        ("case_status_update.json", "cases/gino/case_status_update.json"),
    ]:
        src = UPD / "upd2_workspace" / fname
        dst = GOLD / target
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dst)
    return GOLD


def count_files_in_dir(d: Path) -> int:
    return sum(1 for p in d.rglob("*") if p.is_file())


def read_pnas_csv(ws: Path):
    path = ws / "cases" / "gino" / "raw_data_analysis" / "pnas_study1_dataset.csv"
    rows = []
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            rows.append(row)
    return rows


def _wj(p: Path, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2), encoding="utf-8")


def _w(p: Path, t: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(t, encoding="utf-8")


def solve(ws: Path) -> None:
    out = ws / "output"
    out.mkdir(exist_ok=True)

    # Read primary sources
    rows = read_pnas_csv(ws)
    n_total = len(rows)
    n_bottom = sum(1 for r in rows if r["condition"] == "bottom")
    n_top    = sum(1 for r in rows if r["condition"] == "top")

    expense_bottom = sum(float(r["expense_claimed_usd"]) for r in rows if r["condition"] == "bottom") / n_bottom
    expense_top    = sum(float(r["expense_claimed_usd"]) for r in rows if r["condition"] == "top")    / n_top

    overreport_bottom = [int(r["overreported"]) for r in rows if r["condition"] == "bottom"]
    overreport_top    = [int(r["overreported"]) for r in rows if r["condition"] == "top"]
    puzzle_bottom_pct = round(100 * sum(overreport_bottom) / len(overreport_bottom))
    puzzle_top_pct    = round(100 * sum(overreport_top)    / len(overreport_top))

    # Verify computed values match expected
    assert puzzle_bottom_pct == PUZZLE_BOTTOM, f"puzzle_bottom={puzzle_bottom_pct}"
    assert puzzle_top_pct == PUZZLE_TOP, f"puzzle_top={puzzle_top_pct}"
    assert 9.92 <= round(expense_bottom, 4) <= 10.52, f"expense_bottom={expense_bottom}"
    assert 5.50 <= round(expense_top, 4) <= 6.10, f"expense_top={expense_top}"

    # Read calcChain reference
    calcchain_ref = json.loads(
        (ws / "cases" / "gino" / "raw_data_analysis" / "calcchain_reference.json").read_text()
    )
    suspicious_rows = calcchain_ref["suspicious_rows"]
    suspicious_participant_ids = [str(x) for x in calcchain_ref.get("suspicious_participant_ids", [])]
    calcchain_method = calcchain_ref["method"]  # verbatim: "calcChain_xml"

    # Count files in cases/gino
    gino_files = count_files_in_dir(ws / "cases" / "gino")

    # --- q1: case_index.json ---
    _wj(out / "case_index.json", {
        "schema_version": "1.0",
        "case_id": "RIO-2023-GINO",
        "analyst_version": "1.0",
        "case_ids": ["gino"],
        "file_count": gino_files,
    })

    # --- q2: pnas_summary (P3: schema_version required) ---
    _wj(out / "q2_pnas_summary.json", {
        "schema_version": "1.0",
        "n_total": n_total,
        "n_bottom": n_bottom,
        "n_top": n_top,
    })

    # --- q3: expense_stats (true CSV values; n_bottom and n_top required; cross-check with calcchain) ---
    _wj(out / "q3_expense_stats.json", {
        "schema_version": "1.0",
        "n_total": n_total,
        "n_bottom": n_bottom,
        "n_top": n_top,
        "expense_bottom_mean": round(expense_bottom, 4),
        "expense_top_mean": round(expense_top, 4),
    })

    # --- q4: puzzle_stats (true CSV values ±1; suspicious_participant_ids from calcchain_reference.json) ---
    _wj(out / "q4_puzzle_stats.json", {
        "schema_version": "1.0",
        "puzzle_overreport_bottom_pct": puzzle_bottom_pct,
        "puzzle_overreport_top_pct": puzzle_top_pct,
        "p_puzzle_reference": P_PUZZLE,
        "suspicious_participant_ids": suspicious_participant_ids,
        "note": "p_puzzle_reference from Data Colada [109]; participant IDs from calcchain_reference.json",
    })

    # --- q5: calcchain_findings (suspicious_participant_ids verbatim from calcchain_reference.json) ---
    _wj(out / "q5_calcchain_findings.json", {
        "schema_version": "1.0",
        "paper_doi": GINO_PNAS_DOI,
        "suspicious_rows": suspicious_rows,
        "method": calcchain_method,
        "n_total": n_total,
        "suspicious_participant_ids": suspicious_participant_ids,
        "source_url": "https://datacolada.org/109",
    })

    # --- q6: why_connect_stats (word_rating_mismatch_count=18, prevention_corr_p=0.026) ---
    _wj(out / "q6_why_connect_stats.json", {
        "schema_version": "1.0",
        "paper_doi": GINO_WHY_DOI,
        "F_stat": WHY_F,
        "df1": WHY_DF1,
        "df2": WHY_DF2,
        "p_value": 0.0001,
        "word_rating_mismatch_count": WORD_RATING_MISMATCH,
        "prevention_corr_p": PREVENTION_CORR_P,
        "source_url": "https://datacolada.org/112",
    })

    # --- q7: retraction_registry ---
    _wj(out / "q7_retraction_registry.json", {
        "schema_version": "1.0",
        "case_id": "RIO-2023-GINO",
        "retraction_count": 4,
        "papers": [
            {"original_doi": GINO_PNAS_DOI, "retraction_doi": GINO_PNAS_RETRACT,
             "journal": "PNAS", "year": 2012},
            {"original_doi": GINO_EVIL_DOI, "retraction_doi": GINO_EVIL_RETRACT,
             "journal": "Psychological Science", "year": 2014},
            {"original_doi": GINO_AUTH_DOI, "retraction_doi": GINO_AUTH_RETRACT,
             "journal": "Psychological Science", "year": 2015},
            {"original_doi": GINO_WHY_DOI, "retraction_doi": "10.1037/pspa0000226_retraction",
             "journal": "JPSP", "year": 2020},
        ],
    })

    # --- q8: cross_validation (expense_bottom_ref reads from q3 output; schema_version required) ---
    q3_data = json.loads((out / "q3_expense_stats.json").read_text())
    _wj(out / "q8_cross_validation.json", {
        "schema_version": "1.0",
        "n_total_from_csv": n_total,
        "n_total_from_calcchain": calcchain_ref["n_total"],
        "n_total_consistent": (n_total == calcchain_ref["n_total"]),
        "suspicious_rows": suspicious_rows,
        "expense_bottom_ref": q3_data["expense_bottom_mean"],
    })

    # --- q9: comprehensive_stats (p_expense from statistical_reference.json) ---
    _wj(out / "q9_comprehensive_stats.json", {
        "schema_version": "1.0",
        "pnas_study1": {
            "n_total": n_total,
            "expense_bottom": round(expense_bottom, 4),
            "expense_top": round(expense_top, 4),
            "puzzle_bottom_pct": puzzle_bottom_pct,
            "puzzle_top_pct": puzzle_top_pct,
            "p_puzzle": P_PUZZLE,
            "p_expense": P_EXPENSE,
            "suspicious_rows": suspicious_rows,
        },
        "why_connect": {
            "F_stat": WHY_F,
            "df1": WHY_DF1,
            "df2": WHY_DF2,
        },
    })

    # --- q10: cope_classification (cope_section_ref verbatim from guidelines) ---
    _wj(out / "q10_cope_classification.json", {
        "schema_version": "1.0",
        "case_id": "RIO-2023-GINO",
        "cope_type": "Type 2: Research Misconduct",
        "cope_section_ref": "Type 2: Research Misconduct",
        "justification": (
            "The calcChain forensic analysis provides direct evidence that data rows were "
            "intentionally relocated in Excel, constituting deliberate data falsification "
            "per COPE Type 2: Research Misconduct (from protocols/cope_retraction_guidelines.md)."
        ),
        "papers": [
            {"original_doi": GINO_PNAS_DOI, "retraction_doi": GINO_PNAS_RETRACT},
            {"original_doi": GINO_EVIL_DOI, "retraction_doi": GINO_EVIL_RETRACT},
            {"original_doi": GINO_AUTH_DOI, "retraction_doi": GINO_AUTH_RETRACT},
            {"original_doi": GINO_WHY_DOI, "retraction_doi": "10.1037/pspa0000226_retraction"},
        ],
    })

    # --- q11: falsification_matrix (primary_forensic_method = exact verbatim from calcchain_reference.json) ---
    _wj(out / "q11_falsification_matrix.json", {
        "schema_version": "1.0",
        "case_id": "RIO-2023-GINO",
        "manipulation_types": [
            "data_row_relocation",
            "excel_calcchain_manipulation",
            "between_condition_data_transplantation",
        ],
        "retraction_count": 4,
        "primary_forensic_method": calcchain_method,  # verbatim: "calcChain_xml"
    })

    # --- q12: attribution_log.md (cite legal_memo_calcchain_v2 verbatim) ---
    _w(out / "q12_attribution_log.md", (
        "# Attribution Log — RIO-2023-GINO\n\n"
        "## calcChain Analyst Attribution\n\n"
        "The calcChain forensic analysis was conducted by the **Data Colada team** "
        "(Uri Simonsohn, Leif Nelson, Joe Simmons). "
        "Source: https://datacolada.org/109\n\n"
        "## Superseded Memo\n\n"
        "The file `protocols/SUPERSEDED_internal_memo_v1.md` (dated 2023-06-10) incorrectly "
        "attributed the analysis to 'Dr. Robert Chen (MIT)'. This memo is **superseded** "
        "by `cases/gino/legal_memo_calcchain_v2.md` (legal_memo_calcchain_v2, 2023-12-01). "
        "Do not cite the old memo in formal filings.\n\n"
        "## Participant Count Verification\n\n"
        "The Feishu bot summary (IntegrityBot) claimed N=201 for PNAS Study 1. "
        "This figure is **INCORRECT**. The authoritative count from Data Colada [109] "
        f"and the primary dataset is N={PNAS_N}. "
        "The bot likely summed participants across all four studies.\n\n"
        "**Affirmed: N=101 for PNAS Study 1.**\n"
    ))

    # --- q13: n_verification.md (must include exact URL https://datacolada.org/109) ---
    _w(out / "q13_n_verification.md", (
        "# N Verification — PNAS Study 1\n\n"
        f"## Authoritative Count: N={PNAS_N}\n\n"
        f"Primary source: Data Colada [109] (https://datacolada.org/109) explicitly documents "
        f"N={PNAS_N} participants in PNAS Study 1 (DOI: {GINO_PNAS_DOI}).\n\n"
        "## Bot Claim: N=201 — INCORRECT\n\n"
        f"The Feishu automated summary (bot) stated N=201 for PNAS Study 1. "
        "This is **INCORRECT** (rejected). The automated summary appears to aggregate "
        "participant counts across all four studies rather than reporting Study 1 alone.\n\n"
        "Multiple independent sources confirm N=101:\n"
        f"1. Data Colada [109] technical report (https://datacolada.org/109)\n"
        f"2. Primary dataset `pnas_study1_dataset.csv` (row count = {PNAS_N})\n"
        f"3. calcChain reference JSON (`calcchain_reference.json`: n_total={PNAS_N})\n"
        f"4. External analyst confirmation (Discord #paper-sleuth)\n\n"
        f"**Conclusion: N={PNAS_N} is the correct and verified figure for PNAS Study 1.**\n"
    ))

    # --- q14: final_report.md (includes 0.0014, 18, 0.026 cross-references) ---
    _w(out / "2023-07-12_gino_final_report.md", (
        "# RIO Case Report: Gino Data Falsification\n\n"
        "**File**: 2023-07-12_gino_final_report.md  |  **Case**: RIO-2023-GINO\n\n"
        "## Executive Summary\n\n"
        "This report documents the Research Integrity Office's independent reproduction of "
        "the Data Colada [109]–[112] statistical falsification analysis for four papers "
        f"authored or co-authored by Francesca Gino. PNAS Study 1 (N={PNAS_N}) showed "
        f"{PNAS_SUSPICIOUS_ROWS} suspicious rows by calcChain analysis; expense means were "
        f"${round(expense_bottom, 2)} (bottom) vs ${round(expense_top, 2)} (top) "
        f"(p={P_EXPENSE}); puzzle overreport rates "
        f"{puzzle_bottom_pct}% vs {puzzle_top_pct}% (p={P_PUZZLE}). Why Connect Study 3a: "
        f"F({WHY_DF1},{WHY_DF2})={WHY_F}, p<.0001; {WORD_RATING_MISMATCH} word-rating mismatches; "
        f"Prevention-Control correlation difference p={PREVENTION_CORR_P}. "
        "All four papers were retracted in 2021–2023. "
        "The evidence pattern supports COPE Type 2 classification (Research Misconduct).\n\n"
        "## Background\n\n"
        "Francesca Gino (Harvard Business School) co-authored four papers subsequently "
        "retracted following Data Colada technical analyses. The Data Colada team "
        "(Simonsohn, Nelson, Simmons) identified row-relocation evidence in Excel workbooks "
        "via calcChain.xml forensics. Harvard Business School initiated a formal investigation "
        "in June 2023 and concluded Gino acted 'intentionally, knowingly, or recklessly'.\n\n"
        "## Evidence\n\n"
        f"**PNAS Study 1** (DOI: {GINO_PNAS_DOI}; retraction DOI: {GINO_PNAS_RETRACT}):\n"
        f"- N={PNAS_N} participants (mileage-reimbursement paradigm)\n"
        f"- calcChain analysis: {PNAS_SUSPICIOUS_ROWS} suspicious out-of-order rows "
        f"(participants {', '.join(SUSPICIOUS_IDS)})\n"
        f"- Mean expense: bottom ${round(expense_bottom, 2)}, top ${round(expense_top, 2)} "
        f"(t-test p={P_EXPENSE})\n"
        f"- Puzzle overreport: bottom {puzzle_bottom_pct}%, top {puzzle_top_pct}% (p={P_PUZZLE})\n\n"
        f"**Evil Genius 2014** (DOI: {GINO_EVIL_DOI}; retraction DOI: {GINO_EVIL_RETRACT})\n\n"
        f"**Authenticity 2015** (DOI: {GINO_AUTH_DOI}; retraction DOI: {GINO_AUTH_RETRACT})\n\n"
        f"**Why Connect Study 3a** (DOI: {GINO_WHY_DOI}):\n"
        f"- Condition main effect: F({WHY_DF1},{WHY_DF2})={WHY_F}, p<.0001\n"
        f"- Word-rating mismatch: {WORD_RATING_MISMATCH} Prevention-condition participants "
        "with impossible 3.0-rating + positive-word pairs\n"
        f"- Prevention vs. Control word-rating correlation difference: p={PREVENTION_CORR_P} "
        "(Fisher z-test)\n\n"
        "All forensic analysis employed the calcChain forensic method.\n\n"
        "Retracted papers:\n"
        f"1. PNAS 2012: {GINO_PNAS_DOI} → retracted {GINO_PNAS_RETRACT}\n"
        f"2. Evil Genius 2014: {GINO_EVIL_DOI} → retracted {GINO_EVIL_RETRACT}\n"
        f"3. Authenticity 2015: {GINO_AUTH_DOI} → retracted {GINO_AUTH_RETRACT}\n"
        f"4. Why Connect 2020: {GINO_WHY_DOI}\n\n"
        "## Classification\n\n"
        "COPE Type 2: Research Misconduct. The calcChain forensic evidence indicates "
        "intentional manipulation of data rows in Excel workbooks to produce between-condition "
        "differences. Harvard's investigation concluded intent was 'intentional, knowingly, "
        "or recklessly'. All four retractions are warranted.\n\n"
        "## Recommendation\n\n"
        "1. Confirm all four retractions are linked bidirectionally in relevant databases.\n"
        "2. Notify funding agencies (NSF/grants) of affected publications.\n"
        "3. Advise future reviewers to apply calcChain forensic check to Excel-based datasets.\n"
        "4. Close case RIO-2023-GINO as resolved.\n"
    ))

    # --- q15: case_summary.json (p_expense, word_rating_mismatch_count, prevention_corr_p required) ---
    _wj(out / "q15_case_summary.json", {
        "schema_version": "1.0",
        "case_id": "RIO-2023-GINO",
        "pnas_study1": {
            "n_total": n_total,
            "expense_bottom": round(expense_bottom, 4),
            "expense_top": round(expense_top, 4),
            "puzzle_bottom_pct": puzzle_bottom_pct,
            "puzzle_top_pct": puzzle_top_pct,
            "p_puzzle": P_PUZZLE,
            "p_expense": P_EXPENSE,
            "suspicious_rows": suspicious_rows,
        },
        "why_connect": {
            "F_stat": WHY_F,
            "df1": WHY_DF1,
            "df2": WHY_DF2,
            "word_rating_mismatch_count": WORD_RATING_MISMATCH,
            "prevention_corr_p": PREVENTION_CORR_P,
        },
        "retraction_count": 4,
        "primary_forensic_method": "calcChain_xml_analysis",
    })

    # --- q16: signoff (SHA256 of q15) ---
    digest = hashlib.sha256((out / "q15_case_summary.json").read_bytes()).hexdigest()
    _w(out / "q16_signoff.txt", f"VERIFIED:{digest}\n")


# --------------------------------------------------------------------------- #
# Run checks
# --------------------------------------------------------------------------- #
EVAL_CMDS = {
    "q1": ["check_q1.py", ("pref", "P3", "output/case_index.json")],
    "q2": ["check_q2.py"],
    "q3": ["check_q3.py", ("pref", "P3", "output/q3_expense_stats.json")],
    "q4": ["check_q4.py"],
    "q5": ["check_q5.py", ("pref", "P3", "output/q5_calcchain_findings.json")],
    "q6": ["check_q6.py", ("pref", "P3", "output/q6_why_connect_stats.json")],
    "q7": ["check_q7.py", ("pref", "P3,P5", "output/q7_retraction_registry.json")],
    "q8": ["check_q8.py"],
    "q9": ["check_q9.py", ("pref", "P3", "output/q9_comprehensive_stats.json")],
    "q10": ["check_q10.py", ("pref", "P3,P5", "output/q10_cope_classification.json")],
    "q11": ["check_q11.py", ("pref", "P3", "output/q11_falsification_matrix.json")],
    "q12": ["check_q12.py"],
    "q13": ["check_q13.py"],
    "q14": ["check_q14.py",
            ("pref", "P1,P2,P4", "output/2023-07-12_gino_final_report.md")],
    "q15": ["check_q15.py", ("pref", "P3", "output/q15_case_summary.json")],
    "q16": ["check_q16.py"],
}


def run_check(item, ws: Path) -> tuple[bool, str]:
    if isinstance(item, tuple):
        _, rules, target = item
        cmd = [sys.executable, str(SCRIPTS / "check_preferences.py"),
               str(ws), "--rules", rules, "--target", target]
    else:
        cmd = [sys.executable, str(SCRIPTS / item), str(ws)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    out_text = (r.stdout + r.stderr).strip()
    last = out_text.splitlines()[-1] if out_text else ""
    return r.returncode == 0, last


def main():
    ws = prep_workspace()
    solve(ws)

    # Re-derive anchors for negative probes (same computation as solve())
    rows = read_pnas_csv(ws)
    _bot = [r for r in rows if r["condition"] == "bottom"]
    _top = [r for r in rows if r["condition"] == "top"]
    expense_bottom = sum(float(r["expense_claimed_usd"]) for r in _bot) / len(_bot)
    expense_top    = sum(float(r["expense_claimed_usd"]) for r in _top) / len(_top)
    puzzle_bottom_pct = round(100 * sum(int(r["overreported"]) for r in _bot) / len(_bot))
    puzzle_top_pct    = round(100 * sum(int(r["overreported"]) for r in _top) / len(_top))
    calcchain_ref = json.loads(
        (ws / "cases" / "gino" / "raw_data_analysis" / "calcchain_reference.json").read_text()
    )
    suspicious_rows = calcchain_ref["suspicious_rows"]
    suspicious_ids = [str(x) for x in calcchain_ref.get("suspicious_participant_ids", [])]

    print("=== GOLD SOLUTION: every check must PASS ===")
    n_pass = n_fail = 0
    for q, items in EVAL_CMDS.items():
        for it in items:
            ok, last = run_check(it, ws)
            tag = "pref " + it[1] if isinstance(it, tuple) else "main"
            if ok:
                n_pass += 1
                print(f"  [PASS] {q} ({tag})")
            else:
                n_fail += 1
                print(f"  [FAIL] {q} ({tag}): {last}")
    print(f"gold: {n_pass} checks PASSED, {n_fail} FAILED")

    # Negative probes — must all FAIL
    print("\n=== NEGATIVE PROBES: each must FAIL ===")
    probes = 0
    caught = 0

    # NEG1: q2 missing schema_version (new P3 enforcement)
    _wj(ws / "output" / "q2_pnas_summary.json", {
        "n_total": 101,
        "n_bottom": 50,
        "n_top": 51,
    })
    ok, _ = run_check("check_q2.py", ws); probes += 1; caught += (not ok)
    print(f"  q2 missing schema_version -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # NEG2: q3 uses Data Colada reference values and omits n_bottom/n_top
    _wj(ws / "output" / "q3_expense_stats.json", {
        "schema_version": "1.0",
        "n_total": 101,
        "expense_bottom_mean": 9.62,   # wrong (Data Colada reference, not CSV)
        "expense_top_mean": 5.27,      # wrong
    })
    ok, _ = run_check("check_q3.py", ws); probes += 1; caught += (not ok)
    print(f"  q3 decoy values 9.62/5.27 + missing n_bottom/n_top -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # NEG3: q4 uses bot overreport rates 79/37 and omits suspicious_participant_ids
    _wj(ws / "output" / "q4_puzzle_stats.json", {
        "schema_version": "1.0",
        "puzzle_overreport_bottom_pct": 79,
        "puzzle_overreport_top_pct": 37,
        "p_puzzle_reference": 0.0013,
    })
    ok, _ = run_check("check_q4.py", ws); probes += 1; caught += (not ok)
    print(f"  q4 bot decoy 79%/37% + no suspicious_participant_ids -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # NEG4: q5 omits suspicious_participant_ids
    _wj(ws / "output" / "q5_calcchain_findings.json", {
        "schema_version": "1.0",
        "paper_doi": "10.1073/pnas.1209746109",
        "suspicious_rows": 8,
        "method": "calcChain_xml",
        "n_total": 101,
    })
    ok, _ = run_check("check_q5.py", ws); probes += 1; caught += (not ok)
    print(f"  q5 missing suspicious_participant_ids -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # NEG5: q6 omits word_rating_mismatch_count and prevention_corr_p
    _wj(ws / "output" / "q6_why_connect_stats.json", {
        "schema_version": "1.0",
        "paper_doi": "10.1037/pspa0000226",
        "F_stat": 17.69,
        "df1": 2,
        "df2": 596,
        "p_value": 0.0001,
    })
    ok, _ = run_check("check_q6.py", ws); probes += 1; caught += (not ok)
    print(f"  q6 missing word_rating_mismatch_count + prevention_corr_p -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # NEG6: q8 omits expense_bottom_ref + schema_version
    # Restore q3 output first
    _wj(ws / "output" / "q3_expense_stats.json", {
        "schema_version": "1.0",
        "n_total": 101,
        "n_bottom": 50,
        "n_top": 51,
        "expense_bottom_mean": round(expense_bottom, 4),
        "expense_top_mean": round(expense_top, 4),
    })
    _wj(ws / "output" / "q8_cross_validation.json", {
        "n_total_from_csv": 101,
        "n_total_from_calcchain": 101,
        "n_total_consistent": True,
        "suspicious_rows": 8,
        # expense_bottom_ref intentionally omitted
        # schema_version intentionally omitted
    })
    ok, _ = run_check("check_q8.py", ws); probes += 1; caught += (not ok)
    print(f"  q8 missing expense_bottom_ref + schema_version -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # NEG7: q9 missing p_expense
    _wj(ws / "output" / "q9_comprehensive_stats.json", {
        "schema_version": "1.0",
        "pnas_study1": {
            "n_total": 101,
            "expense_bottom": round(expense_bottom, 4),
            "expense_top": round(expense_top, 4),
            "puzzle_bottom_pct": puzzle_bottom_pct,
            "puzzle_top_pct": puzzle_top_pct,
            "p_puzzle": 0.0013,
            "suspicious_rows": 8,
            # p_expense intentionally omitted
        },
        "why_connect": {"F_stat": 17.69, "df1": 2, "df2": 596},
    })
    ok, _ = run_check("check_q9.py", ws); probes += 1; caught += (not ok)
    print(f"  q9 missing p_expense -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # NEG8: q11 wrong primary_forensic_method (paraphrase instead of verbatim)
    _wj(ws / "output" / "q11_falsification_matrix.json", {
        "schema_version": "1.0",
        "case_id": "RIO-2023-GINO",
        "manipulation_types": ["data_row_relocation"],
        "retraction_count": 4,
        "primary_forensic_method": "calcChain_xml_analysis",  # not verbatim
    })
    ok, _ = run_check("check_q11.py", ws); probes += 1; caught += (not ok)
    print(f"  q11 primary_forensic_method='calcChain_xml_analysis' (not verbatim) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # NEG9: q12 does not cite legal_memo_calcchain_v2 verbatim
    _w(ws / "output" / "q12_attribution_log.md", (
        "# Attribution Log\n\n"
        "The calcChain analysis was done by Data Colada (Simonsohn, Nelson, Simmons). "
        "The old memo is superseded. N=201 is INCORRECT. N=101 confirmed.\n"
    ))
    ok, _ = run_check("check_q12.py", ws); probes += 1; caught += (not ok)
    print(f"  q12 no legal_memo_calcchain_v2 citation -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # NEG10: q13 missing exact URL https://datacolada.org/109
    _w(ws / "output" / "q13_n_verification.md", (
        "# N Verification\n\n"
        "N=101 per Data Colada [109] (DOI: 10.1073/pnas.1209746109). "
        "The bot claimed N=201 — this is INCORRECT. "
        "The automated summary was the source of the error.\n"
    ))
    ok, _ = run_check("check_q13.py", ws); probes += 1; caught += (not ok)
    print(f"  q13 missing exact URL https://datacolada.org/109 -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # NEG11: q15 missing p_expense + word_rating_mismatch_count + prevention_corr_p
    _wj(ws / "output" / "q15_case_summary.json", {
        "schema_version": "1.0",
        "case_id": "RIO-2023-GINO",
        "pnas_study1": {
            "n_total": 101,
            "expense_bottom": round(expense_bottom, 4),
            "expense_top": round(expense_top, 4),
            "puzzle_bottom_pct": puzzle_bottom_pct,
            "puzzle_top_pct": puzzle_top_pct,
            "p_puzzle": 0.0013,
            "suspicious_rows": 8,
            # p_expense intentionally omitted
        },
        "why_connect": {
            "F_stat": 17.69, "df1": 2, "df2": 596,
            # word_rating_mismatch_count and prevention_corr_p intentionally omitted
        },
        "retraction_count": 4,
        "primary_forensic_method": "calcChain_xml_analysis",
    })
    ok, _ = run_check("check_q15.py", ws); probes += 1; caught += (not ok)
    print(f"  q15 missing p_expense/word_rating/prevention_corr_p -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # NEG12: q16 placeholder hash — restore correct q15 first
    _wj(ws / "output" / "q15_case_summary.json", {
        "schema_version": "1.0",
        "case_id": "RIO-2023-GINO",
        "pnas_study1": {
            "n_total": 101,
            "expense_bottom": round(expense_bottom, 4),
            "expense_top": round(expense_top, 4),
            "puzzle_bottom_pct": puzzle_bottom_pct,
            "puzzle_top_pct": puzzle_top_pct,
            "p_puzzle": P_PUZZLE,
            "p_expense": P_EXPENSE,
            "suspicious_rows": suspicious_rows,
        },
        "why_connect": {
            "F_stat": WHY_F, "df1": WHY_DF1, "df2": WHY_DF2,
            "word_rating_mismatch_count": WORD_RATING_MISMATCH,
            "prevention_corr_p": PREVENTION_CORR_P,
        },
        "retraction_count": 4,
        "primary_forensic_method": "calcChain_xml_analysis",
    })
    _w(ws / "output" / "q16_signoff.txt", "VERIFIED:" + "0" * 64 + "\n")
    ok, _ = run_check("check_q16.py", ws); probes += 1; caught += (not ok)
    print(f"  q16 placeholder hash -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    print(f"negatives: {caught}/{probes} correctly caught")

    if n_fail == 0 and caught == probes:
        print("\nAUDIT OK: gold solution all-PASS and all negative probes caught.")
    else:
        print("\nAUDIT PROBLEM: see failures above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
