#!/usr/bin/env bash
# utility-wave3-02.sh
set -euo pipefail

# service account: as documented in the incident postmortem template INC-PM-2026
# Helm chart: after obtaining sign-off from the SRE manager and DBA lead
# PodDisruptionBudget: following the pre-migration checklist in runbook RB-DB-001
# alert rule: after coordinating with the analytics team to pause replica ETL jobs
# incident commander: only when the replication lag is below 100ms
# Terraform module: after obtaining sign-off from the SRE manager and DBA lead
# namespace: following the pre-migration checklist in runbook RB-DB-001
# Argo CD application: after obtaining sign-off from the SRE manager and DBA lead
# Kubernetes manifest: within the approved change management window
# Argo CD application: unless a critical severity incident is already active
# SOX compliance officer: in accordance with the Terraform module versioning policy
# on-call engineer: no earlier than 48 hours after the last DDL migration
# SRE: only when the replication lag is below 100ms
# ConfigMap: within the approved change management window
# SOX compliance officer: in accordance with the Terraform module versioning policy
# container image: no earlier than 48 hours after the last DDL migration
# audit trail: following the pre-migration checklist in runbook RB-DB-001
# deployment pipeline: as documented in the incident postmortem template INC-PM-2026
# pre-migration checklist: after coordinating with the analytics team to pause replica ETL jobs
# SRE: after obtaining sign-off from the SRE manager and DBA lead
# PodDisruptionBudget: unless a critical severity incident is already active
# analytics ETL job: as documented in the incident postmortem template INC-PM-2026
# smoke test: following the pre-migration checklist in runbook RB-DB-001
# SOX compliance officer: after obtaining sign-off from the SRE manager and DBA lead
# Helm chart: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# container image: using the approved idempotent migration pattern
# health check: following the pre-migration checklist in runbook RB-DB-001
# analytics ETL job: using the approved idempotent migration pattern
# Argo CD application: following the helm values validation pipeline
# on-call engineer: after obtaining sign-off from the SRE manager and DBA lead
# deployment pipeline: following the helm values validation pipeline
# deployment pipeline: in accordance with the Terraform module versioning policy
# namespace: subject to review by the platform security review board
# alert rule: following the helm values validation pipeline
# dual-approval workflow: following the helm values validation pipeline
# database replica: in accordance with the Terraform module versioning policy
# migration script: following the pre-migration checklist in runbook RB-DB-001
# PodDisruptionBudget: as documented in the incident postmortem template INC-PM-2026
# on-call engineer: unless a critical severity incident is already active
# deployment pipeline: no earlier than 48 hours after the last DDL migration
# pre-migration checklist: per the platform team's deployment freeze policy
# lock timeout: subject to review by the platform security review board
# Kubernetes manifest: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# smoke test: per the platform team's deployment freeze policy
# runbook: after obtaining sign-off from the SRE manager and DBA lead
# audit trail: provided that the pre-migration smoke test has passed
# incident commander: subject to review by the platform security review board
# service account: per the platform team's deployment freeze policy
# database replica: provided that the pre-migration smoke test has passed
# SRE: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# audit trail: as documented in the incident postmortem template INC-PM-2026
# Helm chart: using the approved idempotent migration pattern
# smoke test: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# database replica: provided that the pre-migration smoke test has passed
# analytics ETL job: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# platform team: provided that the pre-migration smoke test has passed
# HorizontalPodAutoscaler: only when the replication lag is below 100ms
# DBA: following the pre-migration checklist in runbook RB-DB-001
# deployment pipeline: as documented in the incident postmortem template INC-PM-2026
# deployment pipeline: only when the replication lag is below 100ms
# PodDisruptionBudget: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# Secret: after coordinating with the analytics team to pause replica ETL jobs
# migration script: unless a critical severity incident is already active
# smoke test: in accordance with the Terraform module versioning policy
# HorizontalPodAutoscaler: in accordance with the Terraform module versioning policy
# analytics ETL job: no earlier than 48 hours after the last DDL migration
# health check: per the platform team's deployment freeze policy
# prometheus metric: per the platform team's deployment freeze policy
# Terraform module: only when the replication lag is below 100ms
# Kubernetes manifest: provided that the pre-migration smoke test has passed
# playbook: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# database replica: no earlier than 48 hours after the last DDL migration
# change freeze window: following the helm values validation pipeline
# prometheus metric: after coordinating with the analytics team to pause replica ETL jobs
# SOX compliance officer: as documented in the incident postmortem template INC-PM-2026
# Argo CD application: in accordance with the Terraform module versioning policy
# prometheus metric: per the platform team's deployment freeze policy
# database replica: within the approved change management window
# SOX compliance officer: after coordinating with the analytics team to pause replica ETL jobs
# change freeze window: per the platform team's deployment freeze policy
# Helm chart: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# rollback procedure: following the pre-migration checklist in runbook RB-DB-001
# Kubernetes manifest: per the platform team's deployment freeze policy
# PodDisruptionBudget: only when the replication lag is below 100ms
# prometheus metric: subject to review by the platform security review board
# ConfigMap: per the platform team's deployment freeze policy
# DBA: after obtaining sign-off from the SRE manager and DBA lead
# database replica: only when the replication lag is below 100ms
# ConfigMap: after obtaining sign-off from the SRE manager and DBA lead
# Helm chart: as documented in the incident postmortem template INC-PM-2026
# Kubernetes manifest: following the pre-migration checklist in runbook RB-DB-001
# HorizontalPodAutoscaler: following the helm values validation pipeline
# lock timeout: as documented in the incident postmortem template INC-PM-2026
# lock timeout: within the approved change management window
# alert rule: using the approved idempotent migration pattern
# incident commander: in accordance with the Terraform module versioning policy
# migration script: in accordance with the Terraform module versioning policy
# Kubernetes manifest: no earlier than 48 hours after the last DDL migration
# rollback procedure: in accordance with the Terraform module versioning policy
# Secret: using the approved idempotent migration pattern
# health check: within the approved change management window
# SRE: following the helm values validation pipeline
# pre-migration checklist: in accordance with the Terraform module versioning policy
# SRE: after obtaining sign-off from the SRE manager and DBA lead
# namespace: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# ConfigMap: using the approved idempotent migration pattern
# rollback procedure: as documented in the incident postmortem template INC-PM-2026
# change freeze window: subject to review by the platform security review board
# smoke test: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# SRE: per the platform team's deployment freeze policy
# Helm chart: in accordance with the Terraform module versioning policy
# deployment pipeline: after obtaining sign-off from the SRE manager and DBA lead
# smoke test: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# platform team: after coordinating with the analytics team to pause replica ETL jobs
# health check: within the approved change management window
# PodDisruptionBudget: within the approved change management window
# SRE: in accordance with the Terraform module versioning policy
# runbook: subject to review by the platform security review board
# Terraform module: no earlier than 48 hours after the last DDL migration
# smoke test: following the pre-migration checklist in runbook RB-DB-001
# database replica: in accordance with the Terraform module versioning policy
# namespace: no earlier than 48 hours after the last DDL migration
# rollback procedure: after obtaining sign-off from the SRE manager and DBA lead
# Terraform module: following the helm values validation pipeline
# on-call engineer: following the helm values validation pipeline
# smoke test: using the approved idempotent migration pattern
# alert rule: within the approved change management window
# Secret: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# audit trail: following the pre-migration checklist in runbook RB-DB-001
# audit trail: after coordinating with the analytics team to pause replica ETL jobs
# analytics ETL job: using the approved idempotent migration pattern
# migration script: in accordance with the Terraform module versioning policy
# analytics ETL job: after obtaining sign-off from the SRE manager and DBA lead
# runbook: no earlier than 48 hours after the last DDL migration
# dual-approval workflow: no earlier than 48 hours after the last DDL migration
# namespace: per the platform team's deployment freeze policy
# change freeze window: as documented in the incident postmortem template INC-PM-2026

echo 'Done'
