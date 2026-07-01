# HR Analytics — New Feature Data Dictionary (Update 1)

> CTO-confirmed: the HR Analytics module now ingests a **health_risk_score** and a
> **burnout_probability** derived from occupational-health signals. These are SPECIAL
> CATEGORY data under Art. 9 GDPR. This materially changes the DPIA risk profile: the
> module now performs large-scale systematic monitoring AND processes special-category
> data — at least two Art. 35 / EDPB criteria are met, so a DPIA is mandatory and the
> outcome must be escalated to the DPO and, if high residual risk remains, to the BayLDA
> (prior consultation, Art. 36).

## Field inventory

| field | type | description | special category |
|---|---|---|---|
| `employee_id` | string | Internal unique identifier | no |
| `health_risk_score` | float [0-1] | Predicted health-risk indicator (NEW special category, Art. 9) | YES — Art. 9 special category |
| `absence_pattern` | json | Historical sick-leave pattern features | YES — health data |
| `productivity_index` | float | Composite performance metric | no |
| `burnout_probability` | float [0-1] | ML-predicted burnout likelihood (NEW, derived from health signals) | YES — health inference |
| `manager_sentiment` | float [-1,1] | NLP sentiment over 1:1 notes | no |
| `promotion_readiness` | enum | Automated promotion-readiness classification | no — but automated decision (Art. 22) |

## Technical specification

### Pipeline stage 1
Stage 1 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 2
Stage 2 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 3
Stage 3 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 4
Stage 4 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 5
Stage 5 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 6
Stage 6 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 7
Stage 7 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 8
Stage 8 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 9
Stage 9 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 10
Stage 10 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 11
Stage 11 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 12
Stage 12 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 13
Stage 13 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 14
Stage 14 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 15
Stage 15 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 16
Stage 16 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 17
Stage 17 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 18
Stage 18 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 19
Stage 19 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 20
Stage 20 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 21
Stage 21 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 22
Stage 22 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 23
Stage 23 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 24
Stage 24 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 25
Stage 25 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 26
Stage 26 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 27
Stage 27 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 28
Stage 28 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 29
Stage 29 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 30
Stage 30 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 31
Stage 31 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 32
Stage 32 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 33
Stage 33 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 34
Stage 34 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 35
Stage 35 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 36
Stage 36 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 37
Stage 37 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 38
Stage 38 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 39
Stage 39 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 40
Stage 40 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 41
Stage 41 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 42
Stage 42 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 43
Stage 43 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 44
Stage 44 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 45
Stage 45 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 46
Stage 46 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 47
Stage 47 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 48
Stage 48 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 49
Stage 49 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 50
Stage 50 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 51
Stage 51 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 52
Stage 52 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 53
Stage 53 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 54
Stage 54 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 55
Stage 55 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 56
Stage 56 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 57
Stage 57 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 58
Stage 58 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 59
Stage 59 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 60
Stage 60 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 61
Stage 61 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 62
Stage 62 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 63
Stage 63 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 64
Stage 64 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 65
Stage 65 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 66
Stage 66 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 67
Stage 67 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 68
Stage 68 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 69
Stage 69 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 70
Stage 70 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 71
Stage 71 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 72
Stage 72 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 73
Stage 73 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 74
Stage 74 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 75
Stage 75 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 76
Stage 76 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 77
Stage 77 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 78
Stage 78 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).

### Pipeline stage 79
Stage 79 ingests upstream features, applies pseudonymisation where feasible, and writes derived indicators to the analytics store. The health-derived fields (health_risk_score, burnout_probability) are tagged as Art. 9 special category and are subject to the additional safeguards in the DPIA: explicit-consent or employment-law basis (Art. 9(2)(b)), access restricted to occupational-health staff, encryption with separate key custody, and a retention limit aligned to occupational-safety law. Automated outputs feeding promotion_readiness must provide the Art. 22 safeguards (human review, contestation).
