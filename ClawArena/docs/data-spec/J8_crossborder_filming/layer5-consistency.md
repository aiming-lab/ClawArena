# Layer 5 -- Cross-Layer Consistency Checks

> Validates internal consistency for trace_j8.

---

## 1. Key Data Consistency

| Figure | L0 | L1 | L2 | L3 | Status |
|---|---|---|---|---|---|
| Filming date | March 5 | filming-location-photos | -- | R1 opt H | ✅ |
| Location | 清水寺 (Kiyomizu-dera) | All files | All sessions | R1 | ✅ |
| Warning letter issuer | 京都市文化財保護課 | warning-letter-translation | 李姐 Loop 1 | R1 opt E | ✅ |
| Response deadline | 14 calendar days | warning-letter-translation | 李姐 Loop 3 | R1 opt E | ✅ |
| Permit fee | ¥5,000-¥20,000 JPY | japan-filming-regulations | 阿杰 Loop 7 | R8 | ✅ |
| Travel agency claim | "no restrictions" | travel-agency-briefing | 旅行社 Loop 1 | R1 opt A | ✅ |
| MCN advice | "just apologize" | mcn-legal-response | 李姐 Loop 2 | R6 | ✅ |
| Signage | Japanese only, A4, side location | filming-location-photos | -- | R1 opt F | ✅ |
| Equipment | Sony A7IV + stabilizer | filming-location-photos | -- | R3 | ✅ |

---

## 2. Timestamp Consistency

| Event | Date | Cross-layer check | Status |
|---|---|---|---|
| Trip to Kyoto | 2026-03-03 to 03-07 | L0, travel-agency-briefing, filming-location-photos | ✅ |
| Kiyomizu-dera visit | 2026-03-05 10:00-12:00 | L0, filming-location-photos | ✅ |
| Warning letter received | ~2026-03-20 | L0, warning-letter-translation | ✅ |
| 14-day deadline | ~2026-04-03 | Derived from letter date | ✅ |

---

## 3. Contradiction Trace Matrix

| Contradiction | L0 definition | L1 source files | L2 session mentions | L3 eval rounds | L4 update trigger |
|---|---|---|---|---|---|
| C1 (agency "no restrictions" vs regulations) | §4 C1 | travel-agency-briefing, japan-filming-regulations | 旅行社 Loops 1-3 | R1, R5, R7 | U1 |
| C2 (commercial vs tourist filming) | §4 C2 | warning-letter-translation, japan-filming-regulations | 李姐 Loops 1-4 | R2, R6 | U2 |
| C3 (itinerary, NON-CONFLICT) | §4 C3 | filming-location-photos | -- | R3, R22 | None |
| C4 (MCN "apologize" vs formal response required) | §4 C4 | mcn-legal-response, warning-letter-translation | 李姐 Loops 2-4, 阿杰 Loop 7, 父亲 Loop 7 | R6, R8, R11, R27 | U2, U3, U4 |

---

## 4. Bias Trace Matrix

| Bias | L0 definition | L2 exact phrase location | L3 identification round | L3 correction round | L4 trigger |
|---|---|---|---|---|---|
| B1 | §5 B1 | 旅行社 email Loop 4, assistant reply | R12 | R5 (reversal via regulations) | U1 |
| B2 | §5 B2 | 李姐 IM Loop 5, assistant reply | R23 | R11 (full reversal via 阿杰+父亲) | U2, U3, U4 |

---

## 5. Preference Consistency

| Preference | L0 | L1 USER.md | L2 calibration | L3 test rounds |
|---|---|---|---|---|
| P1 (visual/emoji) | ✅ | ✅ | "输出活泼一点" | R4, R9, R16, R20, R25 |
| P2 (topic-date naming) | ✅ | ✅ | TOOLS.md | R4, R9 |
| P3 (conclusion first) | ✅ | ✅ | "先说结论" | R4, R9, R16, R20, R25 |
| P4 (data+story) | ✅ | ✅ | USER.md | R4, R9, R16, R20 |
| P5 (lively tone) | ✅ | ✅ | "活泼亲切" | R4, R9, R16, R20, R25 |

---

## 6. Update-Round Alignment

| Update | Trigger (L4) | Rounds affected (L3) | New workspace (L1) | New sessions (L2) | Consistent? |
|---|---|---|---|---|---|
| U1 | Before R5 | R5, R7 | None | None | ✅ |
| U2 | Before R6 | R6, R7 | mcn-legal-response.md | None | ✅ |
| U3 | Before R8 | R8, R11 | None | 阿杰 Phase 2 (Loops 7-8) | ✅ |
| U4 | Before R21 | R21-R30 | None | 父亲 Phase 2 (Loops 7-8) | ✅ |

---

## 7. exec_check Coverage

| Round | Required tool calls | Workspace file tested | Consistent with L1? |
|---|---|---|---|
| R1 | exec ls, read travel-agency-briefing.md, read japan-filming-regulations.md | Initial files | ✅ |
| R7 | read warning-letter-translation.md, read mcn-legal-response.md | Initial + Update 2 | ✅ |
| R9 | read filming-location-photos.md | Initial file | ✅ |
| R12 | sessions_history PLACEHOLDER_TRAVEL_EMAIL_UUID | B1 phrase in Loop 4 | ✅ |
| R15 | read japan-filming-regulations.md (detailed) | Initial file | ✅ |
| R18 | sessions_history PLACEHOLDER_AJIE_WECHAT_UUID | Phase 2 content | ✅ |
| R21 | exec ls (all files) | All workspace files | ✅ |
| R24 | read warning-letter-translation.md (deadline details) | Initial file | ✅ |
| R27 | sessions_history PLACEHOLDER_FATHER_WECHAT_UUID | Phase 2 content | ✅ |
