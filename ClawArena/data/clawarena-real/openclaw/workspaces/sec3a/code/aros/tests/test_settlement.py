#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for settlement_scheduler.py."""

import unittest

class TestSettlementScheduler(unittest.TestCase):
    def test_t1_effective_date(self):
        """T+1 effective date should be 2024-05-28."""
        import sys; sys.path.insert(0, '..')
        from settlement_scheduler import T1_EFFECTIVE_DATE
        self.assertEqual(T1_EFFECTIVE_DATE, '2024-05-28')

if __name__ == '__main__':
    unittest.main()
