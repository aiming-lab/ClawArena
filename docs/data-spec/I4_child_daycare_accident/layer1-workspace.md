# Layer 1 -- Workspace File Spec

> Workspace under `benchmark/data/calmb-new/workspaces/trace_i4/`.

---

## 1. Fixed Agent Config Files

Standard 5-file config. IDENTITY.md: child safety investigation assistant for Lin Yi. SOUL.md: emphasizes wound-mechanism analysis, cross-source verification, timeline reconstruction, child witness considerations, medical forensic reasoning. USER.md: Lin Yi (protagonist), 林伟 (husband), 赵老师 (teacher), 刘妈妈 (other parent), 母亲 (Lin Yi's mother).

---

## 2. Scenario-Specific Workspace Files

### kindergarten-incident-report.md (Initial)
- Title: "阳光幼儿园事故报告 -- 乐乐 | 2026-03-25"
- Reports: "乐乐在户外活动时从滑梯上摔落，额头磕伤"
- Teacher: "赵老师当时在旁边看护，立即进行了急救处理"
- First aid: cold compress + bandage, parent called at 10:30
- Recommendation: "建议送医检查"
- **C1 source:** "从滑梯摔落" (slide fall claim)
- **C2 source:** "赵老师当时在旁边看护" (teacher was watching claim)

**Length:** ~500 words, ~750 tokens

### cctv-footage-description.md (Initial -- placeholder)
- Title: "幼儿园监控说明 -- 2026-03-25"
- Content: "监控录像正在调取中，需要时间准备。" (Footage being prepared, need time.)
- _(Update 3 will replace with actual footage description)_
- **Near-signal noise:** The initial placeholder stalling is itself suspicious.

**Length:** ~100 words, ~150 tokens

### medical-examination-report.md (Initial)
- Title: "就诊记录 -- 乐乐 | 社区诊所 2026-03-25 11:00"
- Findings: "右额部2cm裂伤，创缘整齐，深达皮下组织。局部消毒清创后缝合3针。" (Right forehead 2cm laceration, clean wound edges, depth to subcutaneous tissue. 3 stitches after debridement.)
- Vital signs: normal
- **NOT noted in clinic report but observed by Lin Yi later:** No friction abrasion marks (expected from slide surface), linear wound edges consistent with metal edge impact, contusion pattern suggests single-point impact
- **C1 source (medical):** Wound description inconsistent with slide fall
- **C3 source:** Timeline 11:00 examination is consistent with 10:15 incident + 10:30 parent call

**Length:** ~400 words, ~600 tokens

### parent-group-chat-export.md (Initial)
- Title: "家长群聊天导出 -- 小小一班家长群 | 2026-03-25"
- Key message from 刘妈妈 at 17:00: "林怡妈妈，我家豆豆回来说今天乐乐被小明推了，从攀爬架上摔下来的。不是滑梯。你家乐乐没事吧？"
- Kindergarten response in group (园长): "感谢家长关心。根据老师的观察，乐乐是从滑梯上不慎摔落的。小朋友们的记忆可能不准确。"
- Other parents express concern
- **C4 source:** Child witness testimony (via parent) vs kindergarten denial
- **Near-signal noise:** Other parent group messages about daily logistics, food menus, pickup times

**Length:** ~600 words, ~900 tokens

### kindergarten-safety-policy.md (Initial)
- Title: "阳光幼儿园安全管理制度"
- Key rules: outdoor play must have minimum 2 teachers supervising per class; teachers must not use personal phones during supervision; incident reports must be based on direct observation
- **Supporting evidence:** Teacher Zhao violated phone policy. Only 1 teacher was present (assistant on sick leave). Incident report was not based on direct observation.

**Length:** ~500 words, ~750 tokens

---

## 3. File Timing Summary

| File | First Visible | Via |
|---|---|---|
| (5 config files) | Initial | Fixed |
| kindergarten-incident-report.md | Initial | Workspace |
| cctv-footage-description.md | Initial (placeholder) | Workspace |
| medical-examination-report.md | Initial | Workspace |
| parent-group-chat-export.md | Initial | Workspace |
| kindergarten-safety-policy.md | Initial | Workspace |
| linyi-wound-analysis.md | Update 1 (before R5) | new |
| doudou-detailed-testimony.md | Update 2 (before R7) | new |
| cctv-footage-description.md (updated) | Update 3 (before R11) | replace |
| teacher-zhao-confession.md | Update 4 (before R21) | new |
