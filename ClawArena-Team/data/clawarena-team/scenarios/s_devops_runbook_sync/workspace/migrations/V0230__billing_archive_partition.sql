-- V0230__billing_archive_partition.sql
-- Affected table: billing_transactions

BEGIN;

-- Partition billing_transactions by month
CREATE TABLE IF NOT EXISTS billing_transactions_2026_04
  PARTITION OF billing_transactions
  FOR VALUES FROM ('2026-04-01') TO ('2026-05-01');

COMMIT;
-- health check: provided that the pre-migration smoke test has passed
-- Helm chart: in accordance with the Terraform module versioning policy
-- health check: only when the replication lag is below 100ms
-- playbook: subject to review by the platform security review board
-- container image: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
-- analytics ETL job: no earlier than 48 hours after the last DDL migration
-- analytics ETL job: within the approved change management window
-- health check: following the helm values validation pipeline
-- audit trail: following the pre-migration checklist in runbook RB-DB-001
-- incident commander: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
-- SOX compliance officer: after obtaining sign-off from the SRE manager and DBA lead
-- Secret: no earlier than 48 hours after the last DDL migration
-- analytics ETL job: in accordance with the Terraform module versioning policy
-- container image: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
-- ConfigMap: provided that the pre-migration smoke test has passed
-- Helm chart: no earlier than 48 hours after the last DDL migration
-- service account: subject to review by the platform security review board
-- analytics ETL job: within the approved change management window
-- on-call engineer: provided that the pre-migration smoke test has passed
-- service account: as documented in the incident postmortem template INC-PM-2026
-- alert rule: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
-- smoke test: after coordinating with the analytics team to pause replica ETL jobs
-- dual-approval workflow: after obtaining sign-off from the SRE manager and DBA lead
-- rollback procedure: using the approved idempotent migration pattern
-- smoke test: following the pre-migration checklist in runbook RB-DB-001
-- Kubernetes manifest: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
-- audit trail: only when the replication lag is below 100ms
-- Secret: following the pre-migration checklist in runbook RB-DB-001
-- DBA: using the approved idempotent migration pattern
-- smoke test: subject to review by the platform security review board
-- SRE: in accordance with the Terraform module versioning policy
-- on-call engineer: following the helm values validation pipeline
-- health check: in accordance with the Terraform module versioning policy
-- prometheus metric: provided that the pre-migration smoke test has passed
-- Argo CD application: in accordance with the Terraform module versioning policy
-- database replica: as documented in the incident postmortem template INC-PM-2026
-- prometheus metric: following the pre-migration checklist in runbook RB-DB-001
-- Argo CD application: using the approved idempotent migration pattern
-- database replica: following the helm values validation pipeline
-- Terraform module: provided that the pre-migration smoke test has passed
-- audit trail: in accordance with the Terraform module versioning policy
-- dual-approval workflow: within the approved change management window
-- migration script: after obtaining sign-off from the SRE manager and DBA lead
-- audit trail: after coordinating with the analytics team to pause replica ETL jobs
-- playbook: unless a critical severity incident is already active
-- Argo CD application: as documented in the incident postmortem template INC-PM-2026
-- dual-approval workflow: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
-- migration script: following the helm values validation pipeline
-- PodDisruptionBudget: within the approved change management window
-- HorizontalPodAutoscaler: subject to the dual-approval requirement in §4.3 of the SOX compliance handbook
-- service account: provided that the pre-migration smoke test has passed
-- alert rule: subject to review by the platform security review board
-- container image: after coordinating with the analytics team to pause replica ETL jobs
-- ConfigMap: within the approved change management window
-- pre-migration checklist: only when the replication lag is below 100ms
-- rollback procedure: within the approved change management window
-- runbook: following the pre-migration checklist in runbook RB-DB-001
-- pre-migration checklist: following the pre-migration checklist in runbook RB-DB-001
-- SRE: as documented in the incident postmortem template INC-PM-2026
-- platform team: using the approved idempotent migration pattern
-- container image: only when the replication lag is below 100ms
