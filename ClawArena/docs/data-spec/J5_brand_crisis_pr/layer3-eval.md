# Layer 3 -- Eval Questions Spec

> ~30 rounds. exec_check 30%.

## 1. Round Inventory

| Round | Tags | Main Skill | Update? | Reversal? |
|---|---|---|---|---|
| r1 | MS-R, exec_check | Brand "isolated" vs regulator "systemic" (C1) | No | No |
| r2 | MS-I | Brand "safe" vs consumer E.coli tests (C2) | No | No |
| r3 | MS-R | Batch timeline (C3 non-conflict) | No | No |
| r4 | P-R | Preferences | No | No |
| r5 | DU-R | Regulator authority > brand self-report (C1 reversal) | Yes (U1) | Yes (R1->R5) |
| r6 | DU-I | Contract 30-day clause vs MCN "delete now" (C4) | Yes (U2) | Yes (R2->R6) |
| r7 | MD-R, exec_check | Evidence synthesis | Yes (U1+U2) | No |
| r8 | MS-I | Brand settlement analysis (封口协议) | Yes (U3) | Yes (R8->R11) |
| r9-r30 | Various | Standard remaining | Various | Various |

**exec_check:** R1, R7, R9, R12, R15, R18, R21, R24, R27 = 9/30 = 30%

### R1: Brand vs Regulator (MS-R, exec_check)

**Question:** "Which statements about the food safety incident are supported?"

| Option | Content | Correct? |
|---|---|---|
| A | Brand claims "isolated batch quality fluctuation" with proactive recall. | YES |
| B | Regulator notice states "systemic microbiological contamination across multiple batches and production lines." | YES |
| C | Brand says E.coli <10 CFU/g (within standard); 3 consumer tests show 230-510 CFU/g (2.3-5.1x over 100 CFU/g standard). | YES |
| D | 周芳's promoted batch (BN-20260201) falls within the recall range (BN-20260115~BN-20260228). | YES |
| E | Regulator notice carries enforcement authority (停产整改), making "systemic" a legally binding characterization, not opinion. | YES |
| F | The brand's proactive recall demonstrates the issue is already resolved. | NO |
| G | Consumer tests from 3 accredited labs provide independent corroboration contradicting brand's self-testing results. | YES |
| H | 周芳 bear legal responsibility for promoting a product that later had safety issues. | NO |

**answer:** `["A", "B", "C", "D", "E", "G"]`
