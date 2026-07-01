# FDA Infusion Pump Lifecycle Regulatory Requirements
## Summary for Device Manufacturers

**Source**: FDA Guidance — Design Considerations for Pivotal Clinical Investigations for
Medical Devices; 21 CFR Parts 820, 803, 806; FDA Total Product Lifecycle (TPLC) Framework

---

## Design Controls (21 CFR 820.30)

All infusion pump manufacturers must implement design controls covering:
- Design and Development Planning
- Design Input (including use-related risk analysis per IEC 62366)
- Design Output (engineering drawings, specifications)
- Design Review at each major stage
- Design Verification (confirms output meets input)
- Design Validation (confirms device meets user needs in intended use environment)
- Design Transfer (from development to production)
- Design Changes (controlled change process, re-validation where required)

**Relevance to Case A (InfuTronix Nimbus)**: Inadequate design validation of the
battery management circuit under realistic clinical conditions (thermal variation,
aged battery chemistry) represents a Design Validation failure under 820.30(g).

---

## Software Lifecycle Requirements (IEC 62304 / FDA Guidance)

Software-based medical devices must follow IEC 62304 software lifecycle processes:
- Software Development Planning
- Software Requirements Analysis
- Software Architectural Design
- Software Detailed Design
- Software Unit Implementation and Verification
- Software Integration and Integration Testing
- Software System Testing
- Software Release

**Relevance to Case B (Ivenix LVP)**: Boundary-case testing gaps (dual-zero input,
aged battery validation) represent Software System Testing failures per IEC 62304-5.7.

---

## Post-Market Surveillance (21 CFR Part 803, 806, 820.198)

Manufacturers must maintain:
- A system for receiving and evaluating complaints (820.198)
- MDR submission processes (Part 803)
- Correction and removal reporting (Part 806)
- Post-market surveillance studies (522 Orders) when warranted

---

## 510(k) Re-submission Requirements

For devices requiring complete redesign after a Class I recall:
- Original 510(k) clearance is no longer valid if the device is substantially changed.
- Manufacturer must submit a new 510(k) and receive FDA clearance before reintroducing.
- **InfuTronix Nimbus**: FDA has indicated the device requires complete redesign and
  a new 510(k) clearance. The device support cutoff (June 20, 2024) marks the end
  of the current product lifecycle.
