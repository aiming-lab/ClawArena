# Data Augmentation Plan v4

> 在 v3（6 个 EC 场景）基础上，再向 `data/clawarena` 添加 5 个场景的 EC 扩充。
> 难度规范与执行约束完整继承 `difficulty-upgrade-guide.md` 和 `v3-plan.md`。

---

## 一、场景选择

### 1.1 已有 7 个场景的域覆盖

| 场景 | 域 |
|------|----|
| hil_s1 | 科技企业（客户流失分析） |
| hil_f3 | 科技企业（量化交易时区 Bug） |
| hil_g3 | HR/职场（薪资数据泄露） |
| hil_d3 | 医疗（ICU 护理超时瞒报） |
| hil_i2 | 教育科研（学术数据重用指控） |
| hil_g1 | HR/职场（背景核查差异） |
| hil_j1 | 科技企业（MCN 数据欺诈） |

### 1.2 新增 5 个场景（最终选定）

| 场景 | 域 | 主角/组织 | 选择理由 |
|------|----|----------|---------|
| **hil_e4** | 非盈利组织 | GlobalBridge Foundation（Nairobi 项目） | 拨款合规审计：预算追踪 × 拨款协议 × 现场叙事三源，M1/M3 精确数值核查潜力最高 |
| **hil_g4** | 法律政策 | HR 经理调查孙伟案 | 不当解雇 + PIP 流程，workspace 明确含 `labor-law-reference.md`，4 个完整 upd_workspace |
| **hil_f7** | 个人/家庭 | 消费者（618 购物节） | GPU 电商欺诈维权：订单 × 支付 × 快递三源交叉，精确时序与金额核查 |
| **hil_h3** | 教育科研 | 王明（UESTC CS 大一） | CS 作业抄袭争议：双仓库 git 历史溯源，全批最独特的 M5 脚本解析类型 |
| **hil_c7** | 科技企业 | Alex Rivera（NexaFlow） | API 安全漏洞泄露事件：7 个初始 workspace 文件，网络安全 + 监管披露角度，与 s1/f3/j1 均无重叠 |

### 1.3 12 场景域分布

| 域 | 场景（共 12） |
|----|-------------|
| 科技企业 | s1, f3, j1, **c7** |
| HR/职场 | g1, g3 |
| 医疗 | d3 |
| 教育科研 | i2, **h3** |
| 法律政策 | **g4** |
| 个人/家庭 | **f7** |
| 非盈利组织 | **e4** |

> 注：extended 数据集中无背景独立的"社区组织"场景（e 系列全属同一 GlobalBridge 生态），故此域暂缺，以整体均衡为优先。

---

## 二、各场景详细分析

---

### 2.1 hil_e4 — GlobalBridge Nairobi 项目中期拨款合规审计

**背景**：Pemberton Foundation 对 GlobalBridge 在内罗毕的 Q2 项目进行中期合规审查，发现现场叙事报告与财务追踪数据之间存在差异，疑似人员部署与预算申报不一致。

**Workspace 初始文件（6 个）**

| 文件 | 内容 |
|------|------|
| `financial_tracking_Q2.md` | Q2 财务支出明细（按预算项分类） |
| `grant_deliverables_annex_C.md` | 拨款协议附件 C（交付物要求与里程碑） |
| `hr_roster_nairobi.md` | 内罗毕项目人员名单（职位、到岗日期） |
| `nairobi_field_narrative_Q2.md` | 现场叙事报告（定性描述，含活动数） |
| `pemberton_dashboard_Q2.md` | Pemberton 资助方看板数据（合规指标） |
| `pemberton_grant_agreement_excerpt.md` | 拨款协议正文摘录（条款、金额上限） |

**Updates（4 个）**

| Update | 新增文件 | 关键信息 |
|--------|---------|---------|
| upd1 | `petrova_assessment_prelim.md` | 外部评估员初步报告（质疑人员部署数） |
| upd2 | `david_board_communication.md` | 董事会内部通信（对差异的内部解释） |
| upd3 | `staff_deployment_Q2.md` | 人员实际部署记录（精确到人到天） |

**Update 结构**：原 questions.json update 结构过密（q7–q30 几乎每轮），须从零重排，建议 upd@q6/q12/q18/q24（均匀分散）。

**EC 设计方向**

- **M1**：从 `financial_tracking_Q2.md` 计算各预算项实际支出 vs `grant_deliverables_annex_C.md` 要求的上限，差额精确到美元
- **M3**：`hr_roster_nairobi.md`（名单人数）×`staff_deployment_Q2.md`（实际部署天数）×`financial_tracking_Q2.md`（人力成本）三者须交叉一致，合并任务要求生成统一合规报告 + 差异 JSON
- **M5**：agent 写脚本解析 Q2 财务追踪，输出各预算类别支出率（actual/approved × 100%）JSON
- **M6**：现场叙事报告（定性，数字来自估算）的活动人次数据不得被作为财务核查依据

**难点**：财务文件与叙事报告的数字精度层级不同；人员部署天数需与人力成本交叉计算，易因单位换算出错。

---

### 2.2 hil_g4 — 不当解雇指控与 PIP 合规核查

**背景**：HR 经理（user）调查前员工孙伟提出的不当解雇投诉，须核实 PIP（绩效改进计划）流程是否符合劳动法规、1-on-1 记录是否与 PIP 触发条件一致、HR 档案与孙伟自述之间是否存在矛盾。

**Workspace 初始文件（5 个）**

| 文件 | 内容 |
|------|------|
| `employee-hr-file.md` | 孙伟完整 HR 档案（入职日期、绩效评级、警告记录） |
| `labor-law-reference.md` | 劳动法规参考（PIP 最短期限、书面通知要求） |
| `pip-email-chain.md` | PIP 触发通知邮件链（日期、签收确认） |
| `calendar-1on1-history.md` | 1-on-1 日历记录（会议日期、议题标注） |
| `todo-pip-followups.md` | PIP 跟进待办记录（HR 内部操作日志） |

**Updates（4 个，结构良好）**

| Update | 新增文件 | 关键信息 |
|--------|---------|---------|
| upd1 | `sunwei-1on1-notes.md` | 孙伟自述的 1-on-1 记录（与 HR 日历版本有差异） |
| upd2 | `sunwei-written-response.md` | 孙伟对 PIP 的书面异议 |
| upd3 | `pip-timeline-analysis.md` | HR 内部 PIP 时间线分析 |
| upd4 | `legal-updated-assessment.md` | 法务部门最新评估意见 |

**Update 结构**：原 questions.json upd@q5/q7/q9，4 个 upd_workspace 目录，间距良好，重排时适当插入 EC 即可。

**EC 设计方向**

- **M1**：从 `pip-email-chain.md` 提取 PIP 启动日期，与 `labor-law-reference.md` 规定的最短通知期对比，计算是否合规（精确到天）
- **M2**：`calendar-1on1-history.md`（HR 版本）vs `sunwei-1on1-notes.md`（孙伟版本）同一日期的会议内容描述互相矛盾，agent 须裁决哪个来源更可信并给出依据
- **M3**：PIP 合规报告须同时引用 `labor-law-reference.md` 条款编号 + `employee-hr-file.md` 具体日期，check 跨文件校验引用数值一致
- **M4**：法律风险评估 JSON 须包含 `risk_level`（枚举）、`applicable_clause`（字符串）、`days_shortfall`（数值）字段，类型须严格匹配
- **M6**：孙伟的书面异议（主观陈述，无文档依据）不得被作为 HR 程序违规的确定性结论来源

**难点**：劳动法规条款须逐字引用，agent 容易用模糊描述代替具体条款编号；两版 1-on-1 记录的矛盾点细微，需精确对比日期与议题。

---

### 2.3 hil_f7 — 618 购物节 GPU 电商欺诈维权

**背景**：消费者在 618 购物节购入 GPU，收到的商品与商品页面描述不符（疑似以次充好）。消费者须通过订单记录、支付明细、快递追踪、商品列表截图四源交叉核实欺诈行为，并构建维权证据链。

**Workspace 初始文件（5 个）**

| 文件 | 内容 |
|------|------|
| `order-history-618.md` | 618 活动订单记录（商品描述、价格、下单时间） |
| `package-tracking-log.md` | 快递追踪日志（各节点时间戳、签收记录） |
| `payment-records.md` | 支付明细（支付金额、优惠券抵扣、实付款） |
| `product-listing-screenshot.md` | 商品页面截图文字转录（规格参数、承诺描述） |
| `return-policy.md` | 平台退换货政策（时效要求、举证责任） |

**Updates（4 个，完整）**

| Update | 新增文件 | 关键信息 |
|--------|---------|---------|
| upd1 | `product-listing-screenshot-append.md` | 补充商品页面（历史版本存档，显示参数变更） |
| upd2 | `payment-detail-export.md` | 支付平台详细导出（含手续费、分期明细） |
| upd3 | `courier-evidence.md` | 快递公司官方调查回复（重量记录、包装异常） |
| upd4 | `seller-response-email.md` | 卖家官方回复邮件（否认欺诈的声明） |

**Update 结构**：原 upd@q5/q7/q8/q11，q7/q8 相邻须插入 EC 拉开，其余间距合理。

**EC 设计方向**

- **M1**：从 `payment-records.md` 计算实付款与商品列表标价的差值（含优惠券抵扣逻辑），精确到分；与 `payment-detail-export.md` 中的手续费交叉验证
- **M3**：订单时间 × 支付时间 × 快递首节点时间须在维权时间线 JSON 中保持一致，check 跨文件校验三个时间戳
- **M5**：agent 写脚本解析快递追踪日志，输出各节点时间差（精确到分钟），标注异常停滞区间
- **M2**：商品列表当前版本（upd1 后揭示参数已悄改）vs 下单时截图版本，agent 须明确引用下单时版本作为约定依据
- **M6**：卖家回复邮件（主观声明，无检测报告支撑）不得被用作"商品符合描述"的结论依据

**难点**：优惠券抵扣逻辑须完整还原（平台补贴 + 店铺券 + 分期手续费），agent 容易计算错误；商品页面历史版本与当前版本的参数差异须精确对比。

---

### 2.4 hil_h3 — CS101 作业代码抄袭争议

**背景**：UESTC CS101 编程作业（链表反转），王明被助教以 MOSS 系统 87% 相似度上报抄袭，嫌疑对象为同学陈伟。陈伟的 GitHub 公开仓库在截止日期后创建；王明自称独立完成并有 GitLab 提交历史为证。调查员须通过 git commit 时间戳、MOSS 报告行号、Stack Overflow 参考页面还原代码来源。

**Workspace 初始文件（5 个）**

| 文件 | 内容 |
|------|------|
| `git-commit-history-wangming.md` | 王明 UESTC GitLab 提交历史（含时间戳、hash、message） |
| `git-commit-history-opponent.md` | 陈伟 UESTC GitLab + GitHub 双仓库提交历史 |
| `plagiarism-detection-report.md` | MOSS 自动检测报告（相似度 87%、匹配片段行号） |
| `course-syllabus-integrity-policy.md` | CS101 学术诚信政策（抄袭认定标准、申诉流程） |
| `stackoverflow-answer-screenshot.md` | Stack Overflow 参考页面（公共解法来源） |

**Updates（4 个）**

| Update | 新增文件 | 关键信息 |
|--------|---------|---------|
| upd1 | （仅 workspace 更新，含 GitHub 仓库创建日期确认） | 陈伟 GitHub 仓库创建时间 vs 作业截止日期 |
| upd2 | `（sessions + 陈伟仓库配置细节）` | MOSS 系统版本/配置 |
| upd3 | `（sessions + 王明 IDE 自动保存记录）` | 独立编写时序证明 |
| upd4 | `（sessions + 刘教授最终邮件）` | 最终判定依据 |

**Update 结构**：upd@q5/q6/q11/q14，q5/q6 相邻须插入 EC 拉开，q11/q14 间距合理。注：原 questions.json 仅有 25 轮，EC 扩充后须设计完整 30 轮。

**EC 设计方向**

- **M1**：计算王明 GitLab 涉嫌相似 commit 与陈伟对应 commit 的时间差（精确到分钟），哪个在前是核心证据
- **M5**：agent 写脚本解析双方 git 历史 md，输出 JSON（各 commit 时间戳、两仓库相似片段首次出现方、时间差）
- **M4**：`code_provenance_analysis.json` 须包含 `commit_owner`、`timestamp`、`source_confidence`（枚举 `confirmed/probable/disputed`）字段，类型严格匹配
- **M2**：MOSS 87% 相似度（算法）vs Stack Overflow 公共解法可解释性（人工判断），agent 须明确裁决两种解释中哪个更充分
- **M6**：陈伟截止日期后创建的 GitHub 仓库 commit 时间戳不得被用作"陈伟先写"的证据（负向断言）

**难点**：两个仓库（GitLab vs GitHub）须明确区分；截止日期是判断的关键锚点，agent 须正确比较仓库创建时间与截止时间的先后关系。

---

### 2.5 hil_c7 — NexaFlow API 安全漏洞泄露事件

**背景**：NexaFlow（SaaS 产品）发现 API 安全漏洞导致客户数据泄露。Alex Rivera（产品经理）须与安全顾问、DevOps、法务协调：核实漏洞技术细节、评估受影响客户数据范围、验证事件响应是否符合监管披露时效要求（72 小时通知窗口）。

**Workspace 初始文件（7 个，最丰富）**

| 文件 | 内容 |
|------|------|
| `api_endpoint_register.md` | API 端点注册表（端点列表、权限级别、暴露数据类型） |
| `customer_data_inventory.md` | 客户数据清单（数据类型、数量、敏感级别分类） |
| `developer_docs_screenshot.md` | 开发者文档截图转录（API 访问控制说明） |
| `disclosure_report_initial.md` | 初始披露报告草稿（事件描述、影响范围初估） |
| `incident_response_checklist.md` | 事件响应检查清单（各步骤完成状态） |
| `notification_draft_v1.md` | 客户通知邮件草稿 v1 |
| `vulnerability_technical_brief.md` | 漏洞技术简报（CVE 编号、CVSS 评分、攻击向量） |

**Updates（4 个）**

| Update | 新增文件 | 关键信息 |
|--------|---------|---------|
| upd1 | `access_log_analysis.md` | 访问日志分析（异常访问时间窗口、受影响端点） |
| upd2 | `deployment_timeline.md` | 部署时间线（漏洞引入版本、修复部署时间） |
| upd3 | `notification_final.md` | 最终客户通知邮件（发送时间戳） |

**Update 结构**：upd@q4/q5/q7/q9，q4/q5 相邻须插入 EC 拉开，q7/q9 间距合理。

**EC 设计方向**

- **M1**：从 `access_log_analysis.md` 提取漏洞首次被利用时间戳，与 `deployment_timeline.md` 中漏洞修复时间对比，计算暴露窗口时长（小时精度）；与 `notification_final.md` 发送时间对比，验证 72 小时监管通知窗口是否满足（关键合规验证）
- **M3**：`customer_data_inventory.md`（受影响数据类型）×`api_endpoint_register.md`（暴露端点所关联数据）×`disclosure_report_initial.md`（初估影响范围）三源须交叉一致，合并任务输出最终影响范围报告 + 差异说明
- **M5**：agent 写脚本解析 `api_endpoint_register.md` 和 `customer_data_inventory.md`，输出受影响客户数量 × 数据类型矩阵 JSON
- **M4**：漏洞影响评估 JSON 须包含 `cvss_score`（数值）、`affected_endpoints`（数组）、`notification_compliant`（布尔，72h 窗口）、`exposure_hours`（数值）字段
- **M6**：`disclosure_report_initial.md` 中的初估影响范围（事件初期，数据不完整）不得被用作最终影响客户数的结论依据

**难点**：72 小时合规窗口的计算需要三个精确时间戳（漏洞发现时间、监管机构报告时间、客户通知时间），任一时间戳混淆即导致合规结论错误；CVSS 评分须与实际攻击向量描述一致。

---

## 三、执行规范（继承 v3）

### 3.1 整体结构目标

| 指标 | 目标 |
|------|------|
| 总轮数 | 30 轮（±3） |
| EC 比例 | ≥ 70% |
| MC 轮数 | 8–10 轮 |
| L3 任务 | 每场景 2–3 道 |

### 3.2 MC 布局（同 v3）

- 场景开篇 2–3 轮（基线矛盾 + 偏好引入）
- 每个 update 触发轮 1 轮
- 最终综合 1–2 轮

### 3.3 EC 合并策略

同批次 update 区间内多个小任务合并为一道多产物任务，`&&` 串联验证：

```bash
python check_primary.py ${workspace} &&
python check_json_schema.py ${workspace}/docs/output.json --schema schemas/schema.json &&
python check_preferences.py ${workspace} --rules P1,P2 --target docs/report*.md
```

### 3.4 pref 两段制

- Phase 0–1（前 1/3 轮）：pref 有 feedback，不计分
- Phase 2–4（后 2/3 轮）：pref 逻辑迁入 eval.command，计分，feedback 为空

### 3.5 造题前必建数值来源表

每场景子计划开头先填 Ground Truth 数值表，写完 check 脚本后逐行回溯核实。

---

## 四、各场景执行优先级

| 顺序 | 场景 | 理由 |
|------|------|------|
| 1 | hil_f7 | 数值类型最纯粹（支付/订单），快速建立电商类 EC 范式 |
| 2 | hil_g4 | 法律文件引用 + 时间线核查，难度适中 |
| 3 | hil_c7 | workspace 最丰富，72h 合规窗口是经典多时间戳验证题 |
| 4 | hil_h3 | git 历史解析脚本是全批最独特类型，须花更多时间设计 |
| 5 | hil_e4 | 财务合规多源交叉最复杂，最后处理 |

---

## 五、注意事项（避雷指南要点）

1. **workspace 文件核实**：造题前先 `ls` 实际目录，尊重现有文件结构，不预设格式
2. **update 重排**：e4（过密）须从零重设 update 触发位置；h3（q5/q6 相邻）、c7（q4/q5 相邻）、f7（q7/q8 相邻）须插入 EC 拉开
3. **Ground Truth 表必须先建**：check 脚本每个期望值须能回溯到 workspace 具体文件行
4. **四框架注册**：加入 clawarena 时须同步注册 openclaw manifest + openclaw.json agents.list + claude-code/picoclaw/nanobot manifest
5. **picoclaw memory 文件**：须复制 `bench_{scene}.jsonl` + `bench_{scene}.meta.json`
6. **openclaw state/agents**：须随 workspaces/updates 同步复制，不得遗漏
7. **clawarena check**：每场景完成后对所有 tests JSON 执行全量 check，须 0 errors
