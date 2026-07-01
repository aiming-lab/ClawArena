-- V0234__add_idempotency_keys.sql
-- Author: priya.nair@mercatorrobotics.com
-- Date: 2026-05-12
-- Phase 1: Add column to payment_events
-- Phase 2: Add column to payments
-- Phase 3: Backfill idempotency_keys on billing_transactions (12M rows)
-- NOTE: This script does NOT set LOCK TIMEOUT — this was identified post-incident
--       as the root cause of the migration failure on 2026-05-12.

BEGIN;

-- Phase 1: payment_events
ALTER TABLE payment_events
  ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(256);

-- Phase 2: payments
ALTER TABLE payments
  ADD COLUMN IF NOT EXISTS billing_idempotency_key VARCHAR(256);

-- Phase 3: backfill idempotency_keys on billing_transactions (12M rows)
-- WARNING: This phase ran without LOCK TIMEOUT and was blocked by the
-- analytics ETL job holding a ShareRowExclusiveLock on billing_transactions.
UPDATE billing_transactions
  SET idempotency_key = md5(id::text || created_at::text)
  WHERE idempotency_key IS NULL;

COMMIT;
