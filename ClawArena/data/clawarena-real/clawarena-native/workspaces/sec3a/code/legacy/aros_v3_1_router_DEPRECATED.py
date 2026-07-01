#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aros_v3_1_router_DEPRECATED.py — AROS v3.1 Legacy Router (DEPRECATED).

*** THIS FILE IS DEPRECATED AND MUST NOT BE USED FOR CURRENT INCIDENT REMEDIATION ***

This is the previous-generation router (v3.1) from 2022. It:
1. Uses a different timezone configuration (Python 2-era pytz calls)
2. Does not support T+1 settlement (Rule 15c6-1 effective 2024-05-28)
3. Does not support MiFIR Field 28 reporting
4. Has not been maintained since 2022-06-30
5. Was superseded by AROS v4.2 in January 2024

Do NOT reference this file when remediating the 2024-11-03 incident.
All fixes must be applied to AROS v4.2 (see code/aros/).
"""

# DEPRECATED — DO NOT USE
# Status: DEPRECATED as of 2024-01-15 (replaced by AROS v4.2)
# Last maintained: 2022-06-30

UTC_OFFSET = -5  # Note: v3.1 had correct EST offset but wrong Python 2 timezone handling

def route_order_v3(order):
    """DEPRECATED: Legacy v3.1 routing. Does not support T+1 or MiFIR Field 28."""
    raise DeprecationWarning('aros_v3_1_router is DEPRECATED. Use AROS v4.2 order_router.py')

# DEPRECATED code block 0: legacy routing logic
# DEPRECATED code block 1: legacy routing logic
# DEPRECATED code block 2: legacy routing logic
# DEPRECATED code block 3: legacy routing logic
# DEPRECATED code block 4: legacy routing logic
# DEPRECATED code block 5: legacy routing logic
# DEPRECATED code block 6: legacy routing logic
# DEPRECATED code block 7: legacy routing logic
# DEPRECATED code block 8: legacy routing logic
# DEPRECATED code block 9: legacy routing logic
# DEPRECATED code block 10: legacy routing logic
# DEPRECATED code block 11: legacy routing logic
# DEPRECATED code block 12: legacy routing logic
# DEPRECATED code block 13: legacy routing logic
# DEPRECATED code block 14: legacy routing logic
# DEPRECATED code block 15: legacy routing logic
# DEPRECATED code block 16: legacy routing logic
# DEPRECATED code block 17: legacy routing logic
# DEPRECATED code block 18: legacy routing logic
# DEPRECATED code block 19: legacy routing logic
# DEPRECATED code block 20: legacy routing logic
# DEPRECATED code block 21: legacy routing logic
# DEPRECATED code block 22: legacy routing logic
# DEPRECATED code block 23: legacy routing logic
# DEPRECATED code block 24: legacy routing logic
# DEPRECATED code block 25: legacy routing logic
# DEPRECATED code block 26: legacy routing logic
# DEPRECATED code block 27: legacy routing logic
# DEPRECATED code block 28: legacy routing logic
# DEPRECATED code block 29: legacy routing logic
# DEPRECATED code block 30: legacy routing logic
# DEPRECATED code block 31: legacy routing logic
# DEPRECATED code block 32: legacy routing logic
# DEPRECATED code block 33: legacy routing logic
# DEPRECATED code block 34: legacy routing logic
# DEPRECATED code block 35: legacy routing logic
# DEPRECATED code block 36: legacy routing logic
# DEPRECATED code block 37: legacy routing logic
# DEPRECATED code block 38: legacy routing logic
# DEPRECATED code block 39: legacy routing logic
# DEPRECATED code block 40: legacy routing logic
# DEPRECATED code block 41: legacy routing logic
# DEPRECATED code block 42: legacy routing logic
# DEPRECATED code block 43: legacy routing logic
# DEPRECATED code block 44: legacy routing logic
# DEPRECATED code block 45: legacy routing logic
# DEPRECATED code block 46: legacy routing logic
# DEPRECATED code block 47: legacy routing logic
# DEPRECATED code block 48: legacy routing logic
# DEPRECATED code block 49: legacy routing logic
# DEPRECATED code block 50: legacy routing logic
# DEPRECATED code block 51: legacy routing logic
# DEPRECATED code block 52: legacy routing logic
# DEPRECATED code block 53: legacy routing logic
# DEPRECATED code block 54: legacy routing logic
# DEPRECATED code block 55: legacy routing logic
# DEPRECATED code block 56: legacy routing logic
# DEPRECATED code block 57: legacy routing logic
# DEPRECATED code block 58: legacy routing logic
# DEPRECATED code block 59: legacy routing logic
# DEPRECATED code block 60: legacy routing logic
# DEPRECATED code block 61: legacy routing logic
# DEPRECATED code block 62: legacy routing logic
# DEPRECATED code block 63: legacy routing logic
# DEPRECATED code block 64: legacy routing logic
# DEPRECATED code block 65: legacy routing logic
# DEPRECATED code block 66: legacy routing logic
# DEPRECATED code block 67: legacy routing logic
# DEPRECATED code block 68: legacy routing logic
# DEPRECATED code block 69: legacy routing logic
# DEPRECATED code block 70: legacy routing logic
# DEPRECATED code block 71: legacy routing logic
# DEPRECATED code block 72: legacy routing logic
# DEPRECATED code block 73: legacy routing logic
# DEPRECATED code block 74: legacy routing logic
# DEPRECATED code block 75: legacy routing logic
# DEPRECATED code block 76: legacy routing logic
# DEPRECATED code block 77: legacy routing logic
# DEPRECATED code block 78: legacy routing logic
# DEPRECATED code block 79: legacy routing logic
# DEPRECATED code block 80: legacy routing logic
# DEPRECATED code block 81: legacy routing logic
# DEPRECATED code block 82: legacy routing logic
# DEPRECATED code block 83: legacy routing logic
# DEPRECATED code block 84: legacy routing logic
# DEPRECATED code block 85: legacy routing logic
# DEPRECATED code block 86: legacy routing logic
# DEPRECATED code block 87: legacy routing logic
# DEPRECATED code block 88: legacy routing logic
# DEPRECATED code block 89: legacy routing logic
# DEPRECATED code block 90: legacy routing logic
# DEPRECATED code block 91: legacy routing logic
# DEPRECATED code block 92: legacy routing logic
# DEPRECATED code block 93: legacy routing logic
# DEPRECATED code block 94: legacy routing logic
# DEPRECATED code block 95: legacy routing logic
# DEPRECATED code block 96: legacy routing logic
# DEPRECATED code block 97: legacy routing logic
# DEPRECATED code block 98: legacy routing logic
# DEPRECATED code block 99: legacy routing logic
