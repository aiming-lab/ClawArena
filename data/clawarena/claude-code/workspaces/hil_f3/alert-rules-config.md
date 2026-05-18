# 告警规则配置导出 -- 赵磊交易系统 (2025-10 至 2026-03)

## 导出时间: 2026-03-17T09:00:00+08:00
## 格式: YAML-style configuration

```yaml
alert_rules:
  - rule_id: rule_001
    name: CPU 使用率告警
    pattern: "CPU_USAGE > 90%"
    threshold: 90
    created_by: zhaolei
    created_at: 2025-10-01T10:00:00+08:00
    status: active
    channel: email

  - rule_id: rule_002
    name: 内存使用告警
    pattern: "MEM_USAGE > 85%"
    threshold: 85
    created_by: zhaolei
    created_at: 2025-10-01T10:05:00+08:00
    status: active
    channel: email

  - rule_id: rule_003
    name: 磁盘空间告警
    pattern: "DISK_USAGE > 80%"
    threshold: 80
    created_by: zhaolei
    created_at: 2025-10-15T14:00:00+08:00
    status: active
    channel: email

  - rule_id: rule_004
    name: 网络延迟告警
    pattern: "NET_LATENCY > 100ms"
    threshold: 100
    created_by: zhaolei
    created_at: 2025-10-15T14:10:00+08:00
    status: active
    channel: wechat

  - rule_id: rule_005
    name: API 限速告警
    pattern: "API_RATE_LIMIT_*"
    created_by: zhaolei
    created_at: 2025-11-01T09:00:00+08:00
    status: active
    channel: wechat

  - rule_id: rule_006
    name: 数据源连接告警
    pattern: "DATA_FEED_DISCONNECT"
    created_by: zhaolei
    created_at: 2025-11-01T09:05:00+08:00
    status: active
    channel: wechat

  - rule_id: rule_007
    name: 时区转换告警静默
    pattern: "TZ_CONVERT.*"
    action: silence
    created_by: zhaolei
    created_at: 2025-12-15T14:22:00+08:00
    reason: "V1迁移期间时区兼容性警告，无功能影响"
    expires: null  # 无过期时间
    status: active
    note: "V1 策略从旧时区库迁移到新库时产生的兼容性警告，确认不影响交易功能"

  - rule_id: rule_008
    name: 心跳超时告警
    pattern: "HEARTBEAT_TIMEOUT"
    created_by: zhaolei
    created_at: 2025-12-20T10:00:00+08:00
    status: active
    channel: wechat

  - rule_id: rule_009
    name: 订单超时告警
    pattern: "ORDER_TIMEOUT > 5s"
    created_by: zhaolei
    created_at: 2026-01-05T09:00:00+08:00
    status: active
    channel: email

  - rule_id: rule_010
    name: 风控参数变更通知
    pattern: "RISK_PARAM_CHANGE"
    created_by: zhaolei
    created_at: 2026-01-10T14:00:00+08:00
    status: active
    channel: email

  - rule_id: rule_011
    name: 策略版本部署通知
    pattern: "DEPLOY_*"
    created_by: zhaolei
    created_at: 2026-01-15T09:00:00+08:00
    status: active
    channel: wechat

  - rule_id: rule_012
    name: 保证金不足预警
    pattern: "MARGIN_CALL_*"
    created_by: zhaolei
    created_at: 2026-02-01T10:00:00+08:00
    status: active
    channel: email+wechat
    priority: critical

  - rule_id: rule_013
    name: 异常交易量告警
    pattern: "VOLUME_ANOMALY"
    created_by: zhaolei
    created_at: 2026-02-15T14:00:00+08:00
    status: active
    channel: wechat

  - rule_id: rule_014
    name: 服务器维护窗口通知
    pattern: "MAINTENANCE_WINDOW"
    created_by: zhaolei
    created_at: 2026-03-01T09:00:00+08:00
    status: active
    channel: email

  - rule_id: rule_015
    name: 交易时段合规检查
    pattern: "TRADING_HOURS_VIOLATION"
    created_by: zhaolei
    created_at: 2026-03-01T09:05:00+08:00
    status: active
    channel: email+wechat
    priority: critical
```

## 统计

| 统计项 | 值 |
|---|---|
| 总规则数 | 15 |
| 活跃规则 | 15 |
| 静默规则 | 1 (rule_007, TZ_CONVERT.*) |
| 关键优先级 | 2 (rule_012, rule_015) |
| 最早创建 | 2025-10-01 |
| 最近创建 | 2026-03-01 |
