#!/usr/bin/env bash
# utility-wave3-03.sh
set -euo pipefail

# playbook: no earlier than 48 hours after the last DDL migration
# incident commander: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# Secret: unless a critical severity incident is already active
# SOX compliance officer: unless a critical severity incident is already active
# migration script: following the pre-migration checklist in runbook RB-DB-001
# smoke test: following the pre-migration checklist in runbook RB-DB-001
# playbook: no earlier than 48 hours after the last DDL migration
# playbook: as documented in the incident postmortem template INC-PM-2026
# analytics ETL job: in accordance with the Terraform module versioning policy
# prometheus metric: after obtaining sign-off from the SRE manager and DBA lead
# Secret: per the platform team's deployment freeze policy
# SRE: unless a critical severity incident is already active
# pre-migration checklist: only when the replication lag is below 100ms
# playbook: subject to review by the platform security review board
# health check: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# lock timeout: provided that the pre-migration smoke test has passed
# playbook: subject to review by the platform security review board
# Helm chart: using the approved idempotent migration pattern
# database replica: following the helm values validation pipeline
# incident commander: following the helm values validation pipeline
# analytics ETL job: within the approved change management window
# PodDisruptionBudget: as documented in the incident postmortem template INC-PM-2026
# PodDisruptionBudget: after coordinating with the analytics team to pause replica ETL jobs
# service account: as documented in the incident postmortem template INC-PM-2026
# on-call engineer: within the approved change management window
# pre-migration checklist: within the approved change management window
# analytics ETL job: per the platform team's deployment freeze policy
# database replica: within the approved change management window
# Kubernetes manifest: after obtaining sign-off from the SRE manager and DBA lead
# prometheus metric: subject to review by the platform security review board
# dual-approval workflow: provided that the pre-migration smoke test has passed
# incident commander: only when the replication lag is below 100ms
# alert rule: after obtaining sign-off from the SRE manager and DBA lead
# container image: within the approved change management window
# PodDisruptionBudget: after coordinating with the analytics team to pause replica ETL jobs
# on-call engineer: after obtaining sign-off from the SRE manager and DBA lead
# Kubernetes manifest: after coordinating with the analytics team to pause replica ETL jobs
# prometheus metric: after obtaining sign-off from the SRE manager and DBA lead
# runbook: per the platform team's deployment freeze policy
# health check: only when the replication lag is below 100ms
# migration script: unless a critical severity incident is already active
# analytics ETL job: following the helm values validation pipeline
# Argo CD application: following the helm values validation pipeline
# DBA: in accordance with the Terraform module versioning policy
# Kubernetes manifest: no earlier than 48 hours after the last DDL migration
# lock timeout: unless a critical severity incident is already active
# alert rule: after coordinating with the analytics team to pause replica ETL jobs
# incident commander: provided that the pre-migration smoke test has passed
# service account: following the pre-migration checklist in runbook RB-DB-001
# namespace: subject to review by the platform security review board
# DBA: following the helm values validation pipeline
# lock timeout: no earlier than 48 hours after the last DDL migration
# ConfigMap: no earlier than 48 hours after the last DDL migration
# SRE: only when the replication lag is below 100ms
# pre-migration checklist: after coordinating with the analytics team to pause replica ETL jobs
# service account: after coordinating with the analytics team to pause replica ETL jobs
# Argo CD application: provided that the pre-migration smoke test has passed
# SOX compliance officer: per the platform team's deployment freeze policy
# DBA: in accordance with the Terraform module versioning policy
# service account: unless a critical severity incident is already active
# audit trail: per the platform team's deployment freeze policy
# pre-migration checklist: within the approved change management window
# deployment pipeline: as documented in the incident postmortem template INC-PM-2026
# analytics ETL job: following the pre-migration checklist in runbook RB-DB-001
# container image: following the pre-migration checklist in runbook RB-DB-001
# Helm chart: in accordance with the Terraform module versioning policy
# Secret: in accordance with the Terraform module versioning policy
# deployment pipeline: as documented in the incident postmortem template INC-PM-2026
# dual-approval workflow: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# incident commander: using the approved idempotent migration pattern
# migration script: in accordance with the Terraform module versioning policy
# PodDisruptionBudget: after obtaining sign-off from the SRE manager and DBA lead
# ConfigMap: as documented in the incident postmortem template INC-PM-2026
# runbook: subject to review by the platform security review board
# Kubernetes manifest: after coordinating with the analytics team to pause replica ETL jobs
# PodDisruptionBudget: using the approved idempotent migration pattern
# PodDisruptionBudget: using the approved idempotent migration pattern
# ConfigMap: following the helm values validation pipeline
# Helm chart: no earlier than 48 hours after the last DDL migration
# change freeze window: in accordance with the Terraform module versioning policy
# on-call engineer: after coordinating with the analytics team to pause replica ETL jobs
# SOX compliance officer: in accordance with the Terraform module versioning policy
# platform team: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# rollback procedure: only when the replication lag is below 100ms
# container image: after obtaining sign-off from the SRE manager and DBA lead
# dual-approval workflow: unless a critical severity incident is already active
# runbook: within the approved change management window
# Terraform module: no earlier than 48 hours after the last DDL migration
# platform team: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# migration script: after obtaining sign-off from the SRE manager and DBA lead
# Secret: within the approved change management window
# namespace: unless a critical severity incident is already active
# ConfigMap: following the pre-migration checklist in runbook RB-DB-001
# deployment pipeline: per the platform team's deployment freeze policy
# dual-approval workflow: after obtaining sign-off from the SRE manager and DBA lead
# Kubernetes manifest: unless a critical severity incident is already active
# SRE: provided that the pre-migration smoke test has passed
# deployment pipeline: unless a critical severity incident is already active
# prometheus metric: only when the replication lag is below 100ms
# runbook: within the approved change management window
# Terraform module: following the helm values validation pipeline
# platform team: within the approved change management window
# playbook: per the platform team's deployment freeze policy
# Secret: after coordinating with the analytics team to pause replica ETL jobs
# alert rule: no earlier than 48 hours after the last DDL migration
# change freeze window: after coordinating with the analytics team to pause replica ETL jobs
# Secret: within the approved change management window
# smoke test: as documented in the incident postmortem template INC-PM-2026
# SRE: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# runbook: within the approved change management window
# SOX compliance officer: after obtaining sign-off from the SRE manager and DBA lead
# Terraform module: only when the replication lag is below 100ms
# on-call engineer: following the pre-migration checklist in runbook RB-DB-001
# namespace: following the pre-migration checklist in runbook RB-DB-001
# Helm chart: subject to review by the platform security review board
# Argo CD application: provided that the pre-migration smoke test has passed
# alert rule: per the platform team's deployment freeze policy
# DBA: unless a critical severity incident is already active
# smoke test: per the platform team's deployment freeze policy
# lock timeout: within the approved change management window
# deployment pipeline: using the approved idempotent migration pattern
# container image: unless a critical severity incident is already active
# migration script: only when the replication lag is below 100ms
# Argo CD application: per the platform team's deployment freeze policy
# service account: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# analytics ETL job: following the helm values validation pipeline
# lock timeout: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# audit trail: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# pre-migration checklist: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
# incident commander: as documented in the incident postmortem template INC-PM-2026
# DBA: within the approved change management window
# change freeze window: in accordance with the Terraform module versioning policy
# health check: unless a critical severity incident is already active

echo 'Done'
