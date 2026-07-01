#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SLA credit calculation template for ArcNode incidents.

Formula (Cloudflare Business SLA):
  (Outage Period minutes * Affected Customer Ratio) / Scheduled Availability minutes
"""

def calculate_credit(outage_minutes: float, affected_ratio: float,
                     scheduled_minutes: float = 43200) -> float:
    """
    Returns the service credit ratio.

    :param outage_minutes: Duration of the outage in minutes.
    :param affected_ratio: Fraction of unique customer IPs affected (0.0 - 1.0).
    :param scheduled_minutes: Total minutes in the billing period (default: 30-day month).
    :return: Service credit ratio (multiply by monthly fee for credit amount).
    """
    return (outage_minutes * affected_ratio) / scheduled_minutes


if __name__ == "__main__":
    # Example: June 20 2024 incident
    outage = 100      # minutes
    ratio  = 0.021    # to be filled from affected_customers.csv
    sched  = 43200     # 30-day month
    credit = calculate_credit(outage, ratio, sched)
    print(f"SLA credit ratio: {credit:.6f}")
