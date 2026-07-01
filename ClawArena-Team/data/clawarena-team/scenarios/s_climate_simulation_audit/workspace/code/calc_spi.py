#!/usr/bin/env python3
"""calc_spi.py — Compute SPI from historical_monthly.parquet.

Usage: python code/calc_spi.py [--input data/historical_monthly.parquet] [--window 12]

Outputs SPI-12 time series and saves to output/spi_computed.csv.
The drought threshold is SPI < -1.5 for consecutive >= 3 months.
"""
import argparse
import math
import pathlib

DROUGHT_THRESHOLD = -1.5
MIN_CONSECUTIVE_MONTHS = 3


def fit_gamma(values):
    """Simplified L-moments gamma fitting."""
    mean_v = sum(values) / len(values)
    variance = sum((v - mean_v) ** 2 for v in values) / (len(values) - 1)
    alpha = mean_v ** 2 / variance
    beta = variance / mean_v
    return alpha, beta


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/historical_monthly.parquet")
    parser.add_argument("--window", type=int, default=12)
    args = parser.parse_args()

    import pyarrow.parquet as pq
    tbl = pq.read_table(args.input)
    dates = tbl["date"].to_pylist()
    precip = tbl["precip_mm"].to_pylist()

    window = args.window
    spi_vals = []
    for i in range(len(precip)):
        if i < window - 1:
            spi_vals.append(None)
            continue
        window_data = [p for p in precip[i - window + 1 : i + 1] if p is not None]
        if not window_data:
            spi_vals.append(None)
            continue
        mean_w = sum(window_data) / len(window_data)
        spi_vals.append(round((window_data[-1] - mean_w) / (max(1e-6, sum(
            (v - mean_w) ** 2 for v in window_data
        ) / max(1, len(window_data) - 1)) ** 0.5), 3))

    out_path = pathlib.Path("output/spi_computed.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        f.write("date,spi_computed\n")
        for d, s in zip(dates, spi_vals):
            f.write(f"{d},{s if s is not None else ''}\n")
    print(f"SPI-{window} saved to {out_path}")
    print(f"Drought threshold: SPI < {DROUGHT_THRESHOLD} for >= {MIN_CONSECUTIVE_MONTHS} months")


if __name__ == "__main__":
    main()
