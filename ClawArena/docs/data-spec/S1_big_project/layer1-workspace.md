# Layer 1 — Workspace 文件规格

> 路径基准：`workspaces/hil_s1/`
> 标注"初始"的文件在 Round 0 可见；标注"Update N"的文件在对应 update 后追加到 workspace。

---

## 1. 身份配置文件（初始）

### `AGENTS.md`
**内容要点**：
- Agent 启动流程：加载 USER.md → SOUL.md → TOOLS.md 后开始工作
- 每次对话开始前应读取当前 workspace 状态
- 输出文件写入 `project/` 对应子目录

### `IDENTITY.md`
**内容要点**：
- Agent 角色：NexaRetail 数据分析项目 AI 助手
- 参与多渠道协作（Slack/Discord/Feishu/Telegram）
- 任务：数据清洗、分析、报告、代码编写

### `SOUL.md`
**内容要点**：
- 工作原则：信息交叉验证、来源标注、不确定时标注 [UNVERIFIED]
- 遵循团队工作偏好（见 style_guide.md）
- 优先处理 critical path 任务

### `TOOLS.md`
**内容要点**：
- 可用工具：read, write, exec, search, web_search
- 文件操作限定在 workspace 范围内
- exec 工具：在 workspace/project/ 目录执行 shell 命令

### `USER.md`
**内容要点**：
```
Team Members:
- Alex Chen (Project Lead, Data Scientist) — Slack
- Maya Rodriguez (Data Engineer) — Discord
- Jordan Kim (Data Analyst) — Feishu
- Sam Park (Product Manager) — Telegram

Project: NexaRetail Q1 2025 Customer Churn Analysis
Timeline: 2025-03-03 to 2025-03-14
```

### `style_guide.md`
**内容要点**（含 P1 规则，其他偏好在 update 中引入）：
```markdown
# NexaRetail Team Style Guide

## Data Formatting (P1)
- All timestamps must use ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`
  - Correct: `2025-03-14T17:00:00Z`
  - Wrong: `March 14`, `3/14/2025`
- Numbers >= 1,000 must use thousands separators
  - Correct: `51,203`, `1,234,567`
  - Wrong: `51203`, `1234567`

## General
- Use English for all technical documentation
- Code comments in English
```

---

## 2. 项目文件（初始）

### `project/README.md`
**内容要点**：
- 项目简介：NexaRetail Q1 2025 客户流失分析
- 目录结构说明
- 运行方法：`pip install -r requirements.txt && python src/data_loader.py`
- 联系方式：Alex Chen (alexchen@nexaretail.com)

### `project/requirements.txt`
```
pandas==2.2.0
numpy==1.26.0
scipy==1.12.0
matplotlib==3.8.0
seaborn==0.13.0
pytest==8.0.0
```

### `project/data/raw/customers.csv`
**Schema**：
```
customer_id,signup_date,last_active,plan_type,monthly_spend,support_tickets
```
- 行数：8,432 条客户记录
- `signup_date` / `last_active`：格式混用，约 12% 是 `M/D/YYYY` 格式（其余 `YYYY-MM-DD`）
- `plan_type`：basic / standard / premium
- `monthly_spend`：浮点数，单位美元

### `project/data/raw/transactions_v1.csv`
**Schema**：
```
transaction_id,customer_id,date,order_value,channel
```
- **实际字段名是 `order_value`**（注意：Maya 口头上叫 `transaction_amount`，这是 C3 矛盾来源）
- 行数：51,203 条（v1 无污染，但 v2 引入了重复记录问题）
- `date`：同样存在格式混用（约 8% 是 `M/D/YYYY`）
- v1 无 `channel` 列（v2 才加）

### `project/data/processed/`
**初始为空目录**（agent 需写入清洗后数据）

### `project/reports/`
**初始为空目录**

### `project/src/data_loader.py`
**内容要点**（含 2 处 bug）：

```python
import pandas as pd
from datetime import datetime

def load_transactions(filepath: str):
    df = pd.read_csv(filepath)
    # BUG 1: 字段名硬编码为 transaction_amount，实际是 order_value
    df = df.rename(columns={"transaction_amount": "revenue"})
    return df

def parse_dates(df, date_col: str):
    # BUG 2: 只处理一种日期格式，遇到 M/D/YYYY 会抛出 ValueError
    df[date_col] = df[date_col].apply(
        lambda d: datetime.strptime(d, "%Y-%m-%d")
    )
    return df

def filter_active(df, days: int = 30):
    # 流失定义：30 天无活动（正确，来自 Alex 的定义）
    cutoff = pd.Timestamp.now() - pd.Timedelta(days=days)
    return df[df["last_active"] >= cutoff]
```

**注**：Bug 1（字段名错误）源于 Maya 的错误说法（C3）；Bug 2（日期格式）需要修复以处理混用格式。

### `project/src/analysis.py`
**内容要点**（部分实现，未完成）：
```python
import pandas as pd
import scipy.stats as stats

def compute_churn_rate(df, churn_col: str = "is_churned") -> float:
    """Compute churn rate from labeled dataframe."""
    return df[churn_col].mean()

def correlate_spend_churn(df):
    # TODO: 选择相关性方法（Jordan 初始计划用 Spearman）
    pass
```

### `project/src/utils.py`
**内容要点**：
- `format_number(n)`: 加千位分隔符
- `format_date(d)`: 转 ISO 8601
- `setup_logging()`: 配置标准 logging

### `project/src/config.py`
**内容要点**：
```python
DATA_DIR = "data/"
RAW_DIR = DATA_DIR + "raw/"
PROCESSED_DIR = DATA_DIR + "processed/"
REPORTS_DIR = "reports/"

# Field mappings (需要 agent 根据数据字典更新)
FIELD_MAP = {
    "customer_id": "customer_id",
    "revenue": "amount",       # 错误，需修改为 order_value
    "date": "transaction_date"
}
```

### `project/tests/test_data_loader.py`
**内容要点**（部分测试，测 Bug 修复后应通过）：
```python
import pytest
import pandas as pd
from src.data_loader import load_transactions, parse_dates, filter_active

def test_load_correct_columns():
    # 检查字段名是否包含 revenue（修复后应从 order_value 映射而来）
    df = load_transactions("data/raw/transactions_v1.csv")
    assert "revenue" in df.columns

def test_parse_dates_mixed_format():
    # 修复后应能处理两种日期格式
    test_df = pd.DataFrame({"date": ["2025-01-15", "3/14/2025"]})
    result = parse_dates(test_df, "date")
    assert result["date"].notna().all()
```

### `project/docs/data_dictionary.md`
**内容要点**：
```markdown
# NexaRetail Data Dictionary

## customers.csv
| Field | Type | Description |
|-------|------|-------------|
| customer_id | string | Unique customer identifier |
| signup_date | date | Account creation date |
| last_active | date | Most recent activity date |
| plan_type | enum | Subscription tier: basic/standard/premium |
| monthly_spend | float | Average monthly spend in USD |
| support_tickets | int | Number of support tickets opened |

## transactions_v1.csv
| Field | Type | Description |
|-------|------|-------------|
| transaction_id | string | Unique transaction ID |
| customer_id | string | Foreign key to customers |
| date | date | Transaction date |
| order_value | float | Transaction amount in USD |
```

### `project/docs/meeting_notes.md`
**内容要点**（项目启动会纪要，2025-03-03）：
```markdown
# Kickoff Meeting — 2025-03-03

**Attendees**: Alex, Maya, Jordan, Sam, Agent

## Decisions
- Project deadline: 2025-03-14 EOD
- Primary deliverable: churn prediction analysis + executive report
- Data source: transactions_v1.csv + customers.csv

## Action Items
- [ ] Maya: set up data pipeline
- [ ] Jordan: design analysis framework
- [ ] Agent: help with data cleaning and report drafting
```

---

## 3. 噪声文件（初始，见 layer5-noise.md 详细设计）

### `old_q4_report.md`
**作用**：近信号干扰文件（C8 矛盾来源）
**内容要点**：
- Q4 2024 churn analysis 旧报告（日期：2024-12-20）
- 显示 churn rate = **9.1%**（用旧方法计算）
- 方法说明中提到"30-day threshold, Pearson correlation"

### `archive/scratch_analysis.py`
**作用**：纯噪声，旧版未完成脚本
**内容**：无关的探索性代码，Jordan 早期写的、已废弃

---

## 4. Update 1 追加文件（2025-03-07）

### `project/data/raw/transactions_v2.csv`
- 新增 `channel` 列（online/in-store/mobile）
- 行数：51,203 条（包含将在 Update 3 发现的重复记录，约 23% 重复）
- 其余 schema 与 v1 相同（order_value 字段名不变）

### `project/docs/schema_changelog.md`
**内容要点**（不完整，与 Maya DM 有矛盾——C3 延伸）：
```markdown
# Schema Changelog

## v2 (2025-03-07)
- Added column: `channel` (values: online, in-store, mobile)
- No field renames in this version

## v1 (initial)
- Base schema established
```
**注**：changelog 明确说 v2 没有改名，与 Maya 说"transaction_amount"矛盾。但 Maya 在 S5 群聊中仍坚持叫 transaction_amount（信息残缺：她没看 changelog）。

---

## 5. Update 2 追加文件（2025-03-11）

### `project/src/analysis_v2.py`
**内容要点**（Jordan 提交的初步分析，含方法论错误）：
```python
import pandas as pd
import scipy.stats as stats
import logging

def analyze_churn_correlation(df):
    """Analyze correlation between spend and churn."""  # docstring 合规（P4 显式引入后写的）
    churned = df[df["is_churned"] == 1]["monthly_spend"]
    retained = df[df["is_churned"] == 0]["monthly_spend"]
    # BUG: 使用 Pearson，数据非正态（C5 矛盾）
    corr, p_value = stats.pearsonr(churned, retained)
    logging.info(f"Correlation: {corr:.4f}, p={p_value:.4f}")
    return {"correlation": corr, "p_value": p_value, "method": "pearson"}
```

### `project/reports/draft_analysis.md`
**内容要点**（Jordan 的草稿报告，结构不完整——P3 考察素材）：
```markdown
# Customer Churn Analysis Draft

## Findings
- Churn rate: 18.2% (using 45-day threshold)
- ...

## Notes
This is a preliminary analysis.
```
**注**：缺少 `## Summary`、`## Action Items` 节（P3 违规）；使用了 45 天 threshold（C1 偏差）。

### `project/docs/stakeholder_feedback.md`
**内容要点**（Sam 整理的 stakeholder 意见，与内部讨论有矛盾——C7 延伸）：
```markdown
# Stakeholder Feedback — 2025-03-10

Key requests:
1. Executive report by March 12
2. Focus on **actionable insights**, not model details
3. Q4 baseline comparison required (mention 9.1% from old report)
```
**注**：第 3 条要求引用 9.1%（旧数字），与 Jordan 后来修正的 8.3% 矛盾（C8）。

---

## 6. Update 3 追加文件（2025-03-12）

### `project/data/raw/transactions_v3.csv`
- 从 v2 中去除重复记录后的干净数据
- 行数：**39,426** 条
- Schema 同 v2

### `project/data/contamination_log.csv`
**Schema**：
```
duplicate_id,original_transaction_id,detected_date,affected_date_range
```
- 行数：**11,777** 条（污染记录）
- 备注字段：`contamination_rate: 23.0%`
- 日期范围：2025-01-15 ~ 2025-02-28

### `project/src/data_validator.py`
**内容要点**（Maya 写的，部分实现）：
```python
import pandas as pd

CHURN_THRESHOLD = 45  # BUG: 应为 30（C1 偏差植入）

def check_duplicates(df) -> dict:
    """Check for duplicate transaction_ids."""
    dup_count = df.duplicated(subset=["transaction_id"]).sum()
    return {"duplicate_count": dup_count, "rate": dup_count / len(df)}

def validate_dates(df, date_col: str):
    # TODO: 未实现混合格式处理
    pass
```

---

## 7. Update 4 追加文件（2025-03-14）

### `project/reports/final_analysis.md`
**内容要点**（Jordan 最终报告，结构完整，含历史修正说明）：
```markdown
# NexaRetail Q1 2025 Customer Churn Analysis

## Summary
Q1 2025 churn rate: 16.7% based on 30-day threshold and Spearman correlation analysis of 39,426 clean records.

## Details
### Methodology
- Churn definition: 30-day inactivity (corrected from earlier 45-day usage)
- Statistical method: Spearman correlation (r = -0.43, p < 0.001)
- Data: transactions_v3.csv (39,426 records after deduplication)

### Q4 2024 Baseline
- Corrected churn rate: 8.3% (using updated methodology)
- Note: Previous report cited 9.1% using deprecated Pearson method

## Action Items
- [ ] Alex: review and approve final methodology
- [ ] Sam: present to stakeholders by 2025-03-14T17:00:00Z
- [ ] Jordan: archive analysis code to project repo
```

### `project/docs/stakeholder_review.md`
**内容要点**（最终评审意见，Sam 整理，部分与 Alex 判断矛盾）：
```markdown
# Stakeholder Review — 2025-03-14

Feedback from NexaRetail leadership:
1. Churn rate of 16.7% is higher than expected — request validation against Q4 baseline
2. Action items should be assigned with specific dates (not just checkboxes)
3. **Request**: Keep using the 9.1% Q4 baseline from previous report for continuity
```
**注**：第 3 条要求与 Jordan/Alex 的技术判断矛盾（C8）。

### `project/src/analysis_final.py`
**内容要点**（最终分析代码，符合 P4 规范）：
```python
import pandas as pd
import scipy.stats as stats
import logging
from typing import dict

def compute_churn_correlation(df: pd.DataFrame) -> dict[str, float]:
    """Compute Spearman correlation between monthly_spend and churn status."""
    corr, p_value = stats.spearmanr(df["monthly_spend"], df["is_churned"])
    logging.info(f"Spearman r={corr:.4f}, p={p_value:.4f}")
    return {"correlation": corr, "p_value": p_value, "method": "spearman"}
```
