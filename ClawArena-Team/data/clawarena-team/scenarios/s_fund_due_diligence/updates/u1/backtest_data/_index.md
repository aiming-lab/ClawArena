# Backtest Data Directory — Column Schema and Notes (Updated: u1)

**Directory:** `backtest_data/`
**Primary file:** `apex_backtest_2018_2025.csv` *(UPDATED — adds the `fee_adj_return_pct` fee-deduction column; supersedes the prior version)*
**Supporting file:** `fee_schedule.md`

---

## Column Schema: apex_backtest_2018_2025.csv (u1 Update)

| Column | Type | Description |
|---|---|---|
| `date` | string | ISO date `YYYY-MM-DD`, trading days only; covers the pre-live backtest window |
| `strategy_return_pct` | float | Daily strategy return in percent |
| `benchmark_return_pct` | float | Daily S&P 500 benchmark return in percent |
| `excess_return_pct` | float | `strategy_return_pct - benchmark_return_pct`; risk-free rate embedded |
| `rolling_vol_30d` | float | 30-day rolling annualised volatility (percent) |
| `drawdown_pct` | float | Drawdown from prior peak in percent; negative values |
| `synthetic_aug` | integer | **CAUTION:** rows where `synthetic_aug == 1` are model-augmented, not live data |
| `fee_adj_return_pct` | float | **NEW (u1):** Fee-adjustment column documenting how the fund's fee load is deducted from gross returns; populated only where live fee-adjusted returns are available |

## NEW COLUMN: fee_adj_return_pct

The `fee_adj_return_pct` column was added in the u1 update. It documents the
fee-adjustment methodology applied to gross returns: each fee-adjusted daily return is
derived by deducting the daily management fee accrual (1.5% p.a. / 252) and the
applicable performance allocation from the gross `strategy_return_pct`. This makes the
fee drag underlying the gross-to-net gap explicit on a per-day basis.

**Important — this CSV covers the pre-live backtest window only.** It does **not**
contain the 2023+ live period rows; those live results are reported in
`live_reports/`, not in this backtest file. Accordingly, the fee-adjusted column is
empty for the backtest rows present here. Do **not** attempt to recompute the live
post-cost Sharpe from this CSV — the authoritative live net-of-fees Sharpe is the one
extracted from the 2024 live performance reports (q3). Use the fee schedule and this
column's documented deduction methodology only as **supporting evidence** when
attributing the gross-to-net (fee-drag) component of the Sharpe reconciliation.

## synthetic_aug Flag — IMPORTANT

(Unchanged from prior version)

Rows where `synthetic_aug == 1` are model-augmented synthetic observations.
Always exclude these rows from performance computations.

Total rows: 756 | `synthetic_aug == 0`: 569 | `synthetic_aug == 1`: 187

## Sharpe Computation (Updated Guidance)

For pre-cost Sharpe (consistent with q2): use `excess_return_pct` with `synthetic_aug == 0`
on this backtest CSV.
For post-cost (net-of-fees) live Sharpe: do **not** derive it from this CSV. Use the
authoritative annualised net Sharpe extracted from the 2024 live performance reports
(`live_reports/`), i.e. the q3 figure of ~1.62. This update's `fee_adj_return_pct`
column and the fee schedule document the per-day fee deduction methodology that explains
the fee-drag portion of the gross-to-net gap; they are supporting evidence for the
reconciliation, not an independent live-Sharpe source.
