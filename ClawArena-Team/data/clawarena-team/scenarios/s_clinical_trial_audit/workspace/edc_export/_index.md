# EDC Export — Column Schema and Site Legend

**Study:** NT-7701 Phase II Randomised Clinical Trial
**Export date:** 2026-04-15 (post-data-freeze; final locked dataset)
**Export format:** CSV, one file per investigator site

---

## Column Schema

| Column | Type | Description |
|---|---|---|
| `subject_id` | string | Subject identifier: `{SITE_CODE}-{4-digit seq}`, e.g. `BLR-0001` |
| `site_id` | string | Site identifier: one of `site_01` through `site_05` |
| `ae_term` | string | MedDRA preferred term for the adverse event |
| `grade` | integer | CTCAE v5.0 grade (1–4) |
| `onset_date` | string | Date of AE onset, ISO format `YYYY-MM-DD` |
| `sae_flag` | string | `"true"` if event meets SAE criteria; `"false"` otherwise |
| `resolved_flag` | string | `"true"` if event resolved by data freeze; `"false"` otherwise |
| `narrative_ref` | string | Free-text cross-reference code linking to source narrative |

**Key filter for audit:** Grade-3 SAEs are rows where `grade == 3 AND sae_flag == "true"`.

---

## Site Legend

| site_id | Site Location | Site Code | Principal Investigator |
|---|---|---|---|
| `site_01` | Bangalore, India | BLR | Dr. Rajan Krishnamurthy |
| `site_02` | Berlin, Germany | BER | Prof. Helga Braun |
| `site_03` | Toronto, Canada | TOR | Dr. Michael Chen |
| `site_04` | São Paulo, Brazil | GRU | Dra. Claudia Faria |
| `site_05` | Seoul, South Korea | SEL | Prof. Ji-young Park |

---

## Data Integrity Notes

- The EDC is the **authoritative source** for all adverse event data, per SOP-DI-003-v3.
- Site 03 (Toronto) has three events with `ae_term = "Elevated liver enzymes"` coded
  Grade 3 by the treating physician. The CRO classified these as Grade 2 in their summary.
  The query resolution in `pi_correspondence/email_site_queries.md` confirms Grade 3 is
  correct per the treating physician's documented clinical rationale. These events must be
  counted as Grade-3 SAEs in any audit reconciliation.
- Data was frozen site-by-site; freeze timestamps are documented in
  `cro_reports/data_freeze_log.txt`.
