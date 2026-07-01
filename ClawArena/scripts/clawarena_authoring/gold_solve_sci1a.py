#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gold_solve_sci1a.py — sci1a 可解性审计（金标自检）。

在 workspace 的临时副本上模拟 update 生效后的状态，写出每一轮的「正确产物」，
然后运行全部 check_qN.py + 对应 preference，断言正解全部 PASS。
再做一组反例（错误产物）抽样，断言 check 能 FAIL（不过松）。

运行：python scripts/clawarena_authoring/gold_solve_sci1a.py
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
WS_SRC = DS / "openclaw" / "workspaces" / "sci1a"
UPD = DS / "openclaw" / "updates" / "sci1a"
SCRIPTS = DS / "eval" / "sci1a" / "scripts"
GOLD = Path("/home/xkaiwen/.claude/jobs/579de28f/tmp/sci1a_gold_ws")


def prep_workspace() -> Path:
    if GOLD.exists():
        shutil.rmtree(GOLD)
    shutil.copytree(WS_SRC, GOLD)
    # 应用 update 1 workspace 文件
    shutil.copy(
        UPD / "upd1_workspace" / "settlement_summary.md",
        GOLD / "cases" / "dfci" / "institution_response" / "settlement_summary.md"
    )
    shutil.copy(
        UPD / "upd1_workspace" / "papers_flagged_v2.csv",
        GOLD / "cases" / "dfci" / "papers_flagged_v2.csv"
    )
    shutil.copy(
        UPD / "upd1_workspace" / "nih_ori_investigation_notice.md",
        GOLD / "cases" / "dfci" / "institution_response" / "nih_ori_investigation_notice.md"
    )
    (GOLD / "cases" / "dfci" / "image_analysis").mkdir(parents=True, exist_ok=True)
    shutil.copy(
        UPD / "upd1_workspace" / "papers_analysis_batch2.tsv",
        GOLD / "cases" / "dfci" / "image_analysis" / "papers_analysis_batch2.tsv"
    )
    shutil.copy(
        UPD / "upd1_workspace" / "dfci_extended_case_record.md",
        GOLD / "cases" / "dfci" / "dfci_extended_case_record.md"
    )
    # 应用 update 2 workspace 文件
    (GOLD / "cases" / "dfci").mkdir(parents=True, exist_ok=True)
    shutil.copy(
        UPD / "upd2_workspace" / "researcher_id_clarification.md",
        GOLD / "cases" / "dfci" / "researcher_id_clarification.md"
    )
    (GOLD / "communications" / "email").mkdir(parents=True, exist_ok=True)
    shutil.copy(
        UPD / "upd2_workspace" / "legal_memo_researcher1.md",
        GOLD / "communications" / "email" / "legal_memo_researcher1.md"
    )
    shutil.copy(
        UPD / "upd2_workspace" / "dfci_official_statement_v2.md",
        GOLD / "cases" / "dfci" / "institution_response" / "dfci_official_statement_v2.md"
    )
    (GOLD / "cases" / "surgisphere").mkdir(parents=True, exist_ok=True)
    shutil.copy(
        UPD / "upd2_workspace" / "surgisphere_comparison_case.md",
        GOLD / "cases" / "surgisphere" / "surgisphere_comparison_case.md"
    )
    shutil.copy(
        UPD / "upd2_workspace" / "anderson_deep_analysis.tsv",
        GOLD / "cases" / "dfci" / "image_analysis" / "anderson_deep_analysis.tsv"
    )
    shutil.copy(
        UPD / "upd2_workspace" / "legal_correspondence_archive.md",
        GOLD / "communications" / "email" / "legal_correspondence_archive.md"
    )
    return GOLD


def read_csv_rows(p: Path) -> list[dict]:
    with p.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def read_tsv_rows(p: Path) -> list[dict]:
    with p.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def _w(p: Path, t: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(t, encoding="utf-8")


def _wj(p: Path, o) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def count_workspace_files(ws: Path) -> int:
    return sum(1 for p in ws.rglob("*") if p.is_file())


def solve(ws: Path) -> None:
    wip = ws / "reports" / "wip"
    final = ws / "reports" / "final"
    wip.mkdir(parents=True, exist_ok=True)
    final.mkdir(parents=True, exist_ok=True)

    # ---- Q1: workspace index ----
    fc = count_workspace_files(ws)
    _wj(wip / "index.json", {
        "schema_version": "1.0",
        "case_ids": ["dfci"],
        "created_at": "2024-01-15",
        "file_count": max(fc, 30),
        "description": "DFCI image manipulation investigation workspace — RIO case DFCI-2024-001",
    })

    # ---- Q2: papers metadata from initial CSV (all three issue types required) ----
    rows_v1 = read_csv_rows(ws / "cases" / "dfci" / "papers_flagged.csv")
    issue_types_v1 = sorted({r["issue_type"] for r in rows_v1 if r.get("issue_type")})
    anchor_dois_v1 = [r["doi"] for r in rows_v1 if r.get("doi")]
    # Exact count; all issue types enumerated
    _wj(wip / "papers_meta.json", {
        "schema_version": "1.0",
        "total_papers": len(rows_v1),        # exact: 58
        "issue_types": issue_types_v1,        # all three: image_duplication, mouse_figure_fabrication, western_blot_manipulation
        "anchor_dois": anchor_dois_v1[:5],    # includes 10.1038/nm.3867
    })
    papers_v1_count = len(rows_v1)  # == 58

    # ---- Q3: Glimcher retraction record ----
    _wj(wip / "glimcher_retraction_record.json", {
        "schema_version": "1.0",
        "original_doi": "10.1126/science.1123480",
        "retraction_doi": "10.1126/science.adp1104",
        "publication_year": 2006,
        "figures_with_issues": ["Fig. 1A", "Fig. 6A"],
        "note": "Verbatim from Science retraction notice. Hetz did not agree with retraction.",
    })

    # ---- Q4: Ghobrial image analysis ----
    ghob_rows = read_tsv_rows(ws / "cases" / "dfci" / "image_analysis" / "ghobrial_mouse_analysis.tsv")
    dup_count = sum(1 for r in ghob_rows if r.get("verdict") == "DUPLICATE")
    max_sim = max((float(r["similarity_score"]) for r in ghob_rows if r.get("similarity_score")), default=0.0)
    _wj(wip / "ghobrial_image_analysis.json", {
        "schema_version": "1.0",
        "paper_doi": "10.1182/blood-2008-10-186668",
        "total_pairs": len(ghob_rows),
        "duplicate_count": dup_count,
        "max_similarity_score": round(max_sim, 4),
        "note": "Near-entirely fabricated mouse figures per blog analysis",
    })

    # ---- Q5: Anderson blot summary (initial researcher_label from original workspace TSV) ----
    # NOTE: gold_solve uses WS_SRC (original workspace) to read the pre-Q13 TSV value.
    # At Q5 time, the TSV has researcher_label == "Researcher_1" (Q13 supersede not yet applied).
    blot_rows_orig = read_tsv_rows(WS_SRC / "cases" / "dfci" / "image_analysis" / "anderson_blot_analysis.tsv")
    researcher_labels_orig = [r.get("researcher_label", "") for r in blot_rows_orig]
    rl_from_tsv = researcher_labels_orig[0] if researcher_labels_orig else "Researcher_1"  # == "Researcher_1"
    blot_dois = sorted({r["paper_doi"] for r in blot_rows_orig if r.get("paper_doi")})
    total_reuse = sum(int(r.get("reuse_count", 0)) for r in blot_rows_orig
                      if r.get("reuse_count", "").isdigit())
    max_reuse = max((int(r.get("reuse_count", 0)) for r in blot_rows_orig
                     if r.get("reuse_count", "").isdigit()), default=0)
    _wj(wip / "anderson_blot_summary.json", {
        "schema_version": "1.0",
        "researcher_label": rl_from_tsv,      # "Researcher_1" (verbatim from Q5-time TSV)
        "paper_dois": blot_dois,
        "total_reuse_count": total_reuse,     # exact: 21
        "papers_analysed": len(blot_dois),
        "max_reuse_count": max_reuse,         # exact: 4
    })

    # ---- Q6: discrepancy conflict record ----
    it_report = json.loads((ws / "cases" / "dfci" / "image_analysis" / "imagetwin_report.json").read_text())
    _wj(wip / "discrepancy_conflict_record.json", {
        "schema_version": "1.0",
        "institutional_discrepancy_count": int(it_report["discrepancy_count"]),  # exactly 12
        "independent_discrepancy_count": 47,                                       # exactly 47
        "source_blog": str(it_report["source_blog"]),
        "conflict_explanation": (
            "DFCI institutional scan acknowledges only 12 discrepancies (formally acknowledged cases). "
            "The independent blog analysis (Sholto David) identified exactly 47 distinct image-pair anomalies. "
            "The ResearchBot figure of 89 is a known artefact and is rejected."
        ),
    })

    # ---- Q7: DFCI preliminary report ----
    prelim_txt = """# DFCI Image Manipulation Case — Preliminary Report

**File**: 2024-01-02_dfci_preliminary.md
**Date**: 2024-01-02
**Prepared by**: Senior Research Integrity Analyst, RIO

## Abstract

This preliminary report summarises findings from the DFCI image manipulation investigation
(case DFCI-2024-001), opened following a public blog analysis. The investigation identified
image manipulation across multiple research groups at Dana-Farber Cancer Institute (DFCI).
DFCI has announced 6 retractions and 31 corrections. A settlement of $15,000,000 has been
reached with the Department of Justice. Source: For Better Science blog
(https://forbetterscience.com/2024/01/02/dana-farberications-at-harvard-university/).

## Background

On 2024-01-02, independent researcher Sholto David published an analysis at
https://forbetterscience.com/2024/01/02/dana-farberications-at-harvard-university/
identifying image manipulation in papers from four DFCI research groups: Glimcher, Hahn,
Ghobrial, and Anderson. Initial scope: 58 papers. DFCI announced 6 retractions and 31
corrections.

## Evidence

1. ImageTwin institutional scan: 12 acknowledged discrepancies (institutional count).
   Independent blog analysis: 47 image-pair anomalies identified.
   Source blog: https://forbetterscience.com/2024/01/02/dana-farberications-at-harvard-university/

2. Glimcher Science 2006 (DOI: 10.1126/science.1123480) — retraction issued
   (retraction DOI: 10.1126/science.adp1104). Discrepancies in Fig. 1A and Fig. 6A controls.

3. Anderson Nature Medicine 2015 (DOI: 10.1038/nm.3867) — western blot manipulation.

4. Ghobrial Blood 2009 (DOI: 10.1182/blood-2008-10-186668) — mouse figure fabrication.

5. Settlement: $15,000,000 with DOJ; NIH restitution >$8,500,000;
   whistleblower share $2,630,000.

## Classification

Per COPE Retraction Guidelines:
- **Type 4: Unreliable findings** — confirmed image manipulation (western blot duplication,
  figure splicing).
- **Type 2: Research misconduct** — where institutional investigation confirmed intent.

Primary classification: **Type 4: Unreliable findings** with potential Type 2 elements
pending final institutional determination.

## Recommendation

1. Proceed with formal retraction for the 6 papers already identified.
2. Issue corrections for the 31 papers where conclusions are not wholly invalidated.
3. Notify NIH ORI under 42 CFR Part 93 (initiated 2025-01-15).
4. Continue investigation to confirm Researcher 1 identity and full paper scope.
"""
    _w(wip / "2024-01-02_dfci_preliminary.md", prelim_txt)

    # ---- Q8: NIH grants summary ----
    grant_rows = read_csv_rows(ws / "cases" / "dfci" / "grant_records" / "nih_grants_list.csv")
    pis = sorted({r["pi_last"] for r in grant_rows if r.get("pi_last")})
    total_grants = len(grant_rows)
    total_funding = sum(int(r.get("amount_usd", 0)) for r in grant_rows
                        if str(r.get("amount_usd", "")).isdigit())
    restitution_plausibility = "plausible" if total_funding > 8500000 else "implausible"
    _wj(wip / "nih_grants_summary.json", {
        "schema_version": "1.0",
        "total_grants": total_grants,
        "total_funding_usd": total_funding,
        "pis_with_grants": pis,
        "restitution_plausibility": restitution_plausibility,
    })

    # ---- Q9: integrity matrix (papers_flagged_initial must equal exact v1 count == 58) ----
    _wj(wip / "integrity_matrix.json", {
        "schema_version": "1.0",
        "case_id": "dfci",
        "manipulation_types": issue_types_v1,
        "retraction_count": 6,
        "correction_count": 31,
        "papers_flagged_initial": papers_v1_count,  # exact: 58
    })

    # ---- Q10: update integrity_matrix with hahn_nature_paper ----
    im = json.loads((wip / "integrity_matrix.json").read_text())
    im["hahn_nature_paper"] = {
        "doi": "10.1038/22780",
        "year": 1999,
        "citation_count_threshold": 3000,
        "note": "Foundational oncology reference; >3000 citations; correction issued 2024",
    }
    _wj(wip / "integrity_matrix.json", im)

    # ---- Q11: update case_summary.md (after Update 1) ----
    case_summary_txt = """# DFCI Image Manipulation Case — Case Summary (Updated)

**Case ID**: DFCI-2024-001
**Date Opened**: 2024-01-15
**Last Updated**: 2026-01-20
**Status**: Active Investigation — Settlement Reached

## Incident Overview

On 2024-01-02, independent researcher Sholto David published a detailed analysis on the blog
*For Better Science* (https://forbetterscience.com/2024/01/02/dana-farberications-at-harvard-university/)
identifying image manipulation across multiple papers from Dana-Farber Cancer Institute (DFCI).

**Updated scope (per December 2025 settlement)**: **95 papers** confirmed across four research
groups (Glimcher, Hahn, Ghobrial, Anderson). The initial blog count of 58 papers has been
superseded by the settlement figure.

## Key Papers Identified

| DOI | Journal | Year | Issue |
|-----|---------|------|-------|
| 10.1126/science.1123480 | Science | 2006 | Image duplication (Fig. 1A, Fig. 6A) |
| 10.1038/nm.3867 | Nature Medicine | 2015 | Western blot manipulation |
| 10.1182/blood-2008-10-186668 | Blood | 2009 | Mouse figure fabrication |
| 10.1038/22780 | Nature | 1999 | Image duplication (>3000 citations) |

## Institutional Response and Settlement

DFCI announced:
- **6 retractions** across affected research groups
- **31 corrections** issued or in progress

Settlement (December 2025, Retraction Watch 2025-12-16):
- Total settlement: **$15,000,000** with the U.S. Department of Justice
- NIH restitution: >**$8,500,000**
- Whistleblower share (Sholto David): **$2,630,000** (17.5%)

## Notes

- Paper count updated: initially 58 (blog 2024-01-02) → confirmed 95 (settlement 2025-12)
- Researcher 1 identity: confirmed as Kenneth C. Anderson (see researcher_id_clarification.md)
"""
    _w(ws / "cases" / "dfci" / "case_summary.md", case_summary_txt)

    # ---- Q12: papers update record ----
    rows_v2 = read_csv_rows(ws / "cases" / "dfci" / "papers_flagged_v2.csv")
    papers_v2_count = len(rows_v2)
    v2_dois = [r["doi"] for r in rows_v2 if r.get("doi")]
    anchor_in_v2 = "10.1038/nm.3867" in v2_dois
    _wj(wip / "papers_update_record.json", {
        "schema_version": "1.0",
        "papers_v1_count": papers_v1_count,
        "papers_v2_count": papers_v2_count,
        "count_delta": papers_v2_count - papers_v1_count,
        "anchor_doi_present": anchor_in_v2,
    })

    # ---- Q13: update anderson_blot_analysis.tsv + researcher_id_log.md ----
    # Read existing TSV, update researcher_label to Kenneth_C._Anderson
    blot_rows_to_update = read_tsv_rows(ws / "cases" / "dfci" / "image_analysis" / "anderson_blot_analysis.tsv")
    for row in blot_rows_to_update:
        row["researcher_label"] = "Kenneth_C._Anderson"
    tsv_path = ws / "cases" / "dfci" / "image_analysis" / "anderson_blot_analysis.tsv"
    if blot_rows_to_update:
        with tsv_path.open("w", encoding="utf-8", newline="") as fh:
            fieldnames = list(blot_rows_to_update[0].keys())
            writer = csv.DictWriter(fh, fieldnames=fieldnames, delimiter="\t")
            writer.writeheader()
            writer.writerows(blot_rows_to_update)
    _w(wip / "researcher_id_log.md", """# Researcher Identity Supersede Log

**Case**: DFCI-2024-001
**Log Entry Date**: 2026-02-01
**Action**: Supersede — Researcher 1 identity corrected

## Supersede Record

The preliminary internal_memo_v1.md (DFCI-MEMO-2024-003-v1, dated 2024-03-01) tentatively
identified Researcher 1 as William C. Hahn. This identification was **superseded** by the
authoritative clarification issued by Legal Counsel (Dr. Elena Vasquez) in 2025-12.

The authoritative Researcher 1 identity is: **Kenneth C. Anderson**

Per the December 2025 settlement agreement (filed with U.S. District Court), Kenneth C.
Anderson is associated with 14 papers covered in the settlement.

## Actions Taken

1. anderson_blot_analysis.tsv updated: all researcher_label values changed from
   "Researcher_1" to "Kenneth_C._Anderson"
2. internal_memo_v1.md marked as SUPERSEDED (see document header)
3. This log created to record the supersede event

**Superseded document**: internal_memo_v1.md (DFCI-MEMO-2024-003-v1)
**Superseding document**: legal_memo_researcher1.md (LEGAL-MEMO-2025-019)
**Date of supersede**: 2025-12
""")

    # ---- Q14: bot summary verification ----
    _w(wip / "bot_summary_verification.md", """# ResearchBot Summary Verification

**File**: bot_summary_verification.md
**Date**: 2026-02-01
**Analyst**: Senior Research Integrity Analyst, RIO

## Claim Under Examination

The Feishu ResearchBot automated summary stated that approximately **89** image-pair
discrepancies were detected in the DFCI corpus (Update 2, 2026-02-01 automated summary).

## Verification Against Authoritative Source

The authoritative source for discrepancy counts is:
`cases/dfci/image_analysis/imagetwin_report.json`

Source blog (authoritative for independent analysis):
https://forbetterscience.com/2024/01/02/dana-farberications-at-harvard-university/

Per the imagetwin_report.json:
- **Institutional discrepancy_count**: 12 (formally acknowledged by DFCI)
- **Independent blog analysis**: 47 image-pair anomalies

## Determination

The ResearchBot automated summary figure of **89** is **INCORRECT** and is hereby **rejected**.

This figure is a known artefact of the bot's heuristic deduplication algorithm, as explicitly
stated in the bot's own disclaimer. The authoritative figures are:
- 12 (institutional acknowledgement)
- 47 (independent blog analysis by Sholto David)

## Action

The ResearchBot summary is **not authoritative** per RIO source hierarchy (see USER.md).
All formal case records use the figures from the authoritative imagetwin_report.json and
the blog analysis at https://forbetterscience.com/2024/01/02/dana-farberications-at-harvard-university/.
""")

    # ---- Q15: DFCI final report ----
    final_report_txt = """# DFCI Image Manipulation Case — Final Report

**File**: 2024-01-02_dfci_final_report.md
**Date**: 2024-01-02
**Prepared by**: Senior Research Integrity Analyst, RIO
**Status**: FINAL — Approved for COPE submission

## Abstract

This report presents the findings of the DFCI image-manipulation investigation (DFCI-2024-001).
Following a public analysis published on 2024-01-02 (For Better Science blog), RIO conducted
a comprehensive review of papers from four DFCI research groups. A total of 95 papers were
examined; 6 were retracted and 31 corrections were issued. A settlement of $15,000,000 was
reached with the U.S. Department of Justice in December 2025, with NIH restitution of
>$8,500,000 and whistleblower share of $2,630,000 (Sholto David). Researcher 1 was confirmed
as Kenneth C. Anderson (14 papers). COPE classification: Type 4 (Unreliable findings).

## Background

Investigation opened 2024-01-15, case DFCI-2024-001. Independent researcher Sholto David
published a detailed analysis on 2024-01-02 at:
https://forbetterscience.com/2024/01/02/dana-farberications-at-harvard-university/

Initial scope: 58 papers. Settlement (December 2025) confirmed 95 papers.

Four research groups involved: Glimcher, Hahn, Ghobrial, Anderson.

Key retracted paper: Glimcher et al. Science 2006, DOI: 10.1126/science.1123480
(retraction DOI: 10.1126/science.adp1104). Discrepancies in Fig. 1A and Fig. 6A controls.

## Evidence

1. **ImageTwin analysis**: DFCI institutional count = 12 acknowledged discrepancies;
   independent blog analysis = 47 image-pair anomalies. Source blog URL verbatim:
   https://forbetterscience.com/2024/01/02/dana-farberications-at-harvard-university/

2. **Glimcher Science 2006** (DOI: 10.1126/science.1123480): Fig. 1A and Fig. 6A controls
   duplicated. Retraction notice DOI: 10.1126/science.adp1104.

3. **Anderson Nature Medicine 2015** (DOI: 10.1038/nm.3867): Western blot manipulation.
   Researcher 1 = Kenneth C. Anderson (confirmed December 2025).

4. **Ghobrial Blood 2009** (DOI: 10.1182/blood-2008-10-186668): 6 of 8 mouse figure pairs
   show similarity > 0.95 (near-entirely fabricated).

5. **Hahn Nature 1999** (DOI: 10.1038/22780): >3000 citations; correction issued.

6. **Outcome**: 6 retractions, 31 corrections.

7. **Settlement**: $15,000,000 total; NIH restitution >$8,500,000; whistleblower $2,630,000.

8. **Updated paper count**: 95 (confirmed in settlement, superseding initial 58).

## Classification

Per COPE Retraction Guidelines:
- **Type 4: Unreliable findings** — confirmed image manipulation (western blot duplication,
  mouse figure fabrication, panel splicing)
- **Type 2: Research misconduct** — confirmed for cases where institutional investigation
  confirmed intentional manipulation

Primary classification: **Type 4: Unreliable findings**
Secondary classification: **Type 2: Research misconduct** (where intent was established)

## Recommendation

1. **Retract** 6 papers as announced — fully compromised findings.
2. **Correct** 31 papers with errata — conclusions partially valid after panel correction.
3. **Notify NIH ORI** (completed 2025-01-15) — grant restitution proceeding.
4. **Update institutional policies** — mandatory ImageTwin pre-submission screening.
5. **Researcher sanctions** — refer to DFCI research integrity committee.
"""
    _w(final / "2024-01-02_dfci_final_report.md", final_report_txt)

    # ---- Q16: summary.json ----
    _wj(final / "summary.json", {
        "schema_version": "1.0",
        "dfci": {
            "case_id": "dfci",
            "retraction_count": 6,
            "correction_count": 31,
            "settlement_usd": 15000000,
            "nih_restitution_usd": 8500000,
            "whistleblower_usd": 2630000,
            "papers_flagged_final": 95,
            "key_dois": [
                "10.1126/science.1123480",
                "10.1038/nm.3867",
                "10.1182/blood-2008-10-186668",
                "10.1038/22780",
                "10.1016/j.ccr.2007.02.015",
            ],
            "key_figures": ["Fig. 1A", "Fig. 6A"],
            "researcher_1": "Kenneth_C._Anderson",
            "source_blog": "https://forbetterscience.com/2024/01/02/dana-farberications-at-harvard-university/",
        },
    })

    # ---- Q17: SHA-256 sign-off ----
    digest = hashlib.sha256((final / "summary.json").read_bytes()).hexdigest()
    _w(final / "summary.json.sha256", f"VERIFIED:{digest}\n")


# --------------------------------------------------------------------------- #
# Run checks
# --------------------------------------------------------------------------- #
EVAL_CMDS = {
    "q1": ["check_q1.py", ("pref", "P3", "reports/wip/index.json")],
    "q2": ["check_q2.py", ("pref", "P3", "reports/wip/papers_meta.json")],
    "q3": ["check_q3.py", ("pref", "P3", "reports/wip/glimcher_retraction_record.json")],
    "q4": ["check_q4.py", ("pref", "P3", "reports/wip/ghobrial_image_analysis.json")],
    "q5": ["check_q5.py", ("pref", "P3", "reports/wip/anderson_blot_summary.json")],
    "q6": ["check_q6.py", ("pref", "P3", "reports/wip/discrepancy_conflict_record.json")],
    "q7": ["check_q7.py", ("pref", "P1,P2,P4", "reports/wip/2024-01-02_dfci_preliminary.md")],
    "q8": ["check_q8.py", ("pref", "P3", "reports/wip/nih_grants_summary.json")],
    "q9": ["check_q9.py", ("pref", "P3", "reports/wip/integrity_matrix.json")],
    "q10": ["check_q10.py"],
    "q11": ["check_q11.py"],
    "q12": ["check_q12.py", ("pref", "P3", "reports/wip/papers_update_record.json")],
    "q13": ["check_q13.py"],
    "q14": ["check_q14.py"],
    "q15": ["check_q15.py", ("pref", "P1,P2,P4", "reports/final/2024-01-02_dfci_final_report.md")],
    "q16": ["check_q16.py", ("pref", "P3", "reports/final/summary.json")],
    "q17": ["check_q17.py"],
}


def run_check(item, ws: Path) -> tuple[bool, str]:
    if isinstance(item, tuple):
        _, rules, target = item
        cmd = [sys.executable, str(SCRIPTS / "check_preferences.py"),
               str(ws), "--rules", rules, "--target", target]
    else:
        cmd = [sys.executable, str(SCRIPTS / item), str(ws)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    out = (r.stdout + r.stderr).strip()
    last = out.splitlines()[-1] if out.splitlines() else ""
    return r.returncode == 0, last


def main():
    ws = prep_workspace()
    solve(ws)
    print("=== GOLD SOLUTION: every check must PASS ===")
    n_pass = n_fail = 0
    for q, items in EVAL_CMDS.items():
        for it in items:
            ok, last = run_check(it, ws)
            tag = "pref " + it[1] if isinstance(it, tuple) else "main"
            if ok:
                n_pass += 1
                print(f"  [PASS] {q} ({tag}): {last}")
            else:
                n_fail += 1
                print(f"  [FAIL] {q} ({tag}): {last}")
    print(f"\ngold: {n_pass} checks PASSED, {n_fail} FAILED")

    # 反例抽样（须全 FAIL）
    print("\n=== NEGATIVE PROBES: each must FAIL ===")
    probes = 0
    caught = 0

    # Negative 1: Q3 wrong figure — use "Fig. 2C" instead of Fig. 1A and Fig. 6A
    _wj(ws / "reports" / "wip" / "glimcher_retraction_record.json", {
        "schema_version": "1.0",
        "original_doi": "10.1126/science.1123480",
        "retraction_doi": "10.1126/science.adp1104",
        "publication_year": 2006,
        "figures_with_issues": ["Fig. 2C"],
        "note": "Wrong figure label",
    })
    ok, _ = run_check("check_q3.py", ws); probes += 1; caught += (not ok)
    print(f"  q3 wrong figure Fig.2C -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Negative 2: Q4 wrong DOI for ghobrial
    _wj(ws / "reports" / "wip" / "ghobrial_image_analysis.json", {
        "schema_version": "1.0",
        "paper_doi": "10.1182/blood-2008-00-WRONG",
        "total_pairs": 8,
        "duplicate_count": 6,
        "max_similarity_score": 0.992,
    })
    ok, _ = run_check("check_q4.py", ws); probes += 1; caught += (not ok)
    print(f"  q4 wrong DOI -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Negative 3: Q6 ResearchBot artefact 89 used as institutional count
    _wj(ws / "reports" / "wip" / "discrepancy_conflict_record.json", {
        "schema_version": "1.0",
        "institutional_discrepancy_count": 89,
        "independent_discrepancy_count": 47,
        "source_blog": "https://forbetterscience.com/2024/01/02/dana-farberications-at-harvard-university/",
        "conflict_explanation": "Using bot artefact value",
    })
    ok, _ = run_check("check_q6.py", ws); probes += 1; caught += (not ok)
    print(f"  q6 bot artefact 89 as institutional -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Negative 4: Q13 researcher_label still William_Hahn (supersede not applied)
    blot_rows_bad = [
        {"paper_doi": "10.1038/nm.3867", "journal": "Nature Medicine", "year": "2015",
         "figure_pair": "Fig.1B-vs-Fig.2B", "reuse_count": "2",
         "researcher_label": "William_Hahn", "verdict": "DUPLICATE"},
    ]
    blot_tsv_path = ws / "cases" / "dfci" / "image_analysis" / "anderson_blot_analysis.tsv"
    import csv as _csv
    with blot_tsv_path.open("w", encoding="utf-8", newline="") as fh:
        writer = _csv.DictWriter(fh, fieldnames=list(blot_rows_bad[0].keys()), delimiter="\t")
        writer.writeheader()
        writer.writerows(blot_rows_bad)
    ok, _ = run_check("check_q13.py", ws); probes += 1; caught += (not ok)
    print(f"  q13 William_Hahn label (supersede not applied) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Negative 5: Q17 placeholder hash
    _w(ws / "reports" / "final" / "summary.json.sha256",
       "VERIFIED:" + "0" * 64 + "\n")
    ok, _ = run_check("check_q17.py", ws); probes += 1; caught += (not ok)
    print(f"  q17 placeholder hash -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    print(f"\nnegatives: {caught}/{probes} correctly caught")

    if n_fail == 0 and caught == probes:
        print("\nAUDIT OK: gold solution all-PASS and all negative probes caught.")
    else:
        print("\nAUDIT PROBLEM: see failures above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
