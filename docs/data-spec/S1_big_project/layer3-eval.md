# Layer 3 — Eval 题目设计

> 共 66 题，4 个 update 轮次（Round 0 含初始状态）。
> multi_choice：选项 A-F（4-6 个），不定项选择，答案为正确选项的集合。
> exec_check：给出完整 eval.command；使用 `${workspace}`、`${eval_dir}` 占位符。
> pref 字段仅在显式偏好阶段（P1/P4/P5 首批题）出现。

---

## Round 0（题目 1-12，初始状态）

### Q1 — 项目优先级真实排序
```
type: multi_choice
dimension: 多信息源 + C7
question: Based on all available session records, which statements about the project's work priority are accurate?

options:
  A: Alex explicitly stated that the prediction model analysis is the core deliverable, and the report is secondary.
  B: The project kickoff meeting established that the report and model should be developed simultaneously with equal priority.
  C: Sam's stated priority (report first) represents the official project decision endorsed by Alex.
  D: Alex privately indicated that "report first" was a diplomatic compromise, not the actual technical priority.
  E: Jordan believes the deadline is March 15.
  F: Sam and Alex are fully aligned on project priorities.

answer: [A, B, D, E]
```
**解析**：A（S1 Loop 4 Alex 明说"model is the priority"）✅；B（S7 Alex 的妥协表述✅，但 B 与 A 并不矛盾——这是表面共识）✅；C（Alex 未背书 Sam 的优先级）❌；D（S1 Update 1 Loop 7 Alex 明说）✅；E（S3 Loop 2 Jordan 说"March 15？"）✅；F（两人明显不一致）❌

---

### Q2 — 数据质量问题描述差异
```
type: multi_choice
dimension: 多信息源 + C3
question: Which of the following accurately describe discrepancies in how team members characterize the transaction data?

options:
  A: Maya refers to the revenue field as "transaction_amount", but the actual CSV field is "order_value".
  B: Maya's data_loader.py uses the correct field name "order_value" throughout.
  C: The schema_changelog.md confirms that the field was renamed from "transaction_amount" to "order_value" in v2.
  D: Maya acknowledged the correct field name is "order_value" when directly shown the CSV header.
  E: The data_loader.py bug directly causes a KeyError when loading transactions_v1.csv.

answer: [A, D, E]
```
**解析**：A（C3 矛盾核心）✅；B（data_loader 用的是 transaction_amount，bug 所在）❌；C（changelog 说 v2 没有改名，即没有改名行为，transaction_amount 从来都不是正式字段名）❌；D（S2 Loop 1 Maya 确认）✅；E（Bug 1，df["transaction_amount"] 不存在会 KeyError）✅

---

### Q3 — 分析方法跨源证据
```
type: multi_choice
dimension: 多信息源 + C5
question: Which statements about the planned statistical analysis method have cross-session support?

options:
  A: Jordan initially planned to use Spearman correlation because the data may not be normally distributed.
  B: Sam recommended Pearson correlation, claiming it is simpler and sufficient.
  C: Alex explicitly approved switching from Spearman to Pearson.
  D: Jordan switched to Pearson after Sam's recommendation.
  E: The analysis.py file implements Spearman correlation correctly.

answer: [A, B, D]
```
**解析**：A（S3 Loop 1 Jordan 原始计划）✅；B（S4 Loop 2 Sam 的误导）✅；C（Alex 从未说过此话）❌；D（S3 Loop 3 Jordan 切换）✅；E（analysis.py 中 correlate_spend_churn 是 TODO，未实现）❌

---

### Q4 — 生成数据质量报告（P1 显式阶段）
```
type: exec_check
mode: E（偏好脚本）
dimension: 人类偏好(P1)

question: |
  Generate a data quality report for the raw transaction data. Save it to
  `project/reports/2025-03-03_data_quality_v1.md`.

  **Format requirements (P1):**
  - All timestamps must use ISO 8601 format (e.g., `2025-03-03T09:00:00Z`)
  - Numbers ≥ 1,000 must use thousands separators (e.g., `51,203`)

  The report must include:
  - Total record count
  - Percentage of records with date format issues
  - Summary of missing values by column

eval:
  command: "test -f ${workspace}/project/reports/2025-03-03_data_quality_v1.md"
  expect_exit: 0

feedback:
  correct: "Report file found. Good work."
  incorrect: "Report file not found at the expected path. Check the filename convention."

pref:
  command: >
    python ${eval_dir}/scripts/check_preferences.py
    --file ${workspace}/project/reports/2025-03-03_data_quality_v1.md
    --rules P1
  expect_exit: 0
  feedback:
    correct: ""
    incorrect: |
      Note: Your report contains P1 violations. Check:
      - Timestamps should be ISO 8601 (e.g., 2025-03-03T09:00:00Z)
      - Numbers ≥ 1,000 need thousands separators (e.g., 51,203 not 51203)
```

---

### Q5 — 修复 data_loader.py Bug
```
type: exec_check
mode: D（测试套件）
dimension: —

question: |
  Fix the bugs in `project/src/data_loader.py`:
  1. The field name `transaction_amount` should be `order_value`
  2. `parse_dates()` should handle both `YYYY-MM-DD` and `M/D/YYYY` formats

  Make sure all tests in `project/tests/test_data_loader.py` pass.

eval:
  command: "cd ${workspace}/project && python -m pytest tests/test_data_loader.py -q 2>&1"
  expect_exit: 0
  expect_stdout: "passed"

feedback:
  correct: "All tests pass. Both bugs are fixed correctly."
  incorrect: "Tests still failing. Check the field name mapping and date format handling."
```

---

### Q6 — 编写数据清洗脚本
```
type: exec_check
mode: C（运行 agent 脚本）
dimension: —

question: |
  Write a data cleaning script at `project/src/clean_data.py` that:
  1. Loads `data/raw/transactions_v1.csv`
  2. Standardizes date formats to YYYY-MM-DD
  3. Removes rows where order_value is null or negative
  4. Saves the cleaned data to `data/processed/transactions_v1_clean.csv`

  Then run the script to produce the output file.

eval:
  command: >
    cd ${workspace}/project &&
    python src/clean_data.py &&
    test -f data/processed/transactions_v1_clean.csv &&
    python -c "import pandas as pd; df=pd.read_csv('data/processed/transactions_v1_clean.csv'); assert len(df) > 0"
  expect_exit: 0

feedback:
  correct: "Cleaned data file created and validated."
  incorrect: "Script failed or output file missing. Check that it loads v1, cleans dates, and saves to processed/."
```

---

### Q7 — 提取里程碑写入文件
```
type: exec_check
mode: B（预置脚本）
dimension: 多信息源 + C4

question: |
  Based on all available session records and workspace files, extract the key project deadlines
  and milestones, and write them to `project/docs/milestones.json` in this format:
  {
    "final_deadline": "YYYY-MM-DD",
    "interim_review": "YYYY-MM-DD",
    "kickoff_date": "YYYY-MM-DD"
  }

eval:
  command: >
    python ${eval_dir}/scripts/check_deadline_file.py
    --file ${workspace}/project/docs/milestones.json
  expect_exit: 0

feedback:
  correct: "Milestone dates are correct."
  incorrect: "Milestone dates are wrong. final_deadline=2025-03-14, interim_review=2025-03-12, kickoff_date=2025-03-03."
```
**check_deadline_file.py 规格**：验证 JSON 存在且三个日期正确（final_deadline=2025-03-14, interim_review=2025-03-12, kickoff_date=2025-03-03）。

---

### Q8 — 整理数据指标定义（P1 显式阶段）
```
type: exec_check
mode: E（偏好脚本）
dimension: 人类偏好(P1)

question: |
  Write a metrics definition file at `project/docs/metrics_definitions.md` that defines:
  - Churn rate (include the threshold in days and the formula)
  - Average monthly spend (include dataset size with proper number formatting)
  - Data coverage period

  Follow P1 formatting rules for all numbers and timestamps.

eval:
  command: "test -s ${workspace}/project/docs/metrics_definitions.md"
  expect_exit: 0

feedback:
  correct: "Metrics definition file created."
  incorrect: "File missing or empty."

pref:
  command: >
    python ${eval_dir}/scripts/check_preferences.py
    --file ${workspace}/project/docs/metrics_definitions.md
    --rules P1
  expect_exit: 0
  feedback:
    correct: ""
    incorrect: "P1 violation in metrics file: ensure numbers use thousands separators and timestamps are ISO 8601."
```

---

### Q9 — 更新 config.py 字段映射
```
type: exec_check
mode: A（inline）
dimension: —

question: |
  Update `project/src/config.py` to fix the FIELD_MAP: the "revenue" key should map to
  "order_value" (not "amount"), and "date" should map to "date" (not "transaction_date").

eval:
  command: >
    grep -q '"order_value"' ${workspace}/project/src/config.py &&
    grep -q '"revenue": "order_value"' ${workspace}/project/src/config.py
  expect_exit: 0

feedback:
  correct: "config.py FIELD_MAP correctly updated."
  incorrect: "config.py still has incorrect field mapping. Check FIELD_MAP."
```

---

### Q10 — 生成需求 JSON task list
```
type: exec_check
mode: G（结构化输出）
dimension: 多信息源

question: |
  Based on all available session discussions, create a consolidated task list at
  `project/docs/task_list.json`. Schema:
  {
    "tasks": [
      {"id": str, "owner": str, "description": str, "priority": "high"|"medium"|"low", "due_date": "YYYY-MM-DD"}
    ]
  }
  Include at least 5 tasks covering: data cleaning, analysis, report writing, code review, stakeholder presentation.

eval:
  command: >
    python ${eval_dir}/scripts/check_schema.py
    --file ${workspace}/project/docs/task_list.json
    --schema task_list
  expect_exit: 0

feedback:
  correct: "Task list JSON is valid and complete."
  incorrect: "JSON schema validation failed. Check that all required fields are present and properly typed."
```

---

### Q11 — 生成数据概览 JSON（P1 联合检查）
```
type: exec_check
mode: F（组合检查）
dimension: 人类偏好(P1)

question: |
  Create a data overview file at `project/docs/data_overview.json`:
  {
    "dataset": "transactions_v1.csv",
    "record_count": <int>,
    "date_range": {"start": "YYYY-MM-DDTHH:MM:SSZ", "end": "YYYY-MM-DDTHH:MM:SSZ"},
    "issues": {"mixed_date_format_count": <int>, "null_order_value_count": <int>}
  }

eval:
  command: >
    python ${eval_dir}/scripts/check_schema.py
    --file ${workspace}/project/docs/data_overview.json
    --schema data_overview &&
    python ${eval_dir}/scripts/check_preferences.py
    --file ${workspace}/project/docs/data_overview.json
    --rules P1
  expect_exit: 0

feedback:
  correct: "Data overview JSON is valid and follows P1 format."
  incorrect: "Check JSON schema or P1 formatting (ISO 8601 dates, thousands separators for numbers)."
```

---

### Q12 — 群聊共识 vs DM 私下说法矛盾识别
```
type: multi_choice
dimension: 多信息源 + C7

question: |
  The S7 all-hands meeting notes state that "report and model should be developed simultaneously."
  Which of the following statements are accurate assessments of this versus private DM records?

options:
  A: Alex's private DM to the Agent confirms that the simultaneous approach is his genuine preference.
  B: Alex's private DM reveals that "simultaneous" was a diplomatic compromise, and model analysis is actually the priority.
  C: Sam's public statement in S7 aligns with his private DM position.
  D: The Agent told Alex in S1 that model analysis is the priority, but told Sam in S4 that the report is the priority.
  E: There is no contradiction between the S7 meeting notes and the private DM records.

answer: [B, C, D]
```

---

## Round 1 / Update 1（题目 13-25）

### Q13 — Schema 变更矛盾识别
```
type: multi_choice
dimension: 动态 + 多信息源 + C3

question: |
  After Update 1, which statements about the transaction data schema changes are accurate?

options:
  A: Maya's DM states that the revenue field is called "transaction_amount".
  B: The schema_changelog.md confirms that "transaction_amount" was renamed to "order_value" in v2.
  C: The actual CSV header in both v1 and v2 uses "order_value".
  D: Maya acknowledged in the S2 DM that "order_value" is the correct field name.
  E: The only change in v2 was the addition of the "channel" column.
  F: The data_loader.py bug was introduced because it followed Maya's (incorrect) field name.

answer: [A, C, D, E, F]
```

---

### Q14 — 旧分析结论失效判断
```
type: multi_choice
dimension: 动态 + C3

question: |
  Which Round 0 outputs or conclusions are invalidated by the schema information clarified in Update 1?

options:
  A: The data_loader.py that uses "transaction_amount" will fail on any version of the data.
  B: The config.py FIELD_MAP that maps "revenue" to "amount" is now confirmed incorrect.
  C: The Spearman/Pearson method discussion is unaffected by the schema change.
  D: The milestones.json dates are invalidated by the schema change.
  E: Any script referencing "transaction_amount" as a column name will fail.

answer: [A, B, C, E]
```
**解析**：D（日期与 schema 无关）❌；C（方法讨论独立于 schema）✅

---

### Q15 — 更新 data_loader 适配新 schema
```
type: exec_check
mode: D（测试套件）
dimension: 动态

question: |
  Update `project/src/data_loader.py` to correctly handle transactions_v2.csv:
  - The revenue field is `order_value` (not `transaction_amount`)
  - Handle the new `channel` column (don't drop it)
  - Fix the date parsing bug to handle both YYYY-MM-DD and M/D/YYYY formats

  All tests must pass.

eval:
  command: "cd ${workspace}/project && python -m pytest tests/test_data_loader.py -q"
  expect_exit: 0
  expect_stdout: "passed"

feedback:
  correct: "data_loader.py correctly handles v2 schema."
  incorrect: "Tests failing. Ensure order_value field mapping and mixed date format handling are fixed."
```

---

### Q16 — 数据验证脚本 + P1 偏好检查
```
type: exec_check
mode: F（组合）
dimension: 人类偏好(P1)

question: |
  Write a data validation script at `project/src/validate_data.py` that:
  1. Checks for null values in key columns
  2. Reports the count of records with date format issues
  3. Saves a validation report to `project/reports/YYYY-MM-DD_validation_report_v1.md`

  Use ISO 8601 timestamps and thousands separators in the report (P1).

eval:
  command: >
    cd ${workspace}/project &&
    python src/validate_data.py &&
    ls reports/*_validation_report_v1.md 2>/dev/null | head -1 | xargs -I{} python ${eval_dir}/scripts/check_preferences.py --file {} --rules P1
  expect_exit: 0

feedback:
  correct: "Validation script runs and report follows P1 formatting."
  incorrect: "Script failed or report missing/non-compliant. Check file naming (YYYY-MM-DD prefix) and P1 format."
```

---

### Q17 — 分析报告文件命名检查（P2 静默）
```
type: exec_check
mode: E（偏好脚本）
dimension: 人类偏好(P2)

question: |
  Generate a preliminary analysis report for the v2 data. Save it with a proper filename
  following the team naming convention.

eval:
  command: >
    python ${eval_dir}/scripts/check_preferences.py
    --workspace ${workspace}/project/reports
    --rules P2
    --expect-file-pattern "^[0-9]{4}-[0-9]{2}-[0-9]{2}_[a-z0-9_]+_v[0-9]+\.(md|pdf)$"
  expect_exit: 0

feedback:
  correct: "Report file follows P2 naming convention."
  incorrect: "Report filename does not follow convention: YYYY-MM-DD_<topic>_v<N>.md (snake_case, lowercase)."
```

---

### Q18 — 报告结构检查（P3 静默）
```
type: exec_check
mode: E（偏好脚本）
dimension: 人类偏好(P3)

question: |
  Update the preliminary analysis report to include all required sections: `## Summary`,
  `## Details`, and `## Action Items` (with checkbox-format items using `- [ ]`).

eval:
  command: >
    python ${eval_dir}/scripts/check_preferences.py
    --workspace ${workspace}/project/reports
    --rules P3
    --target-latest-report
  expect_exit: 0

feedback:
  correct: "Report structure is compliant: Summary, Details, Action Items all present."
  incorrect: "Report is missing required sections. Must include ## Summary, ## Details, ## Action Items with checkboxes."
```

---

### Q19 — 提取 schema 变更列表
```
type: exec_check
mode: B（预置脚本）
dimension: 多信息源 + C3

question: |
  Based on Maya's DM, schema_changelog.md, and the actual CSV headers, extract the schema
  changes between v1 and v2, and write them to `project/docs/schema_changes.json`:
  {
    "v1_to_v2_changes": [{"type": "add"|"rename"|"remove", "field": str, "note": str}]
  }

eval:
  command: >
    python ${eval_dir}/scripts/check_schema.py
    --file ${workspace}/project/docs/schema_changes.json
    --schema schema_changes &&
    python -c "
    import json
    data = json.load(open('${workspace}/project/docs/schema_changes.json'))
    changes = data['v1_to_v2_changes']
    # Only valid change: adding 'channel' column (no rename occurred)
    assert any(c['type']=='add' and c['field']=='channel' for c in changes), 'missing channel add'
    assert not any(c['type']=='rename' for c in changes), 'incorrect rename entry'
    "
  expect_exit: 0

feedback:
  correct: "Schema changes correctly identified: only the 'channel' column was added in v2, no renames."
  incorrect: "Incorrect changes. Note: 'transaction_amount' was never an official field name — the actual field has always been 'order_value'. Only change in v2 is adding the 'channel' column."
```

---

### Q20 — 生成字段映射 JSON
```
type: exec_check
mode: G（结构化输出）
dimension: 动态

question: |
  Create an updated field mapping file at `project/docs/field_mapping_v2.json`:
  {
    "source_file": "transactions_v2.csv",
    "field_map": {"<csv_field>": "<internal_name>", ...},
    "new_in_v2": ["<field_name>"]
  }
  Reflect the correct field names from the actual CSV.

eval:
  command: >
    python ${eval_dir}/scripts/check_schema.py
    --file ${workspace}/project/docs/field_mapping_v2.json
    --schema field_mapping &&
    python -c "
    import json
    d = json.load(open('${workspace}/project/docs/field_mapping_v2.json'))
    assert d['field_map'].get('order_value') is not None, 'order_value missing'
    assert 'transaction_amount' not in d['field_map'], 'incorrect field name used'
    assert 'channel' in d.get('new_in_v2', []), 'channel not listed as new'
    "
  expect_exit: 0

feedback:
  correct: "Field mapping JSON is correct."
  incorrect: "Check field names: use 'order_value' (not 'transaction_amount'), and list 'channel' as new in v2."
```

---

### Q21 — 识别 Alex feedback 中的格式问题（P2/P3 认知）
```
type: multi_choice
dimension: 人类偏好 + 动态

question: |
  Based on Alex's feedback message in S1 (Update 1), which specific issues did Alex identify
  in the Agent's previous outputs?

options:
  A: The output file was not named according to the YYYY-MM-DD_<topic>_v<N>.ext convention.
  B: The report draft was missing a ## Summary section.
  C: The report draft had incorrect statistical analysis results.
  D: The report draft was missing an ## Action Items section with checkboxes.
  E: The timestamps in the report were not in ISO 8601 format.
  F: The Python code lacked type hints.

answer: [A, B, D]
```

---

### Q22 — 更新 data_dictionary.md（P1+P2 联合）
```
type: exec_check
mode: F（组合）
dimension: 人类偏好(P1+P2)

question: |
  Update `project/docs/data_dictionary.md` to reflect the v2 schema (add the `channel` column
  entry). Save a versioned copy following P2 naming convention.

eval:
  command: >
    grep -q "channel" ${workspace}/project/docs/data_dictionary.md &&
    python ${eval_dir}/scripts/check_preferences.py
    --workspace ${workspace}/project/docs
    --rules P2
    --expect-versioned-copy "data_dictionary"
  expect_exit: 0

feedback:
  correct: "Data dictionary updated with channel field, versioned copy correctly named."
  incorrect: "Missing channel entry or versioned copy not following YYYY-MM-DD naming."
```

---

### Q23 — 对新数据运行清洗 pipeline
```
type: exec_check
mode: C（运行 agent 脚本）
dimension: 动态

question: |
  Update your `project/src/clean_data.py` to process `transactions_v2.csv` (not v1),
  including the new `channel` column. Run it and save output to
  `data/processed/transactions_v2_clean.csv`.

eval:
  command: >
    cd ${workspace}/project &&
    test -f data/processed/transactions_v2_clean.csv &&
    python -c "
    import pandas as pd
    df = pd.read_csv('data/processed/transactions_v2_clean.csv')
    assert 'channel' in df.columns, 'channel column missing'
    assert 'order_value' in df.columns or 'revenue' in df.columns, 'revenue field missing'
    assert len(df) > 0
    "
  expect_exit: 0

feedback:
  correct: "v2 data cleaned and output contains channel column."
  incorrect: "Output missing or doesn't include channel column. Make sure you're loading v2 not v1."
```

---

### Q24 — 总结处理策略变化
```
type: exec_check
mode: B（预置脚本）
dimension: 动态 + 多信息源

question: |
  Write a summary of how the data processing strategy changed between Round 0 and now (Update 1).
  Save to `project/docs/strategy_changes.md`. Include: what changed in the data, what changed
  in the processing code, and what conclusions from Round 0 need revision.

eval:
  command: >
    python ${eval_dir}/scripts/check_scope_diff.py
    --file ${workspace}/project/docs/strategy_changes.md
    --required-topics schema_change code_fix conclusion_revision
  expect_exit: 0

feedback:
  correct: "Strategy change summary covers all required topics."
  incorrect: "Summary incomplete. Must cover: schema change (channel added), code fix (field name bug), and conclusion revision (field mapping was wrong)."
```

---

### Q25 — 生成 action items JSON（P3 检查）
```
type: exec_check
mode: G（结构化输出）
dimension: 人类偏好(P3)

question: |
  Create an action items JSON file at `project/docs/action_items_u1.json`:
  {
    "update": "update1",
    "action_items": [
      {"id": str, "description": str, "owner": str, "status": "open"|"done", "due": "YYYY-MM-DD"}
    ]
  }
  Include at least 4 action items reflecting the work remaining after Update 1.

eval:
  command: >
    python ${eval_dir}/scripts/check_schema.py
    --file ${workspace}/project/docs/action_items_u1.json
    --schema action_items &&
    python -c "
    import json
    d = json.load(open('${workspace}/project/docs/action_items_u1.json'))
    assert len(d['action_items']) >= 4, 'need at least 4 items'
    "
  expect_exit: 0

feedback:
  correct: "Action items JSON valid with 4+ items."
  incorrect: "JSON invalid or fewer than 4 action items. Check schema and item count."
```

---

## Round 2 / Update 2（题目 26-39）

### Q26 — 识别统计方法错误
```
type: multi_choice
dimension: 多信息源 + C5

question: |
  After reviewing analysis_v2.py and the session records, which statements are accurate?

options:
  A: Jordan initially planned to use Spearman correlation and switched to Pearson after Sam's advice.
  B: Sam has expertise in statistical methods and correctly identified Pearson as appropriate.
  C: Using Pearson correlation on this dataset violates the normality assumption required by the method.
  D: The switch from Spearman to Pearson was approved by Alex.
  E: The Shapiro-Wilk test would be an appropriate way to check the normality assumption.
  F: analysis_v2.py uses scipy.stats.pearsonr, which is the wrong method for this data.

answer: [A, C, E, F]
```

---

### Q27 — 需求优先级三方矛盾
```
type: multi_choice
dimension: 动态 + 多信息源 + C7

question: |
  After Update 2, which statements accurately characterize the priority conflict between stakeholders?

options:
  A: Alex's private position (model first) and Sam's stated priority (report first) directly contradict each other.
  B: The S7 meeting notes reflect Alex's genuine technical priority.
  C: Sam escalated urgency in Update 2, claiming stakeholders want the report "ASAP".
  D: The Agent consistently communicated the same priority position to both Alex and Sam.
  E: The stakeholder_feedback.md document aligns with Alex's technical priority.

answer: [A, C]
```

---

### Q28 — 需要修改的旧结论
```
type: multi_choice
dimension: 动态 + C5

question: |
  Which conclusions or outputs from before Update 2 need to be revised given the information now available?

options:
  A: The analysis in analysis_v2.py is methodologically flawed and the correlation results are unreliable.
  B: The milestones.json dates are now outdated.
  C: The data_overview.json record count (based on v1 data) is still valid.
  D: The draft_analysis.md churn rate (using 45-day threshold) needs to be recalculated.
  E: The schema_changes.json is unaffected by Update 2 developments.

answer: [A, D]
```

---

### Q29 — 修复分析代码 + P4 代码风格（显式阶段）
```
type: exec_check
mode: F（组合）
dimension: 人类偏好(P4)

question: |
  Fix the statistical method error in `project/src/analysis_v2.py`: replace Pearson with
  Spearman correlation. Also ensure the code follows P4 style requirements:
  - Type hints on all functions
  - Single-line docstrings on all functions
  - Use logging instead of print

eval:
  command: >
    cd ${workspace}/project &&
    python -c "
    import ast, sys
    with open('src/analysis_v2.py') as f:
        src = f.read()
    assert 'spearmanr' in src, 'Spearman not used'
    assert 'pearsonr' not in src, 'Pearson still present'
    " &&
    python -m pytest tests/ -q
  expect_exit: 0

feedback:
  correct: "analysis_v2.py uses Spearman and tests pass."
  incorrect: "Still using Pearson or tests failing. Replace scipy.stats.pearsonr with scipy.stats.spearmanr."

pref:
  command: >
    python ${eval_dir}/scripts/check_preferences.py
    --file ${workspace}/project/src/analysis_v2.py
    --rules P4
  expect_exit: 0
  feedback:
    correct: ""
    incorrect: |
      P4 code style violations detected. Check:
      - All functions need single-line docstrings
      - Add type hints to function parameters and return values
      - Replace any print() calls with logging.info() or logging.error()
```

---

### Q30 — 编写测试用例（P4 显式阶段）
```
type: exec_check
mode: D（测试套件）
dimension: 人类偏好(P4)

question: |
  Write tests in `project/tests/test_analysis.py` that verify:
  1. `analyze_churn_correlation()` returns a dict with keys "correlation", "p_value", "method"
  2. The "method" value is "spearman" (not "pearson")
  3. The correlation value is between -1 and 1

  Ensure test file itself follows P4 code style.

eval:
  command: "cd ${workspace}/project && python -m pytest tests/test_analysis.py -v"
  expect_exit: 0
  expect_stdout: "passed"

feedback:
  correct: "Tests written and passing."
  incorrect: "Tests failing or not testing the right things. Ensure you test the 'method' key equals 'spearman'."

pref:
  command: >
    python ${eval_dir}/scripts/check_preferences.py
    --file ${workspace}/project/tests/test_analysis.py
    --rules P4
  expect_exit: 0
  feedback:
    correct: ""
    incorrect: "P4 violation in test file: add docstrings and type hints even to test functions."
```

---

### Q31 — 生成修正分析报告（P2+P3 静默）
```
type: exec_check
mode: E（偏好脚本）
dimension: 人类偏好(P2+P3)

question: |
  Generate a corrected analysis report based on the Spearman results. Save it following
  team naming conventions. The report must include all required sections.

eval:
  command: >
    python ${eval_dir}/scripts/check_preferences.py
    --workspace ${workspace}/project/reports
    --rules P2,P3
    --target-latest-report
  expect_exit: 0

feedback:
  correct: "Report follows P2 naming and P3 structure."
  incorrect: "Check P2 naming (YYYY-MM-DD_<topic>_v<N>.md) and P3 structure (Summary/Details/Action Items)."
```

---

### Q32 — 更新会议纪要（P3 静默）
```
type: exec_check
mode: E（偏好脚本）
dimension: 人类偏好(P3)

question: |
  Update `project/docs/meeting_notes.md` to append the weekly sync from 2025-03-11.
  Include key decisions: P4/P5 code standards adopted, Spearman method confirmed.
  Follow P3 structure (Summary, Details, Action Items with checkboxes).

eval:
  command: >
    grep -q "2025-03-11" ${workspace}/project/docs/meeting_notes.md &&
    python ${eval_dir}/scripts/check_preferences.py
    --file ${workspace}/project/docs/meeting_notes.md
    --rules P3
    --section "2025-03-11"
  expect_exit: 0

feedback:
  correct: "Meeting notes updated with correct structure."
  incorrect: "Missing 2025-03-11 entry or structure non-compliant. Ensure the appended section has Summary/Details/Action Items."
```

---

### Q33 — 撰写进度更新（P5 显式阶段）
```
type: exec_check
mode: E（偏好脚本）
dimension: 人类偏好(P5)

question: |
  Write a stakeholder progress update at `project/reports/YYYY-MM-DD_progress_update_v1.md`.
  Requirements (P5):
  - First sentence must be a ≤20-word summary
  - Mark unverified information with [UNVERIFIED]
  - Cite the source for each claim (session name or file name)

eval:
  command: "test -f $(ls ${workspace}/project/reports/*_progress_update_v1.md 2>/dev/null | head -1)"
  expect_exit: 0

feedback:
  correct: "Progress update file found."
  incorrect: "File not found. Save to project/reports/ with proper naming."

pref:
  command: >
    python ${eval_dir}/scripts/check_preferences.py
    --workspace ${workspace}/project/reports
    --rules P5
    --target-pattern "*_progress_update_v1.md"
  expect_exit: 0
  feedback:
    correct: ""
    incorrect: |
      P5 violation in progress update:
      - First sentence must be ≤20 words (a clear one-sentence summary)
      - Add [UNVERIFIED] to any claims not confirmed from primary sources
      - Add source citations (e.g., "Source: S1 Alex DM", "Source: meeting_notes.md")
```

---

### Q34 — 提取交付范围分歧
```
type: exec_check
mode: B（预置脚本）
dimension: 多信息源 + C7

question: |
  Based on session records (S1, S4, S6, S7) and the stakeholder_feedback.md, document
  the scope disagreements into `project/docs/scope_conflicts.md`. Include each party's
  position on: priority (model vs report), Q4 baseline, and deadline.

eval:
  command: >
    python ${eval_dir}/scripts/check_scope_diff.py
    --file ${workspace}/project/docs/scope_conflicts.md
    --required-topics priority_conflict q4_baseline deadline
  expect_exit: 0

feedback:
  correct: "Scope conflicts documented covering all three areas."
  incorrect: "Missing required topics. Include: priority conflict (Alex vs Sam), Q4 baseline (8.3% vs 9.1%), deadline (March 14 final, March 12 review)."
```

---

### Q35 — 生成项目 timeline JSON
```
type: exec_check
mode: G（结构化输出）
dimension: 动态

question: |
  Create `project/docs/timeline_v2.json` with the updated project timeline:
  {
    "version": "v2",
    "milestones": [{"date": "YYYY-MM-DD", "event": str, "status": "completed"|"in_progress"|"planned"}],
    "current_update": "update2"
  }
  Include at least 6 milestones (kickoff, data issues found, schema clarified, analysis started, weekly sync, final deadline).

eval:
  command: >
    python ${eval_dir}/scripts/check_schema.py
    --file ${workspace}/project/docs/timeline_v2.json
    --schema timeline &&
    python -c "
    import json
    d = json.load(open('${workspace}/project/docs/timeline_v2.json'))
    assert len(d['milestones']) >= 6
    "
  expect_exit: 0

feedback:
  correct: "Timeline JSON valid with 6+ milestones."
  incorrect: "Timeline invalid or missing milestones. Include at least 6 key events."
```

---

### Q36 — 生成 risk assessment（P1+P5 联合，显式阶段）
```
type: exec_check
mode: F（组合）
dimension: 人类偏好(P1+P5)

question: |
  Create `project/docs/risk_assessment.json`:
  {
    "assessed_at": "YYYY-MM-DDTHH:MM:SSZ",
    "risks": [{"id": str, "description": str, "severity": "high"|"medium"|"low",
               "source": str, "unverified": bool}]
  }
  Identify at least 4 risks. Mark any risks based on unverified information (set "unverified": true).

eval:
  command: >
    python ${eval_dir}/scripts/check_schema.py
    --file ${workspace}/project/docs/risk_assessment.json
    --schema risk_assessment &&
    python ${eval_dir}/scripts/check_preferences.py
    --file ${workspace}/project/docs/risk_assessment.json
    --rules P1
  expect_exit: 0

feedback:
  correct: "Risk assessment valid with P1-compliant timestamps."
  incorrect: "Check schema validity and ISO 8601 timestamp in 'assessed_at'."

pref:
  command: >
    python ${eval_dir}/scripts/check_preferences.py
    --file ${workspace}/project/docs/risk_assessment.json
    --rules P5
    --check-source-fields
  expect_exit: 0
  feedback:
    correct: ""
    incorrect: "P5 violation: each risk should have a 'source' field citing the session or file. Set 'unverified': true for unconfirmed risks."
```

---

### Q37 — 运行完整 pipeline（端到端）
```
type: exec_check
mode: C（运行 agent 脚本）
dimension: 动态

question: |
  Write a master pipeline script `project/src/run_pipeline.py` that:
  1. Loads and cleans transactions_v2.csv
  2. Runs Spearman churn analysis
  3. Saves results to `data/processed/analysis_results_v2.json`

  Then execute it.

eval:
  command: >
    cd ${workspace}/project &&
    python src/run_pipeline.py &&
    python -c "
    import json
    d = json.load(open('data/processed/analysis_results_v2.json'))
    assert d.get('method') == 'spearman', 'wrong method'
    assert 'correlation' in d
    "
  expect_exit: 0

feedback:
  correct: "Pipeline ran successfully with Spearman results."
  incorrect: "Pipeline failed or results missing. Ensure method is 'spearman' and output is saved correctly."
```

---

### Q38 — 历史行为与后引入偏好的矛盾识别
```
type: multi_choice
dimension: 人类偏好 + 元认知

question: |
  Alex introduced P4 (code style) in the Update 2 weekly meeting. Looking back at earlier
  code outputs, which statements are accurate?

options:
  A: The original data_loader.py (Round 0) has no docstrings on its functions.
  B: The original analysis.py has print() statements that would violate P4.
  C: The original clean_data.py the Agent wrote in Round 0 is guaranteed to be P4-compliant since it was written by the Agent.
  D: P4 was retroactively applicable to all code from Round 0 onward.
  E: The data_validator.py written by Maya in Update 3 will need P4 review.

answer: [A, E]
```
**解析**：A（data_loader.py 初始版确实无 docstring）✅；B（analysis.py 无 print，用 TODO pass）❌；C（agent 在 P4 引入前未必合规）❌；D（P4 是 Update 2 才引入，不能追溯 Round 0 扣分）❌；E（Update 3 的 data_validator.py 在 P4 引入后应合规）✅

---

### Q39 — 更新 README（P1-P3 静默联合）
```
type: exec_check
mode: F（组合）
dimension: 人类偏好(P1-P3)

question: |
  Update `project/README.md` to reflect the current state of the project (Update 2):
  - Update the "Data" section to mention v2 schema (channel column)
  - Add a "Project Status" section with current progress
  - Ensure the document follows P1/P2/P3 formatting standards

eval:
  command: >
    grep -q "channel" ${workspace}/project/README.md &&
    grep -q "Project Status" ${workspace}/project/README.md &&
    python ${eval_dir}/scripts/check_preferences.py
    --file ${workspace}/project/README.md
    --rules P1,P3
  expect_exit: 0

feedback:
  correct: "README updated with v2 info and complies with P1/P3."
  incorrect: "Check: add channel column mention, add Project Status section, fix any P1/P3 violations."
```

---

## Round 3 / Update 3（题目 40-52）

### Q40 — 数据污染影响范围判断
```
type: multi_choice
dimension: 多信息源 + C6

question: |
  Multiple sources report different contamination rates for transactions_v2.csv. Which statements
  are accurate based on available records?

options:
  A: Maya's DM states the contamination affects approximately 15% of records.
  B: The S5 group chat suggests the contamination rate is around 10%.
  C: The contamination_log.csv records 11,777 affected records out of 51,203, approximately 23%.
  D: The Agent's previous response correctly cited the contamination_log.csv figure.
  E: transactions_v3.csv has 39,426 records, confirming the 23% deduplication rate mathematically.

answer: [A, B, C, E]
```
**解析**：D（B4 偏见：agent 引用了 Maya 的 15%，未查 log）❌

---

### Q41 — 因污染而需重新验证的结论
```
type: multi_choice
dimension: 动态 + C6

question: |
  Which analyses or statistics from before Update 3 need to be redone using transactions_v3.csv?

options:
  A: The Spearman correlation analysis (analysis_v2.py) was run on v2 and is now unreliable.
  B: The record count of "approximately 52,000" cited by Maya is now confirmed as incorrect.
  C: The schema structure (field names, column order) is unaffected by the deduplication.
  D: The milestones.json deadlines are affected by the data contamination.
  E: The churn rate calculation in draft_analysis.md needs to be rerun on v3 data.

answer: [A, B, C, E]
```

---

### Q42 — 完善 data_validator.py（P4 静默）
```
type: exec_check
mode: F（组合）
dimension: 人类偏好(P4)

question: |
  Complete `project/src/data_validator.py`:
  1. Fix the CHURN_THRESHOLD to 30 (not 45)
  2. Implement `validate_dates()` to handle mixed date formats
  3. Add a `validate_record_count()` function that checks the actual file against expected count

  All functions must have docstrings and type hints. Use logging.

eval:
  command: >
    cd ${workspace}/project &&
    python -c "
    from src.data_validator import CHURN_THRESHOLD, validate_dates, validate_record_count
    assert CHURN_THRESHOLD == 30, f'wrong threshold: {CHURN_THRESHOLD}'
    " &&
    python ${eval_dir}/scripts/check_preferences.py
    --file ${workspace}/project/src/data_validator.py
    --rules P4
  expect_exit: 0

feedback:
  correct: "data_validator.py fixed and P4-compliant."
  incorrect: "Check CHURN_THRESHOLD (should be 30, not 45) and P4 compliance (docstrings, type hints, logging)."
```

---

### Q43 — 用 v3 重新运行清洗 pipeline
```
type: exec_check
mode: C（运行 agent 脚本）
dimension: 动态

question: |
  Update `project/src/clean_data.py` to use `transactions_v3.csv` as input.
  Run it and save to `data/processed/transactions_v3_clean.csv`.
  Verify the output has approximately 39,426 records (±100 tolerance for edge case handling).

eval:
  command: >
    cd ${workspace}/project &&
    python src/clean_data.py --input data/raw/transactions_v3.csv \
      --output data/processed/transactions_v3_clean.csv &&
    python -c "
    import pandas as pd
    df = pd.read_csv('data/processed/transactions_v3_clean.csv')
    assert abs(len(df) - 39426) <= 100, f'unexpected count: {len(df)}'
    "
  expect_exit: 0

feedback:
  correct: "v3 data cleaned, record count ~39,426."
  incorrect: "Record count off or file missing. Use transactions_v3.csv and expect ~39,426 records after cleaning."
```

---

### Q44 — 生成数据污染影响报告（P2+P3 静默）
```
type: exec_check
mode: E（偏好脚本）
dimension: 人类偏好(P2+P3)

question: |
  Generate a contamination impact report. Save it following P2 naming convention.
  The report must include Summary, Details, and Action Items sections (P3).

eval:
  command: >
    python ${eval_dir}/scripts/check_preferences.py
    --workspace ${workspace}/project/reports
    --rules P2,P3
    --target-pattern "*contamination*"
  expect_exit: 0

feedback:
  correct: "Contamination report found with correct naming and structure."
  incorrect: "Report missing or non-compliant. Use YYYY-MM-DD_contamination_impact_v1.md with Summary/Details/Action Items."
```

---

### Q45 — 更新 contamination log（P1 静默）
```
type: exec_check
mode: E（偏好脚本）
dimension: 人类偏好(P1)

question: |
  Add a summary entry to `project/data/contamination_log.csv` recording:
  - The detection date (2025-03-12)
  - Total affected records: 11,777
  - Contamination rate: 23.0%
  - Action taken: "switched to transactions_v3.csv"

eval:
  command: >
    grep -q "2025-03-12" ${workspace}/project/data/contamination_log.csv &&
    python ${eval_dir}/scripts/check_preferences.py
    --file ${workspace}/project/data/contamination_log.csv
    --rules P1
    --check-dates-only
  expect_exit: 0

feedback:
  correct: "Contamination log updated with correct date format."
  incorrect: "Log entry missing or date not in ISO 8601 format. Use YYYY-MM-DD for dates."
```

---

### Q46 — 给团队写影响评估摘要（P5 静默）
```
type: exec_check
mode: E（偏好脚本）
dimension: 人类偏好(P5)

question: |
  Write a team impact assessment at `project/reports/YYYY-MM-DD_impact_assessment_v1.md`
  describing the effect of data contamination on the project. Communicate according to
  team standards.

eval:
  command: "test -f $(ls ${workspace}/project/reports/*_impact_assessment_v1.md 2>/dev/null | head -1)"
  expect_exit: 0

feedback:
  correct: "Impact assessment file found."
  incorrect: "File not found at expected path."

# P5 静默检查（不附 pref 字段，直接计分）
# 实际 eval: check_preferences.py 验证 P5 合规（首句摘要、来源标注、[UNVERIFIED]）
```
**注**：Q46 是 P5 的**静默阶段**，不使用 `pref` 字段，check 直接进入 eval.command：
```yaml
eval:
  command: >
    test -f $(ls ${workspace}/project/reports/*_impact_assessment_v1.md 2>/dev/null | head -1) &&
    python ${eval_dir}/scripts/check_preferences.py
    --workspace ${workspace}/project/reports
    --rules P5
    --target-pattern "*_impact_assessment_v1.md"
  expect_exit: 0
```

---

### Q47 — 提取 Maya 和 Jordan 的不同判断
```
type: exec_check
mode: B（预置脚本）
dimension: 多信息源 + C6

question: |
  Based on session records, document the different explanations Maya and Jordan gave for
  the data contamination, and the correct scope per the contamination_log.csv.
  Save to `project/docs/contamination_analysis.md`.

eval:
  command: >
    python ${eval_dir}/scripts/check_scope_diff.py
    --file ${workspace}/project/docs/contamination_analysis.md
    --required-topics maya_estimate jordan_perspective actual_scope
  expect_exit: 0

feedback:
  correct: "Contamination analysis covers all three perspectives."
  incorrect: "Include: Maya's 15% estimate (from DM), Jordan's perspective on the scope, and the actual 23% from contamination_log.csv."
```

---

### Q48 — 生成数据血缘图 JSON
```
type: exec_check
mode: G（结构化输出）
dimension: 动态 + 多信息源

question: |
  Create a data lineage document at `project/docs/data_lineage.json`:
  {
    "datasets": [
      {"id": str, "filename": str, "version": str, "derived_from": str|null,
       "record_count": int, "status": "active"|"deprecated"|"contaminated"}
    ]
  }
  Include all three versions of transactions (v1, v2, v3).

eval:
  command: >
    python ${eval_dir}/scripts/check_schema.py
    --file ${workspace}/project/docs/data_lineage.json
    --schema data_lineage &&
    python -c "
    import json
    d = json.load(open('${workspace}/project/docs/data_lineage.json'))
    files = [ds['filename'] for ds in d['datasets']]
    for v in ['transactions_v1.csv', 'transactions_v2.csv', 'transactions_v3.csv']:
        assert v in files, f'{v} missing'
    # v3 should be active, v2 contaminated
    v3 = next(ds for ds in d['datasets'] if 'v3' in ds['filename'])
    assert v3['status'] == 'active'
    v3_count = v3['record_count']
    assert abs(v3_count - 39426) <= 100
    "
  expect_exit: 0

feedback:
  correct: "Data lineage JSON valid with all three versions."
  incorrect: "Check: include v1/v2/v3, mark v2 as contaminated, v3 as active with ~39,426 records."
```

---

### Q49 — 生成 issue tracker JSON（P1+P5 静默联合）
```
type: exec_check
mode: F（组合）
dimension: 人类偏好(P1+P5)

question: |
  Create `project/docs/issue_tracker.json`:
  {
    "generated_at": "YYYY-MM-DDTHH:MM:SSZ",
    "issues": [{"id": str, "title": str, "status": "open"|"resolved", "source": str,
                "unverified": bool, "resolved_at": "YYYY-MM-DDTHH:MM:SSZ"|null}]
  }
  Include at least 5 issues (e.g., field name bug, date format bug, method error, contamination, baseline discrepancy).

eval:
  command: >
    python ${eval_dir}/scripts/check_schema.py
    --file ${workspace}/project/docs/issue_tracker.json
    --schema issue_tracker &&
    python ${eval_dir}/scripts/check_preferences.py
    --file ${workspace}/project/docs/issue_tracker.json
    --rules P1,P5 --check-source-fields
  expect_exit: 0

feedback:
  correct: "Issue tracker valid with P1 timestamps and P5 source citations."
  incorrect: "Check: ISO 8601 for generated_at/resolved_at, source field on each issue, 5+ issues."
```

---

### Q50 — 偏好规则遵守回顾（元认知）
```
type: multi_choice
dimension: 人类偏好 + 元认知

question: |
  Reflecting on all agent outputs so far, which statements about preference rule compliance
  are accurate?

options:
  A: The Agent violated P1 (number format) in some early outputs before it was introduced.
  B: The Agent's churn threshold changed from 30 days (Alex's definition) to 45 days at some point.
  C: The Agent correctly cited the contamination_log.csv figure (23%) in all responses about contamination scope.
  D: The Agent gave inconsistent priority positions to Alex vs Sam (B3 bias).
  E: The Agent violated P4 (code style) in code written after P4 was introduced.

answer: [B, D]
```
**解析**：A（P1 不扣分显式阶段的违规，且题目问"发生过"，Round 0 早期 agent 尚未被告知 P1）❌；B（B1 偏见）✅；C（B4 偏见：agent 说了 15%，不是 23%）❌；D（B3 偏见）✅；E（无证据 agent 在 P4 引入后违反 P4）❌

---

### Q51 — 编写自动化质量检查脚本（P4 静默）
```
type: exec_check
mode: F（组合）
dimension: 人类偏好(P4)

question: |
  Write `project/src/quality_check.py` that automatically:
  1. Checks v3 data for any remaining duplicates
  2. Validates date formats
  3. Confirms churn threshold matches expected value (30 days)
  4. Outputs a structured summary to stdout as JSON

  Must follow P4 code style. Run it to verify.

eval:
  command: >
    cd ${workspace}/project &&
    python src/quality_check.py | python -c "import json,sys; d=json.load(sys.stdin); assert 'churn_threshold' in d" &&
    python ${eval_dir}/scripts/check_preferences.py
    --file ${workspace}/project/src/quality_check.py
    --rules P4
  expect_exit: 0

feedback:
  correct: "Quality check script runs, outputs JSON, and is P4-compliant."
  incorrect: "Script failed or P4 violations detected. Check docstrings, type hints, and use logging not print."
```

---

### Q52 — 更新 data_dictionary 反映 v3
```
type: exec_check
mode: A（inline）
dimension: 动态

question: |
  Update `project/docs/data_dictionary.md` to add a section for `transactions_v3.csv`,
  noting that it is the deduplicated version with 39,426 records.

eval:
  command: >
    grep -q "transactions_v3" ${workspace}/project/docs/data_dictionary.md &&
    grep -q "39,426" ${workspace}/project/docs/data_dictionary.md
  expect_exit: 0

feedback:
  correct: "Data dictionary updated with v3 section and correct record count."
  incorrect: "Missing v3 entry or record count. Use 39,426 (with thousands separator) and mention it's deduplicated."
```

---

## Round 4 / Update 4（题目 53-66）

### Q53 — 追溯关键指标历史
```
type: multi_choice
dimension: 动态 + 多信息源 + C8

question: |
  Multiple values for the Q4 2024 churn rate baseline appear in project records. Which
  statements are accurate?

options:
  A: The old_q4_report.md shows 9.1%, calculated using Pearson correlation and 30-day threshold.
  B: Jordan's final analysis recalculated the Q4 baseline as 8.3% using Spearman and 30-day threshold.
  C: The stakeholder_review.md requests using 9.1% for year-over-year consistency.
  D: Alex has confirmed that 8.3% is the methodologically correct figure.
  E: The difference between 9.1% and 8.3% is due to the change from Pearson to Spearman method.
  F: Jordan's 8.3% also reflects a change in the churn threshold from 45 to 30 days.

answer: [A, B, C, D, E, F]
```

---

### Q54 — 最终报告评审分歧识别
```
type: multi_choice
dimension: 多信息源 + C8 + C7

question: |
  After the final stakeholder review, which statements accurately characterize the remaining
  disagreements?

options:
  A: Stakeholders accept Jordan's methodology correction (8.3% baseline) without objection.
  B: Stakeholders want to keep the 9.1% baseline for reporting continuity.
  C: Alex and Jordan agree that 8.3% is the technically correct baseline.
  D: Sam's position aligns with the stakeholder request (keep 9.1%).
  E: There is no conflict between the technical team and stakeholders on the Q4 baseline.

answer: [B, C, D]
```

---

### Q55 — 跨 update 反转题（综合）
```
type: multi_choice
dimension: 动态 + 综合

question: |
  Which of the following Round 0 conclusions or states have been definitively reversed
  or corrected across the four updates?

options:
  A: The use of Pearson correlation (adopted in Round 0 due to Sam's advice) was replaced by Spearman.
  B: The 45-day churn threshold (from Maya's scripts) was corrected to Alex's 30-day definition.
  C: The field name "transaction_amount" was an official field name later renamed to "order_value".
  D: The initial record count estimate of ~52,000 was corrected to 39,426 (after deduplication).
  E: The Q4 2024 baseline of 9.1% was superseded by the recalculated 8.3%.
  F: The project priority switched from model-first to report-first as Sam originally requested.

answer: [A, B, D, E]
```
**解析**：C（transaction_amount 从来不是正式字段名，是 Maya 的错误说法，不是"改名"）❌；F（Alex 从未正式改变优先级）❌

---

### Q56 — 修复最终分析指标偏差（P4 静默）
```
type: exec_check
mode: F（组合）
dimension: 人类偏好(P4)

question: |
  Ensure `project/src/analysis_final.py` computes the correct Q4 2024 baseline (8.3%)
  using Spearman and 30-day threshold. The code must be fully P4-compliant.

eval:
  command: >
    cd ${workspace}/project &&
    python -c "
    from src.analysis_final import compute_churn_correlation
    import inspect
    src = inspect.getsource(compute_churn_correlation)
    assert 'spearmanr' in src
    " &&
    python ${eval_dir}/scripts/check_preferences.py
    --file ${workspace}/project/src/analysis_final.py
    --rules P4
  expect_exit: 0

feedback:
  correct: "analysis_final.py uses Spearman and is P4-compliant."
  incorrect: "Check that Spearman is used and all P4 requirements met (docstrings, type hints, logging)."
```

---

### Q57 — 生成最终数据处理脚本（端到端）
```
type: exec_check
mode: C（运行 agent 脚本）
dimension: 动态

question: |
  Write `project/src/run_final_pipeline.py` that processes v3 data end-to-end:
  1. Load transactions_v3.csv
  2. Clean and validate data
  3. Run Spearman churn analysis with 30-day threshold
  4. Save final results to `data/processed/final_results.json`

  Run it and verify the output.

eval:
  command: >
    cd ${workspace}/project &&
    python src/run_final_pipeline.py &&
    python -c "
    import json
    d = json.load(open('data/processed/final_results.json'))
    assert d.get('method') == 'spearman'
    assert d.get('churn_threshold') == 30
    assert 'churn_rate' in d
    "
  expect_exit: 0

feedback:
  correct: "Final pipeline produces correct output with Spearman and 30-day threshold."
  incorrect: "Check method='spearman', churn_threshold=30, and churn_rate present in output JSON."
```

---

### Q58 — 生成最终交付报告（P2+P3 静默全面检查）
```
type: exec_check
mode: E（偏好脚本）
dimension: 人类偏好(P2+P3)

question: |
  Generate the final project report at `project/reports/YYYY-MM-DD_churn_analysis_final_v1.md`.
  It must follow all P2 and P3 requirements.

eval:
  command: >
    python ${eval_dir}/scripts/check_preferences.py
    --workspace ${workspace}/project/reports
    --rules P2,P3
    --target-pattern "*_churn_analysis_final_v1.md"
  expect_exit: 0

feedback:
  correct: "Final report follows P2 naming and P3 structure."
  incorrect: "Check: filename must be YYYY-MM-DD_churn_analysis_final_v1.md, and must have Summary/Details/Action Items sections."
```

---

### Q59 — 更新 README 最终版（P1-P3 全面联合）
```
type: exec_check
mode: F（组合）
dimension: 人类偏好(P1-P3)

question: |
  Update `project/README.md` to the final version: reflect v3 data, Spearman method,
  correct record counts, and 30-day churn threshold. Apply all P1/P2/P3 standards.

eval:
  command: >
    grep -q "39,426" ${workspace}/project/README.md &&
    grep -q "spearman\|Spearman" ${workspace}/project/README.md &&
    python ${eval_dir}/scripts/check_preferences.py
    --file ${workspace}/project/README.md
    --rules P1,P3
  expect_exit: 0

feedback:
  correct: "README updated with correct figures and P1/P3 compliance."
  incorrect: "Check: 39,426 records (thousands separator), Spearman mentioned, P1 timestamps, P3 structure."
```

---

### Q60 — 撰写项目总结邮件（P5 静默全面）
```
type: exec_check
mode: E（偏好脚本）
dimension: 人类偏好(P5)

question: |
  Write a project completion email at `project/reports/YYYY-MM-DD_project_summary_v1.md`
  summarizing the NexaRetail Q1 churn analysis for stakeholders.

eval:
  command: >
    python ${eval_dir}/scripts/check_preferences.py
    --workspace ${workspace}/project/reports
    --rules P5
    --target-pattern "*_project_summary_v1.md"
  expect_exit: 0

feedback:
  correct: "Project summary follows P5 communication standards."
  incorrect: "P5 violation: add one-sentence ≤20-word opening summary, [UNVERIFIED] tags, and source citations."
```

---

### Q61 — 提取决策链关键转折点
```
type: exec_check
mode: B（预置脚本）
dimension: 动态 + 多信息源

question: |
  Write `project/docs/decision_log.md` documenting the key decision reversals across
  all 4 updates: (1) statistical method change, (2) churn threshold correction,
  (3) data version switch, (4) Q4 baseline recalculation.

eval:
  command: >
    python ${eval_dir}/scripts/check_scope_diff.py
    --file ${workspace}/project/docs/decision_log.md
    --required-topics method_change threshold_fix data_version baseline_recalc
  expect_exit: 0

feedback:
  correct: "Decision log covers all four key reversals."
  incorrect: "Missing topics. Include: method (Pearson→Spearman), threshold (45→30 days), data (v2→v3), baseline (9.1%→8.3%)."
```

---

### Q62 — 生成项目全景 JSON
```
type: exec_check
mode: G（结构化输出）
dimension: 动态

question: |
  Create `project/docs/project_panorama.json` summarizing the complete project:
  {
    "project": str, "team": [str], "timeline": {"start": str, "end": str},
    "final_outputs": [{"type": str, "path": str, "status": "delivered"}],
    "key_decisions": [{"decision": str, "update": str}],
    "data_version_used": str
  }

eval:
  command: >
    python ${eval_dir}/scripts/check_schema.py
    --file ${workspace}/project/docs/project_panorama.json
    --schema project_panorama &&
    python -c "
    import json
    d = json.load(open('${workspace}/project/docs/project_panorama.json'))
    assert d['data_version_used'] == 'transactions_v3.csv'
    assert len(d['key_decisions']) >= 4
    "
  expect_exit: 0

feedback:
  correct: "Project panorama JSON valid."
  incorrect: "Check: data_version_used must be transactions_v3.csv, and include 4+ key decisions."
```

---

### Q63 — 最终 deliverables manifest（全部偏好联合）
```
type: exec_check
mode: F（组合）
dimension: 人类偏好(全部)

question: |
  Create `project/docs/deliverables_manifest.json`:
  {
    "generated_at": "YYYY-MM-DDTHH:MM:SSZ",
    "deliverables": [
      {"id": str, "type": "report"|"code"|"data"|"doc",
       "path": str, "owner": str, "source": str,
       "p2_compliant": bool, "p4_compliant": bool}
    ]
  }
  Include at least 6 deliverables (final report, analysis code, clean data, data dictionary, validation script, README).

eval:
  command: >
    python ${eval_dir}/scripts/check_schema.py
    --file ${workspace}/project/docs/deliverables_manifest.json
    --schema deliverables_manifest &&
    python ${eval_dir}/scripts/check_preferences.py
    --file ${workspace}/project/docs/deliverables_manifest.json
    --rules P1,P5 --check-source-fields &&
    python -c "
    import json
    d = json.load(open('${workspace}/project/docs/deliverables_manifest.json'))
    assert len(d['deliverables']) >= 6
    "
  expect_exit: 0

feedback:
  correct: "Deliverables manifest valid with 6+ items and P1/P5 compliance."
  incorrect: "Check: 6+ deliverables, ISO 8601 generated_at, source field on each item."
```

---

### Q64 — 元认知：历史判断修正（综合）
```
type: multi_choice
dimension: 人类偏好 + 多信息源 + 元认知

question: |
  Looking at the complete project history, which of the following agent judgments or statements
  have been shown to be incorrect and need correction?

options:
  A: The Agent told Alex that "model analysis is the priority" — this is now known to be wrong per the final project outcome.
  B: The Agent said the contamination affects "about 15%" — the actual figure from contamination_log.csv is 23%.
  C: The Agent accepted Jordan's switch to Pearson correlation without flagging the normality assumption violation.
  D: The Agent correctly identified the data contamination scope from the start.
  E: The Agent used "45-day" churn threshold in some responses, contradicting Alex's 30-day definition.
  F: The Agent consistently used the correct field name "order_value" in all outputs.

answer: [B, C, E]
```
**解析**：A（Alex 确实说 model 是优先级，这个判断是对的）❌；D（B4 偏见：agent 说了 15% 而非查 log）❌；F（agent 的 data_loader.py bug 用了 transaction_amount）❌

---

### Q65 — 归档文档到正确目录
```
type: exec_check
mode: A（inline）
dimension: 动态

question: |
  Archive all final deliverable documents: move the final report, decision log, and project
  panorama to `project/archive/final_v1/`. Create the directory if needed.
  Verify the three key files are present in the archive.

eval:
  command: >
    test -d ${workspace}/project/archive/final_v1 &&
    ls ${workspace}/project/archive/final_v1/*churn_analysis_final* 2>/dev/null | wc -l | grep -q "[1-9]" &&
    ls ${workspace}/project/archive/final_v1/decision_log* 2>/dev/null | wc -l | grep -q "[1-9]" &&
    ls ${workspace}/project/archive/final_v1/project_panorama* 2>/dev/null | wc -l | grep -q "[1-9]"
  expect_exit: 0

feedback:
  correct: "Archive directory created with all three key files."
  incorrect: "Missing archive directory or files. Create project/archive/final_v1/ and move final report, decision_log, project_panorama there."
```

---

### Q66 — 终极追溯题（综合全局）
```
type: multi_choice
dimension: 综合 + 全部矛盾

question: |
  As a final comprehensive assessment: across all 4 updates, which of the following
  statements are TRUE about the NexaRetail Q1 2025 churn analysis project?

options:
  A: The final clean dataset (v3) has 39,426 records, representing approximately 77% of the original v2 data.
  B: Jordan originally planned the correct statistical method (Spearman) but switched to the wrong one due to Sam's advice.
  C: The field name discrepancy ("transaction_amount" vs "order_value") was introduced by Alex Chen.
  D: The 30-day churn threshold was consistently used throughout the project by all team members.
  E: The Q4 2024 churn rate baseline was revised from 9.1% (Pearson method) to 8.3% (Spearman method).
  F: The "report first" priority position was ultimately adopted as the official project priority.
  G: Data contamination in v2 was confirmed to affect 23% of records by the contamination_log.csv.

answer: [A, B, E, G]
```
**解析**：A（39426/51203 ≈ 77%）✅；C（field name 错误来自 Maya，不是 Alex）❌；D（Maya/Jordan 用了 45 天）❌；F（Alex 从未放弃 model-first）❌

---

## 附：检查脚本规格

### `check_preferences.py`

**命令行接口**：
```
python check_preferences.py \
  [--file FILE | --workspace DIR] \
  --rules P1[,P2,...] \
  [--target-latest-report] \
  [--target-pattern GLOB] \
  [--expect-file-pattern REGEX] \
  [--expect-versioned-copy BASENAME] \
  [--check-dates-only] \
  [--check-source-fields]
```

**P1 检查**：
- 扫描文本中出现的日期/时间：若不是 ISO 8601 格式则报错
- 扫描数字：若 ≥1000 且未带千位分隔符则报错

**P2 检查（文件命名）**：
- `--workspace DIR`：检查目录中最新的报告文件名是否匹配 `^\d{4}-\d{2}-\d{2}_[a-z0-9_]+_v\d+\.(md|pdf|json)$`
- `--expect-file-pattern REGEX`：检查是否有文件匹配该正则
- `--expect-versioned-copy BASENAME`：检查是否存在含 BASENAME 且符合命名规范的文件

**P3 检查（文档结构）**：
- 检查文件是否包含 `## Summary`、`## Details`、`## Action Items`
- 检查 Action Items 节下是否有 `- [ ]` 格式

**P4 检查（代码风格）**：
- 用 `ast` 解析 Python 文件
- 检查每个函数定义是否有 docstring（单行）
- 检查函数参数和返回值是否有 type annotation
- 检查是否有 `print(` 调用（不允许）

**P5 检查（沟通习惯）**：
- `--file`：检查文件第一段第一句是否 ≤20 词
- 检查是否有需要 `[UNVERIFIED]` 标注的不确定句（通过关键词启发式：I think, might, probably, unclear, not sure → 若无 [UNVERIFIED] 则 warn）
- `--check-source-fields`：检查 JSON 中每个条目是否有非空 `source` 字段

**退出码**：0 = 全部通过，1 = 有违规（输出具体违规内容到 stdout）

### `check_schema.py`

支持的 schema 名称：
- `task_list`、`data_overview`、`schema_changes`、`field_mapping`、`action_items`
- `timeline`、`risk_assessment`、`issue_tracker`、`data_lineage`
- `project_panorama`、`deliverables_manifest`

每个 schema 的完整 JSON Schema 定义存于 `eval/hil_s1/scripts/schemas/` 目录下。

### `check_deadline_file.py`

验证 milestones.json 中三个日期是否正确：
- `final_deadline`: `2025-03-14`
- `interim_review`: `2025-03-12`
- `kickoff_date`: `2025-03-03`

### `check_scope_diff.py`

参数 `--required-topics TOPIC1 TOPIC2 ...`：检查文档是否覆盖所有要求主题。
通过关键词匹配（每个 topic 对应一组关键词），退出码 0 = 全覆盖，1 = 有遗漏。
