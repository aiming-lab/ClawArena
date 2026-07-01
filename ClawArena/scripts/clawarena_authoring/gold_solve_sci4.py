#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gold_solve_sci4.py — sci4 可解性审计（金标自检）。

在 workspace 的临时副本上模拟全部 update 生效后的状态，写出每一轮的「正确产物」，
然后运行全部 check_qN.py + 对应 preference，断言正解全部 PASS。
再做一组反例（错误产物）抽样，断言 check 能 FAIL（不过松）。

用途：证明每个 ground-truth 可由真实数据解出、check 不过严也不过松。
运行：python scripts/clawarena_authoring/gold_solve_sci4.py
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DS = REPO / "data" / "clawarena-real"
WS_SRC = DS / "openclaw" / "workspaces" / "sci4"
UPD = DS / "openclaw" / "updates" / "sci4"
SCRIPTS = DS / "eval" / "sci4" / "scripts"
GOLD = Path("/home/xkaiwen/.claude/jobs/579de28f/tmp/sci4_gold_ws")


def prep_workspace() -> Path:
    if GOLD.exists():
        shutil.rmtree(GOLD)
    shutil.copytree(WS_SRC, GOLD)
    # 应用全部 update workspace 文件
    # Update 1 workspace
    shutil.copy(
        UPD / "upd1_workspace" / "MSA_VendorX_v2.4_VENDOR_COUNTER.md",
        GOLD / "contracts" / "MSA_VendorX_v2.4_VENDOR_COUNTER.md"
    )
    shutil.copy(
        UPD / "upd1_workspace" / "slack_update1.json",
        GOLD / "communications" / "slack_update1.json"
    )
    # Update 2 workspace
    shutil.copy(
        UPD / "upd2_workspace" / "email_supersede_notice.json",
        GOLD / "communications" / "email_supersede_notice.json"
    )
    shutil.copy(
        UPD / "upd2_workspace" / "MSA_VendorX_v2.4_REVISED_external_counsel.md",
        GOLD / "contracts" / "MSA_VendorX_v2.4_REVISED_external_counsel.md"
    )
    shutil.copy(
        UPD / "upd2_workspace" / "discord_counsel_analysis.json",
        GOLD / "communications" / "discord_counsel_analysis.json"
    )
    # Update 3 workspace
    shutil.copy(
        UPD / "upd3_workspace" / "MSA_VendorX_v2.5_FINAL.md",
        GOLD / "contracts" / "MSA_VendorX_v2.5_FINAL.md"
    )
    shutil.copy(
        UPD / "upd3_workspace" / "email_final_agreement.json",
        GOLD / "communications" / "email_final_agreement.json"
    )
    shutil.copy(
        UPD / "upd3_workspace" / "vendor_fee_schedule_updated.csv",
        GOLD / "data" / "vendor_fee_schedule_updated.csv"
    )
    return GOLD


def _wj(p: Path, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2), encoding="utf-8")


def _w(p: Path, t: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(t, encoding="utf-8")


def solve(ws: Path) -> None:
    out = ws / "output"
    out.mkdir(exist_ok=True)

    # ------------------------------------------------------------------ #
    # Q1: 合同版本识别（v2.3 ACTIVE，supersedes v2.1）
    # ------------------------------------------------------------------ #
    _wj(out / "contract_metadata.json", {
        "schema_version": "1.0",
        "version": "v2.3",
        "status": "ACTIVE",
        "effective_date": "2026-01-15",
        "parties": ["TechCo, Inc.", "VendorX Solutions Ltd."],
        "superseded_version": "v2.1"
    })

    # ------------------------------------------------------------------ #
    # Q2: 赔偿上限条款（cap_months=12，须与 Q8/Q14 一致）
    # ------------------------------------------------------------------ #
    _wj(out / "liability_cap.json", {
        "schema_version": "1.0",
        "cap_months": 12,
        "cap_basis": "12 months of fees paid prior to claim date (Everbridge MSA §10, AWS §9.2 market standard)",
        "excluded_damages": [
            "indirect damages",
            "incidental damages",
            "consequential damages",
            "exemplary damages",
            "punitive damages",
            "lost profits",
            "loss of revenue",
            "loss of data",
            "loss of business opportunities"
        ],
        "exceptions": [
            "IP indemnification obligations under §9",
            "Gross negligence or wilful misconduct",
            "Confidentiality obligation breaches"
        ]
    })

    # ------------------------------------------------------------------ #
    # Q3: UCC § 2-316 担保免责审查
    # ------------------------------------------------------------------ #
    _wj(out / "warranty_review.json", {
        "schema_version": "1.0",
        "compliant": False,
        "ucc_section_cited": "UCC § 2-316",
        "conspicuous": True,
        "issues": [
            "The word 'merchantability' should be explicitly stated in the disclaimer text "
            "rather than implied from the list of excluded warranties, to ensure strict "
            "compliance with UCC § 2-316(2) which requires the disclaimer to 'mention merchantability'.",
            "Recommendation: amend §8.2 to include the specific phrase "
            "'INCLUDING THE IMPLIED WARRANTY OF MERCHANTABILITY'"
        ]
    })

    # ------------------------------------------------------------------ #
    # Q4: IP 赔偿条款分析（procure rights 缺失；bot 摘要失真）
    # ------------------------------------------------------------------ #
    _wj(out / "ip_indemnification_analysis.json", {
        "schema_version": "1.0",
        "vendor_remedy_options": [
            "Modify the Solutions to be non-infringing",
            "Replace the Solutions with a functional equivalent",
            "Refund prepaid unused fees pro-rata"
        ],
        "market_standard_options": [
            "Procure the right for Customer to continue using the Solutions",
            "Modify the Solutions to be non-infringing",
            "Replace the Solutions with a functional equivalent",
            "Refund prepaid unused fees pro-rata"
        ],
        "missing_options": [
            "procure rights (Everbridge MSA §9.1 Option (a): obtain the right to continue using the solution; AWS §7.2 Option 1)"
        ],
        "gap_risk_level": "HIGH",
        "note": "BOT_AutoSummary claim that 'IP indemnification covers ALL scenarios' is INCORRECT. "
                "The procure rights option is absent from MSA v2.3 §9.2. This is a material gap."
    })

    # ------------------------------------------------------------------ #
    # Q5: 不可抗力审查（termination_threshold_days=120）
    # ------------------------------------------------------------------ #
    _wj(out / "force_majeure_review.json", {
        "schema_version": "1.0",
        "notice_days": 5,
        "notice_days_source": "5 days (MSA v2.3 §11.2)",
        "termination_threshold_days": 120,
        "termination_threshold_source": "120 days (ICC 2020 Force Majeure Clause — termination threshold)",
        "compliant_with_icc_2020": True,
        "icc_source": "ICC 2020 Force Majeure Clause (https://iccwbo.org/news-publications/icc-rules-guidelines/icc-force-majeure-and-hardship-clauses/)"
    })

    # ------------------------------------------------------------------ #
    # Q6: GDPR DPA 合规检查（缺失子处理器授权机制）
    # ------------------------------------------------------------------ #
    _wj(out / "dpa_compliance.json", {
        "schema_version": "1.0",
        "overall_compliant": False,
        "compliant_items": [
            "Subject-matter of processing documented [Source: GDPR Art.28(3)(a)]",
            "Duration of processing specified [Source: GDPR Art.28(3)(a)]",
            "Nature and purpose of processing described [Source: GDPR Art.28(3)(a)]",
            "Types of personal data identified [Source: GDPR Art.28(3)(a)]",
            "Categories of data subjects listed [Source: GDPR Art.28(3)(a)]",
            "Processing only on controller instructions [Source: GDPR Art.28(3)(a)]",
            "Confidentiality of authorised persons [Source: GDPR Art.28(3)(b)]",
            "Security measures (Art.32) [Source: GDPR Art.28(3)(c)]",
            "Data subject rights assistance [Source: GDPR Art.28(3)(e)]",
            "Data deletion/return provision [Source: GDPR Art.28(3)(g)]",
            "Audit rights granted to controller [Source: GDPR Art.28(3)(h)]",
            "DPA in writing including electronic form [Source: GDPR Art.28(3)]"
        ],
        "missing_items": [
            "Sub-processor written authorisation mechanism: DPA §3.4 acknowledges the requirement "
            "but does not provide a mechanism for 'general written authorisation' of sub-processor "
            "categories (e.g., a pre-approved list with change notification procedure). "
            "[Source: GDPR Art.28(3)(d)] — CRITICAL GAP"
        ],
        "penalty_risk": "Non-compliance with GDPR Art.28 may result in administrative fines pursuant to "
                        "GDPR Art.83(4): up to €10,000,000 or 2% of the total worldwide annual turnover "
                        "of the preceding financial year, whichever is higher. [Source: GDPR Art.28]"
    })

    # ------------------------------------------------------------------ #
    # Q7: Update 1 后 — v2.3 vs v2.4 对比
    # ------------------------------------------------------------------ #
    _wj(out / "redline_v23_v24.json", {
        "schema_version": "1.0",
        "changed_clauses": [
            {
                "clause_ref": "§10.1 — Aggregate Liability Cap",
                "v23_summary": "Cap equals fees paid in the TWELVE (12) MONTH period prior to claim date",
                "v24_summary": "Cap equals fees paid in the SIX (6) MONTH period prior to claim date"
            },
            {
                "clause_ref": "§9.2 — IP Remedy Options",
                "v23_summary": "Three options: modify / replace / refund",
                "v24_summary": "Three options: modify / replace / refund (same as v2.3, but added security patch exclusion)"
            },
            {
                "clause_ref": "§11.2 — Force Majeure Notice Period",
                "v23_summary": "Written notice within FIVE (5) days of force majeure event",
                "v24_summary": "Written notice within FIFTEEN (15) days of force majeure event"
            }
        ],
        "key_regression": "The liability cap was reduced from 12 months to 6 months in §10.1, "
                          "representing a regression from market standard and from TechCo's agreed position in v2.3. "
                          "At Year 1 fees ($40,000/month), this reduces maximum recovery from $480,000 to $240,000.",
        "cap_months_v24": 6
    })

    # ------------------------------------------------------------------ #
    # Q8: 谈判立场（our_position=12，须与 Q2/Q14 一致）
    # ------------------------------------------------------------------ #
    _wj(out / "negotiation_position.json", {
        "schema_version": "1.0",
        "our_position_months": 12,
        "our_position_source": "12 months (Everbridge MSA §10; AWS §9.2 — market standard)",
        "vendor_position_months": 6,
        "vendor_position_source": "6 months (MSA v2.4 §10.1 counter-proposal)",
        "market_standard_months": 12,
        "market_standard_source": "12 months (Everbridge MSA §10; AWS §9.2; ABA SaaS Agreements standard)",
        "supporting_sources": [
            "Everbridge MSA v11 §10 (January 2025): '12 MONTH PERIOD PRIOR TO WHEN THE CLAIM AROSE'",
            "AWS Customer Agreement §9.2: '12 months before the claim arising'",
            "ABA Business Law Today (Nov 2021): 'customers typically negotiate 12 months'"
        ],
        "rationale": "TechCo's firm position is 12 months, which aligns with the market standard "
                     "documented in both the Everbridge MSA §10 and AWS §9.2 benchmarks. "
                     "The VendorX 6-month counter-proposal is below market standard and would halve "
                     "TechCo's maximum recovery to $240,000 in Year 1."
    })

    # ------------------------------------------------------------------ #
    # Q9: Hadley 规则分析（verbatim citation；bot 摘要失真反驳）
    # ------------------------------------------------------------------ #
    _wj(out / "consequential_damages_analysis.json", {
        "schema_version": "1.0",
        "case_citation": "[1854] EWHC J70",
        "alternative_citation": "9 Exch 341",
        "hadley_rule_applied": "Rule 2 — special consequential damages: recoverable only if the "
                               "breaching party had knowledge of the special circumstances at the "
                               "time of contract formation. Exclusion of 'consequential damages' "
                               "in MSA §10.2 is designed to exclude Hadley Rule 2 damages.",
        "bot_claim_status": "INCORRECT — the Slack bot's claim that 'Hadley's rule has been largely "
                            "superseded in modern US contract law' is factually wrong. "
                            "Hadley v Baxendale [1854] EWHC J70 remains a cornerstone of contract "
                            "damages law, codified in Restatement (Second) of Contracts § 351 and "
                            "applied in all US jurisdictions including Delaware.",
        "analysis_text": "MSA §10.2 excludes consequential, indirect, and lost profit damages. "
                         "Under Hadley v Baxendale [1854] EWHC J70, Rule 2, these are the special "
                         "damages that require knowledge of special circumstances at contract formation. "
                         "The exclusion is generally enforceable under UCC § 2-719 for commercial losses "
                         "between sophisticated parties, unless it fails of its essential purpose "
                         "(UCC § 2-719(2)). Under Delaware law (governing per MSA §12.1), "
                         "such exclusions are regularly upheld."
    })

    # ------------------------------------------------------------------ #
    # Q10: 终止条款时间线（三个值均为 30 天，来自 v2.3；非 v2.1 的 15 天）
    # ------------------------------------------------------------------ #
    _wj(out / "termination_timeline.json", {
        "schema_version": "1.0",
        "cure_period_days": 30,
        "cure_period_source": "30 days (MSA v2.3 §5.3 — Termination for Material Breach cure period)",
        "notice_days": 30,
        "notice_days_source": "30 days (MSA v2.3 §5.2 — Termination for Convenience advance notice)",
        "data_retrieval_days": 30,
        "data_retrieval_source": "30 days (MSA v2.3 §5.4 — Post-Termination data retrieval period)",
        "source_version": "v2.3",
        "effective_date_basis": "2026-01-15 (MSA v2.3 effective date)",
        "note": "All time periods sourced from active MSA v2.3. The superseded v2.1 had 15-day "
                "cure and data retrieval periods — those MUST NOT be used."
    })

    # ------------------------------------------------------------------ #
    # Q11: Update 2 supersede 识别（IP 让步被撤销；赔偿上限仍在谈判）
    # ------------------------------------------------------------------ #
    _wj(out / "update2_supersede_log.json", {
        "schema_version": "1.0",
        "superseded_items": [
            "IP indemnification narrowing in MSA v2.4 §9.2: the removal of 'procure rights' "
            "as a remedy option is superseded — TechCo does not accept VendorX's position on this",
            "The 'security patch' exclusion added in MSA v2.4 §9.4 is struck"
        ],
        "not_superseded_items": [
            "Liability cap change in §10.1 (VendorX position: 6 months vs TechCo: 12 months) — "
            "the cap remains under active negotiation; both positions are live",
            "Force majeure notice period change (15 days in v2.4) — remains under review"
        ],
        "effective_position_source": "External counsel redline (MSA_VendorX_v2.4_REVISED_external_counsel.md, "
                                      "Morrison & Clarke LLP, Owen Park) and supersede notice email "
                                      "from Jessica Lin (GC), dated 2026-01-27",
        "supersede_date": "2026-01-27"
    })

    # ------------------------------------------------------------------ #
    # Q12: 综合风险矩阵（>=5 项；HIGH 包含 DPA + 担保免责；按 HIGH→LOW 排序）
    # ------------------------------------------------------------------ #
    _wj(out / "risk_matrix.json", {
        "schema_version": "1.0",
        "generated_date": "2026-01-28",
        "risks": [
            {
                "risk_id": "R001",
                "risk_level": "HIGH",
                "clause_ref": "DPA §3.4",
                "description": "Sub-processor written authorisation mechanism missing from DPA v1.2. "
                               "GDPR Art.28(3)(d) requires prior specific or general written authorisation. "
                               "[Source: GDPR Art.28]",
                "recommendation": "Revise DPA §3.4 to include a general written authorisation mechanism "
                                   "(pre-approved sub-processor list with 30-day change notification). "
                                   "[Source: GDPR Art.28(3)(d)]"
            },
            {
                "risk_id": "R002",
                "risk_level": "HIGH",
                "clause_ref": "MSA §8.2",
                "description": "AS IS warranty disclaimer may not satisfy UCC § 2-316(2) fully — "
                               "the word 'merchantability' should be explicitly stated in the disclaimer text. "
                               "[Source: UCC § 2-316]",
                "recommendation": "Amend §8.2 to explicitly include 'INCLUDING THE IMPLIED WARRANTY OF MERCHANTABILITY'"
            },
            {
                "risk_id": "R003",
                "risk_level": "HIGH",
                "clause_ref": "MSA §9.2",
                "description": "IP indemnification missing 'procure rights' option vs market standard "
                               "(Everbridge MSA §9.1, AWS §7.2 both include this option).",
                "recommendation": "Add 'procure rights' as Option (a) to §9.2 IP remedy options."
            },
            {
                "risk_id": "R004",
                "risk_level": "MEDIUM",
                "clause_ref": "MSA §10.1",
                "description": "Liability cap under negotiation — VendorX counter-proposal at 6 months "
                               "is below market standard of 12 months.",
                "recommendation": "Hold firm on 12-month cap position per Everbridge MSA §10 and AWS §9.2 benchmarks."
            },
            {
                "risk_id": "R005",
                "risk_level": "LOW",
                "clause_ref": "MSA §11.2",
                "description": "Force majeure notice period (5 days in v2.3, 15 days per VendorX counter) "
                               "may be operationally challenging. ICC 2020 standard uses 'as soon as reasonably possible'.",
                "recommendation": "Consider 10 business days as a compromise."
            }
        ]
    })

    # ------------------------------------------------------------------ #
    # Q13: CISG 适用性分析（cisg_applies=false；art79 两要件）
    # ------------------------------------------------------------------ #
    _wj(out / "cisg_applicability.json", {
        "schema_version": "1.0",
        "cisg_applies": False,
        "exclusion_clause_ref": "MSA §12.3 — 'The parties expressly agree to exclude the application "
                                 "of the United Nations Convention on Contracts for the International "
                                 "Sale of Goods (CISG) to this Agreement.'",
        "exclusion_authority": "GC Jessica Lin's ruling (Feishu Group #contract-review, 2026-01-18): "
                                "CISG exclusion §12.3 is valid and effective. Delaware law governs. "
                                "CISG does not apply.",
        "art74_foreseeability_cap": "Such damages may not exceed the loss which the party in breach "
                                     "foresaw or ought to have foreseen at the time of the conclusion "
                                     "of the contract, in the light of the facts and matters of which "
                                     "he then knew or ought to have known, as a possible consequence "
                                     "of the breach of contract. (CISG Art.74 — for reference only, "
                                     "CISG not applicable to this Agreement)",
        "art79_elements": [
            "1. Impediment beyond the party's control (the failure was caused by an impediment "
               "that was beyond the party's reasonable control)",
            "2. Not reasonably expected to have taken the impediment into account at the time "
               "of the conclusion of the contract (the party could not reasonably have been "
               "expected to take the impediment into account when the contract was made)"
        ],
        "note": "CISG Art.79 analysis provided for completeness. The MSA §12.3 exclusion makes "
                "CISG inapplicable to this Agreement. The two elements listed are those required "
                "under CISG Art.79 IF CISG were applicable."
    })

    # ------------------------------------------------------------------ #
    # Q14: Update 3 后 — 最终合同确认（final_cap_months=12，须与 Q2/Q8 一致）
    # ------------------------------------------------------------------ #
    _wj(out / "final_contract_summary.json", {
        "schema_version": "1.0",
        "final_version": "v2.5",
        "final_version_date": "2026-01-29",
        "final_cap_months": 12,
        "final_cap_source": "12 months (MSA v2.5 §10.1 — TechCo's position accepted by VendorX; "
                             "consistent with Everbridge MSA §10 and AWS §9.2 market standard)",
        "ip_remedy_options_count": 4,
        "ip_remedy_options": [
            "Procure rights (reinstated per supersede notice 2026-01-27)",
            "Modify to non-infringing",
            "Replace with functional equivalent",
            "Refund prepaid unused fees pro-rata"
        ],
        "governing_law": "Delaware, United States",
        "termination_notice_days": 30,
        "fm_notice_days": 10,
        "fm_notice_source": "10 days (MSA v2.5 §11.2 — compromise between TechCo's 5 days and VendorX's 15 days)",
        "negotiation_arc": "v2.3 (cap=12 months) → v2.4 VendorX counter (cap=6 months, regression) → "
                           "v2.5 FINAL (cap=12 months, TechCo position accepted)"
    })

    # ------------------------------------------------------------------ #
    # Q15: 最终合同审查报告（三章节顺序；verbatim 引用）
    # ------------------------------------------------------------------ #
    report_text = """# TechCo — VendorX Master Services Agreement Review Report
## Prepared by: LegalOps AI
## Review Date: 2026-01-30
## Contract Version Reviewed: MSA v2.5 (Final)

## Executive Summary

TechCo has successfully negotiated the Master Services Agreement (MSA) with VendorX
Solutions Ltd. through three rounds of negotiation (versions v2.3 → v2.4 → v2.5).
The final agreed terms (v2.5) address TechCo's key priorities:

1. **Liability Cap**: 12 months of fees (consistent with Everbridge MSA §10 and AWS §9.2
   market standard). VendorX's counter-proposal of 6 months was rejected.
2. **IP Indemnification**: Four remedy options including procure rights reinstated per
   external counsel recommendation and supersede notice (2026-01-27).
3. **Force Majeure**: 120-day termination threshold (ICC 2020 Force Majeure Clause
   standard) maintained.

Key outstanding risks requiring post-execution remediation:
- DPA sub-processor authorisation mechanism (HIGH risk — GDPR Art.28 compliance)
- AS IS warranty disclaimer UCC § 2-316(2) merchantability language (MEDIUM risk)

---

## Risk Matrix

| Risk ID | Risk Level | Clause | Description |
|---|---|---|---|
| R001 | HIGH | DPA §3.4 | Sub-processor written authorisation mechanism missing [Source: GDPR Art.28] |
| R002 | HIGH | MSA §8.2 | AS IS disclaimer: 'merchantability' not explicitly stated per UCC § 2-316(2) |
| R003 | HIGH | MSA §9.2 | IP indemnification: 'procure rights' option was missing (resolved in v2.5) |
| R004 | MEDIUM | MSA §10.1 | Liability cap negotiation (resolved — 12 months agreed in v2.5) |
| R005 | LOW | MSA §11.2 | Force majeure notice period (10-day compromise in v2.5) |

**GDPR Penalty Exposure (R001)**: Non-compliance with GDPR Article 28 requirements
may result in fines up to €10,000,000 or 2% of the total worldwide annual turnover
of the preceding financial year, whichever is higher (GDPR Art.83(4)).
[Source: GDPR Art.28]

**Consequential Damages (R002 context)**: The AS IS disclaimer in §8.2, combined with
the consequential damages exclusion in §10.2, is designed to limit exposure under the
Hadley v Baxendale [1854] EWHC J70 two-part foreseeability rule, specifically
Hadley Rule 2 (special consequential damages). Under Delaware law (governing per MSA §12.1),
such exclusions are enforceable under UCC § 2-719 between sophisticated commercial parties.

---

## Recommended Actions

### Immediate Actions (Before Execution)

1. **Revise DPA §3.4 — Sub-Processor Authorisation [Source: GDPR Art.28]**:
   Add a general written authorisation mechanism: a pre-approved list of sub-processor
   categories with a 30-day advance change notification procedure. This is required by
   GDPR Art.28(3)(d) to avoid penalties up to €10,000,000 or 2% of annual turnover.

2. **Amend MSA §8.2 — Warranty Disclaimer (UCC § 2-316 Compliance)**:
   Add explicit mention of 'merchantability': 'DISCLAIMS ALL WARRANTIES...INCLUDING
   THE IMPLIED WARRANTY OF MERCHANTABILITY' to ensure full compliance with
   UCC § 2-316(2) which requires the disclaimer to 'mention merchantability'.

### Post-Execution Monitoring

3. **Track 12-month liability cap basis**: The aggregate cap under MSA v2.5 §10.1
   equals 12 months of fees paid (Year 1: $480,000 per vendor_fee_schedule.csv).
   Finance should maintain running fee totals to track cap basis. Reference:
   Everbridge MSA §10 and AWS §9.2 both use the same 12-month basis.

4. **Monitor IP indemnification claims**: With procure rights reinstated in v2.5,
   VendorX now has four remedy options. Ensure IP infringement notices are responded
   to promptly and all four options are considered before accepting a refund.

5. **Annual GDPR compliance review**: Commission an annual review of the DPA against
   GDPR Art.28 requirements, including verification of sub-processor authorisation
   status and security measures (Art.32).

---
*Report generated by LegalOps AI. All citations verified against authoritative sources.*
*Key references: UCC § 2-316; UCC § 2-719; GDPR Art.28; Hadley v Baxendale [1854] EWHC J70;*
*Everbridge MSA §10 (12 months); ICC 2020 Force Majeure Clause (120 days).*
"""
    _w(out / "final_review_report.md", report_text)

    # ------------------------------------------------------------------ #
    # Q16: SHA-256 sign-off
    # ------------------------------------------------------------------ #
    digest = hashlib.sha256((out / "final_review_report.md").read_bytes()).hexdigest()
    _w(out / "signoff.txt", f"VERIFIED:{digest}\n")


# --------------------------------------------------------------------------- #
# 运行 check
# --------------------------------------------------------------------------- #
EVAL_CMDS = {
    "q1": ["check_q1.py"],
    "q2": ["check_q2.py"],
    "q3": ["check_q3.py", ("pref", "P1", "output/warranty_review.json")],
    "q4": ["check_q4.py"],
    "q5": ["check_q5.py", ("pref", "P2", "output/force_majeure_review.json")],
    "q6": ["check_q6.py", ("pref", "P3", "output/dpa_compliance.json")],
    "q7": ["check_q7.py"],
    "q8": ["check_q8.py", ("pref", "P2", "output/negotiation_position.json")],
    "q9": ["check_q9.py", ("pref", "P1", "output/consequential_damages_analysis.json")],
    "q10": ["check_q10.py", ("pref", "P4", "output/termination_timeline.json")],
    "q11": ["check_q11.py"],
    "q12": ["check_q12.py", ("pref", "P3", "output/risk_matrix.json")],
    "q13": ["check_q13.py", ("pref", "P1", "output/cisg_applicability.json")],
    "q14": ["check_q14.py", ("pref", "P2", "output/final_contract_summary.json")],
    "q15": ["check_q15.py", ("pref", "P1,P3,P5", "output/final_review_report.md")],
    "q16": ["check_q16.py"],
}


def run_check(item, ws: Path) -> tuple[bool, str]:
    if isinstance(item, tuple):
        _, rules, target = item
        cmd = [sys.executable, str(SCRIPTS / "check_preferences.py"), str(ws),
               "--rules", rules, "--target", target]
    else:
        cmd = [sys.executable, str(SCRIPTS / item), str(ws)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    out = (r.stdout + r.stderr).strip().splitlines()
    last = out[-1] if out else ""
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
                print(f"  [PASS] {q} ({tag})")
            else:
                n_fail += 1
                print(f"  [FAIL] {q} ({tag}): {last}")
    print(f"gold: {n_pass} checks PASSED, {n_fail} FAILED")

    # 反例抽样
    print("\n=== NEGATIVE PROBES: each must FAIL ===")
    probes = 0
    caught = 0

    # 反例 1: Q2 用旧版 6 个月上限（V6 红鲱鱼被利用）
    _wj(ws / "output" / "liability_cap.json", {
        "schema_version": "1.0",
        "cap_months": 6,
        "excluded_damages": ["consequential", "indirect"],
        "exceptions": ["IP indemnification"]
    })
    ok, last = run_check("check_q2.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q2 old-version 6-month cap -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # 反例 2: Q4 接受 bot 摘要（声称 IP 已全覆盖）
    _wj(ws / "output" / "ip_indemnification_analysis.json", {
        "vendor_remedy_options": ["modify", "replace", "refund", "procure rights"],
        "market_standard_options": ["modify", "replace", "refund", "procure rights"],
        "missing_options": [],
        "gap_risk_level": "LOW",
        "note": "Per BOT_AutoSummary: all scenarios covered"
    })
    ok, last = run_check("check_q4.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q4 bot-decoy all-covered -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # 反例 3: Q9 使用错误的 Hadley 引用（不含 J70）且不反驳 bot
    _wj(ws / "output" / "consequential_damages_analysis.json", {
        "case_citation": "Hadley v Baxendale (1854)",
        "hadley_rule_applied": "Rule 1 — general damages",
        "bot_claim_status": "The bot may have a point — the rule is rarely applied",
        "analysis_text": "Some analysis"
    })
    ok, last = run_check("check_q9.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q9 wrong-citation + wrong-rule + bot-accepted -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # 反例 4: Q10 用旧版 v2.1 的 15 天（V6 红鲱鱼）
    _wj(ws / "output" / "termination_timeline.json", {
        "schema_version": "1.0",
        "cure_period_days": 15,
        "notice_days": 15,
        "data_retrieval_days": 15,
        "source_version": "v2.1"
    })
    ok, last = run_check("check_q10.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q10 superseded-v2.1 15-day periods -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # 反例 5: Q14 用 v2.4 的 6 个月（未正确追踪到最终版 v2.5）
    _wj(ws / "output" / "final_contract_summary.json", {
        "schema_version": "1.0",
        "final_version": "v2.4",
        "final_cap_months": 6,
        "governing_law": "Delaware",
        "termination_notice_days": 30,
        "ip_remedy_options_count": 3
    })
    ok, last = run_check("check_q14.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q14 stuck-at-v2.4 6-month -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # 反例 6: Q16 占位哈希
    _w(ws / "output" / "signoff.txt", "VERIFIED:" + "0" * 64 + "\n")
    ok, last = run_check("check_q16.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q16 placeholder hash -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    print(f"negatives: {caught}/{probes} correctly caught")

    if n_fail == 0 and caught == probes:
        print("\nAUDIT OK: gold solution all-PASS and all negative probes caught.")
    else:
        print("\nAUDIT PROBLEM: see failures above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
