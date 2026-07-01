# VWAP Price Differential Methodology Note
## ArtemisQ Capital — SEC Response — 2024-11-06

## Overview

This note describes the Volume Weighted Average Price (VWAP) calculation
methodology to be applied in the revised order-level difference report,
per the legal counsel memorandum of 2024-11-06 which superseded the
closing-price basis initially specified in the SEC preliminary inquiry.

## Why VWAP Instead of Closing Price?

The original SEC preliminary inquiry letter (2024-11-05) specified
`price_diff_usd` using end-of-day closing price. Legal counsel has revised
this to VWAP basis (`price_diff_vwap_usd`) for the following reasons:

1. **Market-making context**: ArtemisQ Capital's AROS v4.2 is an automated
   market-making system. VWAP provides a more statistically appropriate
   baseline for evaluating execution quality in high-frequency market-making.

2. **Regulatory precedent**: VWAP-based trade analysis is standard in SEC
   and FCA enforcement proceedings involving automated trading systems.

3. **Reduced outlier sensitivity**: End-of-day closing prices on 2024-11-03
   may be affected by post-DST-transition volatility, making VWAP a more
   robust reference.

## VWAP Calculation Formula

For each affected order:
```
price_diff_vwap_usd = (execution_price - vwap_reference_price) * quantity
```

Where `vwap_reference_price` is the 5-minute VWAP for the instrument
at the time of order execution, as provided in the attached
`incident/vwap_reference_20241103.csv` file.

## Reference Data Schema

The VWAP reference data (`incident/vwap_reference_20241103.csv`) contains:

| Column | Type | Description |
|--------|------|-------------|
| `window_start_utc` | ISO 8601 UTC | Start of 1-minute bar in UTC |
| `instrument` | string | CME instrument code (ESZ4, NQZ4, etc.) |
| `vwap_usd` | float | Volume-weighted average price for the bar |
| `volume_lots` | int | Total volume in lots for the bar |
| `open_usd` | float | Bar open price |
| `high_usd` | float | Bar high price |
| `low_usd` | float | Bar low price |
| `close_usd` | float | Bar close price |
| `num_trades` | int | Number of trades in the bar |
| `tick_direction` | string | up/down/flat |
| `dst_correct_local` | ISO 8601 | Correct EST local time (UTC-5 after switch) |
| `exchange_session` | string | pre_open/regular/post_close |
| `circuit_breaker_active` | bool | CME circuit breaker status |

## VWAP Reference Values for Affected Period

The anomaly window (2024-11-03T14:00:00Z to 15:00:00Z) uses the
following VWAP reference prices (from 5-minute aggregation):

| Window (UTC) | ESZ4 VWAP | NQZ4 VWAP | RTYH5 VWAP |
|--------------|-----------|-----------|------------|
| 14:00 | 4562.50 | 19840.25 | 2197.80 |
| 14:05 | 4563.75 | 19842.00 | 2198.50 |
| 14:10 | 4561.00 | 19839.50 | 2197.20 |
| 14:15 | 4564.25 | 19843.75 | 2199.10 |
| 14:20 | 4565.00 | 19845.00 | 2200.00 |
| 14:25 | 4562.25 | 19841.25 | 2198.00 |
| 14:30 | 4563.50 | 19840.75 | 2197.90 |
| 14:35 | 4564.75 | 19842.50 | 2198.75 |
| 14:40 | 4565.25 | 19844.25 | 2199.50 |
| 14:45 | 4563.00 | 19841.00 | 2198.20 |
| 14:50 | 4562.75 | 19840.50 | 2197.80 |
| 14:55 | 4564.00 | 19843.00 | 2198.90 |

## Data Integrity Notes

- All VWAP timestamps in `vwap_reference_20241103.csv` are in UTC
- The `dst_correct_local` column shows the correct EST local time
  (UTC-5) for reference — contrast with the AROS system's incorrect
  UTC-4 local time during the incident
- Circuit breaker activity was NOT triggered during the affected period
  (2024-11-03T14:00-15:00 UTC)

---

*Issued: 2024-11-06 | Supersedes: closing price methodology from SEC inquiry 2024-11-05*
