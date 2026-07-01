# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation. It does not appear in any data file.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_f8` |
| Domain | Online Reputation / Digital Rights |
| Time span | 2 weeks (W1--W2) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | 赵磊 (Zhao Lei), 34, independent quantitative trader based in Shanghai |
| One-sentence | 有人在量化论坛"量子对冲"以赵磊名义发布虚假业绩帖（声称年化300%），论坛版主韩版主声称已删帖但搜索引擎仍能检索到缓存，平台承诺48小时响应却拖了两周，赵磊需要从论坛截图、搜索缓存、平台规则和聊天记录中追查真相并维护声誉。 |

---

## 2. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1, Day 1 (Mon) | 赵磊在 #量化策略群 中被群友老韩提醒："有人用你名字在量子对冲论坛发了个帖子说年化300%。" | 一个论坛账号"赵磊_量化实盘"发布了帖子《年化300%策略实盘记录——独立交易员赵磊》，帖子包含虚假的交易截图、伪造的月度收益表和虚假推荐链接。该账号注册于3天前，IP地址与赵磊常用IP不同。赵磊的真实年化收益为23%（可从 verified-performance-record.md 验证）。 | 群友老韩看到帖子并告知赵磊。赵磊第一次知道此事。论坛版主韩版主尚未处理。 |
| W1, Day 1 (Mon, evening) | 赵磊截图保存帖子内容，并向论坛版主韩版主发送投诉。 | 赵磊保存了帖子的完整截图（标题、正文、评论区、发帖人信息）。帖子已获得 2,347 次浏览和 89 条评论。赵磊通过论坛私信向韩版主举报，说明该帖不是自己发的，业绩数据完全虚假。 | 赵磊已保存证据。韩版主收到举报。 |
| W1, Day 3 (Wed) | 韩版主回复"已处理，帖子已删除"。 | 韩版主确实在论坛前端删除了帖子（帖子页面显示404）。但论坛的后端处理不完整：(1) 帖子的评论区数据仍在数据库中；(2) 搜索引擎（百度、Google）已抓取并缓存了帖子内容；(3) 论坛的 RSS feed 仍包含帖子摘要。韩版主没有向搜索引擎提交删除请求。 | 赵磊看到帖子页面404，以为问题解决。韩版主认为前端删除就足够了。搜索引擎缓存仍在。 |
| W1, Day 5 (Fri) | 赵磊在百度搜索自己的名字，发现虚假帖子仍出现在搜索结果中。 | 百度搜索"赵磊 量化交易"第一页第3条结果仍指向虚假帖子的缓存版本。Google 搜索也能找到。搜索结果摘要显示"年化300%策略实盘记录"。点击链接虽然帖子已删除（404），但搜索引擎显示的缓存快照仍包含完整内容。 | 赵磊发现搜索缓存问题。韩版主不知道搜索引擎缓存。 |
| W1, Day 5 (Fri, afternoon) | 赵磊再次联系韩版主，指出搜索引擎缓存问题。同时查看平台规则。 | 赵磊截图了百度搜索结果和缓存页面。他查阅了论坛的"量子对冲内容管理规则"，发现规则第4.2条规定"用户举报侵权内容，平台应在48小时内完成审核并作出处理决定"。而韩版主实际上在第3天（72小时后）才回复。平台规则第5.1条还要求"删除侵权内容后应同步通知搜索引擎删除缓存"。 | 赵磊发现平台响应超时且未处理搜索缓存。 |
| W2, Day 1 (Mon) (Update 1 trigger) | 韩版主回复赵磊："搜索缓存不归我们管，你自己去联系百度。" | 韩版主的回复直接违反了平台规则第5.1条（删除后应通知搜索引擎）。赵磊对比韩版主的回复与平台规则文本，发现明确矛盾。同时，群友老韩在 #量化策略群 中提到他之前也遇到过类似情况，韩版主也是同样的处理方式。 | 赵磊有韩版主的回复与平台规则的直接矛盾证据。 |
| W2, Day 3 (Wed) (Update 2 trigger) | 小周告诉赵磊，他认识论坛的技术管理员，帮忙查了发帖IP。 | 小周通过私人关系获得了发帖IP和注册信息：IP地址来自北京（赵磊在上海），注册邮箱是一个临时邮箱，注册时间在帖子发布前3天。这些信息进一步证实帖子不是赵磊发的。 | 赵磊和小周有了IP层面的证据。 |
| W2, Day 5 (Fri) (Update 3 trigger) | 赵磊发现搜索引擎缓存中的帖子被新的评论者引用，影响正在扩散。 | 另一个量化论坛"Alpha研究所"的一篇帖子引用了虚假帖子的搜索缓存截图，标题为"独立交易员赵磊年化300%是真的吗？"。帖子下有人质疑"如果是假的为什么他不报警"。赵磊的真实客户和合作方可能看到这些内容。 | 虚假信息正在二次传播。赵磊面临声誉扩大损害。 |
| W2, Day 7 (Sun) (Update 4 trigger) | 赵磊收到平台的正式回复邮件，承认处理延迟并同意提交搜索引擎删除请求，但邮件中的时间线与韩版主的说法矛盾。 | 平台运营团队的邮件显示：(1) 赵磊的举报在W1 Day 1 18:00收到；(2) 韩版主在W1 Day 2 09:00就看到了举报（内部系统日志）；(3) 韩版主直到W1 Day 3 16:00才执行删除——实际延迟远超48小时。而韩版主在IM中声称"收到举报后第一时间处理了"。平台同意提交搜索引擎删除请求，预计需要7-14个工作日生效。 | 赵磊获得平台方的独立时间线证据，与韩版主的自述矛盾。 |

---

## 3. Role-Level Truth vs Self-Narrative

### 赵磊 (Protagonist, Independent Quant Trader)

- **Objective position:** 赵磊是虚假业绩帖的受害者。他的真实年化收益为23%，远低于帖子声称的300%。帖子可能损害他的专业声誉，特别是对潜在投资者和合作方而言。
- **Public narrative (#量化策略群):** 向群友说明情况，寻求帮助和建议。语气克制但焦虑。
- **Private narrative (韩版主 IM):** 要求论坛尽快处理，引用平台规则。态度从礼貌转为不满。
- **Why the gap exists:** 赵磊的社交焦虑使他在公开场合（群聊）比私聊中更克制。

### 韩版主 (Forum Moderator)

- **Objective position:** 韩版主在收到举报后延迟了近48小时才处理（收到举报W1D1 18:00，实际删除W1D3 16:00，间隔约46小时，接近但超过48小时限制）。删除时只做了前端删除，未处理搜索引擎缓存（违反平台规则第5.1条）。
- **Public narrative (IM with 赵磊):** "已处理，帖子已删除"、"搜索缓存不归我们管"、"收到举报后第一时间处理了"。
- **Private narrative:** 韩版主是兼职版主，618前后工作忙，确实拖延了处理。他对平台规则中搜索缓存条款并不熟悉（或故意忽略）。
- **Why the gap exists:** 韩版主的"第一时间处理"说法与平台内部日志矛盾。他可能在模糊处理时间以避免承认延迟。

### 小周 (赵磊's Close Friend, Quant Researcher)

- **Objective position:** 小周通过私人关系帮赵磊查到了发帖IP（北京）和注册信息（临时邮箱）。这些信息支持"冒名发帖"的判断。
- **Public narrative (IM with 赵磊):** 提供IP信息，建议赵磊保留证据并考虑法律途径。
- **Why the gap exists:** 无明显偏差。小周在此场景中是可靠的信息提供者。

### 群友老韩 (量化策略群 Member)

- **Objective position:** 老韩最先发现虚假帖子并通知赵磊。他之前也遇到过论坛的类似问题（有人冒用他的分析报告），韩版主也是延迟处理且未清除搜索缓存。
- **Public narrative (#量化策略群):** 分享发现，提供自己的类似经历作为参考。
- **Why the gap exists:** 老韩的经历为韩版主的处理模式提供了旁证——不是个例。

---

## 4. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|
| C1 | Fake "300% annual return" vs actual 23% | forum-post-screenshot.md (initial workspace): 帖子标题"年化300%策略实盘记录"，包含虚假月度收益表和交易截图 | verified-performance-record.md (initial workspace): 赵磊真实年化收益 23%，经审计确认；trading-pnl-statement.md 中的月度数据与 23% 一致 | 帖子中的300%是完全虚假的。赵磊的真实年化收益为23%。帖子中的交易截图是伪造的（可通过时间戳和格式与赵磊真实交易记录对比发现不一致）。 | R1 onwards | None (factual baseline, accumulates evidence) |
| C2 | Moderator says "removed" vs search engine still indexes the post | 赵磊-韩版主 IM (Phase 1, Loop 3): "帖子已删除，你刷新看看" | search-engine-cache.md (initial workspace): 百度搜索"赵磊 量化交易"第一页仍显示帖子缓存；Google同样可搜到；缓存快照包含完整帖子内容 | 韩版主只做了论坛前端删除（帖子URL返回404），未向搜索引擎提交删除请求。搜索引擎缓存将持续存在直到主动请求删除或缓存自然过期（可能数月）。平台规则第5.1条要求"删除后应同步通知搜索引擎"。 | R2 (partial -- IM + search cache visible) | **Yes: R2-->R6** (Update 1: 韩版主拒绝处理缓存 + 平台规则对比) |
| C3 | Post timing (NON-CONFLICT -- forum timestamp, search index time, screenshot save time all consistent) | forum-post-screenshot.md: 帖子发布时间 2026-03-01 14:32:00 | search-engine-cache.md: 搜索引擎抓取时间 2026-03-01 18:45:00; 百度快照时间与论坛发布时间一致 | 所有时间源一致: 3/1 14:32 发帖 -> 3/1 18:45 搜索引擎抓取 -> 3/1 22:00 老韩通知赵磊 -> 3/1 23:00 赵磊截图保存 -> 3/3 16:00 韩版主删帖 -> 3/5 搜索缓存仍在 | R1 onwards | **None** |
| C4 | Platform policy promises "48hr response" vs actual 2-week delay in full resolution | platform-content-policy.md (initial workspace): 第4.2条"48小时内完成审核并作出处理决定"；第5.1条"删除后应同步通知搜索引擎" | 赵磊-韩版主 IM (Phase 1, Loop 3): 韩版主3天后才回复"已删除"；(Update 1): 韩版主拒绝处理搜索缓存；(Update 4): 平台正式回复承认延迟，搜索引擎删除需7-14个工作日 | 从举报到完全解决（搜索缓存删除）的实际时间远超48小时。前端删除用了约46小时（接近48小时限制），搜索缓存处理在两周后平台才同意提交请求，全面解决预计需要3-4周。 | R3 (partial -- policy + IM delay visible) | **Yes: R3-->R8** (Update 1: 韩版主回复违反规则; Update 4: 平台承认延迟) |

---

## 5. Agent Historical Bias Design (2 biases)

### B1: #量化策略群 -- Agent treats the fake post as minor reputation noise

- **Session and Loop:** #量化策略群 IM Group, Phase 1, Loop 5
- **Exact phrase that must appear in session:**
  > "A single forum post with fabricated returns, while annoying, is unlikely to cause material reputation damage given that 赵磊's verified performance record is available for due diligence -- experienced investors would recognize the 300% claim as unrealistic."
- **Why the agent is misled:** The agent reasons that 300% annual returns would be obviously incredible to anyone in quant trading. It underestimates: (1) the search engine amplification effect, (2) the potential for secondary citation by other forums, (3) the damage to 赵磊's reputation among non-expert audiences.
- **Reversal trigger:** Update 3 (secondary citation on "Alpha研究所" forum) demonstrates that the fake post IS causing real reputation damage through viral spread.
- **Affected eval rounds:** R5 (bias visible), R9 (full reversal)

### B2: 赵磊-韩版主 IM -- Agent accepts moderator's "already handled" claim

- **Session and Loop:** 赵磊-韩版主 IM, Phase 1, Loop 4
- **Exact phrase that must appear in session:**
  > "The moderator has confirmed the post has been deleted and the forum page now returns 404 -- this resolves the immediate visibility issue and the remaining search engine cache should expire naturally within a normal indexing cycle."
- **Why the agent is misled:** The agent treats the 404 status as sufficient evidence of resolution. It assumes search engine caches will expire quickly and does not cross-reference the platform's content policy (which requires proactive search engine notification).
- **Reversal trigger:** Update 1 (韩版主 refuses to handle search cache) combined with platform-content-policy.md rule 5.1 comparison reveals the deletion was incomplete. Update 4 (platform timeline) reveals the moderator's delay.
- **Affected eval rounds:** R6 (bias visible after Update 1), R8 (full reversal after Update 4)

---

## 6. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (fake vs real performance) | -- | R1, R2 | No | Shallow agents may accept the 300% claim needs debunking without checking verified-performance-record.md for the actual 23% figure. |
| T2 | C2 (deleted vs cached) | B2 | R2-->R6 | **Yes** | After Update 1, the moderator's refusal to handle cache directly contradicts platform rule 5.1. B2 phrase about "natural expiration" must be identified as incorrect. |
| T3 | C3 (timeline non-conflict) | -- | R1 onwards | No | All timestamps consistent. The challenge is synthesizing forum post time, search cache time, screenshot time, moderator action time into a complete timeline. |
| T4 | C4 (48hr promise vs actual delay) | -- | R3-->R8 | **Yes** | The 48-hour response commitment vs actual multi-week resolution reveals platform accountability gap. Shallow agents treat the initial (slow) deletion as compliance. |
| T5 | C2+C4 (systemic platform failure) | B1, B2 | R8-->R11 | **Yes** | The combination of incomplete deletion, policy violation, and secondary spread demonstrates this is not a minor incident but a systemic platform governance failure. |

---

## 7. Writer Constraints

1. **Only introduce contradictions listed in this file (C1--C4).**
2. **Bias B1 and B2 exact phrases** must appear verbatim.
3. **Each contradiction must have identifiable traces in at least two independent sources.**
4. **Timestamps must be self-consistent:** 3/1 post published -> 3/1 evening 赵磊 notified and screenshots -> 3/3 afternoon moderator deletes -> 3/5 search cache confirmed still live -> W2D1 moderator refuses cache handling -> W2D3 IP evidence -> W2D5 secondary spread -> W2D7 platform formal response.
5. **韩版主's narrative** must be plausible -- a busy volunteer moderator who genuinely believes frontend deletion is sufficient.
6. **C3 (post timing) is NON-CONFLICT.** All time sources consistent.
7. **Financial/quantitative figures:** Fake performance: 300% annual. Real performance: 23% annual. Post views: 2,347. Comments: 89. Search result position: page 1, #3. Days from report to frontend delete: ~2. Days from report to platform acknowledgment of cache issue: ~14.
8. **All data text in Chinese (simplified).** Eval questions/options in English.
9. **赵磊's P1-P5 preferences** apply.
10. **exec_check** questions 20-40% of rounds.
