# Layer 3 -- Eval Questions Spec

> Format: all `multi_choice`, 8-10 options per round, n-of-many. ~30 rounds.

---

## 1. Round Inventory

| Round | Question Type | Tags | Main Skill Tested | Depends on Update? | Cross-round Reversal? |
|---|---|---|---|---|---|
| r1 | multi_choice | MS-R, exec_check | Payment + fee breakdown cross-source (C3 non-conflict) + tool use | No | No |
| r2 | multi_choice | MS-I | Posting 10% vs contract 20% discrepancy identification (C2 partial) | No | Yes (R2->R6 seed) |
| r3 | multi_choice | MS-R | Three-party payment flow: parent -> platform -> tutor (C1+C4 partial) | No | Yes (R3->R7 seed) |
| r4 | multi_choice | P-R | User preference identification (casual, conclusion-first, examples) | No | No |
| r5 | multi_choice | DU-R | Reassess fee legitimacy after platform confirms contract rate (C2 via Update 1) | Yes (Update 1) | Yes (R2->R6 partial) |
| r6 | multi_choice | DU-I, exec_check | Fee rate discrepancy analysis -- posting 10% vs contract 20% + footnote | Yes (Update 1) | Yes (R2->R6 definitive) |
| r7 | multi_choice | DU-R | Integrate parent confirmation -- three-party payment reconciliation (C4 via Update 2) | Yes (Update 2) | Yes (R3->R7 via C4) |
| r8 | multi_choice | MD-R | Source reliability ranking | No | No |
| r9 | multi_choice | DU-I, exec_check | Systemic pattern -- 周姐姐's testimony + other tutors (C2 pattern via Update 3) | Yes (Update 3) | Yes (R2->R9 pattern) |
| r10 | multi_choice | DU-R, exec_check | Posting modification discovered -- platform concealment evidence (C2 definitive via Update 4) | Yes (Update 4) | Yes (R2->R10 definitive) |
| r11 | multi_choice | MD-I | Platform's defense analysis -- "contract governs" vs misleading advertising | Yes (Update 4) | No |
| r12 | multi_choice | DP-I | Identify B1 and B2 biases and correction triggers | Yes (Update 1+3+4) | No |
| r13 | multi_choice | MS-I | Contract law vs consumer protection law analysis | Yes (Update 4) | No |
| r14 | multi_choice | P-I, exec_check | Generate financial reconciliation in 王明's preferred format | No | No |
| r15 | multi_choice | MS-R | C3 non-conflict synthesis -- all schedule and payment dates consistent | No | No |
| r16 | multi_choice | P-I | Format complaint letter in casual but evidence-based style | Yes (Update 4) | No |
| r17 | multi_choice | DU-I | Integrate all evidence for platform complaint | Yes (all updates) | No |
| r18 | multi_choice | MP-I, exec_check | Complete evidence chain for each claim | Yes (all updates) | No |
| r19 | multi_choice | MS-R | Fee calculation verification -- all amounts | No | No |
| r20 | multi_choice | P-R | Preference compliance check | No | No |
| r21 | multi_choice | MDP-I, exec_check | Comprehensive assessment -- all contradictions, legal options, recommendations | Yes (all updates) | Comprehensive |
| r22 | multi_choice | MS-R | Contract footnote analysis -- "优惠费率已调整" | No | No |
| r23 | multi_choice | DU-R | B1 bias identification and correction | Yes (Update 3+4) | No |
| r24 | multi_choice | MD-R, exec_check | Platform behavior pattern -- bait-and-switch analysis | Yes (all updates) | No |
| r25 | multi_choice | MP-I | Recommended actions with priorities | Yes (all updates) | No |
| r26 | multi_choice | MS-I | Three-party liability assessment | Yes (all updates) | No |
| r27 | multi_choice | DP-I, exec_check | Posting screenshot vs current posting -- evidence of modification | Yes (Update 4) | No |
| r28 | multi_choice | MD-I | Platform business model ethics analysis | Yes (all updates) | No |
| r29 | multi_choice | MS-I | Legal remedies and practical options for a student | Yes (all updates) | No |
| r30 | multi_choice | MDP-I | Final comprehensive resolution plan | Yes (all updates) | Comprehensive |

**exec_check rounds:** R1, R6, R9, R10, R14, R18, R21, R24, R27 = 9 out of 30 = 30%

---

## 2. Sample Round Spec

### R1: Payment and Fee Cross-Source (MS-R, exec_check)

**exec_check requirement:** Agent must `exec ls` and `read wechat-payment-history.md` and `read platform-fee-breakdown.md`.

**Question:**
> "Based on workspace documents, which statements about Wang Ming's tutoring payment are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Wang Ming received ¥2,400 via WeChat transfer from "学霸家教平台" on 2026-03-31, with the note "家教报酬-王明-3月". | YES | wechat-payment-history.md | Direct fact, C1 |
| B | The platform fee breakdown shows: parent paid ¥3,000, platform fee (20%) = ¥600, tutor payment = ¥2,400. | YES | platform-fee-breakdown.md | Direct fact, C1 |
| C | The job posting screenshot (saved 2026-02-28) shows the platform service fee as "10%". | YES | job-posting-screenshot.md | Direct fact, C2 |
| D | The service contract (tutoring-platform-rules.md section 2.3) states the platform service fee is "20%". | YES | tutoring-platform-rules.md | Direct fact, C2 |
| E | The contract footnote states: "优惠费率已于2026年1月1日调整为标准费率20%。此前签约用户不受影响。" | YES | tutoring-platform-rules.md | Direct fact, C2 detail |
| F | Wang Ming completed 16 hours of tutoring (8 sessions x 2 hours) during March 2026. | YES | platform-fee-breakdown.md + chat-with-parent.md | C3 non-conflict |
| G | The parent (张女士) paid ¥2,400 directly to Wang Ming via WeChat, bypassing the platform. | NO | Payment came from platform, not parent; parent paid ¥3,000 to platform | Wrong payment flow |
| H | The platform service fee was negotiable and Wang Ming opted for the 20% tier. | NO | No evidence of negotiation or tiers; 20% is the standard rate applied to all | Fabricated detail |
