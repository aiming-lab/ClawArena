# HR Analytics — Health Status Prediction Feature

**Feature Name**: HealthPredict v1.0 (beta)
**Release Target**: Q2 2025
**CTO Sponsor**: Stefan Vogel
**Privacy Classification**: RESTRICTED — Special Category Data (Art. 9 GDPR)
**DPO Review Required**: YES
**DPIA Status**: UPDATE REQUIRED (see DPIA draft)

---

## 1. Executive Summary

HealthPredict adds an AI-powered health risk prediction module to the existing HR Analytics
platform. The feature processes employee behavioural indicators (sick leave patterns,
productivity metrics, meeting attendance) to generate a "health risk score" for each employee.
This score is used by HR managers to proactively identify employees who may benefit from
wellness interventions.

**GDPR Classification**: This feature processes health-related data constituting "special
categories of personal data" under Art. 9 GDPR. A DPIA update is mandatory.

---

## 2. Technical Architecture

### 2.1 Data Inputs

| Data Source | Data Type | Granularity | Retention |
|-------------|-----------|-------------|-----------|
| HR Records System | Sick leave days, medical certificates | Per employee, per month | 10 years |
| Calendar System | Meeting attendance rate, OOO blocks | Per employee, per week | 12 months |
| Productivity Monitoring | Task completion rate, login frequency | Per employee, per day | 6 months |
| Health Insurance Data (future) | Aggregate health cost indicators | Per employee, per quarter | TBD |

### 2.2 ML Model Architecture

The HealthPredict model uses a gradient-boosted ensemble (XGBoost + LightGBM) trained on:
- 3 years of historical sick leave patterns (2022-2024)
- Calendar metadata (meeting frequency, OOO frequency, after-hours logins)
- HR performance scores (correlated with health-related absence)

**Model outputs**:
- `health_risk_score`: float 0.0 to 1.0 (0 = low risk, 1 = very high risk)
- `risk_category`: enum {LOW, MEDIUM, HIGH, CRITICAL}
- `intervention_recommendation`: string (wellness programme type)

### 2.3 Data Flow

```
HR Records ──┐
Calendar ────┼──► Feature Engineering ──► XGBoost Model ──► health_risk_score
Productivity ┘                            (monthly retrain)    │
                                                                ▼
                                                         HR Manager Dashboard
                                                         (individual scores)
```

---

## 3. Privacy Impact Assessment Considerations

### 3.1 Art. 9 Special Category Data

The feature processes data "concerning health" per Art. 9(1) GDPR:
- Sick leave records: directly constitute health data
- Medical certificate references: health data
- Productivity correlations with health absence: inferred health data

**Legal basis required**: Art. 9(2) — available bases:
- Art. 9(2)(b): employment law obligations (not sufficient for profiling)
- Art. 9(2)(a): explicit consent (preferred)
- Art. 9(2)(h): health care / occupational medicine (requires medical professional involvement)

### 3.2 EDPB Nine-Criteria Assessment (Updated)

| Criterion | Assessment | Justification |
|-----------|-----------|---------------|
| Evaluation/scoring | YES | Health risk scores generated per employee |
| Automated decision with significant effect | YES | Scores inform HR interventions |
| Systematic monitoring | YES | Continuous monitoring of productivity/calendar |
| Sensitive/special category data | YES | Health data (Art. 9) |
| Large-scale processing | YES | 1,200 employees continuously |
| Data set matching/combining | YES | HR + calendar + productivity combined |
| Vulnerable subjects | YES | Employees (power imbalance) |
| Innovative technology | YES | AI/ML-based health risk prediction |
| Preventing exercise of rights | PARTIAL | Risk scores could affect promotions |

**Criteria met**: 8 of 9 (all but "preventing exercise of rights" is partial)

**DPIA Required**: YES — MANDATORY under both:
- EDPB ≥2 criteria threshold (8 criteria met)
- Art. 35(3)(b): large-scale processing of Art. 9 special category data

**SA Consultation (Art. 36)**: LIKELY REQUIRED given residual high risk

---

## 4. API Specification

### 4.1 Prediction Endpoint

```
POST /api/v1/hr-analytics/health-predict
Content-Type: application/json
Authorization: Bearer {hr_admin_token}

Request Body:
{
  "employee_id": "EMP-{uuid}",
  "assessment_period_start": "YYYY-MM-DD",
  "assessment_period_end": "YYYY-MM-DD",
  "include_recommendations": true
}

Response:
{
  "employee_id": "EMP-{uuid}",
  "assessment_period": {"start": "...", "end": "..."},
  "health_risk_score": 0.72,
  "risk_category": "HIGH",
  "contributing_factors": [
    {"factor": "sick_leave_frequency", "weight": 0.35},
    {"factor": "after_hours_login_rate", "weight": 0.28},
    {"factor": "meeting_attendance_decline", "weight": 0.22},
    {"factor": "productivity_score_trend", "weight": 0.15}
  ],
  "intervention_recommendation": "Referral to occupational health service",
  "model_version": "healthpredict-1.0.3",
  "generated_at": "YYYY-MM-DDTHH:MM:SSZ"
}
```

### 4.2 Batch Processing

```
POST /api/v1/hr-analytics/health-predict/batch
Content-Type: application/json

Request Body:
{
  "employee_ids": ["EMP-001", "EMP-002", ...],
  "assessment_period_start": "YYYY-MM-DD",
  "assessment_period_end": "YYYY-MM-DD"
}
```

Response includes `results` array with per-employee predictions.

---

## 5. Data Dictionary

| Field | Type | Description | Art. 9? |
|-------|------|-------------|---------|
| `sick_leave_days_30d` | integer | Sick leave days in last 30 days | YES |
| `sick_leave_days_90d` | integer | Sick leave days in last 90 days | YES |
| `sick_leave_days_365d` | integer | Sick leave days in last 365 days | YES |
| `medical_cert_count_90d` | integer | Medical certificates submitted in 90 days | YES |
| `meeting_attendance_rate` | float | % of invited meetings attended (last 30d) | NO |
| `ooo_events_30d` | integer | Out-of-office calendar events (30d) | NO |
| `after_hours_login_rate` | float | % of logins after 19:00 local time (30d) | NO |
| `task_completion_rate` | float | % of assigned tasks completed on time (30d) | NO |
| `productivity_score_trend` | float | Delta in productivity score vs prior quarter | NO |
| `health_risk_score` | float | Model output: 0.0 to 1.0 health risk | YES (derived) |
| `risk_category` | string | LOW / MEDIUM / HIGH / CRITICAL | YES (derived) |

---

## Feature Engineering Detail — Input 001

### Feature: `feature_001_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_001_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_001_normalized = (x - min_001) / (max_001 - min_001)
```

Where:
- `min_001` = historical minimum (0.10) computed on training set
- `max_001` = historical maximum (2.30) computed on training set

**Privacy note**: Feature 001 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (0.500)
**Outlier policy**: Winsorise at 99th percentile (2.10)

**Business interpretation**: Coefficient in final model: 0.0130 (relative importance rank: 1)

## Feature Engineering Detail — Input 002

### Feature: `feature_002_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_002_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_002_normalized = (x - min_002) / (max_002 - min_002)
```

Where:
- `min_002` = historical minimum (0.20) computed on training set
- `max_002` = historical maximum (4.60) computed on training set

**Privacy note**: Feature 002 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (1.000)
**Outlier policy**: Winsorise at 99th percentile (4.20)

**Business interpretation**: Coefficient in final model: 0.0160 (relative importance rank: 2)

## Feature Engineering Detail — Input 003

### Feature: `feature_003_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_003_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_003_normalized = (x - min_003) / (max_003 - min_003)
```

Where:
- `min_003` = historical minimum (0.30) computed on training set
- `max_003` = historical maximum (6.90) computed on training set

**Privacy note**: Feature 003 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (1.500)
**Outlier policy**: Winsorise at 99th percentile (6.30)

**Business interpretation**: Coefficient in final model: 0.0190 (relative importance rank: 3)

## Feature Engineering Detail — Input 004

### Feature: `feature_004_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_004_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_004_normalized = (x - min_004) / (max_004 - min_004)
```

Where:
- `min_004` = historical minimum (0.40) computed on training set
- `max_004` = historical maximum (9.20) computed on training set

**Privacy note**: Feature 004 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (2.000)
**Outlier policy**: Winsorise at 99th percentile (8.40)

**Business interpretation**: Coefficient in final model: 0.0220 (relative importance rank: 4)

## Feature Engineering Detail — Input 005

### Feature: `feature_005_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_005_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_005_normalized = (x - min_005) / (max_005 - min_005)
```

Where:
- `min_005` = historical minimum (0.50) computed on training set
- `max_005` = historical maximum (11.50) computed on training set

**Privacy note**: Feature 005 is directly health-related (Art. 9)
**Null handling**: Replace null with population median (2.500)
**Outlier policy**: Winsorise at 99th percentile (10.50)

**Business interpretation**: Coefficient in final model: 0.0250 (relative importance rank: 5)

## Feature Engineering Detail — Input 006

### Feature: `feature_006_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_006_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_006_normalized = (x - min_006) / (max_006 - min_006)
```

Where:
- `min_006` = historical minimum (0.60) computed on training set
- `max_006` = historical maximum (13.80) computed on training set

**Privacy note**: Feature 006 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (3.000)
**Outlier policy**: Winsorise at 99th percentile (12.60)

**Business interpretation**: Coefficient in final model: 0.0280 (relative importance rank: 6)

## Feature Engineering Detail — Input 007

### Feature: `feature_007_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_007_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_007_normalized = (x - min_007) / (max_007 - min_007)
```

Where:
- `min_007` = historical minimum (0.70) computed on training set
- `max_007` = historical maximum (16.10) computed on training set

**Privacy note**: Feature 007 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (3.500)
**Outlier policy**: Winsorise at 99th percentile (14.70)

**Business interpretation**: Coefficient in final model: 0.0310 (relative importance rank: 7)

## Feature Engineering Detail — Input 008

### Feature: `feature_008_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_008_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_008_normalized = (x - min_008) / (max_008 - min_008)
```

Where:
- `min_008` = historical minimum (0.80) computed on training set
- `max_008` = historical maximum (18.40) computed on training set

**Privacy note**: Feature 008 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (4.000)
**Outlier policy**: Winsorise at 99th percentile (16.80)

**Business interpretation**: Coefficient in final model: 0.0340 (relative importance rank: 8)

## Feature Engineering Detail — Input 009

### Feature: `feature_009_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_009_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_009_normalized = (x - min_009) / (max_009 - min_009)
```

Where:
- `min_009` = historical minimum (0.90) computed on training set
- `max_009` = historical maximum (20.70) computed on training set

**Privacy note**: Feature 009 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (4.500)
**Outlier policy**: Winsorise at 99th percentile (18.90)

**Business interpretation**: Coefficient in final model: 0.0370 (relative importance rank: 9)

## Feature Engineering Detail — Input 010

### Feature: `feature_010_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_010_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_010_normalized = (x - min_010) / (max_010 - min_010)
```

Where:
- `min_010` = historical minimum (1.00) computed on training set
- `max_010` = historical maximum (23.00) computed on training set

**Privacy note**: Feature 010 is directly health-related (Art. 9)
**Null handling**: Replace null with population median (5.000)
**Outlier policy**: Winsorise at 99th percentile (21.00)

**Business interpretation**: Coefficient in final model: 0.0400 (relative importance rank: 10)

## Feature Engineering Detail — Input 011

### Feature: `feature_011_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_011_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_011_normalized = (x - min_011) / (max_011 - min_011)
```

Where:
- `min_011` = historical minimum (1.10) computed on training set
- `max_011` = historical maximum (25.30) computed on training set

**Privacy note**: Feature 011 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (5.500)
**Outlier policy**: Winsorise at 99th percentile (23.10)

**Business interpretation**: Coefficient in final model: 0.0430 (relative importance rank: 11)

## Feature Engineering Detail — Input 012

### Feature: `feature_012_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_012_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_012_normalized = (x - min_012) / (max_012 - min_012)
```

Where:
- `min_012` = historical minimum (1.20) computed on training set
- `max_012` = historical maximum (27.60) computed on training set

**Privacy note**: Feature 012 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (6.000)
**Outlier policy**: Winsorise at 99th percentile (25.20)

**Business interpretation**: Coefficient in final model: 0.0460 (relative importance rank: 12)

## Feature Engineering Detail — Input 013

### Feature: `feature_013_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_013_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_013_normalized = (x - min_013) / (max_013 - min_013)
```

Where:
- `min_013` = historical minimum (1.30) computed on training set
- `max_013` = historical maximum (29.90) computed on training set

**Privacy note**: Feature 013 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (6.500)
**Outlier policy**: Winsorise at 99th percentile (27.30)

**Business interpretation**: Coefficient in final model: 0.0490 (relative importance rank: 13)

## Feature Engineering Detail — Input 014

### Feature: `feature_014_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_014_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_014_normalized = (x - min_014) / (max_014 - min_014)
```

Where:
- `min_014` = historical minimum (1.40) computed on training set
- `max_014` = historical maximum (32.20) computed on training set

**Privacy note**: Feature 014 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (7.000)
**Outlier policy**: Winsorise at 99th percentile (29.40)

**Business interpretation**: Coefficient in final model: 0.0520 (relative importance rank: 14)

## Feature Engineering Detail — Input 015

### Feature: `feature_015_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_015_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_015_normalized = (x - min_015) / (max_015 - min_015)
```

Where:
- `min_015` = historical minimum (1.50) computed on training set
- `max_015` = historical maximum (34.50) computed on training set

**Privacy note**: Feature 015 is directly health-related (Art. 9)
**Null handling**: Replace null with population median (7.500)
**Outlier policy**: Winsorise at 99th percentile (31.50)

**Business interpretation**: Coefficient in final model: 0.0550 (relative importance rank: 15)

## Feature Engineering Detail — Input 016

### Feature: `feature_016_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_016_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_016_normalized = (x - min_016) / (max_016 - min_016)
```

Where:
- `min_016` = historical minimum (1.60) computed on training set
- `max_016` = historical maximum (36.80) computed on training set

**Privacy note**: Feature 016 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (8.000)
**Outlier policy**: Winsorise at 99th percentile (33.60)

**Business interpretation**: Coefficient in final model: 0.0580 (relative importance rank: 16)

## Feature Engineering Detail — Input 017

### Feature: `feature_017_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_017_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_017_normalized = (x - min_017) / (max_017 - min_017)
```

Where:
- `min_017` = historical minimum (1.70) computed on training set
- `max_017` = historical maximum (39.10) computed on training set

**Privacy note**: Feature 017 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (8.500)
**Outlier policy**: Winsorise at 99th percentile (35.70)

**Business interpretation**: Coefficient in final model: 0.0610 (relative importance rank: 17)

## Feature Engineering Detail — Input 018

### Feature: `feature_018_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_018_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_018_normalized = (x - min_018) / (max_018 - min_018)
```

Where:
- `min_018` = historical minimum (1.80) computed on training set
- `max_018` = historical maximum (41.40) computed on training set

**Privacy note**: Feature 018 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (9.000)
**Outlier policy**: Winsorise at 99th percentile (37.80)

**Business interpretation**: Coefficient in final model: 0.0640 (relative importance rank: 18)

## Feature Engineering Detail — Input 019

### Feature: `feature_019_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_019_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_019_normalized = (x - min_019) / (max_019 - min_019)
```

Where:
- `min_019` = historical minimum (1.90) computed on training set
- `max_019` = historical maximum (43.70) computed on training set

**Privacy note**: Feature 019 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (9.500)
**Outlier policy**: Winsorise at 99th percentile (39.90)

**Business interpretation**: Coefficient in final model: 0.0670 (relative importance rank: 19)

## Feature Engineering Detail — Input 020

### Feature: `feature_020_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_020_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_020_normalized = (x - min_020) / (max_020 - min_020)
```

Where:
- `min_020` = historical minimum (2.00) computed on training set
- `max_020` = historical maximum (46.00) computed on training set

**Privacy note**: Feature 020 is directly health-related (Art. 9)
**Null handling**: Replace null with population median (10.000)
**Outlier policy**: Winsorise at 99th percentile (42.00)

**Business interpretation**: Coefficient in final model: 0.0700 (relative importance rank: 20)

## Feature Engineering Detail — Input 021

### Feature: `feature_021_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_021_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_021_normalized = (x - min_021) / (max_021 - min_021)
```

Where:
- `min_021` = historical minimum (2.10) computed on training set
- `max_021` = historical maximum (48.30) computed on training set

**Privacy note**: Feature 021 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (10.500)
**Outlier policy**: Winsorise at 99th percentile (44.10)

**Business interpretation**: Coefficient in final model: 0.0730 (relative importance rank: 21)

## Feature Engineering Detail — Input 022

### Feature: `feature_022_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_022_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_022_normalized = (x - min_022) / (max_022 - min_022)
```

Where:
- `min_022` = historical minimum (2.20) computed on training set
- `max_022` = historical maximum (50.60) computed on training set

**Privacy note**: Feature 022 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (11.000)
**Outlier policy**: Winsorise at 99th percentile (46.20)

**Business interpretation**: Coefficient in final model: 0.0760 (relative importance rank: 22)

## Feature Engineering Detail — Input 023

### Feature: `feature_023_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_023_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_023_normalized = (x - min_023) / (max_023 - min_023)
```

Where:
- `min_023` = historical minimum (2.30) computed on training set
- `max_023` = historical maximum (52.90) computed on training set

**Privacy note**: Feature 023 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (11.500)
**Outlier policy**: Winsorise at 99th percentile (48.30)

**Business interpretation**: Coefficient in final model: 0.0790 (relative importance rank: 23)

## Feature Engineering Detail — Input 024

### Feature: `feature_024_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_024_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_024_normalized = (x - min_024) / (max_024 - min_024)
```

Where:
- `min_024` = historical minimum (2.40) computed on training set
- `max_024` = historical maximum (55.20) computed on training set

**Privacy note**: Feature 024 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (12.000)
**Outlier policy**: Winsorise at 99th percentile (50.40)

**Business interpretation**: Coefficient in final model: 0.0820 (relative importance rank: 24)

## Feature Engineering Detail — Input 025

### Feature: `feature_025_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_025_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_025_normalized = (x - min_025) / (max_025 - min_025)
```

Where:
- `min_025` = historical minimum (2.50) computed on training set
- `max_025` = historical maximum (57.50) computed on training set

**Privacy note**: Feature 025 is directly health-related (Art. 9)
**Null handling**: Replace null with population median (12.500)
**Outlier policy**: Winsorise at 99th percentile (52.50)

**Business interpretation**: Coefficient in final model: 0.0850 (relative importance rank: 25)

## Feature Engineering Detail — Input 026

### Feature: `feature_026_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_026_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_026_normalized = (x - min_026) / (max_026 - min_026)
```

Where:
- `min_026` = historical minimum (2.60) computed on training set
- `max_026` = historical maximum (59.80) computed on training set

**Privacy note**: Feature 026 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (13.000)
**Outlier policy**: Winsorise at 99th percentile (54.60)

**Business interpretation**: Coefficient in final model: 0.0880 (relative importance rank: 26)

## Feature Engineering Detail — Input 027

### Feature: `feature_027_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_027_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_027_normalized = (x - min_027) / (max_027 - min_027)
```

Where:
- `min_027` = historical minimum (2.70) computed on training set
- `max_027` = historical maximum (62.10) computed on training set

**Privacy note**: Feature 027 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (13.500)
**Outlier policy**: Winsorise at 99th percentile (56.70)

**Business interpretation**: Coefficient in final model: 0.0910 (relative importance rank: 27)

## Feature Engineering Detail — Input 028

### Feature: `feature_028_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_028_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_028_normalized = (x - min_028) / (max_028 - min_028)
```

Where:
- `min_028` = historical minimum (2.80) computed on training set
- `max_028` = historical maximum (64.40) computed on training set

**Privacy note**: Feature 028 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (14.000)
**Outlier policy**: Winsorise at 99th percentile (58.80)

**Business interpretation**: Coefficient in final model: 0.0940 (relative importance rank: 28)

## Feature Engineering Detail — Input 029

### Feature: `feature_029_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_029_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_029_normalized = (x - min_029) / (max_029 - min_029)
```

Where:
- `min_029` = historical minimum (2.90) computed on training set
- `max_029` = historical maximum (66.70) computed on training set

**Privacy note**: Feature 029 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (14.500)
**Outlier policy**: Winsorise at 99th percentile (60.90)

**Business interpretation**: Coefficient in final model: 0.0970 (relative importance rank: 29)

## Feature Engineering Detail — Input 030

### Feature: `feature_030_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_030_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_030_normalized = (x - min_030) / (max_030 - min_030)
```

Where:
- `min_030` = historical minimum (3.00) computed on training set
- `max_030` = historical maximum (69.00) computed on training set

**Privacy note**: Feature 030 is directly health-related (Art. 9)
**Null handling**: Replace null with population median (15.000)
**Outlier policy**: Winsorise at 99th percentile (63.00)

**Business interpretation**: Coefficient in final model: 0.1000 (relative importance rank: 30)

## Feature Engineering Detail — Input 031

### Feature: `feature_031_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_031_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_031_normalized = (x - min_031) / (max_031 - min_031)
```

Where:
- `min_031` = historical minimum (3.10) computed on training set
- `max_031` = historical maximum (71.30) computed on training set

**Privacy note**: Feature 031 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (15.500)
**Outlier policy**: Winsorise at 99th percentile (65.10)

**Business interpretation**: Coefficient in final model: 0.1030 (relative importance rank: 31)

## Feature Engineering Detail — Input 032

### Feature: `feature_032_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_032_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_032_normalized = (x - min_032) / (max_032 - min_032)
```

Where:
- `min_032` = historical minimum (3.20) computed on training set
- `max_032` = historical maximum (73.60) computed on training set

**Privacy note**: Feature 032 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (16.000)
**Outlier policy**: Winsorise at 99th percentile (67.20)

**Business interpretation**: Coefficient in final model: 0.1060 (relative importance rank: 32)

## Feature Engineering Detail — Input 033

### Feature: `feature_033_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_033_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_033_normalized = (x - min_033) / (max_033 - min_033)
```

Where:
- `min_033` = historical minimum (3.30) computed on training set
- `max_033` = historical maximum (75.90) computed on training set

**Privacy note**: Feature 033 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (16.500)
**Outlier policy**: Winsorise at 99th percentile (69.30)

**Business interpretation**: Coefficient in final model: 0.1090 (relative importance rank: 33)

## Feature Engineering Detail — Input 034

### Feature: `feature_034_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_034_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_034_normalized = (x - min_034) / (max_034 - min_034)
```

Where:
- `min_034` = historical minimum (3.40) computed on training set
- `max_034` = historical maximum (78.20) computed on training set

**Privacy note**: Feature 034 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (17.000)
**Outlier policy**: Winsorise at 99th percentile (71.40)

**Business interpretation**: Coefficient in final model: 0.1120 (relative importance rank: 34)

## Feature Engineering Detail — Input 035

### Feature: `feature_035_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_035_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_035_normalized = (x - min_035) / (max_035 - min_035)
```

Where:
- `min_035` = historical minimum (3.50) computed on training set
- `max_035` = historical maximum (80.50) computed on training set

**Privacy note**: Feature 035 is directly health-related (Art. 9)
**Null handling**: Replace null with population median (17.500)
**Outlier policy**: Winsorise at 99th percentile (73.50)

**Business interpretation**: Coefficient in final model: 0.1150 (relative importance rank: 35)

## Feature Engineering Detail — Input 036

### Feature: `feature_036_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_036_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_036_normalized = (x - min_036) / (max_036 - min_036)
```

Where:
- `min_036` = historical minimum (3.60) computed on training set
- `max_036` = historical maximum (82.80) computed on training set

**Privacy note**: Feature 036 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (18.000)
**Outlier policy**: Winsorise at 99th percentile (75.60)

**Business interpretation**: Coefficient in final model: 0.1180 (relative importance rank: 36)

## Feature Engineering Detail — Input 037

### Feature: `feature_037_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_037_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_037_normalized = (x - min_037) / (max_037 - min_037)
```

Where:
- `min_037` = historical minimum (3.70) computed on training set
- `max_037` = historical maximum (85.10) computed on training set

**Privacy note**: Feature 037 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (18.500)
**Outlier policy**: Winsorise at 99th percentile (77.70)

**Business interpretation**: Coefficient in final model: 0.1210 (relative importance rank: 37)

## Feature Engineering Detail — Input 038

### Feature: `feature_038_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_038_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_038_normalized = (x - min_038) / (max_038 - min_038)
```

Where:
- `min_038` = historical minimum (3.80) computed on training set
- `max_038` = historical maximum (87.40) computed on training set

**Privacy note**: Feature 038 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (19.000)
**Outlier policy**: Winsorise at 99th percentile (79.80)

**Business interpretation**: Coefficient in final model: 0.1240 (relative importance rank: 38)

## Feature Engineering Detail — Input 039

### Feature: `feature_039_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_039_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_039_normalized = (x - min_039) / (max_039 - min_039)
```

Where:
- `min_039` = historical minimum (3.90) computed on training set
- `max_039` = historical maximum (89.70) computed on training set

**Privacy note**: Feature 039 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (19.500)
**Outlier policy**: Winsorise at 99th percentile (81.90)

**Business interpretation**: Coefficient in final model: 0.1270 (relative importance rank: 39)

## Feature Engineering Detail — Input 040

### Feature: `feature_040_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_040_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_040_normalized = (x - min_040) / (max_040 - min_040)
```

Where:
- `min_040` = historical minimum (4.00) computed on training set
- `max_040` = historical maximum (92.00) computed on training set

**Privacy note**: Feature 040 is directly health-related (Art. 9)
**Null handling**: Replace null with population median (20.000)
**Outlier policy**: Winsorise at 99th percentile (84.00)

**Business interpretation**: Coefficient in final model: 0.1300 (relative importance rank: 40)

## Feature Engineering Detail — Input 041

### Feature: `feature_041_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_041_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_041_normalized = (x - min_041) / (max_041 - min_041)
```

Where:
- `min_041` = historical minimum (4.10) computed on training set
- `max_041` = historical maximum (94.30) computed on training set

**Privacy note**: Feature 041 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (20.500)
**Outlier policy**: Winsorise at 99th percentile (86.10)

**Business interpretation**: Coefficient in final model: 0.1330 (relative importance rank: 41)

## Feature Engineering Detail — Input 042

### Feature: `feature_042_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_042_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_042_normalized = (x - min_042) / (max_042 - min_042)
```

Where:
- `min_042` = historical minimum (4.20) computed on training set
- `max_042` = historical maximum (96.60) computed on training set

**Privacy note**: Feature 042 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (21.000)
**Outlier policy**: Winsorise at 99th percentile (88.20)

**Business interpretation**: Coefficient in final model: 0.1360 (relative importance rank: 42)

## Feature Engineering Detail — Input 043

### Feature: `feature_043_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_043_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_043_normalized = (x - min_043) / (max_043 - min_043)
```

Where:
- `min_043` = historical minimum (4.30) computed on training set
- `max_043` = historical maximum (98.90) computed on training set

**Privacy note**: Feature 043 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (21.500)
**Outlier policy**: Winsorise at 99th percentile (90.30)

**Business interpretation**: Coefficient in final model: 0.1390 (relative importance rank: 43)

## Feature Engineering Detail — Input 044

### Feature: `feature_044_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_044_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_044_normalized = (x - min_044) / (max_044 - min_044)
```

Where:
- `min_044` = historical minimum (4.40) computed on training set
- `max_044` = historical maximum (101.20) computed on training set

**Privacy note**: Feature 044 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (22.000)
**Outlier policy**: Winsorise at 99th percentile (92.40)

**Business interpretation**: Coefficient in final model: 0.1420 (relative importance rank: 44)

## Feature Engineering Detail — Input 045

### Feature: `feature_045_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_045_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_045_normalized = (x - min_045) / (max_045 - min_045)
```

Where:
- `min_045` = historical minimum (4.50) computed on training set
- `max_045` = historical maximum (103.50) computed on training set

**Privacy note**: Feature 045 is directly health-related (Art. 9)
**Null handling**: Replace null with population median (22.500)
**Outlier policy**: Winsorise at 99th percentile (94.50)

**Business interpretation**: Coefficient in final model: 0.1450 (relative importance rank: 45)

## Feature Engineering Detail — Input 046

### Feature: `feature_046_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_046_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_046_normalized = (x - min_046) / (max_046 - min_046)
```

Where:
- `min_046` = historical minimum (4.60) computed on training set
- `max_046` = historical maximum (105.80) computed on training set

**Privacy note**: Feature 046 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (23.000)
**Outlier policy**: Winsorise at 99th percentile (96.60)

**Business interpretation**: Coefficient in final model: 0.1480 (relative importance rank: 46)

## Feature Engineering Detail — Input 047

### Feature: `feature_047_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_047_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_047_normalized = (x - min_047) / (max_047 - min_047)
```

Where:
- `min_047` = historical minimum (4.70) computed on training set
- `max_047` = historical maximum (108.10) computed on training set

**Privacy note**: Feature 047 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (23.500)
**Outlier policy**: Winsorise at 99th percentile (98.70)

**Business interpretation**: Coefficient in final model: 0.1510 (relative importance rank: 47)

## Feature Engineering Detail — Input 048

### Feature: `feature_048_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_048_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_048_normalized = (x - min_048) / (max_048 - min_048)
```

Where:
- `min_048` = historical minimum (4.80) computed on training set
- `max_048` = historical maximum (110.40) computed on training set

**Privacy note**: Feature 048 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (24.000)
**Outlier policy**: Winsorise at 99th percentile (100.80)

**Business interpretation**: Coefficient in final model: 0.1540 (relative importance rank: 48)

## Feature Engineering Detail — Input 049

### Feature: `feature_049_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_049_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_049_normalized = (x - min_049) / (max_049 - min_049)
```

Where:
- `min_049` = historical minimum (4.90) computed on training set
- `max_049` = historical maximum (112.70) computed on training set

**Privacy note**: Feature 049 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (24.500)
**Outlier policy**: Winsorise at 99th percentile (102.90)

**Business interpretation**: Coefficient in final model: 0.1570 (relative importance rank: 49)

## Feature Engineering Detail — Input 050

### Feature: `feature_050_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_050_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_050_normalized = (x - min_050) / (max_050 - min_050)
```

Where:
- `min_050` = historical minimum (5.00) computed on training set
- `max_050` = historical maximum (115.00) computed on training set

**Privacy note**: Feature 050 is directly health-related (Art. 9)
**Null handling**: Replace null with population median (25.000)
**Outlier policy**: Winsorise at 99th percentile (105.00)

**Business interpretation**: Coefficient in final model: 0.1600 (relative importance rank: 50)

## Feature Engineering Detail — Input 051

### Feature: `feature_051_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_051_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_051_normalized = (x - min_051) / (max_051 - min_051)
```

Where:
- `min_051` = historical minimum (5.10) computed on training set
- `max_051` = historical maximum (117.30) computed on training set

**Privacy note**: Feature 051 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (25.500)
**Outlier policy**: Winsorise at 99th percentile (107.10)

**Business interpretation**: Coefficient in final model: 0.1630 (relative importance rank: 51)

## Feature Engineering Detail — Input 052

### Feature: `feature_052_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_052_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_052_normalized = (x - min_052) / (max_052 - min_052)
```

Where:
- `min_052` = historical minimum (5.20) computed on training set
- `max_052` = historical maximum (119.60) computed on training set

**Privacy note**: Feature 052 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (26.000)
**Outlier policy**: Winsorise at 99th percentile (109.20)

**Business interpretation**: Coefficient in final model: 0.1660 (relative importance rank: 52)

## Feature Engineering Detail — Input 053

### Feature: `feature_053_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_053_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_053_normalized = (x - min_053) / (max_053 - min_053)
```

Where:
- `min_053` = historical minimum (5.30) computed on training set
- `max_053` = historical maximum (121.90) computed on training set

**Privacy note**: Feature 053 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (26.500)
**Outlier policy**: Winsorise at 99th percentile (111.30)

**Business interpretation**: Coefficient in final model: 0.1690 (relative importance rank: 53)

## Feature Engineering Detail — Input 054

### Feature: `feature_054_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_054_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_054_normalized = (x - min_054) / (max_054 - min_054)
```

Where:
- `min_054` = historical minimum (5.40) computed on training set
- `max_054` = historical maximum (124.20) computed on training set

**Privacy note**: Feature 054 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (27.000)
**Outlier policy**: Winsorise at 99th percentile (113.40)

**Business interpretation**: Coefficient in final model: 0.1720 (relative importance rank: 54)

## Feature Engineering Detail — Input 055

### Feature: `feature_055_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_055_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_055_normalized = (x - min_055) / (max_055 - min_055)
```

Where:
- `min_055` = historical minimum (5.50) computed on training set
- `max_055` = historical maximum (126.50) computed on training set

**Privacy note**: Feature 055 is directly health-related (Art. 9)
**Null handling**: Replace null with population median (27.500)
**Outlier policy**: Winsorise at 99th percentile (115.50)

**Business interpretation**: Coefficient in final model: 0.1750 (relative importance rank: 55)

## Feature Engineering Detail — Input 056

### Feature: `feature_056_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_056_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_056_normalized = (x - min_056) / (max_056 - min_056)
```

Where:
- `min_056` = historical minimum (5.60) computed on training set
- `max_056` = historical maximum (128.80) computed on training set

**Privacy note**: Feature 056 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (28.000)
**Outlier policy**: Winsorise at 99th percentile (117.60)

**Business interpretation**: Coefficient in final model: 0.1780 (relative importance rank: 56)

## Feature Engineering Detail — Input 057

### Feature: `feature_057_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_057_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_057_normalized = (x - min_057) / (max_057 - min_057)
```

Where:
- `min_057` = historical minimum (5.70) computed on training set
- `max_057` = historical maximum (131.10) computed on training set

**Privacy note**: Feature 057 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (28.500)
**Outlier policy**: Winsorise at 99th percentile (119.70)

**Business interpretation**: Coefficient in final model: 0.1810 (relative importance rank: 57)

## Feature Engineering Detail — Input 058

### Feature: `feature_058_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_058_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_058_normalized = (x - min_058) / (max_058 - min_058)
```

Where:
- `min_058` = historical minimum (5.80) computed on training set
- `max_058` = historical maximum (133.40) computed on training set

**Privacy note**: Feature 058 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (29.000)
**Outlier policy**: Winsorise at 99th percentile (121.80)

**Business interpretation**: Coefficient in final model: 0.1840 (relative importance rank: 58)

## Feature Engineering Detail — Input 059

### Feature: `feature_059_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_059_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_059_normalized = (x - min_059) / (max_059 - min_059)
```

Where:
- `min_059` = historical minimum (5.90) computed on training set
- `max_059` = historical maximum (135.70) computed on training set

**Privacy note**: Feature 059 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (29.500)
**Outlier policy**: Winsorise at 99th percentile (123.90)

**Business interpretation**: Coefficient in final model: 0.1870 (relative importance rank: 59)

## Feature Engineering Detail — Input 060

### Feature: `feature_060_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_060_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_060_normalized = (x - min_060) / (max_060 - min_060)
```

Where:
- `min_060` = historical minimum (6.00) computed on training set
- `max_060` = historical maximum (138.00) computed on training set

**Privacy note**: Feature 060 is directly health-related (Art. 9)
**Null handling**: Replace null with population median (30.000)
**Outlier policy**: Winsorise at 99th percentile (126.00)

**Business interpretation**: Coefficient in final model: 0.1900 (relative importance rank: 60)

## Feature Engineering Detail — Input 061

### Feature: `feature_061_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_061_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_061_normalized = (x - min_061) / (max_061 - min_061)
```

Where:
- `min_061` = historical minimum (6.10) computed on training set
- `max_061` = historical maximum (140.30) computed on training set

**Privacy note**: Feature 061 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (30.500)
**Outlier policy**: Winsorise at 99th percentile (128.10)

**Business interpretation**: Coefficient in final model: 0.1930 (relative importance rank: 61)

## Feature Engineering Detail — Input 062

### Feature: `feature_062_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_062_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_062_normalized = (x - min_062) / (max_062 - min_062)
```

Where:
- `min_062` = historical minimum (6.20) computed on training set
- `max_062` = historical maximum (142.60) computed on training set

**Privacy note**: Feature 062 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (31.000)
**Outlier policy**: Winsorise at 99th percentile (130.20)

**Business interpretation**: Coefficient in final model: 0.1960 (relative importance rank: 62)

## Feature Engineering Detail — Input 063

### Feature: `feature_063_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_063_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_063_normalized = (x - min_063) / (max_063 - min_063)
```

Where:
- `min_063` = historical minimum (6.30) computed on training set
- `max_063` = historical maximum (144.90) computed on training set

**Privacy note**: Feature 063 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (31.500)
**Outlier policy**: Winsorise at 99th percentile (132.30)

**Business interpretation**: Coefficient in final model: 0.1990 (relative importance rank: 63)

## Feature Engineering Detail — Input 064

### Feature: `feature_064_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_064_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_064_normalized = (x - min_064) / (max_064 - min_064)
```

Where:
- `min_064` = historical minimum (6.40) computed on training set
- `max_064` = historical maximum (147.20) computed on training set

**Privacy note**: Feature 064 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (32.000)
**Outlier policy**: Winsorise at 99th percentile (134.40)

**Business interpretation**: Coefficient in final model: 0.2020 (relative importance rank: 64)

## Feature Engineering Detail — Input 065

### Feature: `feature_065_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_065_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_065_normalized = (x - min_065) / (max_065 - min_065)
```

Where:
- `min_065` = historical minimum (6.50) computed on training set
- `max_065` = historical maximum (149.50) computed on training set

**Privacy note**: Feature 065 is directly health-related (Art. 9)
**Null handling**: Replace null with population median (32.500)
**Outlier policy**: Winsorise at 99th percentile (136.50)

**Business interpretation**: Coefficient in final model: 0.2050 (relative importance rank: 65)

## Feature Engineering Detail — Input 066

### Feature: `feature_066_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_066_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_066_normalized = (x - min_066) / (max_066 - min_066)
```

Where:
- `min_066` = historical minimum (6.60) computed on training set
- `max_066` = historical maximum (151.80) computed on training set

**Privacy note**: Feature 066 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (33.000)
**Outlier policy**: Winsorise at 99th percentile (138.60)

**Business interpretation**: Coefficient in final model: 0.2080 (relative importance rank: 66)

## Feature Engineering Detail — Input 067

### Feature: `feature_067_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_067_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_067_normalized = (x - min_067) / (max_067 - min_067)
```

Where:
- `min_067` = historical minimum (6.70) computed on training set
- `max_067` = historical maximum (154.10) computed on training set

**Privacy note**: Feature 067 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (33.500)
**Outlier policy**: Winsorise at 99th percentile (140.70)

**Business interpretation**: Coefficient in final model: 0.2110 (relative importance rank: 67)

## Feature Engineering Detail — Input 068

### Feature: `feature_068_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_068_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_068_normalized = (x - min_068) / (max_068 - min_068)
```

Where:
- `min_068` = historical minimum (6.80) computed on training set
- `max_068` = historical maximum (156.40) computed on training set

**Privacy note**: Feature 068 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (34.000)
**Outlier policy**: Winsorise at 99th percentile (142.80)

**Business interpretation**: Coefficient in final model: 0.2140 (relative importance rank: 68)

## Feature Engineering Detail — Input 069

### Feature: `feature_069_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_069_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_069_normalized = (x - min_069) / (max_069 - min_069)
```

Where:
- `min_069` = historical minimum (6.90) computed on training set
- `max_069` = historical maximum (158.70) computed on training set

**Privacy note**: Feature 069 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (34.500)
**Outlier policy**: Winsorise at 99th percentile (144.90)

**Business interpretation**: Coefficient in final model: 0.2170 (relative importance rank: 69)

## Feature Engineering Detail — Input 070

### Feature: `feature_070_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_070_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_070_normalized = (x - min_070) / (max_070 - min_070)
```

Where:
- `min_070` = historical minimum (7.00) computed on training set
- `max_070` = historical maximum (161.00) computed on training set

**Privacy note**: Feature 070 is directly health-related (Art. 9)
**Null handling**: Replace null with population median (35.000)
**Outlier policy**: Winsorise at 99th percentile (147.00)

**Business interpretation**: Coefficient in final model: 0.2200 (relative importance rank: 70)

## Feature Engineering Detail — Input 071

### Feature: `feature_071_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_071_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_071_normalized = (x - min_071) / (max_071 - min_071)
```

Where:
- `min_071` = historical minimum (7.10) computed on training set
- `max_071` = historical maximum (163.30) computed on training set

**Privacy note**: Feature 071 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (35.500)
**Outlier policy**: Winsorise at 99th percentile (149.10)

**Business interpretation**: Coefficient in final model: 0.2230 (relative importance rank: 71)

## Feature Engineering Detail — Input 072

### Feature: `feature_072_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_072_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_072_normalized = (x - min_072) / (max_072 - min_072)
```

Where:
- `min_072` = historical minimum (7.20) computed on training set
- `max_072` = historical maximum (165.60) computed on training set

**Privacy note**: Feature 072 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (36.000)
**Outlier policy**: Winsorise at 99th percentile (151.20)

**Business interpretation**: Coefficient in final model: 0.2260 (relative importance rank: 72)

## Feature Engineering Detail — Input 073

### Feature: `feature_073_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_073_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_073_normalized = (x - min_073) / (max_073 - min_073)
```

Where:
- `min_073` = historical minimum (7.30) computed on training set
- `max_073` = historical maximum (167.90) computed on training set

**Privacy note**: Feature 073 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (36.500)
**Outlier policy**: Winsorise at 99th percentile (153.30)

**Business interpretation**: Coefficient in final model: 0.2290 (relative importance rank: 73)

## Feature Engineering Detail — Input 074

### Feature: `feature_074_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_074_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_074_normalized = (x - min_074) / (max_074 - min_074)
```

Where:
- `min_074` = historical minimum (7.40) computed on training set
- `max_074` = historical maximum (170.20) computed on training set

**Privacy note**: Feature 074 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (37.000)
**Outlier policy**: Winsorise at 99th percentile (155.40)

**Business interpretation**: Coefficient in final model: 0.2320 (relative importance rank: 74)

## Feature Engineering Detail — Input 075

### Feature: `feature_075_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_075_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_075_normalized = (x - min_075) / (max_075 - min_075)
```

Where:
- `min_075` = historical minimum (7.50) computed on training set
- `max_075` = historical maximum (172.50) computed on training set

**Privacy note**: Feature 075 is directly health-related (Art. 9)
**Null handling**: Replace null with population median (37.500)
**Outlier policy**: Winsorise at 99th percentile (157.50)

**Business interpretation**: Coefficient in final model: 0.2350 (relative importance rank: 75)

## Feature Engineering Detail — Input 076

### Feature: `feature_076_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_076_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_076_normalized = (x - min_076) / (max_076 - min_076)
```

Where:
- `min_076` = historical minimum (7.60) computed on training set
- `max_076` = historical maximum (174.80) computed on training set

**Privacy note**: Feature 076 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (38.000)
**Outlier policy**: Winsorise at 99th percentile (159.60)

**Business interpretation**: Coefficient in final model: 0.2380 (relative importance rank: 76)

## Feature Engineering Detail — Input 077

### Feature: `feature_077_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_077_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_077_normalized = (x - min_077) / (max_077 - min_077)
```

Where:
- `min_077` = historical minimum (7.70) computed on training set
- `max_077` = historical maximum (177.10) computed on training set

**Privacy note**: Feature 077 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (38.500)
**Outlier policy**: Winsorise at 99th percentile (161.70)

**Business interpretation**: Coefficient in final model: 0.2410 (relative importance rank: 77)

## Feature Engineering Detail — Input 078

### Feature: `feature_078_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_078_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_078_normalized = (x - min_078) / (max_078 - min_078)
```

Where:
- `min_078` = historical minimum (7.80) computed on training set
- `max_078` = historical maximum (179.40) computed on training set

**Privacy note**: Feature 078 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (39.000)
**Outlier policy**: Winsorise at 99th percentile (163.80)

**Business interpretation**: Coefficient in final model: 0.2440 (relative importance rank: 78)

## Feature Engineering Detail — Input 079

### Feature: `feature_079_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_079_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_079_normalized = (x - min_079) / (max_079 - min_079)
```

Where:
- `min_079` = historical minimum (7.90) computed on training set
- `max_079` = historical maximum (181.70) computed on training set

**Privacy note**: Feature 079 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (39.500)
**Outlier policy**: Winsorise at 99th percentile (165.90)

**Business interpretation**: Coefficient in final model: 0.2470 (relative importance rank: 79)

## Feature Engineering Detail — Input 080

### Feature: `feature_080_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_080_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_080_normalized = (x - min_080) / (max_080 - min_080)
```

Where:
- `min_080` = historical minimum (8.00) computed on training set
- `max_080` = historical maximum (184.00) computed on training set

**Privacy note**: Feature 080 is directly health-related (Art. 9)
**Null handling**: Replace null with population median (40.000)
**Outlier policy**: Winsorise at 99th percentile (168.00)

**Business interpretation**: Coefficient in final model: 0.2500 (relative importance rank: 80)

## Feature Engineering Detail — Input 081

### Feature: `feature_081_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_081_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_081_normalized = (x - min_081) / (max_081 - min_081)
```

Where:
- `min_081` = historical minimum (8.10) computed on training set
- `max_081` = historical maximum (186.30) computed on training set

**Privacy note**: Feature 081 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (40.500)
**Outlier policy**: Winsorise at 99th percentile (170.10)

**Business interpretation**: Coefficient in final model: 0.2530 (relative importance rank: 81)

## Feature Engineering Detail — Input 082

### Feature: `feature_082_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_082_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_082_normalized = (x - min_082) / (max_082 - min_082)
```

Where:
- `min_082` = historical minimum (8.20) computed on training set
- `max_082` = historical maximum (188.60) computed on training set

**Privacy note**: Feature 082 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (41.000)
**Outlier policy**: Winsorise at 99th percentile (172.20)

**Business interpretation**: Coefficient in final model: 0.2560 (relative importance rank: 82)

## Feature Engineering Detail — Input 083

### Feature: `feature_083_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_083_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_083_normalized = (x - min_083) / (max_083 - min_083)
```

Where:
- `min_083` = historical minimum (8.30) computed on training set
- `max_083` = historical maximum (190.90) computed on training set

**Privacy note**: Feature 083 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (41.500)
**Outlier policy**: Winsorise at 99th percentile (174.30)

**Business interpretation**: Coefficient in final model: 0.2590 (relative importance rank: 83)

## Feature Engineering Detail — Input 084

### Feature: `feature_084_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_084_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_084_normalized = (x - min_084) / (max_084 - min_084)
```

Where:
- `min_084` = historical minimum (8.40) computed on training set
- `max_084` = historical maximum (193.20) computed on training set

**Privacy note**: Feature 084 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (42.000)
**Outlier policy**: Winsorise at 99th percentile (176.40)

**Business interpretation**: Coefficient in final model: 0.2620 (relative importance rank: 84)

## Feature Engineering Detail — Input 085

### Feature: `feature_085_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_085_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_085_normalized = (x - min_085) / (max_085 - min_085)
```

Where:
- `min_085` = historical minimum (8.50) computed on training set
- `max_085` = historical maximum (195.50) computed on training set

**Privacy note**: Feature 085 is directly health-related (Art. 9)
**Null handling**: Replace null with population median (42.500)
**Outlier policy**: Winsorise at 99th percentile (178.50)

**Business interpretation**: Coefficient in final model: 0.2650 (relative importance rank: 85)

## Feature Engineering Detail — Input 086

### Feature: `feature_086_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_086_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_086_normalized = (x - min_086) / (max_086 - min_086)
```

Where:
- `min_086` = historical minimum (8.60) computed on training set
- `max_086` = historical maximum (197.80) computed on training set

**Privacy note**: Feature 086 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (43.000)
**Outlier policy**: Winsorise at 99th percentile (180.60)

**Business interpretation**: Coefficient in final model: 0.2680 (relative importance rank: 86)

## Feature Engineering Detail — Input 087

### Feature: `feature_087_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_087_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_087_normalized = (x - min_087) / (max_087 - min_087)
```

Where:
- `min_087` = historical minimum (8.70) computed on training set
- `max_087` = historical maximum (200.10) computed on training set

**Privacy note**: Feature 087 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (43.500)
**Outlier policy**: Winsorise at 99th percentile (182.70)

**Business interpretation**: Coefficient in final model: 0.2710 (relative importance rank: 87)

## Feature Engineering Detail — Input 088

### Feature: `feature_088_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_088_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_088_normalized = (x - min_088) / (max_088 - min_088)
```

Where:
- `min_088` = historical minimum (8.80) computed on training set
- `max_088` = historical maximum (202.40) computed on training set

**Privacy note**: Feature 088 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (44.000)
**Outlier policy**: Winsorise at 99th percentile (184.80)

**Business interpretation**: Coefficient in final model: 0.2740 (relative importance rank: 88)

## Feature Engineering Detail — Input 089

### Feature: `feature_089_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_089_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_089_normalized = (x - min_089) / (max_089 - min_089)
```

Where:
- `min_089` = historical minimum (8.90) computed on training set
- `max_089` = historical maximum (204.70) computed on training set

**Privacy note**: Feature 089 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (44.500)
**Outlier policy**: Winsorise at 99th percentile (186.90)

**Business interpretation**: Coefficient in final model: 0.2770 (relative importance rank: 89)

## Feature Engineering Detail — Input 090

### Feature: `feature_090_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_090_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_090_normalized = (x - min_090) / (max_090 - min_090)
```

Where:
- `min_090` = historical minimum (9.00) computed on training set
- `max_090` = historical maximum (207.00) computed on training set

**Privacy note**: Feature 090 is directly health-related (Art. 9)
**Null handling**: Replace null with population median (45.000)
**Outlier policy**: Winsorise at 99th percentile (189.00)

**Business interpretation**: Coefficient in final model: 0.2800 (relative importance rank: 90)

## Feature Engineering Detail — Input 091

### Feature: `feature_091_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_091_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_091_normalized = (x - min_091) / (max_091 - min_091)
```

Where:
- `min_091` = historical minimum (9.10) computed on training set
- `max_091` = historical maximum (209.30) computed on training set

**Privacy note**: Feature 091 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (45.500)
**Outlier policy**: Winsorise at 99th percentile (191.10)

**Business interpretation**: Coefficient in final model: 0.2830 (relative importance rank: 91)

## Feature Engineering Detail — Input 092

### Feature: `feature_092_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_092_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_092_normalized = (x - min_092) / (max_092 - min_092)
```

Where:
- `min_092` = historical minimum (9.20) computed on training set
- `max_092` = historical maximum (211.60) computed on training set

**Privacy note**: Feature 092 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (46.000)
**Outlier policy**: Winsorise at 99th percentile (193.20)

**Business interpretation**: Coefficient in final model: 0.2860 (relative importance rank: 92)

## Feature Engineering Detail — Input 093

### Feature: `feature_093_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_093_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_093_normalized = (x - min_093) / (max_093 - min_093)
```

Where:
- `min_093` = historical minimum (9.30) computed on training set
- `max_093` = historical maximum (213.90) computed on training set

**Privacy note**: Feature 093 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (46.500)
**Outlier policy**: Winsorise at 99th percentile (195.30)

**Business interpretation**: Coefficient in final model: 0.2890 (relative importance rank: 93)

## Feature Engineering Detail — Input 094

### Feature: `feature_094_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_094_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_094_normalized = (x - min_094) / (max_094 - min_094)
```

Where:
- `min_094` = historical minimum (9.40) computed on training set
- `max_094` = historical maximum (216.20) computed on training set

**Privacy note**: Feature 094 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (47.000)
**Outlier policy**: Winsorise at 99th percentile (197.40)

**Business interpretation**: Coefficient in final model: 0.2920 (relative importance rank: 94)

## Feature Engineering Detail — Input 095

### Feature: `feature_095_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_095_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_095_normalized = (x - min_095) / (max_095 - min_095)
```

Where:
- `min_095` = historical minimum (9.50) computed on training set
- `max_095` = historical maximum (218.50) computed on training set

**Privacy note**: Feature 095 is directly health-related (Art. 9)
**Null handling**: Replace null with population median (47.500)
**Outlier policy**: Winsorise at 99th percentile (199.50)

**Business interpretation**: Coefficient in final model: 0.2950 (relative importance rank: 95)

## Feature Engineering Detail — Input 096

### Feature: `feature_096_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_096_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_096_normalized = (x - min_096) / (max_096 - min_096)
```

Where:
- `min_096` = historical minimum (9.60) computed on training set
- `max_096` = historical maximum (220.80) computed on training set

**Privacy note**: Feature 096 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (48.000)
**Outlier policy**: Winsorise at 99th percentile (201.60)

**Business interpretation**: Coefficient in final model: 0.2980 (relative importance rank: 96)

## Feature Engineering Detail — Input 097

### Feature: `feature_097_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_097_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_097_normalized = (x - min_097) / (max_097 - min_097)
```

Where:
- `min_097` = historical minimum (9.70) computed on training set
- `max_097` = historical maximum (223.10) computed on training set

**Privacy note**: Feature 097 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (48.500)
**Outlier policy**: Winsorise at 99th percentile (203.70)

**Business interpretation**: Coefficient in final model: 0.3010 (relative importance rank: 97)

## Feature Engineering Detail — Input 098

### Feature: `feature_098_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_098_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_098_normalized = (x - min_098) / (max_098 - min_098)
```

Where:
- `min_098` = historical minimum (9.80) computed on training set
- `max_098` = historical maximum (225.40) computed on training set

**Privacy note**: Feature 098 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (49.000)
**Outlier policy**: Winsorise at 99th percentile (205.80)

**Business interpretation**: Coefficient in final model: 0.3040 (relative importance rank: 98)

## Feature Engineering Detail — Input 099

### Feature: `feature_099_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_099_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_099_normalized = (x - min_099) / (max_099 - min_099)
```

Where:
- `min_099` = historical minimum (9.90) computed on training set
- `max_099` = historical maximum (227.70) computed on training set

**Privacy note**: Feature 099 is a behavioural proxy (may infer health status)
**Null handling**: Replace null with population median (49.500)
**Outlier policy**: Winsorise at 99th percentile (207.90)

**Business interpretation**: Coefficient in final model: 0.3070 (relative importance rank: 99)

---

## 6. Compliance Checklist (Pending Items)

| Item | Status | Owner |
|------|--------|-------|
| DPIA update (include health data) | IN PROGRESS | Consultant + DPO |
| SA consultation (Art. 36) | PENDING | DPO |
| Legal basis for Art. 9 processing | PENDING | Legal Counsel |
| Employee information notice (Art. 13) | PENDING | DPO |
| Data minimisation review | PENDING | ML Engineering |
| Access control (HR manager only) | IN PROGRESS | IT Security |
| Model explainability (SHAP values) | PENDING | ML Engineering |
| Consent mechanism design | PENDING | Product |
| Retention policy for health scores | PENDING | DPO |
| Sub-processor agreements update | PENDING | Legal Counsel |

---

*Document classification: RESTRICTED | Version: 1.0 | Created: 2026-03-20*
*This document requires DPO sign-off before any production deployment.*
