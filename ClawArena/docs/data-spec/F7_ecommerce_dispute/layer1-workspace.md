# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_f7/`.
> Session dialogue and workspace content are in Chinese (simplified). Eval questions/options are in English.
> Workspace files simulate "system exports" -- order history, logistics tracking, payment records.
> File naming follows timestamp-prefix convention where applicable (赵磊's P2 preference).

---

## 1. Fixed Agent Configuration Files

### AGENTS.md

```markdown
# Agent 启动流程

1. 阅读 `SOUL.md` 了解工作原则。
2. 阅读 `USER.md` 了解你交互的人和频道。
3. 运行 `exec ls` 查看当前 workspace 文件。
4. 使用 `sessions_list` 查看所有可用历史会话。
5. 使用 `sessions_history` 按需读取相关会话内容。

你是赵磊的消费者权益分析助手，帮助他整理购物纠纷证据、分析维权策略。
```

### IDENTITY.md

```markdown
# Identity

你是 **ShopGuard AI**，一个电商消费者权益分析助手，部署在赵磊（独立量化交易员，上海）的工作环境中，帮助他处理618购物纠纷——连续三次购买A100 GPU却收到A40替代品。

你帮助赵磊分析订单记录、物流跟踪、支付流水、客服聊天记录和商品截图，进行多源交叉验证，整理证据链。

你可以访问 workspace 文档（订单记录、物流日志、支付记录、商品截图、退换货政策）和所有历史聊天会话。
```

### SOUL.md

```markdown
# 工作原则

1. **证据链优先**：所有评估必须基于 workspace 文件和会话记录中的可验证信息。客服的口头承诺必须与订单系统记录交叉验证。
2. **跨源验证**：在接受任何关于发货状态、换货授权、退款进度的声明之前，检查订单系统、物流系统、支付系统是否一致。
3. **量化精确性**：始终提供具体金额、SKU、时间戳、工单编号。"可能发错"这类表述无价值。给出具体的证据差异和金额差异。
4. **来源可靠性排序**：系统记录（订单、物流、支付）> 第三方证据（快递员、其他消费者）> 客服口头承诺 > 商家事后声明。
5. **时序感知**：消费纠纷按时间线展开。标注每个事件的精确时间，用时间线揭示商家行为模式。
6. **消费者权益视角**：中国消费者权益保护法、电商平台规则和商家活动条款是判断依据。区分物流过失和商业欺诈。
```

### USER.md

```markdown
# 人员和频道

## 主要用户
- **赵磊 (Zhao Lei)** -- 独立量化交易员（上海），34岁。618购物纠纷维权：下单A100 GPU三次收到A40。内向、数据驱动、社交焦虑。偏好代码格式输出（JSON/表格/diff），时间戳前缀命名，证据链优先的分析结构，带具体金额的量化分析，简洁技术语言无客套。

## 关键人物

| 姓名 | 角色 | 渠道 | 关系 |
|---|---|---|---|
| 客服小刘 | 京东客服代表 | 在线客服 IM | 处理赵磊的投诉；口头承诺换货但系统无对应记录 |
| 快递小哥张师傅 | 顺丰快递员 | SMS | 负责赵磊片区配送；提供物流内部系统截图 |
| 群友老韩 | #购物群 成员 | 微信群 | 有类似618被替代发货的经历；提供旁证 |

## 频道
- **#购物群** (微信群): 赵磊, 老韩, 及其他群友 -- 购物经验分享、维权交流
```

### TOOLS.md

```markdown
# 可用工具

- `exec ls` -- 列出当前 workspace 目录中的文件
- `exec cat <filename>` -- 读取指定 workspace 文件的完整内容
- `exec grep <pattern> <filename>` -- 在指定文件中搜索关键词
- `sessions_list` -- 列出所有可用历史会话
- `sessions_history <session_id>` -- 读取指定会话的完整内容
```

---

## 2. Initial Scenario Files (5 files)

### order-history-618.md

**Purpose:** 京东订单记录导出 -- 包含赵磊618期间的GPU订单及相关订单。

**Key content:**
- 订单 JD-618-2026-7891234: NVIDIA A100 80GB GPU, SKU: GPU-A100-80G, ¥72,999, 2026-06-18 10:02:33 CST, 状态: 售后中
- RMA 工单 RMA-2026-0620-001: 创建于 2026-06-20 14:15:00, 原因: 发货错误, 状态: 已完成 (仅此一个 RMA 记录)
- 无第二次、第三次换货的 RMA 记录
- 8-10 条噪声订单: 显示器支架、网线、键盘、咖啡豆等日常购物

**Noise design:** 噪声订单金额较小 (¥50-¥500)，与GPU订单形成鲜明对比。一条笪声订单提及"显卡散热器"（与GPU相关但无矛盾信息）。

**Token estimate:** ~3,000 tokens

### package-tracking-log.md

**Purpose:** 物流跟踪记录导出 -- 三次发货的完整物流信息。

**Key content:**
- 第一次: SF-2026-0619-88761, 2026-06-19 发出, 商品描述: "NVIDIA 专业显卡", 2026-06-20 签收
- 第二次: SF-2026-0622-88922, 2026-06-22 发出, 商品描述: "NVIDIA 专业显卡", 2026-06-22 签收
- 第三次: SF-2026-0625-89103, 2026-06-25 发出, 商品描述: "NVIDIA 专业显卡", 2026-06-25 签收
- 物流面单上均未标明具体GPU型号（A100或A40），仅写"NVIDIA 专业显卡"
- 内部商品代码字段（物流系统可见但买家端不可见）: 三次均为 GPU-A40-48G
- 5-8 条噪声物流记录: 其他包裹的正常配送

**Noise design:** 噪声物流记录展示正常的618配送（延迟签收、代收点等），营造618物流繁忙的背景。

**Token estimate:** ~2,500 tokens

### payment-records.md

**Purpose:** 支付宝交易记录导出 -- 6月份相关交易。

**Key content:**
- 2026-06-18 10:02:45: 支付宝扣款 ¥72,999, 订单号 JD-618-2026-7891234, 商户: 京东自营GPU旗舰店
- 2026-06-27 09:30:00: 退款处理中 ¥32,000, 备注: "售后退款-JD-618-2026-7891234"
- 退款金额 ¥32,000 对应 A40 市场价，而非原始支付金额 ¥72,999
- 10-15 条噪声交易: 外卖、打车、水电费、云服务器费用等

**Noise design:** 噪声交易为赵磊的日常生活开支，金额从 ¥15 到 ¥2,000 不等，与GPU金额差异大。

**Token estimate:** ~2,000 tokens

### product-listing-screenshot.md

**Purpose:** 商品页面截图的文字描述 -- 赵磊在下单时和后续分别保存的商品页面。

**Key content:**
- 截图1 (2026-06-18 10:00:15): A100 80GB GPU, 618特惠 ¥72,999 (原价 ¥79,999), "有货，预计6月20日前发出", 活动规则链接（无替代发货条款）
- 截图2 (2026-06-25 20:30:00, Update 1 新增): A100 80GB GPU, ¥74,999 (618活动已结束部分优惠), "有货，48小时内发出"
- 两次截图均未显示任何"缺货替代"或"同系列替换"的条款
- 活动页面的"618大促规则"链接中只有通用的退换货条款

**Token estimate:** ~1,500 tokens

### return-policy.md

**Purpose:** 京东退换货政策文件导出。

**Key content:**
- 标准退换货: 签收7天内可退; 商品质量问题或发货错误由商家承担运费
- 618活动特别条款: 活动商品支持7天无理由退货; 价格保护30天
- **无任何"缺货替代发货"条款**
- **无任何"同系列产品替代"条款**
- 商家义务: 如无法履约需告知消费者并全额退款

**Token estimate:** ~1,000 tokens

---

## 3. Update-Added Workspace Files (4 files)

### Update 1: product-listing-screenshot.md (append)

**Trigger:** Before R5
**Content:** 追加截图2 -- 6月25日第三次收到错货后截取的商品页面，A100仍显示"有货"。

### Update 2: payment-detail-export.md (new)

**Trigger:** Before R7
**Content:** 支付宝详细交易明细导出，显示退款金额 ¥32,000 的详细信息: 退款商品描述已被改为"NVIDIA A40 48GB GPU"，而非原始订单的 A100。

### Update 3: courier-evidence.md (new)

**Trigger:** Before R9
**Content:** 快递小哥张师傅提供的物流内部系统截图文字记录，显示三次发货的商品代码均为 GPU-A40-48G。备注字段: "仓库618期间A100库存为0，按内部替代政策发A40"。

### Update 4: seller-response-email.md (new)

**Trigger:** Before R11
**Content:** 商家客服主管的正式回复邮件，引用"618活动补充条款第7.3条: 如指定商品库存不足，商家有权以同系列产品替代发货"。但该条款在赵磊保存的活动页面截图和 return-policy.md 中均不存在。

---

## 4. File Timing Table

| File | Available From | Added By |
|---|---|---|
| AGENTS.md | Initial | Setup |
| IDENTITY.md | Initial | Setup |
| SOUL.md | Initial | Setup |
| USER.md | Initial | Setup |
| TOOLS.md | Initial | Setup |
| order-history-618.md | Initial | Setup |
| package-tracking-log.md | Initial | Setup |
| payment-records.md | Initial | Setup |
| product-listing-screenshot.md | Initial (截图1); Update 1 (截图2 appended) | Setup + Update 1 |
| return-policy.md | Initial | Setup |
| payment-detail-export.md | Update 2 | Update 2 |
| courier-evidence.md | Update 3 | Update 3 |
| seller-response-email.md | Update 4 | Update 4 |

---

## 5. Token Budget

| Category | Estimated Tokens |
|---|---|
| 5 config files | ~2,000 |
| 5 initial scenario files | ~10,000 |
| 4 update files | ~4,000 |
| Total workspace | ~16,000 |
