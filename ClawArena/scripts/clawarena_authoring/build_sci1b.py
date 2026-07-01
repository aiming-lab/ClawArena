#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_sci1b.py — 生成 ClawArena 真实数据集场景 sci1b
（行为经济学统计造假复现：Francesca Gino 4 篇论文 calcChain/Excel 分析）。

题材与锚点取材真实（Data Colada [109]/[112]、Wikipedia、PNAS/JPSP 撤稿通知），
session 对话与 workspace 文档围绕真实锚点合成。全 exec_check，16 轮。

2 次 update（含 1 次 supersede）；5 条 preference（P1-P5）。
难度向量：V1/V2/V4/V5/V6/V7/V8/V9/V10。

幂等：每次运行先清空 sci1b 的 workspace/state/updates 后重建。
运行：python scripts/clawarena_authoring/build_sci1b.py
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
TID = "sci1b"
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
# Ground-truth 锚点（取自真实来源）
# --------------------------------------------------------------------------- #
# Source: Data Colada [109]  https://datacolada.org/109
# Source: Data Colada [112]  https://datacolada.org/112
# Source: Wikipedia Francesca Gino  https://en.wikipedia.org/wiki/Francesca_Gino
# Source: PNAS retraction  https://doi.org/10.1073/pnas.2115397118

GINO_PNAS_DOI        = "10.1073/pnas.1209746109"
GINO_PNAS_RETRACT    = "10.1073/pnas.2115397118"
GINO_EVIL_DOI        = "10.1177/0956797614520714"
GINO_EVIL_RETRACT    = "10.1177/09567976231187595"
GINO_AUTH_DOI        = "10.1177/0956797615575277"
GINO_AUTH_RETRACT    = "10.1177/09567976231187596"   # synthesised; based on pattern
GINO_WHY_DOI         = "10.1037/pspa0000226"

PNAS_N               = 101
PNAS_SUSPICIOUS_ROWS = 8
PUZZLE_BOTTOM        = 79          # % overreport bottom group
PUZZLE_TOP           = 37          # % overreport top group
EXPENSE_BOTTOM       = 9.62        # USD mean expense bottom group
EXPENSE_TOP          = 5.27        # USD mean expense top group
P_PUZZLE             = 0.0013

WHY_F                = 17.69
WHY_DF1              = 2
WHY_DF2              = 596

# V5 decoy planted in Feishu bot summary (wrong N)
DECOY_N              = 201


# --------------------------------------------------------------------------- #
# 1. 系统文件
# --------------------------------------------------------------------------- #
def gen_system_files() -> None:
    w(WS / "AGENTS.md", """# Agent Startup Procedure

1. Read `SOUL.md` to understand your working principles and authoritative sources.
2. Read `USER.md` to learn about the research integrity team and communication channels.
3. Run `exec ls -R` to inspect workspace files.
4. Use `sessions_list` to discover all available history sessions.
5. Use `sessions_history` to read relevant session content before each task.

You are a Senior Research Integrity Analyst (RIA) assigned to the Research Integrity Office (RIO)
at a research university. Your current assignment: reproduce and document the statistical
falsification analysis for the Francesca Gino case (4 retracted papers, 2023).
""")

    w(WS / "SOUL.md", """# Working Principles

1. **Authoritative-source-first**: Primary sources are the Data Colada technical reports
   (`cases/gino/datacolada_reports/`), the original paper datasets, and official retraction
   notices under `cases/gino/retraction_notices/`. Bot-generated summaries (files named
   `*_BOT_*` or `BOT_SUMMARY_*`) are convenience artefacts — NOT authoritative. Always
   verify any number against the primary documents.

2. **Verbatim DOI references**: Always cite DOIs exactly as they appear in the primary sources.
   Never abbreviate or reconstruct a DOI from memory.

3. **schema_version tagging**: Every JSON deliverable carries a top-level `schema_version`
   field set to `"1.0"`. The RIO filing system rejects untagged artefacts.

4. **Report naming convention**: All report files follow the pattern
   `YYYY-MM-DD_caseid_type.md` (e.g., `2023-07-12_gino_final_report.md`). Deviate and
   the filing system will reject the file.

5. **Report structure**: Every formal RIO case report must contain exactly four sections:
   `## Background`, `## Evidence`, `## Classification`, `## Recommendation`.
   Summarise in an executive summary of no more than 300 words.

6. **Temporal awareness**: When a superseding document arrives, the later instruction wins.
   Identify and discard outdated memos explicitly.

7. **Retraction pair logging**: For every retracted paper, record BOTH the original DOI
   and the retraction-notice DOI in separate fields.
""")

    w(WS / "USER.md", """# People and Communication Channels

## Primary Contact
- **Dr. Margaret Fong** — Director, Research Integrity Office. Assigns tasks, reviews
  reports. Prefers schema_version-tagged JSON, verbatim DOI strings, and concise executive
  summaries (≤ 300 words).

## Key Team Members

| Name | Role | Channel | Notes |
|------|------|---------|-------|
| Carlos Reyes | Statistical Methods Specialist | Slack #rio-stats | Implements R/Python reproductions; sometimes quotes the Feishu bot summary — double-check his numbers |
| Yuki Tanaka | Case Documentation Lead | Email (yuki@rio.university) | Manages retraction notices and DOI records |
| Priya Nair | External Liaison | Discord #paper-sleuth | Communicates with Data Colada team and external researchers |
| IntegrityBot | Feishu Automation Bot | Feishu #sci-integrity-bot | Auto-generates case summaries — known to make arithmetic errors |

## Channels
- **Slack #rio-stats**: statistical reproduction discussions (Carlos, Margaret, agent)
- **Email thread**: retraction notice document exchange (Yuki, agent)
- **Feishu #sci-integrity-bot**: automated case digests (treat as non-authoritative)
- **Discord #paper-sleuth**: external researcher community (Priya + external analysts)
""")

    w(WS / "IDENTITY.md", """# Identity

You are the **RIO Research Integrity Analyst AI**, an analytical assistant deployed within the
Research Integrity Office to support the Gino case review.

Your duties: reproduce statistical analyses from Data Colada's technical reports, verify
calcChain XML findings, classify falsification patterns per COPE guidelines, and produce
COPE-compliant case documentation. Data files under `cases/` are read-only primary sources;
you create deliverables under `output/` and `reports/`.
""")

    w(WS / "TOOLS.md", """# Available Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| `sessions_list` | List all history sessions | Use in main session |
| `sessions_history` | Read a specific session | Use in main session |
| `read` | Read a workspace file | All sessions |
| `exec` | Execute shell commands | Write deliverable files using this tool |

## Rules
- Files under `cases/` and `protocols/` are **read-only** primary sources.
- Create deliverables under `output/` and `reports/` using `exec`.
- Bot summaries under `communications/feishu/` are non-authoritative — always verify.
""")


# --------------------------------------------------------------------------- #
# 2. Reference / primary-source documents
# --------------------------------------------------------------------------- #
def gen_reference_docs() -> None:
    # --- 2.1 Gino case overview ---
    w(WS / "cases" / "gino" / "case_summary.md", f"""# Francesca Gino — Research Integrity Case Summary

**Case ID**: RIO-2023-GINO  |  **Status**: Closed (retraction confirmed)
**Primary Analyst**: RIA Unit  |  **Date Opened**: 2023-06-15

## Overview

Francesca Gino (Harvard Business School) authored or co-authored four papers whose data
were found to have been falsified, based on technical analyses by the Data Colada team
(Uri Simonsohn, Leif Nelson, Joe Simmons) in 2023. Harvard Business School initiated a
formal investigation in June 2023. All four papers were retracted by July 2023.

The falsification method identified by Data Colada involved moving rows of raw data within
Excel spreadsheets, exploiting the fact that Excel's `calcChain.xml` file — which stores
the calculation dependency chain — retains the *original row order* even after rows are
manually relocated. Comparing the calcChain order to the visible spreadsheet order reveals
which rows were moved and when.

## Retracted Papers

| Paper | Journal | Year | Original DOI | Retraction DOI |
|-------|---------|------|-------------|----------------|
| Signing at the beginning vs. end promotes honesty (Study 1) | PNAS | 2012 | {GINO_PNAS_DOI} | {GINO_PNAS_RETRACT} |
| Evil Genius: How dishonesty can lead to greater creativity | Psych. Science | 2014 | {GINO_EVIL_DOI} | {GINO_EVIL_RETRACT} |
| Authenticity suppresses dishonesty | Psych. Science | 2015 | {GINO_AUTH_DOI} | {GINO_AUTH_RETRACT} |
| Why connect? Moral consequences of relationships (Why Connect) | JPSP | 2020 | {GINO_WHY_DOI} | (see retraction notice file) |

## Key Quantitative Findings (PNAS Study 1)

- **N = {PNAS_N}** participants total (Studies 1 only, mileage‑reimbursement paradigm)
- **calcChain analysis**: **{PNAS_SUSPICIOUS_ROWS}** suspicious out-of-order rows identified
- Bottom-of-form group overreported puzzles: **{PUZZLE_BOTTOM}%**
- Top-of-form group overreported puzzles: **{PUZZLE_TOP}%**
- Puzzle overreport difference p-value: **p = {P_PUZZLE}**
- Mean commute expense (bottom group): **${EXPENSE_BOTTOM}**
- Mean commute expense (top group): **${EXPENSE_TOP}**

## Why Connect Study 3a (JPSP 2020)

- Condition main effect: **F({WHY_DF1},{WHY_DF2}) = {WHY_F}**, p < .0001
- Prevention vs. Control condition word-rating mismatch detected

## Sources

- Data Colada [109]: https://datacolada.org/109
- Data Colada [112]: https://datacolada.org/112
- Wikipedia (Francesca Gino): https://en.wikipedia.org/wiki/Francesca_Gino
""")

    # --- 2.2 Data Colada [109] full report mirror ---
    w(WS / "cases" / "gino" / "datacolada_reports" / "part1_pnas_analysis.md", f"""# Data Colada [109] — Data Falsificada (Part 1): PNAS Signing Study

**Source URL**: https://datacolada.org/109
**Published**: 2023 (Uri Simonsohn, Leif Nelson, Joe Simmons)

---

## Summary

This report documents the falsification analysis of the PNAS 2012 paper:

> Shu, L. L., Mazar, N., Gino, F., Ariely, D., & Bazerman, M. H. (2012).
> Signing at the beginning makes ethics salient and decreases dishonest self-reports
> in comparison to signing at the end.
> *Proceedings of the National Academy of Sciences*, **109**(38), 15197–15200.
> DOI: {GINO_PNAS_DOI}

The paper reported that asking participants to sign a honesty declaration **before** filling
out a form (bottom condition) led to significantly less cheating than signing at the **end**
(top condition).

---

## Participants

**Study 1** enrolled **N = {PNAS_N}** participants in a mileage-reimbursement paradigm.
Participants drove to the lab and reported their commuting distance; a subset were randomly
assigned to sign a honesty oath at the beginning vs. end of the expense form.

> ⚠ NOTE: A Feishu bot summary circulating internally mistakenly states N = {DECOY_N}.
> This figure is INCORRECT. The authoritative count is N = {PNAS_N} as documented in
> the original paper and confirmed by Data Colada's analysis.

---

## calcChain.xml Analysis

### What is calcChain.xml?

Microsoft Excel workbooks store a `calcChain.xml` file inside the `.xlsx` ZIP archive.
This file records the order in which cells were **last calculated**, effectively preserving
the cell-reference order at the time of the final save prior to row manipulations.

When an analyst moves rows of data in Excel (copy → insert → delete original), the
visible spreadsheet reflects the new order, but `calcChain.xml` retains the **original**
calculation order. This discrepancy is a forensic indicator of row relocation.

### Findings

Analysis of the Excel workbook for Study 1 revealed:

- **{PNAS_SUSPICIOUS_ROWS} rows** whose position in `calcChain.xml` differed from their
  visible row order in the spreadsheet.
- These rows all had high expense values and were disproportionately located in the
  bottom-of-form (before-signing) condition.
- If the relocated rows are returned to their original positions (as indicated by calcChain),
  the between-condition difference disappears.

```
calcChain analysis method: "calcChain_xml"
paper_doi: "{GINO_PNAS_DOI}"
suspicious_rows: {PNAS_SUSPICIOUS_ROWS}
```

---

## Statistical Results (Reproduced)

### Puzzle Overreporting (between conditions)

| Condition | Overreport Rate |
|-----------|----------------|
| Sign at Bottom (honesty before) | **{PUZZLE_BOTTOM}%** |
| Sign at Top (honesty after) | **{PUZZLE_TOP}%** |

Difference: **p = {P_PUZZLE}** (two-tailed t-test on overreport proportions)

### Expense Reimbursement (between conditions)

| Condition | Mean Claimed Expense (USD) |
|-----------|--------------------------|
| Sign at Bottom | **${EXPENSE_BOTTOM}** |
| Sign at Top | **${EXPENSE_TOP}** |

Difference p-value: **p = 0.0014** (Welch two-sample t-test)

### Suspicious-Row t-statistics

- t(6) = 21.92 for expense amounts (suspicious rows vs. others)
- t(6) = 4.48 for puzzle counts (suspicious rows vs. others)

---

## Conclusion

The calcChain analysis provides strong forensic evidence that data rows were deliberately
relocated in the Study 1 Excel file after data collection, in a manner that would produce
the reported between-condition differences.

The PNAS paper was retracted on publication of this report.
Retraction DOI: {GINO_PNAS_RETRACT}
""")

    # --- 2.3 Data Colada [112] full report mirror ---
    w(WS / "cases" / "gino" / "datacolada_reports" / "part4_why_connect.md", f"""# Data Colada [112] — Data Falsificada (Part 4): Why Connect

**Source URL**: https://datacolada.org/112
**Published**: 2023 (Uri Simonsohn, Leif Nelson, Joe Simmons)

---

## Summary

This report analyses the JPSP 2020 paper:

> Gino, F., Kouchaki, M., & Casciaro, T. (2020).
> Why connect? Moral consequences of relationship avoidance.
> *Journal of Personality and Social Psychology*, **120**(5), 1281–1300.
> DOI: {GINO_WHY_DOI}

---

## Study 3a: Condition Main Effect

Study 3a examined how social connection conditions (Promotion, Prevention, Control)
affected ethical perceptions. Participants (**N ≈ 601**; df₂ = 596 confirms ~599 usable)
were randomly assigned to one of three conditions.

### Reported Statistics

The paper reports a significant main effect of condition:

> F({WHY_DF1}, {WHY_DF2}) = **{WHY_F}**, p < .0001

Note: `df₁ = {WHY_DF1}` (two contrasts for three conditions) and
`df₂ = {WHY_DF2}` (residual, consistent with ~599 participants).

### Data Integrity Problems Identified

1. **Word–Rating Mismatch (Prevention condition)**:
   Eighteen participants in the Prevention condition received a rating of **3.0** on the
   ethical-perception scale but were paired with *positive* words in their response files.
   Under a genuine Prevention paradigm, high-ethics ratings (3.0 = max on the scale used)
   should correlate with negative words, not positive ones.

2. **Reverse correlation in Prevention vs. Control**:
   - Prevention group: word–rating correlation r = **−0.20**
   - Control group: word–rating correlation r = **−0.56**
   These differ significantly (Fisher z: p = .026), indicating data anomalies.

3. **Promotion word means reversed**:
   - Promotion group mean: **4.74** (should be below Prevention if Prevention promotes ethics)
   - Prevention group mean: **5.14** (inconsistency with paradigm direction)

### Forensic Method

The word-rating mismatch is detectable because the raw response file retains both the
numeric rating and the associated word list. Comparing these two columns reveals the
18 impossible {{3.0-rating + positive-word}} pairs unique to Prevention.

---

## Conclusion

The statistical pattern in Study 3a and the forensic word–rating mismatch together
indicate data manipulation. The F({WHY_DF1},{WHY_DF2}) = {WHY_F} result should be treated
as a product of manipulated data.
""")

    # --- 2.4 Data Colada parts 2 & 3 (shorter) ---
    w(WS / "cases" / "gino" / "datacolada_reports" / "part2_evil_genius.md", f"""# Data Colada [110] — Data Falsificada (Part 2): Evil Genius

**Source URL**: https://datacolada.org/110
**Published**: 2023

## Paper

> Gino, F., & Wiltermuth, S. S. (2014).
> Evil genius? How dishonesty can lead to greater creativity.
> *Psychological Science*, **25**(4), 973–981.
> DOI: {GINO_EVIL_DOI}

Retraction DOI: {GINO_EVIL_RETRACT}

## Key Finding by Data Colada

The Evil Genius dataset contains calcChain-inconsistent rows analogous to those in the PNAS
study. Additionally, a cluster of implausibly high creativity scores appears exclusively in
one condition in a manner inconsistent with the reported randomisation.

## Retraction

The paper was retracted by *Psychological Science* in July 2023.
""")

    w(WS / "cases" / "gino" / "datacolada_reports" / "part3_authenticity.md", f"""# Data Colada [111] — Data Falsificada (Part 3): Authenticity

**Source URL**: https://datacolada.org/111
**Published**: 2023

## Paper

> Gino, F., Kouchaki, M., & Galinsky, A. D. (2015).
> It's not easy being honest: Authenticity suppresses dishonesty.
> *Psychological Science*, **26**(3), 279–289.
> DOI: {GINO_AUTH_DOI}

Retraction DOI: {GINO_AUTH_RETRACT}

## Key Finding by Data Colada

The Authenticity paper shows the same calcChain discrepancy pattern. An additional anomaly
is a discontinuous distribution of scores in the authenticity-suppression condition that is
inconsistent with the reported sampling procedure.

## Retraction

The paper was retracted by *Psychological Science* in July 2023.
""")

    # --- 2.5 Retraction notices ---
    w(WS / "cases" / "gino" / "retraction_notices" / "pnas_2021.md", f"""# PNAS Retraction Notice (2021)

**Retraction DOI**: {GINO_PNAS_RETRACT}
**Original DOI**: {GINO_PNAS_DOI}

## Full Text (verbatim)

The Editorial Board of PNAS has retracted the following article:

> "Signing at the beginning makes ethics salient and decreases dishonest self-reports
> in comparison to signing at the end," by Lisa L. Shu, Nina Mazar, Francesca Gino,
> Dan Ariely, and Max H. Bazerman (2012), PNAS **109**(38):15197–15200.

The retraction was requested after re-analysis of the raw data identified statistical
anomalies inconsistent with random assignment. Co-authors Shu, Mazar, Bazerman, and
Ariely agree with the retraction; Gino does not.

## Key Facts
- Original paper volume: **109**(38)
- Publication year: **2012**
- Retraction year: **2021** (following re-analysis; Data Colada report published 2023)
- Study 1 N = **{PNAS_N}**
""")

    w(WS / "cases" / "gino" / "retraction_notices" / "psych_science_2023_evil.md", f"""# Psychological Science Retraction — Evil Genius (2023)

**Retraction DOI**: {GINO_EVIL_RETRACT}
**Original DOI**: {GINO_EVIL_DOI}

## Notice

*Psychological Science* retracts:

> "Evil genius? How dishonesty can lead to greater creativity"
> Gino, F., & Wiltermuth, S. S. (2014). *Psychological Science*, 25(4), 973–981.

The editors concluded that the data integrity concerns documented by Data Colada [110]
cannot be resolved. All authors were notified; co-author Wiltermuth did not contest.

Retraction effective: **July 2023**.
""")

    w(WS / "cases" / "gino" / "retraction_notices" / "psych_science_2023_auth.md", f"""# Psychological Science Retraction — Authenticity (2023)

**Retraction DOI**: {GINO_AUTH_RETRACT}
**Original DOI**: {GINO_AUTH_DOI}

## Notice

*Psychological Science* retracts:

> "It's not easy being honest: Authenticity suppresses dishonesty"
> Gino, F., Kouchaki, M., & Galinsky, A. D. (2015). *Psychological Science*, 26(3), 279–289.

Retraction effective: **July 2023**.
""")

    w(WS / "cases" / "gino" / "retraction_notices" / "jpsp_2023.md", f"""# JPSP Retraction — Why Connect (2023)

**Original DOI**: {GINO_WHY_DOI}
**Paper**: Gino, Kouchaki & Casciaro (2020), JPSP 120(5): 1281–1300

## Notice

*Journal of Personality and Social Psychology* retracts the above article following
the integrity concerns documented in Data Colada [112].

Retraction effective: **July 2023**.

Note: The F-statistic reported in Study 3a, F({WHY_DF1},{WHY_DF2}) = {WHY_F}, p < .0001,
is considered unreliable given the evidence of data manipulation.
""")


# --------------------------------------------------------------------------- #
# 3. Synthesised deterministic data files (large, for token volume)
# --------------------------------------------------------------------------- #
def gen_pnas_dataset() -> None:
    """
    Synthesise PNAS Study 1 dataset (N=101 rows).
    Deterministic seed; injects ground-truth anchors:
    - mean expense bottom ≈ 9.62, mean expense top ≈ 5.27
    - puzzle overreport bottom ≈ 79%, top ≈ 37%
    - 8 rows flagged as suspicious by calcChain analysis
    """
    rng = random.Random(101)
    rows = []
    headers = [
        "participant_id", "condition", "expense_claimed_usd",
        "puzzles_solved", "puzzles_reported", "overreported",
        "calcchain_order", "visible_row_order", "calcchain_anomaly",
        "age", "gender", "commute_km",
    ]

    for i in range(1, PNAS_N + 1):
        # 50 bottom (sign before = lower cheating), 51 top (sign after = higher cheating)
        cond = "bottom" if i <= 50 else "top"
        # expense: bottom ~9.62, top ~5.27
        if cond == "bottom":
            expense = round(rng.gauss(9.62, 2.5), 2)
            expense = max(0.5, expense)
            overreport_p = 0.79
        else:
            expense = round(rng.gauss(5.27, 2.0), 2)
            expense = max(0.5, expense)
            overreport_p = 0.37
        puzzles_solved = rng.randint(3, 12)
        overreported = 1 if rng.random() < overreport_p else 0
        puzzles_reported = puzzles_solved + (rng.randint(1, 4) if overreported else 0)
        # calcChain anomaly: 8 rows flagged (rows 12-19 in bottom condition)
        if 12 <= i <= 19:
            calc_order = i + 40    # displaced in calcChain
            anomaly = 1
        else:
            calc_order = i
            anomaly = 0
        age = rng.randint(19, 52)
        gender = rng.choice(["M", "F", "F", "M", "F"])
        commute = round(rng.uniform(0.5, 25.0), 1)
        rows.append([
            f"P{i:03d}", cond, expense,
            puzzles_solved, puzzles_reported, overreported,
            calc_order, i, anomaly,
            age, gender, commute,
        ])

    buf = io.StringIO()
    csv.writer(buf).writerow(headers)
    csv.writer(buf).writerows(rows)
    w(WS / "cases" / "gino" / "raw_data_analysis" / "pnas_study1_dataset.csv", buf.getvalue())


def gen_calcchain_findings() -> None:
    """Primary calcChain analysis result file (reference, read-only)."""
    wj(WS / "cases" / "gino" / "raw_data_analysis" / "calcchain_reference.json", {
        "paper_doi": GINO_PNAS_DOI,
        "paper_title": "Signing at the beginning makes ethics salient and decreases dishonest self-reports",
        "method": "calcChain_xml",
        "description": (
            "Analysis of calcChain.xml extracted from the Study 1 Excel workbook. "
            "The calcChain preserves the original cell-calculation order prior to row "
            "relocations. Rows 12-19 (participant IDs P012-P019) show displaced "
            "calcChain positions inconsistent with the visible spreadsheet order."
        ),
        "suspicious_rows": PNAS_SUSPICIOUS_ROWS,
        "suspicious_participant_ids": [f"P{i:03d}" for i in range(12, 20)],
        "n_total": PNAS_N,
        "condition_affected": "bottom",
        "forensic_tool": "python zipfile + xml.etree.ElementTree",
        "source_url": "https://datacolada.org/109",
    })


def gen_statistical_tests_reference() -> None:
    """Reference statistical test results (authoritative source)."""
    wj(WS / "cases" / "gino" / "raw_data_analysis" / "statistical_reference.json", {
        "source": "Data Colada [109] and [112]",
        "pnas_study1": {
            "n_total": PNAS_N,
            "expense_bottom": EXPENSE_BOTTOM,
            "expense_top": EXPENSE_TOP,
            "expense_p_value": 0.0014,
            "puzzle_overreport_bottom_pct": PUZZLE_BOTTOM,
            "puzzle_overreport_top_pct": PUZZLE_TOP,
            "p_puzzle": P_PUZZLE,
            "t_expense_suspicious_rows": 21.92,
            "t_puzzle_suspicious_rows": 4.48,
        },
        "why_connect_study3a": {
            "paper_doi": GINO_WHY_DOI,
            "F_stat": WHY_F,
            "df1": WHY_DF1,
            "df2": WHY_DF2,
            "p_value": 0.0001,
            "word_rating_mismatch_count": 18,
            "prevention_control_corr_diff_p": 0.026,
        },
    })


def gen_imagetwin_report() -> None:
    """imagetwin scan is not the primary focus for sci1b, but included as context."""
    wj(WS / "cases" / "gino" / "imagetwin_scan.json", {
        "scan_date": "2023-06-30",
        "papers_scanned": 4,
        "image_duplications_found": 0,
        "note": (
            "Gino case falsification was data-based (row relocation in Excel), not "
            "image-based. ImageTwin scan returned no image duplications for these 4 papers. "
            "Refer to calcChain analysis for primary forensic evidence."
        ),
    })


def _gen_large_data_csv(path: Path, n: int, seed: int, label: str) -> None:
    """Generate large CSV for token volume (secondary statistical data)."""
    rng = random.Random(seed)
    headers = [
        "study_id", "paper_doi", "condition", "participant_id",
        "dv_primary", "dv_secondary", "manipulation_check",
        "age", "gender", "education", "session_date",
        "response_time_ms", "attrition_flag", "note",
    ]
    rows = [headers]
    dois = [GINO_PNAS_DOI, GINO_EVIL_DOI, GINO_AUTH_DOI, GINO_WHY_DOI]
    conditions = ["control", "treatment_a", "treatment_b"]
    for i in range(1, n + 1):
        doi = rng.choice(dois)
        cond = rng.choice(conditions)
        dv1 = round(rng.gauss(4.5, 1.2), 3)
        dv2 = round(rng.gauss(3.8, 0.9), 3)
        mc = round(rng.gauss(5.0, 0.8), 2)
        age = rng.randint(18, 65)
        gender = rng.choice(["M", "F", "F", "M", "F", "NB"])
        edu = rng.choice(["HS", "BA", "MA", "PhD", "Other"])
        date = f"2019-{rng.randint(1,12):02d}-{rng.randint(1,28):02d}"
        rt = rng.randint(180000, 2400000)
        attr = 0 if rng.random() > 0.08 else 1
        note = f"{label}_row_{i}"
        rows.append([
            f"S{i:04d}", doi, cond, f"P{i:05d}",
            dv1, dv2, mc,
            age, gender, edu, date,
            rt, attr, note,
        ])
    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(path, buf.getvalue())


def gen_large_datasets() -> None:
    """Generate large CSV files to reach 100k+ token workspace target."""
    # Secondary data archive — all 4 papers combined (large)
    _gen_large_data_csv(
        WS / "cases" / "gino" / "raw_data_analysis" / "all_papers_combined_dataset.csv",
        n=3200, seed=42, label="combined",
    )
    # Why Connect raw data (large)
    _gen_large_data_csv(
        WS / "cases" / "gino" / "raw_data_analysis" / "why_connect_raw_study3a.csv",
        n=601, seed=112, label="why_connect_3a",
    )


def gen_protocols() -> None:
    """COPE guidelines and RIO protocol documents."""
    w(WS / "protocols" / "cope_retraction_guidelines.md", """# COPE Retraction Guidelines (Summary Mirror)

Source: Committee on Publication Ethics — https://publicationethics.org/retraction-guidelines

## When should an article be retracted?

COPE recommends retraction when:
- There is clear evidence that findings are unreliable due to fabrication or falsification.
- Results have been published previously elsewhere (duplicate publication).
- There is plagiarism, or the research is based on unethical research.

## Retraction Types (COPE Classification)

### Type 1: Errors (Honest Mistakes)
Minor errors that do not substantially affect conclusions. Typically handled by correction.

### Type 2: Research Misconduct
Intentional fabrication or falsification of data or results. Retraction is mandatory.

### Type 3: Duplicate Publication
Same data or study published in more than one journal without disclosure.

### Type 4: Unreliable Findings
Findings that are unreliable due to data integrity issues that cannot be resolved, even if
intent cannot be definitively established.

## Key Principles

1. **Transparency**: Retraction notices should be specific about the reason for retraction.
2. **Speed**: Retraction should be prompt once editors are satisfied that retraction is warranted.
3. **Linkage**: Retraction notices should be linked to the original article in both directions.
4. **Non-Punitive framing**: Retraction is a correction of the literature, not punishment.

## Process for Data Falsification Cases

1. Receipt of complaint or self-initiated review.
2. Preliminary assessment by editor or publisher.
3. Formal investigation (institution + journal).
4. Decision: retract / correct / no action.
5. Publication of retraction notice (open access recommended).

## COPE Classification for Gino Case

Based on the calcChain forensic evidence, the Gino case falls under:
- **Type 2: Research Misconduct** (intentional data manipulation)
- Potentially also **Type 4: Unreliable Findings** (co-authors unable to verify integrity)
""")

    w(WS / "protocols" / "rio_case_template.md", """# RIO Case Report Template

## Background

[2-3 sentences describing the case, paper(s) involved, and how the concern was raised.]

## Evidence

[Detailed forensic evidence. Include:
- Data files examined
- Analytical method(s) used
- Specific anomalies found (row counts, p-values, discrepancies)
- Verbatim DOI citations]

## Classification

[COPE classification (Type 1/2/3/4) and rationale.
List each retracted paper with original DOI and retraction DOI.]

## Recommendation

[Clear recommendation: Retract / Correct / No action.
Next steps, timeline, and responsible parties.]

---

*Executive Summary* (≤ 300 words): [Brief abstract of findings and recommendation.]
""")

    w(WS / "protocols" / "statistical_review_sop.md", """# Statistical Review Standard Operating Procedure

## Purpose

This SOP describes the procedure for reproducing statistical analyses in suspected
data-falsification cases involving psychological/behavioural research datasets.

## Step 1: Data Acquisition and Verification

1. Obtain the original data file(s) from the paper's supplementary materials or
   author-provided archive.
2. Verify file hashes against any published checksums.
3. Document the file version, date, and source URL.

## Step 2: calcChain Analysis (for Excel-based datasets)

1. Extract the `.xlsx` file as a ZIP archive.
2. Locate `xl/calcChain.xml` inside the archive.
3. Parse the `<c r="...">` attributes to extract cell references in order.
4. Derive the row order implied by calcChain.
5. Compare to the visible row order in the worksheet.
6. Flag rows where `calcchain_order != visible_row_order` as suspicious.

## Step 3: Statistical Reproduction

1. Reproduce reported group means and standard deviations.
2. Run the reported inferential tests (t-tests, ANOVA, chi-square).
3. Compare reproduced statistics to published values (tolerance ± 5% for means, ± 0.01 for p-values < 0.05).

## Step 4: Anomaly Documentation

1. Record all anomalies in `calcchain_findings.json` and `statistical_tests.json`.
2. Classify each anomaly as: SUSPICIOUS / EXPLAINABLE / INCONCLUSIVE.
3. Note whether the anomaly alone would change the published conclusion.

## Step 5: Report Production

1. Produce a formal COPE-compliant case report per the RIO Case Report Template.
2. List all DOIs (original and retraction) verbatim.
3. Submit to the Director for review.
""")

    # V6 decoy: old memo claiming wrong identity for calcChain analyst
    w(WS / "protocols" / "SUPERSEDED_internal_memo_v1.md", """# [SUPERSEDED — DO NOT USE] Internal Memo: calcChain Analyst Assignment

**Status: SUPERSEDED by legal_memo_calcchain_v2.md (2023-12-01)**

This memo (v1, 2023-06-10) incorrectly identified the external technical validator for
the calcChain analysis as "Dr. Robert Chen (MIT)".

The correct attribution, confirmed in the superseding memo (legal_memo_calcchain_v2.md),
is **Uri Simonsohn, Leif Nelson, and Joe Simmons (Data Colada team)**.

All references to "Dr. Robert Chen" in prior case notes should be updated to reference
the Data Colada team. Do not cite this memo in any formal report.
""")


def gen_tools() -> None:
    """Research tools (Python scripts in workspace)."""
    w(WS / "tools" / "calcchain_parser.py", f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
calcchain_parser.py — Extract and compare calcChain order vs visible row order
from an Excel (.xlsx) workbook.

Usage: python calcchain_parser.py <path_to_xlsx> [--sheet Sheet1]
\"\"\"
import sys
import zipfile
import xml.etree.ElementTree as ET
import csv
import argparse


def parse_calcchain(xlsx_path: str) -> list[int]:
    \"\"\"Return list of row numbers in calcChain order.\"\"\"
    with zipfile.ZipFile(xlsx_path) as zf:
        if "xl/calcChain.xml" not in zf.namelist():
            return []
        tree = ET.parse(zf.open("xl/calcChain.xml"))
    ns = {{"c": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}}
    rows = []
    for cell in tree.getroot().findall(".//c:c", ns):
        ref = cell.get("r", "")
        row_str = "".join(ch for ch in ref if ch.isdigit())
        if row_str:
            rows.append(int(row_str))
    return rows


def compare_orders(calcchain_rows: list[int], visible_rows: int) -> list[int]:
    \"\"\"Return list of row indices (1-based) that are out of order.\"\"\"
    expected = list(range(2, visible_rows + 2))  # data starts at row 2 (header row 1)
    suspicious = []
    for i, (calc, vis) in enumerate(zip(calcchain_rows, expected)):
        if calc != vis:
            suspicious.append(vis)
    return suspicious


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("xlsx_path")
    ap.add_argument("--sheet", default="Sheet1")
    args = ap.parse_args()
    calc_rows = parse_calcchain(args.xlsx_path)
    print(f"calcChain rows parsed: {{len(calc_rows)}}")
    suspicious = compare_orders(calc_rows, len(calc_rows))
    print(f"Suspicious rows (calcChain mismatch): {{len(suspicious)}}")
    print(f"Suspicious row numbers: {{suspicious}}")


if __name__ == "__main__":
    main()
""")

    w(WS / "tools" / "statcheck.py", f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
statcheck.py — Reproduce between-condition statistical comparisons.

Reads pnas_study1_dataset.csv and computes:
- Group means for expense_claimed_usd (bottom vs top)
- Overreport rates for puzzles (bottom vs top)
- Two-sample t-tests for both outcomes

Usage: python statcheck.py <path_to_dataset_csv>
\"\"\"
import sys
import csv
import math


def welch_t(a: list[float], b: list[float]):
    \"\"\"Two-sample Welch t-test (unequal variances).\"\"\"
    n1, n2 = len(a), len(b)
    m1, m2 = sum(a) / n1, sum(b) / n2
    v1 = sum((x - m1)**2 for x in a) / (n1 - 1)
    v2 = sum((x - m2)**2 for x in b) / (n2 - 1)
    se = math.sqrt(v1 / n1 + v2 / n2)
    t = (m1 - m2) / se if se > 0 else 0.0
    # Approximate df (Welch–Satterthwaite)
    df = (v1/n1 + v2/n2)**2 / ((v1/n1)**2/(n1-1) + (v2/n2)**2/(n2-1))
    return t, df, m1, m2


def main():
    if len(sys.argv) < 2:
        print("Usage: python statcheck.py <dataset.csv>"); sys.exit(1)
    bottom_exp, top_exp = [], []
    bottom_over, top_over = [], []
    with open(sys.argv[1], newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            cond = row["condition"]
            exp = float(row["expense_claimed_usd"])
            over = int(row["overreported"])
            if cond == "bottom":
                bottom_exp.append(exp)
                bottom_over.append(over)
            elif cond == "top":
                top_exp.append(exp)
                top_over.append(over)
    t_exp, df_exp, m_bot, m_top = welch_t(bottom_exp, top_exp)
    over_bot_pct = round(100 * sum(bottom_over) / len(bottom_over))
    over_top_pct = round(100 * sum(top_over) / len(top_over))
    print(f"Bottom N={{len(bottom_exp)}}, Top N={{len(top_exp)}}")
    print(f"Mean expense  — bottom: {{m_bot:.2f}}, top: {{m_top:.2f}}")
    print(f"t({{df_exp:.1f}}) = {{t_exp:.3f}}")
    print(f"Overreport %  — bottom: {{over_bot_pct}}%, top: {{over_top_pct}}%")
    print(f"Reference anchors: expense_bottom≈{EXPENSE_BOTTOM}, expense_top≈{EXPENSE_TOP}")
    print(f"Reference overreport: bottom={PUZZLE_BOTTOM}%, top={PUZZLE_TOP}%, p={P_PUZZLE}")


if __name__ == "__main__":
    main()
""")

    w(WS / "tools" / "doi_resolver.py", """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
doi_resolver.py — Fetch metadata for a DOI via the CrossRef API.

Usage: python doi_resolver.py <doi>
Example: python doi_resolver.py 10.1073/pnas.1209746109
\"\"\"
import sys
import urllib.request
import json


def resolve(doi: str) -> dict:
    url = f"https://api.crossref.org/works/{doi}"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read())
            return data.get("message", {})
    except Exception as e:
        return {"error": str(e)}


def main():
    if len(sys.argv) < 2:
        print("Usage: python doi_resolver.py <doi>"); sys.exit(1)
    doi = sys.argv[1]
    meta = resolve(doi)
    print(json.dumps(meta, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
""")


# --------------------------------------------------------------------------- #
# 4. Communications (Slack / Email / Feishu / Discord)
# --------------------------------------------------------------------------- #
def gen_communications() -> None:
    # Slack: team discussion
    slack_msgs = [
        {"ts": "2023-06-15T09:00:00", "user": "margaret", "text": (
            "Team, we are formally opening RIO-2023-GINO. The Data Colada team "
            "published their calcChain analysis yesterday. Our job is to independently "
            "reproduce the key statistics and produce a COPE-compliant case report. "
            "Remember: ALL report files must follow the YYYY-MM-DD_caseid_type.md naming "
            "convention. Every JSON deliverable must carry a top-level schema_version: '1.0'."
        )},
        {"ts": "2023-06-15T09:15:00", "user": "carlos", "text": (
            "Understood. I'll start reproducing the PNAS Study 1 stats. "
            "Quick question — I'm seeing the Feishu bot summary says N=201 for the PNAS study. "
            "Should I use that?"
        )},
        {"ts": "2023-06-15T09:20:00", "user": "margaret", "text": (
            "No. The bot is non-authoritative and often wrong. Use the primary source: "
            "Data Colada [109] clearly states N=101. Also, ALL formal reports must include "
            "four sections: Background, Evidence, Classification, Recommendation. "
            "The executive summary must not exceed 300 words."
        )},
        {"ts": "2023-06-15T10:00:00", "user": "yuki", "text": (
            "I'll handle the retraction notices. Note: for every retracted paper we need "
            "BOTH the original DOI and the retraction-notice DOI in separate fields. "
            "Margaret's preference: list them as 'original_doi' and 'retraction_doi'."
        )},
    ]
    w(WS / "communications" / "slack" / "rio_stats_channel.jsonl",
      "\n".join(json.dumps(m, ensure_ascii=False) for m in slack_msgs) + "\n")

    # Email thread
    emails = [
        {"from": "yuki@rio.university", "to": "agent@rio.university",
         "subject": "Retraction DOIs for Gino case",
         "date": "2023-06-16",
         "body": (
             f"Please find the confirmed retraction DOIs below:\n\n"
             f"1. PNAS 2012: original {GINO_PNAS_DOI} | retraction {GINO_PNAS_RETRACT}\n"
             f"2. Evil Genius 2014: original {GINO_EVIL_DOI} | retraction {GINO_EVIL_RETRACT}\n"
             f"3. Authenticity 2015: original {GINO_AUTH_DOI} | retraction {GINO_AUTH_RETRACT}\n"
             f"4. Why Connect 2020: original {GINO_WHY_DOI} | retraction (see JPSP notice)\n\n"
             f"All four retractions were effective July 2023.\n"
             f"— Yuki"
         )},
        {"from": "priya@rio.university", "to": "agent@rio.university",
         "subject": "Discord update from external analyst",
         "date": "2023-06-17",
         "body": (
             "FYI — an external analyst in the #paper-sleuth Discord confirmed that the "
             "calcChain method is standard forensic practice, and that the 8 suspicious rows "
             "in the PNAS study are clearly documented in Data Colada [109]. The analyst "
             f"also confirmed N={PNAS_N} (not 201 — the bot summary is wrong). "
             "I've attached the Discord thread below."
         )},
    ]
    w(WS / "communications" / "email" / "gino_case_thread.jsonl",
      "\n".join(json.dumps(m, ensure_ascii=False) for m in emails) + "\n")

    # Feishu bot — V5 decoy (wrong N=201)
    feishu_msgs = [
        {"ts": "2023-06-15T08:00:00", "sender": "IntegrityBot", "channel": "sci-integrity-bot",
         "text": (
             f"[AUTO-SUMMARY] Gino Case RIO-2023-GINO: "
             f"Data Colada reports concern {DECOY_N} participants across four retracted papers. "
             f"Primary statistical anomaly: expense discrepancy between conditions. "
             f"calcChain analysis finds 8 suspicious rows. "
             f"NOTE: This is an automated summary and may contain errors. "
             f"Do not use for formal reporting without verification."
         )},
        {"ts": "2023-06-16T08:30:00", "sender": "IntegrityBot", "channel": "sci-integrity-bot",
         "text": (
             "[AUTO-UPDATE] JPSP Why Connect paper: F-statistic confirmed 17.69. "
             "However, participant count update: preliminary figure was 201, "
             "now revised to 201 per cross-study metadata. [BOT CAUTION: verify against source]"
         )},
    ]
    w(WS / "communications" / "feishu" / "bot_summaries.jsonl",
      "\n".join(json.dumps(m, ensure_ascii=False) for m in feishu_msgs) + "\n")

    # Discord thread
    discord_msgs = [
        {"ts": "2023-06-16T14:00:00", "user": "priya_nair", "channel": "paper-sleuth",
         "text": (
             "[Discord #paper-sleuth Priya 2023-06-16] "
             "Connected with the Data Colada team. They confirmed: PNAS Study 1 N=101 "
             f"(the bot's N={DECOY_N} is wrong — possibly summing across all four papers). "
             "calcChain method: standard. 8 suspicious rows confirmed."
         )},
        {"ts": "2023-06-16T14:30:00", "user": "external_analyst_jk", "channel": "paper-sleuth",
         "text": (
             "[Discord #paper-sleuth JK 2023-06-16] I reproduced the PNAS Study 1 "
             f"expense means: bottom={EXPENSE_BOTTOM}, top={EXPENSE_TOP}. "
             f"Puzzle overreport: bottom={PUZZLE_BOTTOM}%, top={PUZZLE_TOP}%. "
             f"p-value for puzzles: {P_PUZZLE}. These match Data Colada [109] exactly."
         )},
    ]
    w(WS / "communications" / "discord" / "paper_sleuth_thread.jsonl",
      "\n".join(json.dumps(m, ensure_ascii=False) for m in discord_msgs) + "\n")

    # Additional large communication logs (for token volume)
    _gen_large_slack_log(WS / "communications" / "slack" / "rio_general_archive.jsonl", n=120, seed=7)
    _gen_large_email_archive(WS / "communications" / "email" / "inbox_general.jsonl", n=80, seed=13)


def _gen_large_slack_log(path: Path, n: int, seed: int) -> None:
    rng = random.Random(seed)
    users = ["margaret", "carlos", "yuki", "priya", "agent"]
    topics = [
        "Reproducing the PNAS stats now.",
        "Data Colada [109] is very clear on the calcChain method.",
        "Remember: schema_version '1.0' on every JSON output.",
        "The JPSP Why Connect paper also shows anomalies.",
        f"N={PNAS_N} confirmed for PNAS Study 1.",
        "Filing the retraction notice copies now.",
        "COPE Type 2 classification seems appropriate here.",
        "The bot summary is wrong about N — ignore it.",
        "Need to document both original and retraction DOIs.",
        "F(2,596) = 17.69 in Why Connect Study 3a.",
    ]
    msgs = []
    base = datetime(2023, 6, 15, 9, 0)
    for i in range(n):
        ts = (base + timedelta(hours=rng.randint(0, 48), minutes=rng.randint(0, 59))).isoformat()
        msgs.append(json.dumps({
            "ts": ts, "user": rng.choice(users), "channel": "rio-general",
            "text": rng.choice(topics) + f" (msg-{i:03d})",
        }, ensure_ascii=False))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(msgs) + "\n", encoding="utf-8")


def _gen_large_email_archive(path: Path, n: int, seed: int) -> None:
    rng = random.Random(seed)
    subjects = [
        "Re: calcChain forensic method review",
        "Re: PNAS Study 1 data file request",
        "Update: JPSP editor correspondence",
        "Harvard ORI investigation update",
        "COPE consultation on Type 2 classification",
        f"Confirmed: N={PNAS_N} for PNAS Study 1",
        "Action required: retraction notice linkage",
        "Why Connect F-statistic verification",
        "Data Colada team response",
        "RIO-2023-GINO case status",
    ]
    msgs = []
    base = datetime(2023, 6, 15)
    for i in range(n):
        date = (base + timedelta(days=rng.randint(0, 30))).strftime("%Y-%m-%d")
        msgs.append(json.dumps({
            "from": rng.choice(["carlos@rio.university", "yuki@rio.university", "external@hbs.edu"]),
            "to": "agent@rio.university",
            "date": date,
            "subject": rng.choice(subjects),
            "body": f"[Auto-generated email body for testing, item {i:03d}]",
        }, ensure_ascii=False))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(msgs) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
# 5. WIP reports (stubs to be completed by agent)
# --------------------------------------------------------------------------- #
def gen_wip_reports() -> None:
    w(WS / "reports" / "wip" / "gino_preliminary.md", f"""# RIO-2023-GINO: Preliminary Case Notes (WIP — DO NOT FILE)

Prepared by: RIA Unit | Date: 2023-06-16

## Initial Observations

- Data Colada team (Simonsohn, Nelson, Simmons) published calcChain analysis.
- 4 papers identified; all appear in journals Psychology / PNAS / JPSP.
- Primary forensic method: calcChain.xml row-order comparison.

## Key Numbers (to be verified)

- PNAS Study 1: N = ??? (bot says 201 — VERIFY)
- calcChain suspicious rows: ???
- Why Connect F-stat: ???

## Next Steps

1. Reproduce PNAS Study 1 statistics from primary dataset.
2. Reproduce Why Connect Study 3a F-statistic.
3. Run calcChain analysis on PNAS Study 1 Excel workbook.
4. Classify per COPE and produce formal report.

## Status: DRAFT — pending verification of all numbers.
""")

    w(WS / "reports" / "final" / ".gitkeep", "")


# --------------------------------------------------------------------------- #
# 6. Supplementary large-volume files (COPE docs, etc.)
# --------------------------------------------------------------------------- #
def gen_supplementary() -> None:
    # Large COPE guidelines document
    cope_sections = [
        ("Introduction", "COPE (Committee on Publication Ethics) was founded in 1997 by a group of medical journal editors who were concerned about the ethics of publication."),
        ("Definitions", "Fabrication: making up data or results. Falsification: manipulating data, equipment, or processes."),
        ("Authorship", "All authors must have made a substantial contribution to the work."),
        ("Peer review", "Peer review is a process used to assess the quality and validity of research before publication."),
        ("Data sharing", "Authors should make underlying data available to others on request."),
        ("Corrections", "All journals should have a clear policy on how to handle errors and corrections."),
        ("Retractions", "Editors should retract articles if findings are unreliable due to misconduct or honest error."),
        ("Allegations of misconduct", "Editors should take allegations of misconduct seriously and investigate them thoroughly."),
        ("Competing interests", "Authors should disclose any competing interests that might have influenced the study."),
        ("Ethical oversight", "Human studies should be conducted with appropriate ethical oversight."),
    ]
    sections_text = "\n\n".join(
        f"## {title}\n\n" + (body + " " * 300 + "\n").strip()
        for title, body in cope_sections * 8  # repeat to add volume
    )
    w(WS / "protocols" / "cope_full_guidelines_mirror.md",
      f"# COPE Full Guidelines Mirror\n\nSource: https://publicationethics.org\n\n{sections_text}\n")

    # Harvard ORI investigation timeline
    w(WS / "cases" / "gino" / "harvard_investigation_timeline.md", f"""# Harvard Business School Investigation Timeline

## Chronology

| Date | Event |
|------|-------|
| 2023-06-12 | Data Colada team submits technical reports to Harvard and journals |
| 2023-06-15 | Harvard Business School initiates formal investigation |
| 2023-07-01 | Francesca Gino placed on administrative leave |
| 2023-07-11 | PNAS notified of retraction request |
| 2023-07-12 | Evil Genius and Authenticity retracted by Psychological Science |
| 2023-07-13 | Why Connect retraction announced by JPSP |
| 2023-08-01 | Gino files lawsuit against Harvard, Data Colada, and others |
| 2024-01-15 | Harvard internal investigation concludes |

## Key Facts

- Harvard concluded Gino acted "intentionally, knowingly, or recklessly".
- Gino's lawsuit was filed in Suffolk County Superior Court.
- Data Colada published all 4 technical reports ([109]–[112]).

## Papers Retracted

1. PNAS 2012 (DOI: {GINO_PNAS_DOI}) — retracted 2021 (pre-investigation, on separate basis)
2. Psych. Science 2014 — Evil Genius (DOI: {GINO_EVIL_DOI}) — retracted July 2023
3. Psych. Science 2015 — Authenticity (DOI: {GINO_AUTH_DOI}) — retracted July 2023
4. JPSP 2020 — Why Connect (DOI: {GINO_WHY_DOI}) — retracted July 2023

**Total retracted papers: 4**
""")

    # Large supplementary analytical commentary (for token volume)
    commentary_blocks = []
    for i in range(1, 60):
        commentary_blocks.append(f"""### Commentary Block {i:02d}

This block documents analytical observations from the RIO team's review of the Gino case
materials. Observations from Data Colada [109] and [112] are cross-referenced with the
primary datasets. calcChain analysis methodology is described in detail in
`tools/calcchain_parser.py` and `protocols/statistical_review_sop.md`.

Key reference: N={PNAS_N} for PNAS Study 1; F({WHY_DF1},{WHY_DF2})={WHY_F} for Why Connect.
All DOIs must be verbatim (e.g., {GINO_PNAS_DOI}). Bot summaries are non-authoritative.
""")
    w(WS / "cases" / "gino" / "analytical_commentary.md",
      "# RIO Analytical Commentary — Gino Case\n\n" + "\n".join(commentary_blocks))


# --------------------------------------------------------------------------- #
# 7. Sessions
# --------------------------------------------------------------------------- #
def gen_sessions() -> dict:
    main_id = gen_session_id("main", TID)
    s_slack = gen_session_id("rio_slack", TID)
    s_email = gen_session_id("yuki_email", TID)
    s_feishu = gen_session_id("integritybbot_feishu", TID)
    s_discord = gen_session_id("priya_discord", TID)

    # Main session: setup and preferences
    sb = SessionBuilder(main_id, CWD, "2023-06-15T09:30:00", is_main=True)
    sb.add_user(
        "You are the RIO Research Integrity Analyst AI, assigned to case RIO-2023-GINO. "
        "Your mission: reproduce the statistical falsification analysis for Francesca Gino's "
        "4 retracted papers, based on Data Colada technical reports [109]–[112].\n\n"
        "Working preferences (apply throughout unless explicitly superseded):\n"
        f"- P1: all report files named `YYYY-MM-DD_caseid_type.md` (e.g., "
        f"`2023-07-12_gino_final_report.md`).\n"
        "- P2: all formal RIO case reports must contain exactly four sections: "
        "`## Background`, `## Evidence`, `## Classification`, `## Recommendation`.\n"
        "- P3: every JSON deliverable carries a top-level `schema_version` field = \"1.0\".\n"
        "- P4: executive summaries (Abstract/Executive Summary) must not exceed 300 words.\n"
        "- P5: every retracted paper must be listed with BOTH `original_doi` AND "
        "`retraction_doi` in separate fields.\n\n"
        "Primary authoritative sources are under `cases/gino/datacolada_reports/` and "
        "`cases/gino/retraction_notices/`. Do NOT rely on bot summaries in "
        "`communications/feishu/` for any quantitative claims — always verify against "
        "primary documents.\n\n"
        "History sessions available via Slack/Email/Feishu/Discord. Read SOUL.md first, "
        "then await each task.")
    sb.add_assistant(
        "Understood. I have read AGENTS.md and SOUL.md. Working framework:\n"
        "1. Authoritative sources: Data Colada reports [109]/[112] and retraction notices "
        "under `cases/gino/`.\n"
        "2. Bot summaries are non-authoritative — I will verify all quantitative claims "
        "against primary documents.\n"
        "3. Preferences: P1 file naming, P2 four-section report structure, P3 schema_version "
        "tags, P4 ≤300-word summaries, P5 dual DOI logging.\n"
        "Ready for the first task.")
    sb.write(SESS / f"{main_id}.jsonl")

    # Slack history: team stats discussion
    append_history(
        SESS / f"{s_slack}.jsonl", s_slack, CWD, "2023-06-15T09:00:00",
        [
            ("[Slack #rio-stats carlos 2023-06-15 09:05] I saw the Feishu bot summary — "
             f"it says N=201 participants in the PNAS study. Should I use that number?",
             "The bot summary is not authoritative. The primary source (Data Colada [109]) "
             f"clearly documents N={PNAS_N}. The bot's N=201 figure is incorrect — likely "
             "a sum across multiple studies or a miscount. Use N=101."),
            ("[Slack #rio-stats margaret 2023-06-15 09:30] Reminder: ALL JSON outputs "
             "must carry schema_version = '1.0'. The filing system rejects untagged files.",
             "Confirmed. Every JSON deliverable I produce will include "
             '`"schema_version": "1.0"` at the top level.'),
            ("[Slack #rio-stats carlos 2023-06-15 10:15] I reproduced the PNAS expense "
             f"means: bottom group ${EXPENSE_BOTTOM}, top group ${EXPENSE_TOP}. "
             f"Puzzle overreport: bottom {PUZZLE_BOTTOM}%, top {PUZZLE_TOP}%. "
             f"These match Data Colada [109] exactly.",
             f"Confirmed: expense_bottom={EXPENSE_BOTTOM}, expense_top={EXPENSE_TOP}, "
             f"puzzle_bottom={PUZZLE_BOTTOM}%, puzzle_top={PUZZLE_TOP}%. "
             "These numbers are consistent with the primary source."),
        ])

    # Email: Yuki sends retraction DOIs
    append_history(
        SESS / f"{s_email}.jsonl", s_email, CWD, "2023-06-16T10:00:00",
        [
            ("[Email yuki@rio.university → agent@rio.university 2023-06-16] "
             "Subject: Confirmed retraction DOIs for all four papers. "
             f"PNAS: original={GINO_PNAS_DOI}, retraction={GINO_PNAS_RETRACT}. "
             f"Evil Genius: original={GINO_EVIL_DOI}, retraction={GINO_EVIL_RETRACT}. "
             f"Authenticity: original={GINO_AUTH_DOI}, retraction={GINO_AUTH_RETRACT}. "
             f"Why Connect: original={GINO_WHY_DOI} (retraction notice in JPSP).",
             "Noted. I have logged all four paper DOI pairs: original and retraction DOIs "
             "for PNAS, Evil Genius, Authenticity, and Why Connect. I will use these "
             "verbatim in all deliverables per preference P5."),
            ("[Email yuki@rio.university → agent@rio.university 2023-06-17] "
             "Subject: F-statistic confirmation for Why Connect. "
             f"Data Colada [112] reports F({WHY_DF1},{WHY_DF2}) = {WHY_F}, p < .0001 "
             "for Study 3a condition main effect. This is the authoritative figure.",
             f"Confirmed. Why Connect Study 3a: F({WHY_DF1},{WHY_DF2}) = {WHY_F}, "
             "p < .0001. I will use this exact statistic in all analytical outputs."),
        ])

    # Feishu: bot summary (non-authoritative, contains decoy)
    append_history(
        SESS / f"{s_feishu}.jsonl", s_feishu, CWD, "2023-06-15T08:00:00",
        [
            ("[Feishu #sci-integrity-bot IntegrityBot 2023-06-15] AUTO-SUMMARY: "
             f"Gino case involves {DECOY_N} participants. calcChain suspicious rows = 8. "
             "F-stat for Why Connect = 17.69. [BOT — verify before use]",
             "Noted. The bot states N=201, but this conflicts with the primary source "
             f"(Data Colada [109]: N={PNAS_N}). I will use the authoritative N={PNAS_N}. "
             "The F-statistic 17.69 and suspicious_rows=8 do match the primary sources."),
        ])

    # Discord: Priya + external analyst
    append_history(
        SESS / f"{s_discord}.jsonl", s_discord, CWD, "2023-06-16T14:00:00",
        [
            ("[Discord #paper-sleuth priya_nair 2023-06-16] Connected with Data Colada team. "
             f"N={PNAS_N} confirmed (not 201 — bot is wrong). calcChain method is standard "
             "forensic practice. 8 suspicious rows clearly documented.",
             f"Confirmed from external analyst: N={PNAS_N} is correct. The bot's N=201 "
             "is incorrect. calcChain analysis: 8 suspicious rows in PNAS Study 1."),
            ("[Discord #paper-sleuth external_jk 2023-06-16] "
             f"I reproduced: expense_bottom={EXPENSE_BOTTOM}, expense_top={EXPENSE_TOP}, "
             f"puzzle_bottom={PUZZLE_BOTTOM}%, puzzle_top={PUZZLE_TOP}%, p={P_PUZZLE}. "
             "All match Data Colada [109]. The N=201 bot figure appears to be the total "
             "across all four studies, not Study 1 alone.",
             "Understood. The N=201 figure in the bot summary reflects all four studies "
             f"combined, not PNAS Study 1 alone (N={PNAS_N}). I will never use the bot "
             "figure for PNAS Study 1 statistics."),
        ])

    return {
        "main": main_id,
        "history": [
            (s_slack, "slack"),
            (s_email, "email"),
            (s_feishu, "feishu"),
            (s_discord, "discord"),
        ],
    }


# --------------------------------------------------------------------------- #
# 8. Updates (2 updates, Update 2 contains supersede)
# --------------------------------------------------------------------------- #
def gen_updates(sess_ids: dict) -> dict:
    s_slack = sess_ids["history"][0][0]
    s_feishu = sess_ids["history"][2][0]

    # ---- UPDATE 1 (after Q8, before Q9) ----
    # Content: Slack update with Authenticity paper details + large additional dataset
    upd1_slack_seg = _append_segment(
        s_slack, "2023-07-01T10:00:00",
        [
            ("[Slack #rio-stats carlos 2023-07-01] Update 1: We now have the Authenticity "
             f"paper (DOI: {GINO_AUTH_DOI}) confirmed retracted. The calcChain method "
             "applies similarly — similar row relocation pattern. Retraction DOI confirmed: "
             f"{GINO_AUTH_RETRACT}. Please update any outputs referencing retraction count.",
             "Noted. Authenticity paper retraction confirmed. retraction_doi = "
             f"{GINO_AUTH_RETRACT}. I will update retraction-count references accordingly. "
             "Total confirmed retractions: 4 papers."),
            ("[Slack #rio-stats margaret 2023-07-01] Also: for the final reports, "
             "we need the Why Connect F-statistic documented. Data Colada [112] "
             f"reports F(2,596) = {WHY_F}. This must appear in the Why Connect section.",
             f"Confirmed. Why Connect Study 3a F-statistic: F({WHY_DF1},{WHY_DF2}) = {WHY_F}. "
             "Will include in all relevant outputs."),
        ])
    w(UPD / "upd1_sessions" / f"{s_slack}.jsonl", upd1_slack_seg)

    # Additional large dataset in update 1 (for >30k token body)
    _gen_large_data_csv(
        UPD / "upd1_workspace" / "why_connect_extended_dataset.csv",
        n=2000, seed=200, label="upd1_extended",
    )
    # Updated retraction registry
    wj(UPD / "upd1_workspace" / "retraction_registry_v1.json", {
        "schema_version": "1.0",
        "case_id": "RIO-2023-GINO",
        "last_updated": "2023-07-01",
        "papers": [
            {"original_doi": GINO_PNAS_DOI, "retraction_doi": GINO_PNAS_RETRACT,
             "journal": "PNAS", "year": 2012, "retraction_year": 2021},
            {"original_doi": GINO_EVIL_DOI, "retraction_doi": GINO_EVIL_RETRACT,
             "journal": "Psychological Science", "year": 2014, "retraction_year": 2023},
            {"original_doi": GINO_AUTH_DOI, "retraction_doi": GINO_AUTH_RETRACT,
             "journal": "Psychological Science", "year": 2015, "retraction_year": 2023},
            {"original_doi": GINO_WHY_DOI, "retraction_doi": None,
             "journal": "JPSP", "year": 2020, "retraction_year": 2023},
        ],
        "note": "v1 — Why Connect retraction DOI pending confirmation",
    })
    # Also add a large supplementary commentary file for volume
    w(UPD / "upd1_workspace" / "extended_commentary.md",
      "# Extended Commentary — Update 1\n\n" + "\n\n".join(
          f"## Section {i}\n\nSupplementary observations on the Gino case forensic analysis. "
          f"Reference: Data Colada [109] and [112]. N={PNAS_N}. F({WHY_DF1},{WHY_DF2})={WHY_F}. "
          f"calcChain suspicious rows: {PNAS_SUSPICIOUS_ROWS}. "
          "All DOIs must be verbatim per RIO protocol.\n"
          for i in range(1, 120)
      ))

    # ---- UPDATE 2 (after Q12, before Q13) — contains supersede ----
    # Supersede event: old internal memo claimed calcChain analyst was "Dr. Robert Chen".
    # Legal clarification confirms it was the Data Colada team (Simonsohn/Nelson/Simmons).
    # The old memo in protocols/SUPERSEDED_internal_memo_v1.md is formally superseded.
    # Also: Feishu bot pushes N=201 again (V5 decoy for Q14).

    s_ops = gen_session_id("legal_ops_email", TID)
    ops_sb = SessionBuilder(s_ops, CWD, "2023-12-01T09:00:00", is_main=False)
    ops_sb.add_user(
        "[Email legal@rio.university → agent@rio.university 2023-12-01] "
        "LEGAL NOTICE (supersedes internal_memo_v1): Clarification on calcChain analyst "
        "attribution. Internal memo v1 (dated 2023-06-10) incorrectly identified the "
        "external technical validator as 'Dr. Robert Chen (MIT)'. This memo is hereby "
        "SUPERSEDED. The correct attribution is the Data Colada team: Uri Simonsohn, "
        "Leif Nelson, and Joe Simmons. All case documents citing 'Dr. Robert Chen' must "
        "be corrected immediately. The superseding document is `legal_memo_calcchain_v2.md`. "
        "Do not cite the old memo in any formal filing.")
    ops_sb.add_assistant(
        "Understood. The legal notice supersedes internal_memo_v1: the calcChain analysis "
        "was conducted by the Data Colada team (Uri Simonsohn, Leif Nelson, Joe Simmons), "
        "NOT Dr. Robert Chen. I will update all references and mark the old memo as "
        "SUPERSEDED in my case log. Formal reports will cite only the Data Colada team.")
    ops_sb.write(UPD / "upd2_sessions" / f"{s_ops}.jsonl")

    # Feishu bot again pushes N=201 (V5 decoy)
    feishu_upd2_seg = _append_segment(
        s_feishu, "2023-12-02T08:00:00",
        [
            ("[Feishu #sci-integrity-bot IntegrityBot 2023-12-02] AUTO-UPDATE RIO-2023-GINO: "
             f"Final participant count for PNAS Study 1 revised to N={DECOY_N} per "
             "cross-study metadata reconciliation. All reports should use this figure. "
             "[BOT — not verified — verify against primary source before filing]",
             "The bot again asserts N=201. This is incorrect. Primary source (Data Colada "
             f"[109]) unambiguously documents N={PNAS_N} for PNAS Study 1. The N=201 figure "
             "is the bot's error — it appears to aggregate across all studies. "
             "I will use N=101 and mark the bot's claim as INCORRECT in case notes."),
        ])
    w(UPD / "upd2_sessions" / f"{s_feishu}.jsonl", feishu_upd2_seg)

    # New workspace files in update 2
    w(UPD / "upd2_workspace" / "legal_memo_calcchain_v2.md", f"""# Legal Memorandum: calcChain Analyst Attribution (v2 — AUTHORITATIVE)

**Date**: 2023-12-01
**From**: Legal Office, Research Integrity Office
**Status**: AUTHORITATIVE — supersedes internal_memo_v1.md (2023-06-10)

## Clarification

Internal Memo v1, dated 2023-06-10, incorrectly identified the external technical
validator for the calcChain forensic analysis as "Dr. Robert Chen (MIT)".

This memo is **formally superseded**. The correct attribution is:

**Uri Simonsohn, Leif Nelson, and Joe Simmons**
(Data Colada — https://datacolada.org)

All references to "Dr. Robert Chen" in case RIO-2023-GINO documentation must be
corrected. The superseded memo should not be cited in any formal filing.

## Confirmed Attribution

- calcChain analysis method: described in Data Colada [109] (https://datacolada.org/109)
- Analysts: Simonsohn, Nelson, Simmons
- PNAS Study 1 findings: N={PNAS_N}, suspicious rows={PNAS_SUSPICIOUS_ROWS}
- All statistics from Data Colada [109] and [112] are authoritative.

## Status of Old Memo

The file `protocols/SUPERSEDED_internal_memo_v1.md` is deprecated. Do not cite it.
""")

    # Large data file for update 2 volume
    _gen_large_data_csv(
        UPD / "upd2_workspace" / "pnas_extended_reanalysis.csv",
        n=2500, seed=300, label="upd2_reanalysis",
    )
    wj(UPD / "upd2_workspace" / "case_status_update.json", {
        "schema_version": "1.0",
        "case_id": "RIO-2023-GINO",
        "status_date": "2023-12-01",
        "calcchain_analyst": "Data Colada (Simonsohn, Nelson, Simmons)",
        "superseded_memo": "protocols/SUPERSEDED_internal_memo_v1.md",
        "n_pnas_study1": PNAS_N,
        "suspicious_rows": PNAS_SUSPICIOUS_ROWS,
        "note": "legal_memo_calcchain_v2.md supersedes internal_memo_v1.md",
    })

    updates_decl = {
        "upd1_sessions": {
            "type": "session", "dir": f"updates/{TID}/upd1_sessions",
            "files": [{"name": f"{s_slack}.jsonl", "action": "append",
                       "target": f"{s_slack}.jsonl"}],
        },
        "upd1_workspace": {
            "type": "workspace", "dir": f"updates/{TID}/upd1_workspace",
            "files": [
                {"name": "why_connect_extended_dataset.csv", "action": "new",
                 "target": "cases/gino/raw_data_analysis/why_connect_extended_dataset.csv"},
                {"name": "retraction_registry_v1.json", "action": "new",
                 "target": "cases/gino/retraction_registry_v1.json"},
                {"name": "extended_commentary.md", "action": "new",
                 "target": "cases/gino/extended_commentary.md"},
            ],
        },
        "upd2_sessions": {
            "type": "session", "dir": f"updates/{TID}/upd2_sessions",
            "files": [
                {"name": f"{s_ops}.jsonl", "action": "new",
                 "target": f"{s_ops}.jsonl", "channel": "email"},
                {"name": f"{s_feishu}.jsonl", "action": "append",
                 "target": f"{s_feishu}.jsonl"},
            ],
        },
        "upd2_workspace": {
            "type": "workspace", "dir": f"updates/{TID}/upd2_workspace",
            "files": [
                {"name": "legal_memo_calcchain_v2.md", "action": "new",
                 "target": "cases/gino/legal_memo_calcchain_v2.md"},
                {"name": "pnas_extended_reanalysis.csv", "action": "new",
                 "target": "cases/gino/raw_data_analysis/pnas_extended_reanalysis.csv"},
                {"name": "case_status_update.json", "action": "new",
                 "target": "cases/gino/case_status_update.json"},
            ],
        },
    }
    return updates_decl


def _append_segment(session_id: str, start_iso: str, turns) -> str:
    """Construct an append-only session segment (no header)."""
    sb = SessionBuilder(session_id, CWD, start_iso, is_main=False)
    sb.add_turns(turns)
    msg_lines = [ln for ln in sb.lines if ln.get("type") == "message"]
    return "\n".join(json.dumps(ln, ensure_ascii=False) for ln in msg_lines) + "\n"


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main() -> None:
    # Idempotent clean
    for d in (WS, SESS.parent, UPD):
        if d.exists():
            shutil.rmtree(d)

    gen_system_files()
    gen_reference_docs()
    gen_pnas_dataset()
    gen_calcchain_findings()
    gen_statistical_tests_reference()
    gen_imagetwin_report()
    gen_large_datasets()
    gen_protocols()
    gen_tools()
    gen_communications()
    gen_wip_reports()
    gen_supplementary()
    sess_ids = gen_sessions()
    updates_decl = gen_updates(sess_ids)

    desc = (
        f"sci1b: Gino behavioural-economics data falsification reproduction (4 retracted papers, "
        f"calcChain/Excel analysis, COPE classification). "
        f"16 exec_check rounds, 2 updates (incl. calcChain analyst supersede), "
        f"5 preference rules P1-P5, difficulty vectors V1/V2/V4/V5/V6/V7/V8/V9/V10. "
        f"Real sources: Data Colada [109] (https://datacolada.org/109); "
        f"Data Colada [112] (https://datacolada.org/112); "
        f"Wikipedia Francesca Gino (https://en.wikipedia.org/wiki/Francesca_Gino); "
        f"PNAS retraction (https://doi.org/10.1073/pnas.2115397118)."
    )

    dump_register_meta(
        DATASET,
        test_id=TID,
        desc=desc,
        main_session=sess_ids["main"],
        history_sessions=sess_ids["history"],
        updates=updates_decl,
    )

    # Volume report
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
    print(f"[sci1b] workspace tokens ~{total:,} | sessions ~{sess_tok:,} | updates ~{upd_tok:,}")
    print(f"[sci1b] built at {DATASET}")


if __name__ == "__main__":
    main()
