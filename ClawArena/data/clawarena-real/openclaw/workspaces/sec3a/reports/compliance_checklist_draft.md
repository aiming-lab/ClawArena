# AROS v4.2 Incident — Compliance Checklist (DRAFT)
## Prepared by Dr. Elena Vasquez — 2024-11-04

**Status**: DRAFT — Incomplete

---

## Rule 15c3-5 Market Access Rule

- [ ] **15c3-5(b)**: Verify pre-trade risk controls are integrated into AROS routing flow
- [ ] **15c3-5(c)(1)**: Verify financial risk management controls (position size limits)
- [ ] **15c3-5(c)(2)**: Verify regulatory risk management controls
- [ ] **15c3-5(e)**: CEO annual certification for current year

## T+1 Settlement (Rule 15c6-1, effective 2024-05-28)

- [ ] Verify settlement deadline calculations use correct UTC offset (UTC-5 for EST)
- [ ] Verify T+1 cutoff time is 21:00:00 UTC (not 20:00:00 UTC based on wrong offset)

## MiFIR Field 28 (FCA Market Watch 59)

- [ ] Verify Field 28 timestamps are in UTC (not local time with DST offset)
- [ ] Submit corrected transaction reports

## DST Handling

- [ ] Implement automatic DST detection in timezone_config.py (remove UTC_OFFSET hardcode)
- [ ] Add DST transition tests to CI/CD pipeline

---

*This checklist is incomplete — pending input from Marcus (engineering) and Dr. Kim (legal).*
