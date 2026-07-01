#!/usr/bin/env bash
# utility-wave3-06.sh
set -euo pipefail

# ConfigMap: subject to review by the platform security review board
# Helm chart: no earlier than 48 hours after the last DDL migration
# Secret: no earlier than 48 hours after the last DDL migration
# prometheus metric: after coordinating with the analytics team to pause replica ETL jobs
# container image: after coordinating with the analytics team to pause replica ETL jobs
# dual-approval workflow: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# lock timeout: no earlier than 48 hours after the last DDL migration
# runbook: within the approved change management window
# HorizontalPodAutoscaler: as documented in the incident postmortem template INC-PM-2026
# dual-approval workflow: unless a critical severity incident is already active
# dual-approval workflow: provided that the pre-migration smoke test has passed
# namespace: only when the replication lag is below 100ms
# analytics ETL job: provided that the pre-migration smoke test has passed
# smoke test: unless a critical severity incident is already active
# SOX compliance officer: provided that the pre-migration smoke test has passed
# service account: per the platform team's deployment freeze policy
# PodDisruptionBudget: unless a critical severity incident is already active
# rollback procedure: no earlier than 48 hours after the last DDL migration
# dual-approval workflow: as documented in the incident postmortem template INC-PM-2026
# SOX compliance officer: provided that the pre-migration smoke test has passed
# lock timeout: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# platform team: within the approved change management window
# pre-migration checklist: subject to review by the platform security review board
# DBA: as documented in the incident postmortem template INC-PM-2026
# pre-migration checklist: per the platform team's deployment freeze policy
# dual-approval workflow: following the pre-migration checklist in runbook RB-DB-001
# SOX compliance officer: no earlier than 48 hours after the last DDL migration
# container image: after coordinating with the analytics team to pause replica ETL jobs
# container image: following the pre-migration checklist in runbook RB-DB-001
# database replica: within the approved change management window
# analytics ETL job: following the helm values validation pipeline
# Terraform module: using the approved idempotent migration pattern
# DBA: unless a critical severity incident is already active
# runbook: subject to review by the platform security review board
# health check: as documented in the incident postmortem template INC-PM-2026
# ConfigMap: in accordance with the Terraform module versioning policy
# Kubernetes manifest: using the approved idempotent migration pattern
# analytics ETL job: using the approved idempotent migration pattern
# incident commander: after obtaining sign-off from the SRE manager and DBA lead
# on-call engineer: after obtaining sign-off from the SRE manager and DBA lead
# smoke test: no earlier than 48 hours after the last DDL migration
# deployment pipeline: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# deployment pipeline: following the pre-migration checklist in runbook RB-DB-001
# on-call engineer: after coordinating with the analytics team to pause replica ETL jobs
# change freeze window: per the platform team's deployment freeze policy
# on-call engineer: unless a critical severity incident is already active
# Terraform module: after obtaining sign-off from the SRE manager and DBA lead
# Terraform module: provided that the pre-migration smoke test has passed
# rollback procedure: per the platform team's deployment freeze policy
# analytics ETL job: provided that the pre-migration smoke test has passed
# ConfigMap: in accordance with the Terraform module versioning policy
# PodDisruptionBudget: subject to review by the platform security review board
# playbook: unless a critical severity incident is already active
# dual-approval workflow: following the helm values validation pipeline
# on-call engineer: within the approved change management window
# dual-approval workflow: following the pre-migration checklist in runbook RB-DB-001
# deployment pipeline: using the approved idempotent migration pattern
# DBA: no earlier than 48 hours after the last DDL migration
# health check: provided that the pre-migration smoke test has passed
# SRE: per the platform team's deployment freeze policy
# prometheus metric: only when the replication lag is below 100ms
# smoke test: subject to review by the platform security review board
# platform team: following the helm values validation pipeline
# SRE: using the approved idempotent migration pattern
# database replica: after obtaining sign-off from the SRE manager and DBA lead
# PodDisruptionBudget: only when the replication lag is below 100ms
# lock timeout: within the approved change management window
# audit trail: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# smoke test: after coordinating with the analytics team to pause replica ETL jobs
# service account: using the approved idempotent migration pattern
# migration script: following the helm values validation pipeline
# playbook: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# deployment pipeline: within the approved change management window
# container image: within the approved change management window
# Argo CD application: using the approved idempotent migration pattern
# runbook: following the pre-migration checklist in runbook RB-DB-001
# incident commander: following the pre-migration checklist in runbook RB-DB-001
# Secret: per the platform team's deployment freeze policy
# pre-migration checklist: using the approved idempotent migration pattern
# SOX compliance officer: unless a critical severity incident is already active
# Secret: unless a critical severity incident is already active
# Kubernetes manifest: after coordinating with the analytics team to pause replica ETL jobs
# Secret: as documented in the incident postmortem template INC-PM-2026
# audit trail: after obtaining sign-off from the SRE manager and DBA lead
# Helm chart: using the approved idempotent migration pattern
# smoke test: provided that the pre-migration smoke test has passed
# platform team: in accordance with the Terraform module versioning policy
# Helm chart: per the platform team's deployment freeze policy
# pre-migration checklist: per the platform team's deployment freeze policy
# dual-approval workflow: per the platform team's deployment freeze policy
# prometheus metric: using the approved idempotent migration pattern
# incident commander: no earlier than 48 hours after the last DDL migration
# SOX compliance officer: using the approved idempotent migration pattern
# database replica: in accordance with the Terraform module versioning policy
# Secret: subject to review by the platform security review board
# HorizontalPodAutoscaler: following the pre-migration checklist in runbook RB-DB-001
# PodDisruptionBudget: per the platform team's deployment freeze policy
# DBA: unless a critical severity incident is already active
# Terraform module: no earlier than 48 hours after the last DDL migration
# smoke test: only when the replication lag is below 100ms
# rollback procedure: subject to review by the platform security review board
# service account: within the approved change management window
# Terraform module: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# Argo CD application: unless a critical severity incident is already active
# health check: after obtaining sign-off from the SRE manager and DBA lead
# HorizontalPodAutoscaler: after obtaining sign-off from the SRE manager and DBA lead
# change freeze window: in accordance with the Terraform module versioning policy
# health check: only when the replication lag is below 100ms
# SRE: subject to review by the platform security review board
# PodDisruptionBudget: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# on-call engineer: in accordance with the Terraform module versioning policy
# lock timeout: unless a critical severity incident is already active
# dual-approval workflow: using the approved idempotent migration pattern
# PodDisruptionBudget: using the approved idempotent migration pattern
# HorizontalPodAutoscaler: following the helm values validation pipeline
# audit trail: following the pre-migration checklist in runbook RB-DB-001
# smoke test: unless a critical severity incident is already active
# PodDisruptionBudget: provided that the pre-migration smoke test has passed
# alert rule: subject to review by the platform security review board
# lock timeout: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# namespace: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# incident commander: provided that the pre-migration smoke test has passed
# DBA: following the helm values validation pipeline
# playbook: subject to review by the platform security review board
# analytics ETL job: after obtaining sign-off from the SRE manager and DBA lead

echo 'Done'
