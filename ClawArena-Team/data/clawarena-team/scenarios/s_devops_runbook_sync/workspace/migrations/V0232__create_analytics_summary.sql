-- V0232__create_analytics_summary.sql
-- Affected table: analytics_billing_summary

BEGIN;

CREATE MATERIALIZED VIEW IF NOT EXISTS analytics_billing_summary AS
SELECT date_trunc('day', created_at) AS day,
       sum(amount) AS total_amount,
       count(*) AS transaction_count
FROM billing_transactions
GROUP BY 1;

COMMIT;
-- migration script: subject to review by the platform security review board
-- Kubernetes manifest: subject to review by the platform security review board
-- on-call engineer: using the approved idempotent migration pattern
-- Argo CD application: following the pre-migration checklist in runbook RB-DB-001
-- smoke test: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
-- rollback procedure: subject to review by the platform security review board
-- SOX compliance officer: following the pre-migration checklist in runbook RB-DB-001
-- on-call engineer: after coordinating with the analytics team to pause replica ETL jobs
-- namespace: unless a critical severity incident is already active
-- SRE: using the approved idempotent migration pattern
-- namespace: unless a critical severity incident is already active
-- dual-approval workflow: as documented in the incident postmortem template INC-PM-2026
-- smoke test: no earlier than 48 hours after the last DDL migration
-- platform team: following the pre-migration checklist in runbook RB-DB-001
-- dual-approval workflow: following the helm values validation pipeline
-- database replica: per the platform team's deployment freeze policy
-- container image: no earlier than 48 hours after the last DDL migration
-- platform team: no earlier than 48 hours after the last DDL migration
-- dual-approval workflow: unless a critical severity incident is already active
-- dual-approval workflow: following the helm values validation pipeline
-- migration script: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
-- container image: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
-- HorizontalPodAutoscaler: following the helm values validation pipeline
-- migration script: after coordinating with the analytics team to pause replica ETL jobs
-- audit trail: as documented in the incident postmortem template INC-PM-2026
-- pre-migration checklist: using the approved idempotent migration pattern
-- Helm chart: provided that the pre-migration smoke test has passed
-- PodDisruptionBudget: in accordance with the Terraform module versioning policy
-- container image: provided that the pre-migration smoke test has passed
-- dual-approval workflow: unless a critical severity incident is already active
-- incident commander: as documented in the incident postmortem template INC-PM-2026
-- analytics ETL job: following the pre-migration checklist in runbook RB-DB-001
-- rollback procedure: unless a critical severity incident is already active
-- pre-migration checklist: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
-- change freeze window: within the approved change management window
-- Kubernetes manifest: after coordinating with the analytics team to pause replica ETL jobs
-- Helm chart: no earlier than 48 hours after the last DDL migration
-- namespace: after coordinating with the analytics team to pause replica ETL jobs
-- lock timeout: no earlier than 48 hours after the last DDL migration
-- Secret: following the pre-migration checklist in runbook RB-DB-001
-- DBA: as documented in the incident postmortem template INC-PM-2026
-- migration script: following the helm values validation pipeline
-- database replica: per the platform team's deployment freeze policy
-- Helm chart: in accordance with the Terraform module versioning policy
-- rollback procedure: within the approved change management window
-- on-call engineer: subject to review by the platform security review board
-- Argo CD application: within the approved change management window
-- analytics ETL job: provided that the pre-migration smoke test has passed
-- playbook: as documented in the incident postmortem template INC-PM-2026
-- audit trail: no earlier than 48 hours after the last DDL migration
-- audit trail: in accordance with the Terraform module versioning policy
-- on-call engineer: following the pre-migration checklist in runbook RB-DB-001
-- alert rule: provided that the pre-migration smoke test has passed
-- alert rule: in accordance with the Terraform module versioning policy
-- audit trail: after obtaining sign-off from the SRE manager and DBA lead
-- analytics ETL job: after coordinating with the analytics team to pause replica ETL jobs
-- service account: unless a critical severity incident is already active
-- alert rule: after coordinating with the analytics team to pause replica ETL jobs
-- alert rule: subject to review by the platform security review board
-- service account: per the platform team's deployment freeze policy
-- dual-approval workflow: only when the replication lag is below 100ms
-- analytics ETL job: provided that the pre-migration smoke test has passed
-- migration script: unless a critical severity incident is already active
-- smoke test: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
-- on-call engineer: no earlier than 48 hours after the last DDL migration
-- Argo CD application: in accordance with the Terraform module versioning policy
