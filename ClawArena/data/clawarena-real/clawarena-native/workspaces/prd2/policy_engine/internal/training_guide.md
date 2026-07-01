# PolicyOps AI Training Guide — Platform Policy Reference

## Introduction

This training guide provides detailed worked examples for common policy scenarios across YouTube, Meta, TikTok, and Reddit. Engineers should review these examples when uncertain about appropriate enforcement tier selection.

## YouTube Scenarios

### Spam Example 1

**Scenario**: Creator uses clickbait thumbnail misrepresenting video content

**Enforcement Action**: Warning (first offense)

**Applicable Policy**: Misleading Metadata Policy

### Spam Example 2

**Scenario**: Creator purchases 50,000 fake views using bot service

**Enforcement Action**: Strike 1 (7-day freeze)

**Applicable Policy**: Fake Engagement Policy

### Hate Speech Example 1

**Scenario**: Video contains mild ethnic slur in context not targeting anyone

**Enforcement Action**: Warning; age restriction

**Applicable Policy**: Hate Speech Policy

### Hate Speech Example 2

**Scenario**: Channel dedicated to promoting ethnic hatred

**Enforcement Action**: Strike 1 or channel removal depending on severity

**Applicable Policy**: Hate Speech Policy

### CSAM Example

**Scenario**: Any content sexualizing minors

**Enforcement Action**: Immediate channel termination + NCMEC referral

**Applicable Policy**: Child Safety Policy

### Misinformation Example 1

**Scenario**: Health claim contradicting WHO guidance on vaccine safety

**Enforcement Action**: Warning; informational panel added

**Applicable Policy**: Medical Misinformation Policy

### Strike Escalation Example

**Scenario**: Creator receives Strike 1, then 10 days later Strike 2

**Enforcement Action**: Both within 90-day window; next violation triggers Strike 3 (channel removal)

**Applicable Policy**: Three-Strike Policy

### Appeal Example

**Scenario**: Creator appeals Strike 1 within 6 months

**Enforcement Action**: YouTube reviews; possible outcomes: reinstated/age-restricted/upheld

**Applicable Policy**: Appeal Procedures


## Meta Scenarios

### Strike 1 Example

**Scenario**: User posts mildly inflammatory content about political group

**Enforcement Action**: Warning (Strike 1) — no restrictions

**Applicable Policy**: Violence and Incitement (mild)

### Strike 7 Example

**Scenario**: User on seventh violation; posts harassment content

**Enforcement Action**: 1-day content creation ban

**Applicable Policy**: Bullying and Harassment

### Strike 8 Example

**Scenario**: User on eighth violation

**Enforcement Action**: 3-day content creation ban

**Applicable Policy**: Repeat violator

### Strike 10+ Example

**Scenario**: User on eleventh violation

**Enforcement Action**: 30-day content creation ban

**Applicable Policy**: Repeat violator

### CSAM Example

**Scenario**: Any content involving minors sexually

**Enforcement Action**: Immediate account termination + NCMEC referral

**Applicable Policy**: CSAM Policy

### Hate Speech Q3 2025

**Scenario**: Content removed for hate speech

**Enforcement Action**: Facebook precision >90%; Instagram >87%

**Applicable Policy**: Q3 2025 Enforcement Data


## TikTok Scenarios

### Strike 1 Example

**Scenario**: Video contains mild violence or graphic content

**Enforcement Action**: Video removed; Strike 1 added (expires 90 days from issuance)

**Applicable Policy**: Sensitive/Mature Content

### Strike 3 Example

**Scenario**: Creator accumulates 3 strikes within 90-day window

**Enforcement Action**: Permanent account ban

**Applicable Policy**: Three-Strike Policy

### Permanent Ban Without Strikes

**Scenario**: Creator posts CSAM

**Enforcement Action**: Immediate permanent ban regardless of prior strikes

**Applicable Policy**: CSAM Policy

### Appeal Example

**Scenario**: Creator appeals video removal

**Enforcement Action**: Creator taps Appeal in notification; safety team reviews; successful appeal reinstates content and removes penalty

**Applicable Policy**: Appeal Process

### Q1 2025 Scale

**Scenario**: 211 million videos removed in one quarter

**Enforcement Action**: 87.4% by automated systems; 99.0% before user reports

**Applicable Policy**: Q1 2025 Transparency Report


## Reddit Scenarios

### Tier 1 Example

**Scenario**: User posts mildly rule-violating comment (first offense)

**Enforcement Action**: Warning (Tier 1) — no suspension

**Applicable Policy**: Site Rules — minor violation

### Tier 2 Example

**Scenario**: User engages in vote manipulation

**Enforcement Action**: 3-day suspension

**Applicable Policy**: Rule 2 — Content Manipulation

### Tier 3 Example

**Scenario**: User repeatedly harasses specific individual

**Enforcement Action**: 7-day suspension

**Applicable Policy**: Rule 1/Rule 6 — Harassment

### Tier 4 Example

**Scenario**: User posts CSAM

**Enforcement Action**: Immediate permanent ban + NCMEC referral

**Applicable Policy**: Rule 4 — CSAM

### Appeal within Window

**Scenario**: User appeals 3-day suspension within 6 months

**Enforcement Action**: Reddit reviews appeal; H1 2025 harassment reversal rate: 40.7%

**Applicable Policy**: Appeal Process

### Appeal Out of Window

**Scenario**: User attempts appeal after 6 months

**Enforcement Action**: Appeal rejected — outside the 6-month window

**Applicable Policy**: Appeal Process


## Common Mistakes Checklist

| Field | Wrong Value | Correct Value | Source |
|---|---|---|---|
| YouTube appeal window | 3 months | 6 months | [link](https://support.google.com/youtube/answer/185111?hl=en) |
| Meta Strike 7 duration | 3 days | 1 day | [link](https://transparency.meta.com/enforcement/taking-action/restricting-accounts/) |
| TikTok permanent ban threshold | 2 strikes | 3 strikes | [link](https://support.tiktok.com/en/safety-hc/account-and-user-safety/content-violations-and-bans) |
| Reddit appeal window | 3 months | 6 months | [link](https://support.reddithelp.com/hc/en-us/articles/23511059871252) |
| Reddit Tier 2 suspension | 7 days | 3 days | [link](https://ag.ny.gov/sites/default/files/social-media-policy-report/2025-q3-reddit-inc-policy.pdf) |
