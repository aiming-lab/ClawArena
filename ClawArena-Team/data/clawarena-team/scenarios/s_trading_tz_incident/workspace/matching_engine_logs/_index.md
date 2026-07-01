# Matching Engine Logs Index
**Cluster:** FinClear Asia — Singapore (UTC+8 local; all log timestamps in UTC)
**Log format:** Structured text; one event per line.
**Timezone declaration:** ALL timestamps in this log directory are in UTC.
  The `tz_offset_applied` field records the offset applied to dispatch messages,
  NOT the log timestamp timezone.

## Field Legend

| Field | Type | Notes |
|---|---|---|
| `order_id` | string | Pattern: `ORD-{8-digit seq}` |
| `symbol` | string | Affected: SGEX, HKFIN, JPNBK, AUHLD, TWSMC, KRSEC, CNTECH; Test: TESTX, TESTY |
| `side` | string | BUY or SELL |
| `qty` | integer | Share quantity |
| `fill_price` | float | Price in USD equivalent |
| `match_ts_utc` | string | UTC timestamp of match event (always UTC) |
| `dispatch_ts_utc` | string | Timestamp sent in dispatch message (may carry wrong offset after root-cause event) |
| `tz_offset_applied` | string | Critical: correct production value is "+00:00"; wrong value "+08:00" after 17:23:09Z on 2026-03-27 |
| `dispatch_status` | string | SENT, ACK, REJECTED, PENDING |

## CONFIG_RELOAD Events

CONFIG_RELOAD events appear on lines starting with:
  `[MATCHING-CONFIG] CONFIG_RELOAD`

Key fields: `adapter`, `version`, `tz_offset_applied`, `previous_value`, `operator`, `build_id`

**Distinction between adapters:**
- `dispatch_adapter` — production adapter; handles all live trade confirmations to ClearRoute EU
- `test_dispatch_adapter` — test/staging adapter; events on this adapter do NOT affect production settlement

## Files

| File | Time Range | Contents |
|---|---|---|
| `matching_2026-03-27_part1.log` | 07:00–15:00 UTC | Normal production orders; two decoy CONFIG_RELOAD events on test_dispatch_adapter |
| `matching_2026-03-27_part2.log` | 15:00–23:00 UTC | **Contains the root-cause CONFIG_RELOAD event**; mis-offset dispatch begins |
| `matching_2026-03-28_part1.log` | 00:00–09:15 UTC | Continued mis-offset dispatch; batch reconciliation alarm at 09:15:00Z |
| `matching_2026-03-28_part2.log` | 09:15–17:00 UTC | Incident response; config rollback at 09:47:00Z; normal dispatch resumes |
