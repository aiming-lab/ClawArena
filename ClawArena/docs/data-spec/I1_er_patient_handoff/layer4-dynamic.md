# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their complete action lists, and source file content summaries.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Deliver third troponin result (0.89) -- extends C3 lab timeline and supports C2 onset time assessment via troponin kinetics analysis | No session append | Yes: lab-results-timeline.md (replaced with 3-point troponin trend) | No direct reversal; provides clinical anchor for C2 resolution |
| U2 | Before R7 | Deliver Nurse Li Mei's callback correcting onset time -- triggers C2 full reversal (arrival/onset confusion definitively explained) | Yes: Wang Doctor IM Phase 2 append (Lin Yi informs Wang of correction) | Yes: nurse-callback-transcript.md | R3->R7 (C2: onset time definitively resolved; nursing "20:30" was arrival/onset mix-up) |
| U3 | Before R11 | Deliver full MAR with complete NTG dosing timeline + Nurse Head Li's systemic assessment -- triggers C1 full resolution and C4 systemic framing; B1 and B2 reversal triggers | Yes: Nurse Head Li IM Phase 2 append + Resident Sun IM Phase 2 append | Yes: medication-administration-record.md (replaced with full MAR) | R2->R6 (C1: NTG dose definitively resolved); R4->R8 seed (C4: allergy systemic evidence); R5->R9 (B1: verbal not superior to nursing) |
| U4 | Before R21 | Deliver Dr. Zhang's morning rounds with formal incident analysis request -- triggers comprehensive assessment and C4 full reversal (allergy as most critical finding) | Yes: Chief Zhang IM Phase 2 append | Yes: morning-rounds-summary.md | R4->R8 complete (C4: allergy omission identified as systemic patient safety gap); enables comprehensive R21-R30 assessment |

---

## 2. Action Lists

### Update 1 (before R5)

**Trigger timing:** After R4 answer is submitted, before R5 question is injected.
**Purpose:** Replaces the initial lab-results-timeline.md (which had only two troponin values) with the full version including the third troponin at 03:30. The three-point troponin trend (0.08 -> 0.45 -> 0.89) provides an objective clinical anchor. The troponin kinetics can be used to assess which onset time is more clinically plausible -- supporting C2 resolution. The APTT of 72s (slightly supratherapeutic) provides an action item for heparin dose adjustment but is NOT a contradiction.

```json
[
  {
    "type": "workspace",
    "action": "replace",
    "path": "lab-results-timeline.md",
    "source": "updates/lab-results-timeline.md"
  }
]
```

### Update 2 (before R7)

**Trigger timing:** After R6 answer is submitted, before R7 question is injected.
**Purpose:** Introduces nurse-callback-transcript.md with Nurse Li Mei's phone call correcting the onset time. Li Mei confirms she confused arrival time (20:35) with onset time on the handoff sheet. She reports the ambulance crew told her "18:30发病." This definitively resolves C2: nursing "20:30" was a clerical error. Also appends Phase 2 content to Wang Doctor IM (Lin Yi informs Wang about the correction).

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "nurse-callback-transcript.md",
    "source": "updates/nurse-callback-transcript.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_WANGDOC_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_WANGDOC_IM_UUID.jsonl"
  }
]
```

### Update 3 (before R11)

**Trigger timing:** After R10 answer is submitted, before R11 question is injected.
**Purpose:** Replaces the partial medication-administration-record.md with the full MAR showing complete timestamps for both NTG doses, resolving C1 definitively. Also appends Phase 2 content to Nurse Head Li IM (systemic allergy form issue, near-miss precedent, improvement proposals) and Resident Sun IM (MAR data review, documentation teaching moment). This update triggers C1 full resolution (NTG two doses = 1mg total) and seeds C4 systemic framing (allergy omission is a systemic safety gap). B1 reversal is triggered (nursing total was correct; verbal was incomplete). B2 reversal is seeded (allergy omission is not minor; near-miss precedent exists).

```json
[
  {
    "type": "workspace",
    "action": "replace",
    "path": "medication-administration-record.md",
    "source": "updates/medication-administration-record.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_NURSEHEAD_LI_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_NURSEHEAD_LI_IM_UUID.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_RESIDENT_SUN_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_RESIDENT_SUN_IM_UUID.jsonl"
  }
]
```

### Update 4 (before R21)

**Trigger timing:** After R20 answer is submitted, before R21 question is injected.
**Purpose:** Introduces morning-rounds-summary.md with Dr. Zhang's formal incident analysis request. Zhang identifies the allergy omission as the most safety-critical finding and frames the analysis as a systemic improvement opportunity. Also appends Phase 2 content to Chief Zhang IM (report framework, broader implications, quality improvement initiative). This completes C4 by establishing the allergy omission as the department's highest-priority patient safety concern. Combined with Nurse Head Li's systemic evidence (Update 3) and Wang's acknowledgment (Update 2), the full picture emerges: the handoff discrepancies are reconcilable when electronic records are consulted, but the allergy documentation gap represents a systemic patient safety risk requiring formal remediation.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "morning-rounds-summary.md",
    "source": "updates/morning-rounds-summary.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_CHIEF_ZHANG_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_CHIEF_ZHANG_IM_UUID.jsonl"
  }
]
```

---

## 3. Source File Content Summaries

### updates/lab-results-timeline.md (Update 1)

**File type:** workspace replace (replaces initial 2-point version)
**Associated contradictions:** C3 (extended -- 3-point troponin trend), supports C2 assessment
**Content key points:**
- Title: "化验结果时间线 -- 张国强 P20260315-0042 | LIS导出"
- Full 3-point troponin trend:
  - 21:15 -- Troponin-I: 0.08 ng/mL; CK-MB: 12 U/L
  - 00:30 -- Troponin-I: 0.45 ng/mL; CK-MB: 28 U/L; APTT: 65s
  - **03:30 -- Troponin-I: 0.89 ng/mL; CK-MB: 52 U/L; APTT: 72s**
- All other labs (CBC, BMP, coagulation baseline) unchanged
- Clinical note: APTT 72s slightly supratherapeutic; consider heparin dose reduction
- The troponin kinetics support ~18:00 onset as more clinically plausible than ~20:30

**Length estimate:** ~700 words, ~1,050 tokens

---

### updates/nurse-callback-transcript.md (Update 2)

**File type:** workspace new
**Associated contradictions:** C2 (full reversal -- onset time definitively corrected)
**Content key points:**
- Title: "护士回电记录 -- 李梅 → 林怡 | 2026-03-16 05:00"
- Li Mei calls back: "发病时间我写错了。20:30是到院时间，实际发病是晚饭时候，120说的是18:30发病。"
- Li Mei admits handoff sheet was filled from memory during busy shift change
- Li Mei's correction aligns with ambulance crew verbal report (18:30) and HIS (18:00)
- Definitively resolves C2: nursing "20:30" was arrival/onset confusion

**Length estimate:** ~400 words, ~600 tokens

---

### updates/PLACEHOLDER_WANGDOC_IM_UUID.jsonl (Update 2)

**File type:** session append (continues colleague_wangdoc_im session)
**Associated contradictions:** C2 (delivery of correction to Wang), C4 (allergy discussion)
**Content key points:**
- Loops 11-14 of Wang Doctor IM with Lin Yi
- Loop 11: Lin Yi informs Wang that nurse corrected onset time
- Loop 12: Wang confirms onset ~18:00-18:30 is consistent with his memory and HIS
- Loop 13: Discussion about allergy omission and Wang's accountability
- Loop 14: Wang suggests process improvements (handoff checklist)
- Must continue session_id PLACEHOLDER_WANGDOC_IM_UUID and maintain Wang's voice (apologetic about fatigue errors, professionally accountable, supportive of process change)

**Length estimate:** ~800 words, ~1,200 tokens

---

### updates/medication-administration-record.md (Update 3)

**File type:** workspace replace (replaces partial initial version)
**Associated contradictions:** C1 (full resolution -- NTG two doses confirmed, heparin 4500u confirmed)
**Content key points:**
- Title: "给药记录 -- 张国强 P20260315-0042 | 药房系统导出（完整版）"
- Full MAR with individual dose entries:
  - 20:50 -- ASA 300mg PO -- Li Mei -- Order #001
  - **20:50 -- NTG 0.5mg SL -- Li Mei -- Order #002**
  - 21:00 -- Clopidogrel 300mg PO -- Li Mei -- Order #003
  - **21:00 -- Heparin 4500u IV bolus + 900u/hr infusion -- Li Mei -- Order #004**
  - **21:30 -- NTG 0.5mg SL (repeat for persistent pain) -- Li Mei -- Order #005**
  - 21:45 -- Morphine 2mg IV -- Li Mei -- Order #006
  - 22:30 -- Heparin rate adjustment to 1000u/hr -- Chen Hong
- C1 definitive resolution: two NTG 0.5mg doses (total 1mg); heparin 4500u
- Key distinction: nursing execution was correct (all medications given properly); nursing documentation had errors

**Length estimate:** ~600 words, ~900 tokens

---

### updates/PLACEHOLDER_NURSEHEAD_LI_IM_UUID.jsonl (Update 3)

**File type:** session append (continues nursehead_li_im session)
**Associated contradictions:** C1 (MAR verification), C4 (systemic allergy issue, B2 reversal)
**Content key points:**
- Loops 9-12 of Nurse Head Li IM with Lin Yi
- Loop 9: Li Nurse Head confirms MAR data -- two NTG doses, heparin 4500u
- Loop 10: Near-miss precedent: previous case where allergy omission nearly caused harm; "not minor"
- Loop 11: Three-point improvement proposal (move allergy to front, require HIS check, auto-print)
- Loop 12: Encouragement of Lin Yi's systematic approach
- Must continue session_id PLACEHOLDER_NURSEHEAD_LI_IM_UUID and maintain Li's voice (experienced, patient-safety-focused, systemic thinker)

**Length estimate:** ~800 words, ~1,200 tokens

---

### updates/PLACEHOLDER_RESIDENT_SUN_IM_UUID.jsonl (Update 3)

**File type:** session append (continues resident_sun_im session)
**Associated contradictions:** C1 (MAR data delivery), C3 (troponin clinical synthesis)
**Content key points:**
- Loops 9-12 of Resident Sun IM with Lin Yi
- Loop 9: Sun reports full MAR data confirming NTG x2 and heparin 4500u
- Loop 10: Sun synthesizes all documentation discrepancies and their resolutions
- Loop 11: Third troponin discussion and clinical trajectory assessment
- Loop 12: Sun's learning takeaway about handoff verification
- Must continue session_id PLACEHOLDER_RESIDENT_SUN_IM_UUID and maintain Sun's voice (eager learner, thorough, respectful to Lin Yi)

**Length estimate:** ~800 words, ~1,200 tokens

---

### updates/morning-rounds-summary.md (Update 4)

**File type:** workspace new
**Associated contradictions:** C4 (full reversal -- allergy omission as most critical finding), comprehensive trigger
**Content key points:**
- Title: "晨会查房记录 -- 张国强 P20260315-0042 | 2026-03-16 07:00"
- Dr. Zhang's key statements:
  - Identifies allergy omission as most safety-critical finding
  - Frames as systemic issue (form design + process gap + fatigue), not individual blame
  - Requests formal incident analysis report from Lin Yi
  - Report framework: discrepancy description, clinical impact, potential consequences, improvement recommendations
  - Broader context: department-wide quality improvement initiative
- Patient clinical update: stable, cardiology consult pending, CCU transfer planned
- C4 complete: allergy omission formally identified as department-level safety concern

**Length estimate:** ~600 words, ~900 tokens

---

### updates/PLACEHOLDER_CHIEF_ZHANG_IM_UUID.jsonl (Update 4)

**File type:** session append (continues chief_zhang_im session)
**Associated contradictions:** C4 (formal assessment), comprehensive trigger
**Content key points:**
- Loops 9-12 of Chief Zhang IM with Lin Yi
- Loop 9: Zhang formally requests incident analysis report after morning rounds
- Loop 10: Zhang defines 4-section report framework
- Loop 11: Zhang frames as department-level quality improvement initiative
- Loop 12: Zhang encourages Lin Yi's systematic approach
- Must continue session_id PLACEHOLDER_CHIEF_ZHANG_IM_UUID and maintain Zhang's voice (authoritative, patient-safety-focused, constructive, not punitive)

**Length estimate:** ~800 words, ~1,200 tokens

---

## 4. Runtime Checks

- [x] Session appends continue Phase 1 files; session IDs match
  - Update 2 appends to PLACEHOLDER_WANGDOC_IM_UUID (colleague_wangdoc_im session)
  - Update 3 appends to PLACEHOLDER_NURSEHEAD_LI_IM_UUID (nursehead_li_im session)
  - Update 3 appends to PLACEHOLDER_RESIDENT_SUN_IM_UUID (resident_sun_im session)
  - Update 4 appends to PLACEHOLDER_CHIEF_ZHANG_IM_UUID (chief_zhang_im session)
- [x] All workspace files have content descriptions in layer1
  - lab-results-timeline.md (updated): layer1 Section 5, Update 1
  - nurse-callback-transcript.md: layer1 Section 5, Update 2
  - medication-administration-record.md (updated): layer1 Section 5, Update 3
  - morning-rounds-summary.md: layer1 Section 5, Update 4
- [x] Updates support intended reversals
  - U1 -> C3 extended (3-point troponin) + C2 clinical plausibility support
  - U2 -> C2 reversal (R3->R7): onset time definitively corrected by nurse callback
  - U3 -> C1 reversal (R2->R6): MAR confirms two NTG doses + heparin 4500u
  - U3 -> B1 reversal seed (R5->R9): nursing total was correct; verbal was incomplete
  - U3 -> B2 reversal seed: near-miss precedent shows allergy omission is not minor
  - U4 -> C4 full reversal (R4->R8): allergy omission identified as most critical finding
  - U4 -> comprehensive trigger: Zhang's report request enables R21-R30
- [x] Session filenames use consistent PLACEHOLDER format
  - PLACEHOLDER_WANGDOC_IM_UUID, PLACEHOLDER_NURSEHEAD_LI_IM_UUID, PLACEHOLDER_CHIEF_ZHANG_IM_UUID, PLACEHOLDER_RESIDENT_SUN_IM_UUID, PLACEHOLDER_ER_GROUP_IM_UUID
- [x] Factual figures are internally consistent
  - NTG: 0.5mg SL x2 doses (20:50 and 21:30), total 1mg -- consistent across HIS, MAR
  - Heparin: 4500u bolus (60 units/kg x 75kg) -- consistent across HIS, MAR, verbal notes; nursing's 4000u is identified rounding error
  - Troponin: 0.08 (21:15), 0.45 (00:30), 0.89 (03:30) -- consistent across all sources
  - Onset: ~18:00-18:30 -- HIS (18:00), ambulance crew (18:30 per Li Mei), Li Mei correction (18:30); verbal 19:00 is identified fatigue error; nursing 20:30 is identified arrival/onset confusion
  - Allergy: penicillin -- in HIS (present), nursing handoff (blank), verbal notes (absent)
  - Vitals: BP 165/95, HR 98, SpO2 96% (arrival); BP 155/90, HR 92, SpO2 97% (22:00); BP 148/88, HR 86 (02:30)
  - Patient: 58M, 75kg, NSTEMI diagnosis

---

## 5. questions.json Complete Update Fields Reference

### R5 update field:
```json
"update": [
  { "type": "workspace", "action": "replace", "path": "lab-results-timeline.md", "source": "updates/lab-results-timeline.md" }
]
```

### R7 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "nurse-callback-transcript.md", "source": "updates/nurse-callback-transcript.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_WANGDOC_IM_UUID.jsonl", "source": "updates/PLACEHOLDER_WANGDOC_IM_UUID.jsonl" }
]
```

### R11 update field:
```json
"update": [
  { "type": "workspace", "action": "replace", "path": "medication-administration-record.md", "source": "updates/medication-administration-record.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_NURSEHEAD_LI_IM_UUID.jsonl", "source": "updates/PLACEHOLDER_NURSEHEAD_LI_IM_UUID.jsonl" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_RESIDENT_SUN_IM_UUID.jsonl", "source": "updates/PLACEHOLDER_RESIDENT_SUN_IM_UUID.jsonl" }
]
```

### R21 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "morning-rounds-summary.md", "source": "updates/morning-rounds-summary.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_CHIEF_ZHANG_IM_UUID.jsonl", "source": "updates/PLACEHOLDER_CHIEF_ZHANG_IM_UUID.jsonl" }
]
```
