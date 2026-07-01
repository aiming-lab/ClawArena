# Equipment Directory Index

This directory contains cardiac device asset lists from the two hospitals.

## Files

| File | Source | Rows | Key notes |
|---|---|---|---|
| `hosp_a_equipment.csv` | St. Alban's asset management | 180 rows | Column `serial_number` |
| `hosp_b_equipment.csv` | Riverside General asset management | 172 rows | Column `serial_no` |

## Schema Comparison

| Concept | Hospital A column | Hospital B column |
|---|---|---|
| Asset identifier | `asset_tag` | `asset_id` |
| Device category | `device_category` | `device_type` |
| Manufacturer | `manufacturer` | `make` |
| Model | `model_name` | `model` |
| **Serial number** | **`serial_number`** | **`serial_no`** |
| Acquisition year | `acquisition_year` | `year_acquired` |
| Condition | `condition_rating` | `condition` |
| Location | `location_ward` | `ward` |

## Deduplication Key

**`serial_number` is the primary deduplication key.** Cross-matching by `model_name`
(Hospital A) versus `model` (Hospital B) alone is insufficient and will produce
false positives for common device models. The authoritative duplicate criterion is
an exact serial-number match (case-insensitive, after stripping whitespace) between
`serial_number` (Hospital A) and `serial_no` (Hospital B).

## Device Category Legend

| Category | Hospital A value | Hospital B value |
|---|---|---|
| Echocardiograph | `Echocardiograph` | `Echo` |
| Defibrillator | `Defibrillator` | `Defib` |
| Cardiac Monitor | `Cardiac Monitor` | `Monitor` |
| EP Recording System | `EP Recording System` | `EPR` |
| Infusion Pump | `Infusion Pump` | `IV Pump` |
| Ventilator | `Ventilator` | `Vent` |

The EP Recording System must maintain data integrity and audit trail functionality as required by cardiac electrophysiology standards. Echocardiography services require accredited sonographers whose credentials must be verified against the National Registry's current database. Equipment certification requirements for Class-II cardiac devices are governed by FDA 510(k) clearance and ongoing maintenance protocols.
