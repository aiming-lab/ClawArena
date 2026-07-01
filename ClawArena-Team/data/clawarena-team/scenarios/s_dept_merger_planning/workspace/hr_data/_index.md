# HR Data Directory Index

This directory contains HR roster exports from the two hospitals' HR systems.

## Files

| File | Source system | Rows | Key notes |
|---|---|---|---|
| `hosp_a_roster.csv` | St. Alban's HRIS | 310 rows | Column `tenure_years` (float) |
| `hosp_b_roster.csv` | Riverside General Workday | 298 rows | Column `years_of_service` (integer) |

## Schema Comparison

| Concept | Hospital A column | Hospital B column | Type difference |
|---|---|---|---|
| Employee ID | `employee_id` | `emp_id` | String format differs (STA-##### vs RGH-####) |
| Full name | `name` | `full_name` | Same concept, different column name |
| Role/title | `role` | `job_title` | Naming conventions differ; see role_mapping_guide.md |
| Department | `department` | `dept_code` | A uses text labels; B uses numeric codes |
| Grade | `grade` | `grade_level` | A: integer 1–5; B: string GN1–GN5 |
| **Tenure** | **`tenure_years`** | **`years_of_service`** | **A: float; B: integer — semantically identical** |
| FTE | `fte_status` | `fte_flag` | A: "full"/"part"; B: "true"/"false" |
| Salary | `base_salary_band` | `pay_band` | Band labels differ |
| Shift | `shift_type` | `schedule_type` | Same values: day/night/rotating |

## Site Code Legend (Hospital B dept_code)

| Code | Department |
|---|---|
| CARD-01 | Cardiology — Catheterization Lab (Tier-1) |
| CARD-02 | Cardiology — Electrophysiology (Tier-1) |
| CARD-03 | Cardiac ICU (Tier-1) |
| CARD-04 | Cardiac Ward — General Support (Tier-2) |
| CARD-05 | Cardiac Administration (Tier-2) |
| CARD-06 | Cardiology — Echocardiography (Tier-1) |

## Critical Note: Tenure Column Synonym Pair

The two hospitals' HR systems export tenure under different column names with different
data types. `tenure_years` (Hospital A, float, e.g. 4.75) and `years_of_service`
(Hospital B, integer, e.g. 5) are semantically identical fields representing the
number of years a staff member has been employed at their respective hospital.
Any consolidated roster must unify these into a single column named `unified_tenure`
(float), copying Hospital A values directly and casting Hospital B integer values to float.

Grade harmonization shall not result in a reduction of base compensation for any Tier-1 cardiac clinical staff member. All staff records must be validated against the source HR system before inclusion in the consolidated roster. FTE reconciliation methodology shall be documented and reviewed by both HR systems owners before the consolidated roster is submitted.
