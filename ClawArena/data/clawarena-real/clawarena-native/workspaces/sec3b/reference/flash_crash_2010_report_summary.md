# 2010 Flash Crash — Joint SEC/CFTC Report Summary

**Source**: SEC/CFTC Joint Advisory Committee Report, "Findings Regarding the
Market Events of May 6, 2010" (September 30, 2010)
**Reference URL**: https://www.sec.gov/files/marketevents-report.pdf

---

## Event Summary

On **May 6, 2010**, U.S. financial markets experienced one of the most severe
intraday price declines in history, known as the "Flash Crash."

### Key Facts

| Metric | Value |
|--------|-------|
| Date | 2010-05-06 |
| Crash start time | **14:32 EDT** |
| Trigger | Waddell & Reed automated sell order |
| Contracts sold | **75,000 E-Mini S&P 500 contracts** (~$4.1 billion notional) |
| Dow Jones drop | **998.5 points** (~9%) at intraday trough |
| Market cap lost | Approximately $1 trillion (temporarily) |
| CME circuit breaker | Triggered at 14:45:28 EDT |
| Recovery | Markets largely recovered within 36 minutes |

### Waddell & Reed's Algorithm

The sell order used a volume-based execution algorithm (VWAP-style) that
executed at 9% of the trading volume of the prior minute, with no price
or time limits. The algorithm was indifferent to price impact.

### CME Stop Logic Functionality

The CME Globex Stop Logic Functionality triggered at approximately
**14:45:28 PM EDT** on May 6, 2010, briefly pausing E-Mini trading
for approximately 5 seconds. This temporary pause allowed the market
to stabilize and prevented further precipitous decline.

---

## Relevance to Timezone/DST Compliance

The 2010 flash crash highlighted the importance of accurate UTC timestamping
for regulatory purposes:

1. SEC/CFTC post-event analysis relied heavily on precise UTC timestamps
   to reconstruct the sequence of market events
2. MiFIR Field 28 UTC requirement (FCA Market Watch 59) was partly motivated
   by the difficulty of cross-firm event reconstruction when different firms
   used different local-time reporting conventions
3. For CME E-Mini products specifically, settlement timing (15:00 CT) and
   circuit breaker trigger times are always expressed in CT, but must be
   converted to UTC for MiFIR regulatory reporting

---

## CME E-Mini S&P 500 — Settlement Time Reference

For ArtemisQ Capital's 2024-11-03 incident context:

- **CME daily settlement time**: 14:59:30-15:00:00 CT (Central Time)
- **During CDT (April–November, standard)**: CT = UTC-5, so 15:00 CT = **20:00 UTC**
- **During CST (November–March, after DST switch)**: CT = UTC-6, so 15:00 CT = **21:00 UTC**
- **2024-11-03 status**: DST switch occurred at 02:00 ET (07:00 UTC) on Nov 3, 2024;
  therefore for trades on Nov 3 AFTER 07:00 UTC, CT = UTC-6, and CME settlement = **21:00 UTC**

The AROS v4.2 bug caused the system to use 20:00 UTC as the CME settlement reference
on 2024-11-03 instead of the correct 21:00 UTC.
