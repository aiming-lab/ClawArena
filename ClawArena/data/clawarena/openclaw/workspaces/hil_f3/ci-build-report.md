# CI Build Report -- PR #447 (Build #891) -- Jenkins 2026-03-10

## 构建概要

| 字段 | 值 |
|---|---|
| Build 编号 | #891 |
| 触发 PR | #447 (交易调度模块重构) |
| 构建时间 | 2026-03-10T17:00:12+08:00 |
| 构建状态 | **PASSED** ✅ |
| 总测试数 | 34 |
| 通过 | 34 |
| 失败 | 0 |
| 跳过 | 0 |
| 行覆盖率 | 78% |
| 分支覆盖率 | 65% |

## 测试套件详情

### strategy/test_scheduler.py (12 tests)

| 测试名称 | 状态 | 耗时 |
|---|---|---|
| test_schedule_basic | PASSED | 0.12s |
| test_schedule_with_params | PASSED | 0.08s |
| test_batch_ordering | PASSED | 0.15s |
| test_batch_validation | PASSED | 0.11s |
| test_position_sizing_limits | PASSED | 0.09s |
| test_risk_budget_check | PASSED | 0.13s |
| test_order_priority | PASSED | 0.07s |
| test_market_hours_check | PASSED | 0.10s |
| test_pending_orders_collection | PASSED | 0.14s |
| test_slippage_estimation | PASSED | 0.11s |
| test_utc_to_cst_basic | PASSED | 0.06s |
| test_cst_to_utc_basic | PASSED | 0.05s |

### strategy/test_timezone.py (3 tests -- 时区转换专项)

| 测试名称 | 状态 | 耗时 |
|---|---|---|
| test_utc_to_cst_basic | PASSED | 0.04s |
| test_cst_to_utc_basic | PASSED | 0.03s |
| test_market_hours_check | PASSED | 0.05s |

**测试配置:**
```python
# test_timezone.py, line 45
@mock.patch('strategy.scheduler.datetime', wraps=datetime(2026, 1, 15, 10, 0, 0))
def test_utc_to_cst_basic(self, mock_dt):
    """验证 UTC -> CST 基本转换"""
    scheduler = TradingScheduler()
    result = scheduler._convert_to_cst(datetime(2026, 1, 15, 2, 30, 0))
    assert result.hour == 10  # UTC 02:30 + 8 = CST 10:30
    assert result.minute == 30
```

### strategy/test_position.py (8 tests)

| 测试名称 | 状态 | 耗时 |
|---|---|---|
| test_calculate_basic | PASSED | 0.08s |
| test_risk_limits | PASSED | 0.09s |
| test_slippage_calc | PASSED | 0.07s |
| test_direction_long | PASSED | 0.04s |
| test_direction_short | PASSED | 0.04s |
| test_zero_signal | PASSED | 0.03s |
| test_max_position | PASSED | 0.06s |
| test_min_position | PASSED | 0.05s |

### integration/test_pipeline.py (11 tests)

| 测试名称 | 状态 | 耗时 |
|---|---|---|
| test_full_pipeline | PASSED | 1.2s |
| test_error_recovery | PASSED | 0.8s |
| test_concurrent_orders | PASSED | 0.9s |
| test_api_rate_limit | PASSED | 0.4s |
| test_data_feed_reconnect | PASSED | 0.6s |
| test_heartbeat | PASSED | 0.2s |
| test_order_fill_callback | PASSED | 0.5s |
| test_position_sync | PASSED | 0.7s |
| test_risk_check_pipeline | PASSED | 0.3s |
| test_logging_pipeline | PASSED | 0.2s |
| test_shutdown_graceful | PASSED | 0.4s |

## 覆盖率报告

| 模块 | 行覆盖率 | 分支覆盖率 |
|---|---|---|
| strategy/scheduler.py | 82% | 68% |
| strategy/position.py | 85% | 72% |
| strategy/timezone.py | 71% | 55% |
| integration/ | 76% | 62% |
| **总计** | **78%** | **65%** |

## 构建日志摘要

```
[17:00:00] Checking out PR #447 from branch feature/trade-scheduler-refactor
[17:00:02] Installing dependencies...
[17:00:08] Running test suite...
[17:00:12] 34 tests passed, 0 failed, 0 skipped
[17:00:12] Coverage: 78% line, 65% branch
[17:00:12] Build #891 PASSED
```
