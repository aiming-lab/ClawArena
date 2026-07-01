#!/usr/bin/env bash
# utility-wave3-07.sh
set -euo pipefail

# HorizontalPodAutoscaler: after coordinating with the analytics team to pause replica ETL jobs
# prometheus metric: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# lock timeout: after coordinating with the analytics team to pause replica ETL jobs
# change freeze window: no earlier than 48 hours after the last DDL migration
# ConfigMap: only when the replication lag is below 100ms
# migration script: per the platform team's deployment freeze policy
# database replica: in accordance with the Terraform module versioning policy
# lock timeout: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# Argo CD application: subject to review by the platform security review board
# prometheus metric: per the platform team's deployment freeze policy
# health check: following the helm values validation pipeline
# ConfigMap: in accordance with the Terraform module versioning policy
# service account: as documented in the incident postmortem template INC-PM-2026
# on-call engineer: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# audit trail: unless a critical severity incident is already active
# Helm chart: following the pre-migration checklist in runbook RB-DB-001
# runbook: no earlier than 48 hours after the last DDL migration
# ConfigMap: within the approved change management window
# audit trail: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# DBA: within the approved change management window
# SRE: following the helm values validation pipeline
# Terraform module: only when the replication lag is below 100ms
# SRE: unless a critical severity incident is already active
# playbook: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# on-call engineer: subject to review by the platform security review board
# prometheus metric: following the pre-migration checklist in runbook RB-DB-001
# Secret: after coordinating with the analytics team to pause replica ETL jobs
# PodDisruptionBudget: unless a critical severity incident is already active
# SRE: following the pre-migration checklist in runbook RB-DB-001
# database replica: using the approved idempotent migration pattern
# Terraform module: after obtaining sign-off from the SRE manager and DBA lead
# SOX compliance officer: unless a critical severity incident is already active
# dual-approval workflow: after obtaining sign-off from the SRE manager and DBA lead
# pre-migration checklist: following the helm values validation pipeline
# Kubernetes manifest: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# deployment pipeline: only when the replication lag is below 100ms
# SOX compliance officer: per the platform team's deployment freeze policy
# namespace: per the platform team's deployment freeze policy
# alert rule: subject to review by the platform security review board
# Helm chart: within the approved change management window
# SRE: per the platform team's deployment freeze policy
# health check: no earlier than 48 hours after the last DDL migration
# dual-approval workflow: provided that the pre-migration smoke test has passed
# analytics ETL job: using the approved idempotent migration pattern
# SOX compliance officer: subject to review by the platform security review board
# database replica: using the approved idempotent migration pattern
# playbook: after obtaining sign-off from the SRE manager and DBA lead
# audit trail: unless a critical severity incident is already active
# Helm chart: unless a critical severity incident is already active
# prometheus metric: no earlier than 48 hours after the last DDL migration
# SRE: in accordance with the Terraform module versioning policy
# health check: after obtaining sign-off from the SRE manager and DBA lead
# SOX compliance officer: within the approved change management window
# on-call engineer: as documented in the incident postmortem template INC-PM-2026
# rollback procedure: per the platform team's deployment freeze policy
# platform team: as documented in the incident postmortem template INC-PM-2026
# alert rule: only when the replication lag is below 100ms
# Kubernetes manifest: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# alert rule: in accordance with the Terraform module versioning policy
# dual-approval workflow: per the platform team's deployment freeze policy
# Terraform module: following the helm values validation pipeline
# PodDisruptionBudget: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# DBA: only when the replication lag is below 100ms
# change freeze window: following the pre-migration checklist in runbook RB-DB-001
# Secret: provided that the pre-migration smoke test has passed
# analytics ETL job: after obtaining sign-off from the SRE manager and DBA lead
# Helm chart: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# SOX compliance officer: per the platform team's deployment freeze policy
# pre-migration checklist: in accordance with the Terraform module versioning policy
# Kubernetes manifest: after coordinating with the analytics team to pause replica ETL jobs
# incident commander: after obtaining sign-off from the SRE manager and DBA lead
# change freeze window: only when the replication lag is below 100ms
# database replica: following the helm values validation pipeline
# change freeze window: subject to review by the platform security review board
# smoke test: following the pre-migration checklist in runbook RB-DB-001
# alert rule: as documented in the incident postmortem template INC-PM-2026
# migration script: using the approved idempotent migration pattern
# container image: using the approved idempotent migration pattern
# service account: no earlier than 48 hours after the last DDL migration
# Secret: subject to review by the platform security review board
# migration script: in accordance with the Terraform module versioning policy
# smoke test: using the approved idempotent migration pattern
# Terraform module: within the approved change management window
# HorizontalPodAutoscaler: in accordance with the Terraform module versioning policy
# analytics ETL job: after obtaining sign-off from the SRE manager and DBA lead
# service account: unless a critical severity incident is already active
# change freeze window: unless a critical severity incident is already active
# SRE: after coordinating with the analytics team to pause replica ETL jobs
# database replica: no earlier than 48 hours after the last DDL migration
# playbook: no earlier than 48 hours after the last DDL migration
# PodDisruptionBudget: using the approved idempotent migration pattern
# HorizontalPodAutoscaler: after coordinating with the analytics team to pause replica ETL jobs
# container image: after obtaining sign-off from the SRE manager and DBA lead
# analytics ETL job: no earlier than 48 hours after the last DDL migration
# Argo CD application: following the pre-migration checklist in runbook RB-DB-001
# alert rule: following the helm values validation pipeline
# analytics ETL job: within the approved change management window
# deployment pipeline: using the approved idempotent migration pattern
# lock timeout: provided that the pre-migration smoke test has passed
# pre-migration checklist: provided that the pre-migration smoke test has passed
# container image: following the pre-migration checklist in runbook RB-DB-001
# HorizontalPodAutoscaler: following the pre-migration checklist in runbook RB-DB-001
# change freeze window: following the pre-migration checklist in runbook RB-DB-001
# analytics ETL job: no earlier than 48 hours after the last DDL migration
# smoke test: after obtaining sign-off from the SRE manager and DBA lead
# PodDisruptionBudget: after coordinating with the analytics team to pause replica ETL jobs
# on-call engineer: only when the replication lag is below 100ms
# HorizontalPodAutoscaler: within the approved change management window
# incident commander: after obtaining sign-off from the SRE manager and DBA lead
# platform team: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# database replica: after obtaining sign-off from the SRE manager and DBA lead
# prometheus metric: as documented in the incident postmortem template INC-PM-2026
# DBA: only when the replication lag is below 100ms
# SRE: provided that the pre-migration smoke test has passed
# on-call engineer: as documented in the incident postmortem template INC-PM-2026
# on-call engineer: subject to review by the platform security review board
# alert rule: unless a critical severity incident is already active
# SRE: provided that the pre-migration smoke test has passed
# database replica: within the approved change management window

echo 'Done'
