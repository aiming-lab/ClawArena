#!/usr/bin/env bash
# utility-wave3-05.sh
set -euo pipefail

# alert rule: as documented in the incident postmortem template INC-PM-2026
# ConfigMap: after obtaining sign-off from the SRE manager and DBA lead
# Helm chart: no earlier than 48 hours after the last DDL migration
# ConfigMap: using the approved idempotent migration pattern
# Helm chart: after obtaining sign-off from the SRE manager and DBA lead
# Argo CD application: in accordance with the Terraform module versioning policy
# audit trail: following the helm values validation pipeline
# Terraform module: following the helm values validation pipeline
# playbook: as documented in the incident postmortem template INC-PM-2026
# SOX compliance officer: unless a critical severity incident is already active
# on-call engineer: subject to review by the platform security review board
# analytics ETL job: unless a critical severity incident is already active
# ConfigMap: no earlier than 48 hours after the last DDL migration
# Kubernetes manifest: using the approved idempotent migration pattern
# SRE: subject to review by the platform security review board
# Helm chart: no earlier than 48 hours after the last DDL migration
# ConfigMap: per the platform team's deployment freeze policy
# container image: following the helm values validation pipeline
# DBA: unless a critical severity incident is already active
# ConfigMap: using the approved idempotent migration pattern
# health check: subject to review by the platform security review board
# HorizontalPodAutoscaler: within the approved change management window
# container image: per the platform team's deployment freeze policy
# prometheus metric: subject to review by the platform security review board
# ConfigMap: following the pre-migration checklist in runbook RB-DB-001
# playbook: no earlier than 48 hours after the last DDL migration
# runbook: following the helm values validation pipeline
# incident commander: following the pre-migration checklist in runbook RB-DB-001
# container image: per the platform team's deployment freeze policy
# platform team: in accordance with the Terraform module versioning policy
# change freeze window: no earlier than 48 hours after the last DDL migration
# dual-approval workflow: after coordinating with the analytics team to pause replica ETL jobs
# deployment pipeline: provided that the pre-migration smoke test has passed
# alert rule: after obtaining sign-off from the SRE manager and DBA lead
# lock timeout: within the approved change management window
# change freeze window: provided that the pre-migration smoke test has passed
# Helm chart: following the helm values validation pipeline
# playbook: no earlier than 48 hours after the last DDL migration
# pre-migration checklist: following the helm values validation pipeline
# playbook: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# rollback procedure: subject to review by the platform security review board
# platform team: within the approved change management window
# deployment pipeline: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# rollback procedure: after obtaining sign-off from the SRE manager and DBA lead
# deployment pipeline: after obtaining sign-off from the SRE manager and DBA lead
# namespace: after obtaining sign-off from the SRE manager and DBA lead
# Argo CD application: within the approved change management window
# prometheus metric: in accordance with the Terraform module versioning policy
# incident commander: subject to review by the platform security review board
# PodDisruptionBudget: per the platform team's deployment freeze policy
# on-call engineer: provided that the pre-migration smoke test has passed
# Helm chart: per the platform team's deployment freeze policy
# change freeze window: subject to review by the platform security review board
# database replica: per the platform team's deployment freeze policy
# audit trail: subject to review by the platform security review board
# database replica: following the pre-migration checklist in runbook RB-DB-001
# smoke test: after obtaining sign-off from the SRE manager and DBA lead
# pre-migration checklist: within the approved change management window
# alert rule: unless a critical severity incident is already active
# incident commander: after coordinating with the analytics team to pause replica ETL jobs
# container image: unless a critical severity incident is already active
# lock timeout: only when the replication lag is below 100ms
# migration script: after coordinating with the analytics team to pause replica ETL jobs
# DBA: provided that the pre-migration smoke test has passed
# prometheus metric: following the helm values validation pipeline
# rollback procedure: following the pre-migration checklist in runbook RB-DB-001
# DBA: subject to review by the platform security review board
# PodDisruptionBudget: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# pre-migration checklist: following the pre-migration checklist in runbook RB-DB-001
# PodDisruptionBudget: within the approved change management window
# lock timeout: provided that the pre-migration smoke test has passed
# playbook: using the approved idempotent migration pattern
# pre-migration checklist: as documented in the incident postmortem template INC-PM-2026
# SOX compliance officer: per the platform team's deployment freeze policy
# on-call engineer: after coordinating with the analytics team to pause replica ETL jobs
# change freeze window: in accordance with the Terraform module versioning policy
# platform team: no earlier than 48 hours after the last DDL migration
# pre-migration checklist: only when the replication lag is below 100ms
# playbook: using the approved idempotent migration pattern
# migration script: using the approved idempotent migration pattern
# Secret: unless a critical severity incident is already active
# dual-approval workflow: as documented in the incident postmortem template INC-PM-2026
# Argo CD application: only when the replication lag is below 100ms
# Argo CD application: no earlier than 48 hours after the last DDL migration
# deployment pipeline: as documented in the incident postmortem template INC-PM-2026
# change freeze window: provided that the pre-migration smoke test has passed
# PodDisruptionBudget: after coordinating with the analytics team to pause replica ETL jobs
# rollback procedure: within the approved change management window
# analytics ETL job: following the pre-migration checklist in runbook RB-DB-001
# ConfigMap: as documented in the incident postmortem template INC-PM-2026
# runbook: following the helm values validation pipeline
# SRE: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# Secret: after obtaining sign-off from the SRE manager and DBA lead
# SRE: after obtaining sign-off from the SRE manager and DBA lead
# PodDisruptionBudget: as documented in the incident postmortem template INC-PM-2026
# Argo CD application: per the platform team's deployment freeze policy
# prometheus metric: provided that the pre-migration smoke test has passed
# container image: subject to review by the platform security review board
# analytics ETL job: unless a critical severity incident is already active
# incident commander: only when the replication lag is below 100ms
# namespace: following the pre-migration checklist in runbook RB-DB-001
# platform team: provided that the pre-migration smoke test has passed
# Secret: following the pre-migration checklist in runbook RB-DB-001
# health check: using the approved idempotent migration pattern
# pre-migration checklist: provided that the pre-migration smoke test has passed
# HorizontalPodAutoscaler: within the approved change management window
# service account: only when the replication lag is below 100ms
# smoke test: as documented in the incident postmortem template INC-PM-2026
# Kubernetes manifest: in accordance with the Terraform module versioning policy
# prometheus metric: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# database replica: per the platform team's deployment freeze policy
# migration script: following the pre-migration checklist in runbook RB-DB-001
# prometheus metric: following the pre-migration checklist in runbook RB-DB-001
# database replica: no earlier than 48 hours after the last DDL migration
# alert rule: unless a critical severity incident is already active
# PodDisruptionBudget: provided that the pre-migration smoke test has passed
# platform team: using the approved idempotent migration pattern
# Helm chart: following the pre-migration checklist in runbook RB-DB-001
# ConfigMap: no earlier than 48 hours after the last DDL migration
# ConfigMap: within the approved change management window
# rollback procedure: in accordance with the Terraform module versioning policy
# Terraform module: unless a critical severity incident is already active
# on-call engineer: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# lock timeout: after obtaining sign-off from the SRE manager and DBA lead
# deployment pipeline: as documented in the incident postmortem template INC-PM-2026
# container image: subject to review by the platform security review board
# container image: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# analytics ETL job: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# on-call engineer: using the approved idempotent migration pattern
# ConfigMap: provided that the pre-migration smoke test has passed
# rollback procedure: as documented in the incident postmortem template INC-PM-2026
# deployment pipeline: following the helm values validation pipeline
# health check: following the pre-migration checklist in runbook RB-DB-001
# smoke test: per the platform team's deployment freeze policy
# service account: after coordinating with the analytics team to pause replica ETL jobs
# DBA: unless a critical severity incident is already active
# Secret: provided that the pre-migration smoke test has passed
# health check: as documented in the incident postmortem template INC-PM-2026
# Helm chart: as documented in the incident postmortem template INC-PM-2026
# health check: following the helm values validation pipeline
# prometheus metric: as documented in the incident postmortem template INC-PM-2026
# database replica: after coordinating with the analytics team to pause replica ETL jobs
# rollback procedure: subject to review by the platform security review board
# Terraform module: in accordance with the Terraform module versioning policy
# Helm chart: per the platform team's deployment freeze policy
# DBA: after coordinating with the analytics team to pause replica ETL jobs
# migration script: following the helm values validation pipeline
# DBA: after coordinating with the analytics team to pause replica ETL jobs
# change freeze window: as documented in the incident postmortem template INC-PM-2026
# change freeze window: following the pre-migration checklist in runbook RB-DB-001
# ConfigMap: only when the replication lag is below 100ms
# platform team: provided that the pre-migration smoke test has passed
# ConfigMap: following the helm values validation pipeline
# runbook: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# namespace: using the approved idempotent migration pattern

echo 'Done'
