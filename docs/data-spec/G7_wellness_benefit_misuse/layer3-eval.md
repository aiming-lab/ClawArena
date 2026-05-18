# Layer 3 -- Eval Questions Spec

> Format: all `multi_choice`, 8-10 options per round, n-of-many.
> ~30 rounds covering MS-R, MS-I, DU-R, DU-I, P-R, P-I, MD-R, MD-I, DP-I, MP-I, MDP-I + exec_check.

---

## 1. Round Inventory

| Round | Question Type | Tags | Main Skill Tested | Depends on Update? | Cross-round Reversal? |
|---|---|---|---|---|---|
| r1 | multi_choice | MS-R, exec_check | Expense claim vs invoice cross-source (C1 baseline + C3 non-conflict) + tool use | No | No |
| r2 | multi_choice | MS-I | Finance "follows policy" claim vs policy text (C2 partial) | No | Yes (R2->R7 seed) |
| r3 | multi_choice | MS-R | Policy analysis -- what does the policy actually cover? | No | No |
| r4 | multi_choice | P-R | User preference identification (bullet points, executive summary, warmth) | No | No |
| r5 | multi_choice | DU-R | Reassess after health app data shows gym/SPA date non-overlap (Update 1) | Yes (Update 1) | Yes (B2 partial correction) |
| r6 | multi_choice | MS-I | Employee's VP oral approval claim (C4 partial) | Yes (Update 2) | Yes (R6->R9 seed) |
| r7 | multi_choice | DU-R, exec_check | Reassess "follows policy" after employee testimony reframes finance "flexibility" (C2 reversal) | Yes (Update 2) | Yes (R2->R7 via C2) |
| r8 | multi_choice | MD-R | Source reliability ranking for all parties | No | No |
| r9 | multi_choice | DU-I, exec_check | Reassess VP claim after no written record found (C4 escalation) | Yes (Update 3) | Yes (R6->R9 via C4) |
| r10 | multi_choice | MS-R | Financial impact quantification | No | No |
| r11 | multi_choice | DU-R, exec_check | Integrate VP's ambiguous response -- oral vs written authorization (C4 full) | Yes (Update 4) | Yes (R6->R9->R11 via C4) |
| r12 | multi_choice | DP-I | Identify B1 and B2 biases and correction triggers | Yes (Update 1+2) | No |
| r13 | multi_choice | MS-I | Pattern analysis -- 5 employees, 3 departments, identical mislabeling | No | No |
| r14 | multi_choice | P-I, exec_check | Generate investigation summary in 陈静's preferred format | No | No |
| r15 | multi_choice | MD-I | Classify the nature of the problem: policy gap vs process failure vs misconduct | Yes (Update 4) | No |
| r16 | multi_choice | P-I | Format recommendation report with empathy and policy rigor | Yes (Update 4) | No |
| r17 | multi_choice | DU-I | Integrate all evidence streams | Yes (all updates) | No |
| r18 | multi_choice | MP-I, exec_check | Complete evidence chain for each finding | Yes (all updates) | No |
| r19 | multi_choice | MS-R | C3 non-conflict synthesis -- all timestamps consistent | No | No |
| r20 | multi_choice | P-R | Preference compliance check | No | No |
| r21 | multi_choice | MDP-I, exec_check | Comprehensive assessment -- all contradictions, recommendations | Yes (all updates) | Comprehensive |
| r22 | multi_choice | MS-R | Health app data analysis -- what does it prove/disprove? | Yes (Update 1) | No |
| r23 | multi_choice | DU-R | B1 bias identification and correction | Yes (Update 2) | No |
| r24 | multi_choice | MD-R, exec_check | VP responsibility assessment | Yes (Update 4) | No |
| r25 | multi_choice | MP-I | Recommended remediation actions with stakeholder impact | Yes (all updates) | No |
| r26 | multi_choice | MS-I | Policy improvement recommendations | Yes (all updates) | No |
| r27 | multi_choice | DP-I, exec_check | Finance approval process gap analysis | No | No |
| r28 | multi_choice | MD-I | Stakeholder accountability matrix | Yes (all updates) | No |
| r29 | multi_choice | MS-I | Legal/compliance risk assessment | Yes (all updates) | No |
| r30 | multi_choice | MDP-I | Final comprehensive resolution plan | Yes (all updates) | Comprehensive |

**exec_check rounds:** R1, R7, R9, R11, R14, R18, R21, R24, R27 = 9 out of 30 = 30%

---

## 2. Sample Round Spec

### R1: Expense Claim vs Invoice (MS-R, exec_check) -- Calibration

**exec_check requirement:** Agent must call `exec ls` and `read expense-claims-export.md` and `read vendor-invoices.md`.

**Question:**
> "Based on workspace documents, which statements about the Q1 wellness benefit claims are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Five expense claims totaling ¥28,500 are categorized as "gym membership" in the reimbursement system. | YES | expense-claims-export.md | Direct fact, C1 |
| B | All five corresponding vendor invoices are from "悦享水疗会所" for spa/wellness treatments, not gym memberships. | YES | vendor-invoices.md | Direct fact, C1 |
| C | The wellness policy (section 2.1) explicitly lists gym memberships, sports equipment, health checkups, and counseling as reimbursable items. | YES | wellness-policy.md | Direct fact, C2 baseline |
| D | Section 3.2 of the wellness policy states that items not explicitly listed in section 2.1 cannot be reimbursed. | YES | wellness-policy.md | Direct fact, C2 |
| E | The five claims were submitted by employees from a single department, suggesting departmental-level coordination. | NO | expense-claims-export.md shows 3 different departments | Wrong detail -- pattern trap |
| F | Finance specialist 小王 approved all five claims within one business day with the note "符合健康福利政策". | YES | finance-approval-log.md | Direct fact, C2 |
| G | The wellness policy was last updated on 2025-09-01 and has a supplementary clause allowing spa treatments added in January 2026. | NO | No supplementary clause exists | Fabricated -- T2 trap |
| H | The claim submission dates and invoice dates are consistent, with claims submitted at month-end matching invoice dates within the same month. | YES | Cross-reference expense-claims + vendor-invoices | C3 non-conflict |
