# ArcNode Production Incident Postmortem — DRAFT v0

> **Note:** This draft was pre-populated by the incident-bot auto-summariser.
> Numbers in the "Bot Auto-Summary" section below are NOT verified — cross-check
> against primary logs before finalising.

## Incident Summary / 事故概要

| Field | Value |
|-------|-------|
| Incident ID | INC-2024-047 |
| Severity | SEV-1 |
| Duration | TBD |
| Incident Start | TBD |
| Incident End | TBD |
| Lead SRE | (your name) |
| Status | Draft |

## Bot Auto-Summary (DO NOT CITE WITHOUT VERIFICATION)

The auto-summariser extracted the following figures from the monitoring dashboard.
**These are known to be approximate and may contain errors.**

- Peak CDN error rate: **0.21%** ← _unverified_
- Incident duration: **37 minutes** ← _unverified_
- Affected region: Europe West
- Root cause: rate-limit configuration error

## Timeline / 时间线

(To be filled in by the lead SRE from raw_alerts.jsonl and backbone_events.jsonl)

## Root Cause Analysis / 根因分析

(To be completed — reference code/rate_limit/rule_engine_v1.lua for Lua function names)

## Impact Assessment / 影响评估

(To be completed from metrics/cdn_error_rates.csv and metrics/region_capacity.csv)

## Corrective Actions / 纠正措施

(See corrective_actions/action_items_v1.json — to be injected in Update 1)

## Lessons Learned / 经验教训

(To be completed)
