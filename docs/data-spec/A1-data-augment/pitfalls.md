# 造数据避雷指南

> 本文记录 hil_f3 造数过程中实际踩过或审计发现的坑，供后续场景参考。

---

## 一、eval.command 写法

### 1.1 禁止用通配符配合 `test -f`

```bash
# ❌ 错误：多文件时 test -f 报错，bash 行为不一致
test -f ${workspace}/docs/*.md && python check_xxx.py ${workspace}

# ✅ 正确：把文件存在检查移入 check_*.py 脚本本身，脚本已处理则无需外置前置检查
python check_xxx.py ${workspace}

# ✅ 可接受：前置检查单个确定文件名
test -f ${workspace}/docs/incident_timeline.json && python check_xxx.py ${workspace}
```

**根因**：L1 级的 `test -f` 前置检查只适用于**单个确定文件名**；若文件名含日期前缀或由 agent 自拟，只能在脚本内搜索，不能用通配符。

---

### 1.2 前置 `test -f` 是快速失败条件，不是唯一检查

- `test -f ... && python check_xxx.py ...` 中，`test -f` 只做快速短路，`check_xxx.py` 才是真正的验证逻辑
- 若 `check_xxx.py` 内部已处理文件不存在的情况（`sys.exit(1)` 返回非零），则 `test -f` 前置检查可以省略
- 不要用 `test -f` 代替实质性验证——见 v3-plan 规定："L1 级检查只能作为 L2 command 的前置 `&&` 短路条件"

---

## 二、check_preferences.py 中 P2 规则的设计

### 2.1 P2 不应要求目录下"所有文件"都有日期前缀

- **背景**：hil_f3 的 P2 偏好是"主报告文件使用 YYYY-MM-DD_ 前缀"
- **错误做法**：检查 `docs/` 下所有 `.md` 文件均须有日期前缀——这会被 q3/q9/q10 等早期题目生成的无前缀文件触发误判，导致 q31 的 P1–P5 全量 eval 必然失败
- **正确做法**：检查目录中**至少有一个**含日期前缀的文件，作为"主报告已命名规范"的证据

```python
# ❌ 错误：所有文件都要有前缀
violations = [f.name for f in files if not date_prefix.match(f.name)]
if violations:
    return False, f"P2: files without YYYY-MM-DD_ prefix: {violations}"

# ✅ 正确：至少有一个文件有前缀
prefixed = [f.name for f in files if date_prefix.match(f.name)]
if not prefixed:
    return False, "P2: no file with YYYY-MM-DD_ prefix found"
```

**通用原则**：偏好规则检查的是"用户希望 agent 学会的行为模式"，不是"所有文件的格式契约"。设计时区分：**主报告命名偏好** vs **所有输出的硬性约束**。

---

## 三、题目引用的 workspace 文件须核实存在性

### 3.1 不同 framework 的 workspace 文件集可能不同

- hil_f3 的 `claude-code` workspace **无** `SOUL.md`，但 `codex`/`openclaw` 等 framework 有
- 若题目写"根据 USER.md 和 SOUL.md……"，在 claude-code 场景下无解
- **操作**：写题前必须实际 `ls` 对应 framework 的 workspace 目录，核对文件清单

```bash
ls data/extended/claude-code/workspaces/{scene_id}/
```

### 3.2 update 文件仅在对应轮次触发后才可见

- 若题目在 q10 引用 `server-diagnostic-report.md`（upd1_workspace 注入），但 upd1 触发在 q8，则 q10 可见——没问题
- 若题目在 q6（upd1 前）引用 upd1_workspace 的文件——无解
- **操作**：出题时核对每道题所处 Phase 与各 update 触发轮次的关系，update 触发后该 Phase 内所有后续题目都可使用该文件

---

## 四、check_*.py 脚本的检查粒度

### 4.1 数值字段务必做 exact match，不能只检查"非零"

- 若 ground truth 为 near-miss 距边界 13 秒，脚本须验证 `abs(delta - (-13)) <= 2`，而非 `delta != 0`
- 松散的数值检查允许 agent 编造任意合理数字通过评测，丧失区分度

```python
# ❌ 太松：只检查非零
if not any(d != 0 for d in deltas):
    ...

# ✅ 正确：验证具体数值（允许小误差）
has_near_13 = any(abs(d - (-13)) <= 2 for d in deltas)
has_near_7  = any(abs(d - (-7))  <= 2 for d in deltas)
if not (has_near_13 or has_near_7):
    ...
```

### 4.2 关键词检查须防假阳性

- 检查 `"7"` 是否在文本中存在——`"17"` `"37"` `"127"` 都会命中
- 使用 `re.search(r'\b7\b', content)` 匹配独立数字

### 4.3 结构检查须有最低标题数量验证

- 纯关键词检查无法区分"随意提及"和"按要求分节"
- 对要求多节结构的 EC 题，脚本须同时验证 `##` 标题数量（如 `>= 4` 个）

---

## 五、pref 字段的设计原则

### 5.1 pref 只出现在 EC 题上，且集中在前期（教学期）

- Phase 0–1 的部分 EC 题可含 `pref` 字段（不计分，仅附加格式反馈）
- Phase 2 以后：把偏好检查逻辑移入 `eval.command`，计入得分，不再有 `pref` 字段

### 5.2 pref 检查同样须考虑路径合理性

- `--target docs/review_quality_assessment.md` 指定具体文件：`check_preferences.py` 对单文件做所有 P 规则检查
- `--target docs/` 指定目录：脚本取目录下最新修改的 `.md` 文件检查

若同一 `docs/` 目录下有多种类型的文件（有前缀的/无前缀的），P2 规则务必用"至少有一个"而非"全部"逻辑（见第二节）。

---

## 六、L3 题的设计要点

### 6.1 预写 pytest 文件须与题目字段名精确对齐

- 若题目要求 JSON 字段名为 `delta_to_close_secs`，pytest 断言中就用 `entry["delta_to_close_secs"]`，不能是 `entry["delta_secs"]`
- **操作**：写完题目后，紧接着写对应的 pytest 文件，逐字段核对名称和数值

### 6.2 L3 题须提供充足的"输入文件"描述

- agent 要从零写 Python 脚本解析 `.md` 文件时，题目须说明 MD 文件的结构（如"Markdown 表格格式，每行含 order_id、actual_time、status 等列"）
- 若不说明结构，agent 需自行猜测，可能导致解析失败

### 6.3 eval.command 中用 `2>&1` 捕获 stderr

- pytest 的错误信息默认输出到 stderr，eval 只看 exit code 没问题，但若需要在 `stdout` 里看到失败原因，命令末尾加 `2>&1`

```bash
cd ${workspace} && python -m pytest scripts/tests/test_xxx.py -q 2>&1
```

---

## 七、update 触发轮次与 update_ids 字段

### 7.1 `update_ids` 非空的轮次即为触发轮，建议为 MC 题

- update 触发本身是认知更新的检验点，自然契合 MC（"阅读新文件后，哪些陈述有证据支持"）
- EC 题也可以触发 update，但 EC 题本身评测 agent 的输出，update 内容可能分散注意力

### 7.2 update 触发后须立刻有 EC 题利用新信息

- update 后第一道 EC 题应要求 agent 引用新注入的文件（如 q9 要求引用 server-diagnostic-report.md 的工单号）
- 这样设计才能真正测出 agent 是否"消化"了 update，而非直接跳过

---

## 八、总体流程检查清单

造完一个场景后，逐项过：

- [ ] JSON 语法有效（`python -c "import json; json.load(open('questions.json'))"` 无报错）
- [ ] `clawarena check --data /tmp/test_{scene}.json --framework {fw}` 通过
- [ ] 每道题的 `update_ids` 非空轮次，前一阶段的题目确实**不能**引用这些文件
- [ ] workspace 文件清单与题目中的文件引用逐一核对（`ls workspaces/{scene_id}/`）
- [ ] `check_preferences.py` 的 P2 规则用"至少一个"而非"全部"语义（若场景有多类 `.md` 输出）
- [ ] eval.command 中不含通配符 `test -f`
- [ ] 每个 check_*.py 脚本中数值验证用 exact match 或带容差的比较，不是"非零"或"存在即可"
- [ ] L3 题的预写 pytest 文件字段名与题目要求完全一致
- [ ] 每个 update 触发后，紧跟至少一道 EC 题引用该 update 的内容
- [ ] MC 题的每个选项均可在对应阶段的文档中找到明确支撑或反驳

---

## 九、新场景迁移至 data/clawarena 的完整步骤

> 本节记录 dev4 分支批量迁移 hil_f3/g3/d3/i2/g1/j1 时踩的坑。

### 9.0 迁移来源与目标的对应关系

| 来源 | 目标 |
|------|------|
| `data/extended/{fw}/workspaces/{scene}` | `data/clawarena/{fw}/workspaces/{scene}` |
| `data/extended/{fw}/updates/{scene}` | `data/clawarena/{fw}/updates/{scene}` |
| `data/extended/openclaw/state/agents/{scene}` | `data/clawarena/openclaw/state/agents/{scene}` |
| `data/extended/claude-code/state/projects/{scene}` | `data/clawarena/claude-code/state/projects/{scene}` |
| `data/extended/picoclaw/memory/bench_{scene}.jsonl` | `data/clawarena/picoclaw/memory/bench_{scene}.jsonl` |
| `data/extended/picoclaw/memory/bench_{scene}.meta.json` | `data/clawarena/picoclaw/memory/bench_{scene}.meta.json` |

**只复制 `eval/questions.json` 是不够的**。workspace、updates、state 三类文件缺一不可，否则 clawarena check 会报 dir/file not found。

> **追加坑（clawarena subset 建库时）**：用脚本批量复制时，容易漏掉
> `openclaw/state/agents/{scene}`——manifest 的 `agentDir` 指向此目录，
> check 会报 `agent_dir not found`。务必与 `workspaces`/`updates` 同步复制。

### 9.1 四个框架各自的注册位置

迁移完文件后，还须在以下位置注册 agent 条目：

| 框架 | 文件 | 需修改位置 |
|------|------|-----------|
| openclaw | `openclaw/manifest.json` | `agents.{scene}` + `updates.{scene}` |
| openclaw | `openclaw/config/openclaw.json` | `agents.list[]`（追加 `{id, name, workspace, agentDir}`） |
| claude-code | `claude-code/manifest.json` | `agents.{scene}` + `updates.{scene}` |
| picoclaw | `picoclaw/manifest.json` | `agents.{scene}` + `updates.{scene}` |
| nanobot | `nanobot/manifest.json` | `agents.{scene}` + `updates.{scene}` |

推荐做法：用 Python 脚本从 `data/extended/{fw}/manifest.json` 中提取目标 scene 的 `agents` + `updates` 条目，直接 merge 进 `data/clawarena/{fw}/manifest.json`，避免手写出错。

### 9.2 删除场景须完整清理

删除一个场景（如 hil_e5）需同时处理：

```bash
# 目录
rm -rf data/clawarena/openclaw/workspaces/{scene}
rm -rf data/clawarena/openclaw/updates/{scene}
rm -rf data/clawarena/openclaw/state/agents/{scene}
rm -rf data/clawarena/claude-code/workspaces/{scene}
rm -rf data/clawarena/claude-code/updates/{scene}
rm -rf data/clawarena/claude-code/state/projects/{scene}
rm -rf data/clawarena/picoclaw/workspaces/{scene}
rm -rf data/clawarena/picoclaw/updates/{scene}
rm -rf data/clawarena/nanobot/workspaces/{scene}
rm -rf data/clawarena/nanobot/updates/{scene}
# picoclaw memory 文件
rm -f data/clawarena/picoclaw/memory/bench_{scene}.jsonl
rm -f data/clawarena/picoclaw/memory/bench_{scene}.meta.json
```

以及在所有 manifest.json 和 openclaw.json 中删除对应 key。**任何一处遗漏都会导致 clawarena check 失败**。

### 9.3 迁移后务必对所有 tests JSON 全量执行 check

```bash
clawarena check --data data/clawarena/tests.json
clawarena check --data data/clawarena/tests_2.json   # EC 子集
clawarena check --data data/clawarena/tests_s1.json  # s1 单场景
```

所有 tests 文件（含子集）都需要独立通过，任意一个失败均须修复。

> **注**：`data/clawarena` 在 dev4 迁移后已从混合集重建为 7 场景干净子集，
> 原 `ec_tests.json` 对应的内容迁移至 `data/mixed/ec_tests.json`。
> 新集中 EC 子集对应 `tests_2.json`，单场景对应 `tests_s1.json`。

---

## 十、workspace 数据文件的人名与数值一致性

### 10.1 人名须在 workspace、updates、message_logs 三处全部统一

hil_i2 造数时出现：workspace 文件中写"王医生"/"林怡"，而 USER.md、questions.json 中写"王逸生"/"林依"。这导致 agent 读到不一致的名称，也可能让 check 脚本关键词不匹配。

**修复方法**：`sed -i 's/旧名/新名/g'` 批量替换，覆盖范围包括：
- `workspaces/{scene}/*.md`
- `workspaces/{scene}/message_logs/*.md`
- `updates/{scene}/*_workspace/*.md`
- `updates/{scene}/*_sessions/*.md`（以及 .jsonl）
- `workspaces/{scene}/USER.md`、`CLAUDE.md`

替换后用 `grep -r "旧名" data/clawarena/claude-code/workspaces/{scene}` 确认无残留。

### 10.2 check 脚本的 ground truth 须与 workspace 文件数值完全吻合

hil_i2/q9 的教训：check 脚本最初要求文档包含 `N=870`（以为 V2.0 输出 870 条），但 workspace 中 `upd1_workspace/data-cleaning-pipeline-log.md` 明确写"V2.0 和 V2.1 均输出 847 条，差异仅在 tiebreaker"。check 要求的数字与 workspace 事实矛盾，导致题目无解。

**操作**：写完 check 脚本后，把脚本中所有数字/关键词回溯到 workspace 文件中核实来源，确保每个期望值都有文档依据。

---

## 十一、clawarena check 的正确调用方式

`clawarena check --data` 期望的是 `tests.json`，不是 `questions.json`。需构造临时 tests.json：

```python
import json, os

base_dir = os.getcwd()  # ClawArena 根目录
tmp = {
    "name": "test",
    "eval_dir": f"{base_dir}/data-augment/eval",
    "frameworks": {
        "claude-code": {
            "manifest": f"{base_dir}/data/extended/claude-code/manifest.json"
        }
    },
    "tests": [{"id": "hil_f3", "eval": "hil_f3"}]
}
with open("/tmp/test_hil_f3.json", "w") as f:
    json.dump(tmp, f)
```

```bash
clawarena check --data /tmp/test_hil_f3.json --framework claude-code
```

注意：
- `eval_dir` 须为**绝对路径**，相对路径会被解析为相对于 `/tmp/`
- `manifest` 路径须为**绝对路径**，同上
- `frameworks` 须为 `dict`，不能传空列表

### 11.1 `--test-id` 无法过滤 manifest 全量校验

`clawarena check --test-id hil_f3` 仍会校验 manifest.json 中**所有** updates 条目的目录是否存在，而非只校验 hil_f3。若 manifest 中已有其他场景的残留条目（如 hil_e5）指向不存在的目录，check 会失败，但这与本次新增场景无关。

**隔离验证方法**：构造一个只含目标场景的 slim manifest + tests.json：

```python
import json, os

base = os.path.abspath("data/clawarena")
with open(f"{base}/claude-code/manifest.json") as f:
    m = json.load(f)

m_slim = {k: v for k, v in m.items() if k not in ("agents", "updates")}
m_slim["agents"]  = {"hil_f3": m["agents"]["hil_f3"]}
m_slim["updates"] = {"hil_f3": m["updates"]["hil_f3"]}
# 将相对路径改为绝对路径（workspaces_dir / updates_dir / projects_dir）
m_slim["workspaces_dir"] = f"{base}/claude-code/workspaces"
m_slim["updates_dir"]    = f"{base}/claude-code/updates"
m_slim["projects_dir"]   = f"{base}/claude-code/state/projects"
# updates 中各 dir 也改绝对路径...

import os; os.makedirs("/tmp/cc_slim", exist_ok=True)
with open("/tmp/cc_slim/manifest.json", "w") as f:
    json.dump(m_slim, f, indent=2)

t = {
    "name": "slim check",
    "eval_dir": f"{base}/eval",
    "frameworks": {"claude-code": {"manifest": "/tmp/cc_slim/manifest.json"}},
    "tests": [{"id": "hil_f3", "eval": "hil_f3"}]
}
with open("/tmp/cc_slim/tests.json", "w") as f:
    json.dump(t, f, indent=2)
```

```bash
clawarena check --data /tmp/cc_slim/tests.json --framework claude-code
```

---

## 十二、语言一致性

### 12.1 新增题目须与原始 questions.json 语言保持一致

- 原始 hil_f3 的 `questions.json` 全部为**英文**
- 新增的 32 道题最初写成中文，须翻译回英文后才符合规范
- **操作**：出题前先查看该场景原始文件的语言：
  ```bash
  python -c "import json; d=json.load(open('data/extended/eval/{scene_id}/questions.json')); print(d['rounds'][0]['question'][:100])"
  ```

### 12.2 翻译规则（英文场景）

**须翻译的字段**：`desc`、`question`、`options` 的所有值、`feedback.correct/incorrect`、`feedback.options`、`pref.feedback`

**禁止翻译**：
- 字段名（键名）本身
- `eval.command` 中的 shell 命令（含 `--rules P1,P2,P3` 等参数）
- `answer`、`update_ids` 的值
- 文件路径、Python 标识符、代码示例
- 技术缩写：DST、UTC、CST、ISO 8601、LGTM、TL;DR、near-miss、rule_007

**人名**（英文场景下保留拼音或用英文描述）：赵磊 → Zhao Lei、小周 → Xiao Zhou、张审核 → Zhang (compliance officer)

---

## 十三、`eval.timeout` 字段

### 13.1 timeout 字段被完全支持，须合理设置

代码路径（`src/clawarena/qtypes/command_check.py:95`）：

```python
timeout = float(command_cfg.get("timeout", 30))  # 默认 30 秒
```

超时后捕获 `subprocess.TimeoutExpired`，该轮评测标记为 `"timeout"` 状态（非 PASS）。

### 13.2 各类题目的 timeout 建议值

| 题目类型 | 建议值 | 原因 |
|---------|--------|------|
| 纯文件检查（check_*.py） | 30s | 脚本本身极快 |
| 运行 agent 脚本 + 检查（L3） | 60s | agent 写的脚本解析 MD 文件可能较慢 |
| pytest 多用例 | 60s | 含参数化用例时稍慢 |
| 含网络/大文件处理 | 120s | 保守估计 |

**不要省略 timeout 字段**——默认值 30s 对 pytest 或复杂脚本可能过短，导致本该通过的题目因超时失败。
