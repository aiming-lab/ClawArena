# Software Changelog — Ivenix LVP Software

## Version 5.10.2 (Corrective Release — November 2025)

### Bug Fixes
- **[CRITICAL]** Fixed battery state-of-charge algorithm to correctly account for
  battery impedance changes with aging. Battery health below 70%
  now triggers mandatory replacement alert.
- **[CRITICAL]** Fixed input validation for rate entries with leading zeros. Rate
  entry "0010" now correctly parses to 10.0 mL/hr without triggering fail-stop state.
- **[HIGH]** Improved battery alarm trigger logic: low-battery alarm now activates
  at 20% remaining capacity (previously deferred to 10% due to reporting error).

### Regulatory
- This release is required for all units running version 5.10.1 or earlier.
- Update required per FDA Class I Recall Z-0885-2026.
- Product Code: LVP-SW-0005

## Version 5.10.1 (Affected — Recalled)
- Battery state-of-charge reporting contains coulomb counting offset error.
- Leading-zero rate entry causes UI freeze in fail-stop state.
- **RECALL STATUS**: Covered by FDA Recall Z-0885-2026. Do not deploy.

## Version 5.10.0 (Prior Release — Superseded)
- Predecessor release. Also covered by the recall (version 5.10.1 and earlier).
- Note: Some early internal communications incorrectly referenced "5.10.0" as the
  sole affected version. The correct statement is "5.10.1 and earlier"
  which includes 5.10.0, 5.9.x, and all prior versions.

## Version 5.2.2 (IMS Companion Release)
- Companion Infusion Management Software update required alongside LVP v5.10.2.
- Addresses battery health monitoring integration between IMS and LVP.
