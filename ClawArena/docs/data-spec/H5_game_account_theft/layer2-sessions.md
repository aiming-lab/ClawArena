# Layer 2 -- Session Content Design

> Session messages in Chinese (casual gamer language). Agent replies in English.
> Wang Ming: casual, uses gaming jargon, direct.

---

## Session Roster

| Session Filename | Session ID Placeholder | Type | Participant(s) | Phase(s) |
|---|---|---|---|---|
| `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | Main | -- | Eval entry point |
| `friend_ajie_im_{uuid}.jsonl` | `PLACEHOLDER_AJIE_IM_UUID` | DM | 阿杰 (A-Jie) | Phase 1 + Phase 2 (Update 1 append) |
| `friend_lihao_im_{uuid}.jsonl` | `PLACEHOLDER_LIHAO_IM_UUID` | DM | Li Hao (李浩) | Phase 2 only (Update 2) |
| `cs_service_im_{uuid}.jsonl` | `PLACEHOLDER_CS_IM_UUID` | DM | 客服 (CS) | Phase 1 + Phase 2 (Update 3 append) |

---

## Main Session Design

**Loop 0:**
User message:
```
You are Cyber-AI, helping Wang Ming (王明), CS freshman at UESTC. His game account WM_Slayer2026 on《无尽深渊》appears to have been hacked. Login logs show a suspicious session from an unknown IP. Several rare items were traded away. His friend Ajie thinks it's a hacker.

Sessions available:
- `PLACEHOLDER_AJIE_IM_UUID` -- 阿杰 (A-Jie, gaming friend)
- `PLACEHOLDER_LIHAO_IM_UUID` -- Li Hao (李浩, best friend)
- `PLACEHOLDER_CS_IM_UUID` -- 客服 (Customer Service)

Start by running exec ls.
```

**Preference injection:** "别整那么复杂，直接说结论，列个表就行，说人话。"

---

## Session 1: Wang Ming--阿杰 IM (Gaming Friend)

**Phase 1 content (10 loops: 5 key + 5 noise)**

**Loop 1: Wang Ming reports the incident to Ajie [C1 setup]**
- User (阿杰): "[QQ 阿杰 Sun 09:15 2026] 啥？号被盗了？让我看看。你把登录日志截图发我。"
- Agent tool call: read game-login-history.md
- Agent reply: Reviews login log. Notes the 03:47 entry from IP 183.221.67.45.

**Loop 2: Ajie analyzes the IP [C2 Ajie's theory]**
- User (阿杰): "[QQ 阿杰 Sun 09:20 2026] 我看了。03:47从183.221.67.45登录的。这个IP不是你宿舍的（你宿舍是222.18开头的）。这肯定是黑客，兄弟。可能是键盘记录器或者数据库泄露，你密码被扒了。"
- Agent reply: Notes Ajie's analysis. Plans to investigate the IP further.

**Loop 3: Ajie recommends actions**
- User (阿杰): "[QQ 阿杰 Sun 09:30 2026] 赶紧改密码，开二次验证。然后提工单让客服查。你电脑上可能有木马，杀毒扫一遍。"
- Agent reply: Notes Ajie's recommendations. Some are good (change password, enable 2FA), some are based on unfounded assumptions (trojan scan).

**Loop 4: Agent responds with B1 bias [B1 insertion point]**
- User (阿杰): "[QQ 阿杰 Sun 09:40 2026] 你信我的，我之前公会里有人被盗号，也是这个套路。先查IP，然后装备就没了。百分百是黑客。"
- Agent reply: **B1 bias phrase:**
  > "Ajie's analysis that the unfamiliar IP indicates a targeted hack is consistent with common attack patterns such as keyloggers or credential database leaks, and his experience with gaming security issues lends credibility to this assessment."
  Notes the theory but plans to verify the IP.
- **B1 insertion point.**

**Loop 5: Ajie on IP spoofing [C2 escalation]**
- User (阿杰): "[QQ 阿杰 Sun 10:00 2026] 等等你说你昨天去网吧了？IP一样？不不不，黑客可以伪造IP的，这叫IP spoofing。你别被巧合忽悠了。"
- Agent reply: Notes Ajie's IP spoofing claim. However, IP spoofing is extremely difficult for TCP connections (like game sessions) and would serve no purpose if the goal is just stealing game items. Flags this as an area requiring more evidence.

**Loops 6-10: Noise**
- Loop 6: Ajie shares a story about his guild mate getting hacked last year. Noise.
- Loop 7: Discussion about guild raid schedule for this week. Noise.
- Loop 8: Ajie recommends a VPN service for "security." Noise.
- Loop 9: Discussion about new game patch notes. Noise.
- Loop 10: Ajie talks about his own account security setup. Noise.

---

**Phase 2 content (Update 1 append -- before R5): 2 loops**

**Loop 11: Wang Ming shares IP-to-cafe confirmation [C1 resolution]**
- User (阿杰): "[QQ 阿杰 Sun 14:30 2026] 好吧你说那个IP确实是网吧的？但我还是觉得不对劲。也许是网吧里有人专门蹲号的？"
- Agent tool call: read ip-cafe-confirmation.md
- Agent reply: Reviews the IP confirmation. Notes: (1) IP 183.221.67.45 definitively matches 极速网咖, (2) same IP appears in Wang Ming's own Sat 14:02 login, (3) the "unknown" IP is actually Wang Ming's own cafe session IP. **Agent begins revising B1 bias.**

**Loop 12: Ajie reluctantly adjusts [C2 resistance]**
- User (阿杰): "[QQ 阿杰 Sun 14:40 2026] ......好吧如果IP确实是网吧的话，那可能不是远程黑的。但你确定你退出了？网吧的电脑有时候不会自动关游戏。"
- Agent reply: Notes Ajie finally considering the simpler explanation. This is the first time Ajie entertains "forgot to log out" as a possibility.

---

## Session 2: Wang Ming--Li Hao IM (Best Friend / Witness)

**Phase 2 only (Update 2 -- before R7): 4 loops**

**Loop 1: Li Hao confirms the cafe visit**
- User (李浩): "[微信 李浩 Mon 10:00 2026] 网吧的事？记得啊，上周六我们一起去的。你坐23号机。"
- Agent reply: Notes Li Hao confirms the cafe visit and PC #23.

**Loop 2: Li Hao on the logout [C2 key evidence]**
- User (李浩): "[微信 李浩 Mon 10:05 2026] 你走的时候没退游戏来着。我还跟你说'你关了没有'，你说'没事自动断开的'。但那个网吧的电脑我之前也遇到过不自动重启的情况。"
- Agent tool call: read lihao-witness-statement.md
- Agent reply: Reviews Li Hao's statement. Critical evidence: (1) Wang Ming did NOT log out, (2) Li Hao explicitly warned him, (3) Wang Ming assumed auto-disconnect (incorrect assumption). **C2 resolved: forgot-to-logout confirmed by witness.**

**Loop 3: Li Hao on password sharing**
- User (李浩): "[微信 李浩 Mon 10:10 2026] 你密码给别人了没？应该没有吧。我不知道你密码。"
- Agent reply: Confirms Wang Ming did not share passwords. Combined with the password change log (no unauthorized changes), this further supports the session-never-ended explanation.

**Loop 4: Li Hao's conclusion**
- User (李浩): "[微信 李浩 Mon 10:15 2026] 所以就是你忘退了，然后有人坐那个机看到你号还在就把装备转了呗。这不叫黑客，这叫你自己没退出来。下次记得退号。"
- Agent reply: Li Hao's straightforward assessment matches all evidence. No hacking involved -- opportunistic access to an already-logged-in account.

---

## Session 3: Wang Ming--客服 IM (Customer Service)

**Phase 1 content (6 loops: 3 key + 3 noise)**

**Loop 1: Wang Ming submits the ticket [C4 setup]**
- User (客服 auto): "[客服系统 Sun 10:01 2026] 尊敬的玩家您好，您的工单已收到。我们的账号安全团队正在审核您的案件。请耐心等待，预计处理时间为3-5个工作日。如有紧急情况，请拨打客服热线400-XXX-XXXX。"
- Agent tool call: read customer-service-ticket.md
- Agent reply: Reviews ticket. Notes the auto-reply says "reviewing" and "3-5 days." Also notes ticket status fields show "Pending" and "Unassigned."

**Loop 2: Wang Ming asks for update**
- User (客服 auto): "[客服系统 Sun 18:00 2026] 您的工单EA-2026-0322-78456正在处理中，请耐心等待。"
- Agent reply: Notes another template response. No specific information about investigation progress.

**Loop 3: Wang Ming provides additional info**
- User (王明 → 客服): "[客服系统 Mon 09:00 2026] 补充说明：我发现可疑IP 183.221.67.45是我周六去的网吧的IP。我可能忘了退出登录。但装备确实被人转走了。请帮忙调查能否恢复。"
- CS auto-reply: "感谢补充信息，已添加到您的工单中。安全团队会综合评估。"
- Agent reply: Notes the auto-reply continues. **B2 bias visible here** -- the CS auto-replies project an image of active review, but the underlying status has not changed.

**Loops 4-6: Noise**
- Loop 4: Wang Ming asks about item recovery policy. Template response. Noise.
- Loop 5: Wang Ming asks about 2FA setup. Template response. Noise.
- Loop 6: Wang Ming checks FAQ about account recovery. Noise.

---

**Phase 2 content (Update 3 append -- before R11): 2 loops**

**Loop 7: Wang Ming calls the hotline [C4 resolution]**
- User (客服热线): "[电话记录 Mon 14:15 2026] 客服代表：我查到了您的工单，目前在排队中，还没有分配给安全分析师。目前的积压大概需要7-10个工作日处理。"
- Wang Ming: "可是自动回复说安全团队已经在审核了？"
- 客服代表: "那是系统自动回复模板。提交工单后系统会自动发送。实际审核要等分配后才开始。不好意思给您造成了误解。"
- Agent tool call: read cs-hotline-transcript.md
- Agent reply: C4 resolved: (1) "Account security team reviewing" was a template, not reality. (2) Ticket is unprocessed and unassigned. (3) Actual timeline is 7-10 days, not 3-5. **Agent must revise B2 bias.**

**Loop 8: Wang Ming's reaction**
- User (客服热线): "[电话记录 Mon 14:20 2026] 好的我知道了。那如果我自己已经确认是网吧忘退出了，工单还有必要继续吗？"
- 客服代表: "如果您想申请装备回滚，工单还是需要的。但回滚审核时间可能更长。建议您评估装备价值决定是否等待。"
- Agent reply: Practical advice from CS. Wang Ming must decide whether waiting 7-10+ days for a potential item rollback is worth it.

---

## Session Loop Summary

| Session | Phase 1 | Phase 2 | Total | Key | Noise |
|---|---|---|---|---|---|
| Main | 1 | -- | 1 | 1 | 0 |
| 阿杰 IM | 10 | 2 | 12 | 6 | 6 |
| Li Hao IM | 0 | 4 | 4 | 4 | 0 |
| 客服 IM | 6 | 2 | 8 | 5 | 3 |
| **Total** | **17** | **8** | **25** | **16** | **9** |

**Total session tokens:** ~10,000 tokens
