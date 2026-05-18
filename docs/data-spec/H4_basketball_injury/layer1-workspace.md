# Layer 1 -- Workspace File Spec

> All workspace files stored under `benchmark/data/calmb-new/workspaces/trace_h4/`.
> Session dialogue and workspace content in Chinese (simplified). Eval questions/options in English.
> Workspace files simulate "system exports" -- game transcripts, medical records, referee reports, insurance forms.

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

你是王明的运动伤害维权分析助手，帮助他处理篮球赛受伤后的责任认定和保险理赔。
```

### IDENTITY.md

```markdown
# Identity

你是 **SportsRights AI**，一个运动伤害维权分析助手，部署在王明（电子科技大学计算机系大一新生，成都）的环境中，帮助他处理校际篮球赛受伤后的一系列问题——裁判判罚争议、诊断差异和保险理赔。

你帮助王明分析比赛录像描述、裁判报告、校医院和医院的医疗记录、保险理赔文件和比赛规则，进行多源交叉验证。
```

### SOUL.md

```markdown
# 工作原则

1. **证据链优先**：所有评估基于录像描述、裁判报告、医疗记录、保险条款等可验证文档。
2. **跨源验证**：录像（发生了什么）、裁判报告（官方判定）、医疗记录（伤情）、保险条款（覆盖范围）需独立比对。
3. **规则准确性**：引用具体的CUBA篮球规则条款和保险合同条款，不做模糊判断。
4. **来源可靠性**：医院MRI诊断 > 校医院体检 > 裁判报告 > 当事人回忆。
5. **先结论后解释**：直接给出判断，再展开理由（王明偏好）。
6. **举例说明**：用具体场景和类比解释抽象概念。
```

### USER.md

```markdown
# 人员和频道

## 主要用户
- **王明 (Wang Ming)** -- 电子科技大学计算机系大一，17岁。篮球赛受伤后维权。聪明但缺乏维权经验，爱篮球。偏好简洁列表、结论先行、举例优先、口语化。

## 关键人物

| 姓名 | 角色 | 渠道 | 关系 |
|---|---|---|---|
| 马强 | 队友 | IM | 目击证人 |
| 刘教练 | 篮球队教练 | IM | 提供录像分析 |
| 母亲 | 家长 | 电话/微信 | 推动就医和理赔 |
| 辅导员 | 学校辅导员 | IM | 协助调取文件 |

## 频道
- **IM**: 王明与队友、教练、辅导员
- **电话/微信**: 王明与母亲
```

### TOOLS.md

```markdown
# 可用工具

- `exec ls` -- 列出文件
- `exec cat <filename>` -- 读取文件
- `exec grep <pattern> <filename>` -- 搜索
- `sessions_list` -- 列出会话
- `sessions_history <session_id>` -- 读取会话
```

---

## 2. Initial Scenario Files (5 files)

### game-video-transcript.md

**Purpose:** 比赛录像文字描述（因无法嵌入视频，以详细文字描述代替）。

**Key content:**
- 第3节 6:42: "王明(15号)持球从右侧三分线外启动突破。对方32号张强从弱侧移动过来，在罚球线附近两人接触。张强的右膝碰到王明的左膝侧面。接触瞬间张强的左脚尚在移动中（未完全站定）。王明失去平衡，身体向左倾斜，左膝先着地后向内翻转。"
- 接触前后的位置描述、其他球员位置
- 5-8个非关键回合的描述作为噪声

**Token estimate:** ~2,500 tokens

### referee-report.md

**Purpose:** 裁判赛后报告（正式版本）。

**Key content:**
- 比赛信息: 电子科技大学 vs 四川大学, 友谊赛, 2026-03-XX
- 第3节 6:42: "15号王明与对方32号张强身体接触后倒地。判定：无犯规（play on）。"
- **注释栏: "接触发生在受限区域内，防守方处于移动状态。"**
- 其他判罚记录（噪声）

**Token estimate:** ~1,500 tokens

### medical-record-campus.md

**Purpose:** 校医院诊疗记录。

**Key content:**
- 就诊时间: 比赛当天下午
- 主诉: 左膝疼痛，篮球比赛中倒地受伤
- 查体: 左膝肿胀(+), 压痛(+), 活动受限, **前抽屉试验可疑阳性**
- 诊断: **左膝轻度扭伤**
- 处理: 冰敷, 弹力绷带, 布洛芬400mg tid
- 医嘱: 休息一周，避免剧烈运动
- 费用: ¥150

**Token estimate:** ~1,000 tokens

### insurance-claim-form.md

**Purpose:** 保险理赔申请表 + 保单条款摘要 + 华西医院诊断引用。

**Key content:**
- 保单信息: 学生意外险, 保障范围"因运动/体育活动导致的意外伤害", 最高 ¥30,000
- 华西医院诊断引用: "左膝前交叉韧带(ACL)部分撕裂", MRI报告编号, 建议手术评估
- 治疗费用估算: ¥15,000-¥25,000
- 理赔状态: 已提交 (W1D5)
- [Update 1 追加]: 拒赔通知: "本次伤害发生在休闲性质的友谊赛中，不属于保障范围内的'运动伤害'（指学校组织的正式体育课程或校队训练）"

**Token estimate:** ~2,000 tokens

### sports-rules-extract.md

**Purpose:** CUBA篮球规则和保险条款的相关条文摘录。

**Key content:**
- CUBA规则4.14条: "防守球员在对方的行进路线上必须占据合法防守位置（双脚着地，面对对方球员）"
- CUBA规则4.14.2条: "如果防守球员在移动中接触进攻球员，应判阻挡犯规"
- 保险条款第3.1条: "运动/体育活动导致的意外伤害"（无"正式课程"限定）
- 保险条款第3.2条: "休闲活动（如散步、郊游等日常休闲）不在保障范围内"

**Token estimate:** ~1,500 tokens

---

## 3. Update-Added Workspace Files (3 files)

### Update 1: insurance-claim-form.md (append -- rejection notice)

**Trigger:** Before R5
**Content:** 保险公司拒赔通知追加到理赔表中。

### Update 3: coach-video-analysis.md (new)

**Trigger:** Before R9
**Content:** 刘教练的录像分析报告: 关键帧描述，张强双脚未站定的证据，引用CUBA规则4.14条，结论"应判阻挡犯规"。

### Update 4: sports-dept-approval.md (new)

**Trigger:** Before R11
**Content:** 学校体育部文件: 友谊赛审批编号 UESTC-PE-2026-034，"学校组织的课外体育活动"分类，参赛学生保险覆盖确认。

---

## 4. File Timing Table

| File | Available From | Added By |
|---|---|---|
| Config files (5) | Initial | Setup |
| game-video-transcript.md | Initial | Setup |
| referee-report.md | Initial | Setup |
| medical-record-campus.md | Initial | Setup |
| insurance-claim-form.md | Initial + Update 1 (append) | Setup + Update 1 |
| sports-rules-extract.md | Initial | Setup |
| coach-video-analysis.md | Update 3 | Update 3 |
| sports-dept-approval.md | Update 4 | Update 4 |

---

## 5. Token Budget

| Category | Estimated Tokens |
|---|---|
| 5 config files | ~2,000 |
| 5 initial scenario files | ~8,500 |
| 3 update files | ~3,000 |
| Total workspace | ~13,500 |
