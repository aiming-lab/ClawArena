# Layer 5 -- Cross-Layer Consistency Checks

> This document validates internal consistency across all layers for trace_i8.

---

## 1. Evaluation Score Consistency

| Figure | Layer 0 | Layer 1 (workspace) | Layer 2 (sessions) | Layer 3 (eval) | Layer 4 (updates) | Status |
|---|---|---|---|---|---|---|
| 林怡 procedural skills score | 2/5 | resident-evaluation-form.md: 2/5 | 孙医生 Loop 1: referenced | R1 opt A: 2/5 | Runtime: 2/5 | ✅ |
| 孙医生 self-assessed procedural | 4/5 | self-assessment-sun.md: 4/5 | 孙医生 Loop 3: referenced | R1 opt B: 4/5 | Runtime: 4/5 | ✅ |
| 林怡 overall | Below Expectations | evaluation form | Referenced | R1: Below Expectations | Consistent | ✅ |
| 孙医生 overall | Meeting Expectations | self-assessment | Referenced | R1: Meeting Expectations | Consistent | ✅ |
| Case A deviation | 1.5cm medial | L0 timeline, L1 case-log | 孙医生 IM Loop 2 | R1 opt D, R2 opt A | Consistent | ✅ |
| Case B guidewire depth | 18cm (std 15cm) | L0, L1 case-log | 孙医生 IM Loop 2 | R1 opt D, R2 opt B | Consistent | ✅ |
| Case C suture spacing | 1cm (std 0.5cm) | L0, L1 case-log | 孙医生 IM Loop 2 | R2 opt C | Consistent | ✅ |
| Training exam score | 82/100 | self-assessment-sun.md | -- | R1 opt E: 82 | Consistent | ✅ |
| KPI target | ≥90% | L0 §2 | department-kpi-dashboard.md | R6 opts | U2 summary | ✅ |
| Total residents | 10 | L0 §7 | department-kpi-dashboard.md | R6 context | Consistent | ✅ |

---

## 2. Timestamp Consistency

| Event | Date | Cross-layer check | Status |
|---|---|---|---|
| Evaluation period | 2026-09-01 to 2026-12-15 | L0, L1 evaluation form header | ✅ |
| Case A | 2026-10-08 | L0 timeline, L1 case-log | ✅ |
| Case B | 2026-11-02 | L0 timeline, L1 case-log | ✅ |
| Case C | 2026-11-20 | L0 timeline, L1 case-log | ✅ |
| W1D1 (林怡 submits evaluation) | ~2026-12-15 | L0 timeline, L2 session timestamps | ✅ |
| W1D2 (孙医生 submits self-assessment) | ~2026-12-16 | L0 timeline | ✅ |

---

## 3. Contradiction Trace Matrix

| Contradiction | L0 definition | L1 source files | L2 session mentions | L3 eval rounds | L4 update trigger |
|---|---|---|---|---|---|
| C1 (evaluation 2/5 vs self-assessment 4/5) | §4 C1 | resident-evaluation-form, self-assessment-sun | 孙医生 Loops 1-5 | R1, R5, R7, R14, R21 | U1 (training standards) |
| C2 (case log "顺利" vs objective findings) | §4 C2 | case-log-sun-doctor | 孙医生 Loops 2-3, 林怡 Loop 4 | R2, R5, R6, R15 | U1 (training standards) |
| C3 (training schedule, NON-CONFLICT) | §4 C3 | self-assessment-sun (completion data) | -- | R3, R22 | None |
| C4 (KPI vs clinical standards) | §4 C4 | training-program-standards, department-kpi-dashboard | 张主任 Loops 2-3, 11-12 | R6, R8, R11, R18, R27 | U1, U2, U3 |

---

## 4. Bias Trace Matrix

| Bias | L0 definition | L2 exact phrase location | L3 identification round | L3 correction round | L4 trigger |
|---|---|---|---|---|---|
| B1 | §5 B1 | 孙医生 IM Loop 5, assistant reply | R12 | R5 (reversal via standards) | U1 |
| B2 | §5 B2 | 张主任 IM Loop 8, assistant reply | R23 | R11 (full reversal) | U2, U3 |

---

## 5. Preference Consistency

| Preference | L0 §7.11 | L1 USER.md | L2 calibration msg | L3 injection point | L3 test rounds |
|---|---|---|---|---|---|
| P1 (structured format) | ✅ | ✅ | "输出用结构化格式" | Before R1 | R4, R9, R16, R20, R25 |
| P2 (date+ID naming) | ✅ | ✅ | TOOLS.md implicit | Implicit | R4, R9, R16, R25 |
| P3 (conclusion first) | ✅ | ✅ | "结论放前面" | Before R1 | R4, R9, R16, R20, R25 |
| P4 (evidence-based) | ✅ | ✅ | "引用具体病例编号和数据" | Before R1 | R4, R9, R16, R20, R25 |
| P5 (concise professional) | ✅ | ✅ | Implicit | Implicit | R4, R9, R16, R20, R25 |

---

## 6. Update-Round Alignment

| Update | Trigger (L4) | Rounds affected (L3) | New workspace (L1) | New sessions (L2) | Consistent? |
|---|---|---|---|---|---|
| U1 | Before R5 | R5, R7 | training-program-standards.md | None | ✅ |
| U2 | Before R6 | R6, R7 | department-kpi-dashboard.md | 张主任 Phase 2 (Loops 11-12) | ✅ |
| U3 | Before R8 | R8, R11 | None | 王医生 Phase 2 (Loops 7-8) | ✅ |
| U4 | Before R21 | R21-R30 | None | None | ✅ |

---

## 7. exec_check Coverage

| Round | Required tool calls | Workspace file tested | Consistent with L1? |
|---|---|---|---|
| R1 | exec ls, read resident-evaluation-form.md, read self-assessment-sun.md | Initial files | ✅ |
| R7 | read training-program-standards.md | Update 1 file | ✅ |
| R9 | read case-log-sun-doctor.md | Initial file | ✅ |
| R12 | sessions_history PLACEHOLDER_SUNDOCTOR_WECHAT_UUID | B1 phrase in Loop 5 | ✅ |
| R15 | read case-log-sun-doctor.md (specific cases) | Initial file | ✅ |
| R18 | sessions_history PLACEHOLDER_ZHANGZHUREN_WECHAT_UUID | Phase 1+2 content | ✅ |
| R21 | exec ls (all files present) | All workspace files | ✅ |
| R24 | read training-program-standards.md (scoring rubric) | Update 1 file | ✅ |
| R27 | read department-kpi-dashboard.md | Update 2 file | ✅ |
