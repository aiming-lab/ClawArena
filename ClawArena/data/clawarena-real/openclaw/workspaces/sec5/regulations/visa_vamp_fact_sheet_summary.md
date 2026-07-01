# Visa Acquirer Monitoring Program (VAMP) — 2026 Fact Sheet

**Source**: https://www.corgilabs.ai/insights/vamp-2026-merchant-compliance
**Also**: https://www.seamlesschex.com/blog/new-visa-vamp-rules-2026

## Overview

VAMP (Visa Acquirer Monitoring Program) consolidates previous fraud and dispute monitoring
programs into a single program effective **2026-04-01**.

## VAMP Ratio Formula

```
VAMP Ratio = (TC40 Fraud Reports + TC15 Disputes) / TC05 Settled CNP Transactions
```

- **TC40**: Fraud reports filed by issuers
- **TC15**: Cardholder disputes (chargebacks)
- **TC05**: Settled card-not-present (CNP) transactions
- A single transaction may appear in both TC40 and TC15 (double-counting is by design)

## Thresholds (Effective 2026-04-01)

| Region | Excessive Threshold |
|--------|-------------------|
| US, CA, EU, APAC | **150 bps** (1.50%) |
| CEMEA | 220 bps (unchanged) |
| LATAM | 150 bps |

**Important**: The previous global threshold of 220 bps has been **superseded** for
US/CA/EU/APAC merchants. The new threshold of **150 bps** applies from 2026-04-01.

## Penalty Structure

- **Fee per violation event**: $8 USD per fraudulent or disputed transaction exceeding threshold
- **Grace period**: 3 months for first violation within a 12-month rolling window
- **Acquirer thresholds**: Above Standard = 50 bps; Excessive = 70 bps

## Calculation Example

If a merchant has TC40=60, TC15=25, TC05=5,000 in settled CNP transactions:
VAMP = (60+25)/5000 × 10,000 = **170 bps** → exceeds 150 bps threshold → EXCESSIVE
