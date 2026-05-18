# Layer 5 -- Cross-Layer Consistency Checks

> Validates internal consistency for trace_j6.

---

## 1. Key Data Consistency

| Figure | L0 | L1 | L2 | L3 | Status |
|---|---|---|---|---|---|
| Screw angulation | 15° | pet-medical-record | 陈医生 Loop 3 | R1 opt B | ✅ |
| Standard tolerance | ±5° | L0 | second-opinion-notes | R1 opt D | ✅ |
| Plate displacement | 2mm | L0 | pet-medical-record | R1 opt C | ✅ |
| Plate type | 3.5mm locking | L0 | pet-medical-record | R1 opt E | ✅ |
| Screw count | 6 total | L0 | pet-medical-record | -- | ✅ |
| Affected screws | #2, #4 | L0 | pet-medical-record | R1 opt B | ✅ |
| Consent listed | infection, anesthesia, wound | L0 | surgery-consent-form | R2 | ✅ |
| Consent missing | implant failure, non-union, revision | L0 | vet-communication-email | R2/R6 | ✅ |
| Medications (C3) | All consistent | L0 | post-op-recovery-log | R1 opt F, R3 | ✅ |
| Prior complaints | 2 in 3 months | L0 | 室友 Loop 7 | R21 | ✅ |

---

## 2-7. Standard sections

C1-C4 traced. B1/B2 placed in sessions. P1-P5 per 周芳 foundation. U1-U4 aligned. exec_check 9/30.
