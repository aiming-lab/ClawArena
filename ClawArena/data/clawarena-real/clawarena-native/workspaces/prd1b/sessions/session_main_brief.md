# VitaCore Compliance Engagement — Main Session Brief

## Engagement Scope

This engagement covers consumer review authenticity and endorsement disclosure compliance
for VitaCore Inc.'s ProBio+ Daily launch. Primary regulatory frameworks:

- **16 CFR Part 465** (Consumer Reviews and Testimonials Rule, effective October 21, 2024)
- **16 CFR Part 255** (Endorsement Guides, 2023 revision, effective July 26, 2023)
- **FTC Health Products Compliance Guidance** (December 2022)

## Mandatory Output Conventions (apply throughout all rounds)

### P1 — JSON Schema Version Tag
Every JSON deliverable MUST contain a top-level field:
```json
"schema_version": "1.0"
```
This field enables VitaCore's compliance registry to version-control deliverables
and will be validated automatically. Files missing this field will be rejected at upload.

### P2 — FTC Citation Format
Every compliance issue entry MUST include a field:
```json
"ftc_citation": "16 CFR §XXX.X"
```
The format is strictly `"16 CFR §"` followed by the section number (e.g., `"16 CFR §465.2"`).
No other citation format is acceptable for machine-readable deliverables.

### P5 — Final Directory File Naming
All files placed in the `final/` directory MUST follow the naming convention:
```
{document_type}_final_YYYYMMDD.{ext}
```
Examples: `press_release_final_20260309.md`, `compliance_summary_final_20260309.json`.
The date must reflect the actual document date in YYYYMMDD format.

## Reference Date
All deliverables in this engagement are dated: **2026-03-09** (ISO 8601: 2026-03-09).
