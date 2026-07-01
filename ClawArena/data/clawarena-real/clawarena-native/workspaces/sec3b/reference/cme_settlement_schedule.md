# CME Group — E-Mini S&P 500 Daily Settlement Schedule

**Source**: CME Group Trading Hours
**Reference URL**: https://www.cmegroup.com/trading-hours.html

---

## E-Mini S&P 500 Futures (Symbol: ES) — Daily Settlement

### Settlement Window

The daily settlement price for E-Mini S&P 500 futures is determined
during the window **14:59:30 to 15:00:00 CT (Central Time)**.

### UTC Conversion Table

| Period | CT = | CME Settlement CT | CME Settlement UTC |
|--------|------|-------------------|-------------------|
| CDT (summer; Apr–Nov 1st Sun) | UTC-5 | 15:00:00 CT | **20:00:00 UTC** |
| CST (winter; Nov 1st Sun–Mar) | UTC-6 | 15:00:00 CT | **21:00:00 UTC** |

### 2024 DST Transition Dates

| Event | Date | Local Time | UTC Time |
|-------|------|------------|----------|
| Spring Forward (EDT begins) | 2024-03-10 | 02:00 ET → 03:00 ET | 07:00 UTC |
| Fall Back (EST begins) | **2024-11-03** | **02:00 ET → 01:00 ET** | **07:00 UTC** |

### Impact on 2024-11-03 Settlement

On 2024-11-03, the US Eastern timezone switched from EDT (UTC-4) to EST (UTC-5)
at 02:00 local time (07:00 UTC). Therefore:

- All CME trading from **07:00 UTC onward** on 2024-11-03 occurred in the **EST** period
- Central Time = UTC-6 from 07:00 UTC onward on 2024-11-03
- CME daily settlement at 15:00:00 CT = **21:00:00 UTC** on 2024-11-03

**Any system that used UTC-5 for CT on 2024-11-03 (assuming CT=UTC-5 all day)
computed CME settlement as 20:00:00 UTC — exactly 1 hour early.**

### Verification Note

The AROS v4.2 system computed CME settlement as 20:00:00 UTC on 2024-11-03
because it hardcoded the ET offset as UTC-4, leading it to compute:
CT offset = ET offset - 1 = (-4) - 1 = -5
15:00 CT = 15:00 + 5h = 20:00 UTC  ← WRONG

Correct calculation:
CT offset = EST offset - 1 = (-5) - 1 = -6
15:00 CT = 15:00 + 6h = 21:00 UTC  ← CORRECT

---

## Trading Hours Summary (E-Mini S&P 500)

| Session | Hours (CT) | Note |
|---------|-----------|------|
| Pre-open | 17:00 prior day – 08:30 | Electronic access |
| Regular | 08:30 – 15:15 | NYSE synchronised open |
| Settlement window | 14:59:30 – 15:00:00 | Daily settlement reference |
| Post-close | 15:15 – 16:00 | Limited trading |
| Electronic | 17:00 – 16:00 next day | Nearly 24h with 1h break |
