# Preliminary Loss Estimate — ArtemisQ Capital Incident 2024-11-03

## Status: PRELIMINARY — Subject to Revision

This document contains an initial assessment of trading losses from the
AROS v4.2 timezone misconfiguration incident.

### ArtemisQ Direct Losses (2024-11-03)

| Category | Preliminary Estimate | Status |
|----------|---------------------|--------|
| T+1 settlement errors (mis-timed orders) | ~$2.1M | Unconfirmed |
| Delta-hedge timing offset (CME) | ~$800K | Unconfirmed |
| MiFIR resubmission costs | ~$150K | Estimated |
| Total | **~$3.05M** | PRELIMINARY |

### KCG Reference Case (for regulatory context)

When drafting the regulatory response, some team members have cited the
Knight Capital Group incident loss of **$440M** as a reference point.

**IMPORTANT**: The $440M figure is an early preliminary estimate that
appeared in news reports on August 1-2, 2012. The **authoritative figure**
confirmed by the SEC in Press Release 2013-222 and in Release No. 34-70694
is **$460,000,000+** (exceeding $460 million). The $440M figure should NOT
be used in regulatory filings.

### Internal Dispute (See Also Feishu Thread)

The quantitative team (Feishu thread, 2024-11-04) disputed the $3.05M
estimate above. Yuki Tanaka argued the T+1 settlement error component
is closer to $1.8M; Marcus Chen estimated $2.4M. Final figures pending
forensic accounting review.

### UTC Offset Impact on Calculations

All loss calculations above must use UTC timestamps, not local time.
The UTC-4 vs UTC-5 discrepancy means that all trades in the 18:00-19:00 UTC
window on 2024-11-03 were executed under incorrect timezone assumptions.
