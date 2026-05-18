# V3 策略生产日志 -- 2026-03-09 至 2026-03-16 -- 导出自交易服务器

## 日志筛选条件: strategy=V3, level>=WARN, date_range=2026-03-09/2026-03-16

```log
2026-03-09T03:30:02Z [INFO] V3 strategy heartbeat OK. order_check=idle.
2026-03-09T03:30:02Z [WARN] [SILENCED by rule_007] TZ_CONVERT_WARN: expected offset +0800, computed offset +0800, note: DST active on source. server_tz=Asia/Shanghai.
2026-03-09T04:00:00Z [INFO] Data feed connected: vendor=wind, latency=12ms.
2026-03-09T06:30:00Z [INFO] V3-20260309-001 order submitted. expected_cst=10:30:00. actual_cst=10:30:02. status=FILLED. price=3245.50.
2026-03-09T07:00:15Z [INFO] Heartbeat OK.
2026-03-09T08:15:00Z [INFO] Position sync complete. net_pnl=+1,250.00.

2026-03-10T03:29:45Z [WARN] [SILENCED by rule_007] TZ_CONVERT_WARN: timezone offset mismatch detected. expected_local=10:29, actual_local=11:29, delta=+60min.
2026-03-10T03:29:47Z [INFO] V3-20260310-001 order submitted. expected_cst=10:30:00. actual_cst=11:29:47. status=FILLED. price=3251.20. NOTE: execution time shifted +59min47s from expected.
2026-03-10T04:00:00Z [INFO] Data feed reconnect. vendor=wind.
2026-03-10T06:00:00Z [INFO] Heartbeat OK.
2026-03-10T08:30:00Z [INFO] Position sync complete. net_pnl=+890.00.

2026-03-11T03:29:50Z [WARN] [SILENCED by rule_007] TZ_CONVERT_WARN: timezone offset mismatch detected. expected_local=10:30, actual_local=11:30, delta=+60min.
2026-03-11T03:29:53Z [INFO] V3-20260311-001 order submitted. expected_cst=10:30:00. actual_cst=11:29:53. status=FILLED. price=3248.80. NOTE: execution time shifted +59min53s from expected.
2026-03-11T04:15:00Z [INFO] Network latency spike: wind API 85ms (threshold 100ms). No action.
2026-03-11T07:00:00Z [INFO] Heartbeat OK.
2026-03-11T08:45:00Z [INFO] Position sync complete. net_pnl=+420.00.

2026-03-12T03:30:00Z [INFO] V3 strategy heartbeat OK. No trade signal generated today.
2026-03-12T04:00:00Z [INFO] Data feed connected. vendor=wind. latency=15ms.
2026-03-12T07:00:00Z [INFO] Heartbeat OK.

2026-03-13T03:28:10Z [WARN] [SILENCED by rule_007] TZ_CONVERT_WARN: timezone offset mismatch. delta=+60min.
2026-03-13T03:28:12Z [INFO] V3-20260313-001 order submitted. expected_cst=10:28:00. actual_cst=11:28:12. status=FILLED. price=3256.10. NOTE: execution time shifted +60min12s from expected.
2026-03-13T04:00:00Z [INFO] Data feed connected. vendor=wind.
2026-03-13T06:30:00Z [INFO] Heartbeat OK.
2026-03-13T08:00:00Z [INFO] Position sync complete. net_pnl=+1,680.00.

2026-03-14T03:30:00Z [INFO] Weekend. Market closed. V3 idle.
2026-03-15T03:30:00Z [INFO] Weekend. Market closed. V3 idle.

2026-03-16T03:30:05Z [ERROR] TZ_CONVERT_ERROR: expected CST 10:30, actual CST 11:30, delta=+60min. DST offset not accounted for in schedule_trade() line 127.
2026-03-16T03:30:05Z [ERROR] TRADE_REJECTED: order_id=V3-20260316-001, reason=MARKET_CLOSED, exchange_response="沪市午间休市 11:30-13:00".
2026-03-16T03:30:05Z [WARN] [SILENCED by rule_007] TZ_CONVERT_WARN: timezone offset mismatch detected. This alert was suppressed by silence_rule_007.
2026-03-16T03:30:06Z [ERROR] Compliance alert triggered: trading_hours_violation. order_id=V3-20260316-001. execution_time=2026-03-16T11:30:05+08:00. market_status=CLOSED(midday_break).
2026-03-16T04:00:00Z [INFO] Data feed connected. vendor=wind.
2026-03-16T07:00:00Z [INFO] Heartbeat OK.
2026-03-16T08:00:00Z [WARN] Compliance system notification sent to account holder: zhaolei.
```

## 日志统计

| 指标 | 值 |
|---|---|
| 总日志条目 | 52 |
| ERROR 级别 | 3 (均为 2026-03-16) |
| WARN 级别 (含 SILENCED) | 7 |
| SILENCED by rule_007 | 5 |
| 正常 INFO 条目 | 42 |
| 交易执行 | 5 笔 (Mar 9, 10, 11, 13, 16) |
| 时间偏移 > 30min | 4 笔 (Mar 10, 11, 13, 16) |
| 被拒绝交易 | 1 笔 (Mar 16, MARKET_CLOSED) |
