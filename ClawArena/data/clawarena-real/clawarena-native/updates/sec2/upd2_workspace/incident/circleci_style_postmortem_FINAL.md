# NovaBridge Security Incident Postmortem — FINAL v2

**Status**: FINAL — Approved for distribution
**Classification**: CONFIDENTIAL
**Supersedes**: incident/circleci_style_postmortem.md (Draft v1)

---

## SUPERSEDE NOTICE
This document supersedes the draft postmortem with respect to:
- **CircleCI customer anomaly detection date**: corrected from 2022-12-25 to **2022-12-29**
  (2022-12-25 was an error in the draft; the authoritative date per CircleCI's official
  post-mortem is 2022-12-29)
- **CircleCI impact scope**: expanded from "internal systems only" to include
  external customers (corrects vendor_circleci_advisory.eml v1 claim)

---

## Executive Summary (Final)

On January 10, 2026, NovaBridge confirmed a three-key API credential leak:
1. OpenAI API key (openai_api_key, ACTIVE at time of detection)
2. AWS IAM access key (AKIA prefix, long-term credential)
3. Anthropic API key (anthropic_api_key, ACTIVE at time of detection)

All three keys have been revoked/disabled as of postmortem completion.

---

## CircleCI Incident Reference (Corrected)

Based on the official CircleCI January 2023 incident report
(https://circleci.com/blog/jan-4-2023-incident-report/):

- **Data exfiltration date**: 2022-12-22
- **Customer anomaly detection date**: **2022-12-29** ← CORRECTED (was erroneously 2022-12-25 in draft)
- **GitHub OAuth token rotation completed**: 2023-01-07T07:30:00Z
- **Malware artifact (SHA256)**: 8913e38592228adc067d82f66c150d87004ec946e579d4a00c53b61444ff35bf
- **Affected**: fewer than 5 customers reported unauthorized access to third-party systems
- **Attack vector**: session cookie theft via malware (PTX-Player.dmg) on engineer laptop

*The detection date of 2022-12-25 in the draft was a transcription error.
The correct date is 2022-12-29 per the official CircleCI post-mortem.*

---

## NovaBridge Incident Timeline (Final)

| Date | Event | Source |
|---|---|---|
| 2026-01-10T07:58:00Z | Huang Min commits credentials | git history |
| 2026-01-10T08:00:00Z | GitHub Push Protection triggers (openai_api_key, active) | alert_timeline.json |
| 2026-01-10T08:03:00Z | GitGuardian webhook fires, key confirmed active | webhook logs |
| 2026-01-10T08:05:00Z | External scan detected (185.234.219.44 → GetCallerIdentity) | CloudTrail |
| 2026-01-10T08:50:00Z | Anthropic key discovered (Update 1, webhook wh-051) | gitguardian_webhook_v2.json |
| 2026-01-10 | All 3 keys revoked/disabled | remediation log |

**Detection date**: 2026-01-10 (our incident)
**CircleCI reference detection date**: 2022-12-29 (corrected)

---

## Remediation Summary

1. OpenAI key revoked (GitHub SS alert updated: state=resolved, resolution=revoked)
2. AWS IAM key (AKIA) disabled via IAM, replaced with rotation
3. Anthropic key revoked (secret_type: anthropic_api_key)
4. AWS Config rule ACCESS_KEYS_ROTATED enforced (maxAccessKeyAge=90)
5. TruffleHog pre-commit hooks deployed

---

## Industry Benchmarks

- GitGuardian 2024: 2.6% of secrets revoked within 1 hour
- GitGuardian 2024: >90% of exposed secrets remain active 5 days post-detection
- GitGuardian 2024: 1212x surge in OpenAI key leaks in 2023
- GitHub 2024: 39 million secrets leaked; Push Protection precision = 75%
