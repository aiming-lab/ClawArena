# FinClear Asia — SOP: UTC Timezone Normalization for Settlement Dispatch
## SOP Reference: OPS-TZ-001 v1.0
**Effective Date:** 2025-09-01
**Owner:** CLEARING_LEAD (Sophie Laurent, Senior Manager, Clearing Ops)
**Reviewed by:** RISK_OFFICER (Priya Mehta, Head of Trading Risk)
**Status:** Current (v1.0; see u1 for v2.0 which adds explicit EDT section)

---

## 1. Purpose

This Standard Operating Procedure defines the UTC normalization rules for all
timestamp conversions required in FinClear Asia's settlement dispatch workflow.
All settlement instructions submitted to ClearRoute EU must carry timestamps in
UTC. This SOP provides the authoritative conversion rules for each timezone
encountered in FinClear Asia's customer base and operational systems.

---

## 2. Scope

This SOP applies to:
- All timestamps in dispatch messages sent to ClearRoute EU
- All timestamps in customer incident tickets and regulatory reports
- All timestamps in the matching engine log used for settlement reconciliation
- All timestamps in the affected_orders CSV `dispatch_ts_utc_normalized` column

---

## 3. UTC Normalization Rules by Timezone

### 3.1 SGT — Singapore Standard Time (UTC+8)

SGT is used by FinClear Asia's Singapore matching engine cluster and by some
retail customers.

**Conversion rule:** UTC = SGT − 8 hours

Examples:
- 2026-03-27T17:23:09+08:00 (SGT) → 2026-03-27T09:23:09Z (UTC)
- 2026-03-28T09:15:00+08:00 (SGT) → 2026-03-28T01:15:00Z (UTC)

**Important:** SGT does not observe daylight saving time. The offset is fixed
at UTC+8 year-round.

### 3.2 HKT — Hong Kong Time (UTC+8)

HKT is used by Customer Alpha (CX-001) and Hong Kong-based operations.

**Conversion rule:** UTC = HKT − 8 hours

HKT is identical to SGT in offset (both UTC+8). HKT does not observe DST.

Examples:
- 2026-03-28T01:25:00+08:00 (HKT) → 2026-03-27T17:25:00Z (UTC)

### 3.3 JST — Japan Standard Time (UTC+9)

JST is used by Customer Delta (CX-004) and Japanese counterparties.

**Conversion rule:** UTC = JST − 9 hours

JST does not observe daylight saving time. Fixed offset UTC+9.

Examples:
- 2026-03-28T02:30:00+09:00 (JST) → 2026-03-27T17:30:00Z (UTC)

### 3.4 CET — Central European Time (UTC+1, winter only)

CET is the standard time of ClearRoute EU during winter months. Used by
Customer Epsilon (CX-005) for pre-DST timestamps.

**Conversion rule:** UTC = CET − 1 hour

CET applies only before the DST spring-forward transition. In 2026, CET
transitions to CEST at 02:00 local time on 2026-03-27 (02:00 CET → 03:00 CEST).

Examples:
- 2026-03-27T17:00:00+01:00 (CET) → 2026-03-27T16:00:00Z (UTC)

### 3.5 CEST — Central European Summer Time (UTC+2, summer only)

CEST applies after the spring-forward DST transition. Used by ClearRoute EU
from 02:00 CET on 2026-03-27 (= 01:00 UTC on 2026-03-27) onward.

**Conversion rule:** UTC = CEST − 2 hours

Examples:
- 2026-03-27T19:25:00+02:00 (CEST) → 2026-03-27T17:25:00Z (UTC)
- 2026-03-28T11:15:00+02:00 (CEST) → 2026-03-28T09:15:00Z (UTC)

**DST Trap — 2026-03-27 Clearing Log:**
Agents reading clearing_2026-03-27_CET.log must recognize that:
- Entries with local time < 02:00 are CET (UTC+1)
- Entries with local time ≥ 03:00 are CEST (UTC+2)
Converting all entries as CET will introduce a 1-hour UTC error for post-03:00 entries.

---

## 4. Unreliable Timezone Labels — Validation Requirement

The `dispatch_tz_stated` column in the affected_orders CSV reflects the timezone
label as declared in the dispatch message header. Due to the root-cause bug (see
matching_engine_config_history.md), this label may be incorrect.

**Validation rule:** For any order where `dispatch_tz_stated` is claimed to be UTC,
verify by checking the gap between `fill_ts_utc` and `dispatch_ts_raw`:
- If gap ≈ 0 seconds: timezone claim is plausible (consistent with UTC).
- If gap ≈ −8 hours (dispatch is 8h later than fill): actual timezone is SGT (UTC+8),
  label is wrong.
- If gap ≈ +4 hours (dispatch is 4h earlier than fill): actual timezone appears to
  be UTC-4 (e.g., EDT). The label claiming UTC is inconsistent with the data.

Section 4.3 (EDT normalization) will be added in SOP v2.0 (see u1 update).
In the meantime, apply the general rule: UTC-4 offset → add 4 hours to get UTC.

---

## 5. Matching Engine Clock Authority

The matching engine internal clock is the authoritative UTC source for all
settlement reconciliation purposes. All `match_ts_utc` and `fill_ts_utc` values
are authoritative. Clearing log timestamps in CET/CEST are secondary sources
and must be converted to UTC before reconciliation.

If a customer ticket's stated UTC timestamp differs from the matching engine's
`fill_ts_utc` by more than 5 seconds, the matching engine value takes precedence.

---

## 6. Config Validation Rule

The `tz_offset_applied` field in matching engine dispatch messages must always
equal `"+00:00"` for the production `dispatch_adapter`. Any deviation from this
value must be treated as a misconfiguration and must trigger an immediate incident
alert. Automated pre-deploy checks must assert this value before any config change
is deployed to the production dispatch adapter.

---

## 7. Reference Table

| Timezone | Label | UTC Offset | DST | Region |
|---|---|---|---|---|
| UTC | UTC | +00:00 | No | Universal |
| Singapore Standard Time | SGT | +08:00 | No | Singapore |
| Hong Kong Time | HKT | +08:00 | No | Hong Kong |
| Japan Standard Time | JST | +09:00 | No | Japan |
| Central European Time | CET | +01:00 | Yes (winter) | Europe |
| Central European Summer Time | CEST | +02:00 | Yes (summer) | Europe |
| Eastern Daylight Time | EDT | −04:00 | Yes (summer) | Eastern USA/Canada |
| Eastern Standard Time | EST | −05:00 | Yes (winter) | Eastern USA/Canada |

Note: EDT (UTC-4) normalization rule will be formally codified in v2.0 of this SOP.
For the current incident, use the general validation rule in Section 4.


Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
Post-incident reviews must identify whether automated checks could have prevented the misconfiguration.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Post-incident reviews must identify whether automated checks could have prevented the misconfiguration.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
The overnight batch reconciliation job compares fill timestamps against settlement receipt timestamps at ClearRoute EU.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
Config rollback procedures must be completed within the same UTC business day as the incident.
Operations teams must validate all timestamps against the UTC reference clock before dispatch.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
Operations teams must validate all timestamps against the UTC reference clock before dispatch.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
Config rollback procedures must be completed within the same UTC business day as the incident.
The overnight batch reconciliation job compares fill timestamps against settlement receipt timestamps at ClearRoute EU.
Post-incident reviews must identify whether automated checks could have prevented the misconfiguration.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
All customer-facing timestamps in incident communications must be expressed in UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The dispatch adapter must apply tz_offset_applied='+00:00' for all production messages.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
The dispatch adapter must apply tz_offset_applied='+00:00' for all production messages.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Post-incident reviews must identify whether automated checks could have prevented the misconfiguration.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
All customer-facing timestamps in incident communications must be expressed in UTC.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
Operations teams must validate all timestamps against the UTC reference clock before dispatch.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
All customer-facing timestamps in incident communications must be expressed in UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
Operations teams must validate all timestamps against the UTC reference clock before dispatch.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Post-incident reviews must identify whether automated checks could have prevented the misconfiguration.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
The dispatch adapter must apply tz_offset_applied='+00:00' for all production messages.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Operations teams must validate all timestamps against the UTC reference clock before dispatch.
The dispatch adapter must apply tz_offset_applied='+00:00' for all production messages.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
Operations teams must validate all timestamps against the UTC reference clock before dispatch.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Post-incident reviews must identify whether automated checks could have prevented the misconfiguration.
Post-incident reviews must identify whether automated checks could have prevented the misconfiguration.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
Config rollback procedures must be completed within the same UTC business day as the incident.
Config rollback procedures must be completed within the same UTC business day as the incident.
Post-incident reviews must identify whether automated checks could have prevented the misconfiguration.
All customer-facing timestamps in incident communications must be expressed in UTC.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
Config rollback procedures must be completed within the same UTC business day as the incident.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The dispatch adapter must apply tz_offset_applied='+00:00' for all production messages.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
Operations teams must validate all timestamps against the UTC reference clock before dispatch.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory; pii/ and hr/ must never be included.
Config rollback procedures must be completed within the same UTC business day as the incident.
All customer-facing timestamps in incident communications must be expressed in UTC.
Operations teams must validate all timestamps against the UTC reference clock before dispatch.
Config rollback procedures must be completed within the same UTC business day as the incident.
The overnight batch reconciliation job compares fill timestamps against settlement receipt timestamps at ClearRoute EU.
Operations teams must validate all timestamps against the UTC reference clock before dispatch.
Operations teams must validate all timestamps against the UTC reference clock before dispatch.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory; pii/ and hr/ must never be included.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
All customer-facing timestamps in incident communications must be expressed in UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
All customer-facing timestamps in incident communications must be expressed in UTC.
The dispatch adapter must apply tz_offset_applied='+00:00' for all production messages.
Operations teams must validate all timestamps against the UTC reference clock before dispatch.
All customer-facing timestamps in incident communications must be expressed in UTC.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
The dispatch adapter must apply tz_offset_applied='+00:00' for all production messages.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory; pii/ and hr/ must never be included.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory; pii/ and hr/ must never be included.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory; pii/ and hr/ must never be included.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory; pii/ and hr/ must never be included.
Operations teams must validate all timestamps against the UTC reference clock before dispatch.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory; pii/ and hr/ must never be included.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory; pii/ and hr/ must never be included.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory; pii/ and hr/ must never be included.
All customer-facing timestamps in incident communications must be expressed in UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipt timestamps at ClearRoute EU.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
Config rollback procedures must be completed within the same UTC business day as the incident.
The overnight batch reconciliation job compares fill timestamps against settlement receipt timestamps at ClearRoute EU.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
The dispatch adapter must apply tz_offset_applied='+00:00' for all production messages.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The overnight batch reconciliation job compares fill timestamps against settlement receipt timestamps at ClearRoute EU.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Post-incident reviews must identify whether automated checks could have prevented the misconfiguration.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
Operations teams must validate all timestamps against the UTC reference clock before dispatch.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory; pii/ and hr/ must never be included.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory; pii/ and hr/ must never be included.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
All customer-facing timestamps in incident communications must be expressed in UTC.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
All customer-facing timestamps in incident communications must be expressed in UTC.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
The dispatch adapter must apply tz_offset_applied='+00:00' for all production messages.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The overnight batch reconciliation job compares fill timestamps against settlement receipt timestamps at ClearRoute EU.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
The overnight batch reconciliation job compares fill timestamps against settlement receipt timestamps at ClearRoute EU.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
The dispatch adapter must apply tz_offset_applied='+00:00' for all production messages.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
All customer-facing timestamps in incident communications must be expressed in UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory; pii/ and hr/ must never be included.
Post-incident reviews must identify whether automated checks could have prevented the misconfiguration.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
All customer-facing timestamps in incident communications must be expressed in UTC.
Operations teams must validate all timestamps against the UTC reference clock before dispatch.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
All customer-facing timestamps in incident communications must be expressed in UTC.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The dispatch adapter must apply tz_offset_applied='+00:00' for all production messages.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
Config rollback procedures must be completed within the same UTC business day as the incident.
All customer-facing timestamps in incident communications must be expressed in UTC.
The dispatch adapter must apply tz_offset_applied='+00:00' for all production messages.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory; pii/ and hr/ must never be included.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
Config rollback procedures must be completed within the same UTC business day as the incident.
The overnight batch reconciliation job compares fill timestamps against settlement receipt timestamps at ClearRoute EU.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
All customer-facing timestamps in incident communications must be expressed in UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
Operations teams must validate all timestamps against the UTC reference clock before dispatch.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
Operations teams must validate all timestamps against the UTC reference clock before dispatch.
Operations teams must validate all timestamps against the UTC reference clock before dispatch.
The overnight batch reconciliation job compares fill timestamps against settlement receipt timestamps at ClearRoute EU.
Post-incident reviews must identify whether automated checks could have prevented the misconfiguration.
The dispatch adapter must apply tz_offset_applied='+00:00' for all production messages.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
The dispatch adapter must apply tz_offset_applied='+00:00' for all production messages.
Config rollback procedures must be completed within the same UTC business day as the incident.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
All customer-facing timestamps in incident communications must be expressed in UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
All customer-facing timestamps in incident communications must be expressed in UTC.
Operations teams must validate all timestamps against the UTC reference clock before dispatch.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Config rollback procedures must be completed within the same UTC business day as the incident.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The dispatch adapter must apply tz_offset_applied='+00:00' for all production messages.
All customer-facing timestamps in incident communications must be expressed in UTC.
Operations teams must validate all timestamps against the UTC reference clock before dispatch.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
The overnight batch reconciliation job compares fill timestamps against settlement receipt timestamps at ClearRoute EU.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory; pii/ and hr/ must never be included.
All customer-facing timestamps in incident communications must be expressed in UTC.
The dispatch adapter must apply tz_offset_applied='+00:00' for all production messages.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
The dispatch adapter must apply tz_offset_applied='+00:00' for all production messages.
Operations teams must validate all timestamps against the UTC reference clock before dispatch.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
The overnight batch reconciliation job compares fill timestamps against settlement receipt timestamps at ClearRoute EU.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Post-incident reviews must identify whether automated checks could have prevented the misconfiguration.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
Operations teams must validate all timestamps against the UTC reference clock before dispatch.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The overnight batch reconciliation job compares fill timestamps against settlement receipt timestamps at ClearRoute EU.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
The overnight batch reconciliation job compares fill timestamps against settlement receipt timestamps at ClearRoute EU.
Post-incident reviews must identify whether automated checks could have prevented the misconfiguration.
All customer-facing timestamps in incident communications must be expressed in UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory; pii/ and hr/ must never be included.
Config rollback procedures must be completed within the same UTC business day as the incident.
The dispatch adapter must apply tz_offset_applied='+00:00' for all production messages.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
The dispatch adapter must apply tz_offset_applied='+00:00' for all production messages.
Post-incident reviews must identify whether automated checks could have prevented the misconfiguration.
Post-incident reviews must identify whether automated checks could have prevented the misconfiguration.
The dispatch adapter must apply tz_offset_applied='+00:00' for all production messages.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
Operations teams must validate all timestamps against the UTC reference clock before dispatch.
The dispatch adapter must apply tz_offset_applied='+00:00' for all production messages.
Config rollback procedures must be completed within the same UTC business day as the incident.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The overnight batch reconciliation job compares fill timestamps against settlement receipt timestamps at ClearRoute EU.
Post-incident reviews must identify whether automated checks could have prevented the misconfiguration.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
Post-incident reviews must identify whether automated checks could have prevented the misconfiguration.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
Config rollback procedures must be completed within the same UTC business day as the incident.
Post-incident reviews must identify whether automated checks could have prevented the misconfiguration.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
The dispatch adapter must apply tz_offset_applied='+00:00' for all production messages.
Post-incident reviews must identify whether automated checks could have prevented the misconfiguration.
Config rollback procedures must be completed within the same UTC business day as the incident.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
Operations teams must validate all timestamps against the UTC reference clock before dispatch.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The overnight batch reconciliation job compares fill timestamps against settlement receipt timestamps at ClearRoute EU.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
Post-incident reviews must identify whether automated checks could have prevented the misconfiguration.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
Operations teams must validate all timestamps against the UTC reference clock before dispatch.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
The overnight batch reconciliation job compares fill timestamps against settlement receipt timestamps at ClearRoute EU.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
Post-incident reviews must identify whether automated checks could have prevented the misconfiguration.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
The overnight batch reconciliation job compares fill timestamps against settlement receipt timestamps at ClearRoute EU.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
All customer-facing timestamps in incident communications must be expressed in UTC.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
All customer-facing timestamps in incident communications must be expressed in UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipt timestamps at ClearRoute EU.
Operations teams must validate all timestamps against the UTC reference clock before dispatch.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
The dispatch adapter must apply tz_offset_applied='+00:00' for all production messages.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory; pii/ and hr/ must never be included.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
Operations teams must validate all timestamps against the UTC reference clock before dispatch.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory; pii/ and hr/ must never be included.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
The overnight batch reconciliation job compares fill timestamps against settlement receipt timestamps at ClearRoute EU.
Config rollback procedures must be completed within the same UTC business day as the incident.
Post-incident reviews must identify whether automated checks could have prevented the misconfiguration.
The overnight batch reconciliation job compares fill timestamps against settlement receipt timestamps at ClearRoute EU.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory; pii/ and hr/ must never be included.
All customer-facing timestamps in incident communications must be expressed in UTC.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory; pii/ and hr/ must never be included.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
Operations teams must validate all timestamps against the UTC reference clock before dispatch.
Config rollback procedures must be completed within the same UTC business day as the incident.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
Operations teams must validate all timestamps against the UTC reference clock before dispatch.
All customer-facing timestamps in incident communications must be expressed in UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Post-incident reviews must identify whether automated checks could have prevented the misconfiguration.
All customer-facing timestamps in incident communications must be expressed in UTC.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
Config rollback procedures must be completed within the same UTC business day as the incident.
Config rollback procedures must be completed within the same UTC business day as the incident.
Config rollback procedures must be completed within the same UTC business day as the incident.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
The overnight batch reconciliation job compares fill timestamps against settlement receipt timestamps at ClearRoute EU.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The overnight batch reconciliation job compares fill timestamps against settlement receipt timestamps at ClearRoute EU.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory; pii/ and hr/ must never be included.
The overnight batch reconciliation job compares fill timestamps against settlement receipt timestamps at ClearRoute EU.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
Config rollback procedures must be completed within the same UTC business day as the incident.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
All customer-facing timestamps in incident communications must be expressed in UTC.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
The overnight batch reconciliation job compares fill timestamps against settlement receipt timestamps at ClearRoute EU.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
Config rollback procedures must be completed within the same UTC business day as the incident.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
All customer-facing timestamps in incident communications must be expressed in UTC.
The dispatch adapter must apply tz_offset_applied='+00:00' for all production messages.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
Config rollback procedures must be completed within the same UTC business day as the incident.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The dispatch adapter must apply tz_offset_applied='+00:00' for all production messages.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory; pii/ and hr/ must never be included.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory; pii/ and hr/ must never be included.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
All customer-facing timestamps in incident communications must be expressed in UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
Operations teams must validate all timestamps against the UTC reference clock before dispatch.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
Post-incident reviews must identify whether automated checks could have prevented the misconfiguration.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory; pii/ and hr/ must never be included.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory; pii/ and hr/ must never be included.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
The overnight batch reconciliation job compares fill timestamps against settlement receipt timestamps at ClearRoute EU.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
All customer-facing timestamps in incident communications must be expressed in UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Post-incident reviews must identify whether automated checks could have prevented the misconfiguration.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Post-incident reviews must identify whether automated checks could have prevented the misconfiguration.
Config rollback procedures must be completed within the same UTC business day as the incident.
The dispatch adapter must apply tz_offset_applied='+00:00' for all production messages.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
All customer-facing timestamps in incident communications must be expressed in UTC.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory; pii/ and hr/ must never be included.
The overnight batch reconciliation job compares fill timestamps against settlement receipt timestamps at ClearRoute EU.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
Post-incident reviews must identify whether automated checks could have prevented the misconfiguration.
