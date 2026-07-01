#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_sci1a.py — 生成 ClawArena 真实数据集场景 sci1a
（DFCI 图像操纵专项核查 — Dana-Farber Cancer Institute 2024 案）。

题材与锚点取材真实（For Better Science 博客 / Retraction Watch 和解报道 / Science 撤稿声明），
session 对话与 workspace 文档围绕真实锚点合成。全 exec_check，17 轮，2 次 update（含 supersede）。

幂等：每次运行先清空 sci1a 的 workspace/state/updates 后重建，再写 _register.json。
questions.json 与 check 脚本由 eval/sci1a/ 下静态文件提供，本脚本不生成它们。

运行：python scripts/clawarena_authoring/build_sci1a.py
"""
from __future__ import annotations

import csv
import io
import json
import random
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    SessionBuilder, append_history, dump_register_meta,
    est_tokens, gen_session_id,
)

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DATASET = REPO / "data" / "clawarena-real"
TID = "sci1a"
CWD = f"/workspace/{TID}"
OC = DATASET / "openclaw"
WS = OC / "workspaces" / TID
SESS = OC / "state" / "agents" / TID / "sessions"
UPD = OC / "updates" / TID


def w(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def wj(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
# 1. 系统文件（OpenClaw agent 启动文件）
# --------------------------------------------------------------------------- #
def gen_system_files() -> None:
    w(WS / "AGENTS.md", """# Agent Startup Procedure — Research Integrity Office (RIO)

1. Read `SOUL.md` to understand your professional principles and source hierarchy.
2. Read `USER.md` to learn about the people and channels you interact with.
3. Run `exec ls -R` to inspect the current workspace files.
4. Use `sessions_list` to see all available history sessions.
5. Use `sessions_history` to read relevant session content as needed.

You are a Senior Research Integrity Analyst at the Research Integrity Office (RIO),
assigned to lead the DFCI image-manipulation investigation (Dana-Farber Cancer Institute, 2024).
Your primary duties: analyse flagged papers, produce COPE-compliant case records, and
coordinate with journal editors, legal counsel, and NIH ORI.
""")

    w(WS / "SOUL.md", """# Working Principles — Senior Research Integrity Analyst

1. **Source hierarchy**: Peer-reviewed retraction notices and official institutional/legal
   documents take precedence over blog posts or auto-generated summaries. When two sources
   conflict, cite both and state which is authoritative for the specific fact cited.

2. **Verbatim precision**: DOIs, figure labels, and statutory references must be quoted
   verbatim as they appear in the primary source. Paraphrasing DOIs or figure numbers
   is a documentation defect.

3. **Schema discipline**: Every JSON deliverable carries a top-level `schema_version`
   field set to `"1.0"`. The RIO case-management system rejects untagged files.

4. **Report structure**: All formal case reports follow the four-section RIO template:
   Background / Evidence / Classification / Recommendation. Omitting any section voids
   the report for COPE submission.

5. **Executive-summary length**: The Abstract / Executive Summary section of any report
   must not exceed 300 words. Legal review enforces this limit.

6. **Retraction-entry completeness**: Each retracted paper must list both the original
   DOI and the retraction-notice DOI separately. Co-citing them as a single entry is
   insufficient for the case record.

7. **Supersede discipline**: When a later document revokes an earlier instruction or
   finding, the earlier document must be explicitly labelled "SUPERSEDED" in the case log.
   Acting on a superseded document is a procedural breach.
""")

    w(WS / "USER.md", """# People and Channels — DFCI Case Team

## Primary User
- **Dr. Margaret Foster** — Director, Research Integrity Office. Assigns tasks, reviews reports.
  Strict on COPE compliance, four-section structure, and 300-word abstract limit. Communicates via
  main session and email.

## Key Contacts

| Name | Role | Channel | Notes |
|---|---|---|---|
| Sholto David | Independent researcher (whistleblower) | Discord #paper-sleuth | Provides raw image analysis; his blog is the primary public record (S1) |
| Dr. Elena Vasquez | RIO Legal Counsel | Email | Issues official memos; supersede notices |
| James Park | RIO Data Analyst | Slack #rio-general | Assists with data downloads, statistical queries |
| Dr. Liu Wei | NIH ORI Liaison | Email | Formal investigation communications |
| ResearchBot | Automated summarisation tool | Feishu #sci-integrity | Known to produce inaccurate participant counts — NOT authoritative |

## Source Hierarchy
1. Peer-reviewed retraction notices (Science, Nature Medicine, Blood)
2. Legal / DOJ settlement documents (S2: Retraction Watch 2025-12)
3. NIH ORI formal notices
4. Institutional statements (DFCI)
5. For Better Science blog (S1) — blog, useful but not peer-reviewed
6. Feishu ResearchBot summaries — **not authoritative, known errors**

## Channels
- **Main session**: director-level task assignments, formal report review
- **Slack #rio-general**: James Park day-to-day coordination
- **Email**: legal counsel (Elena Vasquez), NIH ORI (Liu Wei), journal editors
- **Discord #paper-sleuth**: Sholto David — raw image analysis data
- **Feishu #sci-integrity**: team discussion + ResearchBot summaries (treat with caution)
""")

    w(WS / "IDENTITY.md", """# Identity

You are a **Senior Research Integrity Analyst** deployed by the Research Integrity Office (RIO)
to lead the DFCI image-manipulation case investigation.

Your deliverables include:
- Structured case records (JSON + Markdown) conforming to the COPE Retraction Guidelines
- Pixel-level image analysis reports (TSV) cross-checking DFCI institutional claims
- A final summary JSON (signed with SHA-256) integrating all findings

Source files and reference documents under `cases/` and `protocols/` are authoritative read-only
inputs. Write your deliverables to `reports/wip/` and `reports/final/`.
""")

    w(WS / "TOOLS.md", """# Available Tools

| Tool | Purpose |
|---|---|
| `sessions_list` | List all available history sessions |
| `sessions_history` | Read a specific history session |
| `read` | Read a workspace file |
| `exec` | Execute a shell command (write deliverables, run analysis) |

## Rules
- Source files under `cases/` and `protocols/` are **read-only** inputs.
- Deliver outputs under `reports/wip/` (draft) and `reports/final/` (finalised).
- In history sessions, use `read` and `exec` only; do not call `sessions_list`/`sessions_history` there.
""")


# --------------------------------------------------------------------------- #
# 2. Reference 数据与真实锚点文件
# --------------------------------------------------------------------------- #
def gen_reference() -> None:
    # 2.1 papers_flagged.csv — 初始 58 篇论文（真实锚点，BRIEF S1）
    rng = random.Random(2024)
    issue_types = [
        "western_blot_manipulation", "image_duplication", "western_blot_manipulation",
        "image_duplication", "mouse_figure_fabrication", "image_duplication",
        "western_blot_manipulation", "image_duplication",
    ]
    journals = [
        "Cancer Cell", "Blood", "Nature Medicine", "Science", "Nature",
        "Journal of Clinical Oncology", "Leukemia", "Oncogene",
        "Cell", "Molecular Cell", "Experimental Hematology",
    ]
    researchers = ["Glimcher", "Hahn", "Ghobrial", "Anderson"]
    rows_58 = [["doi", "journal", "year", "lead_author", "issue_type", "researcher_group", "flagged_by"]]
    # 真实锚点 DOIs 必须在列
    anchor_entries = [
        ["10.1038/nm.3867", "Nature Medicine", 2015, "Anderson KC", "western_blot_manipulation", "Anderson", "Sholto_David"],
        ["10.1182/blood-2008-10-186668", "Blood", 2009, "Ghobrial IM", "mouse_figure_fabrication", "Ghobrial", "Sholto_David"],
        ["10.1038/22780", "Nature", 1999, "Hahn WC", "image_duplication", "Hahn", "Sholto_David"],
        ["10.1126/science.1123480", "Science", 2006, "Glimcher LH", "image_duplication", "Glimcher", "Sholto_David"],
        ["10.1016/j.ccr.2007.02.015", "Cancer Cell", 2007, "Anderson KC", "western_blot_manipulation", "Anderson", "Sholto_David"],
    ]
    for entry in anchor_entries:
        rows_58.append(entry)
    # 合成其余 53 行
    used_dois = {e[0] for e in anchor_entries}
    synthetic_count = 0
    while synthetic_count < 53:
        year = rng.randint(1998, 2022)
        doi_sfx = "".join([str(rng.randint(0, 9)) for _ in range(7)])
        doi_prefix = rng.choice(["10.1182/bld", "10.1016/j.ccr", "10.1038/nm",
                                  "10.1182/blood", "10.1126/sci", "10.1002/jco"])
        doi = f"{doi_prefix}.{doi_sfx}"
        if doi in used_dois:
            continue
        used_dois.add(doi)
        author_last = rng.choice(["Anderson", "Hahn", "Ghobrial", "Glimcher",
                                   "Carrasco", "Mitsiades", "Munshi", "Richardson"])
        issue = rng.choice(issue_types)
        researcher = rng.choice(researchers)
        journal = rng.choice(journals)
        rows_58.append([doi, journal, year, f"{author_last} et al.", issue, researcher, "Sholto_David"])
        synthetic_count += 1

    buf = io.StringIO()
    csv.writer(buf).writerows(rows_58)
    w(WS / "cases" / "dfci" / "papers_flagged.csv", buf.getvalue())

    # 2.2 case_summary.md — 初始版本（58 篇，明确锚点）
    w(WS / "cases" / "dfci" / "case_summary.md", """# DFCI Image Manipulation Case — Case Summary (Initial)

**Case ID**: DFCI-2024-001
**Date Opened**: 2024-01-15
**Status**: Active Investigation

## Incident Overview

On 2024-01-02, independent researcher Sholto David published a detailed analysis on the blog
*For Better Science* (https://forbetterscience.com/2024/01/02/dana-farberications-at-harvard-university/)
identifying image manipulation across multiple papers from Dana-Farber Cancer Institute (DFCI).

Initial scope: **58 papers** flagged across four research groups (Glimcher, Hahn, Ghobrial, Anderson).

## Key Papers Identified (Initial)

| DOI | Journal | Year | Issue |
|-----|---------|------|-------|
| 10.1126/science.1123480 | Science | 2006 | Image duplication (Fig. 1A, Fig. 6A) |
| 10.1038/nm.3867 | Nature Medicine | 2015 | Western blot manipulation |
| 10.1182/blood-2008-10-186668 | Blood | 2009 | Mouse figure fabrication |
| 10.1038/22780 | Nature | 1999 | Image duplication (>3000 citations) |

## Institutional Response (Preliminary)

DFCI announced:
- **6 retractions** across affected research groups
- **31 corrections** issued or in progress

## Notes

- Researcher 1 identity: **[PENDING CLARIFICATION]** (see internal_memo_v1.md)
- Settlement discussions with DOJ: ongoing as of case opening date
""")

    # 2.3 blog_post_mirror.md — For Better Science 博客镜像（长文，锚点丰富）
    blog_content = """# Dana-Farberications at Harvard University
*Posted by Sholto David on For Better Science, 2024-01-02*
*Source: https://forbetterscience.com/2024/01/02/dana-farberications-at-harvard-university/*

---

## Overview

This post documents extensive image manipulation across **58 papers** from Dana-Farber Cancer
Institute (DFCI), Harvard Medical School, involving four senior researchers: Laurie Glimcher
(President/CEO), William Hahn (Executive VP for Research), Irene Ghobrial, and Kenneth Anderson.

The manipulations were identified using ImageTwin and manual pixel comparison. Types include:
western blot duplication/splice, mouse experiment figure reuse, and panel rearrangement.

---

## Research Group: Glimcher (Science 2006)

**DOI: 10.1126/science.1123480** — *Proapoptotic BAX and BAK modulate the unfolded protein
response by a direct interaction with IRE1α* (2006, Science).

This paper has been retracted (retraction DOI: 10.1126/science.adp1104). The retraction notice
identifies discrepancies in **Fig. 1A and Fig. 6A** controls. Co-author Claudio Hetz did not
agree with retraction.

Analysis: Fig. 1A control lane appears identical to a panel in a separate 2005 publication.
ImageTwin similarity score: 0.987. The authors' internal review began in February 2021.

---

## Research Group: Anderson (Nature Medicine 2015)

**DOI: 10.1038/nm.3867** — *CyclophilinA is a novel regulator of MGMT in multiple myeloma* (2015).

Kenneth Anderson group. Multiple western blot panels appear duplicated across independent
experiments. The blot in Fig. 2B shows pixel-level identity with a panel in Fig. 4D of the same
paper, consistent with copy-paste rather than independent replication.

Anderson's research group also produced:
- **DOI: 10.1016/j.ccr.2007.02.015** (Cancer Cell 2007): Blot panels inverted and re-used.

For the settlement document, Kenneth Anderson is designated as **Researcher 1** (14 papers).

---

## Research Group: Ghobrial (Blood 2009)

**DOI: 10.1182/blood-2008-10-186668** — *CXCR4 regulates migration and development of human
plasmacytoid dendritic cell precursors in mouse models* (Blood 2009).

Mouse experiment figures in this paper are **near-entirely fabricated** according to the analysis.
ImageTwin analysis reveals that 6 of 8 lane comparison pairs show similarity > 0.95.
At least one image pair has been traced to an entirely different experimental context.

---

## Research Group: Hahn (Nature 1999)

**DOI: 10.1038/22780** — *Creation of human tumour cells with defined genetic elements* (1999).

This paper has accumulated **>3000 citations** and is a foundational oncology reference.
Image concerns were raised during the 2024 investigation. Corrections have been issued.

---

## Methodology

ImageTwin (https://imagetwin.ai) was used for automated duplicate detection. Manual review
confirmed all high-confidence flags. Pixel-level analysis was performed at 300 DPI resolution.

The blog identified a total of **58 papers** in the initial analysis. Subsequent institutional
and legal review has expanded this count.

---

## Discrepancy Note (V1 Multi-source Conflict)

DFCI's internal ImageTwin report claims **discrepancy_count = 12** at institutional level.
However, this blog's independent analysis identified **47 distinct image-pair anomalies**
across the same paper corpus. The DFCI number reflects only cases where the institution
acknowledged a discrepancy; the blog number includes all flagged pairs regardless of
institutional acknowledgement.

**For this investigation, the blog URL is the authoritative source for initial discrepancy
identification**: https://forbetterscience.com/2024/01/02/dana-farberications-at-harvard-university/

---

## Appendix: Full Paper List (Initial 58)

See `papers_flagged.csv` for the complete machine-readable list of 58 flagged papers with
DOI, journal, year, lead author, and issue type.

---

*End of blog mirror. All figures described above are available through the original post.*
"""
    # 多次重复博客内容以达到约 60KB 体量
    blog_extended = blog_content * 8 + "\n\n---\n\n## Extended Analysis Archive\n\n"
    for i in range(1, 120):
        blog_extended += f"""### Paper Analysis #{i + 5}

Additional flagged paper analysis #{i + 5}: Cross-referencing pixel data shows similarity
patterns consistent with systematic image reuse. Analysis timestamp: 2024-01-{(i % 28) + 1:02d}.
ImageTwin batch result ID: IT-2024-{1000 + i:04d}. Confidence: HIGH.

"""
    w(WS / "cases" / "dfci" / "blog_post_mirror.md", blog_extended)

    # 2.4 retraction notices
    w(WS / "cases" / "dfci" / "retraction_notices" / "glimcher_science_2006.md", """# Retraction Notice: Science 2006 — Glimcher et al.

**Retraction DOI**: 10.1126/science.adp1104
**Original Paper DOI**: 10.1126/science.1123480
**Original Publication Year**: 2006
**Journal**: Science
**Original Title**: Proapoptotic BAX and BAK modulate the unfolded protein response by a
direct interaction with IRE1α

## Retraction Statement

The editors of *Science* retract this article following an investigation by Dana-Farber Cancer
Institute that identified discrepancies in the control panels of **Fig. 1A and Fig. 6A**.
The institution's internal review, initiated in February 2021, concluded that the controls
shown in these figures do not represent the independent experiments described.

Co-author Claudio Hetz did not agree with the decision to retract.

Laurie H. Glimcher (corresponding author) and the remaining co-authors agreed to retraction.

## COPE Classification

This retraction falls under COPE guidelines for **Type 4: Unreliable findings** due to image
manipulation, and potentially **Type 2: Research misconduct** pending final institutional findings.

## RIO Notes

- Fig. 1A: control band appears duplicated from an earlier 2005 publication
- Fig. 6A: controls discrepancy — pixel analysis shows copy-paste artefacts
- Original paper accumulated approximately 500 citations
- Internal review timeline: February 2021 → retraction notice 2024
""")

    w(WS / "cases" / "dfci" / "retraction_notices" / "anderson_natmed_2015.md", """# Correction/Retraction Notice: Nature Medicine 2015 — Anderson et al.

**Paper DOI**: 10.1038/nm.3867
**Journal**: Nature Medicine
**Year**: 2015
**Lead Researcher**: Kenneth C. Anderson (Researcher 1 per settlement)

## Notice

Nature Medicine issued a correction notice following institutional review. Western blot panels
in Fig. 2B and Fig. 4D were identified as duplicates. The corresponding author agreed that an
error occurred in figure assembly.

## RIO Notes

- researcher_label: Researcher_1 (per settlement agreement)
- Reuse pattern: Fig. 2B identical to Fig. 4D at pixel level
- Issue type: western_blot_manipulation
""")

    w(WS / "cases" / "dfci" / "retraction_notices" / "ghobrial_blood_2009.md", """# Retraction Notice: Blood 2009 — Ghobrial et al.

**Paper DOI**: 10.1182/blood-2008-10-186668
**Journal**: Blood (ASH)
**Year**: 2009
**Lead Researcher**: Irene M. Ghobrial

## Analysis Summary

Mouse experiment figures in this paper are described in independent analysis as
"near entirely fabricated." ImageTwin analysis reveals similarity scores > 0.95 for
6 of 8 lane comparison pairs.

At least one panel has been traced to an entirely different experimental context
(cross-paper contamination).

## RIO Notes

- Issue type: mouse_figure_fabrication
- Similarity threshold used: 0.95
- Verdict: DUPLICATE for ≥ 6 image pairs
- Reference blog: https://forbetterscience.com/2024/01/02/dana-farberications-at-harvard-university/
""")

    w(WS / "cases" / "dfci" / "retraction_notices" / "hahn_nature_1999.md", """# Correction Notice: Nature 1999 — Hahn et al.

**Paper DOI**: 10.1038/22780
**Journal**: Nature
**Year**: 1999
**Lead Researcher**: William C. Hahn
**Citation Count**: >3000

## Notice

A correction was issued for this paper, which is a foundational oncology reference.
Image concerns were identified during the 2024 DFCI investigation.

## RIO Notes

- High-impact paper: >3000 citations
- Issue type: image_duplication
- Correction (not full retraction) as of case opening
""")

    # 2.5 institution_response
    w(WS / "cases" / "dfci" / "institution_response" / "dfci_statement_jan22.md", """# DFCI Official Statement — 2024-01-22

Dana-Farber Cancer Institute issued the following statement on 2024-01-22:

> "DFCI takes all concerns about research integrity extremely seriously. Following a thorough
> internal review initiated in early 2021, we have determined that a number of papers require
> retraction or correction. We are committed to full transparency with our journal partners
> and the broader scientific community."

## Announced Actions (as of 2024-01-22)

- **6 retractions** — papers with irreparably compromised findings
- **31 corrections** — papers with identified issues that can be addressed through errata

## Notes

This statement does not specify the total number of papers under investigation. See
`blog_post_mirror.md` for the 58-paper initial scope from the independent analysis.
The institutional figure for acknowledged discrepancies differs from the independent tally.

Source: DFCI media communications, January 2024.
""")

    w(WS / "cases" / "dfci" / "institution_response" / "dfci_internal_review.md", """# DFCI Internal Review Report (Synthetic Summary)

**Report Date**: 2024-03-15 (synthetic — based on publicly available information)
**Prepared by**: DFCI Research Integrity Committee
**Classification**: Internal Use Only

## Executive Summary

DFCI's internal review examined papers from four research groups identified by the independent
analysis of Sholto David (For Better Science blog, 2024-01-02).

## Findings

### ImageTwin Institutional Scan Results

DFCI commissioned an institutional ImageTwin scan. The internal report records:
- **discrepancy_count**: 12 (cases where DFCI's review panel acknowledged a discrepancy)
- Scan coverage: 58 papers identified in the independent analysis

**Note**: The independent analysis (S1 blog) identified 47 distinct image-pair anomalies.
The DFCI institutional count (12) reflects only cases formally acknowledged in internal review.
For RIO purposes, treat the blog source as the basis for initial discrepancy identification.

### Settlement Context

Settlement discussions with the Department of Justice (DOJ) were ongoing. The institution
acknowledged involvement of at minimum:
- Researcher 1: [identity pending public confirmation] — 14 papers
- Researcher 2: Ruben Carrasco — additional papers

### Correction/Retraction Summary

- Retractions announced: 6
- Corrections announced: 31

---

*This document synthesises publicly available information for RIO case record purposes.*
""")

    # 2.6 image_analysis（合成 TSV，含真实锚点）
    # ghobrial_mouse_analysis.tsv
    rng2 = random.Random(2025)
    tsv_rows = [["image_pair", "similarity_score", "verdict", "paper_doi", "notes"]]
    # 保证至少 6 行 DUPLICATE，similarity > 0.95，且含真实 DOI
    for i in range(1, 9):
        sim = round(rng2.uniform(0.96, 0.999), 4) if i <= 6 else round(rng2.uniform(0.60, 0.89), 4)
        verdict = "DUPLICATE" if sim > 0.95 else "SIMILAR"
        tsv_rows.append([
            f"pair_{i:02d}",
            sim,
            verdict,
            "10.1182/blood-2008-10-186668",
            f"Fig.{i}A vs Fig.{i}B pixel comparison",
        ])
    buf2 = io.StringIO()
    csv.writer(buf2, delimiter="\t").writerows(tsv_rows)
    w(WS / "cases" / "dfci" / "image_analysis" / "ghobrial_mouse_analysis.tsv", buf2.getvalue())

    # anderson_blot_analysis.tsv — 初始版（researcher_label 故意模糊为 Researcher_1）
    rng3 = random.Random(2026)
    blot_rows = [["paper_doi", "journal", "year", "figure_pair", "reuse_count",
                  "researcher_label", "verdict"]]
    anderson_dois = [
        "10.1038/nm.3867", "10.1016/j.ccr.2007.02.015",
    ]
    for doi in anderson_dois:
        for fig_idx in range(1, 5):
            reuse = rng3.randint(1, 4)
            blot_rows.append([
                doi, "Cancer Cell" if "ccr" in doi else "Nature Medicine",
                2007 if "ccr" in doi else 2015,
                f"Fig.{fig_idx}B-vs-Fig.{fig_idx + 1}B",
                reuse,
                "Researcher_1",   # 初始版：label 用代号，update2 后须改为 Kenneth_C._Anderson
                "DUPLICATE" if reuse >= 2 else "SIMILAR",
            ])
    buf3 = io.StringIO()
    csv.writer(buf3, delimiter="\t").writerows(blot_rows)
    w(WS / "cases" / "dfci" / "image_analysis" / "anderson_blot_analysis.tsv", buf3.getvalue())

    # imagetwin_report.json — 含真实 URL 锚点（discrepancy_count 取机构值 12，非博客值 47）
    wj(WS / "cases" / "dfci" / "image_analysis" / "imagetwin_report.json", {
        "schema_version": "1.0",
        "scan_date": "2024-02-10",
        "tool": "ImageTwin",
        "source_blog": "https://forbetterscience.com/2024/01/02/dana-farberications-at-harvard-university/",
        "papers_scanned": 58,
        "discrepancy_count": 12,
        "note_conflict": (
            "DFCI institutional scan acknowledges 12 discrepancies; independent blog analysis "
            "identified 47 image-pair anomalies. The institutional count (12) reflects only "
            "formally acknowledged cases. The blog figure (47) is the independent tally. "
            "The Slack bot summary inflated this to 89 — treat as INCORRECT (V5 decoy)."
        ),
        "high_confidence_duplicates": [
            {"paper_doi": "10.1182/blood-2008-10-186668", "pair": "pair_01", "score": 0.992},
            {"paper_doi": "10.1038/nm.3867", "pair": "pair_01", "score": 0.978},
            {"paper_doi": "10.1126/science.1123480", "pair": "pair_01", "score": 0.987},
        ],
    })

    # grant_records
    rng4 = random.Random(2027)
    grant_rows = [["grant_id", "pi_last", "nih_institute", "amount_usd", "fiscal_year",
                   "project_title", "associated_paper_doi"]]
    for i in range(1, 151):
        grant_rows.append([
            f"R01CA{100000 + i}",
            rng4.choice(["Anderson", "Hahn", "Ghobrial", "Glimcher"]),
            rng4.choice(["NCI", "NHLBI", "NIAID"]),
            rng4.randint(250000, 1200000),
            rng4.randint(2001, 2022),
            f"Cancer research project #{i}",
            f"10.1182/bld.{2000000 + i}",
        ])
    buf4 = io.StringIO()
    csv.writer(buf4).writerows(grant_rows)
    w(WS / "cases" / "dfci" / "grant_records" / "nih_grants_list.csv", buf4.getvalue())

    # 2.7 image_analysis_full_corpus.tsv — 完整语料图像分析（大体量合成，~40KB TSV）
    rng_big = random.Random(9001)
    full_corpus_rows = [["paper_id", "paper_doi", "researcher_group", "journal", "year",
                          "fig_pair", "similarity_score", "verdict", "method",
                          "review_status", "notes"]]
    all_dois_corpus = [
        "10.1038/nm.3867", "10.1182/blood-2008-10-186668",
        "10.1038/22780", "10.1126/science.1123480",
        "10.1016/j.ccr.2007.02.015",
    ]
    # 合成 350 行完整语料
    for i in range(350):
        doi = rng_big.choice(all_dois_corpus) if i < 20 else (
            f"10.1182/bld.{9000000 + i}"
        )
        researcher = rng_big.choice(["Glimcher", "Hahn", "Ghobrial", "Anderson"])
        journal = rng_big.choice(["Blood", "Cancer Cell", "Nature Medicine", "Science",
                                   "Leukemia", "PNAS", "Oncogene", "Molecular Cell"])
        year = rng_big.randint(1998, 2022)
        sim = round(rng_big.uniform(0.45, 0.999), 4)
        verdict = "DUPLICATE" if sim > 0.95 else ("SIMILAR" if sim > 0.80 else "DISTINCT")
        status = rng_big.choice(["reviewed", "pending", "confirmed", "disputed"])
        full_corpus_rows.append([
            f"PID-{i + 1:04d}", doi, researcher, journal, year,
            f"Fig.{rng_big.randint(1, 8)}{rng_big.choice(['A','B','C','D'])}"
            f"-vs-Fig.{rng_big.randint(1, 8)}{rng_big.choice(['A','B','C','D'])}",
            sim, verdict, "ImageTwin_v2.1", status,
            f"Batch analysis #{i // 50 + 1}, scan date 2024-{(i % 12) + 1:02d}-15"
        ])
    buf_big = io.StringIO()
    csv.writer(buf_big, delimiter="\t").writerows(full_corpus_rows)
    w(WS / "cases" / "dfci" / "image_analysis" / "full_corpus_analysis.tsv", buf_big.getvalue())

    # 2.8 detailed_paper_analyses/ — 每篇被点名论文的详细分析（4篇 × ~10KB = ~40KB）
    for doi, title, researcher, year, details in [
        ("10.1126/science.1123480",
         "Proapoptotic BAX and BAK modulate the unfolded protein response by a direct interaction with IRE1alpha",
         "Glimcher", 2006,
         "Science 2006 paper. Fig. 1A: control lane duplicated from 2005 companion paper. "
         "Fig. 6A: control shows pixel-level identity with Fig. 3B of same paper. "
         "ImageTwin scan: pair score 0.987. Manual confirmation: copy-paste artefact confirmed. "
         "Hetz (co-author) disputed findings — rare disagreement in retraction notices."),
        ("10.1038/nm.3867",
         "CyclophilinA is a novel regulator of MGMT expression in multiple myeloma",
         "Anderson", 2015,
         "Nature Medicine 2015 paper. Fig. 2B identical to Fig. 4D at pixel level. "
         "Western blot panel shows characteristic splicing artefacts. "
         "ImageTwin score: 0.978. Manual: copy-paste with brightness adjustment confirmed. "
         "Anderson group; Researcher 1 identity confirmed December 2025."),
        ("10.1182/blood-2008-10-186668",
         "CXCR4 regulates migration and development of human plasmacytoid dendritic cell precursors in mouse models",
         "Ghobrial", 2009,
         "Blood 2009 paper. 6 of 8 mouse experiment image pairs exceed 0.95 similarity. "
         "Pair_01 through Pair_06: DUPLICATE verdict. Pair_07: SIMILAR. Pair_08: SIMILAR. "
         "At least one panel traced to different experimental context (cross-paper). "
         "Near-entirely fabricated per independent analysis."),
        ("10.1038/22780",
         "Creation of human tumour cells with defined genetic elements",
         "Hahn", 1999,
         "Nature 1999 paper. >3000 citations. Foundational oncology reference. "
         "Image concerns identified during 2024 investigation. "
         "Correction (not retraction) issued — core findings partially replicable. "
         "Impact: foundational status means correction affects large downstream literature."),
    ]:
        content = f"""# Detailed Paper Analysis

**DOI**: {doi}
**Title**: {title}
**Researcher Group**: {researcher}
**Publication Year**: {year}
**Journal**: {"Science" if "science" in doi else ("Nature Medicine" if "nm.3867" in doi else ("Blood" if "blood" in doi else "Nature"))}

---

## Image Analysis Summary

{details}

---

## Detailed Pixel Comparison Notes

"""
        for p_i in range(1, 9):
            content += f"""### Pair {p_i:02d}

Analysis of panel pair {p_i:02d} for this paper. ImageTwin scan performed at 300 DPI resolution
using the standard institutional protocol (see `protocols/image_analysis_sop.md`).

Comparison methodology: panels exported to PNG, CMYK colour space normalised to sRGB,
aligned using affine transformation, difference image computed.

Results:
- Similarity score (pixel overlap): computed from ImageTwin batch analysis
- Manual review: completed by primary analyst and independent reviewer
- Artefact flags: brightness/contrast adjustments, potential JPEG re-compression

"""
        # Add a lot more padding to bulk up
        content += "\n---\n\n## Full Pixel Difference Report (Extended)\n\n"
        for row_i in range(1, 120):
            content += (
                f"Row {row_i:03d}: pixel value comparison at y={row_i * 4}px — "
                f"channel_R delta={random.Random(row_i).randint(0, 12)}, "
                f"channel_G delta={random.Random(row_i + 1000).randint(0, 8)}, "
                f"channel_B delta={random.Random(row_i + 2000).randint(0, 15)}. "
                f"Cumulative deviation index: {round(random.Random(row_i + 3000).uniform(0.001, 0.045), 4)}.\n"
            )
        safe_doi = doi.replace("/", "_").replace(".", "-")
        w(WS / "cases" / "dfci" / "image_analysis" / "detailed" / f"analysis_{safe_doi}.md", content)

    # 2.9 extended_communications — 大体量通讯记录（~80KB）
    # Extended Slack archive (historical messages)
    slack_archive = []
    for i in range(1200):
        user = ["james_park", "dr_foster", "analyst_jr", "rio_admin"][i % 4]
        slack_archive.append(json.dumps({
            "ts": f"2024-{(i % 11) + 1:02d}-{(i % 28) + 1:02d}T{(i % 12) + 8:02d}:00:00Z",
            "user": user,
            "text": (
                f"[Slack #rio-general {user.replace('_', ' ').title()} 2024] "
                f"Case DFCI-2024-001 working note #{i + 100}: "
                f"cross-referencing paper batch {i // 20 + 1}, "
                f"verifying DOI integrity and COPE compliance for batch member {i % 20 + 1}. "
                f"Analyst: confirming issue_type classification for papers {i * 2 + 1}-{i * 2 + 2}. "
                f"Status: {'reviewed' if i % 3 == 0 else ('pending' if i % 3 == 1 else 'confirmed')}."
            ),
        }, ensure_ascii=False))
    w(WS / "communications" / "slack" / "channel_archive_2024.jsonl",
      "\n".join(slack_archive) + "\n")

    # Extended email archive
    email_archive = ""
    for i in range(80):
        email_archive += f"""From: contact-{i}@journal-{i % 10}.edu
To: analyst@university.edu
Date: 2024-{(i % 11) + 1:02d}-{(i % 28) + 1:02d}
Subject: RE: DFCI case inquiry #{i + 1}

Dear Research Integrity Analyst,

Thank you for your inquiry regarding paper reference DFCI-{i + 1:04d} in the current
investigation (case DFCI-2024-001).

We have reviewed our records and can confirm the following:
- The paper identified by your office was published in our journal in year {2000 + i % 23}.
- The editorial office has been in contact with the corresponding author regarding
  the image manipulation concerns raised by the independent analysis.
- Journal policy requires us to follow COPE guidelines for any retraction or correction process.
- We are cooperating fully with your office and with the institutional review.

Please note that all communications regarding this matter should reference case ID DFCI-2024-001.
If you require certified copies of the original submission files or peer review correspondence,
please submit a formal records request to our editorial office.

Best regards,
Journal Editorial Office {i % 10 + 1}
Contact: editorial-{i % 10}@journal-{i % 10}.edu

---

"""
    w(WS / "communications" / "email" / "journal_correspondence_archive.mbox", email_archive)

    # Extended Discord archive (Sholto David extended analysis)
    discord_ext = []
    for i in range(200):
        discord_ext.append(json.dumps({
            "ts": f"2024-{(i % 6) + 1:02d}-{(i % 28) + 1:02d}T{(i % 12) + 9:02d}:00:00Z",
            "user": "sholto_david",
            "text": (
                f"[Discord #paper-sleuth sholto_david 2024] "
                f"Extended analysis note #{i + 50}: "
                f"reviewing paper group {i // 15 + 1}. "
                f"ImageTwin batch {i // 20 + 1}: {'high-confidence flags detected' if i % 4 == 0 else 'low-confidence, manual review queued'}. "
                f"Total flagged so far: {i * 3 + 58}. "
                f"Blog URL authoritative: "
                f"https://forbetterscience.com/2024/01/02/dana-farberications-at-harvard-university/"
            ),
        }, ensure_ascii=False))
    w(WS / "communications" / "discord" / "channel_extended_analysis.jsonl",
      "\n".join(discord_ext) + "\n")

    # Extended Feishu archive (team discussion)
    feishu_ext = []
    for i in range(250):
        feishu_ext.append(json.dumps({
            "ts": f"2024-{(i % 11) + 1:02d}-{(i % 28) + 1:02d}T{(i % 10) + 9:02d}:00:00Z",
            "user": ["james_park", "analyst_jr", "dr_foster", "ResearchBot"][i % 4],
            "text": (
                f"[Feishu #sci-integrity {'james_park' if i % 4 == 0 else ('analyst_jr' if i % 4 == 1 else ('dr_foster' if i % 4 == 2 else 'ResearchBot AUTO-SUMMARY'))} 2024] "
                + (
                    f"Cross-referencing note #{i + 1}: batch {i // 15 + 1} papers reviewed. "
                    f"COPE compliance: {'PASS' if i % 3 != 2 else 'NEEDS_REVIEW'}. "
                    f"Schema version: 1.0 confirmed on all JSON deliverables."
                    if i % 4 != 3 else
                    f"AUTOMATED SUMMARY (not authoritative): batch {i // 15 + 1} "
                    f"heuristic count update: {i * 2 + 12} items processed. "
                    f"Note: this count generated by heuristic sampling — verify against primary sources."
                )
            ),
        }, ensure_ascii=False))
    w(WS / "communications" / "feishu" / "group_extended_archive.jsonl",
      "\n".join(feishu_ext) + "\n")

    # 2.7 internal_memo_v1 — V6 废弃副本红鲱鱼（声称 Researcher 1 = William Hahn）
    w(WS / "cases" / "dfci" / "institution_response" / "internal_memo_v1.md", """# DFCI Internal Memo — Researcher Identity (PRELIMINARY DRAFT)

**MEMO ID**: DFCI-MEMO-2024-003-v1
**Date**: 2024-03-01
**Status**: DRAFT — PRELIMINARY — NOT FOR EXTERNAL DISTRIBUTION

## Researcher 1 Identity

Based on preliminary internal analysis, the individual designated as "Researcher 1" in the
Department of Justice complaint correspondence is believed to be **William C. Hahn**
(Executive VP for Research, DFCI).

This assessment is based on the paper count matching the 14-paper subset identified in the
DOJ complaint. However, this identification is **preliminary and unconfirmed**.

---

⚠️ **THIS MEMO IS SUPERSEDED** — See `legal_memo_researcher1.md` for the authoritative
clarification issued by Legal Counsel in December 2025. The identification of Researcher 1
as William Hahn was **incorrect**. The authoritative identity is **Kenneth C. Anderson**.

Do not cite this memo as a source for Researcher 1 identity.
""")


# --------------------------------------------------------------------------- #
# 3. Protocols（长文档撑体量）
# --------------------------------------------------------------------------- #
def gen_protocols() -> None:
    # 3.1 COPE 撤稿指引（~25 KB）
    cope_text = """# COPE Retraction Guidelines (Mirror for RIO Internal Use)

Source: Committee on Publication Ethics (COPE) — https://publicationethics.org/retraction-guidelines
Version: 2019 (amended 2022). For official use, refer to the current COPE website.

---

## Preamble

Retraction is a mechanism for correcting the literature and alerting readers to publications
that contain such seriously flawed or erroneous data that their findings and conclusions cannot
be relied upon. Unreliable findings may result from honest error or research misconduct.

---

## Section 1: Circumstances for Retraction

Journals should consider issuing a retraction when:

1. **Type 1 — Honest error**: They have clear evidence of unreliable findings, even if honest
   mistake. The error significantly affects the conclusions.

2. **Type 2 — Research misconduct**: The findings are unreliable as a result of data
   fabrication or data falsification (including image manipulation).

3. **Type 3 — Plagiarism**: Prior publication in another journal without appropriate
   cross-referencing, permission, or justification.

4. **Type 4 — Unreliable findings**: Due to image manipulation, statistical errors, or
   misrepresentation of data. This covers Western blot duplication, figure splicing,
   and computer-assisted image manipulation.

---

## Section 2: Retraction Process

### 2.1 Triggering an Investigation

When a concern is raised (e.g., via post-publication peer review, blog analysis, or institutional
audit), editors should:

a) Acknowledge receipt within 2 weeks
b) Inform institutional research integrity offices
c) Consult COPE flowcharts for guidance on handling

### 2.2 Cooperative Authors

Where authors cooperate, a signed retraction notice should be agreed and published promptly.

### 2.3 Non-cooperative Authors or Institutions

Where authors or institutions do not respond or disagree with retraction, editors may still
proceed with retraction if the evidence is compelling, noting the author's disagreement.

---

## Section 3: Retraction Notice Format

Retraction notices should:

- Appear on a numbered page in a regular section of the journal
- Be linked to the original article (both directions)
- State the reason for retraction
- Identify authors who agreed and those who did not
- Not be misleadingly brief (avoid "withdrawn by authors" without explanation)

---

## Section 4: Retraction Types and RIO Classification

For the DFCI case, the following classification applies:

| Type | Description | DFCI Applicability |
|------|-------------|-------------------|
| Type 2 | Research misconduct (data fabrication/falsification) | Image duplication with intent |
| Type 4 | Unreliable findings (image manipulation, stats errors) | Western blot copy-paste |

**Primary classification for DFCI papers**: **Type 4: Unreliable findings** due to confirmed
image manipulation; **Type 2: Research misconduct** where institutional investigation confirmed
intent.

---

## Section 5: Expression of Concern

As an interim measure before full retraction:

- Expression of Concern may be issued when an investigation is ongoing
- Should be linked bidirectionally to the paper
- Must state that an investigation is ongoing
- Should be replaced with retraction or clearance notice on investigation completion

---

## Section 6: Corrections

Corrections (erratum/corrigendum) are appropriate when:

- The core findings are unaffected
- The error is a genuine honest mistake
- The correction is transparent and complete

The DFCI case used **6 retractions** and **31 corrections** — the corrections were applied to
papers where the image issues were less severe or the scientific conclusions remained valid
after corrected panels were provided.

---

## Section 7: Author Disputes

Where one or more authors dispute the retraction (as occurred with Claudio Hetz for the
Glimcher Science 2006 paper, DOI: 10.1126/science.1123480), the retraction notice should
state: "Author [Name] does not agree with this retraction."

---

## Section 8: Post-Retraction Duties

After retraction:

- Authors must not republish retracted data without full disclosure
- Citing institutions must be notified
- Funders (e.g. NIH) must be notified where grant misconduct is implicated

---

## Appendix: COPE Flowcharts (Summary)

### Flowchart A: Suspected fabricated data

1. Raise concern with corresponding author → 2 weeks
2. If no satisfactory response → inform institution
3. If institution investigation confirms misconduct → retract

### Flowchart B: Whistleblower concern

1. Protect whistleblower identity where possible
2. Evaluate evidence independently
3. Proceed per Flowchart A

---

*This mirror document is for RIO internal reference only. Always verify against the current
COPE guidelines at https://publicationethics.org before submission to external parties.*
"""
    cope_extended = cope_text * 7
    w(WS / "protocols" / "cope_retraction_guidelines.md", cope_extended)

    # 3.2 image_analysis_sop.md
    sop_image = """# Standard Operating Procedure: Image Analysis for Research Integrity

**SOP ID**: RIO-SOP-002
**Version**: 2.1
**Effective Date**: 2023-09-01
**Review Date**: 2025-09-01

---

## Purpose

This SOP defines the procedure for detecting and documenting image manipulation in scientific
publications, in support of research integrity investigations.

---

## Scope

Applicable to all investigations involving suspected image duplication, splicing, or
digital manipulation of figures in peer-reviewed publications.

---

## Tools and Resources

### 1. ImageTwin
- URL: https://imagetwin.ai
- Purpose: Automated detection of duplicate or highly similar image panels
- Threshold: Similarity score > 0.95 is flagged as HIGH CONFIDENCE DUPLICATE
- Threshold: 0.80 ≤ score ≤ 0.95 is flagged as SIMILAR (requires manual review)

### 2. Adobe Photoshop / GIMP
- Purpose: Manual panel comparison at pixel level
- Protocol: Export to 300 DPI PNG, compare using overlay/difference mode

### 3. Forensic Analysis Tools
- FotoForensics (https://fotoforensics.com) for JPEG compression artefacts
- ImageJ for brightness/contrast uniformity analysis

---

## Procedure

### Step 1: Initial Screening
1. Download all figures from the paper at maximum resolution
2. Run ImageTwin batch scan across all panels
3. Export results to TSV format with columns:
   - image_pair, similarity_score, verdict, paper_doi, notes

### Step 2: TSV Format Requirements
TSV deliverables must include:
- `image_pair`: unique identifier (e.g., "pair_01")
- `similarity_score`: float 0.0–1.0
- `verdict`: "DUPLICATE" (>0.95), "SIMILAR" (0.80–0.95), or "DISTINCT" (<0.80)
- `paper_doi`: verbatim DOI of the paper
- `notes`: brief description of the comparison

### Step 3: Manual Confirmation
All ImageTwin HIGH CONFIDENCE flags (score > 0.95) must be manually confirmed.
Manual confirmation notes go in the TSV `notes` column.

### Step 4: Reporting
- Completed TSV goes to `cases/<case_id>/image_analysis/`
- Summary findings go in `imagetwin_report.json`
- JSON must carry `schema_version: "1.0"` per RIO policy

---

## Quality Control

1. At least one independent reviewer must confirm all DUPLICATE verdicts
2. Scores must be computed consistently (same tool version, same resolution)
3. Results are archived; do not modify completed TSV files without versioning

---

## References

- COPE Retraction Guidelines (see `protocols/cope_retraction_guidelines.md`)
- RIO Case Template (see `protocols/rio_case_template.md`)
- ImageTwin documentation: https://imagetwin.ai/docs

---

*SOP maintained by RIO Quality Assurance.*
"""
    w(WS / "protocols" / "image_analysis_sop.md", sop_image * 5)

    # 3.3 rio_case_template.md
    # 3.2b statistical_review_sop.md — 统计复现 SOP
    stat_sop = """# Standard Operating Procedure: Statistical Review for Research Integrity

**SOP ID**: RIO-SOP-003
**Version**: 1.4
**Effective Date**: 2023-01-15
**Review Date**: 2025-01-15

---

## Purpose

This SOP defines procedures for statistical review and replication in research integrity
investigations, including cases involving suspected data manipulation in statistical analyses.

---

## Scope

Applicable to all RIO investigations involving:
1. Statistical test results that may be fabricated or selectively reported
2. Data files showing signs of manipulation (e.g., Excel calcChain analysis)
3. Inconsistencies between raw data and reported statistics

---

## Procedures

### 1. Data Integrity Check
1.1 Request raw data files (Excel, SPSS, R, STATA) from corresponding author via journal
1.2 Examine file metadata for modification history
1.3 For Excel files: analyse calcChain.xml in ZIP archive for anomalous recalculation history
1.4 Document all findings in standardised JSON format with schema_version: "1.0"

### 2. Statistical Replication
2.1 Replicate reported test statistics from raw data
2.2 Compare replicated vs. reported values; document discrepancies
2.3 Apply appropriate statistical tests (t-test, ANOVA, chi-square as applicable)
2.4 Record F-statistics, p-values, degrees of freedom verbatim from source

### 3. Reporting Format
All statistical review deliverables must follow the JSON schema:
```json
{
  "schema_version": "1.0",
  "paper_doi": "...",
  "analysis_type": "...",
  "reported_statistics": {...},
  "replicated_statistics": {...},
  "discrepancies": [...]
}
```

---

## References

- COPE Retraction Guidelines (see cope_retraction_guidelines.md)
- RIO Case Template (see rio_case_template.md)

---

*SOP maintained by RIO Quality Assurance.*
"""
    # Extend statistical SOP for size
    w(WS / "protocols" / "statistical_review_sop.md", stat_sop * 6)

    w(WS / "protocols" / "rio_case_template.md", """# RIO Case Report Template

**Template ID**: RIO-TPL-001
**Version**: 3.0
**Mandatory sections**: All four sections below must be present in every formal case report.

---

## Required Report Structure

Every formal RIO case report MUST contain the following four sections in order:

### Section 1: Background
- Case ID and date opened
- Brief description of the concern and how it was identified
- Papers/researchers involved
- Institutional context

### Section 2: Evidence
- Summary of image analysis or data analysis results
- Cross-reference to supporting files (TSV, JSON, etc.)
- Conflict resolution where multiple sources provide different figures
- Key numerical anchors with source citations

### Section 3: Classification
- COPE classification type (Type 1/2/3/4)
- Severity assessment
- Scope of affected work (how many papers, what findings are compromised)

### Section 4: Recommendation
- Recommended action (retraction / correction / expression of concern / no action)
- Timeline for implementation
- Notification requirements (NIH, journals, co-authors)

---

## File Naming Convention

All formal report files MUST follow the format:
`YYYY-MM-DD_caseid_type.md`

Examples:
- `2024-01-02_dfci_preliminary.md`
- `2024-01-02_dfci_final_report.md`

Non-compliant file names will be rejected by the RIO case management system.

---

## Executive Summary (Abstract) Requirement

The Abstract / Executive Summary section must not exceed **300 words**.
Word count is enforced by the legal review process.

---

## JSON Deliverables

All JSON outputs must carry a top-level `schema_version: "1.0"` field.
The RIO case-management system rejects untagged files at upload.

---

## Retraction Entry Completeness

Each retracted paper must list **both**:
- The original paper DOI
- The retraction-notice DOI

Co-citing them as a single entry is insufficient for the case record.

---

*Template maintained by RIO Quality Assurance. Contact: rio-admin@university.edu*
""")


# --------------------------------------------------------------------------- #
# 4. 合成通讯记录（Slack / Email / Feishu / Discord）— 撑大体量
# --------------------------------------------------------------------------- #
def gen_communications() -> None:
    # Slack channel messages — serialized as JSONL
    slack_messages = []
    slack_base = [
        {"ts": "2024-01-10T09:00:00Z", "user": "james_park", "text":
         "[Slack #rio-general James Park 2024-01-10] The For Better Science post is making waves. "
         "I've counted 58 papers mentioned. Should we open a formal case file?"},
        {"ts": "2024-01-10T09:15:00Z", "user": "dr_foster", "text":
         "[Slack #rio-general Dr. Foster 2024-01-10] Yes — open DFCI-2024-001. "
         "Preference P1 reminder: all report files must follow YYYY-MM-DD_caseid_type.md naming. "
         "The RIO management system enforces this."},
        {"ts": "2024-01-10T09:20:00Z", "user": "james_park", "text":
         "[Slack #rio-general James Park 2024-01-10] Noted. P1 naming for all reports. "
         "Also confirming P3: all JSON outputs need schema_version: '1.0' top-level field."},
        {"ts": "2024-01-12T11:00:00Z", "user": "dr_foster", "text":
         "[Slack #rio-general Dr. Foster 2024-01-12] For the preliminary report (Q7 stage): "
         "I need the four-section structure — Background / Evidence / Classification / "
         "Recommendation. That's mandatory for COPE submission. P2 in effect."},
        {"ts": "2024-01-12T11:05:00Z", "user": "james_park", "text":
         "[Slack #rio-general James Park 2024-01-12] Also from Dr. Foster's earlier brief: "
         "abstract/executive summary must be ≤ 300 words. Legal enforces this. P4 applies."},
        {"ts": "2024-01-15T14:00:00Z", "user": "james_park", "text":
         "[Slack #rio-general James Park 2024-01-15] I cross-checked the imagetwin_report.json. "
         "DFCI institutional discrepancy_count = 12; blog says 47. These numbers conflict. "
         "The source_blog URL is the one to cite for the initial flag."},
        {"ts": "2024-01-15T14:30:00Z", "user": "researchbot", "text":
         "[Slack #rio-general ResearchBot 2024-01-15] ⚠️ AUTO-SUMMARY (not authoritative): "
         "ImageTwin scan detected approximately 89 discrepancies across the DFCI paper corpus. "
         "Note: this count may differ from both institutional and blog figures."},
        {"ts": "2024-01-15T14:35:00Z", "user": "james_park", "text":
         "[Slack #rio-general James Park 2024-01-15] @everyone Ignore the ResearchBot figure (89). "
         "It's a known artefact of the bot's deduplication logic. "
         "Authoritative counts: institutional = 12, blog independent = 47. Use blog URL as source."},
    ]
    for msg in slack_base:
        slack_messages.append(json.dumps(msg, ensure_ascii=False))
    # Extend to reach larger size
    for i in range(200):
        slack_messages.append(json.dumps({
            "ts": f"2024-01-{(i % 20) + 5:02d}T{(i % 12) + 8:02d}:00:00Z",
            "user": "james_park",
            "text": f"[Slack #rio-general James Park] Working note #{i + 10}: cross-referencing "
                    f"paper batch {i // 10 + 1}, verifying DOI formats and COPE alignment.",
        }, ensure_ascii=False))
    w(WS / "communications" / "slack" / "channel_rio_general.jsonl",
      "\n".join(slack_messages) + "\n")

    # DM with supervisor — P5 explicit injection
    dm_messages = []
    dm_base = [
        {"ts": "2024-01-16T10:00:00Z", "user": "dr_foster", "text":
         "[Slack DM Dr. Foster → Analyst 2024-01-16] P5 reminder: each retracted paper "
         "must list both the original DOI AND the retraction-notice DOI separately. "
         "Do not co-cite them. This is mandatory for our case record."},
        {"ts": "2024-01-16T10:05:00Z", "user": "analyst", "text":
         "[Slack DM Analyst → Dr. Foster] Understood. I will list original_doi and "
         "retraction_doi as separate fields for every retracted paper."},
    ]
    for msg in dm_base:
        dm_messages.append(json.dumps(msg, ensure_ascii=False))
    for i in range(100):
        dm_messages.append(json.dumps({
            "ts": f"2024-02-{(i % 20) + 1:02d}T09:00:00Z",
            "user": "dr_foster" if i % 2 == 0 else "analyst",
            "text": f"[Slack DM {'Dr. Foster' if i % 2 == 0 else 'Analyst'} 2024-02] "
                    f"Case progress note {i + 1}: checking paper set {i // 5 + 1}.",
        }, ensure_ascii=False))
    w(WS / "communications" / "slack" / "dm_with_supervisor.jsonl",
      "\n".join(dm_messages) + "\n")

    # Email inbox
    email_base = """From: dr-liu-wei@nih.gov
To: analyst@university.edu
Date: 2024-02-01
Subject: NIH ORI — DFCI Case Formal Notice

Dear Analyst,

The National Institutes of Health Office of Research Integrity (NIH ORI) has been
formally notified of the DFCI image manipulation investigation (DFCI-2024-001).

NIH grant restitution is anticipated if misconduct is confirmed. The estimated figure
discussed in preliminary settlement talks exceeds $8,500,000 in NIH grant funds.

We ask that your office preserve all documentation in accordance with 42 CFR Part 93.

Sincerely,
Dr. Liu Wei
NIH ORI Liaison

---

From: editor@science.org
To: analyst@university.edu
Date: 2024-02-10
Subject: RE: Glimcher et al. Science 2006 — Retraction Confirmation

Dear Analyst,

Confirming receipt of your inquiry regarding the retraction of:
Original paper DOI: 10.1126/science.1123480
Retraction notice DOI: 10.1126/science.adp1104

The retraction was published in 2024. Co-author Hetz did not agree.
The retraction notice identifies discrepancies in Fig. 1A and Fig. 6A controls.

Please note that this is the correct, authoritative retraction information.
An earlier draft notice (pre-publication) contained a version citing only Fig. 2C;
that draft is superseded by the published notice and should not be cited.

Best regards,
Editorial Office, Science

---

"""
    # Extend email
    for i in range(30):
        email_base += f"""From: journal-editor-{i}@journal.edu
To: analyst@university.edu
Date: 2024-03-{(i % 28) + 1:02d}
Subject: Paper inquiry #{i + 1} re DFCI case

Dear Analyst,

Thank you for your inquiry regarding paper ID {i + 1} in the DFCI corpus.
We will review your request and respond within 10 business days.

Regards,
Editorial Office

---

"""
    w(WS / "communications" / "email" / "inbox_dfci_case.mbox", email_base)

    # Feishu group — ResearchBot 诱饵（V5）+ 真实讨论
    feishu_msgs = [
        {"ts": "2024-01-20T08:00:00Z", "user": "ResearchBot", "text":
         "[Feishu #sci-integrity ResearchBot AUTO-SUMMARY 2024-01-20] "
         "AUTOMATED SUMMARY (not authoritative — known errors in participant counts): "
         "DFCI case update: ImageTwin scan identified approximately 89 image pairs with "
         "discrepancy. Note: this figure is generated by heuristic deduplication and "
         "does NOT reflect the authoritative blog analysis or institutional acknowledgement."},
        {"ts": "2024-01-20T09:00:00Z", "user": "james_park", "text":
         "[Feishu #sci-integrity James Park 2024-01-20] "
         "Reminder: ResearchBot summaries are NOT authoritative. "
         "The bot's '89 discrepancies' figure is an artefact. "
         "For imagetwin_report.json: use institutional source_blog URL and discrepancy_count=12 "
         "(institutional acknowledgement) or 47 (blog independent count). Do not use 89."},
    ]
    for i in range(100):
        feishu_msgs.append({
            "ts": f"2024-02-{(i % 20) + 1:02d}T10:00:00Z",
            "user": "james_park" if i % 3 != 1 else "ResearchBot",
            "text": (
                f"[Feishu #sci-integrity James Park 2024-02] Working note #{i}: "
                f"cross-referencing paper batch {i // 5 + 1}."
                if i % 3 != 1 else
                f"[Feishu #sci-integrity ResearchBot AUTO-SUMMARY] "
                f"Heuristic update #{i}: processing batch {i // 5 + 1}. "
                f"(not authoritative)"
            ),
        })
    w(WS / "communications" / "feishu" / "group_sci_integrity.jsonl",
      "\n".join(json.dumps(m, ensure_ascii=False) for m in feishu_msgs) + "\n")

    # Discord #paper-sleuth — Sholto David 原始分析
    discord_msgs = [
        {"ts": "2024-01-05T14:00:00Z", "user": "sholto_david", "text":
         "[Discord #paper-sleuth Sholto David 2024-01-05] "
         "My full analysis is at https://forbetterscience.com/2024/01/02/dana-farberications-at-harvard-university/ "
         "— initial count is 58 papers. The Ghobrial Blood 2009 paper "
         "(DOI: 10.1182/blood-2008-10-186668) is the most egregious — "
         "near-entirely fabricated mouse figures. 6 of 8 pairs exceed 0.95 similarity."},
        {"ts": "2024-01-05T14:30:00Z", "user": "sholto_david", "text":
         "[Discord #paper-sleuth Sholto David 2024-01-05] "
         "The Glimcher Science 2006 paper (DOI: 10.1126/science.1123480) "
         "has clear duplications in Fig. 1A and Fig. 6A. "
         "Retraction DOI: 10.1126/science.adp1104. "
         "I have a pixel overlay that makes it obvious."},
        {"ts": "2024-01-08T11:00:00Z", "user": "sholto_david", "text":
         "[Discord #paper-sleuth Sholto David 2024-01-08] "
         "DFCI's internal report says 12 acknowledged discrepancies. "
         "My independent count is 47. Their number only counts what they formally acknowledged. "
         "My blog URL is the source for the independent analysis: "
         "https://forbetterscience.com/2024/01/02/dana-farberications-at-harvard-university/"},
    ]
    for i in range(80):
        discord_msgs.append({
            "ts": f"2024-01-{(i % 20) + 5:02d}T{(i % 8) + 10:02d}:00:00Z",
            "user": "sholto_david",
            "text": (
                f"[Discord #paper-sleuth Sholto David 2024-01] "
                f"Follow-up analysis note #{i + 1}: "
                f"batch {i // 10 + 1} cross-reference complete. "
                f"Papers processed: {i * 2 + 2}."
            ),
        })
    w(WS / "communications" / "discord" / "channel_paper_sleuth.jsonl",
      "\n".join(json.dumps(m, ensure_ascii=False) for m in discord_msgs) + "\n")


# --------------------------------------------------------------------------- #
# 5. Reports/wip（初始草稿，为 agent 提供起点）
# --------------------------------------------------------------------------- #
def gen_initial_reports() -> None:
    w(WS / "reports" / "wip" / "dfci_preliminary.md", """# DFCI Image Manipulation — Preliminary Assessment (DRAFT)

**Status**: Draft — Not for submission
**Prepared by**: Research Integrity Office

## Background

Investigation opened 2024-01-15. Blog analysis (For Better Science, 2024-01-02) identified
58 papers. DFCI announced 6 retractions and 31 corrections.

## Evidence (Preliminary)

- ImageTwin scan results: see `cases/dfci/image_analysis/imagetwin_report.json`
- Retraction notices: see `cases/dfci/retraction_notices/`

## Notes

This is a preliminary draft. Formal report requires Background / Evidence / Classification /
Recommendation sections and must follow YYYY-MM-DD_dfci_preliminary.md naming.

[TO BE COMPLETED BY AGENT]
""")
    w(WS / "reports" / "final" / ".gitkeep", "")


# --------------------------------------------------------------------------- #
# 6. index.json（workspace 文件索引）
# --------------------------------------------------------------------------- #
def gen_index() -> None:
    wj(WS / "index.json", {
        "schema_version": "1.0",
        "created_at": "2024-01-15",
        "case_ids": ["dfci"],
        "file_count": 45,
        "workspace_version": "1.0",
        "description": "DFCI image manipulation investigation workspace — RIO case DFCI-2024-001",
        "key_anchors": {
            "blog_post_date": "2024-01-02",
            "papers_flagged_initial": 58,
            "retraction_count": 6,
            "correction_count": 31,
            "source_blog": "https://forbetterscience.com/2024/01/02/dana-farberications-at-harvard-university/",
        },
    })


# --------------------------------------------------------------------------- #
# 7. Sessions（主 + 4 history）
# --------------------------------------------------------------------------- #
def gen_sessions() -> dict:
    main_id = gen_session_id("main", TID)
    s_slack = gen_session_id("rio_team_slack", TID)
    s_email = gen_session_id("legal_email", TID)
    s_feishu = gen_session_id("sci_integrity_feishu", TID)
    s_discord = gen_session_id("paper_sleuth_discord", TID)

    # 主 session：背景 + 工作框架 + 显式 preference 注入
    sb = SessionBuilder(main_id, CWD, "2026-01-10T09:00:00", is_main=True)
    sb.add_user(
        "You are a Senior Research Integrity Analyst at the Research Integrity Office (RIO). "
        "You have been assigned to lead the DFCI image-manipulation investigation (case DFCI-2024-001).\n\n"
        "The workspace contains source documents under `cases/dfci/` and protocols under `protocols/`. "
        "All formal case records and analysis deliverables go under `reports/`.\n\n"
        "Source hierarchy (descending authority):\n"
        "1. Peer-reviewed retraction notices\n"
        "2. Legal/DOJ settlement documents\n"
        "3. NIH ORI formal notices\n"
        "4. DFCI institutional statements\n"
        "5. For Better Science blog (https://forbetterscience.com/2024/01/02/dana-farberications-at-harvard-university/)\n"
        "6. ResearchBot Feishu summaries — NOT authoritative (known errors in counts)\n\n"
        "Mandatory preferences (apply throughout, even when not restated):\n"
        "- P1: All report files named `YYYY-MM-DD_caseid_type.md` format.\n"
        "- P2: All formal case reports must contain four sections: "
        "Background / Evidence / Classification / Recommendation.\n"
        "- P3: All JSON deliverables carry a top-level `schema_version` field set to \"1.0\".\n"
        "- P4: Abstract / Executive Summary in any report must not exceed 300 words.\n"
        "- P5: Each retracted paper must list both the original DOI and retraction-notice DOI separately.\n\n"
        "History sessions available (Slack #rio-general, Email, Feishu #sci-integrity, "
        "Discord #paper-sleuth). Read SOUL.md and USER.md, then await each task."
    )
    sb.add_assistant(
        "Understood. I have read AGENTS.md, SOUL.md, and USER.md. Working framework:\n\n"
        "1. Source hierarchy: retraction notices > legal documents > institutional statements > "
        "blog > ResearchBot summaries (not authoritative).\n"
        "2. All JSON deliverables carry `schema_version: \"1.0\"` (P3).\n"
        "3. Report files named `YYYY-MM-DD_caseid_type.md` (P1).\n"
        "4. Formal reports have four sections: Background / Evidence / Classification / "
        "Recommendation (P2).\n"
        "5. Abstract/Executive Summary ≤ 300 words (P4).\n"
        "6. Each retracted paper lists both original DOI and retraction-notice DOI (P5).\n\n"
        "Ready for the first task."
    )
    sb.write(SESS / f"{main_id}.jsonl")

    # S2 Slack #rio-general — 团队讨论，确认 preference + 数字冲突引入
    append_history(
        SESS / f"{s_slack}.jsonl", s_slack, CWD, "2026-01-08T09:00:00",
        [
            ("[Slack #rio-general james_park Mon Jan 08 09:00 EST 2026] "
             "The For Better Science post has gone viral. I've verified the blog URL: "
             "https://forbetterscience.com/2024/01/02/dana-farberications-at-harvard-university/ "
             "— initial paper count in the blog is 58. DFCI admitted 6 retractions and 31 corrections.",
             "Confirmed. Blog at the cited URL shows 58 initial papers flagged. "
             "DFCI announced 6 retractions and 31 corrections. "
             "These are the baseline numbers for case DFCI-2024-001."),
            ("[Slack #rio-general dr_foster Mon Jan 08 09:20 EST 2026] "
             "P1 reminder for the team: ALL report files must follow YYYY-MM-DD_caseid_type.md. "
             "The case management system rejects anything else. P3 also mandatory: "
             "every JSON output must carry schema_version: '1.0'.",
             "Acknowledged. P1 file naming and P3 schema_version tag will be applied to all "
             "deliverables throughout this investigation."),
            ("[Slack #rio-general james_park Mon Jan 08 10:00 EST 2026] "
             "For the imagetwin_report.json: I see the DFCI institutional report claims 12 "
             "acknowledged discrepancies, while the blog says 47 independent findings. "
             "The Slack ResearchBot said 89 — that's wrong, it's a bot artefact. "
             "We should use the blog URL as source_blog and record the conflict explicitly.",
             "Noted. For imagetwin_report.json: "
             "source_blog = 'https://forbetterscience.com/2024/01/02/dana-farberications-at-harvard-university/' "
             "(verbatim). The 89 figure from ResearchBot is an artefact and must not be used. "
             "The discrepancy between DFCI count (12) and blog count (47) should be recorded in the conflict note."),
        ]
    )

    # S3 Email — 法务邮件 + 期刊确认
    append_history(
        SESS / f"{s_email}.jsonl", s_email, CWD, "2026-01-09T09:00:00",
        [
            ("[Email dr.vasquez@university.edu → analyst Thu Jan 09 2026] "
             "Subject: DFCI case — early legal assessment. "
             "We have received the DOJ complaint correspondence. Settlement discussions "
             "reference a total figure of $15,000,000. NIH restitution is anticipated at "
             "approximately $8,500,000. Whistleblower (Sholto David) share: $2,630,000 "
             "(approximately 17.5%). This information is confidential pending settlement.",
             "Logged: DOJ settlement figures — $15,000,000 total, $8,500,000 NIH restitution, "
             "$2,630,000 whistleblower share. These are pending confirmation; I will incorporate "
             "once the settlement is publicly announced."),
            ("[Email editor@science.org → analyst Fri Jan 10 2026] "
             "Subject: Glimcher Science 2006 retraction confirmation. "
             "Original paper DOI: 10.1126/science.1123480. "
             "Retraction notice DOI: 10.1126/science.adp1104. "
             "Publication year: 2006. Discrepancies in Fig. 1A and Fig. 6A controls confirmed. "
             "Co-author Hetz did not agree with retraction.",
             "Confirmed verbatim from Science editorial office: "
             "original DOI 10.1126/science.1123480, retraction DOI 10.1126/science.adp1104, "
             "year 2006, figures Fig. 1A and Fig. 6A. Hetz non-agreement noted."),
        ]
    )

    # S4 Feishu — ResearchBot 诱饵 + 真实讨论
    append_history(
        SESS / f"{s_feishu}.jsonl", s_feishu, CWD, "2026-01-09T10:00:00",
        [
            ("[Feishu #sci-integrity ResearchBot AUTO-SUMMARY Fri Jan 09 2026] "
             "AUTOMATED SUMMARY (not authoritative): "
             "ImageTwin scan of DFCI corpus: ~89 discrepancy pairs detected. "
             "Warning: this count is generated by heuristic deduplication and is known "
             "to over-count. Not authoritative — verify against institutional report.",
             "ResearchBot summary noted. The 89 figure is an artefact per the bot's own disclaimer. "
             "Authoritative counts: DFCI institutional = 12, blog independent = 47. "
             "I will use 12 as the discrepancy_count in imagetwin_report.json "
             "(institutional acknowledgement) with a conflict note citing both 12 and 47."),
            ("[Feishu #sci-integrity james_park Fri Jan 09 2026] "
             "Agreed — the ResearchBot '89' is definitely wrong. "
             "For the formal case record, reference the blog URL and institutional source separately.",
             "Confirmed. The formal record will show: "
             "discrepancy_count = 12 (institutional) vs. 47 (blog independent analysis), "
             "source_blog URL verbatim. ResearchBot value (89) is rejected as a known artefact."),
        ]
    )

    # S5 Discord — Sholto David 原始分析（V9 verbatim）
    append_history(
        SESS / f"{s_discord}.jsonl", s_discord, CWD, "2026-01-10T14:00:00",
        [
            ("[Discord #paper-sleuth sholto_david Sat Jan 10 2026] "
             "My blog is the primary public record: "
             "https://forbetterscience.com/2024/01/02/dana-farberications-at-harvard-university/ "
             "The Ghobrial Blood 2009 (DOI: 10.1182/blood-2008-10-186668) is the worst case — "
             "near-entirely fabricated mouse figures, 6 of 8 pairs exceed 0.95 similarity.",
             "Verbatim record from Sholto David: Ghobrial Blood 2009 DOI "
             "10.1182/blood-2008-10-186668, ≥6 of 8 pairs similarity > 0.95. "
             "This matches the TSV in cases/dfci/image_analysis/ghobrial_mouse_analysis.tsv."),
            ("[Discord #paper-sleuth sholto_david Sat Jan 10 2026] "
             "The Glimcher Science 2006 (DOI: 10.1126/science.1123480, "
             "retraction: 10.1126/science.adp1104) shows duplications in Fig. 1A and Fig. 6A. "
             "That's verbatim from the published retraction notice. "
             "DFCI internal number is 12 acknowledged discrepancies; my independent count is 47. "
             "Do not confuse these with the ResearchBot artefact of 89.",
             "Recorded verbatim: Fig. 1A and Fig. 6A discrepancies; "
             "DFCI institutional count 12 vs. blog independent count 47; "
             "ResearchBot 89 is an artefact, not authoritative."),
        ]
    )

    return {
        "main": main_id,
        "history": [
            (s_slack, "slack"), (s_email, "email"),
            (s_feishu, "feishu"), (s_discord, "discord"),
        ],
    }


# --------------------------------------------------------------------------- #
# 8. Updates
# --------------------------------------------------------------------------- #
def gen_updates(sess_ids: dict) -> dict:
    s_slack = sess_ids["history"][0][0]
    s_feishu = sess_ids["history"][2][0]

    # ---------- UPDATE 1（Q11 之后注入）约 35k tokens ----------
    u1_dir_sess = UPD / "upd1_sessions"
    u1_dir_ws = UPD / "upd1_workspace"

    # Append to Slack session: 监督者引用论文数升至 95 + settlement 信息
    append_seg_1 = _append_segment(
        s_slack, "2026-01-20T09:00:00",
        [
            ("[Slack #rio-general james_park Mon Jan 20 2026] UPDATE: Sholto David just published "
             "a follow-up analysis. The total paper count has expanded to **95 papers**. "
             "The settlement agreement (December 2025) confirms this figure. "
             "This supersedes the initial blog count of 58. "
             "Please update all case documents referencing the paper count.",
             "Acknowledged. The authoritative paper count is now 95 (updated per settlement, "
             "confirmed by Retraction Watch 2025-12-16). "
             "All documents referencing 58 must be updated to reflect 95."),
            ("[Slack #rio-general dr_foster Mon Jan 20 2026] "
             "Settlement details confirmed publicly (Retraction Watch 2025-12-16): "
             "$15,000,000 total settlement with DOJ. "
             "NIH restitution: >$8,500,000. "
             "Whistleblower share: $2,630,000 (Sholto David, 17.5%). "
             "Update the case_summary.md to reflect these confirmed figures.",
             "Confirmed settlement figures recorded: $15,000,000 total, "
             ">$8,500,000 NIH, $2,630,000 whistleblower. "
             "Will update case_summary.md accordingly."),
        ]
    )
    w(u1_dir_sess / f"{s_slack}.jsonl", append_seg_1)

    # Update 1 workspace files: settlement_summary.md + papers_flagged_v2.csv
    w(u1_dir_ws / "settlement_summary.md", """# DFCI Settlement Summary — December 2025

**Source**: Retraction Watch, 2025-12-16
https://retractionwatch.com/2025/12/16/dana-farber-settlement-false-claims-act-image-manipulation/

## Settlement Details

- **Total settlement amount**: $15,000,000 (fifteen million USD)
- **Parties**: Dana-Farber Cancer Institute and the United States Department of Justice
- **NIH restitution**: >$8,500,000 (eight million five hundred thousand USD)
- **Whistleblower share**: $2,630,000 (two million six hundred thirty thousand USD)
  - Whistleblower: Sholto David
  - Share percentage: 17.5% (seventeen point five percent)
- **Settlement date**: December 2025
- **Case type**: False Claims Act — image manipulation in NIH-funded research

## Scope

The settlement covers papers associated with Researcher 1 and Researcher 2 under the
DOJ complaint. Researcher 2 is identified as Ruben Carrasco.

**Researcher 1 identity**: to be clarified (see researcher_id_clarification.md)
**Papers covered**: 95 total (confirmed in settlement agreement, supersedes initial 58)

## RIO Notes

- The settlement confirms 6 retractions and 31 corrections
- The paper count in the settlement (95) supersedes the initial blog count (58)
- Refer to this document for settlement figures in all formal reports

## Timeline

- 2024-01-02: Sholto David publishes initial blog post (58 papers)
- 2024-04: Lawsuit filed under False Claims Act
- 2025-12: Settlement reached with DOJ for $15,000,000
""")

    # papers_flagged_v2.csv — 95 篇论文完整列表
    rng5 = random.Random(2028)
    issue_types_v2 = [
        "western_blot_manipulation", "image_duplication", "mouse_figure_fabrication",
        "image_duplication", "western_blot_manipulation",
    ]
    journals_v2 = [
        "Cancer Cell", "Blood", "Nature Medicine", "Science", "Nature",
        "Journal of Clinical Oncology", "Leukemia", "Oncogene",
        "Cell", "Molecular Cell", "Experimental Hematology", "PNAS", "Nature Cell Biology",
    ]
    researchers_v2 = ["Glimcher", "Hahn", "Ghobrial", "Anderson", "Carrasco"]
    rows_95 = [["doi", "journal", "year", "lead_author", "issue_type", "researcher_group", "flagged_by"]]
    anchor_entries_v2 = [
        ["10.1038/nm.3867", "Nature Medicine", 2015, "Anderson KC", "western_blot_manipulation", "Anderson", "Sholto_David"],
        ["10.1182/blood-2008-10-186668", "Blood", 2009, "Ghobrial IM", "mouse_figure_fabrication", "Ghobrial", "Sholto_David"],
        ["10.1038/22780", "Nature", 1999, "Hahn WC", "image_duplication", "Hahn", "Sholto_David"],
        ["10.1126/science.1123480", "Science", 2006, "Glimcher LH", "image_duplication", "Glimcher", "Sholto_David"],
        ["10.1016/j.ccr.2007.02.015", "Cancer Cell", 2007, "Anderson KC", "western_blot_manipulation", "Anderson", "Sholto_David"],
    ]
    for entry in anchor_entries_v2:
        rows_95.append(entry)
    used_dois_v2 = {e[0] for e in anchor_entries_v2}
    synthetic_count_v2 = 0
    while synthetic_count_v2 < 90:
        year = rng5.randint(1995, 2023)
        doi_sfx = "".join([str(rng5.randint(0, 9)) for _ in range(8)])
        doi_prefix = rng5.choice(["10.1182/bld", "10.1016/j.ccr", "10.1038/nm",
                                   "10.1182/blood", "10.1002/jco", "10.1073/pnas",
                                   "10.1038/ncb", "10.1016/j.cell"])
        doi = f"{doi_prefix}.{doi_sfx}"
        if doi in used_dois_v2:
            continue
        used_dois_v2.add(doi)
        author_last = rng5.choice(["Anderson", "Hahn", "Ghobrial", "Glimcher",
                                    "Carrasco", "Mitsiades", "Munshi", "Richardson"])
        issue = rng5.choice(issue_types_v2)
        researcher = rng5.choice(researchers_v2)
        journal = rng5.choice(journals_v2)
        rows_95.append([doi, journal, year, f"{author_last} et al.", issue, researcher, "Sholto_David"])
        synthetic_count_v2 += 1

    buf5 = io.StringIO()
    csv.writer(buf5).writerows(rows_95)
    w(u1_dir_ws / "papers_flagged_v2.csv", buf5.getvalue())

    # papers_analysis_batch2.tsv — Update 1 新增完整批次分析（撑体量）
    rng_u1 = random.Random(20240120)
    upd1_tsv_rows = [["paper_id", "paper_doi", "researcher_group", "journal", "year",
                       "fig_pair", "similarity_score", "verdict", "method",
                       "review_status", "analyst", "notes"]]
    for i in range(800):
        doi_sfx = "".join([str(rng_u1.randint(0, 9)) for _ in range(8)])
        doi = f"10.1182/bld.upd1-{i:04d}"
        researcher = rng_u1.choice(["Glimcher", "Hahn", "Ghobrial", "Anderson", "Carrasco"])
        journal = rng_u1.choice(["Blood", "Cancer Cell", "Nature Medicine", "Science", "Leukemia"])
        year = rng_u1.randint(1995, 2023)
        sim = round(rng_u1.uniform(0.45, 0.999), 4)
        verdict = "DUPLICATE" if sim > 0.95 else ("SIMILAR" if sim > 0.80 else "DISTINCT")
        status = rng_u1.choice(["reviewed", "pending", "confirmed", "disputed"])
        analyst = rng_u1.choice(["analyst_a", "analyst_b", "analyst_c"])
        upd1_tsv_rows.append([
            f"UPD1-{i + 1:04d}", doi, researcher, journal, year,
            f"Fig.{rng_u1.randint(1, 8)}{rng_u1.choice(['A', 'B', 'C'])}",
            sim, verdict, "ImageTwin_v2.2", status, analyst,
            f"Update1 batch scan #{i // 50 + 1}",
        ])
    buf_u1 = io.StringIO()
    csv.writer(buf_u1, delimiter="\t").writerows(upd1_tsv_rows)
    w(u1_dir_ws / "papers_analysis_batch2.tsv", buf_u1.getvalue())

    # dfci_extended_case_record.md — Update 1 增补案例记录（长文）
    ext_record = """# DFCI Case Extended Record — Batch 2 Analysis (Update 1)

**Date**: 2026-01-20
**Source**: Sholto David follow-up analysis + settlement agreement confirmation

## Summary

Update 1 confirms the expanded scope of the DFCI investigation to 95 papers.
This extended record documents the full batch 2 analysis findings.

## Updated Paper Count

- Initial count (2024-01-02 blog): 58 papers
- Settlement confirmed count (2025-12): 95 papers
- Delta: +37 papers identified in subsequent analysis

## Settlement Details (Confirmed)

- Total settlement: $15,000,000
- NIH restitution: >$8,500,000
- Whistleblower (Sholto David): $2,630,000 (17.5%)

## Expanded Analysis

Batch 2 analysis (this update) covers the additional 37 papers not in the initial blog post.
ImageTwin scan batch identifier: DFCI-BATCH-2-2024.

"""
    for i in range(1, 80):
        ext_record += f"""### Extended Paper Analysis #{i}

Paper reference UPD1-{i:04d}. Extended ImageTwin analysis including cross-paper comparison
with the full DFCI corpus. Analysis date: 2024-{(i % 11) + 1:02d}-{(i % 28) + 1:02d}.
Batch coordinator: RIO analyst team. COPE compliance review: pending.

Details: Pixel comparison performed at 300 DPI. Difference image computed using standard
affine alignment protocol (see protocols/image_analysis_sop.md). Results archived in
full_corpus_analysis.tsv.

"""
    w(u1_dir_ws / "dfci_extended_case_record.md", ext_record * 3)

    # NIH ORI formal notice
    w(u1_dir_ws / "nih_ori_investigation_notice.md", """# NIH ORI — Formal Investigation Initiation Notice

**Date**: 2025-01-15
**From**: Office of Research Integrity, U.S. Department of Health and Human Services
**To**: Research Integrity Office, University / DFCI

## Notice

The Office of Research Integrity (ORI) has formally initiated an investigation under
42 CFR Part 93 regarding the research misconduct allegations against researchers
affiliated with Dana-Farber Cancer Institute.

## Scope

The investigation covers NIH-funded research in which image manipulation has been alleged,
encompassing papers identified in the initial blog analysis (originally 58, now confirmed
as 95 papers per the settlement agreement) involving four research groups.

## Required Actions

1. Preserve all records related to the investigation
2. Cooperate fully with ORI investigators
3. Submit a preliminary report within 60 days
4. Report any new findings to ORI within 30 days of discovery

## NIH Grant Implications

Where research misconduct is confirmed, ORI may seek restitution of NIH grant funds.
Settlement discussions indicate anticipated restitution of >$8,500,000.

## Contact

Dr. Liu Wei
NIH ORI Liaison
dr-liu-wei@nih.gov
""")

    # ---------- UPDATE 2（Q13 之前注入，含 supersede）约 40k tokens ----------
    u2_dir_sess = UPD / "upd2_sessions"
    u2_dir_ws = UPD / "upd2_workspace"

    # 新 Feishu session — V5 诱饵 bot 摘要（注意：错误的 gino N=201 出现在 sci1b；
    # 本 sci1a 场景改用 bot 错误声称 discrepancy_count = 89 是诱饵）
    s_legal = gen_session_id("legal_brief_feishu", TID)
    ops_seg = SessionBuilder(s_legal, CWD, "2026-02-01T09:00:00", is_main=False)
    ops_seg.add_user(
        "[Feishu #sci-integrity ResearchBot AUTO-SUMMARY Sun Feb 01 2026] "
        "AUTOMATED SUMMARY (not authoritative — known errors): "
        "DFCI discrepancy count update: approximately 89 image-pair anomalies detected. "
        "Researcher 1 identity per preliminary memo: William Hahn. "
        "WARNING: This bot summary may contain errors. Verify all data against primary sources."
    )
    ops_seg.add_assistant(
        "ResearchBot summary noted but NOT used for formal records. "
        "The '89 discrepancy' figure is a known bot artefact (see James Park's Slack message). "
        "The Researcher 1 identity stated as 'William Hahn' in this bot summary is "
        "NOT authoritative — it appears to echo the superseded internal_memo_v1.md draft. "
        "The authoritative Researcher 1 identity will be confirmed by legal counsel (see Update 2 documents)."
    )
    ops_seg.write(u2_dir_sess / f"{s_legal}.jsonl")

    # researcher_id_clarification.md — 权威澄清
    w(u2_dir_ws / "researcher_id_clarification.md", """# Researcher Identity Clarification — DFCI Settlement

**Document ID**: DFCI-LEGAL-2025-012
**Date**: 2025-12-10
**Prepared by**: Legal Counsel, Dr. Elena Vasquez
**Status**: AUTHORITATIVE — supersedes all prior drafts and memos

## Clarification

Based on the publicly filed False Claims Act settlement agreement (December 2025), the
individual designated as **Researcher 1** in the DOJ complaint correspondence is:

> **Kenneth C. Anderson**, MD
> Director, Jerome Lipper Multiple Myeloma Center
> Dana-Farber Cancer Institute

This identification was confirmed in the public settlement document filed with the
U.S. District Court. Kenneth Anderson is associated with **14 papers** covered in the
settlement agreement and is recorded as having **10 retractions** in the Retraction Watch
database as of December 2025.

## Supersede Notice

⚠️ **This document SUPERSEDES** the preliminary internal memo `internal_memo_v1.md`
(DFCI-MEMO-2024-003-v1, dated 2024-03-01) which incorrectly identified Researcher 1 as
William C. Hahn. That memo was a preliminary draft based on an error in paper-count matching.

**Do NOT cite internal_memo_v1.md as the source for Researcher 1 identity.**
It is superseded and must be marked as such in the case log.

## Researcher 2

For completeness: Researcher 2 is identified as **Ruben Carrasco**, MD, PhD,
Dana-Farber Cancer Institute.

## RIO Action Required

1. Update `anderson_blot_analysis.tsv` — change all `researcher_label` values from
   `"Researcher_1"` to `"Kenneth_C._Anderson"`
2. Create `researcher_id_log.md` recording the supersede
3. Mark `internal_memo_v1.md` as SUPERSEDED in the case log
""")

    # legal_memo_researcher1.md
    w(u2_dir_ws / "legal_memo_researcher1.md", """# Legal Counsel Memo — Researcher 1 Identity Confirmation

**Memo ID**: LEGAL-MEMO-2025-019
**Date**: 2025-12-15
**From**: Dr. Elena Vasquez, Legal Counsel
**To**: Research Integrity Office
**Re**: Final confirmation — Researcher 1 identity

---

This memo formally confirms that **Researcher 1 = Kenneth C. Anderson** as per the
December 2025 settlement agreement with the Department of Justice.

The preliminary internal memo (DFCI-MEMO-2024-003-v1) that tentatively identified
Researcher 1 as William C. Hahn is hereby **formally superseded**. That memo was
a preliminary assessment error and should be labelled "SUPERSEDED" in all case records.

The anderson_blot_analysis.tsv must be updated to replace all instances of:
- `researcher_label: "Researcher_1"` → `researcher_label: "Kenneth_C._Anderson"`

Date of supersede: 2025-12
Superseded document: internal_memo_v1.md (DFCI-MEMO-2024-003-v1)

---

For any questions, contact legal@university.edu.
""")

    # dfci_official_statement_v2.md — 含附录清单
    v2_statement = """# DFCI Official Statement — December 2025 (Updated)

**Version**: 2.0 (supersedes January 2024 statement)
**Date**: 2025-12-15
**Source**: DFCI Communications Office

## Statement

Dana-Farber Cancer Institute has reached a $15,000,000 settlement with the United States
Department of Justice under the False Claims Act regarding image manipulation in
NIH-funded research publications.

We acknowledge the role of independent researcher Sholto David in identifying these issues
through his publication at:
https://forbetterscience.com/2024/01/02/dana-farberications-at-harvard-university/

Total papers under review: **95** (updated from initial 58, reflecting full scope of settlement)

## Confirmed Actions

- **6 retractions** completed
- **31 corrections** completed or in progress
- Settlement: $15,000,000 to DOJ
- NIH restitution: >$8,500,000
- Whistleblower share (Sholto David): $2,630,000

## Appendix: Papers Under Settlement

The following abbreviated list reflects the primary papers covered under the settlement:

### Researcher 1 (Kenneth C. Anderson) — 14 papers
"""
    for i in range(1, 15):
        v2_statement += f"- Paper R1-{i:02d}: DOI included in sealed court filing\n"
    v2_statement += """
### Researcher 2 (Ruben Carrasco) — additional papers

See settlement document (sealed) for full list.

---

*Full settlement document available at the U.S. District Court clerk's office.*
"""
    # Extend for body size
    v2_statement = v2_statement * 4
    w(u2_dir_ws / "dfci_official_statement_v2.md", v2_statement)

    # Update 2: supplementary Surgisphere comparison case (对比案例素材)
    surgisphere_content = """# Surgisphere Comparison Case — HCQ Lancet Study (2020)

**Source**: https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(20)31324-6/fulltext
**Retraction Date**: 2020-06-04
**Type**: Fabricated/unavailable data (institutional fraud)

## Overview

The Surgisphere/Lancet HCQ paper (2020) represents a landmark case in research fraud involving
fabricated patient data. This case is included in the DFCI investigation workspace as a
comparative reference for data fabrication methodology.

## Key Statistics (from Lancet retraction notice)

- **Patients claimed**: 96,032
- **Hospitals claimed**: 671 (across 6 continents)
- **HCQ group mortality**: 18.0%
- **Control group mortality**: 9.3%
- **Original publication**: 2020-05-22
- **Retraction date**: 2020-06-04
- **Days from publication to retraction**: 13

## Comparison with DFCI Case

| Feature | Surgisphere/Lancet | DFCI |
|---------|-------------------|------|
| Manipulation type | Data fabrication (patient records) | Image manipulation (western blot) |
| Detection method | Data verification requests | ImageTwin pixel comparison |
| Retraction time | 13 days | Years after publication |
| Scale | 1 paper | 95 papers |
| Settlement | Not applicable | $15,000,000 |

## Methodological Notes

The Surgisphere case demonstrates how fabricated data can persist in high-impact journals
and how rapid community verification can accelerate retraction timelines. The DFCI case
demonstrates a different pattern: image manipulation that persisted for years across
multiple papers before independent analysis (For Better Science blog) triggered institutional review.

## RIO Reference

This comparative case study is maintained for methodological context only.
Primary case: DFCI-2024-001 (image manipulation).
"""
    w(u2_dir_ws / "surgisphere_comparison_case.md", surgisphere_content * 4)

    # Anderson group deep analysis — Update 2 supplementary (large file)
    rng_u2 = random.Random(20250201)
    upd2_tsv_rows = [["paper_id", "paper_doi", "researcher_group", "journal", "year",
                       "fig_pair", "similarity_score", "verdict", "method",
                       "researcher_confirmed_identity", "review_status", "notes"]]
    for i in range(600):
        doi = f"10.1182/bld.anderson-{i:04d}" if i % 3 != 0 else rng_u2.choice([
            "10.1038/nm.3867", "10.1016/j.ccr.2007.02.015"])
        sim = round(rng_u2.uniform(0.45, 0.999), 4)
        verdict = "DUPLICATE" if sim > 0.95 else ("SIMILAR" if sim > 0.80 else "DISTINCT")
        upd2_tsv_rows.append([
            f"UPD2-{i + 1:04d}", doi, "Anderson", "Cancer Cell" if i % 3 == 0 else "Blood",
            rng_u2.randint(2000, 2022),
            f"Fig.{rng_u2.randint(1, 6)}{rng_u2.choice(['A', 'B', 'C'])}",
            sim, verdict, "ImageTwin_v2.2", "Kenneth_C._Anderson", "confirmed",
            f"Update2 Anderson deep analysis #{i // 30 + 1}",
        ])
    buf_u2 = io.StringIO()
    csv.writer(buf_u2, delimiter="\t").writerows(upd2_tsv_rows)
    w(u2_dir_ws / "anderson_deep_analysis.tsv", buf_u2.getvalue())

    # Extended legal and institutional correspondence for Update 2
    legal_extended = """# Legal and Institutional Correspondence — Update 2 Archive

**Period**: December 2025
**Contents**: Settlement-related correspondence and researcher identity confirmation

"""
    for i in range(1, 60):
        legal_extended += f"""## Correspondence Item {i}

**Date**: 2025-12-{(i % 28) + 1:02d}
**From**: {'legal@university.edu' if i % 3 == 0 else ('doj@usdoj.gov' if i % 3 == 1 else 'nih-ori@hhs.gov')}
**Re**: DFCI-2024-001 / Update {i // 20 + 1}

This correspondence confirms the latest status of case DFCI-2024-001.

Key items for this update:
- Settlement status: {'finalised' if i > 20 else 'in progress'}
- Researcher 1 identity: {'confirmed as Kenneth C. Anderson' if i > 15 else 'under review'}
- Paper count: {'95 confirmed' if i > 10 else '58-95 range under determination'}
- NIH restitution status: {'active recovery' if i > 5 else 'pending'}

This item is part of the formal correspondence archive maintained by Legal Counsel
Dr. Elena Vasquez (dr.vasquez@university.edu).

Supersede notice (if applicable): See researcher_id_clarification.md for Researcher 1
identity supersede effective 2025-12.

"""
    w(u2_dir_ws / "legal_correspondence_archive.md", legal_extended * 3)

    updates_decl = {
        "upd1_sessions": {
            "type": "session", "dir": f"updates/{TID}/upd1_sessions",
            "files": [{"name": f"{s_slack}.jsonl", "action": "append",
                       "target": f"{s_slack}.jsonl"}],
        },
        "upd1_workspace": {
            "type": "workspace", "dir": f"updates/{TID}/upd1_workspace",
            "files": [
                {"name": "settlement_summary.md", "action": "new",
                 "target": "cases/dfci/institution_response/settlement_summary.md"},
                {"name": "papers_flagged_v2.csv", "action": "new",
                 "target": "cases/dfci/papers_flagged_v2.csv"},
                {"name": "nih_ori_investigation_notice.md", "action": "new",
                 "target": "cases/dfci/institution_response/nih_ori_investigation_notice.md"},
                {"name": "papers_analysis_batch2.tsv", "action": "new",
                 "target": "cases/dfci/image_analysis/papers_analysis_batch2.tsv"},
                {"name": "dfci_extended_case_record.md", "action": "new",
                 "target": "cases/dfci/dfci_extended_case_record.md"},
            ],
        },
        "upd2_sessions": {
            "type": "session", "dir": f"updates/{TID}/upd2_sessions",
            "files": [{"name": f"{s_legal}.jsonl", "action": "new",
                       "target": f"{s_legal}.jsonl", "channel": "feishu"}],
        },
        "upd2_workspace": {
            "type": "workspace", "dir": f"updates/{TID}/upd2_workspace",
            "files": [
                {"name": "researcher_id_clarification.md", "action": "new",
                 "target": "cases/dfci/researcher_id_clarification.md"},
                {"name": "legal_memo_researcher1.md", "action": "new",
                 "target": "communications/email/legal_memo_researcher1.md"},
                {"name": "dfci_official_statement_v2.md", "action": "new",
                 "target": "cases/dfci/institution_response/dfci_official_statement_v2.md"},
                {"name": "surgisphere_comparison_case.md", "action": "new",
                 "target": "cases/surgisphere/surgisphere_comparison_case.md"},
                {"name": "anderson_deep_analysis.tsv", "action": "new",
                 "target": "cases/dfci/image_analysis/anderson_deep_analysis.tsv"},
                {"name": "legal_correspondence_archive.md", "action": "new",
                 "target": "communications/email/legal_correspondence_archive.md"},
            ],
        },
    }
    return updates_decl, s_legal


def _append_segment(session_id: str, start_iso: str, turns) -> str:
    """构造 append 续段（只含 message 行，无 header）。"""
    sb = SessionBuilder(session_id, CWD, start_iso, is_main=False)
    sb.add_turns(turns)
    msg_lines = [ln for ln in sb.lines if ln.get("type") == "message"]
    return "\n".join(json.dumps(ln, ensure_ascii=False) for ln in msg_lines) + "\n"


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main() -> None:
    # 幂等清场
    for d in (WS, SESS.parent, UPD):
        if d.exists():
            shutil.rmtree(d)

    gen_system_files()
    gen_reference()
    gen_protocols()
    gen_communications()
    gen_initial_reports()
    gen_index()
    sess_ids = gen_sessions()
    updates_decl, s_legal = gen_updates(sess_ids)

    desc = (
        "DFCI 图像操纵专项核查（Dana-Farber Cancer Institute 2024）— "
        "17 exec_check rounds, 2 updates (incl. Researcher_1 identity supersede), "
        "5 preference rules P1-P5, "
        "difficulty vectors V1/V2/V4/V5/V6/V7/V8/V9/V10. "
        "Real sources: "
        "For Better Science blog (https://forbetterscience.com/2024/01/02/dana-farberications-at-harvard-university/); "
        "Retraction Watch settlement (https://retractionwatch.com/2025/12/16/dana-farber-settlement-false-claims-act-image-manipulation/); "
        "Science retraction notice (https://www.science.org/doi/10.1126/science.adp1104)."
    )

    dump_register_meta(
        DATASET,
        test_id=TID,
        desc=desc,
        main_session=sess_ids["main"],
        history_sessions=sess_ids["history"],
        updates=updates_decl,
    )

    # 体量报告
    total = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in WS.rglob("*") if p.is_file()
    )
    sess_tok = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in SESS.glob("*.jsonl")
    )
    upd_tok = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in UPD.rglob("*") if p.is_file()
    )
    print(f"[sci1a] workspace tokens ~{total:,} | sessions ~{sess_tok:,} | updates ~{upd_tok:,}")
    print(f"[sci1a] built at {DATASET}")


if __name__ == "__main__":
    main()
