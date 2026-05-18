# Layer 1 -- Workspace File Spec

> All workspace files under `benchmark/data/calmb-new/workspaces/trace_i7/`.
> Content in Chinese (simplified). Eval questions in English.
> Files simulate hospital inventory exports, procurement records, dispensing logs.

---

## 1. Fixed Agent Configuration Files

### AGENTS.md
```markdown
# Agent 启动流程
1. 阅读 `SOUL.md` 了解工作原则。
2. 阅读 `USER.md` 了解你交互的人和频道。
3. 运行 `exec ls` 查看当前 workspace 文件。
4. 使用 `sessions_list` 和 `sessions_history` 读取历史会话。

你是林怡的医院物资管理分析助手，帮助她调查流感季物资短缺的根因——库存系统、采购记录和各科室领用之间的数据差异。
```

### IDENTITY.md
```markdown
# Identity
你是 **MedOps AI**，一个医院运营与物资管理分析助手，部署在林怡（急诊科主治医生，北京友谊医院）的工作环境中。

你帮助林怡分析库存系统数据、采购订单、签收记录、科室领用日志、药房发药汇总——跨系统进行数据交叉验证，识别物资管理中的差异和问题。
```

### SOUL.md
```markdown
# 工作原则
1. **数据溯源优先**：系统记录 vs 实物盘点 vs 签收单据，每个数据点必须追溯到原始来源。
2. **跨源对比**：同一物资在不同系统的数量差异必须量化并标注。
3. **流程合规**：物资领用必须满足正式审批流程，口头审批不等于正式授权。
4. **模式识别**：单一差异可能是录入误差；系统性差异可能是管理漏洞。
5. **患者安全优先**：物资短缺直接影响医护人员防护和患者安全。
6. **事实导向**：分析聚焦于数据和流程，不做动机推断。
```

### USER.md
```markdown
# 人员和频道
## 主要用户
- **林怡 (Lin Yi)** -- 急诊科主治医生（北京友谊医院），30岁。调查流感季物资短缺根因。偏好结构化格式（主诉/检查/诊断/处理），日期+ID命名，结论优先，循证分析，简洁专业。

## 关键人物
| 姓名 | 角色 | 渠道 | 关系 |
|---|---|---|---|
| 张主任 | 急诊科主任 | 微信 | 林怡上级，试图压下问题 |
| 药房主任 | 药房负责人 | 邮件 | 负责物资管理，有未上报的手工发放 |
| 李主任 | 呼吸内科主任 | 微信/物资群 | 声称未多领但记录显示多领300只 |
| 库管员小赵 | 库房管理员 | 微信 | 签收了1500只但系统录入2000只 |
```

### TOOLS.md
```markdown
# 可用工具
| 工具 | 用途 |
|---|---|
| `sessions_list` | 列出可用历史会话 |
| `sessions_history` | 读取历史会话 |
| `read` | 读取workspace文件 |
| `exec` | shell命令 |

文件命名：日期+类型前缀（2026-12_库存导出.md, 采购订单_PO2026.md），符合林怡 P2 偏好。
```

---

## 2. Scenario-Specific Workspace Files

### inventory-system-export.md (Initial)

**Content key points:**
- Title: `医院物资管理系统导出 -- N95口罩库存 -- 导出日期 2026-12-15`
- Format: Simulates hospital inventory management system export
- **Key data (C1 Source A):**
  - 物资编号: MED-N95-001
  - 品名: N95医用防护口罩
  - 期初库存（12月1日）: 800只
  - 本月采购入库: 2,000只（采购单 PO-2026-1205）
  - 本月系统领用合计: 2,300只
    - 急诊科: 800只
    - 呼吸内科: 800只（系统记录）
    - 其他科室合计: 200只
    - 手工调配: 500只（备注：紧急调配）
  - **系统余额: 500只**
  - 最后更新: 2026-12-15 08:00
- **C1 source:** System shows 500 remaining. Ground truth is 200 (physical count).
- **Near-signal noise:** Other supply items (surgical masks, gloves, gowns), their inventory levels, automated reorder thresholds.

**Length estimate:** ~800 words, ~1,200 tokens

---

### procurement-orders.md (Initial)

**Content key points:**
- Title: `采购订单记录 -- 2026年12月 -- 医疗防护物资`
- Format: Simulates procurement system export
- **Key data (C2 Source A):**
  - 采购单号: PO-2026-1205
  - 下单日期: 2026-12-05
  - 供应商: 华康医疗器械有限公司
  - 品名: N95医用防护口罩
  - 采购数量: 2,000只
  - 单价: ¥4.50/只
  - 总金额: ¥9,000
  - 状态: 已入库
  - 入库日期: 2026-12-10
  - 入库数量: 2,000只（系统自动按订单量录入）
- **C2 source:** Procurement says 2000 ordered and "received." But delivery receipt shows only 1500.
- **Near-signal noise:** Other procurement orders (surgical masks, antiseptic, thermometers), supplier contact info, payment status.

**Length estimate:** ~600 words, ~900 tokens

---

### department-requisition-log.md (Initial)

**Content key points:**
- Title: `科室物资领用日志 -- 急诊科 -- 2026年12月`
- Format: Simulates department-level requisition log with signatures
- **Key data (C3 -- NON-CONFLICT):**
  - 10次领用记录，每次含：日期、时间、品名、数量、领用人签字、药房确认签字
  - 12/01: 100只, 领用人王护士, 药房确认✓
  - 12/03: 80只, 领用人李护士, 药房确认✓
  - 12/05: 100只, 领用人王护士, 药房确认✓
  - 12/07: 80只, 领用人张护士, 药房确认✓
  - 12/08: 60只, 领用人王护士, 药房确认✓
  - 12/09: 80只, 领用人李护士, 药房确认✓
  - 12/10: 100只, 领用人王护士, 药房确认✓
  - 12/11: 60只, 领用人张护士, 药房确认✓
  - 12/13: 80只, 领用人李护士, 药房确认✓
  - 12/14: 60只, 领用人王护士, 药房确认✓
  - **合计: 800只**
- **C3 confirmation:** ER requisitions = 800, matching pharmacy dispensing records. No discrepancy.
- **Near-signal noise:** Other supply requisitions (gloves, gowns), nurse shift schedule references.

**Length estimate:** ~700 words, ~1,050 tokens

---

### pharmacy-dispensing-summary.md (Initial)

**Content key points:**
- Title: `药房发药汇总 -- N95口罩 -- 2026年12月 -- 截至12月15日`
- Format: Simulates pharmacy dispensing summary
- **Key data (C4 Source B):**
  - 按科室汇总:
    - 急诊科: 800只（10次正式领用，与科室日志一致）
    - 呼吸内科: 1,100只（8次正式领用800只 + 3次紧急手工发放各100只，手工发放备注"口头审批-药房主任"）
    - 其他科室合计: 200只
  - **发药总计: 2,100只**
  - 呼吸内科分配额: 800只/月
  - 呼吸内科实际领用: 1,100只（超额300只）
- **C4 evidence:** Respiratory dept received 1100, 300 over their 800 allocation. Manual dispensing records present but marked "oral approval."
- **Near-signal noise:** Other medication dispensing records, expiration date tracking, batch numbers.

**Length estimate:** ~600 words, ~900 tokens

---

### delivery-receipt.md (Update 1, before R5)

**Content key points:**
- Title: `送货签收单 -- 华康医疗器械有限公司 -- 2026-12-10`
- Format: Simulates physical delivery receipt scan
- **Key evidence (C2 Source B):**
  - 签收单号: DR-2026-1210
  - 对应采购单: PO-2026-1205
  - 送货品名: N95医用防护口罩
  - 订单数量: 2,000只
  - **实收数量: 1,500只**
  - 差异说明: 供应商产能不足，剩余500只预计下批次补发（预计12月25日）
  - 签收人: 小赵（库管员）
  - 签收日期: 2026-12-10
  - 签收备注: "已与供应商确认，余量将补发。已通知药房主任。"
- **C2 evidence:** Only 1500 received vs 2000 ordered. System auto-recorded 2000.

**Length estimate:** ~350 words, ~525 tokens

---

### supply-chain-email-thread.md (Update 2, before R6)

**Content key points:**
- Title: `物资调配邮件链 -- 2026年11月-12月 -- N95口罩供应`
- Format: Simulates email thread export
- **Key evidence (C4 Source B expanded, pharmacy director warning):**
  - Email 1 (Nov 15): 华康医疗 -> 药房主任: "尊敬的主任，受原材料价格上涨和产能调整影响，12月N95口罩供应可能延迟或减量交付，建议贵院提前备货或启动备选供应商。"
  - Email 2 (Nov 18): 药房主任 -> 华康医疗: "收到，我们会关注。请尽量保证交付。"（未转发给科室）
  - Email 3 (Dec 10): 小赵 -> 药房主任: "今天收到华康N95口罩1500只，比订单少500只。签收单已签。请确认系统是否需要修改入库数量。"
  - Email 4 (Dec 10): 药房主任 -> 小赵: "先按2000录系统，等补货到了再说。"
  - Email 5 (Dec 12): 呼吸内科护士长 -> 药房主任: "李主任说流感病人太多，需要额外100只N95，请紧急调配。"（此类邮件有3封，12/05, 12/08, 12/12）
  - Email 6 (Dec 12): 药房主任 -> 呼吸内科护士长: "批了，直接来取。" （无正式审批单）
- **Critical evidence:** Pharmacy director (a) knew about supply shortage in advance, (b) instructed system to over-record, (c) approved manual dispensing without formal process.

**Length estimate:** ~600 words, ~900 tokens

---

## 3. File Timing Summary

| File | First Visible | Purpose |
|---|---|---|
| inventory-system-export.md | Initial | C1 Source A (system balance 500) |
| procurement-orders.md | Initial | C2 Source A (ordered 2000, "received" 2000) |
| department-requisition-log.md | Initial | C3 (ER requisitions = 800, consistent) |
| pharmacy-dispensing-summary.md | Initial | C4 Source B (respiratory 1100, allocation 800) |
| delivery-receipt.md | Update 1 (before R5) | C2 Source B (actually received 1500) |
| supply-chain-email-thread.md | Update 2 (before R6) | Pharmacy director warnings + manual approval evidence |

---

## 4. Near-Signal Noise Design

### inventory-system-export.md
- **Why it looks relevant:** Official hospital system data.
- **Why it should not settle C1:** The system auto-records procurement at order quantity, not receipt quantity. Without delivery receipt, system data appears authoritative.
- **Noise risk:** Agent may trust system balance of 500 as accurate.

### pharmacy-dispensing-summary.md
- **Why it looks relevant:** Shows all departmental dispensing.
- **Why detail may be missed:** The "口头审批-药房主任" annotation on respiratory's extra 300 is easy to overlook among many line items.

---

## 5. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | ~2,000 tokens |
| Initial scenario files (4 files) | ~4,050 tokens |
| Update files (2 files) | ~1,425 tokens |
| **Total workspace** | **11 files** | **~7,475 tokens** |
