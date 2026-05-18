# 小周分享 -- 标准时区处理方案 (2026-03-23)

## 来源
小周在 #策略群 分享的代码方案和经验总结。

## 正确写法

```python
from zoneinfo import ZoneInfo
from datetime import datetime

# 正确: timezone-aware datetime
schedule_time = datetime.now(tz=ZoneInfo('Asia/Shanghai'))

# 也可以用 pytz (兼容旧版本)
import pytz
shanghai_tz = pytz.timezone('Asia/Shanghai')
schedule_time = datetime.now(tz=shanghai_tz)
```

## 反模式对比

```python
# ❌ 反模式: 硬编码 UTC+8
schedule_time = datetime.utcnow() + timedelta(hours=8)

# 为什么不行:
# 1. CST (China Standard Time) 本身没有 DST
# 2. 但如果服务器或依赖库受 US DST 影响，utcnow() 可能返回
#    非预期的 UTC 时间
# 3. timedelta(hours=8) 是静态偏移，不考虑任何时区规则
# 4. 这种写法在 90% 的时间能工作，但在 DST 切换期间会出错
```

## 小周的机构案例

> "我们公司的回测引擎上个月也出过 DST 问题，原因一样——`utcnow() + timedelta(hours=n)` 这种写法。
> 回测时因为用的是历史数据所以没问题，但实盘的时候一到 DST 切换期间就偏了。
> 最后统一改成 `zoneinfo` 处理，所有时间相关的代码都用 timezone-aware datetime。"

## 建议测试用例

```python
import pytest
from zoneinfo import ZoneInfo
from datetime import datetime

# 测试 DST 切换前后
@pytest.mark.parametrize("utc_time,expected_cst", [
    # Non-DST period
    (datetime(2026, 1, 15, 2, 30, tzinfo=ZoneInfo('UTC')), "10:30"),
    # US DST active (Mar 8+)
    (datetime(2026, 3, 10, 3, 30, tzinfo=ZoneInfo('UTC')), "11:30"),
    # US DST end (Nov)
    (datetime(2026, 11, 2, 2, 30, tzinfo=ZoneInfo('UTC')), "10:30"),
])
def test_timezone_conversion(utc_time, expected_cst):
    cst = utc_time.astimezone(ZoneInfo('Asia/Shanghai'))
    assert cst.strftime("%H:%M") == expected_cst
```
