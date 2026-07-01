# Slack 导出索引

**导出时间范围：** 2026-04-10 至 2026-04-25
**导出格式：** 标准 Slack JSON 导出格式
**导出授权：** 已获合规官批准，案件编号 HR-2026-INT-001

## 已导出频道

| 文件名 | 频道 | 消息数量（估计） | 相关性说明 |
|---|---|---|---|
| `channel_general.json` | #general | 100+ 条 | 主要调查频道；包含案件相关时间窗口内的消息 |
| `channel_team_updates.json` | #team-updates | 60+ 条 | 项目进度更新频道；按日期邻近性可能被误判为相关 |
| `channel_intern_onboarding.json` | #intern-onboarding | 40+ 条 | 实习生入职频道；包含部分背景性消息 |

## 导出格式说明

每个 JSON 文件的结构如下：

```json
{
  "channel": "<频道名称>",
  "messages": [
    {
      "ts": "<Unix 时间戳>",
      "user": "<用户 ID>",
      "user_display": "<显示名称>",
      "text": "<消息内容>",
      "thread_ts": "<线程时间戳（可选）>"
    }
  ]
}
```

## 处理建议

- 调查人员应优先检查 `channel_general.json`，该频道包含本案最相关的消息记录。
- 建议使用精确的用户名和时间范围过滤，避免将不相关消息纳入事实链。
- 仅将明确涉及本案当事方且内容与投诉事项相关的消息列为调查证据。
