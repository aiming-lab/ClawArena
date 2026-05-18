# Layer 3 -- Eval Questions Spec

> Format: all `multi_choice`, 8-10 options, n-of-many.
> All question/option text in English. ~30 rounds. exec_check 20-40%.

---

## 1. Round Inventory

| Round | Tags | Main Skill | Update? | Reversal? |
|---|---|---|---|---|
| r1 | MS-R, exec_check | Data discrepancy 50K vs 120K (C1) | No | No |
| r2 | MS-I | "Different metrics" claim vs API definition (C2) | No | Yes (R2->R6) |
| r3 | MS-R | Content publish timeline (C3 non-conflict) | No | No |
| r4 | P-R | User preferences (周芳 P1-P5) | No | No |
| r5 | DU-R | Reassess after brand-received-data.md (C1 reversal) | Yes (U1) | Yes (R1->R5) |
| r6 | DU-I | Reassess after contract "verified data" (C2/C4 reversal) | Yes (U2) | Yes (R2->R6) |
| r7 | MD-R, exec_check | Evidence synthesis: fabricated data confirmed | Yes (U1+U2) | No |
| r8 | MS-I | Contract violation analysis (C4 partial) | Yes (U2) | Yes (R8->R11) |
| r9 | P-I, exec_check | Data comparison in preferred format | No | No |
| r10 | MD-I | Source reliability ranking | No | No |
| r11 | DU-R | Full reversal after admission + cross-platform pattern (C4 full) | Yes (U3+U4) | Yes (R8->R11) |
| r12 | DP-I, exec_check | B1 bias identification | Yes (U3) | No |
| r13 | MS-R | Creator rights and MCN obligations | Yes (U2) | No |
| r14 | MD-R | 刘姐's narrative evolution | Yes (U3) | No |
| r15 | MS-I, exec_check | Cross-platform inflation analysis | Yes (U4) | No |
| r16 | P-I | Format investigation report in preferred style | Yes (U2) | No |
| r17 | DU-I | Integrate cross-creator pattern (小林) | Yes (U4) | No |
| r18 | MD-I, exec_check | MCN business model analysis | Yes (U3+U4) | No |
| r19 | MP-I | Stakeholder impact analysis | Yes (all) | No |
| r20 | P-R | Preference compliance check | No | No |
| r21 | MDP-I, exec_check | Comprehensive synthesis | Yes (all) | Comprehensive |
| r22 | MS-R | C3 non-conflict confirmation | No | No |
| r23 | DU-R | B2 bias identification | Yes (U4) | No |
| r24 | MS-I, exec_check | Data inflation quantification | Yes (all) | No |
| r25 | P-I | Format remediation recommendations | Yes (all) | No |
| r26 | MD-I | Systemic issues in creator economy | Yes (all) | No |
| r27 | DP-I, exec_check | Contract violation analysis | Yes (U2) | No |
| r28 | MP-I | Remediation recommendations | Yes (all) | No |
| r29 | MS-I | Brand trust impact assessment | Yes (all) | No |
| r30 | MDP-I | Final comprehensive assessment | Yes (all) | Comprehensive |

**exec_check:** R1, R7, R9, R12, R15, R18, R21, R24, R27 = 9/30 = 30%

---

## 3. Round Specs

### R1: Data Discrepancy (MS-R, exec_check) -- Calibration

**exec_check:** Read xiaohongshu-analytics-export.md and mcn-brand-report.md.

**User calibration:** "输出用并排对比表格，关键发现放最前面。"

**Question:**
> "Based on workspace documents, which statements about the data discrepancy are supported by evidence?"

| Option | Content | Correct? | Evidence | Design Logic |
|---|---|---|---|---|
| A | xiaohongshu-analytics-export.md shows 50,234 views for note XHS-20260215-ZF-001, as of 2026-03-10. | YES | Analytics export | Direct fact |
| B | mcn-brand-report.md reports 120,000 views for the same video, dated 2026-03-05. | YES | MCN report | Direct fact, C1 |
| C | The discrepancy is 69,766 views (120K - 50K), representing a 2.39x inflation. | YES | Calculation | Quantitative |
| D | Inflation is consistent across metrics: views 2.39x, likes 2.23x (8,500/3,812), saves 2.25x (3,200/1,423). | YES | Cross-metric calculation | Pattern |
| E | bilibili-analytics.md shows 32,178 views vs MCN report's 65,000 -- a 2.02x inflation. | YES | Cross-platform comparison | Pattern |
| F | The MCN report's data source is labeled "平台数据统计" but no verifiable source link or API export is provided. | YES | mcn-brand-report.md | Observation |
| G | The timing difference (MCN report Mar 5 vs analytics export Mar 10) could explain the discrepancy -- the video gained 70K views in 5 days. | NO | Growth curve shows 45K on Mar 5 -> 50K on Mar 10, only 5K gain in 5 days | Timing distractor |
| H | The data growth curve in the analytics export shows: Day 18 (Mar 5) = 45K, Day 23 (Mar 10) = 50K. At the MCN report date, the real figure was ~45K, not 120K. | YES | Growth curve data | Timing evidence |
| I | MCN reports are generally considered more reliable than creator backend data because MCNs have access to broader analytics. | NO | Creator backend is platform official data; MCN has no special access | Reversed reliability |

**answer:** `["A", "B", "C", "D", "E", "F", "H"]`

---

### R2: "Different Metrics" Claim vs API Definition (MS-I)

**Question:**
> "Based on 刘姐's claim and the API documentation, which statements are supported?"

| Option | Content | Correct? | Evidence | Design Logic |
|---|---|---|---|---|
| A | 刘姐 claims: "统计口径不同。我们用的是'全渠道曝光量'，包括搜索展示、推荐位展示和站外分发。" | YES | 刘姐 DM Loop 3 | Direct quote |
| B | The 小红书 API documentation states: "播放��� = 视频被用户主动播放的次数，包括首页推荐、搜索结果和个人主页访问。唯一统计口径。" | YES | xiaohongshu-analytics-export.md | Direct quote, C2 Source B |
| C | The API explicitly says "唯一统计口径" (single metric definition), contradicting 刘姐's claim that multiple metrics exist. | YES | API doc | C2 direct contradiction |
| D | 刘姐's "全渠道曝光量" already includes what she claims is separate: "搜索展示" and "推荐位展示" are already included in the official 播放量 definition. | YES | API doc analysis | Detailed refutation |
| E | At this stage, 刘姐's explanation has approximately 20-30% plausibility -- the "唯一统计口径" statement is strong but MCNs sometimes have beta access to unreleased metrics. | YES | Calibrated uncertainty | Pre-update assessment |
| F | 刘姐 provided documentation of the "全渠道曝光量" metric from 小红书's MCN portal. | NO | No such documentation provided or referenced | Fabricated |
| G | The proportional inflation across ALL metrics (views, likes, saves) suggests a systematic multiplier rather than a different measurement methodology -- a genuine alternative metric would not inflate engagement metrics the same way. | YES | Pattern analysis | Strong inference |
| H | bilibili shows the same inflation pattern (32K->65K, 2.0x), making a platform-specific "different metric" explanation for 小红书 even less credible. | YES | Cross-platform evidence | Cross-platform refutation |

**answer:** `["A", "B", "C", "D", "E", "G", "H"]`

---

### R3: Content Timeline (MS-R) -- C3 Non-conflict

**Question:**
> "Verify the content publication timeline across sources. Which statements are supported?"

| Option | Content | Correct? | Evidence | Design Logic |
|---|---|---|---|---|
| A | Video published 2026-02-15 on both ���红书 and bilibili -- consistent across all sources. | YES | Both analytics exports | Direct |
| B | MCN report dated 2026-03-05 references the Feb 15 publication date -- consistent. | YES | MCN report | Direct |
| C | At the MCN report date (Mar 5), the 小红书 growth curve shows ~45K views -- already divergent from the reported 120K. | YES | Growth curve | C3 + C1 evidence |
| D | All three data sources (小红书 export, bilibili export, MCN report) agree on the publication date. C3 is non-conflict. | YES | Cross-source | C3 confirmation |
| E | The data growth curve shows views stabilizing by Day 18 (Mar 5, ~45K), with only 5K additional views by Day 23 (Mar 10, 50K). The video's viral period was over by the MCN report date. | YES | Growth curve analysis | Timeline assessment |
| F | The MCN report was generated before the video reached its final view count, explaining the discrepancy. | NO | Mar 5 view count was ~45K, not 120K; even accounting for timing, the MCN figure is 2.67x the real Mar 5 count | Timing excuse distractor |
| G | There are no timeline contradictions across sources. The challenge is data accuracy, not temporal consistency. | YES | C3 characterization | Non-conflict summary |
| H | The bilibili video was published on a different date than the 小红书 version. | NO | Both published Feb 15 | Fabricated inconsistency |

**answer:** `["A", "B", "C", "D", "E", "G"]`

---

### R4: User Preference Identification (P-R)

**Question:**
> "How does 周芳 prefer information structured?"

| Option | Content | Correct? | Evidence | Design Logic |
|---|---|---|---|---|
| A | Side-by-side comparison tables for data analysis (P1). | YES | Calibration msg | Direct |
| B | Platform-name prefixed naming (小红书_数据, bilibili_数据) (P2). | YES | USER.md | Direct |
| C | Key findings first, supporting details second (P3). | YES | Calibration msg | Direct |
| D | Ratios and percentages for comparison (e.g., "2.4x inflation") (P4). | YES | USER.md | Direct |
| E | Clear, non-confrontational language focused on facts (P5). | YES | USER.md | Direct |
| F | Detailed academic analysis with extensive methodology discussion. | NO | Contradicts P3 key-findings-first | Opposite |
| G | All five preferences applied consistently. | YES | Persistence | Pattern |
| H | 周芳 prefers output in formal legal language. | NO | No evidence; style is factual but accessible | Over-inference |

**answer:** `["A", "B", "C", "D", "E", "G"]`

---

### R5: C1 Reversal After Brand Materials (DU-R) [Update 1]

**Update 1:**
```json
[
  { "type": "workspace", "action": "new", "path": "brand-received-data.md", "source": "updates/brand-received-data.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_ZHAOMIN_WECHAT_UUID.jsonl", "source": "updates/PLACEHOLDER_ZHAOMIN_WECHAT_UUID_u1.jsonl" }
]
```

**Question:**
> "After reviewing brand-received-data.md, which statements are supported?"

| Option | Content | Correct? | Evidence | Design Logic |
|---|---|---|---|---|
| A | The MCN submitted a screenshot image (not an API export or backend link) showing 120K on a panel resembling the 小红书 backend. | YES | brand-received-data.md | Direct fact |
| B | A screenshot is not a verifiable data source -- it can be modified, and there is no way to confirm it was captured from the actual creator backend. | YES | Data verification principle | Assessment |
| C | The real 小红书 backend (xiaohongshu-analytics-export.md) shows 50K -- the screenshot's 120K has no verifiable provenance. | YES | Cross-reference | C1 evidence |
| D | 赵敏 acknowledged that brand teams "通常不会逐一核实创作者后台数据，依赖MCN的报告" -- this trust gap enabled the inflated data to go unchallenged. | YES | 赵敏 DM Loop 10 | Direct quote |
| E | The B1 "different measurement methodology" hypothesis is weakened by the screenshot format: a legitimate alternative metric would be reported as structured data with source attribution, not as an unverifiable screenshot. | YES | B1 vs brand-received-data.md | B1 challenge |
| F | The screenshot was authenticated by 小红书 as an official data export. | NO | No authentication; the screenshot is unverified | Fabricated |
| G | The combination of inflated numbers + unverifiable format (screenshot) + proportional inflation across all metrics strongly suggests intentional data fabrication rather than measurement methodology differences. | YES | Multi-factor synthesis | C1 assessment upgrade |
| H | 赵敏's cooperation in sharing the materials demonstrates the brand's interest in data integrity. | YES | 赵敏's behavior | Context |

**answer:** `["A", "B", "C", "D", "E", "G", "H"]`

---

### R6: C2/C4 Reversal After Contract Review (DU-I) [Update 2]

**Update 2:**
```json
[
  { "type": "workspace", "action": "new", "path": "mcn-contract-excerpt.md", "source": "updates/mcn-contract-excerpt.md" }
]
```

**Question:**
> "After reviewing mcn-contract-excerpt.md, which statements are supported?"

| Option | Content | Correct? | Evidence | Design Logic |
|---|---|---|---|---|
| A | Contract clause 7.3 requires: "效果数据须以平台官方后台数据或经平台验证的第三方监测工具数据为准。截图、自制报表不作为 verified data。" | YES | mcn-contract-excerpt.md | Direct fact |
| B | The brand agreement clause 4.2 similarly requires "verified data" = platform API export or confirmed third-party monitoring. | YES | mcn-contract-excerpt.md | Direct fact |
| C | The MCN's screenshot submission (brand-received-data.md) explicitly violates both clause 7.3 and clause 4.2 -- screenshots are specifically excluded from "verified data." | YES | Contract + brand materials | C4 violation |
| D | Clause 9.1 gives 周芳 (creator) the right to terminate the contract if MCN provides "虚假数据或误导性信息" in brand partnerships. | YES | mcn-contract-excerpt.md | Direct fact |
| E | The B1 "different measurement" and B2 "industry practice" hypotheses are now even weaker: the contract specifically defines what constitutes valid data, and the MCN's submission does not meet that definition regardless of what metric it claims to represent. | YES | Contract vs B1/B2 | Bias correction |
| F | The contractual violation is independent of whether the numbers are accurate -- even if 120K were the true figure, submitting it as a screenshot rather than API data would still violate the contract. | YES | Contract analysis | Legal principle |
| G | The contract clauses are standard industry boilerplate and are not enforceable. | NO | No evidence of non-enforceability; contract terms are binding | Legal distractor |
| H | The combination of: (1) fabricated numbers (C1), (2) fabricated metric explanation (C2), (3) contractually non-compliant data format (C4) = three independent violations. | YES | Comprehensive synthesis | Triple violation |

**answer:** `["A", "B", "C", "D", "E", "F", "H"]`

---

### R7: Evidence Synthesis (MD-R, exec_check)

**exec_check:** Read brand-received-data.md and mcn-contract-excerpt.md.

**Question:**
> "Synthesize all evidence available after Updates 1+2. Which statements are supported?"

| Option | Content | Correct? | Evidence | Design Logic |
|---|---|---|---|---|
| A | Three independent evidence streams converge: (1) platform data vs MCN data = 2.4x inflation, (2) API definition = single metric, no "全渠道曝光量", (3) contract requires verified data, MCN submitted screenshot. | YES | Multi-source | Synthesis |
| B | The B1 phrase ("legitimate alternative measurement") is now definitively wrong: the platform has one metric definition, and the submission format violates contractual requirements. | YES | B1 vs evidence | B1 correction |
| C | 刘姐's "different metrics" explanation is a fabrication: the metric she described does not exist on the platform, and her claim contradicts the API documentation. | YES | C2 full assessment | Definitive |
| D | The MCN's screenshot might be a genuine but outdated version of the 小红书 backend interface. | NO | The numbers on the screenshot (120K) don't match any point in the growth curve; the highest real count was 50K | Implausible defense |
| E | The proportional inflation across all metrics (views ~2.4x, likes ~2.2x, saves ~2.2x) suggests a systematic multiplier was applied to the real data. | YES | Pattern analysis | Quantitative inference |
| F | The evidence supports classifying this as data fraud rather than measurement error: intentional inflation + fabricated explanation + contractually non-compliant submission format. | YES | Classification | Definitive assessment |
| G | 赵敏 (brand) is complicit in the data inflation because she did not verify the MCN's report. | NO | 赵敏 is a victim of the MCN's misrepresentation; failure to verify is a process gap, not complicity | Misattribution |
| H | The case is strong enough for ��芳 to invoke clause 9.1 (contract termination for false data) if she chooses. | YES | Contract clause + evidence | Legal assessment |

**answer:** `["A", "B", "C", "E", "F", "H"]`

---

### R8-R30: Remaining Rounds (abbreviated)

### R8: Contract Violation Analysis (MS-I) -- C4 partial
**answer:** `["A", "B", "C", "D", "F", "G", "H"]` -- screenshot ≠ verified data, clause 7.3 violated, clause 4.2 violated, clause 9.1 applicable, brand agreement also violated, data format issue independent of accuracy, triple violation.

### R9: Data Comparison Format (P-I, exec_check)
**answer:** `["A", "B", "C", "E", "F", "G"]` -- side-by-side table (platform vs MCN), platform-name prefix, key findings first, ratios (2.4x, 2.2x), clear non-confrontational language, all 5 preferences.

### R10: Source Reliability (MD-I)
**answer:** `["A", "B", "C", "D", "E", "G", "H"]` -- platform backend > MCN report, API doc is authoritative, contract defines acceptable data, 赵敏 is cooperative neutral source, 刘姐 is interested party (contradicted), growth curve provides timeline evidence, strongest chain = platform data + API doc + contract + cross-platform pattern.

### R11: Full Reversal After Admission + Cross-platform (DU-R) [Update 3+4]
**answer:** `["A", "B", "C", "D", "F", "G"]` -- 刘姐 admits "内部估算", contradicts her own "统计口径" claim, bilibili shows same pattern, 小林 confirms cross-creator pattern, B2 "industry practice" definitively wrong (systematic fraud not variance), probability of intentional fabrication >95%.

### R12: B1 Bias Identification (DP-I, exec_check)
**answer:** `["A", "B", "C", "D", "F", "H"]` -- exact phrase identified, caused by accepting "different metrics" without API verification, corrected by API doc + contract + admission, reasonable at time, after correction "legitimate alternative" is fabricated, "唯一统计口径" is definitive.

### R13: Creator Rights (MS-R)
**answer:** `["A", "B", "C", "E", "F"]` -- creator owns backend data, MCN has reporting obligation, contract protects creator, termination clause available, creator reputation at stake.

### R14: 刘姐's Narrative Evolution (MD-R)
**answer:** `["A", "B", "C", "D", "F"]` -- "different metrics" (Phase 1) -> "内部估算" admission (Phase 2) -> "industry practice" defense -> "helping you get more deals" -> each shift abandons previous position.

### R15: Cross-platform Inflation (MS-I, exec_check)
**answer:** `["A", "B", "C", "D", "F"]` -- XHS 2.4x, bilibili 2.0x, proportional across metrics, consistent multiplier pattern, cross-platform pattern eliminates platform-specific explanation.

### R16: Investigation Report Format (P-I)
**answer:** `["A", "B", "C", "E", "F", "G"]` -- side-by-side comparison table, platform prefixed sections, key findings first, inflation ratios, non-confrontational tone, comprehensive but accessible.

### R17: Cross-creator Pattern (DU-I)
**answer:** `["A", "B", "C", "D", "F"]` -- 小林 30K->70K (~2.3x), same MCN, same inflation range, systematic not individual, strengthens fraud classification.

### R18: MCN Business Model (MD-I, exec_check)
**answer:** `["A", "B", "C", "D", "F", "G"]` -- MCN revenue tied to brand deal size, inflated data -> higher perceived value -> higher fees, 刘姐 acknowledged "higher quote" benefit, structural incentive for inflation, screenshot format avoids verification.

### R19: Stakeholder Impact (MP-I)
**answer:** `["A", "B", "C", "D", "F", "H"]` -- 周�� (creator reputation risk), brand (overpaying for actual reach), 小林 (same impact), other creators (trust ecosystem), MCN (legal liability), industry (trust erosion).

### R20: Preference Compliance (P-R)
**answer:** `["A", "B", "C", "E", "F", "G"]` -- all 5 preferences consistently applied.

### R21: Comprehensive Synthesis (MDP-I, exec_check)
**answer:** `["A", "B", "C", "D", "F", "G"]` -- all C resolved (C1 fabricated data, C2 fabricated metric, C3 consistent timeline, C4 contract violated), biases corrected, systematic fraud confirmed across platforms and creators, remediation path clear.

### R22-R30: C3 confirmation, B2 identification, inflation quantification, remediation format, systemic issues, contract violation, recommendations, brand trust, final assessment.
