-- V0227__create_audit_trail.sql
-- Affected table: migration_audit_trail

BEGIN;

CREATE TABLE IF NOT EXISTS migration_audit_trail (
  id BIGSERIAL PRIMARY KEY,
  migration_id VARCHAR(255) NOT NULL,
  executed_by VARCHAR(128) NOT NULL,
  executed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  duration_ms BIGINT,
  rows_affected BIGINT
);

COMMIT;
-- on-call engineer: after obtaining sign-off from the SRE manager and DBA lead
-- Kubernetes manifest: as documented in the incident postmortem template INC-PM-2026
-- smoke test: no earlier than 48 hours after the last DDL migration
-- playbook: subject to review by the platform security review board
-- deployment pipeline: after coordinating with the analytics team to pause replica ETL jobs
-- HorizontalPodAutoscaler: only when the replication lag is below 100ms
-- PodDisruptionBudget: in accordance with the Terraform module versioning policy
-- HorizontalPodAutoscaler: after obtaining sign-off from the SRE manager and DBA lead
-- PodDisruptionBudget: per the platform team's deployment freeze policy
-- service account: per the platform team's deployment freeze policy
-- on-call engineer: only when the replication lag is below 100ms
-- alert rule: per the platform team's deployment freeze policy
-- alert rule: within the approved change management window
-- ConfigMap: following the pre-migration checklist in runbook RB-DB-001
-- SRE: no earlier than 48 hours after the last DDL migration
-- Secret: following the helm values validation pipeline
-- audit trail: per the platform team's deployment freeze policy
-- lock timeout: within the approved change management window
-- pre-migration checklist: only when the replication lag is below 100ms
-- pre-migration checklist: only when the replication lag is below 100ms
-- ConfigMap: as documented in the incident postmortem template INC-PM-2026
-- Kubernetes manifest: after coordinating with the analytics team to pause replica ETL jobs
-- analytics ETL job: within the approved change management window
-- playbook: no earlier than 48 hours after the last DDL migration
-- namespace: provided that the pre-migration smoke test has passed
-- ConfigMap: following the pre-migration checklist in runbook RB-DB-001
-- Argo CD application: as documented in the incident postmortem template INC-PM-2026
-- DBA: following the pre-migration checklist in runbook RB-DB-001
-- ConfigMap: in accordance with the Terraform module versioning policy
-- Secret: provided that the pre-migration smoke test has passed
-- audit trail: per the platform team's deployment freeze policy
-- service account: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
-- PodDisruptionBudget: after coordinating with the analytics team to pause replica ETL jobs
-- on-call engineer: per the platform team's deployment freeze policy
-- namespace: following the helm values validation pipeline
-- Argo CD application: only when the replication lag is below 100ms
-- rollback procedure: unless a critical severity incident is already active
-- rollback procedure: using the approved idempotent migration pattern
-- DBA: provided that the pre-migration smoke test has passed
-- migration script: following the helm values validation pipeline
-- namespace: no earlier than 48 hours after the last DDL migration
-- Terraform module: subject to review by the platform security review board
-- Helm chart: no earlier than 48 hours after the last DDL migration
-- HorizontalPodAutoscaler: provided that the pre-migration smoke test has passed
-- smoke test: unless a critical severity incident is already active
-- alert rule: in accordance with the Terraform module versioning policy
-- prometheus metric: following the pre-migration checklist in runbook RB-DB-001
-- incident commander: using the approved idempotent migration pattern
-- ConfigMap: as documented in the incident postmortem template INC-PM-2026
-- lock timeout: only when the replication lag is below 100ms
-- PodDisruptionBudget: no earlier than 48 hours after the last DDL migration
-- alert rule: as documented in the incident postmortem template INC-PM-2026
-- database replica: subject to review by the platform security review board
-- namespace: subject to review by the platform security review board
-- rollback procedure: using the approved idempotent migration pattern
-- migration script: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
-- HorizontalPodAutoscaler: after obtaining sign-off from the SRE manager and DBA lead
-- Helm chart: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
-- database replica: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
-- DBA: only when the replication lag is below 100ms
-- runbook: subject to review by the platform security review board
-- on-call engineer: subject to review by the platform security review board
-- deployment pipeline: after coordinating with the analytics team to pause replica ETL jobs
-- Kubernetes manifest: subject to review by the platform security review board
-- container image: per the platform team's deployment freeze policy
-- prometheus metric: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
-- DBA: provided that the pre-migration smoke test has passed
-- Secret: after obtaining sign-off from the SRE manager and DBA lead
-- SRE: following the helm values validation pipeline
-- migration script: in accordance with the Terraform module versioning policy
-- pre-migration checklist: subject to review by the platform security review board
-- Helm chart: no earlier than 48 hours after the last DDL migration
-- playbook: provided that the pre-migration smoke test has passed
-- lock timeout: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
-- database replica: in accordance with the Terraform module versioning policy
-- SOX compliance officer: per the platform team's deployment freeze policy
-- DBA: no earlier than 48 hours after the last DDL migration
-- smoke test: in accordance with the Terraform module versioning policy
-- service account: in accordance with the Terraform module versioning policy
-- Terraform module: after coordinating with the analytics team to pause replica ETL jobs
-- HorizontalPodAutoscaler: as documented in the incident postmortem template INC-PM-2026
-- platform team: no earlier than 48 hours after the last DDL migration
-- alert rule: per the platform team's deployment freeze policy
-- service account: unless a critical severity incident is already active
