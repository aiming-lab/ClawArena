# DTCC T+1 Settlement Cycle Conversion Guide
## Based on DTCC T+1 Conversion Document, March 2024

**Source**: https://www.dtcc.com/-/media/Files/PDFs/T2/T1-Conversion-Document-March-2024.pdf

---

## T+1 Transition Summary

| Item | Value |
|------|-------|
| Effective date | **May 28, 2024** |
| Prior standard | T+2 (two business days) |
| New standard | T+1 (one business day) |
| Regulatory basis | SEC Rule 15c6-1 (amended) |

## Key Operational Changes

1. **Affirmation deadline**: By end of trade date (T) for institutional trades
2. **STP requirement**: Straight-through processing (Rule 17Ad-27)
3. **Timestamp precision**: UTC-aligned timestamps become more critical under T+1

## Impact on Timezone Accuracy

Under T+2, a 1-hour timestamp error rarely caused settlement fails.
Under T+1, the same 1-hour error can cause settlement deadline miscalculation,
leading to T+1 settlement fails with regulatory consequences.

---

*Source: DTCC MAY 2024 T+1 Conversion Guide, https://www.dtcc.com/-/media/Files/PDFs/T2/T1-Conversion-Document-March-2024.pdf*
