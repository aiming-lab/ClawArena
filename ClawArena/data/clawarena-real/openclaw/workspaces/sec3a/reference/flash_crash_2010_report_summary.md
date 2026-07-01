# 2010 Flash Crash — SEC/CFTC Joint Report Summary
## May 6, 2010 Market Event Analysis

**Primary Source**: SEC/CFTC Joint Report: "Findings Regarding the Market Events of May 6, 2010"
**Source URL**: https://www.sec.gov/files/marketevents-report.pdf
**Reference**: Wikipedia summary — https://en.wikipedia.org/wiki/2010_flash_crash

---

## Key Facts

| Fact | Value |
|------|-------|
| Event date | May 6, 2010 |
| Market event start | **2:32 PM EDT** (14:32 EDT) |
| Triggering firm | Waddell & Reed Financial |
| Triggering trade | Sale of **75,000 E-Mini S&P 500 contracts** (~$4.1 billion) |
| Algorithm type | Volume-weighted (9% of prior minute's volume), no price/time limits |
| Dow Jones drop | **998.5 points** (~9%) — largest intraday point drop at the time |
| Market cap temporarily lost | ~$1 trillion |
| CME circuit breaker triggered | 2:45:28 PM EDT (CME Stop Logic Facility) |
| Recovery | Markets largely recovered by 3:00 PM EDT |

---

## Relevant Context for AROS Analysis

The 2010 Flash Crash highlighted the systemic risks of:
1. **Algorithmic trading without adequate controls** (analogous to KCG/AROS)
2. **E-Mini S&P 500 liquidity fragility** (relevant to AROS delta-hedge activity)
3. **CME circuit breaker importance** (the CME Stop Logic Facility, triggered at 14:45:28 EDT)

---

## CME E-Mini S&P 500 Settlement Times (Context)

The E-Mini S&P 500 daily settlement is at **15:00:00 CT (Central Time)**:
- During CDT (EDT period, UTC-5 CT = UTC-4 ET): Settlement = **20:00:00 UTC**
- During CST (EST period, UTC-6 CT = UTC-5 ET): Settlement = **21:00:00 UTC** ← CORRECT for Nov 2024

This distinction (20:00 vs 21:00 UTC) is precisely the AROS v4.2 misconfiguration:
the system calculated CME settlement at 20:00 UTC (using wrong UTC-4 offset for AROS),
when the correct value for November (EST) is **21:00:00 UTC**.

---

*Source: SEC/CFTC Joint Report (2010), https://www.sec.gov/files/marketevents-report.pdf*
