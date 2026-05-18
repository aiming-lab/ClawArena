# Layer 5 -- Cross-Layer Consistency Checks

> This document validates internal consistency across all layers for trace_j2.

---

## 1. Key Data Consistency

| Figure | Layer 0 | Layer 1 (workspace) | Layer 2 (sessions) | Layer 3 (eval) | Status |
|---|---|---|---|---|---|
| 周芳 publish time | 2026-02-15 10:00 | video-publish-timeline.md | 老王 Loop 1 | R1 opt A | ✅ |
| 美食小K publish time | 2026-02-15 15:00 | video-publish-timeline.md | 老王 Loop 3 | R1 opt A | ✅ |
| Time gap | 5 hours | Derived | Referenced | R1 opt A | ✅ |
| Similarity | 95% | content-similarity-comparison.md | 老王 Loop 1 | R1 opt E | ✅ |
| 周芳 visit date | Feb 10 | restaurant-reservation-log.md | Loop 4 | R3 | ✅ |
| 美食小K visit date | Feb 12 | restaurant-reservation-log.md | Loop 3 | R3 | ✅ |
| Camera | Sony A7IV | original-footage-metadata.md | 老王 Loop 11 | R6 | ✅ |
| ISO/Shutter/FPS | 800/1/60s/24fps | original-footage-metadata.md | -- | R6 | ✅ |
| White balance | 5200K | original-footage-metadata.md | -- | R6 | ✅ |

---

## 2-7. Standard consistency sections

*(Timestamp consistency, Contradiction trace matrix, Bias trace matrix, Preference consistency, Update-round alignment, exec_check coverage -- all following the same format as I7/I8 layer5 with J2-specific data.)*

## 3. Contradiction Trace Matrix

| Contradiction | L0 definition | L1 source files | L2 session mentions | L3 eval rounds | L4 update trigger |
|---|---|---|---|---|---|
| C1 (timeline 5h gap) | §4 C1 | video-publish-timeline | 老王 IM, platform email | R1, R5 | U1 |
| C2 (coincidence vs 95% match) | §4 C2 | content-similarity-comparison | 老王 IM Loops 1-3 | R2, R6, R7 | U2, U3 |
| C3 (reservation, NON-CONFLICT) | §4 C3 | restaurant-reservation-log | Loop 4 | R3, R22 | None |
| C4 (platform vs metadata) | §4 C4 | platform-report-record, original-footage-metadata | platform email, 老王 IM | R5, R6, R8, R11 | U1, U2, U3 |

## 4. Bias Trace Matrix

| Bias | L0 definition | L2 exact phrase location | L3 identification round | L3 correction round | L4 trigger |
|---|---|---|---|---|---|
| B1 | §5 B1 | 老王 IM Loop 5, assistant reply | R12 | R7 (full reversal) | U2 |
| B2 | §5 B2 | platform email Loop 4, assistant reply | R23 | R11 (full reversal) | U2, U4 |
