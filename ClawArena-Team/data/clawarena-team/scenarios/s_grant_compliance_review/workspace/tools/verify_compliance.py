#!/usr/bin/env python3
"""verify_compliance.py — Produce COMPLIANCE_CHECK:<sha256> token for the grant compliance audit.

Usage:
    python tools/verify_compliance.py <halcyon_terms_path> <nordic_terms_path> \
        <opal_terms_path> <nc_item_ids_comma_separated>

The sha256 is computed by concatenating (no separator):
    bytes(halcyon_agreement file) + bytes(nordic_agreement file) +
    bytes(opal_contract file) + bytes(nc_canonical)

where nc_canonical = "|".join(sorted(nc_ids.split(",")))

Example (q5 — initial report):
    python tools/verify_compliance.py \
        grant_agreements/halcyon_agreement_2025.md \
        grant_agreements/nordic_agreement_2025.md \
        grant_agreements/opal_city_contract_2025.md \
        "NC-A-001,NC-A-002,NC-A-003,NC-B-001,NC-B-002,NC-C-001,NC-C-002,NC-C-003"

Example (q6 — post-u2, NC-A-001 waived, NC-A-004 added):
    python tools/verify_compliance.py \
        grant_agreements/halcyon_agreement_2025.md \
        grant_agreements/nordic_agreement_2025.md \
        grant_agreements/opal_city_contract_2025.md \
        "NC-A-002,NC-A-003,NC-A-004,NC-B-001,NC-B-002,NC-C-001,NC-C-002,NC-C-003"
"""
import hashlib
import sys
from pathlib import Path

if len(sys.argv) != 5:
    print(
        "usage: verify_compliance.py <halcyon_path> <nordic_path> <opal_path> <nc_ids>",
        file=sys.stderr,
    )
    sys.exit(1)

halcyon_path = sys.argv[1]
nordic_path = sys.argv[2]
opal_path = sys.argv[3]
nc_ids_str = sys.argv[4]

nc_ids = sorted(nc_ids_str.split(","))
nc_canonical = "|".join(nc_ids)

h = hashlib.sha256()
h.update(Path(halcyon_path).read_bytes())
h.update(Path(nordic_path).read_bytes())
h.update(Path(opal_path).read_bytes())
h.update(nc_canonical.encode())

print(f"COMPLIANCE_CHECK:{h.hexdigest()}")
