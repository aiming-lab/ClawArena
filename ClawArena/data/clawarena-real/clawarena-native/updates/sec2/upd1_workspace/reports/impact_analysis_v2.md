# Impact Analysis — v2 (Update 1)

**Date**: 2026-01-10
**Prepared by**: Li Wei
**Status**: CURRENT — SUPERSEDES impact_analysis_v1.md

## SUPERSEDE NOTICE
This document supersedes impact_analysis_v1.md with respect to:
- **affected_keys_count**: updated from 2 to 3
- **affected_services**: added Anthropic (Claude API)

## Affected Keys

| Key Type | Service | Status | Key Prefix / Type |
|---|---|---|---|
| OpenAI API Key | OpenAI API | Active (not yet revoked) | sk-proj- |
| AWS Access Key | AWS S3, IAM | Active (not yet revoked) | AKIA |
| Anthropic API Key | Anthropic Claude API | Active (not yet revoked) | sk-ant- |

**affected_keys_count: 3**
**superseded_fields**: ["affected_keys_count", "affected_services"]

## Affected Services

- openai (text generation, summarization)
- aws (S3 data storage, IAM identity)
- anthropic (LLM inference via Claude API)

## Evidence Sources
- Primary: incident/alert_timeline.json (alerts #1, #2)
- Update 1: incident/gitguardian_webhook_v2.json (webhook wh-051: anthropic_api_key, active)
- Confirms: Huang Min's revocation claim was false (wh-052: OpenAI key still active)
