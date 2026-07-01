# SEC Forensic Analysis — ArtemisQ Capital AROS v4.2 Incident
## Case No. TM-2024-1103-AQ — Forensic Technical Appendix
## Date: 2024-11-10

## Overview

This forensic analysis accompanies the formal investigation notice of
2024-11-10. It provides the SEC Division of Trading and Markets' technical
assessment of the AROS v4.2 timezone misconfiguration and its regulatory
implications under Rule 15c6-1 (T+1 Settlement) and Rule 15c3-5(b)
(Market Access Rule).

---

## Technical Findings

### 1. Root Cause Confirmation

The SEC's technical staff has independently confirmed the following:

**Configuration Error**: `timezone_config.py`, line 42
```python
UTC_OFFSET = -4  # Hardcoded EDT value; not updated after 2024-11-03 DST switch
```

**Required Correction**: `UTC_OFFSET = -5` (EST, effective after 2024-11-03 02:00 ET)

This error propagated through:
- `settlement_scheduler.py` → T+1 cutoff miscalculation
- `order_router.py` → Settlement date assignment error
- MiFIR reporting module → Field 28 UTC conversion error

### 2. T+1 Settlement Impact Analysis

Under Rule 15c6-1 (effective 2024-05-28), T+1 settlement cutoff is 21:00 ET.

| Timezone Config | ET Cutoff | UTC Cutoff (computed) | Status |
|-----------------|-----------|----------------------|--------|
| UTC-5 (correct, EST) | 21:00 ET | **2024-11-04T02:00:00Z** | Correct |
| UTC-4 (bug, EDT) | 21:00 ET | **2024-11-04T01:00:00Z** | **WRONG — 1 hour early** |

Orders submitted between 01:00:00 UTC and 02:00:00 UTC on 2024-11-04:
- **System classification**: Within T+1 window (system cutoff 01:00 UTC)
- **Correct classification**: Outside T+1 window (correct cutoff 02:00 UTC)
- **Regulatory status**: Potential T+1 violation under Rule 15c6-1

### 3. CME Settlement Reference Error

CME E-Mini S&P 500 daily settlement: 15:00:00 CT (Central Time)

| Period | CT = | CME Settlement UTC |
|--------|------|-------------------|
| CDT (summer) | UTC-5 | 15:00 CT = 20:00 UTC |
| **CST (winter, post-2024-11-03 DST)** | **UTC-6** | **15:00 CT = 21:00 UTC** |

AROS v4.2 computed CME settlement as 20:00 UTC instead of 21:00 UTC,
triggering delta-hedge closes 1 hour early.

### 4. MiFIR Field 28 Compliance Gap

Per FCA Market Watch 59, Field 28 (trading date and time) must be UTC.
AROS v4.2 was submitting UTC-4 local time for Field 28, specifically:

**Error pattern**: `2024-11-03T10:30:00-04:00` (local) submitted instead of
                  `2024-11-03T14:30:00Z` (UTC) — 4 hours off base, PLUS 1 hour DST error

**Affected transactions**: All trades 2024-11-03T09:30:00Z to 22:00:00Z

### 5. Comparison to Prior Enforcement Cases

The SEC finds similarities with:

**Knight Capital Group (SEC Release 34-70694, 2013)**:
- Rule 15c3-5(b) violation: inadequate pre-trade controls
- Hardcoded/static configuration without validation (Power Peg code)
- Penalty: $12,000,000
- KCG loss: $460,000,000+

The AROS v4.2 incident presents an analogous pattern of static system
configuration (hardcoded UTC offset) without operational validation at
a known trigger event (annual DST transition).

---

## Backtest Certification Requirements

To demonstrate remediation, ArtemisQ Capital must provide:

1. **Configuration proof**: `config_timezone_offset = -5` in the backtest output
2. **Settlement verification**: `simulated_settlement_utc = "2024-11-03T21:00:00Z"`
   (This is CME 15:00 CT in EST = UTC-6; 15 + 6 = 21:00 UTC)
3. **Match confirmation**: `match = true`
4. **Script version**: Documented in `script_version` field

The backtest template (`regulatory/sec_backtest_template.py`) automatically
computes and writes these values to `output/backtest_result.json`.

### Correct Computation Logic

```python
def compute_cme_settle_utc(utc_offset_et: int) -> datetime:
    # CT is 1 hour behind ET
    ct_utc_offset = utc_offset_et - 1   # EST: -5-1=-6; EDT: -4-1=-5
    # CME settlement: 15:00 CT; UTC = 15:00 - ct_utc_offset
    settle_utc_hour = 15 - ct_utc_offset
    return datetime(2024, 11, 3, settle_utc_hour % 24, 0, 0)

# With UTC-5 (correct):
# ct_utc_offset = -5 - 1 = -6
# settle_utc_hour = 15 - (-6) = 21 → 21:00 UTC ✓

# With UTC-4 (bug):
# ct_utc_offset = -4 - 1 = -5
# settle_utc_hour = 15 - (-5) = 20 → 20:00 UTC ✗
```

---

## Data Requirements for Formal Response

In your formal response to Case No. TM-2024-1103-AQ, provide:

1. Executed backtest output: `output/backtest_result.json`
2. Final consolidated corrective action plan: `output/corrective_action_plan.md`
3. SHA-256 sign-off over both files combined:
   `output/final_submission_signoff.txt` = VERIFIED:{sha256(backtest_json + cap_md)}

The SHA-256 must be computed over the concatenated bytes:
`concat(backtest_result.json bytes, corrective_action_plan.md bytes)`

---

## Regulatory Timeline Summary

| Date | Event |
|------|-------|
| 2024-05-28 | Rule 15c6-1 T+1 settlement effective |
| 2024-10-15 | AROS v4.2 deployed (UTC_OFFSET = -4 for EDT) |
| 2024-11-03 | US Eastern DST switch: EDT → EST (UTC-4 → UTC-5) |
| 2024-11-03 | AROS v4.2 fails to update UTC_OFFSET; incident begins |
| 2024-11-04 | Incident identified and AROS halted |
| 2024-11-05 | SEC preliminary inquiry notice issued |
| 2024-11-06 | Legal counsel memo: price_diff_usd superseded by price_diff_vwap_usd |
| 2024-11-10 | SEC formal investigation opened (Case TM-2024-1103-AQ) |
| 2024-11-17 | Backtest certification deadline |

SEC Division of Trading and Markets
Case No. TM-2024-1103-AQ
2024-11-10T15:00:00Z
