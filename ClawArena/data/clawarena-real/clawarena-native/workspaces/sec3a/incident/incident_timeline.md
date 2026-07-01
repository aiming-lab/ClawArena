# ArtemisQ Capital — AROS v4.2 Incident Timeline (DRAFT)
## Date: 2024-11-03 (US Eastern Standard Time Transition Day)

**Author**: Marcus Chen (Lead Quant Engineer)
**Status**: DRAFT — pending compliance review

---

## Background

On Sunday, November 3, 2024, US clocks transitioned from Eastern Daylight Time (EDT, UTC-4)
to Eastern Standard Time (EST, UTC-5) at 2:00 AM local time. The AROS v4.2 automatic market
order routing system had a hard-coded timezone offset of UTC-4 in its configuration, which
was not updated for the DST transition.

---

## Timeline of Events (All times in UTC unless noted)

| Time (UTC) | Event |
|-----------|-------|
| 2024-11-03T06:00:00Z | DST transition: US clocks set back. AROS still configured UTC-4. |
| 2024-11-03T13:30:00Z | NYSE market open (9:30 AM ET = 14:30 UTC in EST; system believes 13:30 UTC) |
| **2024-11-03T14:00:00Z** | **Start of AROS error window: T+1 orders begin processing with wrong cutoff** |
| **2024-11-03T15:00:00Z** | **End of AROS error window: CME delta-hedge trigger missed by 1h** |
| 2024-11-03T19:00:00Z | AROS system generates Field 28 reports with UTC-4 offset (WRONG: should be UTC-5) |
| 2024-11-03T21:00:00Z | CME E-Mini daily settlement (15:00 CT = 21:00 UTC in EST) — AROS calculated 20:00 UTC |

---

## Incident Characteristics

- **Root cause**: Hard-coded `UTC_OFFSET = -4` in `timezone_config.py` (line 47), not updated for DST
- **Correct value**: `UTC_OFFSET = -5` (EST, November through March)
- **Duration of impact**: Approximately 1 hour offset error throughout trading day
- **Affected systems**: T+1 settlement scheduler, CME delta-hedge trigger, MiFIR Field 28 reporting

---

## [DRAFT ERROR 1 — DO NOT USE]
~~The initial loss estimate from Li Wei's Feishu message was $440M — this figure is cited in
the bot summary but has been flagged as potentially erroneous. Pending confirmation.~~

## [DRAFT ERROR 2 — DO NOT USE]
~~The CME E-Mini daily settlement time was incorrectly noted as 20:00:00 UTC (EDT equivalent).
The correct value for EST period is 21:00:00 UTC (15:00 CT = UTC+6 in EST).~~

---

## Reference: Knight Capital Group 2012 Incident (SEC Release No. 34-70694)

The KCG incident on August 1, 2012 shares structural similarities with the AROS incident:
- **KCG**: Manual deployment to 8 SMARS servers; 1 server missed update → errant trading
- **AROS**: Manual timezone config update missed on DST transition → systematic time errors
- **KCG financial loss**: $460M+ (SEC-confirmed; initial $440M estimate was incorrect)
- **KCG penalty**: $12M (SEC civil money penalty)
- **KCG rule violated**: Rule 15c3-5(b)
- **KCG servers**: 8 SMARS servers
- **KCG pre-market emails**: 97 automated emails ("Power Peg disabled"), ignored before open
