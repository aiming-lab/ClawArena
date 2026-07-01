# Layer 4 — Dynamic Update 规格

> 4 次 update 的完整规格：触发时机、source 文件清单、manifest `files` 配置。
> session 更新均为 `action: "append"`；workspace 更新均为 `action: "new"`。

---

## Update 1（触发：Round 0 结束后）

**触发时机**：题目 Q1-Q12 全部完成后，系统执行 Update 1。

**信息格局目标**：
- 引入 P2/P3 偏好（Alex feedback）
- 引入 v2 数据及 schema changelog（数据演进）
- Maya/changelog 之间的 C3 矛盾延伸

### Source 文件清单

| Source 文件 | 类型 | 内容摘要 |
|------------|------|---------|
| `update1/s1_alex_dm_p2.jsonl` | append_session | Alex feedback → P2/P3 引入 + 优先级确认 |
| `update1/s2_maya_dm_p2.jsonl` | append_session | Maya：v2 数据上传，记录数再次给出不同估算 |
| `update1/s5_eng_group_p2.jsonl` | append_session | S5 群聊技术讨论，Maya 再次说错字段名 |
| `update1/transactions_v2.csv` | add_file | 新版数据，含 channel 列（workspace: data/raw/） |
| `update1/schema_changelog.md` | add_file | schema 变更记录（workspace: project/docs/） |

### Manifest files 配置

`upd1_sessions`（dir: `updates/hil_s1/upd1_sessions`）：
```json
[
  {"name": "alex_slack_5ba4976f-e34a-4fee-ad19-c39c49aecc59.jsonl", "action": "append"},
  {"name": "maya_discord_26597928-810c-4a52-ab0e-147b488c166c.jsonl", "action": "append"},
  {"name": "data_engineering_slack_d84ae024-69c3-4679-bc3b-d1dffafab625.jsonl", "action": "append"}
]
```

`upd1_workspace`（dir: `updates/hil_s1/upd1_workspace`）：
```json
[
  {"name": "project/data/raw/transactions_v2.csv", "action": "new"},
  {"name": "project/docs/schema_changelog.md", "action": "new"}
]
```

---

## Update 2（触发：Round 1 / Q13-Q25 全部完成后）

**触发时机**：题目 Q13-Q25 全部完成后，系统执行 Update 2。

**信息格局目标**：
- 引入 P4/P5 偏好（S7 周会，Alex 明确说明）
- Jordan 提交有方法论错误的分析草稿
- 需求优先级冲突升级（Sam 压力增加）

### Source 文件清单

| Source 文件 | 类型 | 内容摘要 |
|------------|------|---------|
| `update2/s3_jordan_dm_p2.jsonl` | append_session | Jordan 提交 analysis_v2.py，讨论草稿报告 |
| `update2/s4_sam_dm_p2.jsonl` | append_session | Sam 升级报告优先级诉求 |
| `update2/s6_report_group_p2.jsonl` | append_session | Jordan+Sam 群聊报告内容讨论，C8 矛盾种入 |
| `update2/s7_allhands_p2.jsonl` | append_session | 周会：P4/P5 引入，方法论确认 |
| `update2/analysis_v2.py` | add_file | Jordan 的分析代码（Pearson，有错，workspace: project/src/） |
| `update2/draft_analysis.md` | add_file | 分析草稿报告（workspace: project/reports/） |
| `update2/stakeholder_feedback.md` | add_file | stakeholder 意见（workspace: project/docs/） |

### Manifest files 配置

`upd2_sessions`（dir: `updates/hil_s1/upd2_sessions`）：
```json
[
  {"name": "jordan_feishu_0c923eb4-2888-4e40-afb0-af6f5f3e8117.jsonl", "action": "append"},
  {"name": "sam_telegram_5609fa34-0f8b-4530-a9e3-12a6cdb81037.jsonl", "action": "append"},
  {"name": "analysis_report_discord_15916984-6100-4314-96d8-5819af6c77fe.jsonl", "action": "append"},
  {"name": "all_hands_feishu_e0f00482-67c2-4108-beac-276d95c0ff22.jsonl", "action": "append"}
]
```

`upd2_workspace`（dir: `updates/hil_s1/upd2_workspace`）：
```json
[
  {"name": "project/src/analysis_v2.py", "action": "new"},
  {"name": "project/reports/draft_analysis.md", "action": "new"},
  {"name": "project/docs/stakeholder_feedback.md", "action": "new"}
]
```

---

## Update 3（触发：Round 2 / Q26-Q39 全部完成后）

**触发时机**：题目 Q26-Q39 全部完成后，系统执行 Update 3。

**信息格局目标**：
- 引入数据污染危机（C6 矛盾核心）
- contamination_log.csv 提供真实 23% 数据（vs Maya 的 15% 估算）
- 提供去污染后的 v3 数据
- data_validator.py 含 45 天 bug（C1 延伸）

### Source 文件清单

| Source 文件 | 类型 | 内容摘要 |
|------------|------|---------|
| `update3/s1_alex_dm_p3.jsonl` | append_session | Alex 告知污染问题，要求切换 v3 |
| `update3/s2_maya_dm_p3.jsonl` | append_session | Maya 报告污染（说 15%），提供 v3 和 log |
| `update3/s5_eng_group_p3.jsonl` | append_session | 群聊紧急讨论，信息混乱，有人说 10% |
| `update3/transactions_v3.csv` | add_file | 干净数据（workspace: project/data/raw/） |
| `update3/contamination_log.csv` | add_file | 污染记录，含 23% 数据（workspace: project/data/） |
| `update3/data_validator.py` | add_file | Maya 写的验证脚本，含 45 天 bug（workspace: project/src/） |

### Manifest files 配置

`upd3_sessions`（dir: `updates/hil_s1/upd3_sessions`）：
```json
[
  {"name": "alex_slack_5ba4976f-e34a-4fee-ad19-c39c49aecc59.jsonl", "action": "append"},
  {"name": "maya_discord_26597928-810c-4a52-ab0e-147b488c166c.jsonl", "action": "append"},
  {"name": "data_engineering_slack_d84ae024-69c3-4679-bc3b-d1dffafab625.jsonl", "action": "append"}
]
```

`upd3_workspace`（dir: `updates/hil_s1/upd3_workspace`）：
```json
[
  {"name": "project/data/raw/transactions_v3.csv", "action": "new"},
  {"name": "project/data/contamination_log.csv", "action": "new"},
  {"name": "project/src/data_validator.py", "action": "new"}
]
```

---

## Update 4（触发：Round 3 / Q40-Q52 全部完成后）

**触发时机**：题目 Q40-Q52 全部完成后，系统执行 Update 4。

**信息格局目标**：
- Jordan 提交最终分析（修正方法和 threshold，C1/C5/C8 最终解决）
- stakeholder review 引入新矛盾（坚持 9.1% 基准，C8 延伸）
- 项目回顾强化 C1/C5 教训
- 引入最终交付代码和报告

### Source 文件清单

| Source 文件 | 类型 | 内容摘要 |
|------------|------|---------|
| `update4/s3_jordan_dm_p3.jsonl` | append_session | Jordan 最终分析提交，解释方法修正 |
| `update4/s4_sam_dm_p3.jsonl` | append_session | Sam 转达 stakeholder 评审（C8 矛盾） |
| `update4/s6_report_group_p3.jsonl` | append_session | 最终报告评审群聊，基准数字争议 |
| `update4/s7_allhands_p3.jsonl` | append_session | 项目回顾会，总结决策链教训 |
| `update4/final_analysis.md` | add_file | 最终分析报告（workspace: project/reports/） |
| `update4/stakeholder_review.md` | add_file | 最终评审意见（workspace: project/docs/） |
| `update4/analysis_final.py` | add_file | 最终分析代码（workspace: project/src/） |

### Manifest files 配置

`upd4_sessions`（dir: `updates/hil_s1/upd4_sessions`）：
```json
[
  {"name": "jordan_feishu_0c923eb4-2888-4e40-afb0-af6f5f3e8117.jsonl", "action": "append"},
  {"name": "sam_telegram_5609fa34-0f8b-4530-a9e3-12a6cdb81037.jsonl", "action": "append"},
  {"name": "analysis_report_discord_15916984-6100-4314-96d8-5819af6c77fe.jsonl", "action": "append"},
  {"name": "all_hands_feishu_e0f00482-67c2-4108-beac-276d95c0ff22.jsonl", "action": "append"}
]
```

`upd4_workspace`（dir: `updates/hil_s1/upd4_workspace`）：
```json
[
  {"name": "project/reports/final_analysis.md", "action": "new"},
  {"name": "project/docs/stakeholder_review.md", "action": "new"},
  {"name": "project/src/analysis_final.py", "action": "new"}
]
```

---

## Update Source 文件生成规范

所有 `.jsonl` source 文件使用 `session_builder.py append` 命令生成，输出文件名须与 manifest `files[].name` 一致（即完整 session ID 文件名）：

```bash
cd ./data-synthesis

python session_builder.py append \
  --loops hil_s1/loops/s1_alex_dm_p2.json \
  --base-session ../data/hbench/openclaw/state/agents/hil_s1/sessions/alex_slack_5ba4976f-e34a-4fee-ad19-c39c49aecc59.jsonl \
  --workspace-dir ../data/hbench/openclaw/workspaces/hil_s1 \
  --output ../data/hbench/openclaw/updates/hil_s1/upd1_sessions/alex_slack_5ba4976f-e34a-4fee-ad19-c39c49aecc59.jsonl
```

输出文件只含新消息（无 session header），第一条新消息的 `parentId` = base-session 最后一行的 `id`。实际执行由 `assemble.sh` 统一完成，无需手动运行上述命令。

---

## 题目与 update 关系

| 题目范围 | 可用 update | 可见 session 内容 | 可见 workspace 文件 |
|---------|-----------|-----------------|-------------------|
| Q1-Q12 | 无（初始状态） | S1-S7 Phase 1 | 初始文件集 |
| Q13-Q25 | Update 1 | + S1/S2/S5 Phase 2 | + v2.csv, changelog |
| Q26-Q39 | Update 2 | + S3/S4/S6/S7 Phase 2 | + analysis_v2.py, draft, stakeholder_fb |
| Q40-Q52 | Update 3 | + S1/S2/S5 Phase 3 | + v3.csv, contamination_log, data_validator |
| Q53-Q66 | Update 4 | + S3/S4/S6/S7 Phase 3 | + final_analysis, stakeholder_review, analysis_final |
