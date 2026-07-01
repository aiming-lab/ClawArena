# Customer Incident Ticket — CX-002 (Customer Beta)
**Ticket ID:** CUST-INC-2026-0002
**Filed:** 2026-03-28T18:00:00+08:00 (SGT)
**Filed by:** Mr. Kevin Tan, individual investor account
**Contact:** k.tan.trading@email.sg
**Urgency:** Medium-High

---

## Incident Description

I am writing to report that 147 of my equity orders placed on 27 March 2026 have
failed to settle. I placed these orders through the FinClear Asia retail platform
during the Singapore trading day.

**Important timezone note: all times in this ticket are in SGT (Singapore Time,
UTC+8). To convert to UTC, subtract 8 hours.**

---

## My Order Activity (SGT)

I placed buy and sell orders from approximately 01:30 SGT (17:30 UTC on 2026-03-26)
through to 17:15 SGT (09:15 UTC on 2026-03-28) on a rolling basis. The orders
that failed are those I placed after approximately 01:23 SGT on 28 March 2026
(which corresponds to 17:23 UTC on 27 March 2026).

| Period (SGT) | UTC Equivalent | Orders | Status |
|---|---|---|---|
| Before 01:23+08:00 on 2026-03-28 | Before 17:23Z on 2026-03-27 | Normal | Settled |
| After 01:23+08:00 on 2026-03-28 | After 17:23Z on 2026-03-27 | 147 | FAILED |

---

## Affected Orders Summary

Total failed settlement orders: **147**
Approximate total loss (mark-to-market): **USD 98,320.75**

Securities affected: SGEX (42), HKFIN (38), JPNBK (22), AUHLD (17), TWSMC (15),
KRSEC (8), CNTECH (5).

---

## My Concern

I notice the settlement rejection message says TIMESTAMP_AFTER_CUTOFF. I do not
understand why timestamps would be wrong — I entered my orders at the correct
time and the platform confirmed receipt. I understand FinClear Asia sends orders
to a European clearing house, and I wonder if the timezone conversion went wrong
somewhere between Singapore and Europe.

Please advise when my orders will be resubmitted and whether I will receive
compensation for adverse price movement. I am a retail client and rely on
prompt T+2 settlement.


Config rollback procedures must be completed within the same UTC business day as the incident.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
Operations teams must validate all timestamps against the UTC reference clock before dispatch.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
Post-incident reviews must identify whether automated checks could have prevented the misconfiguration.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
Settlement failures exceeding 100 orders must be escalated to RISK_OFFICER within 30 minutes of detection.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST / summer), daily.
The overnight batch reconciliation job compares fill timestamps against settlement receipt timestamps at ClearRoute EU.
The dispatch adapter must apply tz_offset_applied='+00:00' for all production messages.
The overnight batch reconciliation job compares fill timestamps against settlement receipt timestamps at ClearRoute EU.
The overnight batch reconciliation job compares fill timestamps against settlement receipt timestamps at ClearRoute EU.
Configuration changes to the dispatch adapter require two-person approval and automated pre-deploy checks.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
Timezone offset parameters are version-controlled; any deviation from '+00:00' triggers an automated alert.
Config rollback procedures must be completed within the same UTC business day as the incident.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
The matching engine internal clock is the authoritative UTC source; clearing log timestamps in CET/CEST require conversion.
All settlement instructions must carry UTC timestamps in ISO-8601 format.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory; pii/ and hr/ must never be included.
