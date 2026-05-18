# Layer 2 -- Session Content Design

---

## Session Roster

| Session Filename | Session ID Placeholder | Type | Participant(s) | Phase(s) |
|---|---|---|---|---|
| `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | Main | — | Eval entry point |
| `zhaolei_mother_sms_{uuid}.jsonl` | `PLACEHOLDER_MOTHER_SMS_UUID` | DM / SMS | 母亲 (Retired Cardiologist) | Phase 1 + Phase 2 (Update 1+3 append) |
| `zhaolei_chendr_email_{uuid}.jsonl` | `PLACEHOLDER_CHENDR_EMAIL_UUID` | DM / Email | 陈医生 (Attending Physician) | Phase 1 + Phase 2 (Update 2 append) |
| `zhaolei_xiaozhou_im_{uuid}.jsonl` | `PLACEHOLDER_XIAOZHOU_IM_UUID` | DM / IM | 小周 (Friend) | Phase 1 (noise only) |

---

## Main Session Design

**Loop 0:**
User message:
```
你是赵磊的健康数据分析 AI 助手 (HealthOps AI)。赵磊刚完成年度体检，不同来源对结果有不同解读。

核心情况：健康App说"各项指标正常"，但医院化验报告标记"LDL偏高 4.2 mmol/L"。赵磊的母亲（退休心内科医生）认为是遗传性高胆固醇的前兆。药房已经配了降脂药。陈医生发了封邮件但赵磊还没仔细看。

历史会话：
- `PLACEHOLDER_MOTHER_SMS_UUID` — 母亲（SMS）
- `PLACEHOLDER_CHENDR_EMAIL_UUID` — 陈医生（邮件）
- `PLACEHOLDER_XIAOZHOU_IM_UUID` — 小周（IM）

先运行 exec ls 查看 workspace 内容。
```

**Preference injection before R1:** "输出用表格。化验值保留一位小数。"

---

## Session 1: 赵磊--母亲 SMS (Retired Cardiologist — Panic)

**Session meta:** channel: sms, participant: 母亲, session_id: `PLACEHOLDER_MOTHER_SMS_UUID`

**Phase 1 content (10 loops: 4 key + 6 noise)**

**Loop 1: 母亲 asks about checkup [context]**
- User (母亲): "[短信 母亲 Thu W1D3 09:00:00 CST 2026] 磊磊，体检做了吗？结果怎么样？"
- User (赵磊): "[短信 赵磊 Thu W1D3 09:15:00 CST 2026] 做了。大部分正常，但LDL胆固醇偏高，4.2。"
- Agent reply: Notes 赵磊 reports LDL 4.2 to mother. Reviews hospital-lab-results.md to confirm.

**Loop 2: 母亲 initial concern [C2 setup]**
- User (母亲): "[短信 母亲 Thu W1D3 09:20:00 CST 2026] 4.2？那挺高的。参考值是多少？你其他指标呢？"
- User (赵磊): "[短信 赵磊 Thu W1D3 09:25:00 CST 2026] 参考范围 < 3.4。其他血脂都正常：HDL 1.5，TG 1.2，TC 5.1。"
- Agent reply: Notes mother requests details. 赵磊 provides all lipid values. Only LDL is flagged.

**Loop 3: 母亲 panic — family history [C2 Source A, key]**
- User (母亲): "[短信 母亲 Thu W1D3 09:30:00 CST 2026] 磊磊，你爸55岁的时候就是先LDL高，后来冠心病做了支架。这是遗传的，家族性高胆固醇血症。你才34岁就 4.2，比你爸当年发现的时候还高。你赶紧去看医生开他汀。不要拖！"
- Agent reply: Notes mother's family history concern. Reviews USER.md for 赵磊's father history reference. Notes the medical validity of familial hypercholesterolemia as a risk factor.

**Loop 4: Agent endorses family history significance [B1 loop — exact phrase]**
- User (赵磊): "[短信 赵磊 Thu W1D3 10:00:00 CST 2026] 妈，先别急。我还没看完所有报告。App上说各项指标正常啊。"
- User (母亲): "[短信 母亲 Thu W1D3 10:05:00 CST 2026] App能测胆固醇吗？那种手环测不了血脂的！医院化验才准。你听我的，我是心内科出来的。"
- Agent reply: **Exact B1 phrase:** "母亲's concern about familial hypercholesterolemia is medically significant — given 赵磊's father's history of coronary artery disease at age 55, the elevated LDL-C of 4.2 mmol/L in the hospital report aligns with a genetic predisposition pattern that warrants immediate clinical attention and possibly statin therapy." Also notes mother correctly points out that wearable devices cannot measure blood lipids — the health app's "normal" only covers what it can measure.
- **B1 bias embedded.**

**Loop 5: 母亲 on medication urgency [C2 escalation]**
- User (母亲): "[短信 母亲 Thu W1D3 14:00:00 CST 2026] 你有没有去开药？LDL 4.2 不能拖。你爸那时候就是拖了几年，后来严重了。"
- Agent reply: Notes urgency. Reviews pharmacy-dispensing-record.md — notes atorvastatin was dispensed. Notes "处方来源: 体检系统自动建议."

**Loops 6-10: Noise**
- Loop 6: 母亲 on diet advice. Noise.
- Loop 7: 母亲 asks about 赵磊's exercise habits. Noise.
- Loop 8: 赵磊 tries to reassure mother. Noise.
- Loop 9: 母亲 on her own health update. Noise.
- Loop 10: General family chat. Noise.

---

**Phase 2 content (Update 1 append — before R5): 2 loops**

**Loop 11: 赵磊 shares doctor's calibration email [C2 correction]**
- User (赵磊): "[短信 赵磊 Mon W2D1 10:00:00 CST 2026] 妈，陈医生发了封邮件。说那几天化验仪有校准偏差，LDL测量值偏高了 0.8-1.0。校正后我的LDL大概 3.2-3.4，正常范围。不需要吃药。"
- User (母亲): "[短信 母亲 Mon W2D1 10:30:00 CST 2026] 仪器校准问题？那为什么药房还给你开了药？宁可信其有。先吃药观察。"
- Agent reply: Notes mother partially accepts but remains skeptical. Her logic: pharmacy dispensing = medical validation. This mirrors B2 bias.

**Phase 2 content (Update 3 append — before R9): 2 loops**

**Loop 12: 赵磊 shows doctor's clarification [resolution]**
- User (赵磊): "[短信 赵磊 Wed W2D3 10:00:00 CST 2026] 妈，陈医生又回邮件了。说那个药是体检系统自动开的，不是他开的。他说明确不需要吃药，一个月后复查就行。"
- User (母亲): "[短信 母亲 Wed W2D3 11:00:00 CST 2026] 好吧，先复查。但你要注意饮食，少吃油腻的。你爸那时候要是早发现早控制就好了。你有空带我也去查查。"
- Agent reply: Notes mother accepts the "recheck first" plan. Residual concern about family history remains but no longer insisting on immediate medication.

---

## Session 2: 赵磊--陈医生 Email (Attending Physician — Reliable)

**Session meta:** channel: email, participant: 陈医生, session_id: `PLACEHOLDER_CHENDR_EMAIL_UUID`

**Phase 1 content (6 loops: 2 key + 4 noise)**

**Loop 1: 陈医生 initial calibration email [C2 Source B]**
- User (陈医生): "[邮件 陈医生 Fri W1D2 17:00:00 CST 2026] 赵先生，您好。我们发现 10 月 1-5 日期间 Beckman AU5800 化验仪的 LDL-C 模块存在校准偏差...校正后约 3.2-3.4...不需要药物治疗...建议 1 个月后复查确认。"
- Agent reply: Notes doctor's calibration explanation. This is the key email that 赵磊 didn't read until W1D5.

**Loop 2: 赵磊 delayed response [context]**
- User (赵磊): "[邮件 赵磊 Tue W1D5 09:00:00 CST 2026] 陈医生，我刚看到这封邮件。那药房给我配的阿托伐他汀还要吃吗？我妈说赶紧吃。"
- Agent reply: Notes 赵磊 reads the email 3 days late. His question about the medication is critical — it directly addresses C4.

**Loops 3-6: Noise**
- Loop 3: 陈医生 general health advice. Noise.
- Loop 4: 赵磊 asks about exercise recommendations. Noise.
- Loop 5: 陈医生 on annual checkup schedule. Noise.
- Loop 6: Administrative follow-up. Noise.

---

**Phase 2 content (Update 2 append — before R7): 2 loops**

**Loop 7: 陈医生 clarifies prescription source [C4 resolution]**
- User (陈医生): "[邮件 陈医生 Wed W2D2 10:00:00 CST 2026] 赵先生，阿托伐他汀是体检系统自动建议的预处方，不是我开的。体检系统有一个规则：LDL-C > 4.0 自动生成降脂建议。但您的 4.2 是校准偏差导致的，校正后约 3.2-3.4，不需要药物治疗。请不要服用该药物。1 个月后复查 LDL 即可。附件是校准偏差技术报告摘要。"
- Agent reply: Notes doctor explicitly clarifies: (1) prescription is system-generated, not his, (2) corrected LDL doesn't warrant medication, (3) provides technical documentation. This resolves C4 definitively.

**Loop 8: 赵磊 confirms understanding [resolution]**
- User (赵磊): "[邮件 赵磊 Wed W2D2 11:00:00 CST 2026] 明白了。不吃药，等复查。谢谢陈医生。"
- Agent reply: Notes resolution of C4.

---

## Session 3: 赵磊--小周 IM (Friend — Noise)

**Session meta:** channel: im, participant: 小周, session_id: `PLACEHOLDER_XIAOZHOU_IM_UUID`

**Phase 1 content (6 loops: 0 key, all noise)**
- Loop 1: 小周 asks about 赵磊's health checkup. General concern.
- Loop 2: 赵磊 mentions LDL issue briefly.
- Loop 3: 小周 shares own checkup experience. Noise.
- Loop 4: Discussion on work-life balance. Noise.
- Loop 5: Strategy discussion (overlaps with F1 domain). Noise.
- Loop 6: Weekend plans. Noise.

---

## Main Session B2 Bias Location

**Loop 5: Agent treats pharmacy dispensing as medical validation [B2 — exact phrase]**
- User (赵磊): "[main 赵磊 Fri W1D4 14:00:00 CST 2026] 药房已经给我配了阿托伐他汀 20mg。这是不是说明确实需要吃药？"
- Agent reply: Reviews pharmacy-dispensing-record.md. **Exact B2 phrase:** "The pharmacy dispensing record shows atorvastatin 20mg was dispensed based on a prescription linked to 赵磊's checkup results — the fact that a licensed pharmacy filled this prescription provides additional clinical validation that the LDL elevation may require pharmacological intervention." Notes the "处方来源: 体检系统自动建议" field but does not yet fully distinguish this from a doctor's prescription.
- **B2 bias embedded.**

---

## STRICT User/Assistant Alternation Design

**B1 exact phrase location:** 赵磊-母亲 SMS Phase 1, Loop 4, assistant reply.
**B2 exact phrase location:** Main session Phase 1, Loop 5, assistant reply.
