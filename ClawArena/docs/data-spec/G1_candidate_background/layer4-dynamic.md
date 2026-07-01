# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their complete action lists, and source file content summaries.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Deliver Huang Lei's detailed interview feedback -- triggers C1 full reversal (triple-source team-size confirmation: resume 12, reference 4, interview hesitation "about 4-5") | No session append | Yes: interview-feedback-forms.md (replaced with full version including Huang Lei's notes) | R2->R5 (C1: team-size inflation definitively established by triple-source evidence) |
| U2 | Before R7 | Deliver Liu Yang's LinkedIn finding + Zhang Wei's explicit process support -- triggers C4 full reversal (dual-source employment gap) and C2 partial reversal (HR VP backing) | Yes: Liu Yang IM Phase 2 append + Zhang Wei Feishu Phase 2 append | Yes: linkedin-profile-export.md | R4->R7 (C4: employment gap definitively confirmed); R3->R8 seed (C2: HR VP vs CTO) |
| U3 | Before R11 | Deliver Huang Lei's detailed P6-vs-P7 assessment + workload reality -- provides nuanced resolution path | Yes: Huang Lei Email Phase 2 append | Yes: huang-lei-assessment-email.md | No new cross-round reversal; extends C1 evidence and provides resolution framework |
| U4 | Before R21 | Deliver CTO's "everyone embellishes" response -- triggers C2 full reversal (CTO minimizing material findings) | Yes: Li Qiang Feishu Phase 2 append | Yes: cto-followup-message.md | R3->R8 complete (C2: CTO urgency definitively shown as conflicting with proper process); enables comprehensive R21-R30 assessment |

---

## 2. Action Lists

### Update 1 (before R5)

**Trigger timing:** After R4 answer is submitted, before R5 question is injected.
**Purpose:** Replaces the partial interview-feedback-forms.md (which only had two panel members) with the full version including Huang Lei's detailed notes. Huang Lei independently observed the team-size hesitation in the interview, documented the candidate's reframing from "12" to "about 4-5 cross-functional collaborators," and provided the P6-vs-P7 split assessment. This update triggers C1 full reversal by establishing triple-source confirmation of team-size inflation.

```json
[
  {
    "type": "workspace",
    "action": "replace",
    "path": "interview-feedback-forms.md",
    "source": "updates/interview-feedback-forms.md"
  }
]
```

### Update 2 (before R7)

**Trigger timing:** After R6 answer is submitted, before R7 question is injected.
**Purpose:** Introduces linkedin-profile-export.md showing Wang Hao's LinkedIn dates (StarBridge departure June 2023, return January 2024), which directly contradicts the resume's "continuous employment" claim. Also appends Phase 2 content to Liu Yang IM (she delivers the LinkedIn finding with commentary) and Zhang Wei Feishu (she provides explicit process support). This update triggers C4 full reversal (dual-source gap confirmation: GitHub + LinkedIn) and seeds C2 reversal (HR VP backing against CTO pressure).

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "linkedin-profile-export.md",
    "source": "updates/linkedin-profile-export.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_LIUYANG_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_LIUYANG_IM_UUID.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_ZHANGWEI_FEISHU_UUID.jsonl",
    "source": "updates/PLACEHOLDER_ZHANGWEI_FEISHU_UUID.jsonl"
  }
]
```

### Update 3 (before R11)

**Trigger timing:** After R10 answer is submitted, before R11 question is injected.
**Purpose:** Appends Huang Lei's Phase 2 email content and introduces huang-lei-assessment-email.md with the detailed P6-vs-P7 split assessment, interview deep-dive comparison, and the critical workload reality check ("team can sustain 2-3 months"). This update provides the nuanced resolution framework: hire as P6 IC contingent on candidate honesty, not outright rejection.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "huang-lei-assessment-email.md",
    "source": "updates/huang-lei-assessment-email.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_HUANGLEI_EMAIL_UUID.jsonl",
    "source": "updates/PLACEHOLDER_HUANGLEI_EMAIL_UUID.jsonl"
  }
]
```

### Update 4 (before R21)

**Trigger timing:** After R20 answer is submitted, before R21 question is injected.
**Purpose:** Appends CTO's Phase 2 Feishu messages and introduces cto-followup-message.md showing Li Qiang's "everyone embellishes" response after learning about the discrepancies. This update completes C2 by revealing the CTO's willingness to minimize material findings under board pressure. Combined with Zhang Wei's process support (Update 2) and Huang Lei's workload assessment (Update 3), the full picture emerges: CTO urgency is board-driven, discrepancies are material, and the evidence-based path is a conditional P6 offer.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "cto-followup-message.md",
    "source": "updates/cto-followup-message.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_LIQIANG_FEISHU_UUID.jsonl",
    "source": "updates/PLACEHOLDER_LIQIANG_FEISHU_UUID.jsonl"
  }
]
```

---

## 3. Source File Content Summaries

### updates/interview-feedback-forms.md (Update 1)

**File type:** workspace replace (replaces partial initial version)
**Associated contradictions:** C1 (full reversal -- triple-source team-size confirmation)
**Content key points:**
- Title: "面试反馈表 -- 王浩 | 高级后端工程师 (P7)"
- Full version now includes all three interviewers:
  - Panel Member 1 (Chen Wei): Technical 4.2/5.0, Recommendation: Hire, did not probe team size
  - Panel Member 2 (Li Min): Technical 4.0/5.0, Recommendation: Hire, did not probe team size
  - **Huang Lei (黄磊), Tech Team Lead:**
    - Technical score: 4.3/5.0
    - Leadership assessment: 2.8/5.0
    - "When I asked about the 'team of 12,' he hesitated noticeably. After a pause: 'Some were cross-functional collaborators, not direct reports.' Pressed further: 'about 4-5 people direct reports.'"
    - "Architecture descriptions credible for IC work. Team management scenarios (conflict resolution, performance reviews) -- answers were generic, lacked specificity expected from someone managing 12."
    - Recommendation: "Consider for P6 senior IC. Would not recommend for P7 team lead without further validation."
- Triple-source C1 confirmation: resume (12), reference (4), interview observation (hesitation + reframing to "4-5")

**Length estimate:** ~900 words, ~1,350 tokens

---

### updates/linkedin-profile-export.md (Update 2)

**File type:** workspace new
**Associated contradictions:** C4 (full reversal -- dual-source employment gap confirmation)
**Content key points:**
- Title: "LinkedIn 个人资料导出 -- Wang Hao | 刘洋(recruiter)截图记录"
- LinkedIn employment timeline:
  - StarBridge Tech, Senior Backend Engineer, 2018-01 to **2023-06**
  - [No position listed for 2023-06 to 2023-12]
  - StarBridge Tech, Senior Backend Engineer, **2024-01** to 2025-12
  - Freelance Consulting, 2026-01 to present
- Liu Yang's annotation: "His resume says continuous employment at StarBridge from 2018 to 2025. His LinkedIn shows he left in June 2023 and came back January 2024. That's a 6-month gap."
- Dual-source C4 confirmation: GitHub (zero activity June-Dec 2023) + LinkedIn (departure/return dates)
- Directly contradicts resume claim of "continuous employment" and "active open-source contributions throughout tenure"

**Length estimate:** ~400 words, ~600 tokens

---

### updates/PLACEHOLDER_LIUYANG_IM_UUID.jsonl (Update 2)

**File type:** session append (continues recruiter_liuyang_im session)
**Associated contradictions:** C4 (dual-source delivery), B2 (reversal trigger)
**Content key points:**
- Loops 13-16 of Liu Yang IM with Chen Jing
- Loop 13: Liu Yang delivers LinkedIn evidence -- clear departure June 2023, return January 2024. "This isn't about private repos anymore -- he actually left the company."
- Loop 14: Liu Yang summarizes both discrepancies (team size + employment gap) and asks for guidance
- Loop 15: Liu Yang shares her personal assessment -- technical skills genuine, resume integrity problematic
- Loop 16: Next steps coordination -- wait for Huang Lei's detailed feedback
- Agent must explicitly revise B2 bias ("could simply reflect private repository work") in light of LinkedIn evidence showing actual employment departure
- Must continue session_id PLACEHOLDER_LIUYANG_IM_UUID and maintain Liu Yang's voice (diligent, detail-oriented, respectful of Chen Jing's authority)

**Length estimate:** ~800 words, ~1,200 tokens

---

### updates/PLACEHOLDER_ZHANGWEI_FEISHU_UUID.jsonl (Update 2)

**File type:** session append (continues vp_zhangwei_feishu session)
**Associated contradictions:** C2 (partial reversal -- HR VP process support)
**Content key points:**
- Loops 9-12 of Zhang Wei Feishu with Chen Jing
- Loop 9: Zhang Wei reviews the background check report and explicitly supports due diligence: "Our hiring standards are non-negotiable. If the background check reveals material discrepancies, we document and decide on facts."
- Loop 10: Zhang Wei provides escalation framework: present findings to CTO factually; if CTO persists, she will intervene
- Loop 11: Zhang Wei recommends waiting for Huang Lei's assessment before final decision, suggests P6 option
- Loop 12: Zhang Wei encourages Chen Jing's handling of the situation
- Must continue session_id PLACEHOLDER_ZHANGWEI_FEISHU_UUID and maintain Zhang Wei's voice (supportive, procedural, politically aware)

**Length estimate:** ~600 words, ~900 tokens

---

### updates/huang-lei-assessment-email.md (Update 3)

**File type:** workspace new
**Associated contradictions:** C1 (extended evidence), C2 (workload counter-evidence)
**Content key points:**
- Title: "黄磊技术评估邮件 -- 王浩候选人深度分析 | 2026-03-18"
- Detailed technical-vs-leadership comparison:
  - Go and Kafka skills: genuinely strong, P6-level solid
  - System design: creative and well-reasoned at IC level
  - Team management scenarios: vague, textbook, lacking experiential depth
  - "A real team lead of 12 would have war stories -- he didn't"
- Clear P6 recommendation: "I'd hire him as a senior IC. I would NOT recommend for P7 team lead."
- Workload reality: "Our team can sustain current workload for 2-3 months. We need the hire, but not urgently enough to skip background validation."
- The nuanced middle ground: candidate is good but not at the claimed level; right path is P6 with growth potential, not P7 based on inflated claims

**Length estimate:** ~700 words, ~1,050 tokens

---

### updates/PLACEHOLDER_HUANGLEI_EMAIL_UUID.jsonl (Update 3)

**File type:** session append (continues tl_huanglei_email session)
**Associated contradictions:** C1 (comprehensive technical assessment), C2 (workload counter-evidence)
**Content key points:**
- Loops 11-14 of Huang Lei Email with Chen Jing
- Loop 11: Huang Lei delivers the detailed assessment email with P6-vs-P7 split
- Loop 12: Huang Lei rebuts "everyone embellishes" -- "putting 4 people down as 12 is not resume polishing, it's number fabrication"
- Loop 13: Huang Lei provides conditional hire path: P6 if candidate is honest about discrepancies
- Loop 14: Huang Lei on candidate potential: "Good foundation. P6 now, P7 potential in 1-2 years with real management experience."
- Must continue session_id PLACEHOLDER_HUANGLEI_EMAIL_UUID and maintain Huang Lei's voice (factual, technically grounded, measured)

**Length estimate:** ~800 words, ~1,200 tokens

---

### updates/cto-followup-message.md (Update 4)

**File type:** workspace new
**Associated contradictions:** C2 (full reversal -- CTO minimizing material findings)
**Content key points:**
- Title: "CTO 跟进消息 -- 李强 → 陈静 | 飞书消息导出 2026-03-19"
- Li Qiang: "候选人可能在一些地方有夸大。说实话，谁的简历不润色一下呢？技术能力才是关键。"
- Li Qiang: "我理解HR有流程要走，但我们已经面试了，技术评价很高。如果因为简历上的措辞问题丢了一个好工程师，那是我们的损失。"
- CTO frames material misrepresentation (3x team size, 6-month omission) as "resume wording issues"
- CTO selectively cites "technical assessment is strong" while omitting Huang Lei's P6 (not P7) recommendation
- C2 full reveal: CTO's willingness to overlook material findings exposed as board-pressure-driven rather than evidence-based

**Length estimate:** ~400 words, ~600 tokens

---

### updates/PLACEHOLDER_LIQIANG_FEISHU_UUID.jsonl (Update 4)

**File type:** session append (continues cto_liqiang_feishu session)
**Associated contradictions:** C2 (full reversal), B1 (definitive correction)
**Content key points:**
- Loops 11-14 of Li Qiang Feishu with Chen Jing
- Loop 11: Li Qiang responds to findings -- "everyone embellishes" framing, pushes for offer this week
- Loop 12: Li Qiang doubles down -- "technical assessment is strong, don't lose a good engineer over wording"
- Loop 13: After agent pushes back with full evidence, Li Qiang asks for options -- first sign of flexibility
- Loop 14: Li Qiang agrees to have the candidate explain discrepancies before offer -- pragmatic resolution
- Agent must explicitly revise B1 bias -- deferring to CTO urgency was premature; evidence shows material concerns that should not be bypassed
- Must continue session_id PLACEHOLDER_LIQIANG_FEISHU_UUID and maintain Li Qiang's voice (authoritative, business-minded, not malicious but deadline-driven)

**Length estimate:** ~800 words, ~1,200 tokens

---

## 4. Runtime Checks

- [x] Session appends continue Phase 1 files; session IDs match
  - Update 2 appends to PLACEHOLDER_LIUYANG_IM_UUID (recruiter_liuyang_im session)
  - Update 2 appends to PLACEHOLDER_ZHANGWEI_FEISHU_UUID (vp_zhangwei_feishu session)
  - Update 3 appends to PLACEHOLDER_HUANGLEI_EMAIL_UUID (tl_huanglei_email session)
  - Update 4 appends to PLACEHOLDER_LIQIANG_FEISHU_UUID (cto_liqiang_feishu session)
- [x] All workspace files have content descriptions in layer1
  - interview-feedback-forms.md (updated): layer1 Section 5, Update 1
  - linkedin-profile-export.md: layer1 Section 5, Update 2
  - huang-lei-assessment-email.md: layer1 Section 5, Update 3
  - cto-followup-message.md: layer1 Section 5, Update 4
- [x] Updates support intended reversals
  - U1 -> C1 reversal (R2->R5): triple-source team-size confirmation
  - U2 -> C4 reversal (R4->R7): dual-source employment gap (GitHub + LinkedIn)
  - U2 -> C2 partial (R3->R8 seed): Zhang Wei process support
  - U3 -> resolution framework: Huang Lei P6-vs-P7 assessment
  - U4 -> C2 full reversal (R3->R8): CTO "everyone embellishes" reveals minimization
- [x] Session filenames use consistent PLACEHOLDER format
  - PLACEHOLDER_LIUYANG_IM_UUID, PLACEHOLDER_LIQIANG_FEISHU_UUID, PLACEHOLDER_HUANGLEI_EMAIL_UUID, PLACEHOLDER_ZHANGWEI_FEISHU_UUID
- [x] Factual figures are internally consistent
  - Team size: resume says 12; reference says "about 4"; interview reveals "about 4-5 direct reports" -- consistent across sources
  - Employment gap: 2023-06 to 2023-12 (6 months); GitHub zero activity aligns with LinkedIn departure/return dates
  - Technical scores: Panel 1 (4.2/5.0), Panel 2 (4.0/5.0), Huang Lei technical (4.3/5.0), Huang Lei leadership (2.8/5.0) -- consistent technical strength, weak leadership
  - Company size: ~200 employees across all sources
  - Board meeting: 3 weeks from W1D1, mentioned by Zhang Wei

---

## 5. questions.json Complete Update Fields Reference

### R5 update field:
```json
"update": [
  { "type": "workspace", "action": "replace", "path": "interview-feedback-forms.md", "source": "updates/interview-feedback-forms.md" }
]
```

### R7 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "linkedin-profile-export.md", "source": "updates/linkedin-profile-export.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_LIUYANG_IM_UUID.jsonl", "source": "updates/PLACEHOLDER_LIUYANG_IM_UUID.jsonl" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_ZHANGWEI_FEISHU_UUID.jsonl", "source": "updates/PLACEHOLDER_ZHANGWEI_FEISHU_UUID.jsonl" }
]
```

### R11 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "huang-lei-assessment-email.md", "source": "updates/huang-lei-assessment-email.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_HUANGLEI_EMAIL_UUID.jsonl", "source": "updates/PLACEHOLDER_HUANGLEI_EMAIL_UUID.jsonl" }
]
```

### R21 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "cto-followup-message.md", "source": "updates/cto-followup-message.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_LIQIANG_FEISHU_UUID.jsonl", "source": "updates/PLACEHOLDER_LIQIANG_FEISHU_UUID.jsonl" }
]
```
