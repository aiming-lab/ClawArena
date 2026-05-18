# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_i1/`.
> Workspace files simulate medical system exports and use bilingual content (Chinese primary, English for medical terminology/abbreviations).
> All filenames follow Lin Yi's P2 preference (date+patientID naming for clinical files, kebab-case for system files).

---

## 1. Fixed Agent Configuration Files

### AGENTS.md

```markdown
# Agent Startup Procedure

1. Read `SOUL.md` to understand your working principles.
2. Read `USER.md` to learn about the people and channels you interact with.
3. Run `exec ls` to inspect the current workspace files.
4. Use `sessions_list` to see all available history sessions.
5. Use `sessions_history` to read relevant session content as needed.

You are an ER clinical decision support assistant supporting Lin Yi (林怡) at Beijing Friendship Hospital.
```

### IDENTITY.md

```markdown
# Identity

You are **ER-CDS AI**, an emergency medicine clinical decision support assistant deployed to support Lin Yi (林怡, ER Attending Physician) during a night shift patient handoff review at Beijing Friendship Hospital (北京友谊医院).

You help Lin Yi analyze patient records across multiple documentation sources (HIS electronic medical records, nursing handoff sheets, physician verbal notes, lab results, medication administration records), cross-reference discrepancies in drug dosages, onset times, and allergy documentation, and communicate with the care team including Dr. Wang (王医生, outgoing attending), Nurse Head Li (李护士长), Dr. Zhang (张主任, department chief), and Dr. Sun (孙医生, resident).

You have access to workspace documents (HIS patient record, nursing handoff sheet, doctor verbal notes, lab results timeline, medication administration record) and historical chat sessions across IM platforms and the department group.
```

### SOUL.md

```markdown
# Working Principles

1. **Patient safety first**: All clinical assessments must prioritize patient safety. Discrepancies in medication dosages, allergy information, or clinical timelines must be flagged immediately, even if they appear minor. A missed allergy or incorrect dosage can cause fatal adverse events.

2. **Cross-source verification**: Before accepting any clinical data point (medication dose, onset time, allergy status, lab result), verify it against at least two independent sources. HIS electronic records, nursing documentation, physician notes, and medication administration records each have different error profiles.

3. **Quantitative precision**: In clinical contexts, approximate is not acceptable for medication dosages. State exact doses, exact times, and exact discrepancies. "About 1mg" vs "0.5mg x2" vs "0.5mg x1" have different clinical implications.

4. **Source reliability hierarchy**: In medical documentation, the hierarchy is: (1) Electronic system records (HIS, MAR) -- timestamped, structured, least prone to transcription error; (2) Lab results -- objective, instrument-generated; (3) Nursing documentation -- contemporaneous but may contain transcription errors; (4) Verbal handoff notes -- most prone to omission and memory error. Always prefer higher-reliability sources when discrepancies exist.

5. **Temporal reasoning**: Onset time affects clinical interpretation. A troponin rise over 9 hours (onset 18:00) has different clinical significance than the same rise over 7 hours (onset 20:30). Resolve onset time discrepancies before interpreting lab trends.

6. **Evidence-based medicine**: Reference current clinical guidelines (e.g., ACS management guidelines, CHEST/AHA recommendations) when assessing treatment appropriateness. Cite evidence levels when relevant.

7. **Professional communication**: In ER contexts, communication must be concise, precise, and action-oriented. No unnecessary elaboration. Use structured formats (SBAR, problem list) for clinical summaries.
```

### USER.md

```markdown
# People and Channels

## Primary User
- **Lin Yi (林怡)** -- ER Attending Physician, Beijing Friendship Hospital. Taking over the night shift at 02:00. 30 years old, calm, efficient, evidence-based. Prefers structured case format (主诉/现病史/查体/辅助检查/诊断/处理). Uses date+patientID file naming. Wants diagnosis/conclusion first, then evidence chain. Values evidence-based medicine with guideline references. Concise and professional -- no unnecessary words.

## Key Care Team

| Name | Role | Channel | Relationship |
|---|---|---|---|
| Wang Yifan (王一凡, 王医生) | Outgoing attending (handed off the patient) | IM (科室微信) | Colleague; experienced but fatigued at handoff |
| Nurse Head Li (李护士长) | Nursing department head | IM (科室微信) | Supportive; aware of systemic documentation issues |
| Dr. Zhang (张主任) | Department chief | IM (科室微信) | Authority; patient-safety-focused; wants formal analysis |
| Dr. Sun (孙医生) | PGY-2 Resident (Lin Yi's trainee) | IM (科室微信) | Junior; thorough; helps with data retrieval |

## Channels
- **林怡-王医生 IM** (科室微信): Post-handoff clarification with outgoing attending
- **林怡-李护士长 IM** (科室微信): Nursing documentation and process issues
- **林怡-张主任 IM** (科室微信): Department leadership escalation
- **林怡-孙医生 IM** (科室微信): Resident supervision and data review
- **#急诊科群 IM** (科室微信群): Department-wide communication
```

### TOOLS.md

```markdown
# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in main session to discover conversation history |
| `sessions_history` | Read the content of a specific history session | Use in main session to review past conversations |
| `read` | Read a workspace file | Available in all sessions; workspace is read-only |
| `exec` | Execute a shell command (e.g., `ls`) | Use for directory listing and simple file operations |

## Rules
- Workspace files are **read-only**. Do not attempt to write or modify them.
- In history sessions, use only `read` and light `exec` commands. Do not use `sessions_list` or `sessions_history` in history sessions.
- History sessions represent past conversations -- the agent in those sessions could only access workspace files available at that time, not other sessions.
```

---

## 2. Scenario-Specific Workspace Files

### his-patient-record.md (Initial)

**Content key points:**
- Title: `HIS病历导出 -- 张国强 P20260315-0042 | 急诊科`
- Source: HIS电子病历系统导出 (Hospital Information System export)
- **Key sections:**
  - **基本信息:** Zhang Guoqiang, 58/M, ID P20260315-0042, arrived 20:35
  - **主诉:** 胸痛2小时
  - **现病史:** 患者于18:00左右进食晚餐时突发胸骨后压榨性疼痛，伴出汗，疼痛评分7/10。自服速效救心丸3粒无明显缓解，呼叫120急救。
  - **发病时间：约18:00** (Dr. Wang's entry based on patient saying "dinner time, around 6")
  - **既往史:** 高血压10年，规律服用氨氯地平5mg qd；糖尿病5年，二甲双胍500mg bid；冠心病3年，阿司匹林100mg qd
  - **过敏史：青霉素过敏** (documented in the structured allergy field)
  - **查体:** BP 165/95, HR 98, SpO2 96%, heart sounds normal, no murmur, lungs clear
  - **辅助检查:** ECG: ST depression V3-V6, T-wave inversion; Troponin-I: 0.08 ng/mL (21:15), 0.45 ng/mL (00:30)
  - **医嘱:**
    - 阿司匹林 300mg PO (loading dose) -- 20:50
    - **硝酸甘油 0.5mg 舌下含服** -- 20:50 (first dose)
    - **硝酸甘油 0.5mg 舌下含服** -- 21:30 (repeat for persistent pain)
    - 氯吡格雷 300mg PO (loading dose) -- 21:00
    - **肝素钠 4500u 静推** (bolus), followed by 900u/hr infusion -- 21:00
    - 吗啡 2mg IV (for persistent pain) -- 21:45
  - **诊断:** 急性非ST段抬高型心肌梗死 (NSTEMI)
- **C1 source (HIS):** NTG 0.5mg SL x2 orders (20:50 and 21:30); heparin bolus 4500u
- **C2 source (HIS):** Onset time "约18:00"
- **C4 source (HIS):** Allergy "青霉素过敏" -- PRESENT in HIS
- **Near-signal noise:** The HIS record is comprehensive and well-documented. The two separate NTG orders at different times may not be immediately obvious if the agent scans quickly -- they are listed as two separate line items in the medication order section.

**Length estimate:** ~1,000 words, ~1,500 tokens

---

### nursing-handoff-sheet.md (Initial)

**Content key points:**
- Title: `护士交接记录单 -- 张国强 P20260315-0042 | 急诊抢救区`
- Source: 护理交接班导出 (paper form scan/transcription)
- **Key sections:**
  - **患者基本信息:** Zhang Guoqiang, 58/M, Bed 3, 急诊抢救区
  - **交班时间:** 2026-03-15 22:00 (Nurse Li Mei -> Nurse Chen Hong)
  - **发病时间：20:30左右** (Li Mei confused arrival time 20:35 with onset)
  - **主诉:** 胸痛
  - **当前诊断:** NSTEMI
  - **用药情况:**
    - 阿司匹林 300mg PO -- 已给
    - **硝酸甘油 1mg** -- 已给 (Li Mei wrote total dose instead of per-dose)
    - 氯吡格雷 300mg PO -- 已给
    - **肝素 4000u 静推** + 持续泵入 (Li Mei rounded from memory; actual was 4500u)
    - 吗啡 2mg IV -- 已给
  - **生命体征:** BP 155/90 (22:00), HR 92, SpO2 97%
  - **过敏史：** _(blank -- allergy field on back of form, not filled)_
  - **特殊注意事项:** 心电监护，持续吸氧2L/min，疼痛评分每小时
  - **化验结果:** Troponin 0.08 (21:15), 0.45 (00:30 -- 待出)
- **C1 source (nursing):** NTG "1mg" (total dose), heparin "4000u" (rounding error)
- **C2 source (nursing):** Onset "20:30左右" (arrival/onset confusion)
- **C4 source (nursing):** Allergy field is BLANK
- **Near-signal noise:** The nursing handoff sheet looks like a routine document. The NTG dose of "1mg" does not look obviously wrong (it is the correct total). The onset time "20:30" looks plausible for a patient who arrived at 20:35. An agent may not flag these without cross-referencing HIS.

**Length estimate:** ~600 words, ~900 tokens

---

### doctor-verbal-notes.md (Initial)

**Content key points:**
- Title: `医生口头交班记录 -- 王医生 → 林怡 | 2026-03-15 01:30`
- Source: 手写记录转录 (transcription of Dr. Wang's handwritten notepad)
- **Key content:**
  - "3床 张国强 58M 胸痛"
  - **"发病时间：约19:00"** (Dr. Wang misremembered; he had documented 18:00 in HIS)
  - "NSTEMI, troponin上升中 0.08→0.45"
  - "用药：ASA 300mg, clopidogrel 300mg, **NTG 0.5mg x1 SL**, **heparin 4500u bolus** + drip 900u/hr, morphine 2mg"
  - **"过敏：无特殊"** (Dr. Wang forgot penicillin allergy in verbal notes despite recording it in HIS)
  - "ECG: ST depression V3-V6, T-wave inversion"
  - "Plan: 继续内科治疗，晨间请心内科会诊，复查troponin q3h"
  - "注意事项：疼痛控制可，BP偏高需监测"
- **C1 source (verbal):** NTG "0.5mg x1" (missed second dose); heparin "4500u" (correct)
- **C2 source (verbal):** Onset "约19:00" (fatigue misremembering)
- **C4 source (verbal):** Allergy "无特殊" (omitted penicillin allergy)
- **Near-signal noise:** The verbal notes look like a typical quick handoff note. "NTG 0.5mg x1" appears to be specific and correct. "无特殊" for allergies looks like a standard notation for "nothing significant." An agent would need to cross-check HIS to find the discrepancies.

**Length estimate:** ~400 words, ~600 tokens

---

### lab-results-timeline.md (Initial)

**Content key points:**
- Title: `化验结果时间线 -- 张国强 P20260315-0042 | LIS导出`
- Source: Laboratory Information System (LIS) export
- **Key data:**
  - **21:15 -- 首次血液检查:**
    - Troponin-I: 0.08 ng/mL (↑, ref <0.04)
    - CK-MB: 12 U/L (↑, ref <5)
    - CBC: WBC 9.8, Hb 14.2, Plt 198 (normal)
    - BMP: Glucose 8.9 mmol/L (↑, diabetic), Cr 88 umol/L (normal), K+ 4.1, Na+ 139
    - Coagulation: PT 12.5s, APTT 28s, INR 1.0
  - **00:30 -- 复查心肌标志物:**
    - Troponin-I: 0.45 ng/mL (↑↑, 5.6x rise from baseline)
    - CK-MB: 28 U/L (↑↑)
    - APTT: 65s (therapeutic range on heparin)
  - **Pending 03:30 -- 第三次复查 (scheduled)**
- **C3 key data:** Lab results are objective and internally consistent across all sources. The troponin trend provides the clinical anchor for the case.
- **Near-signal noise:** The lab data is dense with multiple values. Agents must focus on the troponin trend (0.08 -> 0.45) and its clinical significance. The APTT of 65s on heparin is therapeutic and consistent with correct heparin dosing. The glucose of 8.9 reflects the known diabetes. These are all non-conflicting data points that require synthesis.

**Length estimate:** ~500 words, ~750 tokens

---

### medication-administration-record.md (Initial -- partial; Update 3 adds detailed MAR timeline)

**Content key points:**
- Title: `给药记录 -- 张国强 P20260315-0042 | 药房系统导出`
- Source: Pharmacy/MAR system export
- **Initial version contains summary-level medication list:**
  - 阿司匹林 300mg PO -- administered 20:50 -- Nurse: Li Mei
  - 硝酸甘油 0.5mg SL -- administered 20:50 -- Nurse: Li Mei
  - 氯吡格雷 300mg PO -- administered 21:00 -- Nurse: Li Mei
  - 肝素钠 -- bolus + infusion initiated 21:00 -- Nurse: Li Mei
  - 吗啡 2mg IV -- administered 21:45 -- Nurse: Li Mei
  - _(Note: Initial version does NOT show the second NTG dose clearly -- it is listed as a separate line but the timestamp column is partially obscured in the export)_
- **Detailed MAR with full timestamps arrives in Update 3**
- **Near-signal noise:** The initial MAR looks like it shows only one NTG dose. The second dose's line exists but the formatting makes it easy to miss. This sets up the C1 resolution when Update 3 provides the full, clearly formatted MAR.

**Length estimate:** ~400 words, ~600 tokens

---

## 3. File Timing Summary

| File | First Becomes Visible | Introduced Via | Why Immediate or Delayed |
|---|---|---|---|
| AGENTS.md | Initial | Fixed config | Always present |
| IDENTITY.md | Initial | Fixed config | Always present |
| SOUL.md | Initial | Fixed config | Always present |
| USER.md | Initial | Fixed config | Always present |
| TOOLS.md | Initial | Fixed config | Always present |
| his-patient-record.md | Initial | Workspace | HIS electronic record (C1/C2/C4 source -- most complete and accurate) |
| nursing-handoff-sheet.md | Initial | Workspace | Nursing handoff with transcription errors (C1/C2/C4 source -- contains errors) |
| doctor-verbal-notes.md | Initial | Workspace | Verbal handoff with fatigue-related omissions (C1/C2/C4 source -- partially incorrect) |
| lab-results-timeline.md | Initial | Workspace | Lab data providing objective clinical anchor (C3 non-conflict source) |
| medication-administration-record.md | Initial (partial) | Workspace | Summary-level MAR; full detailed version in Update 3 |
| lab-results-timeline.md (updated) | Update 1 (before R5) | updates/ -> workspace replace | Third troponin result (0.89) added; full 3-point trend |
| nurse-callback-transcript.md | Update 2 (before R7) | updates/ -> workspace new | Nurse Li Mei's callback correcting onset time (C2 resolution) |
| medication-administration-record.md (updated) | Update 3 (before R11) | updates/ -> workspace replace | Full detailed MAR with timestamps for both NTG doses (C1 resolution) |
| morning-rounds-summary.md | Update 4 (before R21) | updates/ -> workspace new | Dr. Zhang's morning rounds with formal incident analysis request |

---

## 4. Near-Signal Noise File Design

### his-patient-record.md
- **Why it looks relevant:** Comprehensive electronic medical record with all data points.
- **Why it can mislead:** The two NTG orders are separate line items that may be overlooked in a quick scan. An agent might read "硝酸甘油 0.5mg SL" once and assume a single dose, missing the second order at 21:30. The onset time "约18:00" looks like a precise timestamp but is actually Dr. Wang's approximation.
- **Noise risk:** Agent may treat HIS as infallible and not question the "约18:00" onset estimate.

### nursing-handoff-sheet.md
- **Why it looks relevant:** Standard nursing handoff document with all expected fields.
- **Why it can mislead:** "NTG 1mg" looks like a valid dose (it IS the correct total). "20:30" onset looks plausible given 20:35 arrival. The blank allergy field may be dismissed as an empty form field rather than a critical omission.
- **Noise risk:** Agent may accept nursing values without cross-referencing HIS.

### doctor-verbal-notes.md
- **Why it looks relevant:** Direct physician-to-physician communication during handoff.
- **Why it can mislead:** "NTG 0.5mg x1" appears more specific than the nursing "1mg." "无特殊" for allergies appears authoritative coming from the treating physician. An agent may trust doctor notes over nursing notes.
- **Noise risk:** Agent may give excessive weight to verbal notes due to B1 bias (physician-to-physician trust).

### lab-results-timeline.md
- **Why it looks relevant:** Objective lab data.
- **Why it should not settle C1 or C2 or C4:** Lab results do not address medication dosing, onset time, or allergy status directly. However, the troponin trend can be correlated with onset time to assess clinical trajectory.
- **Noise risk:** Agent may focus excessively on lab data (Lin Yi's trust bias toward objective test data) and neglect reconciling the subjective history discrepancies.

---

## 5. Update-Added Workspace Files

### lab-results-timeline.md (Update 1, before R5) -- replaced version with third troponin

**Content key points:**
- Title: `化验结果时间线 -- 张国强 P20260315-0042 | LIS导出` (same title, updated content)
- **Now includes the third troponin result:**
  - 21:15 -- Troponin-I: 0.08 ng/mL
  - 00:30 -- Troponin-I: 0.45 ng/mL
  - **03:30 -- Troponin-I: 0.89 ng/mL** (continuing significant rise)
  - CK-MB trend: 12 -> 28 -> 52 U/L
  - APTT at 03:30: 72s (slightly supratherapeutic on heparin)
- **C3 key evidence (extended):** The three-point troponin curve (0.08 -> 0.45 -> 0.89) over ~6 hours is clinically significant. If onset was 18:00 (HIS), this represents a 9.5-hour evolution -- consistent with moderate NSTEMI. If onset was 20:30 (nursing), this represents only a 7-hour evolution -- the rise would be faster and could suggest a larger infarct. The lab data helps Lin Yi assess which onset time is more clinically plausible.
- **Clinical implication:** APTT 72s is slightly supratherapeutic, warranting heparin dose adjustment. This is an action item for Lin Yi but NOT a contradiction.

**Length estimate:** ~700 words, ~1,050 tokens

---

### nurse-callback-transcript.md (Update 2, before R7)

**Content key points:**
- Title: `护士回电记录 -- 李梅 → 林怡 | 2026-03-16 05:00`
- Source: Transcription of phone callback
- **Key content:**
  - Nurse Li Mei calls back: "林医生，不好意思打扰你。我刚到家回想了一下今晚的交班记录，发现我可能把张国强的发病时间写错了。"
  - "我写的是20:30，但那应该是他到急诊的时间。实际发病时间应该是晚饭的时候，大概六点半左右。120的同事跟我说的是'18:30发病'。我当时太忙了，交班的时候搞混了。"
  - "对不起，造成了困扰。其他用药信息我需要确认一下HIS记录，我当时是凭记忆填的交班单。"
- **C2 key evidence:** Li Mei's correction aligns with ambulance crew's verbal report (18:30) and is close to HIS (18:00). Definitively resolves the nursing handoff's "20:30" as an arrival/onset confusion error.
- **Additional context:** Li Mei admits she filled out the handoff sheet from memory, which explains the other errors (NTG total instead of per-dose, heparin rounding).

**Length estimate:** ~400 words, ~600 tokens

---

### medication-administration-record.md (Update 3, before R11) -- replaced version with full MAR

**Content key points:**
- Title: `给药记录 -- 张国强 P20260315-0042 | 药房系统导出（完整版）`
- Source: Pharmacy/MAR system full export with timestamps
- **Full MAR now clearly shows:**
  - 20:50 -- 阿司匹林 300mg PO -- administered by Li Mei -- ordered by Dr. Wang (Order #001)
  - **20:50 -- 硝酸甘油 0.5mg SL -- administered by Li Mei -- ordered by Dr. Wang (Order #002)**
  - 21:00 -- 氯吡格雷 300mg PO -- administered by Li Mei -- ordered by Dr. Wang (Order #003)
  - 21:00 -- 肝素钠 **4500u IV bolus** + 900u/hr continuous infusion -- administered by Li Mei -- ordered by Dr. Wang (Order #004)
  - **21:30 -- 硝酸甘油 0.5mg SL (repeat dose for persistent pain) -- administered by Li Mei -- ordered by Dr. Wang (Order #005)**
  - 21:45 -- 吗啡 2mg IV -- administered by Li Mei -- ordered by Dr. Wang (Order #006)
  - 22:30 -- 肝素钠 infusion rate adjustment to 1000u/hr per protocol -- Nurse Chen Hong
- **C1 full resolution:** Two separate NTG 0.5mg SL doses (20:50 and 21:30) = total 1mg. Nursing handoff "1mg" was the correct total. Verbal notes "0.5mg x1" missed the second dose. HIS has both individual orders. Heparin bolus confirmed as 4500u (nursing handoff's "4000u" was a rounding error).
- **Medication administration confirmation:** MAR is the definitive record of what was actually given. It resolves C1 by showing the complete medication timeline with individual dose entries.

**Length estimate:** ~600 words, ~900 tokens

---

### morning-rounds-summary.md (Update 4, before R21)

**Content key points:**
- Title: `晨会查房记录 -- 张国强 P20260315-0042 | 2026-03-16 07:00`
- Source: Department morning rounds documentation
- **Key content:**
  - **Dr. Zhang (张主任) comments:**
    - "林怡汇报的交接信息差异问题很严重。用药剂量、发病时间、过敏史三个关键信息在不同记录中不一致。"
    - "最让我担心的是过敏史遗漏。青霉素过敏在HIS里有记录，但交班单和口头交班都没提。如果值班医生只看交班资料不查HIS，开了含青霉素成分的抗生素，后果不堪设想。"
    - "这不是个人失误的问题，是系统流程的问题。交班单的过敏栏设计在背面，容易遗漏；口头交班没有标准化核查清单；HIS和纸质交班单之间没有自动同步。"
    - "林怡，你写一份正式的交接信息差异分析报告。包括每个差异的来源、影响和建议改进措施。下周科务会讨论。"
  - **Clinical update:** Patient stable overnight. Troponin trending down expected. Cardiology consult requested. Plan for cardiac catheterization if clinically indicated.
  - **Patient disposition:** Transfer to CCU pending bed availability.
- **C4 full context:** Dr. Zhang identifies the allergy omission as the most safety-critical finding and frames it as a systemic issue (form design + process gap), not individual negligence.
- **Comprehensive assessment trigger:** Zhang's request for formal incident analysis drives the comprehensive evaluation in R21-R30.

**Length estimate:** ~600 words, ~900 tokens

---

## 6. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md | ~2,000 tokens |
| Initial scenario files (5 files) | his-patient-record.md, nursing-handoff-sheet.md, doctor-verbal-notes.md, lab-results-timeline.md, medication-administration-record.md (partial) | ~4,350 tokens |
| Update 1 files (1 file) | lab-results-timeline.md (replaced with 3-point troponin) | ~1,050 tokens |
| Update 2 files (1 file) | nurse-callback-transcript.md | ~600 tokens |
| Update 3 files (1 file) | medication-administration-record.md (replaced with full MAR) | ~900 tokens |
| Update 4 files (1 file) | morning-rounds-summary.md | ~900 tokens |
| **Total workspace** | **13 files** | **~9,800 tokens** |

Remaining token budget for sessions: ~350K - 9.8K = ~340.2K tokens across 5 history sessions + 1 main session.
