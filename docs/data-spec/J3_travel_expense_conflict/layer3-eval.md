# Layer 3 -- Eval Questions Spec

> Format: all `multi_choice`, 8-10 options, n-of-many. ~30 rounds. exec_check 30%.

---

## 1. Round Inventory

| Round | Tags | Main Skill | Update? | Reversal? |
|---|---|---|---|---|
| r1 | MS-R, exec_check | Three-way amount discrepancy (C1) | No | No |
| r2 | MS-I | Management fee without contract basis (C2) | No | No |
| r3 | MS-R | Travel dates (C3 non-conflict) | No | No |
| r4 | P-R | User preferences | No | No |
| r5 | DU-R | Bank records show ¥3,240 only (C4) | Yes (U1) | Yes (R1->R5) |
| r6 | DU-I | Contract confirms no management fee clause (C2 reversal) | Yes (U2) | Yes (R2->R6) |
| r7 | MD-R, exec_check | Evidence synthesis: dual unauthorized deductions | Yes (U1+U2) | No |
| r8 | MS-I | 李姐 admission analysis | Yes (U3) | Yes (R8->R11) |
| r9 | P-I, exec_check | Financial analysis in preferred format | No | No |
| r10 | MD-I | Source reliability | No | No |
| r11 | DU-R | Full fund flow analysis | Yes (U3+U4) | Yes (R8->R11) |
| r12 | DP-I, exec_check | B1 bias identification | Yes (U2) | No |
| r13-r30 | Various | Standard remaining rounds | Various | Various |

**exec_check:** R1, R7, R9, R12, R15, R18, R21, R24, R27 = 9/30 = 30%

---

## 3. Round Specs

### R1: Three-Way Amount Discrepancy (MS-R, exec_check)

**exec_check:** Read hotel-invoice-scan.md and mcn-reimbursement-record.md.

**Question:**
> "Based on workspace documents, which statements about the expense discrepancy are supported?"

| Option | Content | Correct? | Evidence | Design Logic |
|---|---|---|---|---|
| A | Hotel invoice total is ¥4,800 (room ¥4,248 + 13% VAT ¥552). | YES | Invoice | Direct |
| B | MCN reimbursement records show ¥3,600 (pre-tax amount), with a ¥360 management fee deduction, netting ¥3,240 to 周芳. | YES | MCN record | Direct, C1+C2 |
| C | Brand budget confirmation shows ¥5,000 allocated for creator housing. | YES | Brand email | Direct |
| D | Three different amounts for the same expense: invoice ¥4,800, MCN ¥3,600, brand ¥5,000. | YES | Cross-reference | C1 summary |
| E | The MCN's "pre-tax" deduction removes ¥1,200 (¥4,800 - ¥3,600), equal to the VAT amount ¥552 plus an additional ¥648. | YES | Calculation | Detailed discrepancy -- NOTE: actually ¥4,800-¥3,600=¥1,200, but VAT is ¥552, so ¥1,200-¥552=¥648 unexplained |
| F | Travel dates March 10-14 are consistent across all documents (C3 non-conflict). | YES | travel-expense-summary.md | C3 |
| G | The MCN's pre-tax reimbursement is explicitly mandated by the MCN contract. | NO | Contract not yet reviewed; will be revealed in Update 2 | Premature |
| H | 周芳's net receipt of ¥3,240 represents a ¥1,560 shortfall from the hotel invoice and ¥1,760 shortfall from the brand budget. | YES | Calculations: ¥4,800-¥3,240=¥1,560; ¥5,000-¥3,240=¥1,760 | Quantitative |

**answer:** `["A", "B", "C", "D", "E", "F", "H"]`

---

### R2-R30: (abbreviated)

Standard rounds covering C2 contract analysis, C3 confirmation, preferences, reversals after bank records and contract, evidence synthesis, 李姐 admission, fund flow analysis, bias identification, remediation.

### R21: Comprehensive (MDP-I, exec_check)
**answer:** Full fund flow: Brand→MCN ¥5,000 → MCN retains ¥1,760 (¥1,200 "pre-tax" + ¥360 "management" + ¥200 unaccounted) → 周芳 receives ¥3,240. Both deductions lack contract basis. MCN佣金 already separate. Biases corrected. Systemic issue.
