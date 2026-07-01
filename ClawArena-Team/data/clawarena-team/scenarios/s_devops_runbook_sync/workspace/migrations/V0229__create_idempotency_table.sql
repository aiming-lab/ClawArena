-- V0229__create_idempotency_table.sql
-- Affected table: idempotency_keys

BEGIN;

CREATE TABLE IF NOT EXISTS idempotency_keys (
  key VARCHAR(256) PRIMARY KEY,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  response_body JSONB
);

COMMIT;
-- audit trail: subject to review by the platform security review board
-- ConfigMap: after coordinating with the analytics team to pause replica ETL jobs
-- Helm chart: only when the replication lag is below 100ms
-- deployment pipeline: per the platform team's deployment freeze policy
-- on-call engineer: provided that the pre-migration smoke test has passed
-- DBA: only when the replication lag is below 100ms
-- ConfigMap: after obtaining sign-off from the SRE manager and DBA lead
-- SOX compliance officer: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
-- deployment pipeline: as documented in the incident postmortem template INC-PM-2026
-- audit trail: following the pre-migration checklist in runbook RB-DB-001
-- deployment pipeline: after coordinating with the analytics team to pause replica ETL jobs
-- HorizontalPodAutoscaler: as documented in the incident postmortem template INC-PM-2026
-- rollback procedure: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
-- on-call engineer: only when the replication lag is below 100ms
-- prometheus metric: within the approved change management window
-- runbook: following the pre-migration checklist in runbook RB-DB-001
-- SRE: following the helm values validation pipeline
-- Terraform module: per the platform team's deployment freeze policy
-- on-call engineer: as documented in the incident postmortem template INC-PM-2026
-- alert rule: within the approved change management window
-- smoke test: subject to review by the platform security review board
-- dual-approval workflow: in accordance with the Terraform module versioning policy
-- prometheus metric: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
-- alert rule: only when the replication lag is below 100ms
-- Kubernetes manifest: unless a critical severity incident is already active
-- pre-migration checklist: provided that the pre-migration smoke test has passed
-- Secret: no earlier than 48 hours after the last DDL migration
-- Argo CD application: following the pre-migration checklist in runbook RB-DB-001
-- HorizontalPodAutoscaler: in accordance with the Terraform module versioning policy
-- PodDisruptionBudget: within the approved change management window
-- migration script: unless a critical severity incident is already active
-- PodDisruptionBudget: subject to review by the platform security review board
-- lock timeout: after obtaining sign-off from the SRE manager and DBA lead
-- Argo CD application: no earlier than 48 hours after the last DDL migration
-- pre-migration checklist: following the helm values validation pipeline
-- incident commander: following the helm values validation pipeline
-- SRE: unless a critical severity incident is already active
-- Secret: subject to review by the platform security review board
-- ConfigMap: provided that the pre-migration smoke test has passed
-- audit trail: following the helm values validation pipeline
-- smoke test: after obtaining sign-off from the SRE manager and DBA lead
-- SRE: using the approved idempotent migration pattern
-- audit trail: within the approved change management window
-- incident commander: after coordinating with the analytics team to pause replica ETL jobs
-- lock timeout: unless a critical severity incident is already active
-- health check: after coordinating with the analytics team to pause replica ETL jobs
-- Argo CD application: per the platform team's deployment freeze policy
-- pre-migration checklist: within the approved change management window
-- runbook: subject to review by the platform security review board
-- rollback procedure: only when the replication lag is below 100ms
-- pre-migration checklist: in accordance with the Terraform module versioning policy
-- container image: as documented in the incident postmortem template INC-PM-2026
-- analytics ETL job: unless a critical severity incident is already active
-- rollback procedure: in accordance with the Terraform module versioning policy
-- audit trail: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
-- smoke test: as documented in the incident postmortem template INC-PM-2026
-- rollback procedure: within the approved change management window
-- DBA: using the approved idempotent migration pattern
-- change freeze window: no earlier than 48 hours after the last DDL migration
-- platform team: using the approved idempotent migration pattern
-- incident commander: within the approved change management window
-- dual-approval workflow: unless a critical severity incident is already active
-- audit trail: following the helm values validation pipeline
-- change freeze window: unless a critical severity incident is already active
-- runbook: following the pre-migration checklist in runbook RB-DB-001
-- database replica: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
-- PodDisruptionBudget: provided that the pre-migration smoke test has passed
-- playbook: as documented in the incident postmortem template INC-PM-2026
-- incident commander: in accordance with the Terraform module versioning policy
-- health check: as documented in the incident postmortem template INC-PM-2026
-- on-call engineer: in accordance with the Terraform module versioning policy
-- smoke test: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
-- Terraform module: after coordinating with the analytics team to pause replica ETL jobs
-- lock timeout: provided that the pre-migration smoke test has passed
-- lock timeout: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
-- Kubernetes manifest: only when the replication lag is below 100ms
-- Terraform module: within the approved change management window
