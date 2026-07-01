#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for timezone_config.py — some tests fail due to DST bug."""

import unittest
import sys
sys.path.insert(0, '..')

class TestTimezoneConfig(unittest.TestCase):
    def test_utc_offset_est(self):
        """Test that UTC_OFFSET is -5 for EST (winter time). FAILS due to bug."""
        from timezone_config import UTC_OFFSET
        # This test FAILS: UTC_OFFSET = -4 but should be -5 for EST
        self.assertEqual(UTC_OFFSET, -5, 'UTC_OFFSET must be -5 for EST')

    def test_cme_settle_utc(self):
        """CME E-Mini settle time in UTC for EST: should be 21:00:00. FAILS."""
        from timezone_config import get_cme_settle_utc
        result = get_cme_settle_utc()
        # Expected: 21:00:00 (15:00 CT = UTC+6 in winter EST)
        # Actual (buggy): 20:00:00
        self.assertEqual(result, '21:00:00', f'Expected 21:00:00, got {result}')

if __name__ == '__main__':
    unittest.main()
