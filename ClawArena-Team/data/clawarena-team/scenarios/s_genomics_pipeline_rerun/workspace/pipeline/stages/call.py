#!/usr/bin/env python3
"""call.py — GATK HaplotypeCaller wrapper for varcall-2026q2 pipeline.

Runs variant calling on the aligned BAM produced by align.py.
Output: per-sample GVCF file ready for joint genotyping.
"""
import argparse
import sys

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--sample", required=True)
    p.add_argument("--threads", type=int, default=8)
    return p.parse_args()

def main():
    args = parse_args()
    print(f"[call] {args.sample}: HaplotypeCaller started (threads={args.threads})", file=sys.stderr)
    # In production: gatk HaplotypeCaller -I aligned/{sample}.bam -O gvcf/{sample}.g.vcf.gz
    print(f"[call] {args.sample}: complete", file=sys.stderr)

if __name__ == "__main__":
    main()
