#!/usr/bin/env python3
"""bs_reference.py — Black-Scholes analytical reference (no vol-of-vol adjustment).

Usage:
    python bs_reference.py --spot 52.50 --strike 52.50 --T 0.25 --sigma 0.18 --r 0.04

Expected output (default args): BS_REFERENCE:2.1477
"""
# audit-top10 #1（已收敛）：原注释 "4.798" 是凭空写的伪值——BS 公式在场景自带参数
# (spot=K=52.5, T=0.25, sigma=0.18, r=0.04) 下数学上只能算出 2.1477。整个场景的 4.8x
# 数值族已统一重构为真值（BS=2.1477 / MC=2.1552 / model=2.1684），见 docs/discussions/FIX_NOTES.md。
# 另注：原 main() 把 r/sigma 实参传反（bs_call(...,sigma,r)），会用 r=0.18/σ=0.04 算出
# 伪值 2.3145；已修正为正确顺序，pricer.py 同款 bug 一并修复。
import argparse
import math
from statistics import NormalDist


def bs_call(spot: float, strike: float, T: float, r: float, sigma: float) -> float:
    d1 = (math.log(spot / strike) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    nd = NormalDist()
    return round(spot * nd.cdf(d1) - strike * math.exp(-r * T) * nd.cdf(d2), 4)


def main() -> None:
    parser = argparse.ArgumentParser(description="BS reference pricer")
    parser.add_argument("--spot",   type=float, default=52.5)
    parser.add_argument("--strike", type=float, default=52.5)
    parser.add_argument("--T",      type=float, default=0.25)
    parser.add_argument("--sigma",  type=float, default=0.18)
    parser.add_argument("--r",      type=float, default=0.04)
    args = parser.parse_args()
    price = bs_call(args.spot, args.strike, args.T, args.r, args.sigma)
    print(f"BS_REFERENCE:{price:.4f}")


if __name__ == "__main__":
    main()
