# Layer 1 -- Workspace File Spec

> All workspace files under `benchmark/data/calmb-new/workspaces/trace_j6/`.

---

## 1. Fixed Agent Configuration Files
*(Standard: AGENTS.md, IDENTITY.md (**PetCare AI**, pet medical analysis assistant), SOUL.md (pet welfare priority, medical evidence-based, consent law), USER.md (周芳, 陈医生/original vet, 李医生/second opinion, 母亲, 大学室友), TOOLS.md)*

---

## 2. Scenario-Specific Workspace Files

### pet-medical-record.md (Initial)
- Title: `宠物医疗记录 -- 豆豆(柯基) -- 爱宠佳宠物医院`
- **C1:** Surgery record: "右前肢桡骨骨折内固定，3.5mm锁定钢板+6骨钉，术后X光确认位置正确。" 2-week follow-up X-ray: 骨钉2号4号偏斜15度，钢板偏移2mm。
- **Length:** ~800 words, ~1,200 tokens

### surgery-consent-form.md (Initial)
- Title: `手术知情同意书 -- 豆豆 -- 2026-03-01`
- **C2:** Lists: infection, anesthesia risk, wound healing. **Missing:** implant failure/loosening, non-union, revision surgery. Signed by 周芳.
- **Length:** ~400 words, ~600 tokens

### post-op-recovery-log.md (Initial)
- Title: `术后恢复记录 -- 豆豆 -- 2026-03-01至03-15`
- **C3 NON-CONFLICT:** Amoxicillin-clavulanate 7 days (03/01-03/07), meloxicam 5 days (03/01-03/05), wound dressing 03/03, 03/06, 03/09. All timestamps consistent.
- **Length:** ~500 words, ~750 tokens

### second-opinion-notes.md (Update 1, before R5)
- Title: `第二诊意见 -- 李医生 -- 骨科专科 -- 2026-03-16`
- **C4 Source A:** "骨钉2号4号偏斜约15度(标准±5度)。锁定钢板角稳定设计下，正常活动不应导致角度改变。判断为术中置入问题。建议翻修。"
- **Length:** ~500 words, ~750 tokens

### vet-communication-email.md (Update 2, before R6)
- Title: `与宠物医生沟通记录 + 标准知情同意指南`
- **C2 Source B:** 引用《小动物骨科手术知情同意标准》："内固定术同意书应包括但不限于：感染、麻醉、伤口愈合、**内固定松动/失败、骨不连/延迟愈合、需要二次手术**。"
- **Length:** ~400 words, ~600 tokens

---

## 3. File Timing Summary

| File | First Visible | Purpose |
|---|---|---|
| pet-medical-record.md | Initial | C1 (surgery vs X-ray) |
| surgery-consent-form.md | Initial | C2 (incomplete consent) |
| post-op-recovery-log.md | Initial | C3 (medication, non-conflict) |
| second-opinion-notes.md | Update 1 | C4 (second vet opinion) |
| vet-communication-email.md | Update 2 | C2 (consent standard reference) |

## 5. Total: ~9 files, ~6,300 tokens
