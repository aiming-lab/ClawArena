# PR #447: 交易调度模块重构 -- git diff + review 记录 (merged 2026-03-10)

## PR 元数据

| 字段 | 值 |
|---|---|
| PR 编号 | #447 |
| 标题 | refactor: 交易调度模块 -- 统一时间处理和 order batching |
| 作者 | 赵磊 (zhaolei) |
| 审核人 | 小周 (xiaozhou) |
| 状态 | Merged |
| 合并时间 | 2026-03-10T16:45:00+08:00 |
| 文件变更 | 3 files changed, +187, -92 |
| CI 构建 | Build #891 -- PASSED |

## Diff 摘要

### strategy/scheduler.py (+98, -45)

```diff
@@ -120,12 +120,15 @@ class TradingScheduler:
     def schedule_trade(self, strategy_id: str, params: dict) -> dict:
         \"\"\"调度交易执行时间\"\"\"
         # 获取当前市场时间
-        market_time = self._get_market_time()
-        schedule_time = get_market_open_time()
+        # 统一使用 UTC + 固定偏移计算 CST
+        utc_now = datetime.utcnow()
+        schedule_time = datetime.utcnow() + timedelta(hours=8)

         # 检查是否在交易时段
         if not self._is_market_open(schedule_time):
-            raise MarketClosedError(f"当前非交易时段: {market_time}")
+            logger.warning(f"非交易时段: {schedule_time}")
+            return {"status": "queued", "scheduled_for": schedule_time}

         # Order batching 优化
         batch = self._create_batch(strategy_id, params)
@@ -145,8 +148,20 @@ class TradingScheduler:
+    def _create_batch(self, strategy_id: str, params: dict) -> OrderBatch:
+        \"\"\"批量订单处理 -- 减少 API 调用\"\"\"
+        orders = self._collect_pending_orders(strategy_id)
+        batch = OrderBatch(strategy_id=strategy_id)
+        for order in orders:
+            batch.add(order, priority=params.get('priority', 'normal'))
+        batch.validate()
+        return batch
+
+    def _optimize_position_sizing(self, batch: OrderBatch) -> OrderBatch:
+        \"\"\"仓位优化 -- 根据风控参数调整\"\"\"
+        risk_budget = self._get_risk_budget()
+        for order in batch.orders:
+            order.size = min(order.size, risk_budget.max_single_order)
+            order.size = max(order.size, risk_budget.min_order_size)
+        return batch
```

### strategy/position.py (+52, -28)

```diff
@@ -80,15 +80,30 @@ class PositionManager:
-    def calculate_position(self, signal: Signal) -> Position:
-        raw_size = signal.strength * self.base_size
-        return Position(size=raw_size, direction=signal.direction)
+    def calculate_position(self, signal: Signal) -> Position:
+        raw_size = signal.strength * self.base_size
+        adjusted = self._apply_risk_limits(raw_size)
+        slippage = self._estimate_slippage(adjusted)
+        return Position(
+            size=adjusted,
+            direction=signal.direction,
+            estimated_slippage=slippage,
+            timestamp=datetime.utcnow()
+        )
```

### tests/test_scheduler.py (+37, -19)

```diff
@@ -40,10 +40,25 @@ class TestTradingScheduler:
+    def test_batch_ordering(self):
+        scheduler = TradingScheduler()
+        result = scheduler._create_batch("V3", {"priority": "high"})
+        assert result.is_valid()
+        assert len(result.orders) > 0
+
+    def test_position_sizing_limits(self):
+        pm = PositionManager(base_size=1000)
+        signal = Signal(strength=0.8, direction="long")
+        pos = pm.calculate_position(signal)
+        assert pos.size <= pm.risk_budget.max_single_order
```

## Review 记录

### 小周 (xiaozhou) -- 2026-03-10T15:30:00+08:00

> LGTM, 逻辑清晰，交易调度模块改动合理。
>
> order batching 的实现很干净，position sizing 的风控参数检查也到位了。
>
> Approved.

**注：review 中无针对第 127 行 `datetime.utcnow() + timedelta(hours=8)` 的具体评论。**

## 关联信息

- 本 PR 触发 CI Build #891（详见 ci-build-report.md）
- PR 合并后 V3 策略于 2026-03-10 部署到生产环境
- 2026-03-16 生产日志记录时区转换错误（详见 production-error-log.md）
