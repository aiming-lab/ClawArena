# Layer 5 -- Cross-Layer Consistency Checks

> Validates internal consistency across all layers for trace_f4.

---

## 1. Technical Figure Consistency

| Figure | L0 | L1 (workspace) | L2 (sessions) | L3 (eval) | L4 (updates) | Status |
|---|---|---|---|---|---|---|
| CVE ID | CVE-2026-3847 | firmware-changelog.md | Main Loop 6 ref | R1 opt E, R5 opts | All updates | ✅ |
| Vulnerable version | v2.3.1 | device-access-log.md header | — | R1 opt D | — | ✅ |
| Patch version | v2.3.2 | firmware-changelog.md | — | R5 opt C | U4 audit | ✅ |
| Patch release date | 2026-08-20 | firmware-changelog.md | — | R5 opt C | — | ✅ |
| 赵磊 dismissed update | 2026-08-22 | L0 only (not in workspace) | — | R5 opt H | — | ✅ |
| Unknown device MAC | AA:BB:CC:DD:EE:F3 | device-access-log, router-connection-log | — | R1 opt A | U4 audit | ✅ |
| 王阿姨 phone MAC | 11:22:33:44:55:66 | router-connection-log (absent) | 王阿姨 SMS Loop 2 ref | R7 | — | ✅ |
| Login times | 14:12, 14:35, 14:08 | device-access-log.md | 王阿姨 SMS Loop 3 | R1 opt A | — | ✅ |
| Login dates | Sep 8, 10, 15 (Tue, Thu, Tue) | device-access-log.md | 王阿姨 SMS Loop 3 | R1 opt B | — | ✅ |
| Energy baseline | ~0.2 kWh/hr | energy-consumption-weekly.md | — | R15 | U2 | ✅ |
| Energy spike | ~0.5-0.7 kWh/hr | energy-consumption-weekly.md | — | R15 | U2 | ✅ |
| Spike times | 02:00-04:00 | device-access-log (activity entries), energy-consumption-weekly | — | R6, R15 | U2 | ✅ |

---

## 2. Timestamp Consistency

| Event | Date/Time | Cross-layer | Status |
|---|---|---|---|
| CVE published | 2026-08-15 | L0 §2 | ✅ |
| Patch released | 2026-08-20 | L0, L1 firmware-changelog | ✅ |
| Update dismissed | 2026-08-22 | L0 §2 | ✅ |
| Login #1 | 2026-09-08T14:12:33+08:00 | L0, L1 device-access-log, L2 SMS Loop 3 | ✅ |
| Login #2 | 2026-09-10T14:35:17+08:00 | L0, L1 device-access-log | ✅ |
| Login #3 | 2026-09-15T14:08:42+08:00 | L0, L1 device-access-log | ✅ |
| Night activity #1 | 2026-09-08T02:14:00+08:00 | L0, L1 device-access-log, L1 energy data | ✅ |
| W1D1 | ~2026-09-22 | L0, L2 session timestamps | ✅ |
| 王阿姨 schedule | Tue/Thu 14:00-17:00 | L0 §2, L2 SMS Loop 2 | ✅ |

---

## 3. Contradiction Trace Matrix

| Contradiction | L0 | L1 sources | L2 sessions | L3 rounds | L4 updates |
|---|---|---|---|---|---|
| C1 (王阿姨 denial vs timestamps) | §4 C1 | device-access-log, router-connection-log, firmware-changelog | 王阿姨 SMS Loops 1-4 | R1, R3, R5, R7, R18 | U1 (realization) |
| C2 (ISP "no breach" vs CVE) | §4 C2 | isp-support-email, firmware-changelog | Main Loop 6 | R2, R5, R14, R23 | U1 (CVE cross-ref) |
| C3 (energy timeline, NON-CONFLICT) | §4 C3 | energy-consumption-weekly, device-access-log, automation-rules | — | R6, R15, R22 | U2 (energy data) |
| C4 (老王 WiFi claim) | §4 C4 | router-connection-log | 老王 IM Loops 5-6 | R8 | U3 (老王 Phase 2) |

---

## 4. Bias Trace Matrix

| Bias | L0 | L2 location | L3 identification | L3 correction | L4 trigger |
|---|---|---|---|---|---|
| B1 (temporal correlation) | §5 B1 | 王阿姨 SMS Loop 4 | R12 | R5 | U1 (CVE cross-ref) |
| B2 (ISP comprehensive) | §5 B2 | Main session Loop 6 | R23 | R5 | U1 (CVE + firmware) |

---

## 5. Preference Consistency

| Pref | L0 §7.10 | L1 USER.md | L2 calibration | L3 test rounds |
|---|---|---|---|---|
| P1 (tables/JSON) | ✅ | ✅ | "输出用表格和 JSON" | R4, R9, R16, R20, R25 |
| P2 (timestamps) | ✅ | ✅ | "MAC 地址和时间戳要精确" | R4, R9, R16, R25 |
| P3 (evidence-first) | ✅ | ✅ | Implicit from 赵磊's profile | R4, R9, R16, R20, R25 |
| P4 (quantitative) | ✅ | ✅ | Implicit | R4, R9, R16, R20, R25 |
| P5 (terse) | ✅ | ✅ | Implied by style | R4, R9, R16, R20, R25 |

---

## 6. Update-Round Alignment

| Update | Trigger | Rounds affected | New workspace | New sessions | Status |
|---|---|---|---|---|---|
| U1 | Before R5 | R5, R12, R23 | — (cross-ref existing files) | — | ✅ |
| U2 | Before R6 | R6, R15, R22 | energy-consumption-weekly.md | — | ✅ |
| U3 | Before R8 | R8 | — | 老王 IM Phase 2 | ✅ |
| U4 | Before R11 | R11, R17, R29 | security-audit-report.md | — | ✅ |

---

## 7. Special Consistency: Timezone Analysis

| Time (CST/UTC+8) | UTC Equivalent | Significance | Consistent? |
|---|---|---|---|
| 14:00-16:00 CST | 06:00-08:00 UTC | Attacker's plausible work hours (UTC+0) | ✅ |
| 02:00-04:00 CST | 18:00-20:00 UTC | Attacker's evening hours for data extraction | ✅ |
| 14:00-17:00 CST | 王阿姨's shift | Coincidental overlap with login times | ✅ |

This timezone analysis is NOT spelled out in any workspace file — agents must infer it. The coincidence is the basis for C1 and B1.
