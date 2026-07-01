#!/usr/bin/env python3
"""run_crosstab.py — cross-tab a segment parquet file.

Usage:
    python tools/run_crosstab.py data/exp_2421/<segment>.parquet

Outputs a simple cross-tabulation: variant groups × conversion metric.
Columns are inferred by shape (schema-by-shape):
  - binary column (0/1) with max=1 → treated as 'converted'
  - string column with 2 unique values → treated as 'variant'
  - all other columns → diagnostic

Exit 0 on success; prints tab-separated result to stdout.
"""
from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: run_crosstab.py <parquet_file>", file=sys.stderr)
        return 2

    try:
        import pyarrow.parquet as pq
        import pyarrow.compute as pc
    except ImportError:
        print("ERROR: pyarrow is required", file=sys.stderr)
        return 1

    pq_path = Path(sys.argv[1])
    if not pq_path.exists():
        print(f"ERROR: file not found: {pq_path}", file=sys.stderr)
        return 1

    table = pq.read_table(pq_path)
    schema = table.schema

    # Infer variant column: string/large_string with exactly 2 unique values
    variant_col = None
    converted_col = None
    for i, field in enumerate(schema):
        col = table.column(i)
        if str(field.type) in ("string", "large_string", "utf8", "large_utf8"):
            uvals = pc.unique(col).to_pylist()
            if len(uvals) == 2:
                variant_col = field.name
        elif str(field.type) in ("int64", "int32", "double", "float", "bool"):
            try:
                arr = col.cast("int64").to_pylist()
                if all(v in (0, 1) for v in arr if v is not None):
                    mx = max((v for v in arr if v is not None), default=0)
                    if mx == 1:
                        converted_col = field.name
            except Exception:
                pass

    if variant_col is None or converted_col is None:
        print(f"ERROR: could not infer variant ({variant_col}) or converted ({converted_col}) columns", file=sys.stderr)
        return 1

    # Cross-tab
    df_like: dict[str, list] = {}
    variant_vals = table.column(variant_col).to_pylist()
    converted_vals = table.column(converted_col).to_pylist()

    groups: dict[str, list[int]] = {}
    for var, conv in zip(variant_vals, converted_vals):
        groups.setdefault(str(var), []).append(int(conv) if conv is not None else 0)

    print(f"segment_parquet\t{pq_path.stem}")
    print(f"variant_column\t{variant_col}")
    print(f"converted_column\t{converted_col}")
    print("---")
    print("variant\tsessions\tconverted\tcvr\tconversion_delta")
    group_results = {}
    for var_label, vals in sorted(groups.items()):
        n = len(vals)
        conv_n = sum(vals)
        cvr = conv_n / n if n > 0 else 0.0
        group_results[var_label] = {"sessions": n, "converted": conv_n, "cvr": cvr}

    ctrl_cvr = None
    for var_label, res in sorted(group_results.items()):
        delta = ""
        if ctrl_cvr is None:
            ctrl_cvr = res["cvr"]
            delta = "baseline"
        else:
            d = (res["cvr"] - ctrl_cvr) / ctrl_cvr * 100
            delta = f"{d:+.2f}%"
        print(f"{var_label}\t{res['sessions']}\t{res['converted']}\t{res['cvr']:.4f}\t{delta}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
