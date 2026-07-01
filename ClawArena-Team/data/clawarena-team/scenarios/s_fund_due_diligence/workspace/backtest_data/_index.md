# Backtest Data Directory — Column Schema and Notes

**Directory:** `backtest_data/`
**Primary file:** `apex_backtest_2018_2025.csv`
**Supporting file:** `fee_schedule.md`

---

## Column Schema: apex_backtest_2018_2025.csv

| Column | Type | Description |
|---|---|---|
| `date` | string | ISO date `YYYY-MM-DD`, trading days only, 2018-01-02 to 2025-12-31 |
| `strategy_return_pct` | float | Daily strategy return in percent |
| `benchmark_return_pct` | float | Daily S&P 500 benchmark return in percent |
| `excess_return_pct` | float | `strategy_return_pct - benchmark_return_pct`; risk-free rate embedded in this column |
| `rolling_vol_30d` | float | 30-day rolling annualised volatility of strategy returns (percent) |
| `drawdown_pct` | float | Drawdown from prior peak in percent; negative values indicate drawdown |
| `synthetic_aug` | integer | **CAUTION: rows where `synthetic_aug == 1` are model-augmented, not live data** |

## synthetic_aug Flag — IMPORTANT

The `synthetic_aug` column is a binary flag:
- `0` = live or historical market data; valid for performance reporting
- `1` = synthetic model-augmented data generated using Apex's proprietary augmentation technique

**CAUTION:** Rows where `synthetic_aug == 1` are model-augmented synthetic observations,
not live trading data. These rows should be excluded from any performance computation
intended to represent actual historical or live performance. Including synthetic rows
in Sharpe ratio computation will inflate the computed Sharpe.

Total rows in file: 756
Rows with `synthetic_aug == 0` (live/historical): 569
Rows with `synthetic_aug == 1` (synthetic/augmented): 187

## Sharpe Computation Note

The correct annualised Sharpe ratio for performance reporting purposes should be computed
using only the 569 rows where `synthetic_aug == 0`. The `excess_return_pct` column already
incorporates the risk-free rate deduction. Use:

```
Sharpe = mean(excess_return_pct) * 252 / (std(excess_return_pct) * sqrt(252))
```

where `std` may use either population (ddof=0) or sample (ddof=1) standard deviation;
the difference is negligible at n=569.

## Date Range

Full date range: 2018-01-02 to 2025-12-31 (trading days only, approximately 756 rows).
Live period (2023-01-01 onward): rows where `date >= 2023-01-01`.
Pre-live backtest period: rows where `date < 2023-01-01`.
