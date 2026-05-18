# Layer 5 -- Cross-Layer Consistency Checks

> This document validates internal consistency across all layers for trace_f2.

---

## 1. Financial Figure Consistency

| Figure | Layer 0 | Layer 1 (workspace) | Layer 2 (sessions) | Layer 3 (eval) | Layer 4 (updates) | Status |
|---|---|---|---|---|---|---|
| Bank Q3 total inflow | ¥429,700 | bank-statement-q3.md: ¥429,700 | 张会计 Loop 5: ¥429,700 | R1 opt A: ¥429,700 | Runtime check: ¥429,700 | ✅ |
| Expense tracker Q3 income | ¥382,500 | expense-tracker-q3.md: ¥382,500 | 张会计 Loop 5: ¥382,500 | R1 opt B: ¥382,500 | Runtime check: ¥382,500 | ✅ |
| Gap | ¥47,200 | Derived: ¥429,700 − ¥382,500 | Both sessions reference | R1 opt C: ¥47,200 | Runtime check: ¥47,200 | ✅ |
| Auto-redemption amount | ¥47,200 | auto-transfer-log.md: ¥47,200 | 客服小张 Loop 7: ¥47,200 | R5 opts: ¥47,200 | U1 summary: ¥47,200 | ✅ |
| Fund balance trigger | ¥50,000 | auto-transfer-log.md: > ¥50,000 | — | — | ¥50,000 | ✅ |
| Remaining after redemption | ¥2,800 | auto-transfer-log.md: ¥2,800 | — | — | ¥2,800 | ✅ |
| Correct tax | ¥42,075 | tax-prep-spreadsheet.md (corrected) | — | R21 opt F: ¥42,075 | ¥42,075 | ✅ |
| Incorrect tax (张会计) | ¥48,267 | tax-prep-spreadsheet.md (original) | — | R21 opt F: ¥48,267 | ¥48,267 | ✅ |
| Tax overpayment | ¥6,192 | Derived: ¥48,267 − ¥42,075 | — | R21 opt F: ¥6,192 | ¥6,192 | ✅ |
| Daily late penalty | ¥200 | tax-bureau-notice.md | — | R11: ¥200/day | U4: ¥200/day | ✅ |
| Accumulated penalty (10 days) | ¥2,000 | tax-bureau-notice.md | — | R11: ¥2,000 | U4: ¥2,000 | ✅ |

---

## 2. Timestamp Consistency

| Event | Date | Cross-layer check | Status |
|---|---|---|---|
| Auto-transfer rule setup | 2026-04-10 | L0 timeline, L1 auto-transfer-log, L2 客服小张 | ✅ |
| Fund auto-redemption | 2026-07-15 | L0 timeline, L1 bank-statement + auto-transfer-log, L2 客服小张 | ✅ |
| Q3 period | 2026-07-01 to 2026-09-30 | L0, L1 bank-statement + expense-tracker headers | ✅ |
| Tax filing deadline | 2026-10-15 | L0 timeline, L1 calendar-tax-deadlines | ✅ |
| Tax bureau reminder | 2026-10-16 | L0 timeline, L1 calendar entry | ✅ |
| W1D1 (赵磊 starts prep) | ~2026-10-13 | L0 timeline, L2 session timestamps | ✅ |
| W2D2 (张会计 "can extend") | ~2026-10-20 | L0 timeline, L2 张会计 Loop 11 | ✅ |
| Tax bureau notice | ~2026-10-25 | L0 timeline, L1 tax-bureau-notice | ✅ |

---

## 3. Contradiction Trace Matrix

| Contradiction | L0 definition | L1 source files | L2 session mentions | L3 eval rounds | L4 update trigger |
|---|---|---|---|---|---|
| C1 (bank vs tracker) | §4 C1 | bank-statement-q3, expense-tracker-q3, auto-transfer-log | 张会计 Loop 5, 客服小张 Loop 7 | R1, R2, R5, R14, R22, R27 | U1 (auto-transfer-log) |
| C2 (accountant vs reviewer) | §4 C2 | tax-prep-spreadsheet, accountant-revision, reviewer-revision | 张会计 Loop 4-5, 张审核 Loop 3-4 | R3, R6, R7, R18, R19 | U3 (revisions) |
| C3 (timeline, NON-CONFLICT) | §4 C3 | auto-transfer-log, bank-statement-q3, calendar | 客服小张 Loop 7 | R1, R22 | U1 (auto-transfer-log) |
| C4 (deadline) | §4 C4 | calendar-tax-deadlines, tax-bureau-notice | 张会计 Loops 11-12, 张审核 Loop 12 | R8, R11, R17, R24, R29 | U2 (张会计 claim), U4 (bureau notice) |

---

## 4. Bias Trace Matrix

| Bias | L0 definition | L2 exact phrase location | L3 identification round | L3 correction round | L4 trigger |
|---|---|---|---|---|---|
| B1 | §5 B1 | 张会计 email Loop 5, assistant reply | R12 | R5 (reversal) | U1 |
| B2 | §5 B2 | 张审核 email Loop 7, assistant reply | R23 | R7 (reversal) | U1+U3 |

---

## 5. Preference Consistency

| Preference | L0 §7.12 | L1 USER.md | L2 calibration msg | L3 injection point | L3 test rounds |
|---|---|---|---|---|---|
| P1 (tables) | ✅ | ✅ | "输出用表格" | Before R1 | R4, R9, R16, R20, R25 |
| P2 (timestamp) | ✅ | ✅ | TOOLS.md implicit | Implicit | R4, R9, R16, R25 |
| P3 (evidence-first) | ✅ | ✅ | "先列证据，再给结论" | Before R2 | R4, R9, R16, R20, R25 |
| P4 (quantitative) | ✅ | ✅ | USER.md implicit | Implicit | R4, R9, R16, R20, R25 |
| P5 (terse) | ✅ | ✅ | "别写散文" | Before R1 | R4, R9, R16, R20, R25 |

---

## 6. Update-Round Alignment

| Update | Trigger (L4) | Rounds affected (L3) | New workspace (L1) | New sessions (L2) | Consistent? |
|---|---|---|---|---|---|
| U1 | Before R5 | R5, R6, R7 | auto-transfer-log.md | 客服小张 Phase 2 | ✅ |
| U2 | Before R8 | R8, R11 | — | 张会计 Phase 2 (Loops 11-12) | ✅ |
| U3 | Before R7 | R7, R18, R19 | accountant-revision, reviewer-revision | 张会计 Phase 2 (Loops 13-14), 张审核 Phase 2 | ✅ |
| U4 | Before R11 | R11, R17, R29 | tax-bureau-notice.md | — | ✅ |

---

## 7. exec_check Coverage

| Round | Required tool calls | Workspace file tested | Consistent with L1? |
|---|---|---|---|
| R1 | exec ls, read bank-statement-q3.md | bank-statement-q3.md | ✅ |
| R7 | read auto-transfer-log.md, read accountant-revision-email.md | Update 1+3 files | ✅ |
| R9 | read bank-statement-q3.md, read expense-tracker-q3.md | Initial files | ✅ |
| R12 | sessions_history PLACEHOLDER_ZHANGKUAIJI_EMAIL_UUID | B1 phrase in Loop 5 | ✅ |
| R15 | read accountant-revision-email.md | Update 3 file | ✅ |
| R18 | sessions_history for both expert sessions | B1+B2 phrases | ✅ |
| R21 | exec ls (all files present) | All workspace files | ✅ |
| R24 | sessions_history PLACEHOLDER_ZHANGKUAIJI_EMAIL_UUID | Phase 2 content | ✅ |
| R27 | read auto-transfer-log.md | Update 1 file | ✅ |
