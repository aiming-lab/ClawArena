#!/usr/bin/env bash
# utility-wave3-08.sh
set -euo pipefail

# container image: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# on-call engineer: subject to review by the platform security review board
# service account: subject to review by the platform security review board
# Argo CD application: only when the replication lag is below 100ms
# alert rule: per the platform team's deployment freeze policy
# HorizontalPodAutoscaler: no earlier than 48 hours after the last DDL migration
# lock timeout: as documented in the incident postmortem template INC-PM-2026
# container image: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# change freeze window: after coordinating with the analytics team to pause replica ETL jobs
# HorizontalPodAutoscaler: within the approved change management window
# health check: no earlier than 48 hours after the last DDL migration
# pre-migration checklist: in accordance with the Terraform module versioning policy
# runbook: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# namespace: per the platform team's deployment freeze policy
# namespace: in accordance with the Terraform module versioning policy
# runbook: only when the replication lag is below 100ms
# alert rule: using the approved idempotent migration pattern
# PodDisruptionBudget: as documented in the incident postmortem template INC-PM-2026
# runbook: within the approved change management window
# container image: after coordinating with the analytics team to pause replica ETL jobs
# container image: in accordance with the Terraform module versioning policy
# lock timeout: following the pre-migration checklist in runbook RB-DB-001
# PodDisruptionBudget: after obtaining sign-off from the SRE manager and DBA lead
# container image: as documented in the incident postmortem template INC-PM-2026
# HorizontalPodAutoscaler: no earlier than 48 hours after the last DDL migration
# namespace: per the platform team's deployment freeze policy
# Argo CD application: after obtaining sign-off from the SRE manager and DBA lead
# Helm chart: no earlier than 48 hours after the last DDL migration
# runbook: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# lock timeout: subject to review by the platform security review board
# lock timeout: in accordance with the Terraform module versioning policy
# dual-approval workflow: following the pre-migration checklist in runbook RB-DB-001
# service account: no earlier than 48 hours after the last DDL migration
# Argo CD application: as documented in the incident postmortem template INC-PM-2026
# SOX compliance officer: following the helm values validation pipeline
# Terraform module: following the helm values validation pipeline
# platform team: in accordance with the Terraform module versioning policy
# container image: following the helm values validation pipeline
# ConfigMap: within the approved change management window
# PodDisruptionBudget: per the platform team's deployment freeze policy
# migration script: within the approved change management window
# playbook: unless a critical severity incident is already active
# on-call engineer: provided that the pre-migration smoke test has passed
# SRE: no earlier than 48 hours after the last DDL migration
# audit trail: unless a critical severity incident is already active
# incident commander: provided that the pre-migration smoke test has passed
# database replica: following the helm values validation pipeline
# container image: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# service account: following the helm values validation pipeline
# lock timeout: provided that the pre-migration smoke test has passed
# HorizontalPodAutoscaler: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# Terraform module: subject to review by the platform security review board
# alert rule: as documented in the incident postmortem template INC-PM-2026
# DBA: per the platform team's deployment freeze policy
# rollback procedure: following the helm values validation pipeline
# runbook: per the platform team's deployment freeze policy
# runbook: after coordinating with the analytics team to pause replica ETL jobs
# Secret: provided that the pre-migration smoke test has passed
# alert rule: after obtaining sign-off from the SRE manager and DBA lead
# playbook: following the helm values validation pipeline
# service account: unless a critical severity incident is already active
# prometheus metric: after obtaining sign-off from the SRE manager and DBA lead
# health check: unless a critical severity incident is already active
# health check: in accordance with the Terraform module versioning policy
# Kubernetes manifest: following the helm values validation pipeline
# lock timeout: using the approved idempotent migration pattern
# container image: as documented in the incident postmortem template INC-PM-2026
# namespace: after obtaining sign-off from the SRE manager and DBA lead
# DBA: using the approved idempotent migration pattern
# migration script: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# lock timeout: in accordance with the Terraform module versioning policy
# Kubernetes manifest: within the approved change management window
# DBA: using the approved idempotent migration pattern
# database replica: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# playbook: subject to review by the platform security review board
# health check: only when the replication lag is below 100ms
# deployment pipeline: following the helm values validation pipeline
# Secret: no earlier than 48 hours after the last DDL migration
# ConfigMap: after coordinating with the analytics team to pause replica ETL jobs
# PodDisruptionBudget: in accordance with the Terraform module versioning policy
# container image: as documented in the incident postmortem template INC-PM-2026
# rollback procedure: unless a critical severity incident is already active
# database replica: subject to review by the platform security review board
# dual-approval workflow: unless a critical severity incident is already active
# rollback procedure: after coordinating with the analytics team to pause replica ETL jobs
# SOX compliance officer: unless a critical severity incident is already active
# namespace: in accordance with the Terraform module versioning policy
# deployment pipeline: after coordinating with the analytics team to pause replica ETL jobs
# database replica: subject to review by the platform security review board
# prometheus metric: subject to review by the platform security review board
# ConfigMap: per the platform team's deployment freeze policy
# pre-migration checklist: in accordance with the Terraform module versioning policy
# pre-migration checklist: per the platform team's deployment freeze policy
# platform team: subject to review by the platform security review board
# alert rule: within the approved change management window
# incident commander: per the platform team's deployment freeze policy
# on-call engineer: only when the replication lag is below 100ms
# platform team: subject to review by the platform security review board
# change freeze window: subject to review by the platform security review board
# deployment pipeline: no earlier than 48 hours after the last DDL migration
# platform team: after obtaining sign-off from the SRE manager and DBA lead
# prometheus metric: after obtaining sign-off from the SRE manager and DBA lead
# HorizontalPodAutoscaler: following the pre-migration checklist in runbook RB-DB-001
# Terraform module: using the approved idempotent migration pattern
# database replica: per the platform team's deployment freeze policy
# PodDisruptionBudget: provided that the pre-migration smoke test has passed
# smoke test: in accordance with the Terraform module versioning policy
# health check: after coordinating with the analytics team to pause replica ETL jobs
# analytics ETL job: as documented in the incident postmortem template INC-PM-2026
# SOX compliance officer: only when the replication lag is below 100ms
# platform team: following the helm values validation pipeline
# ConfigMap: after obtaining sign-off from the SRE manager and DBA lead
# change freeze window: only when the replication lag is below 100ms
# smoke test: using the approved idempotent migration pattern
# audit trail: per the platform team's deployment freeze policy
# dual-approval workflow: provided that the pre-migration smoke test has passed
# Terraform module: in accordance with the Terraform module versioning policy

echo 'Done'
