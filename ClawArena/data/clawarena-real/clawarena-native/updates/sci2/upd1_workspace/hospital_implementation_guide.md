# Hospital Implementation Guide
## Fresenius Kabi Ivenix LVP Software Recall Z-0885-2026
## Version 2.0 — Revised Following FSN Update

**Distribution**: All affected facilities in CA, CO, FL, GA, ID, IL, MD, MI, MN, MS,
NE, NJ, NV, OK, OR, SC, TX, VA, WA, WI

---

## Phase 1: Immediate Assessment (Days 1-3)

### Step 1: Device Inventory
Locate all Ivenix LVP units in your facility. Check firmware version on each device.
Affected versions: **5.10.1 and earlier**.
Note: The recall affects software version 5.10.1 AND ALL PRIOR VERSIONS.
An earlier communication from one source said only "5.10.0" was affected — this was
INCORRECT. The correct scope is "5.10.1 and earlier".

### Step 2: Battery Health Assessment
For each affected device:
1. Navigate to Device Settings > Diagnostics > Battery Health
2. Record the battery health percentage
3. Flag all devices with battery health < 70%
4. Segregate flagged devices from clinical use immediately

### Step 3: Risk Stratification
| Battery Health | Risk Level | Action |
|---------------|------------|--------|
| < 70% | HIGH | Remove from service immediately; replace battery |
| 70%-85% | MEDIUM | Schedule update within 48 hours |
| > 85% | LOWER | Schedule update within 5 business days |

---

## Phase 2: Software Update (Days 3-14)

### Update Sequence
**IMPORTANT**: Always update IMS first, then LVP software.

1. **IMS Update** — Update Infusion Management Software to v5.2.2
   - Estimated time: 20-30 minutes per IMS workstation
   - Requires network downtime: No
   - Requires device connection: No (IMS update is server-side)

2. **LVP Software Update** — Update each pump to v5.10.2
   - Estimated time: 15-20 minutes per device
   - Requires device to be removed from active patient use
   - Verify completion: Check firmware version on device screen

3. **Battery Replacement** (if health < 70%)
   - Order replacement batteries using part number [contact Fresenius Kabi]
   - Installation requires trained biomedical engineering staff
   - Post-replacement: verify battery health > 70% before returning to service

---

## Phase 3: Verification and Documentation (Days 14-21)

### Post-Update Checklist
- [ ] All devices updated to v5.10.2
- [ ] IMS updated to v5.2.2
- [ ] All batteries with health < 70% replaced
- [ ] Post-update self-test run on all devices
- [ ] Staff re-education on dual-zero rate entry (historical awareness)
- [ ] Documentation of update completion submitted to Fresenius Kabi

### Adverse Event Reporting During Remediation
- Any patient harm events during the remediation period must be reported per 21 CFR 803.50(a)(1)
- Urgent events requiring immediate action: report per 21 CFR 803.53 (5 work days)
- Recall correction report already filed by Fresenius Kabi per 21 CFR 806.10

---

## Contact Information

**Fresenius Kabi Field Service**: 1-800-XXX-XXXX (24/7)
**Technical Support**: ivenix-support@fresenius-kabi.com
**FDA MedWatch Reporting**: https://www.fda.gov/safety/medwatch

**Recall Reference**: Z-0885-2026
**Product Code**: LVP-SW-0005
