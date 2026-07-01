# 造数据避雷指南

本文记录 hil_s1 场景造数据全程踩过的所有坑，供后续场景造数据时对照规避。

**背景**：hil_s1（NexaRetail Q1 2025 customer churn analysis）共 7 个 session、4 轮 update、66 道评测题，是第一个由 subagent 批量生成对话内容的场景，暴露了大量流程与格式问题。

---

## 坑 1：subagent 生成的 loops 格式与 session_builder.py 期望格式不符

**现象**：所有 session JSONL 文件只有 header 行，无对话内容（或 user 消息内容为空）。

**根因**：subagent 生成的 loops JSON 是 OpenAI messages 格式：

```json
{
  "session_meta": { ... },
  "loops": [
    {
      "messages": [
        {"role": "user", "content": "..."},
        {"role": "assistant", "tool_calls": [...]}
      ]
    }
  ]
}
```

而 `session_builder.py` 期望 GUIDE.md 定义的 user/turns 格式：

```json
{
  "session_meta": { ... },
  "loops": [
    {
      "user": {"speaker": "Alex", "text": "..."},
      "turns": [
        {
          "assistant": {"tools": [{"id": "...", "name": "...", "args": {...}}]},
          "results": [{"tool_id": "...", "content": "...", "is_error": false}]
        },
        {
          "assistant": {"text": "最终回复"}
        }
      ]
    }
  ]
}
```

**修复**：写 `data-synthesis/hil_s1/convert_loops.py` 做一次性批量格式转换（含备份到 `loops_backup/`），再重建所有 session。

**预防**：给 subagent 写 loops 内容时，在 prompt 里明确提供格式样例，并要求输出 user/turns 格式，不要使用 messages 格式。或在 subagent prompt 里直接引用 GUIDE.md 的格式定义。

---

## 坑 2：history session header 含多余的 cwd 字段

**现象**：`hbench check` 未直接报错，但 session 文件的 header 行含 `"cwd": "/path/to/workspace"`，导致 openclaw 加载历史 session 时路径错乱。

**根因**：`session_builder.py` 第 443 行原代码：

```python
cwd = args.cwd or workspace_dir  # 即使不传 --cwd 也会用 workspace_dir 填充
```

所有 `append` 命令调用均会写入 cwd，即使历史 session 不应有此字段。

**修复**：改为 `cwd = args.cwd`（`None` 时不写入 header）；`make_session_header` 改为只有 `cwd` 非 None 时才添加该字段（`session_builder.py` 第 174/181 行）。

**规则**：history session 的 header 行不含 `cwd` 字段；只有主 session 才含 `cwd`（通过 `--cwd` 显式传入）。

---

## 坑 3：group session 语义理解错误——将其建模为群聊

**现象**：`hbench check` 报出 257 处 `"consecutive 'user' messages"` 错误，几乎所有 group session 文件全部不合法。

**根因**：subagent 将 group session（S5/S6/S7）建模为群聊——多个用户彼此互相发言，agent 只在最后回复一次。实际语义是：

> group session = 多人**共用一个 agent**，每个人向 agent 提问，agent 必须逐条回复。

openclaw 框架要求 user/assistant 严格交替，连续的 user 消息是非法状态。

**修复**：6 个并行 subagent 为 257 个空 turns（只有 user 消息、无 agent 回复的位置）生成 agent 回复，重建所有 session。

**预防**：在 subagent prompt 中明确说明：group session 不是群聊，每一条 user 消息后必须有 agent 的完整回复（可含工具调用链）。

---

## 坑 4：group session 的 group_name 带 `#` 前缀

**现象**：`convert_loops.py` 无法找到对应的 `GROUP_PARTICIPANTS`，导致 speaker 分配为默认的 `["User"]`，且生成的 envelope 出现双 `##`（如 `##data-engineering`）。

**根因**：部分 subagent 生成的 p2/p3 文件 `session_meta.group_name` 为 `"#data-engineering"`，而 p1 文件为 `"data-engineering"`，格式不统一。`GROUP_PARTICIPANTS` 字典的键不带 `#`。

**修复**：`convert_loops.py` 的 `convert_file()` 中自动剥离前缀：

```python
if group_name and group_name.startswith("#"):
    group_name = group_name[1:]
    session_meta = dict(session_meta)
    session_meta["group_name"] = group_name
```

**预防**：`session_meta.group_name` 统一不带 `#`；在 subagent prompt 里注明此规范。

---

## 坑 5：group session 无 participant 字段导致 AttributeError

**现象**：`convert_loops.py` 在处理 group session 时崩溃，报 `AttributeError: 'NoneType' object has no attribute 'lower'`。

**根因**：group session 的 `session_meta` 不含 `participant` 字段（DM session 有），代码调用 `participant.lower()` 时 `participant` 为 `None`。

**修复**：

```python
participant = session_meta.get("participant") or "user"
```

**预防**：处理可选字段时始终使用 `or` 提供默认值，不直接链式调用方法。

---

## 坑 6：assemble.sh 和 register_sessions.py 路径指向旧目录

**现象**：脚本执行后文件写入了 `data/hbench/openclaw/`，而非独立测试目录 `data/hilbench/openclaw/`。

**根因**：迁移到独立 `hilbench` 目录时，只改了数据文件，忘记同步更新两个脚本的路径变量：
- `assemble.sh`：`DATA_ROOT`、`EVAL_ROOT`
- `register_sessions.py`：第 19 行 `SESSIONS_DIR`

**修复**：将两处均从 `data/hbench/...` 改为 `data/hilbench/...`。

**预防**：将路径变量集中定义在 `assemble.sh` 顶部，`register_sessions.py` 读取同一变量来源，或使用相对路径。每次迁移数据目录后，执行 `grep -r "data/hbench" data-synthesis/hil_s1/` 检查残留引用。

---

## 坑 7：主 session 文件缺失

**现象**：`hbench check` 报错，`manifest.json` 声明了 `main_7643b677-…` 为主 session，但 `state/agents/hil_s1/sessions/` 下不存在对应文件。

**根因**：`assemble.sh` 只负责生成历史 session（S1-S7），未创建主 session 文件。主 session 需要单独手动创建，包含项目背景介绍消息。

**修复**：手动创建 `main_7643b677-948c-4211-a390-b6f32e16d58d.jsonl`，内容为合法的 6 行 JSONL（header + model_change + thinking_level_change + model-snapshot + user 消息 + assistant 回复）。

**预防**：在 GUIDE.md 或造数步骤说明中明确列出"主 session 须单独创建"这一步骤，并在 `assemble.sh` 末尾提示。

---

## 坑 8：openclaw.json 未配置新场景

**现象**：`hbench check` 报错，manifest 校验失败——`manifest.agents` 中声明的 `hil_s1` 在 `openclaw/config/openclaw.json` 的 `agents.list` 中无对应条目。

**根因**：`openclaw.json` 是手动维护的配置文件，新增场景后需手动添加条目。

**修复**：在 `openclaw.json` 的 `agents.list` 中添加：

```json
{
  "id": "hil_s1",
  "name": "hil_s1",
  "workspace": "${BENCHMARK_ROOT}/data/hilbench/openclaw/workspaces/hil_s1",
  "agentDir": "${BENCHMARK_ROOT}/data/hilbench/openclaw/state/agents/hil_s1/agent"
}
```

**预防**：在 `assemble.sh` 末尾的 Next steps 提示中，明确加上"更新 openclaw.json"这一步。

---

## 坑 9：`cp -r` 目标目录不存在时内容溢出父目录

**现象**：执行 `cp -r src/ dst/` 时，若 `dst/` 不存在，`cp` 将 `src/` 的**内容**直接复制到 `dst/` 的父目录，而非在父目录下新建 `dst/`。

**根因**：`cp -r src/ dst/` 在 `dst/` 已存在时，会在 `dst/` 下新建 `src/` 目录；在 `dst/` 不存在时，行为等同于 `mv src/ dst/`，将内容平铺到父目录。

**修复**：先用 `find ... -maxdepth 1 -not -name "hil_s1" -exec rm -rf {} +` 清理溢出的文件，再用 `mkdir -p dst/ && cp -r src/. dst/` 确保目标目录存在。

**预防**：迁移目录时，始终先 `mkdir -p dst/` 再 `cp -r src/. dst/`（注意 `src/.` 而非 `src/`）。

---

## 坑 10：并行 subagent 写入同一 loops 文件导致内容冲突

**现象**：多个 subagent 并行处理不同的 loops 文件，但有两个 subagent 同时写了同一个文件（`s7_all_hands_group_p1.json`），后写者的内容覆盖了前写者。

**根因**：subagent 任务分配时没有严格隔离文件边界，历史 context 残留的 subagent 与新启动的 subagent 产生竞争写入。

**结果**：本次最终写入内容完整（0 空 turns），无数据丢失——纯属幸运，后写者的内容恰好是完整版本。

**预防**：并行 subagent 任务分配时，按文件明确划分，每个 subagent 只负责一个文件；分配前检查是否有残留 subagent 正在运行。

---

## 坑 11：exec_check 脚本路径使用 `${eval_dir}/scripts/`，实际应为 `${eval_dir}/${agent_id}/scripts/`

**现象**：运行 exec_check 时报错 `python: can't open file '.../data/hilbench/eval/scripts/check_preferences.py'`，脚本文件找不到。

**根因**：`${eval_dir}` 解析为 eval **根**目录（如 `data/hilbench/eval`），不含 agent/scenario 子目录。而检查脚本实际位于 `eval/<agent_id>/scripts/`（如 `eval/hil_s1/scripts/`）。subagent 生成 questions.json 时误用了 `${eval_dir}/scripts/`，漏掉了 `/${agent_id}` 层级。

**正确路径**：
```
${eval_dir}/${agent_id}/scripts/check_preferences.py
```
其中 `${agent_id}` 在 TestContext 中等于 `test_id`（即当前场景 ID，如 `hil_s1`）。

**修复**：在 `questions.json` 中将全部 42 处 `${eval_dir}/scripts/` 替换为 `${eval_dir}/${agent_id}/scripts/`；同步更新 `docs/question-types.md` 中的占位符说明和所有示例。

**预防**：给 subagent 写 eval 题目时，明确告知 `${eval_dir}` 是根目录，访问本场景检查脚本必须用 `${eval_dir}/${agent_id}/scripts/`。可在 GUIDE.md 或 prompt 中提供完整示例。

---

## 坑 12：多选题 feedback.options 只有错误选项解析，缺失正确选项解析

**现象**：`questions.json` 中所有多选题的 `feedback.options` 仅为错误选项（被错选者）提供解释，正确选项没有对应解析。当 agent 漏选了某个正确选项时，系统无法向其解释该选项为何正确。

**根因**：subagent 生成 eval 内容时，默认将 `feedback.options` 理解为"错误原因说明"，只写了错误选项（C、F 等），未为正确选项补充"为何正确"的解析。

**修复**：
- 新建 `feedback_patch_correct_options.json`，包含全部 19 道多选题、共 65 个正确选项的逐条解析。
- 新建 `merge_feedback_patch.py`，将 patch 合并进 `questions.json`（原地更新，备份到 `questions_backup_before_patch.json`）；已有解析的 key 不覆盖（幂等）。
- 合并后每道多选题的 `feedback.options` 同时覆盖正确与错误选项。

**预防**：在 subagent 生成 eval 的 prompt 中明确要求：`feedback.options` 必须包含**所有选项**（正确选项解释为何正确，错误选项解释为何错误），不能只写错误选项。

---

## 坑 13：check_preferences.py P3 正则因 f-string 解析错误导致全部假性失败

**现象**：所有含 P3 检查的题目全部失败，报 `Missing required sections: Summary, Details, Action Items`，即便报告文件中明确包含 `## Summary / ## Details / ## Action Items` 标题。

**根因**：`validation_utils.py` 中用 f-string 构造 Markdown 标题正则：

```python
pattern = rf'^#{1,6}\s*{re.escape(section)}\s*$'
```

Python f-string 将 `{1,6}` 解析为表达式，结果是元组 `(1, 6)` 转字符串 `"(1, 6)"`，最终正则变为 `^#(1, 6)\s*Summary\s*$`，根本不匹配任何 Markdown 标题。

**修复**：将该行改为字符串拼接，避免 f-string 处理正则量词：

```python
pattern = r'^#{1,6}\s*' + re.escape(section) + r'\s*$'
```

**预防**：在正则中混用 f-string 时，量词 `{n,m}` 必须转义为 `{{n,m}}`，或改用字符串拼接方式构造正则。造数完成后建议对所有检查脚本做单元测试（含已知通过和失败的文件各一份）。

---

## 坑 14：JSON schema 的 required 字段远超题目要求，导致 agent 按题目生成的 JSON 无法通过验证

**现象**：多道 exec_check 题目（q11/q19/q20/q35/q36/q48/q62/q63 等）schema 校验失败，报 `Missing required field: xxx`，但 agent 完全按照题目描述的格式结构生成了 JSON。

**根因**：生成 JSON schema 的 subagent 将 schema 设计为"完整规范"（含大量可选字段），并将其中多数列为 `required`。而题目 question 给 agent 的格式示例是简化版，只包含核心字段。两者之间存在系统性不一致：schema 要求 > 题目示例。

典型案例：
- `data_overview` schema 要求 `fields`（字段元数据数组），题目示例无此字段
- `data_overview` schema 要求 `issues` 为对象数组，题目示例中 `issues` 是普通 key-value object
- `timeline` schema 要求 `project`/`kickoff_date`/`final_deadline`，题目均未提及

**修复**：采用方案 B——简化 schema，将题目中未明确要求的字段从 `required` 数组中移除，改为可选；对类型不一致的字段改为 `anyOf` 或 `["array","object"]`。

**预防**：
1. 生成 schema 后，必须与对应题目的 question 文本逐字段对照，确保 `required` 中的每个字段在题目示例或明确说明中均有体现
2. 造数完成后用 agent 实际生成的文件验证一遍所有 schema（`check_schema.py --file <实际文件> --schema <名称>`）

---

## 坑 15：eval 命令过松，仅检查文件存在而不验证内容质量

**现象**：部分 exec_check 题目评测命令形如 `test -f file.md` 或 `test -s file.md`，agent 只需创建一个空文件或任意内容的文件即可通过，无法真正考察输出质量。

**受影响题目示例**：
- `test -f .../reports/2025-03-03_data_quality_v1.md`（只查文件存在）
- `test -s .../docs/metrics_definitions.md`（只查非空）
- `ls .../reports/*_progress_update_v1.md | head -1 | xargs test -f`（不稳定且只查存在）

**修复**：对这类命令追加内容关键词检查，例如：

```bash
test -f file.md && grep -qiE "51[,.]?203|record.count" file.md && grep -qiE "date|format|mixed" file.md
```

**预防**：每道 exec_check 题目的评测命令必须验证**内容语义**，不能只验文件存在或非空。设计时问自己：「如果 agent 只写了一行随机文字，这个命令还会通过吗？」——如果答案是会，说明命令过松。

---

## 坑 16：eval 环境缺少 pandas/scipy，导致所有依赖这些库的 pytest 假性失败

**现象**：所有用 `pytest` 测试 data_loader、analysis 等模块的 exec_check 题目全部失败，报 `ModuleNotFoundError: No module named 'pandas'`。Agent 在推理阶段已正确完成任务并通过测试，评测阶段却失败。

**根因**：agent 推理使用的 Python 环境（含 pandas/scipy）与 hbench 评测使用的环境（miniconda3 基础环境）不同，评测环境未安装项目所需依赖。

**修复**：在评测机器的 hbench 环境中安装依赖（`pip install pandas scipy`），并在 `pyproject.toml` 中显式声明依赖：

```toml
dependencies = [
    "pandas>=2.0",
    "scipy>=1.11",
]
```

**预防**：
1. 凡是 exec_check 命令中 `import` 了第三方库，必须确保 hbench 运行环境中已安装
2. 在 `pyproject.toml` 中声明这些依赖，使 `pip install -e .` 时自动安装
3. 造数完成后，用 hbench 的 Python 手动执行一遍所有 exec_check 命令验证环境

---

## 坑 17：workspace 测试文件使用 pandas 废弃频率码，导致 pytest 假性失败

**现象**：q5/q15 的 exec_check 命令运行 `pytest tests/test_data_loader.py` 持续报 3 个 FAILED，即使 agent 的 data_loader.py 已正确修复。错误信息如下：

```
FutureWarning: 'M' is deprecated and will be removed in a future version, please use 'ME' instead.
ValueError: Invalid frequency: H
```

**根因**：workspace 初始测试文件 `tests/test_data_loader.py` 的 fixtures 中使用了 pandas 2.2+ 已废弃或移除的频率码：
- `freq='M'`（月末）→ 应改为 `freq='ME'`
- `freq='H'`（小时）→ 应改为 `freq='h'`

这是**测试文件本身的 bug**，与 agent 的实现无关，但评分直接失败。

**修复**：在 workspace 初始文件中将所有废弃频率码替换为新版写法。

**预防**：
1. workspace 测试文件生成后，在目标 Python 环境中本地执行一遍 `pytest`，确保初始状态全部通过（agent 尚未修改任何代码时）
2. 造数时注意 pandas 版本：`pyproject.toml` 声明 `pandas>=2.0`，则 `freq='M'/'H'` 等旧写法在 2.2+ 会触发 FutureWarning，在 2.2 某小版本后直接报错

---

## 坑 18：eval command 用 `python -c "import ast..."` 做代码分析，运行时超时

**现象**：q29 的 eval.command 在评测时 exit_code 为 -1，stderr 为 `Timeout after 30s`，整题判失败。Agent 实际已正确将 Pearson 替换为 Spearman。

**根因**：eval.command 设计为：

```bash
python -c "import ast, sys; src = open('src/analysis_v2.py').read(); assert 'spearmanr' in src ..."
```

在某些环境中，`python -c` 启动开销叠加上后续 `python -m pytest tests/ -q` 的全量测试，总耗时超过默认 30 秒超时限制。且 `import ast` 为无用导入，增加了不必要开销。

**修复**：将源码字符串检查替换为 `grep -q`：

```bash
cd ${workspace}/project && grep -q 'spearmanr' src/analysis_v2.py && python -m pytest tests/ -q 2>&1
```

**预防**：eval.command 中需要检查源码是否含某关键词时，优先用 `grep -q`；避免用 `python -c "import ast..."` 做字符串级检查（AST 解析对于此类检查完全多余）。若必须用 pytest，考虑适当增大 `timeout` 字段（默认 30s）。

---

## 坑 19：eval command 调用脚本时传入脚本不支持的参数

**现象**：q32 的 eval.command 执行时报 `error: unrecognized arguments: --section 2025-03-11`，exit_code 为 2，整题判失败。Agent 实际已正确追加了 2025-03-11 会议记录。

**根因**：eval.command 设计为：

```bash
python check_preferences.py --file meeting_notes.md --rules P3 --section "2025-03-11"
```

而 `check_preferences.py` 实际支持的参数包括 `--file`/`--workspace`/`--rules`/`--target-latest-report` 等，**不支持 `--section`**。命令中传入了一个臆想的参数。

**修复**：移除 `--section` 参数，日期存在性改用 `grep -q` 验证：

```bash
grep -q "2025-03-11" ${workspace}/project/docs/meeting_notes.md && \
  python ${eval_dir}/${agent_id}/scripts/check_preferences.py \
    --file ${workspace}/project/docs/meeting_notes.md --rules P3
```

**预防**：eval.command 中调用的每一个脚本，必须先查阅该脚本的 `argparse` 定义或 `--help` 输出，确认所有传入的参数确实存在。生成 questions.json 的 subagent 通常不会自动核对参数名，需要人工或造数完成后批量 dry-run 验证。

---

## 坑 20：eval command 对 pipeline 输出 JSON 的结构假设过死

**现象**：q37/q57 的 eval.command 运行时报 `AssertionError: wrong method`，exit_code 为 1，整题判失败。Agent 实际已成功运行 pipeline 并生成 JSON，其中正确包含了 `spearman`，但结构与 command 预期不符。

**根因**：eval.command 硬断言顶级字段：

```python
# q37
assert d.get('method') == 'spearman'
assert 'correlation' in d

# q57
assert d.get('method') == 'spearman'
assert d.get('churn_threshold') == 30
assert 'churn_rate' in d
```

而 agent 生成的 JSON 将这些信息置于嵌套子对象中，例如：

```json
{ "spearman_correlation": { "method": "spearman", "rho": 0.42, ... } }
```

这是**合理的 JSON 设计**，但 command 的断言要求顶级平铺结构，两者不匹配。

**修复**：改用 `json.dumps(d).lower()` 检查关键词是否出现在整个 JSON 字符串中，放宽对具体嵌套层级的约束：

```bash
python -c "import json; d=json.load(open('results.json')); s=json.dumps(d).lower(); \
  assert 'spearman' in s; assert 'corr' in s"
```

**预防**：
1. eval.command 验证 pipeline 输出时，应只断言**语义要求**（如"包含 spearman 方法"），不应断言**具体 JSON 层级结构**（如 `d.get('method')`）
2. 如果需要严格的结构检查，应在题目 question 中明确给出 JSON 示例，agent 须完全遵循；同时 eval.command 与题目示例保持一致
3. 造数完成后用 agent 实际生成的典型 JSON 文件，在评测环境中跑一遍所有 `python -c` 断言，确认不会因合理的结构变体而失败

---

## 坑 21：`ls | head | xargs -I{}` 空输入时假性通过，eval 命令漏报

**现象**：q16 的 eval.command 在 agent 没有生成验证报告文件时，整条命令仍以 exit 0 通过，`check_preferences.py` 从未被调用，实际上没有做任何检查。

**根因**：命令结构如下：

```bash
python src/validate_data.py && \
  ls reports/*_validation_report_v1.md 2>/dev/null | head -1 | \
  xargs -I{} python check_preferences.py --file {} --rules P1
```

执行路径分析：
1. `validate_data.py` 成功退出（exit 0）
2. `ls` 无匹配文件 → 输出空、退出 1，但因为**管道**，exit code 传给 `head`
3. `head -1` 读到空输入 → 输出空、**退出 0**（head 不关心上游 exit code）
4. `xargs -I{}` 读到空输入 → 不执行任何命令、**退出 0**
5. 整条命令链以 0 退出 ✓（假性通过）

**修复**：用变量暂存文件名，加入 `test -n` 和 `test -f` 的显式检查：

```bash
cd ${workspace}/project && python src/validate_data.py && \
  RFILE=$(ls reports/*_validation_report_v1.md 2>/dev/null | head -1) && \
  test -n "$RFILE" && test -f "$RFILE" && \
  python ${eval_dir}/${agent_id}/scripts/check_preferences.py --file "$RFILE" --rules P1
```

`test -n "$RFILE"` 确保变量非空，若无报告文件则立即失败，后续检查不会被跳过。

**预防**：凡是用 `ls ... | xargs -I{}` 或 `cmd | head -1 | xargs` 的模式，都需要额外验证管道输入非空。更安全的替代：

```bash
# 方案A：变量 + test -n（推荐）
FILE=$(ls pattern 2>/dev/null | head -1) && test -n "$FILE" && test -f "$FILE" && cmd "$FILE"

# 方案B：用 find 替代 ls（find 无匹配时退出 0，但不输出，同样需要 test -n）
FILE=$(find dir -name "pattern" | head -1) && test -n "$FILE" && cmd "$FILE"
```

---

## 造数流程核对清单

新增场景时，按顺序逐项确认：

1. **loops JSON 格式**：所有 loops 文件使用 user/turns 格式，不使用 messages 格式
2. **group session 语义**：每条 user 消息后必须有 agent 完整回复，不允许连续 user
3. **主 session 文件**：手动创建，含项目背景介绍
4. **history session header**：不含 `cwd` 字段（不传 `--cwd` 参数）
5. **assemble.sh 路径**：`DATA_ROOT`、`EVAL_ROOT` 指向正确目录
6. **register_sessions.py 路径**：`SESSIONS_DIR` 与 `assemble.sh` 一致
7. **openclaw.json**：新场景在 `agents.list` 中有对应条目
8. **manifest.json**：`agents` 和 `updates` 中的声明与实际文件一一对应
9. **tests.json**：新场景已添加
10. **exec_check 脚本路径**：command 中使用 `${eval_dir}/${agent_id}/scripts/`，不能省略 `/${agent_id}`
11. **多选题 feedback.options**：正确与错误选项均有逐条解析
12. **检查脚本正则**：避免在 f-string 中直接使用正则量词 `{n,m}`，应改用字符串拼接
13. **JSON schema 与题目对齐**：`required` 中的字段必须在题目示例或说明中有对应体现
14. **exec_check 命令强度**：每条命令须验证内容语义，不能只检查文件存在/非空
15. **eval 环境依赖**：eval 命令 import 的第三方库须在 hbench 环境安装并在 pyproject.toml 声明
16. **`hbench check`**：0 errors，0 warnings
17. **workspace 测试文件 pandas 频率码**：生成后在目标环境跑一遍 pytest，初始状态应全部通过；注意 `freq='M'`/`'H'` 在 pandas 2.2+ 废弃
18. **eval command 不用 `python -c` 做关键词检查**：改用 `grep -q`，避免超时；若用 pytest 需确认 timeout 足够
19. **eval command 调用脚本前核对参数**：查阅脚本 argparse 定义，确认每个传入参数确实存在
20. **eval command 不断言 pipeline JSON 具体层级结构**：用 `json.dumps(d).lower()` 检查关键词；若需严格结构，题目与 command 须同步给出示例
21. **`ls | xargs -I{}` 空输入假性通过**：管道空输入时 xargs 不执行命令却退出 0；改用变量暂存文件名并加 `test -n "$VAR"` 显式检查
