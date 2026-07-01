#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
legacy/aros_v3_1_router_DEPRECATED.py — DEPRECATED LEGACY CODE

WARNING: THIS FILE IS DEPRECATED AS OF 2023-06-01.
DO NOT USE THIS CODE FOR ANY PURPOSE.
DO NOT REFERENCE THIS CODE IN INCIDENT REMEDIATION.

Superseded by: code/aros/order_router.py (AROS v4.2)

Reasons for deprecation:
1. Does NOT implement MiFIR Field 28 UTC timestamp requirement
   (reports local time instead of UTC — non-compliant with FCA Market Watch 59)
2. Does NOT handle DST transitions for settlement scheduling
3. Incompatible with T+1 settlement rule (Rule 15c6-1, effective 2024-05-28)
4. Uses obsolete venue connectivity (pre-2022 CME API)
5. Power Peg-style order splitting not compliant with Rule 15c3-5(b) position limits

Archived for historical reference only. If you are reading this file during
an incident remediation, you are looking at the wrong code — use order_router.py.
"""

# LEGACY constants (do not use)
LEGACY_UTC_OFFSET = -5  # This was correct for v3.1 but lacks DST handling
LEGACY_VERSION = "3.1.7"
LEGACY_DEPRECATED_DATE = "2023-06-01"

# Legacy MiFIR field — INCORRECTLY reports local time (non-compliant)
LEGACY_MIFIR_TZ = "LOCAL"  # BUG: Should be "UTC" per Field 28 requirement

def legacy_route_order(instrument, qty, price, order_time_local):
    """
    DEPRECATED: Do not use.
    This function routes orders using local time for MiFIR Field 28 reporting,
    which is NON-COMPLIANT with FCA Market Watch 59 UTC requirement.
    """
    raise NotImplementedError(
        "aros_v3_1_router_DEPRECATED: This function is deprecated and must not be called. "
        "Use code.aros.order_router.OrderRouter instead."
    )


def legacy_compute_settlement(trade_time_local, utc_offset=-5):
    """
    DEPRECATED: Uses static UTC-5 offset without DST awareness.
    This is INCOMPATIBLE with T+1 settlement rule (Rule 15c6-1).
    """
    raise NotImplementedError("DEPRECATED")
