# HIL-S1 数据造数工作综述

> **Test ID**：`hil_s1`
> 本文件是全新窗口的完整工作入口。阅读本文件（及同目录 spec 文件）后无需回溯历史对话。

---

## 任务概述

**目标**：为 hbench trace benchmark 造一个完整场景的数据，task ID 为 `hil_s1`。

**场景**：小型工程团队（4 人 + AI Agent）使用 AI 协作完成 NexaRetail Q1 2025 客户流失分析项目，历时约 2 周（2025-03-03 ~ 2025-03-14）。考察三个维度：**多信息源**（8 条矛盾）、**动态**（4 次 update）、**人类偏好**（P1-P5 渐进注入）。

**总体规模**：66 道题，~700k tokens，7 个 session，4 次 update。

---

## Spec 文件索引（必读顺序）

| 文件 | 内容摘要 |
|------|---------|
| **本文件** | 数据路径、执行步骤、格式规格 |
| [layer0-narrative.md](./layer0-narrative.md) | **造数据真相基准**：项目时间线、角色详情、8 条矛盾 map（每条含来源/真相/偏差标注）、4 处 agent 偏见（B1-B4，含植入位置）、P1-P5 偏好注入弧 |
| [layer1-workspace.md](./layer1-workspace.md) | 所有 workspace 文件路径、关键内容要点（含代码片段）、加入时机 |
| [layer2-sessions.md](./layer2-sessions.md) | 7 个 session（4 DM + 3 群聊）各 Phase 的逐 loop 对话设计 |
| [layer3-eval.md](./layer3-eval.md) | 66 道题完整设计（选项/答案/解析/eval command/pref 字段）+ 检查脚本规格 |
| [layer4-dynamic.md](./layer4-dynamic.md) | 4 次 update 的 action 规格（JSON 格式）、source 文件清单、题目与 update 对应表 |
| [layer5-noise.md](./layer5-noise.md) | 噪声设计：session 闲聊分布、2 个近信号干扰文件（old_q4_report.md 等） |

---

## 数据路径结构

所有数据文件位于 `./data/clawarena/`，相对于该目录：

```
data/hbench/
├── tests.json                                     # 追加 hil_s1 条目
├── eval/hil_s1/
│   ├── questions.json                             # 66 道题
│   └── scripts/                                   # 检查脚本
│       ├── check_preferences.py
│       ├── check_schema.py
│       ├── check_deadline_file.py
│       ├── check_scope_diff.py
│       └── schemas/                               # JSON schema 定义文件
└── openclaw/
    ├── manifest.json                              # 追加 hil_s1 agents/updates 条目
    ├── workspaces/hil_s1/                         # workspace 初始文件
    │   ├── AGENTS.md
    │   ├── IDENTITY.md
    │   ├── SOUL.md
    │   ├── TOOLS.md
    │   ├── USER.md
    │   ├── style_guide.md
    │   ├── old_q4_report.md                       # 噪声（近信号干扰）
    │   ├── archive/
    │   │   ├── old_pipeline_config.json           # 噪声（近信号干扰）
    │   │   ├── scratch_analysis.py                # 纯噪声
    │   │   └── q3_2024_notes.md                   # 纯噪声
    │   ├── misc/
    │   │   ├── team_directory.md
    │   │   └── onboarding_checklist.md
    │   └── project/
    │       ├── README.md
    │       ├── requirements.txt
    │       ├── data/raw/
    │       │   ├── customers.csv
    │       │   └── transactions_v1.csv
    │       ├── data/processed/          # 初始为空
    │       ├── reports/                 # 初始为空
    │       ├── src/
    │       │   ├── data_loader.py       # 含 2 个 bug（见 layer1）
    │       │   ├── analysis.py
    │       │   ├── utils.py
    │       │   └── config.py
    │       ├── tests/
    │       │   └── test_data_loader.py
    │       └── docs/
    │           ├── data_dictionary.md
    │           └── meeting_notes.md
    ├── state/agents/hil_s1/
    │   └── sessions/
    │       ├── sessions.json                      # session 注册表（由脚本生成）
    │       ├── alex_slack_5ba4976f-...jsonl        # S1
    │       ├── maya_discord_26597928-...jsonl      # S2
    │       ├── jordan_feishu_0c923eb4-...jsonl     # S3
    │       ├── sam_telegram_5609fa34-...jsonl      # S4
    │       ├── data_engineering_slack_d84ae024-...jsonl  # S5
    │       ├── analysis_report_discord_15916984-...jsonl # S6（初始为空壳）
    │       └── all_hands_feishu_e0f00482-...jsonl  # S7
    └── updates/hil_s1/
        ├── upd1_sessions/               # Update 1 session appends
        ├── upd1_workspace/              # Update 1 workspace 新文件
        ├── upd2_sessions/
        ├── upd2_workspace/
        ├── upd3_sessions/
        ├── upd3_workspace/
        ├── upd4_sessions/
        └── upd4_workspace/
```

**中间文件目录**（不进入最终数据）：
```
data-synthesis/
├── session_builder.py                 # 通用构建工具（见下节）
└── hil_s1/
    ├── session_ids.json               # 固定 session UUID（勿修改）
    ├── assemble.sh                    # 一键构建所有 session jsonl
    ├── register_sessions.py           # 生成 sessions.json 注册表
    └── loops/                         # session 中间 JSON（由造数者创建）
        ├── s1_alex_dm_p1.json
        ├── s1_alex_dm_p2.json
        ├── s1_alex_dm_p3.json
        ├── s2_maya_dm_p1.json
        ├── ... （共 ~20 个 loops JSON 文件）
        └── s6_analysis_report_group_placeholder.json
```

---

## 固定 Session ID 表

**必须使用以下 session ID**（已固定，修改会导致 manifest.json 和 assemble.sh 不一致）：

| Session | 参与者 | Channel | Session ID |
|---------|--------|---------|-----------|
| S1 | Alex ↔ Agent | Slack DM | `alex_slack_5ba4976f-e34a-4fee-ad19-c39c49aecc59` |
| S2 | Maya ↔ Agent | Discord DM | `maya_discord_26597928-810c-4a52-ab0e-147b488c166c` |
| S3 | Jordan ↔ Agent | Feishu DM | `jordan_feishu_0c923eb4-2888-4e40-afb0-af6f5f3e8117` |
| S4 | Sam ↔ Agent | Telegram DM | `sam_telegram_5609fa34-0f8b-4530-a9e3-12a6cdb81037` |
| S5 | Alex+Maya+Agent | Slack `#data-engineering` | `data_engineering_slack_d84ae024-69c3-4679-bc3b-d1dffafab625` |
| S6 | Jordan+Sam+Agent | Discord `#analysis-report` | `analysis_report_discord_15916984-6100-4314-96d8-5819af6c77fe` |
| S7 | 全员+Agent | Feishu `#all-hands` | `all_hands_feishu_e0f00482-67c2-4108-beac-276d95c0ff22` |

---

## 需要修改的配置文件

### A. 追加 `tests.json` 条目

文件：`./data/clawarena/tests.json`

在 `"tests"` 数组末尾追加：
```json
{
  "id": "hil_s1",
  "desc": "NexaRetail Q1 2025 customer churn analysis — 4-person engineering team with AI agent, 8 contradictions across 7 sessions, 4 dynamic updates, 5 progressive preference rules (P1-P5)",
  "eval": "hil_s1"
}
```

### B. 追加 `manifest.json` 条目

文件：`./data/clawarena/openclaw/manifest.json`

在 `"agents"` 字段中追加：
```json
"hil_s1": {
  "agent_id": "hil_s1",
  "agent_dir": "state/agents/hil_s1",
  "session": "main_7643b677-948c-4211-a390-b6f32e16d58d",
  "history_sessions": [
    "alex_slack_5ba4976f-e34a-4fee-ad19-c39c49aecc59",
    "maya_discord_26597928-810c-4a52-ab0e-147b488c166c",
    "jordan_feishu_0c923eb4-2888-4e40-afb0-af6f5f3e8117",
    "sam_telegram_5609fa34-0f8b-4530-a9e3-12a6cdb81037",
    "data_engineering_slack_d84ae024-69c3-4679-bc3b-d1dffafab625",
    "analysis_report_discord_15916984-6100-4314-96d8-5819af6c77fe",
    "all_hands_feishu_e0f00482-67c2-4108-beac-276d95c0ff22"
  ],
  "workspace": "workspaces/hil_s1"
}
```

在 `"updates"` 字段中追加：

> **格式说明**：session 更新均为 `action: "append"`（追加至已有 session），workspace 更新均为 `action: "new"`（新增文件）。`action: "new"` 的 session 条目需提供 `channel` 字段；`append` 不需要。

```json
"hil_s1": {
  "upd1_sessions": {
    "type": "session",
    "dir": "updates/hil_s1/upd1_sessions",
    "files": [
      {"name": "alex_slack_5ba4976f-e34a-4fee-ad19-c39c49aecc59.jsonl", "action": "append"},
      {"name": "maya_discord_26597928-810c-4a52-ab0e-147b488c166c.jsonl", "action": "append"},
      {"name": "data_engineering_slack_d84ae024-69c3-4679-bc3b-d1dffafab625.jsonl", "action": "append"}
    ]
  },
  "upd1_workspace": {
    "type": "workspace",
    "dir": "updates/hil_s1/upd1_workspace",
    "files": [
      {"name": "project/data/raw/transactions_v2.csv", "action": "new"},
      {"name": "project/docs/schema_changelog.md", "action": "new"}
    ]
  },
  "upd2_sessions": {
    "type": "session",
    "dir": "updates/hil_s1/upd2_sessions",
    "files": [
      {"name": "jordan_feishu_0c923eb4-2888-4e40-afb0-af6f5f3e8117.jsonl", "action": "append"},
      {"name": "sam_telegram_5609fa34-0f8b-4530-a9e3-12a6cdb81037.jsonl", "action": "append"},
      {"name": "analysis_report_discord_15916984-6100-4314-96d8-5819af6c77fe.jsonl", "action": "append"},
      {"name": "all_hands_feishu_e0f00482-67c2-4108-beac-276d95c0ff22.jsonl", "action": "append"}
    ]
  },
  "upd2_workspace": {
    "type": "workspace",
    "dir": "updates/hil_s1/upd2_workspace",
    "files": [
      {"name": "project/src/analysis_v2.py", "action": "new"},
      {"name": "project/reports/draft_analysis.md", "action": "new"},
      {"name": "project/docs/stakeholder_feedback.md", "action": "new"}
    ]
  },
  "upd3_sessions": {
    "type": "session",
    "dir": "updates/hil_s1/upd3_sessions",
    "files": [
      {"name": "alex_slack_5ba4976f-e34a-4fee-ad19-c39c49aecc59.jsonl", "action": "append"},
      {"name": "maya_discord_26597928-810c-4a52-ab0e-147b488c166c.jsonl", "action": "append"},
      {"name": "data_engineering_slack_d84ae024-69c3-4679-bc3b-d1dffafab625.jsonl", "action": "append"}
    ]
  },
  "upd3_workspace": {
    "type": "workspace",
    "dir": "updates/hil_s1/upd3_workspace",
    "files": [
      {"name": "project/data/raw/transactions_v3.csv", "action": "new"},
      {"name": "project/data/contamination_log.csv", "action": "new"},
      {"name": "project/src/data_validator.py", "action": "new"}
    ]
  },
  "upd4_sessions": {
    "type": "session",
    "dir": "updates/hil_s1/upd4_sessions",
    "files": [
      {"name": "jordan_feishu_0c923eb4-2888-4e40-afb0-af6f5f3e8117.jsonl", "action": "append"},
      {"name": "sam_telegram_5609fa34-0f8b-4530-a9e3-12a6cdb81037.jsonl", "action": "append"},
      {"name": "analysis_report_discord_15916984-6100-4314-96d8-5819af6c77fe.jsonl", "action": "append"},
      {"name": "all_hands_feishu_e0f00482-67c2-4108-beac-276d95c0ff22.jsonl", "action": "append"}
    ]
  },
  "upd4_workspace": {
    "type": "workspace",
    "dir": "updates/hil_s1/upd4_workspace",
    "files": [
      {"name": "project/reports/final_analysis.md", "action": "new"},
      {"name": "project/docs/stakeholder_review.md", "action": "new"},
      {"name": "project/src/analysis_final.py", "action": "new"}
    ]
  }
}
```

---

## questions.json 结构规格

文件：`data/hbench/eval/hil_s1/questions.json`

```json
{
  "id": "hil_s1",
  "desc": "NexaRetail Q1 2025 customer churn analysis — ...",
  "rounds": [
    {
      "id": "r1",
      "type": "multi_choice",
      "question": "...",
      "eval": {
        "options": {"A": "...", "B": "...", "C": "...", "D": "...", "E": "...", "F": "..."},
        "answer": ["A", "B", "D", "E"]
      },
      "feedback": {
        "correct": "...",
        "options": {"C": "C is wrong because...", "F": "F is wrong because..."}
      },
      "update_ids": []
    },
    ...
    {
      "id": "r13",
      "type": "multi_choice",
      "question": "...",
      "eval": { ... },
      "feedback": { ... },
      "update_ids": ["upd1_sessions", "upd1_workspace"]
    },
    ...
  ]
}
```

**update_ids 触发规则**（来自 layer4-dynamic.md）：

| 题目范围 | update_ids（第一道题设置，后续题为空） |
|---------|--------------------------------------|
| Q1-Q12 | `[]` |
| **Q13**（第一道） | `["upd1_sessions", "upd1_workspace"]` |
| Q14-Q25 | `[]` |
| **Q26**（第一道） | `["upd2_sessions", "upd2_workspace"]` |
| Q27-Q39 | `[]` |
| **Q40**（第一道） | `["upd3_sessions", "upd3_workspace"]` |
| Q41-Q52 | `[]` |
| **Q53**（第一道） | `["upd4_sessions", "upd4_workspace"]` |
| Q54-Q66 | `[]` |

---

## Session 中间格式规格

造数者需要创建 `data-synthesis/hil_s1/loops/` 下的 JSON 中间文件，`session_builder.py` 负责将其转换为 jsonl。

### 基本结构

```json
{
  "session_meta": {
    "channel": "slack",
    "participant": "alex",
    "group_name": null
  },
  "loops": [
    {
      "user": {
        "speaker": "Alex",
        "text": "用户消息内容（纯文本，不含 envelope 前缀，builder 自动加）"
      },
      "turns": [
        {
          "assistant": {
            "thinking": "可选，agent 思考过程",
            "text": "可选，mid-turn 说明文字",
            "tools": [
              {
                "id": "call_001",
                "name": "read",
                "args": {"file_path": "style_guide.md"}
              }
            ]
          },
          "results": [
            {
              "tool_id": "call_001",
              "file": "style_guide.md",
              "is_error": false
            }
          ]
        },
        {
          "assistant": {
            "text": "最终回复（无 tools 字段或 tools 为空列表）"
          }
        }
      ]
    }
  ]
}
```

### 规则

- **`loops`**：每个元素是一次完整的 user → agent 交互
- **`turns`**：agent 的多轮处理（工具调用→工具结果→最终回复）；最后一个 turn 的 `assistant` 无 `tools`，代表最终回复
- **每个 turn 若有 `tools`，必须有对应的 `results`**，`tool_id` 一一对应
- **`results` 引用方式**：
  - `{"tool_id": "...", "file": "project/src/data_loader.py", "is_error": false}` → builder 自动 inline 文件内容
  - `{"tool_id": "...", "content": "直接给出文本", "is_error": false}` → 用于非文件工具结果（exec 输出等）
- **DM session**：`group_name: null`，builder 自动加 DM envelope 前缀
- **群聊 session**：`group_name` 非 null（如 `"data-engineering"`），builder 自动加群聊 envelope 前缀（含时间戳）

### Group Session 示例

```json
{
  "session_meta": {
    "channel": "slack",
    "group_name": "data-engineering"
  },
  "loops": [
    {
      "user": {
        "speaker": "Maya",
        "text": "Hey team, quick schema check — the revenue field, is it transaction_amount?"
      },
      "turns": [
        {
          "assistant": {
            "tools": [
              {"id": "call_001", "name": "read", "args": {"file_path": "project/data/raw/transactions_v1.csv"}}
            ]
          },
          "results": [
            {"tool_id": "call_001", "content": "transaction_id,customer_id,date,order_value,channel\n...", "is_error": false}
          ]
        },
        {
          "assistant": {
            "text": "Confirmed: the CSV header shows `order_value`. The schema_changelog also doesn't mention any rename."
          }
        }
      ]
    }
  ]
}
```

### S6 占位符文件

S6（analysis-report 群聊）Phase 1 无内容（首次消息在 Update 2），需创建一个最小占位符文件：

```json
{
  "session_meta": {
    "channel": "discord",
    "group_name": "analysis-report"
  },
  "loops": []
}
```

保存为 `data-synthesis/hil_s1/loops/s6_analysis_report_group_placeholder.json`。

---

## Channel Envelope 格式参考

Builder 自动处理，但造数者需了解最终格式：

| Session 类型 | Channel | 用户消息格式 |
|------------|---------|------------|
| DM | Slack | `[Slack Alex Mon Mar 03 09:00:00 CST 2025] 消息内容` |
| DM | Discord | `[Discord Maya Mon Mar 03 09:30:00 CST 2025] 消息内容` |
| DM | Feishu | `[Feishu Jordan Mon Mar 03 10:00:00 CST 2025] 消息内容` |
| DM | Telegram | `[Telegram Sam Mon Mar 03 11:00:00 CST 2025] 消息内容` |
| 群聊 | Slack | `[Slack #data-engineering Thu Mar 06 14:00:00 CST 2025] Maya: 消息内容` |
| 群聊 | Discord | `[Discord #analysis-report Tue Mar 11 10:00:00 CST 2025] Jordan: 消息内容` |
| 群聊 | Feishu | `[Feishu #all-hands Mon Mar 03 16:00:00 CST 2025] Alex: 消息内容` |

---

## 执行步骤

### Step 1：创建 workspace 初始文件

按 [layer1-workspace.md](./layer1-workspace.md) 规格，在 `data/hbench/openclaw/workspaces/hil_s1/` 下创建所有初始文件。

**重要**：
- `data_loader.py` 必须包含 2 处 bug（字段名 `transaction_amount`、日期格式单一处理）
- `style_guide.md` 必须包含完整 P1 规则（ISO 8601 + 千位分隔符）
- `old_q4_report.md`（根目录，显眼位置）必须显示 Q4 churn rate = **9.1%**（C8 矛盾干扰项）

### Step 2：创建 loops 中间 JSON

按 [layer2-sessions.md](./layer2-sessions.md) 规格，为每个 session 的每个 Phase 创建 loops JSON：

| 文件名 | 对应 |
|--------|------|
| `loops/s1_alex_dm_p1.json` | S1 Phase 1（初始，Q1-Q12 可见） |
| `loops/s1_alex_dm_p2.json` | S1 Phase 2（Update 1 追加） |
| `loops/s1_alex_dm_p3.json` | S1 Phase 3（Update 3 追加） |
| `loops/s2_maya_dm_p1.json` | S2 Phase 1 |
| `loops/s2_maya_dm_p2.json` | S2 Phase 2（Update 1 追加） |
| `loops/s2_maya_dm_p3.json` | S2 Phase 3（Update 3 追加） |
| `loops/s3_jordan_dm_p1.json` | S3 Phase 1 |
| `loops/s3_jordan_dm_p2.json` | S3 Phase 2（Update 2 追加） |
| `loops/s3_jordan_dm_p3.json` | S3 Phase 3（Update 4 追加） |
| `loops/s4_sam_dm_p1.json` | S4 Phase 1 |
| `loops/s4_sam_dm_p2.json` | S4 Phase 2（Update 2 追加） |
| `loops/s4_sam_dm_p3.json` | S4 Phase 3（Update 4 追加） |
| `loops/s5_data_eng_group_p1.json` | S5 Phase 1 |
| `loops/s5_data_eng_group_p2.json` | S5 Phase 2（Update 1 追加） |
| `loops/s5_data_eng_group_p3.json` | S5 Phase 3（Update 3 追加） |
| `loops/s6_analysis_report_group_placeholder.json` | S6 占位符（空 loops） |
| `loops/s6_analysis_report_group_p2.json` | S6 Phase 2（Update 2 追加） |
| `loops/s6_analysis_report_group_p3.json` | S6 Phase 3（Update 4 追加） |
| `loops/s7_all_hands_group_p1.json` | S7 Phase 1 |
| `loops/s7_all_hands_group_p2.json` | S7 Phase 2（Update 2 追加，P4/P5 引入） |
| `loops/s7_all_hands_group_p3.json` | S7 Phase 3（Update 4 追加，项目回顾） |

**造数约束（必须遵守）**：
1. 矛盾措辞见 layer0-narrative.md §4，每条矛盾的「偏差」说法须精确植入对应 session/角色
2. Agent 偏见 B1-B4 在 layer0-narrative.md §5 指定的位置植入，措辞须清晰体现偏见（不能含糊）
3. P1-P5 偏好规则见 layer0-narrative.md §6，在指定 session/轮次首次引入，引入前 agent 不应提及这些规则
4. Tool call 密度：DM session ~35% agent 回复含 tool call，群聊 ~20%
5. 噪声分布见 layer5-noise.md，闲聊穿插在关键内容之间

### Step 3：运行 assemble.sh 构建 session jsonl

```bash
cd ./data-synthesis
bash hil_s1/assemble.sh
```

**前提**：Step 1 和 Step 2 已完成（workspace 文件存在，loops JSON 已创建）。

### Step 4：生成 sessions.json 注册表

```bash
cd ./data-synthesis
python hil_s1/register_sessions.py
```

### Step 5：创建 update workspace 文件

按 layer1-workspace.md 各 update 节的规格，将 workspace 新增文件放入对应目录：

```bash
# Update 1 workspace 文件
data/hbench/openclaw/updates/hil_s1/upd1_workspace/
├── project/data/raw/transactions_v2.csv         # 51,203 行，含 channel 列，含污染
└── project/docs/schema_changelog.md             # 说明 v2 只加了 channel 列，无改名

# Update 2 workspace 文件
data/hbench/openclaw/updates/hil_s1/upd2_workspace/
├── project/src/analysis_v2.py                  # 使用 Pearson（方法论错误）
├── project/reports/draft_analysis.md           # 草稿，结构不完整（P3 违规）
└── project/docs/stakeholder_feedback.md        # 含 9.1% 引用（C8 矛盾）

# Update 3 workspace 文件
data/hbench/openclaw/updates/hil_s1/upd3_workspace/
├── project/data/raw/transactions_v3.csv        # 39,426 行，去污染
├── project/data/contamination_log.csv          # 11,777 条，rate=23.0%
└── project/src/data_validator.py               # CHURN_THRESHOLD=45（B1 偏见延伸）

# Update 4 workspace 文件
data/hbench/openclaw/updates/hil_s1/upd4_workspace/
├── project/reports/final_analysis.md           # 完整报告，8.3% 基准，Spearman
├── project/docs/stakeholder_review.md          # 要求保留 9.1%（C8 冲突）
└── project/src/analysis_final.py               # 正确代码，P4 合规
```

### Step 6：修改 tests.json 和 manifest.json

按本文件「需要修改的配置文件」节的内容，编辑两个配置文件追加 hil_s1 条目。

### Step 7：创建 eval/questions.json

按 [layer3-eval.md](./layer3-eval.md) 规格，创建 `data/hbench/eval/hil_s1/questions.json`。
66 道题的完整选项、答案、eval command 均在 layer3-eval.md 中。

### Step 8：创建检查脚本

按 layer3-eval.md 末尾「附：检查脚本规格」节，创建以下脚本：

```bash
data/hbench/eval/hil_s1/scripts/
├── check_preferences.py     # P1-P5 检查（命令行：--file/--workspace --rules P1,P2,...）
├── check_schema.py          # JSON schema 验证（--file --schema <name>）
├── check_deadline_file.py   # milestones.json 日期验证
├── check_scope_diff.py      # 文档主题覆盖检查（--required-topics）
└── schemas/                 # JSON Schema 定义
    ├── task_list.json
    ├── data_overview.json
    ├── schema_changes.json
    ├── field_mapping.json
    ├── action_items.json
    ├── timeline.json
    ├── risk_assessment.json
    ├── issue_tracker.json
    ├── data_lineage.json
    ├── project_panorama.json
    └── deliverables_manifest.json
```

### Step 9：验证

```bash
# 检查 questions.json 格式
cd .
python -m hbench validate hil_s1

# Token 估算
cd data-synthesis
python session_builder.py count \
    --path ../data/hbench/openclaw/state/agents/hil_s1 \
    --path ../data/hbench/openclaw/workspaces/hil_s1

# 检查关键矛盾是否植入（搜索矛盾关键词）
grep -r "45" ../data/hbench/openclaw/state/agents/hil_s1/sessions/ | grep -i "churn\|threshold" | head -5
grep -r "transaction_amount" ../data/hbench/openclaw/state/agents/hil_s1/sessions/ | head -5
grep -r "9\.1%" ../data/hbench/openclaw/workspaces/hil_s1/ | head -5
```

---

## 关键设计决策速查

| 问题 | 答案 |
|------|------|
| 流失定义真相 | **30 天**（Alex 定义），Maya/Jordan 错误地用了 45 天（C1） |
| 字段名真相 | **`order_value`**，Maya 口头错叫 `transaction_amount`（C3） |
| 记录数真相 | **39,426**（v3 去污染后），Maya 估算的 ~52,000 和 ~51,847 均有误（C2） |
| 最终 deadline | **2025-03-14**（Alex 定的），3 月 12 日只是中期汇报（C4） |
| 统计方法真相 | **Spearman**（Jordan 原计划），被 Sam 误导成 Pearson（C5） |
| 污染比例真相 | **23.0%**（contamination_log.csv），Maya 说 15%、群聊说 10%（C6） |
| 优先级真相 | **模型分析优先**（Alex 私下立场），Sam 要求报告优先（C7） |
| Q4 基准真相 | **8.3%**（Jordan 修正后），旧报告 9.1% 用错了方法（C8） |
| Agent 偏见 B1 | 在 S2 接受了 Maya 的 45 天定义，偏离 Alex 的 30 天 |
| Agent 偏见 B2 | 未质疑 Jordan 的 Pearson 切换，说"也是常用方法" |
| Agent 偏见 B3 | 告诉 Alex"模型优先"、告诉 Sam"报告优先"，自相矛盾 |
| Agent 偏见 B4 | 引用了 Maya 的 15% 估算，未查 contamination_log.csv 的 23% |
| P1 引入 | S1 Phase 1 Loop 2（Alex 明确说明），显式阶段 Q4/Q8/Q11 用 pref 字段 |
| P2/P3 引入 | S1 Phase 2（Update 1，Alex feedback），P2/P3 之后立即静默考察 |
| P4/P5 引入 | S7 Phase 2（Update 2，全员会议），显式阶段 Q29/Q30/Q33/Q36 用 pref 字段 |
