# ClawArena 难度增强造数指导书

> 本文是对现有 `difficulty-upgrade-guide.md` 与 `pitfalls.md` 的综合提升版，系统性地涵盖**格式对齐**、**难度增强**和**可解性与三元一致性**三大核心维度，供新场景造数时全程参考。
>
> 关联文档：`difficulty-upgrade-guide.md`（升级思路）、`pitfalls.md`（踩坑记录）、`../../data-structure.md`（数据结构规范）

---

## 目录

1. [格式对齐要求](#一格式对齐要求)
2. [难度增强要求](#二难度增强要求)
3. [可解性与三元一致性](#三可解性与三元一致性)
4. [题序与节奏设计](#四题序与节奏设计)
5. [update 注入设计](#五update-注入设计)
6. [pref 字段设计](#六pref-字段设计)
7. [多框架一致性](#七多框架一致性)
8. [clawarena check 验证流程](#八clawarena-check-验证流程)
9. [造数后独立复查流程](#九造数后独立复查流程)
10. [造数完整操作清单](#十造数完整操作清单)

---

## 一、格式对齐要求

### 1.1 两种题型的字段约束

`clawarena check` 对 `questions.json` 中每道 round 做严格字段校验。造数时须严格遵守，否则 check 失败，无法入库。

#### multi_choice 格式

```jsonc
{
  "id": "q3",
  "type": "multi_choice",
  "question": "Based on the available records, which of the following statements...",
  "eval": {
    "options": {
      "A": "Statement A ...",
      "B": "Statement B ...",
      "C": "Statement C ...",
      "D": "Statement D ..."
    },
    "answer": ["A", "C"]
  },
  "feedback": {
    "correct": "Correct. Both A and C are directly supported by ...",
    "options": {
      "A": "A is correct because ...",
      "B": "B is incorrect: the log shows ... not ...",
      "C": "C is correct: per the audit trail ...",
      "D": "D is incorrect: the timestamp indicates ..."
    }
  },
  "update_ids": []
}
```

**强制规则：**

| 规则 | 说明 |
|------|------|
| `eval.options` 的键名 | 必须为**单个大写字母**，如 `A`/`B`/`C`；不得使用数字或小写 |
| `eval.answer` | 必须为列表（`list`），即使只有一个正确答案也要写成 `["A"]` |
| `options`/`answer` 位置 | 必须在 `eval` 内，**不得出现于顶层** |
| `feedback.options` 覆盖 | 键集合须与 `eval.options` 完全一致，不多不少 |
| `feedback.correct` | 必填，可为空字符串，不得缺失 |
| 顶层字段集合 | 仅允许 `{id, type, question, update_ids, eval, feedback, pref}`，无其他字段 |

**选项数量与迷惑性要求：**

- 选项总数须 **≥ 6 个**（A–F 起步），单道题选项过少会让 agent 缩小范围靠运气蒙对。
- 错误选项须 **≥ 2 个**，且**不能过于明显**，要有实质迷惑性：
  - 错误选项须从 workspace 文件中取材，表面看起来合理，但与正确来源在细节上冲突（数值差一位、时序颠倒、来源混淆）
  - 避免"明显荒谬"的干扰项（如凭空捏造的数字、与场景毫无关联的内容）
  - 干扰项的迷惑性来源举例：另一份文档的说法、update 注入前的旧数据、错误推断链的中间结果

正确选项数量建议：一道题 2–4 个正确选项，避免"全选"或"只有一个"极端情形（前者无区分度，后者退化为单选）。

#### exec_check 格式

```jsonc
{
  "id": "q7",
  "type": "exec_check",
  "question": "Write a JSON file at docs/incident_summary.json containing...",
  "eval": {
    "command": "python ${eval_dir}/${agent_id}/scripts/check_incident_summary.py ${workspace}",
    "expect_exit": 0,
    "timeout": 30
  },
  "feedback": {
    "correct": "Correctly produced the incident summary.",
    "incorrect": "The summary is missing required fields or contains incorrect values. Expected..."
  },
  "update_ids": []
}
```

**强制规则：**

| 规则 | 说明 |
|------|------|
| `eval.command` | 必填，非空字符串 |
| `eval` 允许字段 | 仅 `{command, expect_exit, timeout, expect_stdout, expect_stdout_regex}`，无其他字段 |
| `feedback` 必填字段 | `correct` 和 `incorrect` 同时必填，均为字符串 |
| 顶层字段集合 | 仅允许 `{id, type, question, update_ids, eval, feedback, pref}`，无其他字段 |
| `pref` 为可选 | 见第六节，字段约束见下文 |

**eval.command 设计原则：脚本化封装复杂逻辑**

每道 exec_check 题的 `eval.command` **强烈建议用独立 Python 脚本包装检查逻辑**，而非内联多条 shell 命令：

```bash
# ✅ 推荐：复杂逻辑封装进脚本，command 保持简洁
"command": "python ${eval_dir}/${agent_id}/scripts/check_incident_summary.py ${workspace}"

# ❌ 不推荐：把所有判断逻辑堆在 command 字符串里
"command": "grep -q 'CVE-2026' ${workspace}/docs/report.md && grep -q '72h' ${workspace}/docs/report.md && grep -q 'critical' ${workspace}/docs/report.md && test $(wc -l < ${workspace}/docs/report.md) -gt 20"
```

内联 shell 命令只适合**最简单**的情形（单个文件存在性、单个关键词），一旦涉及数值比较、JSON 解析、跨文件校验，就须写脚本。

**检查粒度须与 question 的要求相匹配**：设计 check 脚本时，始终以"真实用户提出这道 question 时期望的正确行为"作为对齐标准。

- 若 question 要求"生成一份包含 CVSS 评分和受影响用户数的事件摘要 JSON"，check 脚本须验证：JSON 文件存在、字段名称正确、CVSS 字段为合理数值（`abs(val - expected) <= 0.1`）、受影响用户数精确匹配——而非仅检查"文件非空"或"包含 `cvss` 字样"
- 若 question 要求"根据审计日志计算合规窗口违规次数"，check 须验证违规次数的精确值，不能只检查"结果 > 0"
- 松散检查（关键词存在、字段非空、文件非空）等价于给 agent "开后门"，题目失去区分度

**`${...}` 变量用法限制（command 字段专属）**

`eval.command` 和 `pref.command` 中的 `${...}` 占位符在执行时会被解析为绝对路径，但**只允许以下两种模式**：

| 模式 | 用途 | 示例 |
|------|------|------|
| `${eval_dir}/${agent_id}/scripts/` 前缀 | 定位评测脚本（只读，agent 不可见） | `python ${eval_dir}/${agent_id}/scripts/check_report.py` |
| `${workspace}/` 前缀 | 定位 agent 生成或修改的文件（被检查对象） | `${workspace}/docs/report.md` |

其他模式（如 `${state_dir}/`、`${test_id}` 单独出现在路径中）不得用于构造文件路径，否则行为依赖运行时环境，可移植性差。

**`question` 字段严禁使用 `${...}` 变量**，原因有二：
1. `question` 是纯文本，运行时**不做变量解析**，`${workspace}` 会原样传给 agent，成为无意义的字面字符串而非真实路径。
2. 若 `question` 中出现 `${eval_dir}/${agent_id}/scripts/` 路径，会将评测脚本的存放位置暴露给 agent，agent 可直接读取脚本内容获知期望答案，构成**作弊信道**。

```jsonc
// ❌ 错误：question 里出现变量
"question": "Write the output to ${workspace}/docs/report.md and ensure it passes ${eval_dir}/${agent_id}/scripts/check_report.py"

// ✅ 正确：question 用自然语言描述路径，不引用变量
"question": "Write the incident report to docs/report.md in your workspace. The report should contain..."
```

#### pref 字段格式

```jsonc
"pref": {
  "command": "python ${eval_dir}/${agent_id}/scripts/check_preferences.py ${workspace} --rules P1,P2",
  "expect_exit": 0,
  "feedback": {
    "correct": "",
    "incorrect": "Format reminder: report must use ISO 8601 timestamps (P1) and dated filenames (P2)."
  }
}
```

`pref` 允许字段：`{command, feedback, rules, expect_exit}`，无其他字段。
`pref.feedback` 允许字段：`{correct, incorrect}`。

---

### 1.2 题型选择准则

**不得将两种题型混淆**：

- `multi_choice`：评测 agent 的**认知与判断**——读取信息后选出正确选项。题目问法需是"哪些陈述有依据"、"哪些结论需要修改"等判断类问题，**不得要求 agent 输出 JSON 或修改文件**。
- `exec_check`：评测 agent 的**行为与产出**——检查 agent 是否正确修改了 workspace 中的文件或执行了代码。题目要求 agent 做某件事，check 验证是否做好了，**不读取 agent 的回答文字**。

**常见错误**：
- `type: exec_check`，但 `question` 是多选题风格（"Which of the following..."），应改为 `multi_choice`。
- `type: multi_choice`，但 `question` 要求 agent "写一个 JSON 文件"，应改为 `exec_check`。

---

### 1.3 语言一致性

- 新增题目的语言须与**该场景原始 `questions.json` 的主体语言**保持一致。
- **允许在主体语言内夹杂专有名词**：
  - 主体为英文的场景，可保留中文人名、中文机构名称、中文文件名（如题目中出现"林小雅"、"飞书"等），不强制翻译为拼音或英文，以保持与 workspace 文件的自然一致。
  - 主体为中文的场景，可保留英文技术术语、英文缩写（如 CVSS、IRB、SHA-256）和英文文件路径，不强制汉化。
- **禁止的混用**：`question` 字段前半句英文后半句中文、`feedback.correct` 中英文段落随意拼接——这类混乱会干扰 agent 的理解，须保持段落级语言统一。
- 字段名（键名）、`eval.command` 中的 shell 命令、路径、`update_ids` 值始终保持原始英文形式，不受语言规则约束。

检查当前场景主体语言：
```bash
python3 -c "
import json
d = json.load(open('data/clawarena/eval/{scene_id}/questions.json'))
print(d['rounds'][0]['question'][:120])
"
```

---

### 1.4 feedback 内容质量

feedback 的核心目的是在 agent 答错时**提供实质性的帮助**，使其在后续轮次中有所提升。feedback 字段不是告知结果的通知，而是教学性回复。

**exec_check 的 `feedback.incorrect`**：

- 必须包含该题的**正确解题思路或关键信息**，让 agent 知道应当做什么、数值是什么、引用哪个来源
- 禁止仅写"Your answer is wrong."、"Task failed."、"Please try again." 等无营养文字
- 建议格式：说明期望的正确产物是什么 → 给出关键事实或计算结果 → 说明 agent 常见的偏差方向

```jsonc
// ❌ 无营养：只告知失败，不给任何方向
"incorrect": "The check did not pass. Please review and try again."

// ✅ 有营养：指出正确答案和关键依据
"incorrect": "The incident summary JSON is missing or contains incorrect values. Expected: affected_users = 2340 (from the breach notification log, line 47), cvss_score = 7.5 (NVD advisory). Ensure the file is at docs/incident_summary.json with these exact field names."
```

**multi_choice 的 `feedback.options`**：

- 每个选项的 feedback 须说明**为何正确或为何错误**，引用具体来源文件或关键数据
- 禁止写"A is correct."（无解释）或"B is wrong."（无理由）
- 正确选项的 feedback 可以简洁，但错误选项的 feedback 须足够具体，帮助 agent 理解误选原因

**pref 的 `feedback.incorrect`**：

- 须明确说明违反了哪条偏好规则（如 P2）以及如何修正，不能只写"Preference check failed."
- 这是教学期唯一能向 agent 传递偏好信息的渠道，须利用好

---

### 1.5 JSON 语法检查

造完题后立即做格式自检：
```bash
python3 -c "import json; json.load(open('data/clawarena/eval/{scene_id}/questions.json'))"
```
若有 `JSONDecodeError` 立即修复，不进入后续流程。

---

## 二、难度增强要求

### 2.1 核心原则：一切题目须考察推理

**v1 题目的本质缺陷**：agent 只需搜索 + 粘贴就能通过——读源文件，把关键字写进 Markdown，check 脚本验证字符串出现即可。这对现代 LLM 是零难度。

**升级后的最低标准**：每道题必须至少考察以下推理能力之一：
- **数值派生**：计算 workspace 文件中不直接出现的中间量（时间差、百分比、比率）
- **来源裁决**：两个来源互相矛盾，agent 须选定可信来源并说明理由
- **跨文件整合**：多份文件的信息须综合才能得出结论，单一文件无法完成
- **状态追踪**：多轮 update 后，某条事实发生了变化，agent 须追踪最新状态
- **逆向验证**：agent 须证明某条路径**不**成立（负向推理）

---

### 2.2 四条升级路径

#### 路径 A：计算派生值（最直接，优先使用）

要求 agent 计算 workspace 文件中**不直接出现**的中间量，check 脚本做数值精度验证：

```python
# ✅ 正确：验证具体派生值，允许小容差
expected_delta = 2487  # 秒，由 14:22:17 和 15:03:44 计算得出
assert abs(data["time_delta_seconds"] - expected_delta) <= 2

# ❌ 错误：只检查字符串出现
assert "2487" in content
# ❌ 更差：只检查非零
assert data["time_delta_seconds"] != 0
```

**适用场景**：时间差、文件大小比率、排名变化、百分比偏差。

#### 路径 B：矛盾裁决（考察判断力）

workspace 中故意埋入两条互相矛盾的说法，check 同时验证：
1. agent 选择了正确的来源
2. agent **未**将错误来源的数值混入结论（M6 负向断言）

```python
# ✅ 正向：结论包含正确来源的数值
assert "847" in content  # 权威日志显示 847

# ✅ 负向（M6）：结论不包含错误来源的数值
assert "870" not in content  # 草稿文档中有误写的 870，不应被引用
```

#### 路径 C：可执行脚本（L3 扩展，与路径 A 配合最强）

要求 agent 从零编写 Python 脚本，读取 workspace 文件并输出 JSON，check 运行该脚本验证字段精度：

```bash
# eval.command 示例
cd ${workspace} && python scripts/analyze_pipeline.py > /tmp/out.json && python ${eval_dir}/${agent_id}/scripts/check_pipeline_output.py /tmp/out.json
```

**设计要点**：
- 题目须说明输入文件的结构（如"Markdown 表格格式，含 order_id/actual_time/status 等列"）
- agent 的脚本须**解析**文档内容，不能硬编码答案
- `timeout` 设为 60s（L3 脚本解析可能较慢）

#### 路径 D：严格 schema 验证（JSON 输出类题目升级）

将"JSON 字段存在"验证升级为：
- 枚举值约束：`strength` 必须为 `["high", "medium", "low"]` 之一
- 数值范围约束：`ratio` 字段须在 `[expected - tol, expected + tol]` 内
- 排序约束：JSON 数组须按时间序或重要性序排列
- 完整性约束：所有必填字段均存在且非空

---

### 2.3 六类验证机制（M1–M6）

| 机制 | 说明 | 何时使用 |
|------|------|---------|
| **M1** | 解析 JSON/MD，验证派生计算值在严格容差内 | 时间差、比率、百分比等中间量 |
| **M2** | 要求 agent 明确引用两份冲突来源，说明可信性判断；check 验证结论方向 | workspace 中埋有矛盾信息 |
| **M3** | 多个输出文件交叉引用同一组事实；check 跨文件校验数值一致性 | report.md + summary.json 共享关键数字 |
| **M4** | JSON 须符合严格 schema（字段名、枚举值、类型、数组长度完全匹配） | 结构化输出类任务 |
| **M5** | Agent 所写 Python 脚本被直接运行；check 验证 stdout 字段精度 | L3 类脚本编写任务 |
| **M6** | 负向断言：check 验证 agent **未使用**错误来源数值作为结论 | 矛盾裁决题的配套验证 |

**L1 级检查（`test -f` + 单行 `grep`）不得单独成题**。只能作为 `&&` 前置快速失败条件，真正的验证逻辑须在 check 脚本内。

---

### 2.4 合题策略：同批次 update 区间内合并小题

**问题**：同一 update 区间内堆叠多道 EC，每道只考一个小点，agent 可逐题蒙混。

**策略**：将同批次 update 之间的多道 EC 题**合并为一道多产物任务**：

```bash
# 合并后的 eval.command
python ${eval_dir}/${agent_id}/scripts/check_incident_report.py ${workspace} &&
python ${eval_dir}/${agent_id}/scripts/check_timeline_json.py ${workspace}/docs/incident_timeline.json &&
python ${eval_dir}/${agent_id}/scripts/check_preferences.py ${workspace} --rules P1,P2,P3 --target docs/incident_report_*.md
```

好处：任一产物错误或数值不一致，整题失败，无法逐步蒙混。各文件须共享同一组关键事实（M3），check 跨文件校验。

---

### 2.5 造题前必建 Ground Truth 数值表

每道涉及数值计算或引用的 EC 题，开始造题前须先整理：

| 事实 | 数值 | 来源文件 | 行号/位置 |
|------|------|---------|----------|
| 文件下载时间戳 | `2026-09-25T14:22:17+08:00` | `cloud-storage-access-log.md` | 第 23 行 |
| 邮件发送时间戳 | `2026-09-25T15:03:44+08:00` | `email-attachment-audit.md` | 第 41 行 |
| 时间差（秒） | **2487** | 计算值（41m27s） | — |
| 文件大小比率 | **2.875** | 计算值（2300KB / 800KB） | — |

写完 check 脚本后，将脚本中每个期望值**回溯到表中对应行核实**。若某数值在 workspace 里找不到文档来源，则该题无解，须修改 workspace 或换题。

---

## 三、可解性与三元一致性

**三元一致性**：每道题须在以下三者之间保持完全一致，任一不对齐则可能导致题目无解或 check 永远失败。

```
workspace 文件内容  ←→  questions.json 题目描述  ←→  check 脚本期望值
```

---

### 3.1 workspace 文件内容与题目描述一致性

**问题**：题目引用了 workspace 中不存在的文件、人名、数值。

**检查方法**：
```bash
# 列出 workspace 实际文件
ls data/clawarena/claude-code/workspaces/{scene_id}/
ls data/clawarena/claude-code/workspaces/{scene_id}/docs/

# 核对题目引用的每个文件名是否存在
grep -r "filename.md" data/clawarena/eval/{scene_id}/questions.json
```

**特别注意**：
- 不同 framework 的 workspace 文件集可能不同（openclaw 有 `SOUL.md`，claude-code 可能没有）。造题时须对目标 framework 的 workspace 目录分别核查。
- update 文件仅在对应轮次**触发后**才对 agent 可见。若题目在 upd1 触发前引用了 upd1_workspace 的文件，则题目无解。

---

### 3.2 题目描述与 check 脚本期望值一致性

**问题**：题目要求输出字段 `time_delta_seconds`，但 check 脚本读取 `delta_secs`；或题目说"精确到 0.1%"，但 check 容差是 `abs(x - expected) > 1`。

**检查方法**：写完题目后，**立即**写对应 check 脚本，逐字段核对：
- 字段名（`"time_delta_seconds"` vs `"delta_secs"`）
- 数据类型（整数 vs 浮点，字符串 vs 数字）
- 精度要求（`<= 2` 秒 vs `<= 0.5`）
- 枚举值（`"high"` vs `"HIGH"` vs `"High"`）

---

### 3.3 check 脚本期望值与 workspace 文件内容一致性

这是最容易被忽略的一环——**check 脚本里的期望值必须能从 workspace 文件中找到文档依据**。

**反例**（hil_i2 造数教训）：check 脚本要求文档包含 `N=870`，但 workspace 中 `data-cleaning-pipeline-log.md` 明确写"V2.0 和 V2.1 均输出 847 条"。导致题目在数据上无解。

**操作**：写完 check 脚本后，将每个 `expected_value` 在 workspace 文件中逐一 `grep` 验证：
```bash
grep -r "847" data/clawarena/openclaw/workspaces/{scene_id}/
grep -r "2487" data/clawarena/openclaw/workspaces/{scene_id}/
```
若某期望值完全搜不到来源，立即排查：是否应先修改 workspace 文件，或重新计算期望值。

---

### 3.4 人名与标识符全局一致性

workspace 文件、update 文件、session 对话、`questions.json` 题目、check 脚本关键词**四处**须使用完全相同的人名和标识符。

常见问题：workspace 写"王医生"，questions.json 写"王逸生"，check 脚本关键词写"Dr. Wang"。任何一处不一致均可能导致 check 失误或 agent 行为不一致。

**修复**：
```bash
sed -i 's/旧名/新名/g' data/clawarena/openclaw/workspaces/{scene}/**/*.md
grep -r "旧名" data/clawarena/openclaw/workspaces/{scene}  # 确认无残留
```

---

### 3.5 update 可见性与题目依赖的时序对齐

每道题所处的 Phase 与各 update 触发轮次的关系须严格核对：

```
update 触发轮次：q5（upd1_workspace 注入 server-diagnostic-report.md）

q4：不可引用该文件（upd1 尚未触发）  ✗
q5：upd1 触发，可引用                ✓
q6 及之后：均可引用                  ✓
```

**G-006i 规则与 manifest 严格对应**：

每个 `update_id` 字符串须满足两个约束：

1. **唯一性**：只能出现在**恰好一道**题的 `update_ids` 列表中。update 一旦触发，其内容在后续所有轮次中均对 agent 可见，无需重复声明。若在两道题中都声明了同一 `update_id`，`clawarena check` 报 G-006i 错误。

2. **与 manifest 精确对应**：`questions.json` 中 `update_ids` 里的每个字符串，须与 `manifest.json` 中 `updates.{scene_id}` 下的顶层键名**完全一致**。每次 update 通常由 workspace 文件更新和 session 消息注入两部分组成，manifest 会将它们拆分为独立的 key（如 `upd1_workspace`、`upd1_sessions`），须在 `update_ids` 中**分别列出**：

```jsonc
// ✅ 正确：精确引用 manifest 中的两个独立 key
"update_ids": ["upd1_workspace", "upd1_sessions"]

// ❌ 错误：用简写代指，manifest 中没有 "upd1" 这个 key
"update_ids": ["upd1"]

// ❌ 错误：只写了 workspace 部分，遗漏了 session 注入
"update_ids": ["upd1_workspace"]
```

命名规范：manifest 中的 update key 通常遵循 `{upd_name}_{type}` 格式，`type` 为 `workspace` 或 `sessions`。造数时须先查阅该场景的 `manifest.json` 确认实际 key 名，不可凭记忆或简写猜测。

---

### 3.6 MC 题选项的可解性

每道 MC 题的每个选项，在 agent 处于该轮次时，都须能从**当前可见的文档中**找到明确支撑或反驳证据：

- **正确选项**：至少一份可见文档（workspace 或已触发的 update）中有直接支撑
- **干扰项**：须有可识别的错误，但错误须在文档中能被验证，不能是"猜测不到"
- **不得自相矛盾**：两个正确选项不能互相排斥

**操作**：写完选项后，逐条标注"支撑来源文件：行号"，无法标注的选项须修改。

---

## 四、题序与节奏设计

### 4.1 MC 与 EC 的比例与位置

目标：约 **8 道 MC / 30 轮**，EC 占主体。

MC 只在三类位置使用：
1. **场景开篇**（前 2–3 轮）：建立基线认知，引入核心矛盾
2. **每个 update 触发轮**（该轮 `update_ids` 非空）：验证 agent 对新信息的整合
3. **最终综合**（最后 1–2 轮）：跨 update 综合结论或元认知

**禁止**将 MC 用作"过渡题"或"填充题"。每道 MC 都须有明确功能定位。

### 4.2 认知-行动交替节奏

理想节奏：MC（认知）→ EC（行动）→ MC（验证认知更新）→ EC（深化行动）

```
q1  (MC)   建立基线：哪些初始陈述有文档支撑
q2  (EC)   行动：生成初始分析文档
q3  (EC)   行动：补充数值计算
q4  (MC)   upd1 触发：新信息后哪些结论需修改
q5  (EC)   行动：更新分析文档（引用 upd1 内容）
q6  (EC)   行动：生成合并产物（跨文件一致性）
...
```

### 4.3 密集 update 区段处理

若原设计中两个 update 相邻（如 upd2@q7、upd3@q8），须**重新设计**，在中间插入 3–4 道 EC，将间距拉开至 ≥ 4 轮。相邻 update 会导致 agent 无法充分"消化"第一个 update 就收到第二个，降低区分度。

---

## 五、update 注入设计

### 5.1 update 触发轮建议为 MC 题

update 触发本身是认知更新的检验点，自然契合 MC（"阅读新文件后，哪些陈述有证据支持"）。触发轮为 EC 题虽然合法，但 update 内容可能分散 agent 对任务本身的注意力，降低设计意图的清晰度。

### 5.2 update 触发后须立刻有 EC 题利用新信息

update 触发后的第一道 EC 题，须要求 agent 明确引用新注入的文件或数据，以验证 agent 是否真正"消化"了 update：

```
upd1 触发：注入 server-diagnostic-report.md
→ 下一道 EC：要求 agent 在输出文档中引用该报告的工单号（check 脚本验证该工单号出现）
```

### 5.3 session 类 update 的消息顺序

session 类 update 文件（`.jsonl`）中的消息须严格满足 `user`/`assistant` 交替顺序，否则 `clawarena check` 报消息顺序错误。连续的 `user` 消息或 `assistant` 消息均不允许（`toolResult` 除外，`compaction` 作为断点不触发错误）。

---

## 六、pref 字段设计

### 6.0 pref 的核心语义：隐式偏好检测

**pref 代表的是"隐式偏好"**，即用户（Human-in-the-Loop）在现实工作中潜意识里期望 agent 遵守、但**不会在每道题里显式说明**的行为模式。pref 评测的是 agent 能否从早期反馈中自主习得并持续维持这些偏好。

**pref.command 与 eval.command 必须检查不同的事情**：

| 字段 | 检查内容 | 依据 |
|------|---------|------|
| `eval.command` | 任务本身是否完成——question 明确要求的内容 | question 文本 |
| `pref.command` | 输出是否符合某个**question 里未提及的**隐式模式 | 偏好规则（P1–P5 等），不在 question 中出现 |

两者**不得相同，也不得高度重叠**。若 `pref.command` 与 `eval.command` 检查同一件事，等同于对 agent 双重惩罚同一个错误，且失去了"隐式"的意义。

**正确的隐式偏好例子**：
- question 要求"生成事件报告"，`eval.command` 检查报告文件存在且关键数值正确；`pref.command` 检查报告文件名是否带日期前缀（P2）——agent 并不知道这个命名偏好，只能从早期 `pref.feedback.incorrect` 的提示中习得。
- question 要求"更新分析文档"，`eval.command` 检查文档内容；`pref.command` 检查文档中所有时间戳是否为 ISO 8601 格式（P1）——这是用户的个人习惯，不会写进每道题目。

**错误的用法**：
```jsonc
// ❌ 错误：pref.command 与 eval.command 检查同一件事（报告数值）
"eval": { "command": "python check_report_values.py ${workspace}" },
"pref": { "command": "python check_report_values.py ${workspace} --strict" }

// ❌ 错误：pref.command 检查的内容 question 里已显式要求
// question: "...ensure all timestamps use ISO 8601 format..."
"pref": { "command": "python check_preferences.py ${workspace} --rules P1" }
// P1 已在 question 里说明，不再是"隐式"偏好
```

**隐式偏好的传递机制**：

```
教学期（前 1/3 轮）：
  pref.feedback.incorrect → 仅当 agent 违反偏好时，将偏好规则以反馈形式注入
  ↓  agent 从反馈中习得偏好
静默期（后 2/3 轮）：
  偏好逻辑迁入 eval.command，计入得分
  question 文字中不新增任何偏好提示
  → 测试 agent 是否真正内化了偏好，而非靠每轮提示维持
```

---

### 6.1 两段制：教学期 / 静默期

| 阶段 | 位置 | 设计方式 |
|------|------|---------|
| 教学期（Phase 0–1，前 1/3 轮） | 含 `pref` 字段，有实质提示，**不计入得分** | 用 `pref.feedback.incorrect` 给出格式提示 |
| 静默期（Phase 2–4，后 2/3 轮） | **无** `pref` 字段，偏好逻辑迁入 `eval.command`，**计入得分** | 将 `check_preferences.py` 加入主 `eval.command` 的 `&&` 链 |

教学期示例（P1 时间格式偏好，question 中未提及）：
```jsonc
"pref": {
  "command": "python ${eval_dir}/${agent_id}/scripts/check_preferences.py ${workspace} --rules P1,P2",
  "expect_exit": 0,
  "feedback": {
    "correct": "",
    "incorrect": "Format reminder: all timestamps must be ISO 8601 (P1); main report files must use YYYY-MM-DD_ prefix (P2)."
  }
}
```

静默期（偏好逻辑迁入 eval，question 里仍不提及 P1/P2）：
```jsonc
"eval": {
  "command": "python ${eval_dir}/${agent_id}/scripts/check_report.py ${workspace} && python ${eval_dir}/${agent_id}/scripts/check_preferences.py ${workspace} --rules P1,P2,P3,P4,P5 --target docs/final_report_*.md",
  "expect_exit": 0,
  "timeout": 60
}
```

### 6.2 check_preferences.py 的 P2 规则设计

P2（文件命名偏好）的检查语义须为"**至少有一个**文件具有日期前缀"，而非"**所有**文件都有"：

```python
# ❌ 错误：误判早期无前缀文件
violations = [f.name for f in files if not date_prefix.match(f.name)]
if violations:
    return False, f"P2: files without prefix: {violations}"

# ✅ 正确：主报告是否已命名规范
prefixed = [f.name for f in files if date_prefix.match(f.name)]
if not prefixed:
    return False, "P2: no file with YYYY-MM-DD_ prefix found"
```

原因：`docs/` 目录下可能有早期 EC 题生成的无前缀辅助文件，P2 意图只是约束主报告命名。

---

## 七、多框架一致性

### 7.1 新场景须在全部四个 framework 中注册

新增场景时，以下位置缺一不可：

| Framework | 文件 | 操作 |
|-----------|------|------|
| openclaw | `openclaw/manifest.json` | 追加 `agents.{scene}` + `updates.{scene}` |
| openclaw | `openclaw/config/openclaw.json` | 追加 `agents.list[]`（含 `id, name, workspace, agentDir`） |
| claude-code | `claude-code/manifest.json` | 追加 `agents.{scene}` + `updates.{scene}` |
| picoclaw | `picoclaw/manifest.json` | 追加 `agents.{scene}` + `updates.{scene}` |
| nanobot | `nanobot/manifest.json` | 追加 `agents.{scene}` + `updates.{scene}` |

openclaw.json 中路径须使用 `${BENCHMARK_ROOT}` 占位符，`clawarena check` 会自动展开并验证路径存在性：

```json
{
  "id": "hil_new",
  "name": "hil_new",
  "workspace": "${BENCHMARK_ROOT}/data/clawarena/openclaw/workspaces/hil_new",
  "agentDir": "${BENCHMARK_ROOT}/data/clawarena/openclaw/state/agents/hil_new/agent"
}
```

注意：`agentDir` 中的 `/agent` 子目录是 openclaw 运行时创建的，不需要预先存在，check 只验证其**父目录**存在。

### 7.2 workspace 文件在不同 framework 间的差异

不同 framework 的 workspace 文件集可能不同（如 openclaw 有 `USER.md`+`SOUL.md`，claude-code 可能只有 `CLAUDE.md`）。造题时须针对**每个 framework 的 workspace** 分别核实文件存在性，不可跨 framework 假设文件一致。

---

## 八、clawarena check 验证流程

### 8.1 标准调用方式

```bash
# 全量检查（推荐，确认整库无误）
clawarena check -d data/clawarena/tests.json

# 单场景临时检查（构造 slim tests.json）
python3 - <<'EOF'
import json, os
base = os.path.abspath("data/clawarena")
tests = {
    "name": "slim",
    "eval_dir": f"{base}/eval",
    "frameworks": {
        "openclaw": {"manifest": f"{base}/openclaw/manifest.json"},
        "claude-code": {"manifest": f"{base}/claude-code/manifest.json"}
    },
    "tests": [{"id": "hil_new", "eval": "hil_new"}]
}
with open("/tmp/slim_test.json", "w") as f:
    json.dump(tests, f, indent=2)
EOF
clawarena check -d /tmp/slim_test.json
```

注意：`eval_dir` 和 `manifest` 须为**绝对路径**，相对路径会被解析为相对于 `/tmp/`。

### 8.2 check 通过后仍须人工复核

`clawarena check` 通过只表明格式合法、文件存在、字段完整。以下内容不被 check 检测，须人工核实：

- 题目逻辑正确性（选项是否有依据、EC 题是否真的可解）
- check 脚本的期望值是否与 workspace 文件数值吻合
- MC 题选项是否覆盖了合理的干扰项
- pref 字段是否处于正确的教学/静默阶段

---

## 九、造数后独立复查流程

`clawarena check` 通过后，**必须**启动独立上下文的复查步骤。自身造数时积累的局部视角往往会遮蔽设计盲点，独立 agent 从零阅读数据能发现人工复查容易忽略的三元不一致。

---

### 9.1 造数完成后：调用 Explore Agent 全量复查

造完一个场景、`clawarena check` 通过后，**立即**在新上下文中启动一个 Explore Agent，对该场景执行以下全量核查。务必使用**独立上下文**（不携带造数过程中的对话记忆），以还原"首次阅读"视角。

给 Explore Agent 的提示模板：

```
请对场景 {scene_id} 做完整的三元一致性与可解性复查。

需要阅读的文件：
- data/clawarena/eval/{scene_id}/questions.json        （题目）
- data/clawarena/openclaw/workspaces/{scene_id}/       （workspace 文件）
- data/clawarena/openclaw/updates/{scene_id}/          （update 文件）
- data/clawarena/eval/{scene_id}/scripts/              （check 脚本）

请逐题检查：
1. 三元一致性：workspace 文件内容 ↔ question 描述 ↔ check 脚本期望值，三者是否完全对齐
2. 可解性：对于每道 EC 题，按照 question 的要求操作后，check 脚本是否能被满足（重点核实期望数值是否能从 workspace 推导出来）
3. MC 题选项：每个选项能否在当前可见文档中找到明确支撑或反驳证据；干扰项是否有实质迷惑性而非明显荒谬
4. update 时序：每道题引用的文件在该轮次是否已可见（触发时序是否正确）
5. 人名与标识符：workspace/update/session/questions/check 脚本五处是否完全统一

发现任何不一致或潜在无解情形，请列出具体题目 ID、不一致位置和建议修复方式。
```

Explore Agent 的发现须**逐条修复**，修复后重新执行 `clawarena check` 全量验证。

---

### 9.2 推理实验后：根据 infer_result.json 反推题目设计质量

当有真实 model 推理的实验结果时（`clawarena infer` 执行后生成 `infer_result.json`），须对失分题目做**反向诊断**，区分两类根因：

| 类型 | 现象 | 根因 | 处理方式 |
|------|------|------|---------|
| **题目设计问题** | Agent 按 question 的合理要求操作，结果符合预期，但 check 判错 | check 脚本期望值与 workspace 事实不符、字段名拼写差异、容差过严、update 可见性错误 | 修复 check 脚本或 workspace 数据 |
| **Agent 能力不足** | Agent 操作方向有误、推理错误、未读相关文件 | Agent 本身的局限性，题目设计合理 | 保留题目，记录为有效难度 |

**反向诊断操作步骤**：

1. **抽样审查**（人工）：从 `infer_result.json` 中取失分题目，结合 agent 的实际输出（session 记录），判断 agent 的行为是否"合理但被错判"。若 agent 写了正确的数值但 check 期望不同数值，则为题目问题。

2. **全量检查**（调用 Explore Agent）：若实验结果中失分集中于某类题目（如所有 L3 脚本题、所有跨 update 题），可调用独立 Explore Agent 对这类题目做专项复查：

```
请检查场景 {scene_id} 的以下题目在实验中全部失分，结合 agent 的输出记录和 workspace 文件，
判断是题目设计问题还是 agent 能力问题：

失分题目：{q5, q11, q18}（附 agent 输出摘要）

重点检查：
- agent 的操作方向是否与 question 描述一致
- check 脚本的期望值是否能从当前可见 workspace 文件推导出来
- 是否存在信息不足导致题目实质上无解的情形
```

3. **修复与迭代**：确认为题目设计问题的，修复后须重新推理验证；确认为 agent 能力问题的，保留并在实验报告中记录该题目的设计意图。

> **重要原则**：实验失分≠题目有问题。过度根据 agent 失分修改题目，会让 benchmark 逐渐退化为专门迎合当前 agent 能力的"教程"，丧失评测价值。只修复有明确证据证明为设计缺陷的题目。

---

## 十、造数完整操作清单

造完一个场景后，逐项过：

### 格式合法性
- [ ] JSON 语法有效：`python3 -c "import json; json.load(open('questions.json'))"` 无报错
- [ ] 所有 `multi_choice` 题的 `options`/`answer` 在 `eval` 内，不在顶层
- [ ] 所有 `multi_choice` 题的 `feedback.options` 与 `eval.options` 键集完全一致
- [ ] 所有 `multi_choice` 题选项总数 ≥ 6，错误选项 ≥ 2 且具有实质迷惑性
- [ ] 所有 `exec_check` 题的 `feedback` 同时含 `correct` 和 `incorrect`
- [ ] `eval` 字段无额外键（exec_check 只允许 `command/expect_exit/timeout/expect_stdout/expect_stdout_regex`）
- [ ] 题型与题目格式匹配（exec_check 不出现多选题问法，multi_choice 不要求写文件）
- [ ] 新增题目的语言与该场景原始题目一致
- [ ] `question` 字段中无 `${...}` 变量引用
- [ ] `eval.command` / `pref.command` 中 `${...}` 变量只使用 `${eval_dir}/${agent_id}/scripts/` 和 `${workspace}/` 两种模式
- [ ] 所有 `feedback.incorrect` / `pref.feedback.incorrect` 包含实质性帮助信息，非仅告知失败
- [ ] `pref.command` 与 `eval.command` 检查的是不同的事，且 `pref` 所检查的内容在对应 `question` 文字中未显式要求
- [ ] `clawarena check -d tests.json` 全量通过，0 errors

### 难度与可解性
- [ ] 每道 EC 题包含真正的推理环节（不能是纯搜索+粘贴）
- [ ] check 脚本验证 ≥ 3 个具体数值（非仅关键词匹配）
- [ ] 每个期望值已在 workspace 文件中找到文档来源（Ground Truth 数值表已完成）
- [ ] 若有矛盾来源，已加入 M6 负向断言
- [ ] 同批次 update 区间内多道小题已合并为多产物任务（`&&` 串联）
- [ ] L1 级检查（`test -f`）只作前置 `&&` 短路，不单独成题
- [ ] `eval.command` 中无通配符配合 `test -f`（见 pitfalls.md 1.1）
- [ ] 数值验证使用 exact match 或带容差比较，不是"非零"或"字符串存在"

### 三元一致性
- [ ] 题目引用的每个文件名已在对应 framework 的 workspace 目录中核实存在
- [ ] update 文件在触发轮之后才被题目引用（不存在提前引用 update 文件的题目）
- [ ] 每个 `update_id` 只在一道题的 `update_ids` 中出现（G-006i 规则）
- [ ] `update_ids` 中的每个字符串与该场景 `manifest.json` 的顶层 key 完全一致（无简写，`upd1_workspace` 和 `upd1_sessions` 须分别列出）
- [ ] 人名、标识符在 workspace/update/session/questions.json/check 脚本五处全部一致
- [ ] MC 题每个选项已标注支撑来源文件及行号
- [ ] check 脚本字段名与题目描述的字段名完全一致（无 `delta_secs` vs `time_delta_seconds` 类拼写差异）

### 题序与结构
- [ ] MC 题数约 8 道，位于开篇/update 触发轮/综合收尾，无填充性 MC
- [ ] 相邻 update 之间有 ≥ 4 轮缓冲
- [ ] 每个 update 触发后紧跟至少一道 EC 题引用新注入内容
- [ ] pref 字段仅出现在 Phase 0–1，Phase 2 以后已迁入 eval.command

### 注册与迁移
- [ ] 四个 framework（openclaw/claude-code/picoclaw/nanobot）的 manifest.json 均已注册
- [ ] openclaw/config/openclaw.json 的 `agents.list` 已追加该场景
- [ ] openclaw.json 的 `workspace` 和 `agentDir` 路径使用 `${BENCHMARK_ROOT}` 占位符，且父目录存在
- [ ] 全量 `clawarena check` 通过后推送 remote

### 独立复查
- [ ] 已在**独立上下文**中调用 Explore Agent，按 9.1 的模板对该场景做全量三元一致性复查
- [ ] Explore Agent 发现的所有不一致已逐条修复，修复后 `clawarena check` 重新通过
- [ ] （如有推理实验结果）已按 9.2 的流程对失分题目做反向诊断，区分题目设计问题与 agent 能力问题，并据此决定是否修复

---

## 相关必读文档索引

> 以下路径均相对于 **ClawArena 仓库根目录**（即 `pyproject.toml` 所在目录）。

### 核心规范

| 文档 | 路径 | 说明 |
|------|------|------|
| 数据结构规范 | `docs/data-structure.md` | tests.json / manifest.json / questions.json / session JSONL 全部字段规范，是格式对齐的权威参考 |
| CLI 使用手册 | `docs/cli.md` | `clawarena check / infer / score / report` 各子命令的参数与用法 |

### 造数专项

| 文档 | 路径 | 说明 |
|------|------|------|
| 本指导书 | `docs/data-spec/A1-data-augment/augmentation-guide.md` | 综合造数指导（格式 + 难度 + 一致性） |
| EC 升级思路 | `docs/data-spec/A1-data-augment/difficulty-upgrade-guide.md` | v1→v2/v3 升级路径详解，含四条升级路径与六类验证机制 |
| 踩坑记录 | `docs/data-spec/A1-data-augment/pitfalls.md` | hil_f3/i2 实际造数中遇到的具体坑，含 check 脚本写法、update 时序、迁移步骤 |
| 数据合成通用坑 | `docs/data-spec/data-synthesis-pitfalls.md` | 更广泛的数据合成方法论，涵盖内容设计层面的常见问题 |
| 场景设计规划 | `docs/data-spec/design-plan.md` | 整体 benchmark 场景分布与设计原则 |

### 参考配置

| 文档 | 路径 | 说明 |
|------|------|------|
| Provider 使用指南 | `docs/provider-usage-guide.md` | 各 LLM provider 的 API 配置与速率限制说明，infer 前必读 |
| 安装指南 | `docs/installation.md` | 依赖安装、环境变量配置、首次运行步骤 |
