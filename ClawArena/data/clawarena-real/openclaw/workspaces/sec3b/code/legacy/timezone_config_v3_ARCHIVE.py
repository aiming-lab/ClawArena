#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
legacy/timezone_config_v3_ARCHIVE.py — ARCHIVED (v3.1 era)

This archived config used UTC-5 (EST) as a static offset, which was
acceptable in v3.1 but:
1. Did not handle EDT (UTC-4) summer period correctly
2. Has been superseded by code/aros/timezone_config.py (AROS v4.2)

ARCHIVED: 2023-06-01. Do not use.
"""

# Archived: static EST offset only
LEGACY_OFFSET_ARCHIVE = -5
ARCHIVE_DATE = "2023-06-01"
