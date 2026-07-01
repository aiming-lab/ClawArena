# IR Team Contacts — SEC-2026-0419

**Primary IR Lead** : Jordan Park  jordan.park@corp.internal  ext. 4521
**Secondary** : Sam Rivera   sam.rivera@corp.internal    ext. 4522
**Legal counsel** : Alex Morgan  alex.morgan@corp.legal     ext. 3310
**CISO notification** : ciso@corp.internal (auto-notified on CRITICAL decisions)

## Escalation SLA

- HIGH severity   → IR lead paged within 30 minutes of detection
- CRITICAL        → CISO + Legal notified within 15 minutes

## Escalation procedure

1. Analyst completes findings/ and audit/escalation.json
2. Decision field must be one of: monitor / contain / escalate_to_IR
3. Run tools/generate_token.sh (in runbooks/) to produce compliance token
4. Email IR lead with incident ID and JSON attachment
