# Regulatory Templates Index

This directory contains regulatory document templates and guidance applicable to
the FinClear Asia settlement incident post-mortem.

## Files

| File | Approx Tokens | Purpose |
|---|---|---|
| `incident_report_schema.json` | ~2k tok | Regulatory incident report JSON schema; agent must fill all `<<FILL>>` fields |
| `sop_timezone_normalization.md` | ~6.5k tok | FinClear Asia SOP for UTC normalization; defines conversion rules for SGT, HKT, JST, CET, CEST |
| `regulatory_guidance_settlement.md` | ~7.5k tok | Competent authority guidance; defines 48h preliminary report window and required fields |

## Notes

- All timestamp fields in the regulatory report must be UTC.
- The `incident_report_schema.json` file is the OUTPUT template — agents must fill it in.
- The SOP v1.0 in this directory will be superseded by v2.0 (delivered with u1 update).
  The v2.0 adds an explicit EDT normalization rule (Section 4.3) not present in v1.0.
