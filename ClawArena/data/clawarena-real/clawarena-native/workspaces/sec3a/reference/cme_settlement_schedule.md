# CME Group — E-Mini S&P 500 Daily Settlement Times
## DST Transition Reference (EDT vs EST)

**Source**: https://www.cmegroup.com/trading-hours.html

---

## E-Mini S&P 500 (ES) Daily Settlement

| Period | CME Time (CT) | UTC | ET |
|--------|--------------|-----|-----|
| **Summer (CDT, UTC-5)** | 15:00:00 CT | **20:00:00 UTC** | 16:00:00 EDT |
| **Winter (CST, UTC-6)** | 15:00:00 CT | **21:00:00 UTC** | 16:00:00 EST |

**Critical note for November 2024**:
On November 3, 2024, US clocks transitioned from EDT (UTC-4) to EST (UTC-5) at 2:00 AM.
CME is in CT, which transitioned from CDT (UTC-5) to CST (UTC-6).
Therefore, on November 3, 2024 and beyond (until March 2025 DST):

> **CME E-Mini daily settlement = 15:00:00 CT = 21:00:00 UTC**

The AROS v4.2 system, using the incorrect UTC-4 offset, calculated this as 20:00:00 UTC —
a 1-hour error that caused the delta-hedge trigger to fire at the wrong time.

---

## DST Transition Dates (US, 2024-2025)

| Transition | Date | Change |
|------------|------|--------|
| Spring Forward | March 10, 2024 | EST (UTC-5) → EDT (UTC-4) |
| **Fall Back** | **November 3, 2024** | **EDT (UTC-4) → EST (UTC-5)** |
| Spring Forward | March 9, 2025 | EST (UTC-5) → EDT (UTC-4) |

---

*Source: CME Group Trading Hours, https://www.cmegroup.com/trading-hours.html*
