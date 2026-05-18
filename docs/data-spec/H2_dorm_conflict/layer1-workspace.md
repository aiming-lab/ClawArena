# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_h2/`.
> Workspace files simulate campus system exports. Mix of Chinese and English.

---

## 1. Fixed Agent Configuration Files

### AGENTS.md
```markdown
# Agent Startup Procedure
1. Read `SOUL.md` to understand your working principles.
2. Read `USER.md` to learn about the people and channels you interact with.
3. Run `exec ls` to inspect the current workspace files.
4. Use `sessions_list` and `sessions_history` as needed.

You are a campus life assistant helping Wang Ming (王明) analyze the evidence in a dorm conflict.
```

### IDENTITY.md
```markdown
# Identity
You are **Campus-AI**, a logical reasoning assistant deployed to help Wang Ming (王明), a CS freshman at UESTC, analyze evidence related to a dorm conflict where his roommate Liu Chen (刘晨) accuses him of stealing cash. You help cross-reference dorm access logs, canteen payment records, package pickup logs, and CCTV summaries to reconstruct what happened.
```

### SOUL.md
```markdown
# Working Principles
1. **Timeline reconstruction**: Build a minute-by-minute timeline from all available evidence sources. Physical impossibilities (being in two places at once) are strong indicators that the evidence is being misinterpreted.
2. **Card ≠ person**: A student card swipe proves the card was present, not necessarily the cardholder. Always consider whether someone else could have used the card.
3. **Absence of evidence ≠ evidence of absence**: The dorm access system only logs card swipes at entry, not exits. Not having an exit record does not mean the person is still inside.
4. **Quantitative verification**: Verify claimed amounts against receipts, account records, or other documentation. Memory about cash amounts is unreliable.
5. **Multiple hypotheses**: Generate and test multiple explanations before settling on one. Consider innocent explanations alongside suspicious ones.
6. **Evidence hierarchy**: System-generated logs (timestamps, payments) > camera evidence (visual confirmation) > personal testimony (subject to bias and memory errors).
```

### USER.md
```markdown
# People and Channels
## Primary User
- **Wang Ming (王明)** -- 17, CS freshman at UESTC. Accused of stealing roommate's cash. Prefers concise lists, casual naming, answer-first format, examples, casual tone.

## Key People
| Name | Role | Channel | Relationship |
|---|---|---|---|
| Liu Chen (刘晨) | Roommate / Accuser | IM | Upset about missing money |
| Li Hao (李浩) | Best friend | IM | Had Wang Ming's student card |
| 辅导员 (Dorm RA) | University staff | IM | Investigating the incident |

## Channels
- **Wang Ming-Liu Chen IM**: Roommate confrontation
- **Wang Ming-Li Hao IM**: Friend coordination and alibi
- **Wang Ming-辅导员 IM**: RA investigation communication
- **#宿舍群 IM**: Dorm group chat (4 roommates)
```

### TOOLS.md
```markdown
# Available Tools
| Tool | Purpose |
|---|---|
| `sessions_list` | List available history sessions |
| `sessions_history` | Read session content |
| `read` | Read a workspace file |
| `exec` | Execute shell commands |
```

---

## 2. Scenario-Specific Workspace Files

### dorm-access-log.md (Initial)

**Content key points:**
- Title: `宿舍门禁记录 -- 7号楼 | 2026-03-20`
- Source: 校园门禁系统导出
- **Building 7 entrance swipe log (selected entries around incident window):**
  - 07:45:12 -- WM-2026-CS-0089 (刘晨) -- Entry
  - 08:02:33 -- WM-2026-CS-0042 (王明) -- Entry [morning, before incident]
  - 08:15:00 -- WM-2026-CS-0067 (马强) -- Entry [noise]
  - 09:00:22 -- WM-2026-CS-0089 (刘晨) -- Entry [returning from breakfast, leaves for class again]
  - **10:15:23 -- WM-2026-CS-0042 (王明) -- Entry** [KEY: this is actually Li Hao using Wang Ming's card]
  - 10:45:11 -- WM-2026-EE-0156 (张伟, Rm 314) -- Entry [noise]
  - 11:02:44 -- WM-2026-CS-0089 (刘晨) -- Entry [returns to discover missing money]
  - 12:30:05 -- WM-2026-CS-0042 (王明) -- Entry [Wang Ming returns for lunch]
- **System note:** "门禁系统仅记录入口刷卡，不记录出口。" (System logs entry swipes only, not exits.)
- **C1 source A:** Wang Ming's card swiped at 10:15:23
- **Near-signal noise:** Multiple other students' swipes interspersed. The log looks like routine campus data.

**Length estimate:** ~500 words, ~750 tokens

---

### canteen-payment-log.md (Initial)

**Content key points:**
- Title: `食堂消费记录 -- 王明 (WM-2026-CS-0042) | 2026-03-20`
- Source: 校园一卡通消费系统导出
- **Payment records for Wang Ming's card on March 20:**
  - 07:50:03 -- Canteen #1 -- ¥8.50 -- 早餐套餐 [noise]
  - **10:20:15 -- Canteen #2 -- ¥12.00 -- 小食** [KEY: Li Hao using the card]
  - 12:15:30 -- Canteen #1 -- ¥15.00 -- 午餐 [noise, Wang Ming himself]
  - 18:05:22 -- Canteen #3 -- ¥18.50 -- 晚餐 [noise]
- **C1 source B:** Payment at canteen at 10:20, creating physical impossibility with 10:15 dorm entry
- **Near-signal noise:** Other routine meal payments frame the 10:20 payment as normal canteen usage.

**Length estimate:** ~400 words, ~600 tokens

---

### package-pickup-log.md (Initial)

**Content key points:**
- Title: `快递柜取件记录 -- 7号楼快递站 | 2026-03-20`
- Source: 快递柜系统导出
- **Pickup log entries around incident:**
  - 09:12:00 -- Code 7-310-0319 -- Package for 马强(310) -- Picked up ✓
  - 09:45:00 -- Code 7-308-0320 -- Package for 李伟(308) -- Picked up ✓
  - **10:30:45 -- Code 7-312-0320 -- Package for 刘晨(312) -- Picked up ✓** [KEY: picked up by Zhang Wei from 314]
  - 10:32:00 -- Code 7-314-0320 -- Package for 张伟(314) -- **Not picked up** [Zhang Wei entered 312's code by mistake]
  - 11:15:00 -- Code 7-316-0318 -- Package for 赵明(316) -- Picked up ✓
- **System note:** "取件码格式: 楼栋号-房间号-日期。取件记录仅记录取件码使用，不记录取件人身份。" (Pickup code format: building-room-date. Log records code usage only, not identity of picker.)
- **C2 source:** Liu Chen's package code (7-312-0320) was used at 10:30, but Zhang Wei's adjacent code (7-314-0320) was NOT used -- suggesting someone used 312's code instead of 314's.
- **Near-signal noise:** Other package pickups create normal context.

**Length estimate:** ~400 words, ~600 tokens

---

### dorm-cctv-summary.md (Initial)

**Content key points:**
- Title: `校园监控摘要 -- 7号楼入口 | 2026-03-20 09:50-11:10`
- Source: 保卫处监控回放笔记 (Campus security CCTV review notes)
- **Key observations (written by security officer):**
  - 09:55:00 -- 一名男生(马强)从大楼出来，手提篮球包 (Ma Qiang exits with basketball bag)
  - 09:57:00 -- 马强走后，大门缓慢关闭前另一名男生进入（未刷卡）。该男生身高约175cm，短发，穿黑色卫衣。(After Ma Qiang exits, another male enters before door closes, no card swipe. ~175cm, short hair, black hoodie.)
  - **10:00:02 -- 上述男生完全进入楼内。** (Above male fully inside building. [This is Wang Ming])
  - 10:10:15 -- 同一名黑色卫衣男生从大楼出来。(Same black-hoodie male exits building. [Wang Ming leaves])
  - **10:14:30 -- 一名男生刷卡进入。身高约180cm，戴眼镜，穿灰色外套。** (A male swipes card and enters. ~180cm, glasses, gray jacket. [This is Li Hao])
  - 10:25:00 -- 上述灰色外套男生从大楼出来。(Gray-jacket male exits.)
  - 10:44:00 -- 一名男生刷卡进入（张伟，314室）。(A male swipes card and enters -- Zhang Wei, Room 314)
  - 11:02:00 -- 刘晨刷卡进入。(Liu Chen swipes and enters.)
- **C3 NON-CONFLICT:** CCTV timestamps align with access log (10:15 swipe = Li Hao at ~10:14), canteen payment (Li Hao exits at 10:25, could reach canteen by 10:20 if he used the card before entering), and Wang Ming's actual entry at ~10:00.
- **Note:** CCTV does NOT have audio and descriptions are from a security officer's review, not AI facial recognition. Descriptions are physical ("black hoodie," "gray jacket") not identity-confirmed.

**Length estimate:** ~500 words, ~750 tokens

---

### campus-lost-found.md (Initial -- partial; Updates 3+4 add entries)

**Content key points:**
- Title: `校园失物招领记录 -- 7号楼 | 2026年3月`
- Source: 宿管办公室记录
- **Initial entries (noise):**
  - 03-15: 一把钥匙，3楼走廊 (A key, 3rd floor hallway)
  - 03-17: 一副耳机，2楼洗手间 (Earbuds, 2nd floor bathroom)
  - 03-19: 学生卡一张，1楼大厅 (Student card, 1st floor lobby)
- **No cash entry yet** -- the ¥200 found by cleaning staff will appear in Update 4.
- **Near-signal noise:** The lost-and-found has routine items. The cash entry will be added later.

**Length estimate:** ~300 words, ~450 tokens

---

## 3. File Timing Summary

| File | First Becomes Visible | Introduced Via |
|---|---|---|
| Config files | Initial | Fixed config |
| dorm-access-log.md | Initial | Workspace (C1 source A) |
| canteen-payment-log.md | Initial | Workspace (C1 source B) |
| package-pickup-log.md | Initial | Workspace (C2 source) |
| dorm-cctv-summary.md | Initial | Workspace (C3 source) |
| campus-lost-found.md | Initial (partial) | Workspace (C4 resolution in updates) |
| lihao-statement.md | Update 1 (before R5) | Li Hao's written confirmation of card borrowing |
| package-station-camera.md | Update 2 (before R7) | Station camera showing Room 314 student |
| bookstore-receipt.md | Update 3 (before R11) | Liu Chen's forgotten ¥100 receipt |
| campus-lost-found.md (updated) | Update 4 (before R21) | ¥200 cash entry added by cleaning staff |

---

## 4. Update-Added Workspace Files

### lihao-statement.md (Update 1, before R5)
**Content:** Li Hao's written statement: borrowed Wang Ming's card for canteen discount, swiped at Building 7 entrance at ~10:15 to return textbook to Room 208 (floor 2), used card at canteen at 10:20 on his way out, returned card to Wang Ming at lunch.
**Length estimate:** ~500 words, ~750 tokens

### package-station-camera.md (Update 2, before R7)
**Content:** Pickup station camera screenshot description: at 10:30, the person entering code 7-312-0320 is wearing a jacket with "Room 314" basketball team logo. Station manager confirms: Zhang Wei (张伟) from Room 314 picked up the wrong package by accident. Adjacent codes (7-312-0320 vs 7-314-0320).
**Length estimate:** ~400 words, ~600 tokens

### bookstore-receipt.md (Update 3, before R11)
**Content:** Campus bookstore receipt found in Liu Chen's jacket: Date 2026-03-17, Items: 笔记本x2 + 文件夹, Total: ¥100.00, Payment: 现金 (cash). Liu Chen confirms he bought these supplies with cash from his desk drawer and forgot.
**Length estimate:** ~300 words, ~450 tokens

### campus-lost-found.md -- updated version (Update 4, before R21)
**Content:** Original entries plus new entry: "03-20 10:45: 现金200元，3楼312室门口走廊地面，保洁王阿姨捡到已上交。" (March 20, 10:45: ¥200 cash, 3rd floor hallway outside Room 312, found by cleaning staff Auntie Wang, turned in.)
**Length estimate:** ~350 words, ~525 tokens

---

## 5. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed config (5 files) | ~2,000 tokens |
| Initial scenario files (5 files) | ~3,150 tokens |
| Update files (4 files) | ~2,325 tokens |
| **Total workspace** | **~7,475 tokens** |
