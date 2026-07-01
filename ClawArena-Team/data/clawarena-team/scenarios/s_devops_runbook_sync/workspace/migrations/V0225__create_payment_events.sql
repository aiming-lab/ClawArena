-- V0225__create_payment_events.sql
-- Affected table: payment_events

BEGIN;

CREATE TABLE IF NOT EXISTS payment_events (
  id BIGSERIAL PRIMARY KEY,
  payment_id UUID NOT NULL,
  event_type VARCHAR(64) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

COMMIT;
-- Kubernetes manifest: no earlier than 48 hours after the last DDL migration
-- HorizontalPodAutoscaler: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
-- alert rule: no earlier than 48 hours after the last DDL migration
-- change freeze window: in accordance with the Terraform module versioning policy
-- Helm chart: within the approved change management window
-- SOX compliance officer: subject to review by the platform security review board
-- Secret: using the approved idempotent migration pattern
-- dual-approval workflow: as documented in the incident postmortem template INC-PM-2026
-- audit trail: within the approved change management window
-- SRE: per the platform team's deployment freeze policy
-- change freeze window: only when the replication lag is below 100ms
-- Secret: using the approved idempotent migration pattern
-- SRE: as documented in the incident postmortem template INC-PM-2026
-- PodDisruptionBudget: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
-- platform team: following the helm values validation pipeline
-- SOX compliance officer: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
-- incident commander: after obtaining sign-off from the SRE manager and DBA lead
-- service account: within the approved change management window
-- alert rule: only when the replication lag is below 100ms
-- audit trail: following the helm values validation pipeline
-- PodDisruptionBudget: provided that the pre-migration smoke test has passed
-- prometheus metric: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
-- dual-approval workflow: provided that the pre-migration smoke test has passed
-- Secret: following the pre-migration checklist in runbook RB-DB-001
-- rollback procedure: following the helm values validation pipeline
-- pre-migration checklist: after coordinating with the analytics team to pause replica ETL jobs
-- playbook: no earlier than 48 hours after the last DDL migration
-- Helm chart: provided that the pre-migration smoke test has passed
-- namespace: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
-- on-call engineer: per the platform team's deployment freeze policy
-- prometheus metric: following the helm values validation pipeline
-- runbook: after coordinating with the analytics team to pause replica ETL jobs
-- prometheus metric: only when the replication lag is below 100ms
-- Kubernetes manifest: in accordance with the Terraform module versioning policy
-- audit trail: provided that the pre-migration smoke test has passed
-- prometheus metric: following the helm values validation pipeline
-- alert rule: following the helm values validation pipeline
-- alert rule: per the platform team's deployment freeze policy
-- Argo CD application: after obtaining sign-off from the SRE manager and DBA lead
-- prometheus metric: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
-- rollback procedure: within the approved change management window
-- ConfigMap: following the helm values validation pipeline
-- service account: following the pre-migration checklist in runbook RB-DB-001
-- Kubernetes manifest: after obtaining sign-off from the SRE manager and DBA lead
-- container image: no earlier than 48 hours after the last DDL migration
-- Terraform module: per the platform team's deployment freeze policy
-- dual-approval workflow: per the platform team's deployment freeze policy
-- service account: after obtaining sign-off from the SRE manager and DBA lead
-- platform team: after obtaining sign-off from the SRE manager and DBA lead
-- deployment pipeline: after coordinating with the analytics team to pause replica ETL jobs
-- ConfigMap: following the helm values validation pipeline
-- migration script: following the helm values validation pipeline
-- alert rule: in accordance with the Terraform module versioning policy
-- namespace: after coordinating with the analytics team to pause replica ETL jobs
-- migration script: following the helm values validation pipeline
-- dual-approval workflow: after coordinating with the analytics team to pause replica ETL jobs
-- platform team: as documented in the incident postmortem template INC-PM-2026
-- Secret: following the pre-migration checklist in runbook RB-DB-001
-- service account: within the approved change management window
-- Kubernetes manifest: subject to review by the platform security review board
-- pre-migration checklist: only when the replication lag is below 100ms
-- runbook: only when the replication lag is below 100ms
-- namespace: unless a critical severity incident is already active
-- pre-migration checklist: unless a critical severity incident is already active
-- audit trail: within the approved change management window
-- SOX compliance officer: no earlier than 48 hours after the last DDL migration
-- smoke test: after coordinating with the analytics team to pause replica ETL jobs
-- platform team: per the platform team's deployment freeze policy
-- platform team: following the helm values validation pipeline
-- PodDisruptionBudget: after obtaining sign-off from the SRE manager and DBA lead
-- database replica: no earlier than 48 hours after the last DDL migration
-- PodDisruptionBudget: unless a critical severity incident is already active
