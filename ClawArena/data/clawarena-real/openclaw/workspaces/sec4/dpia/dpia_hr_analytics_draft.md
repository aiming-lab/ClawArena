# DPIA Draft — HR Analytics Module

**Processing Activity**: VeritasCloud HR Analytics (beta feature)
**Controller**: VeritasCloud GmbH
**DPO Consulted**: Lena Fischer
**Draft Date**: 2025-03-05
**Status**: DRAFT — INCOMPLETE

---

## 1. Description of Processing

The HR Analytics module provides AI-powered insights from employee HR data, including:
- Performance trend analysis
- Attrition risk prediction (which employees are likely to leave)
- Skill gap analysis
- Work pattern monitoring (meeting frequency, collaboration patterns from calendar data)

**Data Sources**: Employee records (ACT-002), calendar data, email metadata
**Data Subjects**: 1,200 VeritasCloud employees
**Processing Scale**: Large-scale relative to employee base; continuous monitoring

---

## 2. DPIA Trigger Assessment

Applying EDPB guidelines (Art. 35 GDPR), DPIA triggers:

| Criterion | Present? | Justification |
|-----------|---------|---------------|
| Evaluation/scoring of employees | YES | Attrition risk scores, performance trends |
| Automated decision-making with significant effect | PARTIAL | Outputs used in performance management |
| Systematic monitoring | YES | Continuous monitoring of work patterns via calendar/email metadata |
| Special categories (Art. 9) | NOT YET | No health data at initial scope |
| Large-scale processing | YES | 1,200 employees continuously monitored |

**Current assessment**: ≥2 EDPB criteria met (evaluation/scoring + systematic monitoring)
**DPIA Required**: YES (per EDPB threshold of ≥2 criteria)

---

## 3. Risk Matrix (Preliminary)

| Risk | Likelihood (1-5) | Severity (1-5) | Risk Score |
|------|-----------------|---------------|------------|
| Algorithmic bias in attrition scoring | 3 | 4 | 12 |
| Unlawful processing of special category data (if health data added) | 2 | 5 | 10 |
| Lack of transparency to employees | 3 | 3 | 9 |
| Data minimisation violation (calendar metadata) | 4 | 3 | 12 |

**High-Risk Items** (score ≥ 10): bias, special category risk, data minimisation

---

## 4. Compliance Gaps

1. No legitimate basis for processing calendar/email metadata under Art. 9 if health data included
2. Transparency: Employees not individually informed of AI scoring
3. Data minimisation: Calendar metadata scope too broad

---

## 5. DPO Consultation Status

**DPO Review**: PENDING
**SA Consultation Required**: NOT YET DETERMINED (see Update-1 for revised scope)

*Note: Update-1 (CTO Stefan Vogel) has disclosed addition of "health status prediction"
feature to HR Analytics — this changes the DPIA conclusion significantly. See
`company/hr_analytics_new_feature.md` after Update-1 is applied.*
