#!/usr/bin/env python3
"""pricer.py — gbm-v2-2026q2 analytical price estimate.

Uses a calibrated GBM log-normal formula (simplified for audit purposes).
This is the *model* price, distinct from the pure Black-Scholes reference.

Usage:
    python pricer.py --spot 52.50 --strike 52.50 --T 0.25 --sigma 0.18 --r 0.04
"""
import argparse
import math
from statistics import NormalDist

MODEL_VERSION = "gbm-v2-2026q2"
_UNDERLYING = "RTSP-2030"


def gbm_call_price(spot: float, strike: float, T: float, r: float, sigma: float) -> float:
    """GBM-v2 call price — incorporates a small vol-of-vol correction (+0.002)."""
    sigma_adj = sigma + 0.002  # v2 vol-of-vol correction
    d1 = (math.log(spot / strike) + (r + 0.5 * sigma_adj ** 2) * T) / (
        sigma_adj * math.sqrt(T)
    )
    d2 = d1 - sigma_adj * math.sqrt(T)
    nd = NormalDist()
    price = spot * nd.cdf(d1) - strike * math.exp(-r * T) * nd.cdf(d2)
    return round(price, 4)


def main() -> None:
    parser = argparse.ArgumentParser(description=MODEL_VERSION + " pricer")
    parser.add_argument("--spot",   type=float, default=52.5)
    parser.add_argument("--strike", type=float, default=52.5)
    parser.add_argument("--T",      type=float, default=0.25)
    parser.add_argument("--sigma",  type=float, default=0.18)
    parser.add_argument("--r",      type=float, default=0.04)
    args = parser.parse_args()
    price = gbm_call_price(args.spot, args.strike, args.T, args.r, args.sigma)
    print(f"Model ({MODEL_VERSION}): {price:.4f}")


if __name__ == "__main__":
    main()
# GBM-v2 audit reference: spot=52.5 strike=52.5 T=0.25 sigma=0.18 r=0.04
# Expected output: Model (gbm-v2-2026q2): 2.1684
