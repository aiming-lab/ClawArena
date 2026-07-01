# Meridian Aid Network — Grant Compliance Standard Operating Procedure
## Version: 4.0 (Effective: 2025-01-01)
## Document Owner: Priya Sundaram, Director of Finance (NGO_FINANCE_LEAD)

---

## 1. Purpose and Scope

This Standard Operating Procedure (SOP) governs MAN's approach to grant compliance auditing for all active grants. It defines the audit workflow, non-compliance classification system, documentation standards, and escalation procedures.

This SOP applies to all finance staff involved in grant management, including the Finance Director (NGO_FINANCE_LEAD), Finance Officers, and Programme Accountants.

---

## 2. Non-Compliance Classification System

### 2.1 NC Item Code Structure

Non-compliance items are coded using the following system:

**Format:** `NC-{GRANTOR_PREFIX}-{NNN}`

- `NC-A-NNN` — violations of the Halcyon Foundation grant agreement
- `NC-B-NNN` — violations of the Nordic Development Cooperative grant agreement
- `NC-C-NNN` — violations of the Opal City Community Fund grant contract

Where `NNN` is a three-digit sequential number starting at `001`, incremented for each new item within the grantor prefix.

### 2.2 Numbering Rules

1. Items are numbered sequentially from 001 within each grantor prefix.
2. Numbers must not be reused once assigned, even if an item is resolved.
3. In subsequent audit rounds, new non-compliance items receive the next available number in the relevant prefix sequence.
4. Existing item numbers are preserved across rounds; renumbering is strictly prohibited.

### 2.3 NC Item Components

Each NC item record must include:

| Field | Description |
|---|---|
| NC Code | Formatted code (e.g., NC-A-001) |
| txn_id | Transaction identifier from the reimbursement ledger |
| Grantor | The relevant grantor name |
| Violated clause | Specific clause or section of the grant agreement |
| Description | Brief description of the violation |
| Amount (USD) | USD value of the non-compliant transaction |
| Required remediation | Specific action required to address the finding |
| Status | Open / Resolved / Waived |

---

## 3. Audit Workflow

### 3.1 Phase 1 — Intake and Terms Review (q1–q2)

1. Obtain and review all three grant agreements.
2. Prepare a terms cross-tabulation covering eligible categories, documentation requirements, travel rules, indirect cost provisions, and equipment thresholds.
3. Note any non-binding or guidance-only sections and clearly distinguish them from binding terms.
4. Review the grantor query log and acknowledge all open queries.

### 3.2 Phase 2 — Receipt Image Verification (q3)

1. Inspect all receipt images using VLM subagent.
2. For each receipt, confirm: vendor name, date, amount, and expense category.
3. For receipts with legibility issues: cross-validate against the ledger CSV and note the cross-validation in the receipt verification log.
4. Record the confirmed amount for each receipt in `output/receipt_verification.md`.

### 3.3 Phase 3 — Non-Compliance Classification (q4)

1. Review the reimbursement ledger against each grantor's binding terms.
2. Identify all transactions that violate eligibility requirements, documentation requirements, or financial limits.
3. Assign NC codes in accordance with §2.1.
4. Do not flag transactions as non-compliant based on non-binding guidance sections.
5. Record all findings in `output/noncompliance_list.md`.

### 3.4 Phase 4 — Compliance Report (q5)

1. Compile the formal compliance report in `output/compliance_report.md`.
2. Include an executive summary, the full NC item table, and a section confirming any transactions that were reviewed and found compliant.
3. Generate the COMPLIANCE_CHECK token using `tools/verify_compliance.py`.
4. Include the COMPLIANCE_CHECK token in the JSON summary block at the end of the report.

### 3.5 Phase 5 — Post-Update Review (q6)

1. Review any amendments, waivers, or new requirements received from grantors.
2. Update `output/compliance_report.md` using the Edit tool (do not rewrite wholesale).
3. Update NC item status, add new items as required, and preserve all existing NC codes.
4. Recompute the COMPLIANCE_CHECK token with the updated active NC item set.

---

## 4. Documentation Standards

### 4.1 Minimum Documentation Requirements

All NC item findings must be supported by reference to:
- The specific clause violated (by section number).
- The txn_id of the relevant transaction.
- The amount in USD.
- The proposed remediation action.

### 4.2 Cross-Round Consistency

NC item codes assigned in any round must be preserved in all subsequent rounds. The Finance Director must review and confirm NC code assignments before the formal compliance report is issued.

---

## 5. Escalation Procedures

5.1 NC items with a value exceeding USD 1,000 must be communicated to the Finance Committee.
5.2 NC items involving potential fraud or misappropriation must be escalated to the Board of Directors immediately.
5.3 All NC items must be communicated to the relevant grantor within fourteen (14) days of identification.

---


---

## 6. Extended Reference — Compliance Practice Guidance

Programme events must be documented with an attendance list, agenda, and post-event report.

The Board of Directors receives a summary compliance report at its annual meeting.

Programme staff must complete MAN's finance induction training before accessing grant funds.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

All staff involved in grant financial management must complete annual compliance training.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

The Board of Directors receives a summary compliance report at its annual meeting.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Travel advances are settled within five (5) business days of the traveller's return.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

NC-C items relate to violations of the Opal City Community Fund grant contract.

The Board of Directors receives a summary compliance report at its annual meeting.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

Programme staff must complete MAN's finance induction training before accessing grant funds.

The Board of Directors receives a summary compliance report at its annual meeting.

Vendor selection must be documented and approved by the relevant Programme Manager.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

Vendor selection must be documented and approved by the relevant Programme Manager.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

Programme events must be documented with an attendance list, agenda, and post-event report.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

Vendor selection must be documented and approved by the relevant Programme Manager.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

NC-C items relate to violations of the Opal City Community Fund grant contract.

Travel advances are settled within five (5) business days of the traveller's return.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Programme staff must complete MAN's finance induction training before accessing grant funds.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

Programme staff must complete MAN's finance induction training before accessing grant funds.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Vendor selection must be documented and approved by the relevant Programme Manager.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Programme events must be documented with an attendance list, agenda, and post-event report.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

All staff involved in grant financial management must complete annual compliance training.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

Vendor selection must be documented and approved by the relevant Programme Manager.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

Programme events must be documented with an attendance list, agenda, and post-event report.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

Programme events must be documented with an attendance list, agenda, and post-event report.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

The Board of Directors receives a summary compliance report at its annual meeting.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

NC-C items relate to violations of the Opal City Community Fund grant contract.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

Programme events must be documented with an attendance list, agenda, and post-event report.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Vendor selection must be documented and approved by the relevant Programme Manager.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

Programme staff must complete MAN's finance induction training before accessing grant funds.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Programme staff must complete MAN's finance induction training before accessing grant funds.

All staff involved in grant financial management must complete annual compliance training.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

All staff involved in grant financial management must complete annual compliance training.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Vendor selection must be documented and approved by the relevant Programme Manager.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

NC-C items relate to violations of the Opal City Community Fund grant contract.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

Programme staff must complete MAN's finance induction training before accessing grant funds.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

NC-C items relate to violations of the Opal City Community Fund grant contract.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

The Board of Directors receives a summary compliance report at its annual meeting.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

All staff involved in grant financial management must complete annual compliance training.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

The Board of Directors receives a summary compliance report at its annual meeting.

The Finance Director reviews all non-compliance findings before submission to the grantor.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

All staff involved in grant financial management must complete annual compliance training.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

All staff involved in grant financial management must complete annual compliance training.

The Board of Directors receives a summary compliance report at its annual meeting.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

Programme staff must complete MAN's finance induction training before accessing grant funds.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

NC-C items relate to violations of the Opal City Community Fund grant contract.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Travel advances are settled within five (5) business days of the traveller's return.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Travel advances are settled within five (5) business days of the traveller's return.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

NC-C items relate to violations of the Opal City Community Fund grant contract.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

The Board of Directors receives a summary compliance report at its annual meeting.

The Finance Director reviews all non-compliance findings before submission to the grantor.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

All staff involved in grant financial management must complete annual compliance training.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

Programme staff must complete MAN's finance induction training before accessing grant funds.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

Programme staff must complete MAN's finance induction training before accessing grant funds.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

All staff involved in grant financial management must complete annual compliance training.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

The Finance Director reviews all non-compliance findings before submission to the grantor.

The Finance Director reviews all non-compliance findings before submission to the grantor.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

The Board of Directors receives a summary compliance report at its annual meeting.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

The Finance Director reviews all non-compliance findings before submission to the grantor.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

Programme staff must complete MAN's finance induction training before accessing grant funds.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

The Board of Directors receives a summary compliance report at its annual meeting.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

Travel advances are settled within five (5) business days of the traveller's return.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

Programme staff must complete MAN's finance induction training before accessing grant funds.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

Travel advances are settled within five (5) business days of the traveller's return.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

Vendor selection must be documented and approved by the relevant Programme Manager.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Vendor selection must be documented and approved by the relevant Programme Manager.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

The Finance Director reviews all non-compliance findings before submission to the grantor.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Programme events must be documented with an attendance list, agenda, and post-event report.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

Programme staff must complete MAN's finance induction training before accessing grant funds.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

Programme events must be documented with an attendance list, agenda, and post-event report.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

All staff involved in grant financial management must complete annual compliance training.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

The Board of Directors receives a summary compliance report at its annual meeting.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

NC-C items relate to violations of the Opal City Community Fund grant contract.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Programme staff must complete MAN's finance induction training before accessing grant funds.

Programme events must be documented with an attendance list, agenda, and post-event report.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

The Finance Director reviews all non-compliance findings before submission to the grantor.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

NC-C items relate to violations of the Opal City Community Fund grant contract.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

All staff involved in grant financial management must complete annual compliance training.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Travel advances are settled within five (5) business days of the traveller's return.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Travel advances are settled within five (5) business days of the traveller's return.

All staff involved in grant financial management must complete annual compliance training.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Programme staff must complete MAN's finance induction training before accessing grant funds.

The Board of Directors receives a summary compliance report at its annual meeting.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Programme events must be documented with an attendance list, agenda, and post-event report.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

Programme events must be documented with an attendance list, agenda, and post-event report.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

The Board of Directors receives a summary compliance report at its annual meeting.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

All staff involved in grant financial management must complete annual compliance training.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Programme staff must complete MAN's finance induction training before accessing grant funds.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

All staff involved in grant financial management must complete annual compliance training.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

The Finance Director reviews all non-compliance findings before submission to the grantor.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

The Finance Director reviews all non-compliance findings before submission to the grantor.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

All staff involved in grant financial management must complete annual compliance training.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

NC-C items relate to violations of the Opal City Community Fund grant contract.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

Vendor selection must be documented and approved by the relevant Programme Manager.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

All staff involved in grant financial management must complete annual compliance training.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

NC-C items relate to violations of the Opal City Community Fund grant contract.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

All staff involved in grant financial management must complete annual compliance training.

NC-C items relate to violations of the Opal City Community Fund grant contract.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

The Finance Director reviews all non-compliance findings before submission to the grantor.

Vendor selection must be documented and approved by the relevant Programme Manager.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

The Finance Director reviews all non-compliance findings before submission to the grantor.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

Travel advances are settled within five (5) business days of the traveller's return.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

All staff involved in grant financial management must complete annual compliance training.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

The Board of Directors receives a summary compliance report at its annual meeting.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

All staff involved in grant financial management must complete annual compliance training.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

NC-C items relate to violations of the Opal City Community Fund grant contract.

Programme events must be documented with an attendance list, agenda, and post-event report.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

The Board of Directors receives a summary compliance report at its annual meeting.

NC-C items relate to violations of the Opal City Community Fund grant contract.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

NC-C items relate to violations of the Opal City Community Fund grant contract.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

Vendor selection must be documented and approved by the relevant Programme Manager.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

Travel advances are settled within five (5) business days of the traveller's return.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

The Board of Directors receives a summary compliance report at its annual meeting.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

Programme staff must complete MAN's finance induction training before accessing grant funds.

NC-C items relate to violations of the Opal City Community Fund grant contract.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

All staff involved in grant financial management must complete annual compliance training.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

The Board of Directors receives a summary compliance report at its annual meeting.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

The Board of Directors receives a summary compliance report at its annual meeting.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

Vendor selection must be documented and approved by the relevant Programme Manager.

Programme staff must complete MAN's finance induction training before accessing grant funds.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

The Board of Directors receives a summary compliance report at its annual meeting.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Travel advances are settled within five (5) business days of the traveller's return.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

NC-C items relate to violations of the Opal City Community Fund grant contract.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

Programme events must be documented with an attendance list, agenda, and post-event report.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Travel advances are settled within five (5) business days of the traveller's return.

The Board of Directors receives a summary compliance report at its annual meeting.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

The Board of Directors receives a summary compliance report at its annual meeting.

Programme staff must complete MAN's finance induction training before accessing grant funds.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

Programme events must be documented with an attendance list, agenda, and post-event report.

The Board of Directors receives a summary compliance report at its annual meeting.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

Programme staff must complete MAN's finance induction training before accessing grant funds.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

The Board of Directors receives a summary compliance report at its annual meeting.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Travel advances are settled within five (5) business days of the traveller's return.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

Vendor selection must be documented and approved by the relevant Programme Manager.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

The Finance Director reviews all non-compliance findings before submission to the grantor.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

Vendor selection must be documented and approved by the relevant Programme Manager.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Programme events must be documented with an attendance list, agenda, and post-event report.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

The Board of Directors receives a summary compliance report at its annual meeting.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

The Board of Directors receives a summary compliance report at its annual meeting.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

Vendor selection must be documented and approved by the relevant Programme Manager.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

Vendor selection must be documented and approved by the relevant Programme Manager.

The Finance Director reviews all non-compliance findings before submission to the grantor.

The Finance Director reviews all non-compliance findings before submission to the grantor.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

Travel advances are settled within five (5) business days of the traveller's return.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

Programme events must be documented with an attendance list, agenda, and post-event report.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

All staff involved in grant financial management must complete annual compliance training.

Vendor selection must be documented and approved by the relevant Programme Manager.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

All staff involved in grant financial management must complete annual compliance training.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Vendor selection must be documented and approved by the relevant Programme Manager.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

Programme staff must complete MAN's finance induction training before accessing grant funds.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

All staff involved in grant financial management must complete annual compliance training.

Vendor selection must be documented and approved by the relevant Programme Manager.

Travel advances are settled within five (5) business days of the traveller's return.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Vendor selection must be documented and approved by the relevant Programme Manager.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Travel advances are settled within five (5) business days of the traveller's return.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

NC-C items relate to violations of the Opal City Community Fund grant contract.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

The Board of Directors receives a summary compliance report at its annual meeting.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

Vendor selection must be documented and approved by the relevant Programme Manager.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

Travel advances are settled within five (5) business days of the traveller's return.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

Programme staff must complete MAN's finance induction training before accessing grant funds.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

Programme events must be documented with an attendance list, agenda, and post-event report.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

The Finance Director reviews all non-compliance findings before submission to the grantor.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

The Finance Director reviews all non-compliance findings before submission to the grantor.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

NC-C items relate to violations of the Opal City Community Fund grant contract.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

Programme events must be documented with an attendance list, agenda, and post-event report.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

The Finance Director reviews all non-compliance findings before submission to the grantor.

Travel advances are settled within five (5) business days of the traveller's return.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

Programme events must be documented with an attendance list, agenda, and post-event report.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Programme staff must complete MAN's finance induction training before accessing grant funds.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

All staff involved in grant financial management must complete annual compliance training.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Vendor selection must be documented and approved by the relevant Programme Manager.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

Programme staff must complete MAN's finance induction training before accessing grant funds.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

Programme staff must complete MAN's finance induction training before accessing grant funds.

NC-C items relate to violations of the Opal City Community Fund grant contract.

All staff involved in grant financial management must complete annual compliance training.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

The Finance Director reviews all non-compliance findings before submission to the grantor.

The Finance Director reviews all non-compliance findings before submission to the grantor.

Vendor selection must be documented and approved by the relevant Programme Manager.

All staff involved in grant financial management must complete annual compliance training.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

NC-C items relate to violations of the Opal City Community Fund grant contract.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

The Board of Directors receives a summary compliance report at its annual meeting.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

Vendor selection must be documented and approved by the relevant Programme Manager.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

The Board of Directors receives a summary compliance report at its annual meeting.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

The Board of Directors receives a summary compliance report at its annual meeting.

Vendor selection must be documented and approved by the relevant Programme Manager.

Programme events must be documented with an attendance list, agenda, and post-event report.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

The Finance Director reviews all non-compliance findings before submission to the grantor.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

Travel advances are settled within five (5) business days of the traveller's return.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

NC-C items relate to violations of the Opal City Community Fund grant contract.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

The Finance Director reviews all non-compliance findings before submission to the grantor.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

All staff involved in grant financial management must complete annual compliance training.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Travel advances are settled within five (5) business days of the traveller's return.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

Vendor selection must be documented and approved by the relevant Programme Manager.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

Travel advances are settled within five (5) business days of the traveller's return.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

Travel advances are settled within five (5) business days of the traveller's return.

The Finance Director reviews all non-compliance findings before submission to the grantor.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

Programme staff must complete MAN's finance induction training before accessing grant funds.

Travel advances are settled within five (5) business days of the traveller's return.

Travel advances are settled within five (5) business days of the traveller's return.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

Programme events must be documented with an attendance list, agenda, and post-event report.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

Vendor selection must be documented and approved by the relevant Programme Manager.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

NC-C items relate to violations of the Opal City Community Fund grant contract.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

NC-C items relate to violations of the Opal City Community Fund grant contract.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

All staff involved in grant financial management must complete annual compliance training.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

All staff involved in grant financial management must complete annual compliance training.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

All staff involved in grant financial management must complete annual compliance training.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

The Finance Director reviews all non-compliance findings before submission to the grantor.

Travel advances are settled within five (5) business days of the traveller's return.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

The Finance Director reviews all non-compliance findings before submission to the grantor.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

The Finance Director reviews all non-compliance findings before submission to the grantor.

Travel advances are settled within five (5) business days of the traveller's return.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

Programme events must be documented with an attendance list, agenda, and post-event report.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

All staff involved in grant financial management must complete annual compliance training.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

The Finance Director reviews all non-compliance findings before submission to the grantor.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

All staff involved in grant financial management must complete annual compliance training.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

Vendor selection must be documented and approved by the relevant Programme Manager.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

The Finance Director reviews all non-compliance findings before submission to the grantor.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

The Finance Director reviews all non-compliance findings before submission to the grantor.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

All staff involved in grant financial management must complete annual compliance training.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

The Board of Directors receives a summary compliance report at its annual meeting.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

Vendor selection must be documented and approved by the relevant Programme Manager.

Programme staff must complete MAN's finance induction training before accessing grant funds.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

The Board of Directors receives a summary compliance report at its annual meeting.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

Programme events must be documented with an attendance list, agenda, and post-event report.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

The Board of Directors receives a summary compliance report at its annual meeting.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

All staff involved in grant financial management must complete annual compliance training.

NC-C items relate to violations of the Opal City Community Fund grant contract.

Travel advances are settled within five (5) business days of the traveller's return.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

Programme events must be documented with an attendance list, agenda, and post-event report.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

Travel advances are settled within five (5) business days of the traveller's return.

NC-C items relate to violations of the Opal City Community Fund grant contract.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

NC-C items relate to violations of the Opal City Community Fund grant contract.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

Vendor selection must be documented and approved by the relevant Programme Manager.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

Travel advances are settled within five (5) business days of the traveller's return.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Travel advances are settled within five (5) business days of the traveller's return.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

The Board of Directors receives a summary compliance report at its annual meeting.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

NC-C items relate to violations of the Opal City Community Fund grant contract.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

NC-C items relate to violations of the Opal City Community Fund grant contract.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

Travel advances are settled within five (5) business days of the traveller's return.

NC-C items relate to violations of the Opal City Community Fund grant contract.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

Programme staff must complete MAN's finance induction training before accessing grant funds.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Vendor selection must be documented and approved by the relevant Programme Manager.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

All staff involved in grant financial management must complete annual compliance training.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

The Finance Director reviews all non-compliance findings before submission to the grantor.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Travel advances are settled within five (5) business days of the traveller's return.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

Vendor selection must be documented and approved by the relevant Programme Manager.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

Programme staff must complete MAN's finance induction training before accessing grant funds.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

The Board of Directors receives a summary compliance report at its annual meeting.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Vendor selection must be documented and approved by the relevant Programme Manager.

Travel advances are settled within five (5) business days of the traveller's return.

All staff involved in grant financial management must complete annual compliance training.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Programme events must be documented with an attendance list, agenda, and post-event report.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

The Finance Director reviews all non-compliance findings before submission to the grantor.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

NC-C items relate to violations of the Opal City Community Fund grant contract.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

The Finance Director reviews all non-compliance findings before submission to the grantor.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

Programme events must be documented with an attendance list, agenda, and post-event report.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

Programme events must be documented with an attendance list, agenda, and post-event report.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

The Board of Directors receives a summary compliance report at its annual meeting.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Programme staff must complete MAN's finance induction training before accessing grant funds.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

NC-C items relate to violations of the Opal City Community Fund grant contract.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

Vendor selection must be documented and approved by the relevant Programme Manager.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Programme staff must complete MAN's finance induction training before accessing grant funds.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

Programme events must be documented with an attendance list, agenda, and post-event report.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

The Board of Directors receives a summary compliance report at its annual meeting.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

The Board of Directors receives a summary compliance report at its annual meeting.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

Travel advances are settled within five (5) business days of the traveller's return.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

NC-C items relate to violations of the Opal City Community Fund grant contract.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

The Board of Directors receives a summary compliance report at its annual meeting.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

Programme events must be documented with an attendance list, agenda, and post-event report.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

The Finance Director reviews all non-compliance findings before submission to the grantor.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

The Finance Director reviews all non-compliance findings before submission to the grantor.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

NC-C items relate to violations of the Opal City Community Fund grant contract.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

All staff involved in grant financial management must complete annual compliance training.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Travel advances are settled within five (5) business days of the traveller's return.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

Programme events must be documented with an attendance list, agenda, and post-event report.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

The Finance Director reviews all non-compliance findings before submission to the grantor.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

Vendor selection must be documented and approved by the relevant Programme Manager.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Vendor selection must be documented and approved by the relevant Programme Manager.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

Programme events must be documented with an attendance list, agenda, and post-event report.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Travel advances are settled within five (5) business days of the traveller's return.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

The Board of Directors receives a summary compliance report at its annual meeting.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

Travel advances are settled within five (5) business days of the traveller's return.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

NC-C items relate to violations of the Opal City Community Fund grant contract.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

Programme events must be documented with an attendance list, agenda, and post-event report.

Vendor selection must be documented and approved by the relevant Programme Manager.

Vendor selection must be documented and approved by the relevant Programme Manager.

All staff involved in grant financial management must complete annual compliance training.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

All staff involved in grant financial management must complete annual compliance training.

Vendor selection must be documented and approved by the relevant Programme Manager.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

The Board of Directors receives a summary compliance report at its annual meeting.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

The Finance Director reviews all non-compliance findings before submission to the grantor.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

Programme staff must complete MAN's finance induction training before accessing grant funds.

Programme staff must complete MAN's finance induction training before accessing grant funds.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

Programme staff must complete MAN's finance induction training before accessing grant funds.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

Programme events must be documented with an attendance list, agenda, and post-event report.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

The Board of Directors receives a summary compliance report at its annual meeting.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

Travel advances are settled within five (5) business days of the traveller's return.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Travel advances are settled within five (5) business days of the traveller's return.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

Vendor selection must be documented and approved by the relevant Programme Manager.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Travel advances are settled within five (5) business days of the traveller's return.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

All staff involved in grant financial management must complete annual compliance training.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

The Board of Directors receives a summary compliance report at its annual meeting.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

NC-C items relate to violations of the Opal City Community Fund grant contract.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

NC-C items relate to violations of the Opal City Community Fund grant contract.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

Programme staff must complete MAN's finance induction training before accessing grant funds.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Programme staff must complete MAN's finance induction training before accessing grant funds.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

The Board of Directors receives a summary compliance report at its annual meeting.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

The Finance Director reviews all non-compliance findings before submission to the grantor.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

The Board of Directors receives a summary compliance report at its annual meeting.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

All staff involved in grant financial management must complete annual compliance training.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

Vendor selection must be documented and approved by the relevant Programme Manager.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

All staff involved in grant financial management must complete annual compliance training.

Vendor selection must be documented and approved by the relevant Programme Manager.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

Travel advances are settled within five (5) business days of the traveller's return.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Programme events must be documented with an attendance list, agenda, and post-event report.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

The Finance Director reviews all non-compliance findings before submission to the grantor.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

NC-C items relate to violations of the Opal City Community Fund grant contract.

The Board of Directors receives a summary compliance report at its annual meeting.

Programme staff must complete MAN's finance induction training before accessing grant funds.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

NC-C items relate to violations of the Opal City Community Fund grant contract.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

All staff involved in grant financial management must complete annual compliance training.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

Vendor selection must be documented and approved by the relevant Programme Manager.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

The Board of Directors receives a summary compliance report at its annual meeting.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

All staff involved in grant financial management must complete annual compliance training.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

Programme staff must complete MAN's finance induction training before accessing grant funds.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

The Finance Director reviews all non-compliance findings before submission to the grantor.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

The Board of Directors receives a summary compliance report at its annual meeting.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

The Board of Directors receives a summary compliance report at its annual meeting.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

NC-C items relate to violations of the Opal City Community Fund grant contract.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

Travel advances are settled within five (5) business days of the traveller's return.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

NC-C items relate to violations of the Opal City Community Fund grant contract.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

Travel advances are settled within five (5) business days of the traveller's return.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Travel advances are settled within five (5) business days of the traveller's return.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

Vendor selection must be documented and approved by the relevant Programme Manager.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

Travel advances are settled within five (5) business days of the traveller's return.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

All staff involved in grant financial management must complete annual compliance training.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

Programme staff must complete MAN's finance induction training before accessing grant funds.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

NC-C items relate to violations of the Opal City Community Fund grant contract.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

Vendor selection must be documented and approved by the relevant Programme Manager.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

The Board of Directors receives a summary compliance report at its annual meeting.

The Board of Directors receives a summary compliance report at its annual meeting.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

NC-C items relate to violations of the Opal City Community Fund grant contract.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

The Finance Director reviews all non-compliance findings before submission to the grantor.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Programme staff must complete MAN's finance induction training before accessing grant funds.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Programme staff must complete MAN's finance induction training before accessing grant funds.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Vendor selection must be documented and approved by the relevant Programme Manager.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

The Board of Directors receives a summary compliance report at its annual meeting.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

Programme staff must complete MAN's finance induction training before accessing grant funds.

All staff involved in grant financial management must complete annual compliance training.

Travel advances are settled within five (5) business days of the traveller's return.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

NC-C items relate to violations of the Opal City Community Fund grant contract.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

All staff involved in grant financial management must complete annual compliance training.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Programme staff must complete MAN's finance induction training before accessing grant funds.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Programme staff must complete MAN's finance induction training before accessing grant funds.

NC-C items relate to violations of the Opal City Community Fund grant contract.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

Vendor selection must be documented and approved by the relevant Programme Manager.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

NC-C items relate to violations of the Opal City Community Fund grant contract.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Vendor selection must be documented and approved by the relevant Programme Manager.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

The Finance Director reviews all non-compliance findings before submission to the grantor.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

Travel advances are settled within five (5) business days of the traveller's return.

Vendor selection must be documented and approved by the relevant Programme Manager.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

The Finance Director reviews all non-compliance findings before submission to the grantor.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

All staff involved in grant financial management must complete annual compliance training.

Programme events must be documented with an attendance list, agenda, and post-event report.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

NC-C items relate to violations of the Opal City Community Fund grant contract.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

The Finance Director reviews all non-compliance findings before submission to the grantor.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

All staff involved in grant financial management must complete annual compliance training.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

The Finance Director reviews all non-compliance findings before submission to the grantor.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Travel advances are settled within five (5) business days of the traveller's return.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

The Finance Director reviews all non-compliance findings before submission to the grantor.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

Programme events must be documented with an attendance list, agenda, and post-event report.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

Programme events must be documented with an attendance list, agenda, and post-event report.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

Programme events must be documented with an attendance list, agenda, and post-event report.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

Vendor selection must be documented and approved by the relevant Programme Manager.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Programme events must be documented with an attendance list, agenda, and post-event report.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

All staff involved in grant financial management must complete annual compliance training.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

Travel advances are settled within five (5) business days of the traveller's return.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

Vendor selection must be documented and approved by the relevant Programme Manager.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Programme staff must complete MAN's finance induction training before accessing grant funds.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

Programme staff must complete MAN's finance induction training before accessing grant funds.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

All staff involved in grant financial management must complete annual compliance training.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

The Board of Directors receives a summary compliance report at its annual meeting.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

The Finance Director reviews all non-compliance findings before submission to the grantor.

Programme events must be documented with an attendance list, agenda, and post-event report.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

NC-C items relate to violations of the Opal City Community Fund grant contract.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Vendor selection must be documented and approved by the relevant Programme Manager.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

Programme staff must complete MAN's finance induction training before accessing grant funds.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Programme events must be documented with an attendance list, agenda, and post-event report.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

All staff involved in grant financial management must complete annual compliance training.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

The Board of Directors receives a summary compliance report at its annual meeting.

The Board of Directors receives a summary compliance report at its annual meeting.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

The Board of Directors receives a summary compliance report at its annual meeting.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

Programme staff must complete MAN's finance induction training before accessing grant funds.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Vendor selection must be documented and approved by the relevant Programme Manager.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Programme events must be documented with an attendance list, agenda, and post-event report.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

All staff involved in grant financial management must complete annual compliance training.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

The Finance Director reviews all non-compliance findings before submission to the grantor.

The Finance Director reviews all non-compliance findings before submission to the grantor.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

Programme events must be documented with an attendance list, agenda, and post-event report.

NC-C items relate to violations of the Opal City Community Fund grant contract.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

Vendor selection must be documented and approved by the relevant Programme Manager.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

The Board of Directors receives a summary compliance report at its annual meeting.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Programme staff must complete MAN's finance induction training before accessing grant funds.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

Programme staff must complete MAN's finance induction training before accessing grant funds.

Vendor selection must be documented and approved by the relevant Programme Manager.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

NC-C items relate to violations of the Opal City Community Fund grant contract.

Programme events must be documented with an attendance list, agenda, and post-event report.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

Programme staff must complete MAN's finance induction training before accessing grant funds.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

Programme staff must complete MAN's finance induction training before accessing grant funds.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

Programme staff must complete MAN's finance induction training before accessing grant funds.

All staff involved in grant financial management must complete annual compliance training.

NC-C items relate to violations of the Opal City Community Fund grant contract.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

All staff involved in grant financial management must complete annual compliance training.

Programme events must be documented with an attendance list, agenda, and post-event report.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Programme staff must complete MAN's finance induction training before accessing grant funds.

Programme staff must complete MAN's finance induction training before accessing grant funds.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Programme staff must complete MAN's finance induction training before accessing grant funds.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Travel advances are settled within five (5) business days of the traveller's return.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

Vendor selection must be documented and approved by the relevant Programme Manager.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

The Finance Director reviews all non-compliance findings before submission to the grantor.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

The Finance Director reviews all non-compliance findings before submission to the grantor.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

All staff involved in grant financial management must complete annual compliance training.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

Programme staff must complete MAN's finance induction training before accessing grant funds.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Programme staff must complete MAN's finance induction training before accessing grant funds.

The Board of Directors receives a summary compliance report at its annual meeting.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

The Finance Director reviews all non-compliance findings before submission to the grantor.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Travel advances are settled within five (5) business days of the traveller's return.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

The Board of Directors receives a summary compliance report at its annual meeting.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

Programme staff must complete MAN's finance induction training before accessing grant funds.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

Programme events must be documented with an attendance list, agenda, and post-event report.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Travel advances are settled within five (5) business days of the traveller's return.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

The Finance Director reviews all non-compliance findings before submission to the grantor.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Programme events must be documented with an attendance list, agenda, and post-event report.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

All staff involved in grant financial management must complete annual compliance training.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

NC-C items relate to violations of the Opal City Community Fund grant contract.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Programme staff must complete MAN's finance induction training before accessing grant funds.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Programme staff must complete MAN's finance induction training before accessing grant funds.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

Programme events must be documented with an attendance list, agenda, and post-event report.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

Programme events must be documented with an attendance list, agenda, and post-event report.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

Vendor selection must be documented and approved by the relevant Programme Manager.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

Programme staff must complete MAN's finance induction training before accessing grant funds.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

The Finance Director reviews all non-compliance findings before submission to the grantor.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

The Board of Directors receives a summary compliance report at its annual meeting.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

The Finance Director reviews all non-compliance findings before submission to the grantor.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

Programme events must be documented with an attendance list, agenda, and post-event report.

Travel advances are settled within five (5) business days of the traveller's return.

Programme staff must complete MAN's finance induction training before accessing grant funds.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Vendor selection must be documented and approved by the relevant Programme Manager.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Vendor selection must be documented and approved by the relevant Programme Manager.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Vendor selection must be documented and approved by the relevant Programme Manager.

NC-C items relate to violations of the Opal City Community Fund grant contract.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

All staff involved in grant financial management must complete annual compliance training.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

Vendor selection must be documented and approved by the relevant Programme Manager.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

All staff involved in grant financial management must complete annual compliance training.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Programme staff must complete MAN's finance induction training before accessing grant funds.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

The Finance Director reviews all non-compliance findings before submission to the grantor.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

NC-C items relate to violations of the Opal City Community Fund grant contract.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

Programme events must be documented with an attendance list, agenda, and post-event report.

Programme events must be documented with an attendance list, agenda, and post-event report.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

The Board of Directors receives a summary compliance report at its annual meeting.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

All staff involved in grant financial management must complete annual compliance training.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Vendor selection must be documented and approved by the relevant Programme Manager.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

Programme staff must complete MAN's finance induction training before accessing grant funds.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

Vendor selection must be documented and approved by the relevant Programme Manager.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

Programme events must be documented with an attendance list, agenda, and post-event report.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

The Finance Director reviews all non-compliance findings before submission to the grantor.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Programme staff must complete MAN's finance induction training before accessing grant funds.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Programme events must be documented with an attendance list, agenda, and post-event report.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

The Board of Directors receives a summary compliance report at its annual meeting.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

The Board of Directors receives a summary compliance report at its annual meeting.

The Finance Director reviews all non-compliance findings before submission to the grantor.

NC-C items relate to violations of the Opal City Community Fund grant contract.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

NC-C items relate to violations of the Opal City Community Fund grant contract.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

Programme events must be documented with an attendance list, agenda, and post-event report.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

All staff involved in grant financial management must complete annual compliance training.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

The Finance Director reviews all non-compliance findings before submission to the grantor.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

Travel advances are settled within five (5) business days of the traveller's return.

Travel advances are settled within five (5) business days of the traveller's return.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

Travel advances are settled within five (5) business days of the traveller's return.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

Vendor selection must be documented and approved by the relevant Programme Manager.

All staff involved in grant financial management must complete annual compliance training.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

All staff involved in grant financial management must complete annual compliance training.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

Travel advances are settled within five (5) business days of the traveller's return.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

All staff involved in grant financial management must complete annual compliance training.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

Programme events must be documented with an attendance list, agenda, and post-event report.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

All staff involved in grant financial management must complete annual compliance training.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

All staff involved in grant financial management must complete annual compliance training.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

The Finance Director reviews all non-compliance findings before submission to the grantor.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Programme staff must complete MAN's finance induction training before accessing grant funds.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

The Board of Directors receives a summary compliance report at its annual meeting.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

Vendor selection must be documented and approved by the relevant Programme Manager.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

All staff involved in grant financial management must complete annual compliance training.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

The Finance Director reviews all non-compliance findings before submission to the grantor.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Programme staff must complete MAN's finance induction training before accessing grant funds.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Programme staff must complete MAN's finance induction training before accessing grant funds.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

NC-C items relate to violations of the Opal City Community Fund grant contract.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Programme events must be documented with an attendance list, agenda, and post-event report.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

The Board of Directors receives a summary compliance report at its annual meeting.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Programme staff must complete MAN's finance induction training before accessing grant funds.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

Programme events must be documented with an attendance list, agenda, and post-event report.

The Finance Director reviews all non-compliance findings before submission to the grantor.

Programme events must be documented with an attendance list, agenda, and post-event report.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

The Board of Directors receives a summary compliance report at its annual meeting.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

Programme events must be documented with an attendance list, agenda, and post-event report.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

Travel advances are settled within five (5) business days of the traveller's return.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

The Finance Director reviews all non-compliance findings before submission to the grantor.

The Board of Directors receives a summary compliance report at its annual meeting.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

NC-C items relate to violations of the Opal City Community Fund grant contract.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

Programme events must be documented with an attendance list, agenda, and post-event report.

Programme staff must complete MAN's finance induction training before accessing grant funds.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Vendor selection must be documented and approved by the relevant Programme Manager.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

Travel advances are settled within five (5) business days of the traveller's return.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

The Finance Director reviews all non-compliance findings before submission to the grantor.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

All staff involved in grant financial management must complete annual compliance training.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

Travel advances are settled within five (5) business days of the traveller's return.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

All staff involved in grant financial management must complete annual compliance training.

Vendor selection must be documented and approved by the relevant Programme Manager.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

The Board of Directors receives a summary compliance report at its annual meeting.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

The Finance Director reviews all non-compliance findings before submission to the grantor.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Programme events must be documented with an attendance list, agenda, and post-event report.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Programme staff must complete MAN's finance induction training before accessing grant funds.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

NC-C items relate to violations of the Opal City Community Fund grant contract.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Vendor selection must be documented and approved by the relevant Programme Manager.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

All staff involved in grant financial management must complete annual compliance training.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Programme staff must complete MAN's finance induction training before accessing grant funds.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Programme events must be documented with an attendance list, agenda, and post-event report.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

Travel advances are settled within five (5) business days of the traveller's return.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

The Board of Directors receives a summary compliance report at its annual meeting.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

The Finance Director reviews all non-compliance findings before submission to the grantor.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

NC-C items relate to violations of the Opal City Community Fund grant contract.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

NC-C items relate to violations of the Opal City Community Fund grant contract.

Vendor selection must be documented and approved by the relevant Programme Manager.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Travel advances are settled within five (5) business days of the traveller's return.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

Travel advances are settled within five (5) business days of the traveller's return.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

All staff involved in grant financial management must complete annual compliance training.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

All staff involved in grant financial management must complete annual compliance training.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

Programme events must be documented with an attendance list, agenda, and post-event report.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

NC-C items relate to violations of the Opal City Community Fund grant contract.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

The Finance Director reviews all non-compliance findings before submission to the grantor.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Programme events must be documented with an attendance list, agenda, and post-event report.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Programme events must be documented with an attendance list, agenda, and post-event report.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

NC-C items relate to violations of the Opal City Community Fund grant contract.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

Programme events must be documented with an attendance list, agenda, and post-event report.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

The Finance Director reviews all non-compliance findings before submission to the grantor.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

The Board of Directors receives a summary compliance report at its annual meeting.

Travel advances are settled within five (5) business days of the traveller's return.

Vendor selection must be documented and approved by the relevant Programme Manager.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Programme staff must complete MAN's finance induction training before accessing grant funds.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Programme events must be documented with an attendance list, agenda, and post-event report.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

All staff involved in grant financial management must complete annual compliance training.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

The Board of Directors receives a summary compliance report at its annual meeting.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

The Finance Director reviews all non-compliance findings before submission to the grantor.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

All staff involved in grant financial management must complete annual compliance training.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Vendor selection must be documented and approved by the relevant Programme Manager.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Travel advances are settled within five (5) business days of the traveller's return.

All staff involved in grant financial management must complete annual compliance training.

NC-C items relate to violations of the Opal City Community Fund grant contract.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

The Finance Director reviews all non-compliance findings before submission to the grantor.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

The Board of Directors receives a summary compliance report at its annual meeting.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

Programme events must be documented with an attendance list, agenda, and post-event report.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

The Finance Director reviews all non-compliance findings before submission to the grantor.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

The Board of Directors receives a summary compliance report at its annual meeting.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

The Board of Directors receives a summary compliance report at its annual meeting.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

NC-C items relate to violations of the Opal City Community Fund grant contract.

Programme staff must complete MAN's finance induction training before accessing grant funds.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

All staff involved in grant financial management must complete annual compliance training.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

Programme events must be documented with an attendance list, agenda, and post-event report.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Vendor selection must be documented and approved by the relevant Programme Manager.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Travel advances are settled within five (5) business days of the traveller's return.

The Board of Directors receives a summary compliance report at its annual meeting.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

Travel advances are settled within five (5) business days of the traveller's return.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

NC-C items relate to violations of the Opal City Community Fund grant contract.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

Programme staff must complete MAN's finance induction training before accessing grant funds.

Travel advances are settled within five (5) business days of the traveller's return.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

Vendor selection must be documented and approved by the relevant Programme Manager.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

Programme events must be documented with an attendance list, agenda, and post-event report.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

The Board of Directors receives a summary compliance report at its annual meeting.

The Finance Director reviews all non-compliance findings before submission to the grantor.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

MAN's external auditors will conduct an annual audit of grant expenditure as required by organizational policy.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

All staff involved in grant financial management must complete annual compliance training.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

Programme staff must complete MAN's finance induction training before accessing grant funds.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

Non-compliance with grant terms may result in disallowance of the relevant expenditure and recovery of funds from MAN.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

The Board of Directors receives a summary compliance report at its annual meeting.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

All transactions must be recorded in MAN's accounting system within ten (10) business days of occurrence.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

Vendor selection must be documented and approved by the relevant Programme Manager.

NC-C items relate to violations of the Opal City Community Fund grant contract.

All staff involved in grant financial management must complete annual compliance training.

Programme staff must complete MAN's finance induction training before accessing grant funds.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

The Finance Director reviews all non-compliance findings before submission to the grantor.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

Travel advances are settled within five (5) business days of the traveller's return.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

NC-C items relate to violations of the Opal City Community Fund grant contract.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

NC-C items relate to violations of the Opal City Community Fund grant contract.

Programme events must be documented with an attendance list, agenda, and post-event report.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

The Finance Director reviews all non-compliance findings before submission to the grantor.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

Intermingling of grant funds between different grantor accounts is strictly prohibited.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

Vendor selection must be documented and approved by the relevant Programme Manager.

The Finance Director reviews all non-compliance findings before submission to the grantor.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

MAN's Finance Committee provides oversight of all grant-funded expenditure on a quarterly basis.

Programme activities are subject to periodic review and assessment by the relevant grantor bodies.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

Remediation of non-compliance items must be documented and evidence submitted to the relevant grantor.

Vendor selection must be documented and approved by the relevant Programme Manager.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

MAN's internal auditors conduct quarterly interim checks to identify emerging compliance issues.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Travel advances are settled within five (5) business days of the traveller's return.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

Programme events must be documented with an attendance list, agenda, and post-event report.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

MAN's Finance Director is authorized to make representations to grantors regarding compliance matters.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

The Finance Director is responsible for ensuring compliance with all applicable grant terms and conditions.

All procurement above USD 5,000 must follow MAN's competitive tendering procedures.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

Non-compliance with documentation requirements does not automatically render an expenditure ineligible.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

Vendor selection must be documented and approved by the relevant Programme Manager.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

MAN's internal audit function conducts periodic spot-checks on grant expenditure throughout the year.

NC-C items relate to violations of the Opal City Community Fund grant contract.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Budget reallocations exceeding 10% of any budget line require grantor approval before implementation.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Programme events must be documented with an attendance list, agenda, and post-event report.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

MAN's Finance Committee must be notified of any non-compliance item with a value exceeding USD 1,000.

Meridian Aid Network (MAN) operates in accordance with its organizational mandate to deliver sustainable development programming across multiple jurisdictions.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

The Finance Director reviews all non-compliance findings before submission to the grantor.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

NC-A items relate to violations of the Halcyon Foundation grant agreement.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

Vendor selection must be documented and approved by the relevant Programme Manager.

Programme staff must complete MAN's finance induction training before accessing grant funds.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

NC-B items relate to violations of the Nordic Development Cooperative grant agreement.

Vendor selection must be documented and approved by the relevant Programme Manager.

Programme staff must complete MAN's finance induction training before accessing grant funds.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

All non-compliance findings must be communicated to the relevant grantor within fourteen (14) days of identification.

MAN maintains a commitment to transparency, accountability, and the highest standards of fiduciary stewardship.

MAN's whistleblower policy encourages staff to report suspected financial misconduct or non-compliance.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

All non-compliance items must include the relevant txn_id, violated clause, and proposed remediation action.

MAN shall maintain a dedicated project account for each active grant to ensure accurate financial tracking.

Programme events must be documented with an attendance list, agenda, and post-event report.

Any deviation from approved budget lines requires prior written authorization from the relevant grantor.

Sub-grantee expenditure is subject to the same documentation and eligibility requirements as direct MAN expenditure.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.

Documentation requirements set forth in grant agreements supersede MAN's internal policies where there is a conflict.

MAN maintains a non-compliance register that tracks all active and resolved items across all grants.

Travel advances are settled within five (5) business days of the traveller's return.

Grantors may accept a management response in lieu of full remediation for minor or technical violations.

Reimbursement claims must be supported by original documentation and approved by authorized signatories.

The Finance Director may delegate authority for day-to-day grant management to designated Finance Officers.

NC-C items relate to violations of the Opal City Community Fund grant contract.

All expenditure must be consistent with the applicable grant agreement and MAN's internal financial management procedures.

Receipts and supporting documentation must be retained for a minimum of seven (7) years from the grant closeout date.

A consolidated expenditure report is submitted to each grantor within sixty (60) days of the grant period close.

MAN retains external legal counsel for advice on complex compliance and regulatory matters.

Vendor selection must be documented and approved by the relevant Programme Manager.

The annual compliance audit is the primary mechanism for identifying and addressing non-compliance.

MAN's SOP classifies non-compliance items by grantor prefix and sequential number for cross-round tracking.

Foreign currency transactions are converted to USD at the Bank of Kenya mid-market rate on the date of expenditure.