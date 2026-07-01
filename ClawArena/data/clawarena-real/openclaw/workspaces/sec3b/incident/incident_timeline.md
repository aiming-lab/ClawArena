# ArtemisQ Capital — Incident Timeline (DRAFT)
## Event: AROS v4.2 Timezone Misconfiguration (2024-11-03)

> DRAFT — Subject to revision. Two data points below marked [VERIFY] are contested.

### Background
AROS v4.2 was deployed 2024-10-15. The timezone configuration was set to UTC-4
(America/New_York EDT) at deployment time. The US Eastern timezone switched from
EDT (UTC-4) to EST (UTC-5) on **2024-11-03 at 02:00 local time**.

AROS v4.2 hardcoded `UTC_OFFSET = -4` in `code/aros/timezone_config.py`.
No automatic DST adjustment was implemented.

### Timeline (UTC)

| Time (UTC) | Event |
|------------|-------|
| 2024-11-03T07:00:00Z | AROS v4.2 pre-market startup; timezone_config loads UTC-4 |
| 2024-11-03T09:30:00Z | NYSE/CME markets open |
| 2024-11-03T14:00:00Z | [ANOMALY START] System begins T+1 cutoff calculations using wrong offset |
| 2024-11-03T14:30:00Z | First mis-timed T+1 settlement order fired |
| 2024-11-03T19:00:00Z | System computes CME settle trigger at 20:00 UTC [VERIFY — may be 21:00] |
| 2024-11-03T20:00:00Z | System triggers delta-hedge closes, 1 hour early |
| 2024-11-03T21:00:00Z | Correct CME daily settlement time (15:00 CT = 21:00 UTC in EST) |
| 2024-11-03T21:30:00Z | Compliance team detects MiFIR Field 28 timestamp discrepancy |
| 2024-11-03T22:00:00Z | AROS v4.2 trading halted by manual override |
| 2024-11-04T08:00:00Z | Root cause identified: UTC_OFFSET hardcoded as -4 instead of -5 |

### Estimated Impact

**[VERIFY]** Some internal estimates put the loss from mis-timed orders at approximately
the same scale as the Knight Capital incident loss figure of **$440M** (KCG preliminary
estimate). This figure is UNCONFIRMED and disputed — the authoritative KCG SEC figure
should be consulted. The actual ArtemisQ event loss is separately estimated and
much smaller.

The UTC offset error caused:
1. T+1 settlement orders submitted outside correct window (60-minute offset)
2. CME delta-hedge triggered 1 hour early (at 20:00 UTC instead of 21:00 UTC)
3. MiFIR Field 28 timestamps reported as local time (UTC-4) instead of UTC

### Key Configuration Error
- **File**: `code/aros/timezone_config.py`, line 42
- **Error value**: `UTC_OFFSET = -4`
- **Correct value**: `UTC_OFFSET = -5` (EST, after 2024-11-03 02:00 switchover)
