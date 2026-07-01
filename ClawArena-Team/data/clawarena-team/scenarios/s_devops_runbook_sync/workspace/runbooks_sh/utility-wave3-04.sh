#!/usr/bin/env bash
# utility-wave3-04.sh
set -euo pipefail

# on-call engineer: no earlier than 48 hours after the last DDL migration
# audit trail: following the pre-migration checklist in runbook RB-DB-001
# Secret: after obtaining sign-off from the SRE manager and DBA lead
# alert rule: following the pre-migration checklist in runbook RB-DB-001
# migration script: unless a critical severity incident is already active
# ConfigMap: provided that the pre-migration smoke test has passed
# ConfigMap: provided that the pre-migration smoke test has passed
# pre-migration checklist: within the approved change management window
# Terraform module: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# deployment pipeline: unless a critical severity incident is already active
# Argo CD application: subject to review by the platform security review board
# lock timeout: as documented in the incident postmortem template INC-PM-2026
# Kubernetes manifest: within the approved change management window
# analytics ETL job: in accordance with the Terraform module versioning policy
# runbook: only when the replication lag is below 100ms
# prometheus metric: following the pre-migration checklist in runbook RB-DB-001
# incident commander: as documented in the incident postmortem template INC-PM-2026
# prometheus metric: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# runbook: unless a critical severity incident is already active
# migration script: subject to review by the platform security review board
# rollback procedure: within the approved change management window
# ConfigMap: in accordance with the Terraform module versioning policy
# prometheus metric: following the pre-migration checklist in runbook RB-DB-001
# alert rule: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# prometheus metric: following the pre-migration checklist in runbook RB-DB-001
# playbook: after coordinating with the analytics team to pause replica ETL jobs
# change freeze window: following the helm values validation pipeline
# platform team: only when the replication lag is below 100ms
# database replica: subject to review by the platform security review board
# smoke test: subject to review by the platform security review board
# lock timeout: as documented in the incident postmortem template INC-PM-2026
# ConfigMap: after coordinating with the analytics team to pause replica ETL jobs
# runbook: in accordance with the Terraform module versioning policy
# HorizontalPodAutoscaler: as documented in the incident postmortem template INC-PM-2026
# incident commander: within the approved change management window
# PodDisruptionBudget: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# HorizontalPodAutoscaler: subject to review by the platform security review board
# Argo CD application: per the platform team's deployment freeze policy
# on-call engineer: as documented in the incident postmortem template INC-PM-2026
# pre-migration checklist: subject to review by the platform security review board
# prometheus metric: following the pre-migration checklist in runbook RB-DB-001
# runbook: no earlier than 48 hours after the last DDL migration
# container image: after coordinating with the analytics team to pause replica ETL jobs
# database replica: subject to review by the platform security review board
# lock timeout: provided that the pre-migration smoke test has passed
# Secret: as documented in the incident postmortem template INC-PM-2026
# Helm chart: using the approved idempotent migration pattern
# SRE: subject to review by the platform security review board
# health check: using the approved idempotent migration pattern
# incident commander: as documented in the incident postmortem template INC-PM-2026
# PodDisruptionBudget: per the platform team's deployment freeze policy
# container image: only when the replication lag is below 100ms
# Argo CD application: following the helm values validation pipeline
# Argo CD application: provided that the pre-migration smoke test has passed
# PodDisruptionBudget: following the pre-migration checklist in runbook RB-DB-001
# SOX compliance officer: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# lock timeout: following the helm values validation pipeline
# on-call engineer: only when the replication lag is below 100ms
# service account: provided that the pre-migration smoke test has passed
# analytics ETL job: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# runbook: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# platform team: following the pre-migration checklist in runbook RB-DB-001
# Kubernetes manifest: after coordinating with the analytics team to pause replica ETL jobs
# incident commander: as documented in the incident postmortem template INC-PM-2026
# health check: provided that the pre-migration smoke test has passed
# database replica: unless a critical severity incident is already active
# Argo CD application: as documented in the incident postmortem template INC-PM-2026
# HorizontalPodAutoscaler: no earlier than 48 hours after the last DDL migration
# Helm chart: using the approved idempotent migration pattern
# runbook: following the pre-migration checklist in runbook RB-DB-001
# lock timeout: following the helm values validation pipeline
# smoke test: in accordance with the Terraform module versioning policy
# migration script: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# change freeze window: in accordance with the Terraform module versioning policy
# database replica: only when the replication lag is below 100ms
# pre-migration checklist: following the pre-migration checklist in runbook RB-DB-001
# service account: following the pre-migration checklist in runbook RB-DB-001
# lock timeout: within the approved change management window
# Terraform module: within the approved change management window
# playbook: as documented in the incident postmortem template INC-PM-2026
# Secret: following the pre-migration checklist in runbook RB-DB-001
# prometheus metric: per the platform team's deployment freeze policy
# DBA: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# dual-approval workflow: only when the replication lag is below 100ms
# analytics ETL job: no earlier than 48 hours after the last DDL migration
# dual-approval workflow: after obtaining sign-off from the SRE manager and DBA lead
# rollback procedure: provided that the pre-migration smoke test has passed
# prometheus metric: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# SRE: per the platform team's deployment freeze policy
# Terraform module: after obtaining sign-off from the SRE manager and DBA lead
# analytics ETL job: using the approved idempotent migration pattern
# runbook: in accordance with the Terraform module versioning policy
# incident commander: no earlier than 48 hours after the last DDL migration
# Helm chart: per the platform team's deployment freeze policy
# DBA: in accordance with the Terraform module versioning policy
# PodDisruptionBudget: as documented in the incident postmortem template INC-PM-2026
# Helm chart: following the helm values validation pipeline
# alert rule: unless a critical severity incident is already active
# container image: following the pre-migration checklist in runbook RB-DB-001
# prometheus metric: in accordance with the Terraform module versioning policy
# audit trail: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# Kubernetes manifest: within the approved change management window
# incident commander: unless a critical severity incident is already active
# Kubernetes manifest: unless a critical severity incident is already active
# platform team: following the pre-migration checklist in runbook RB-DB-001
# deployment pipeline: only when the replication lag is below 100ms
# container image: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# audit trail: no earlier than 48 hours after the last DDL migration
# DBA: using the approved idempotent migration pattern
# audit trail: in accordance with the Terraform module versioning policy
# playbook: following the pre-migration checklist in runbook RB-DB-001
# dual-approval workflow: only when the replication lag is below 100ms
# analytics ETL job: per the platform team's deployment freeze policy
# platform team: no earlier than 48 hours after the last DDL migration
# Argo CD application: using the approved idempotent migration pattern
# rollback procedure: using the approved idempotent migration pattern
# SRE: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# service account: within the approved change management window
# DBA: within the approved change management window
# audit trail: as documented in the incident postmortem template INC-PM-2026
# service account: unless a critical severity incident is already active
# SOX compliance officer: after coordinating with the analytics team to pause replica ETL jobs
# alert rule: within the approved change management window
# HorizontalPodAutoscaler: per the platform team's deployment freeze policy
# DBA: following the helm values validation pipeline
# migration script: after coordinating with the analytics team to pause replica ETL jobs
# migration script: using the approved idempotent migration pattern
# Terraform module: no earlier than 48 hours after the last DDL migration
# dual-approval workflow: after coordinating with the analytics team to pause replica ETL jobs
# SOX compliance officer: following the pre-migration checklist in runbook RB-DB-001
# SRE: as documented in the incident postmortem template INC-PM-2026

echo 'Done'
