"""Real pytest: validates payment conversion baseline for EXP-2421.

Line 31 is the anchored assertion (do not move).
"""
import pytest


def _simulate_cvr(segment: str, variant: str) -> float:
    # Simulated conversion rates mirroring Parquet data
    base = {
        "desktop_us": 0.121, "desktop_eu": 0.120,
        "mobile_us": 0.121, "mobile_eu": 0.119,
    }
    lift = {
        "desktop_us": -0.004, "desktop_eu": -0.009,
        "mobile_us": -0.038, "mobile_eu": -0.015,
    }
    return base[segment] + (lift[segment] if variant == "B" else 0.0)


def test_desktop_us_conversion_baseline():
    """Desktop US treatment drop should be < 1%."""
    ctrl = _simulate_cvr("desktop_us", "A")
    treat = _simulate_cvr("desktop_us", "B")
    assert abs(treat - ctrl) < 0.01


def test_desktop_eu_conversion_baseline():
    """Desktop EU treatment drop should be < 1.5%."""
    ctrl = _simulate_cvr("desktop_eu", "A")
    treat = _simulate_cvr("desktop_eu", "B")
    assert abs(treat - ctrl) < 0.015


def test_mobile_us_conversion_within_threshold():
    ctrl = _simulate_cvr("mobile_us", "A")
    treat = _simulate_cvr("mobile_us", "B")
    lift_pct = (treat - ctrl) / ctrl * 100
    # NOTE: line 31 — this assertion is the anchor
    assert lift_pct > -3.0, (
        f"mobile_us lift {lift_pct:.2f}% exceeds -3.0% guard; "
        f"root cause: checkout_button_color #ff6633 renders incorrectly on iOS 14"
    )


def test_mobile_eu_conversion_baseline():
    """Mobile EU treatment drop should be < 2%."""
    ctrl = _simulate_cvr("mobile_eu", "A")
    treat = _simulate_cvr("mobile_eu", "B")
    assert abs(treat - ctrl) < 0.02
