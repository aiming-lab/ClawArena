#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
doi_resolver.py — Fetch metadata for a DOI via the CrossRef API.

Usage: python doi_resolver.py <doi>
Example: python doi_resolver.py 10.1073/pnas.1209746109
"""
import sys
import urllib.request
import json


def resolve(doi: str) -> dict:
    url = f"https://api.crossref.org/works/{doi}"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read())
            return data.get("message", {})
    except Exception as e:
        return {"error": str(e)}


def main():
    if len(sys.argv) < 2:
        print("Usage: python doi_resolver.py <doi>"); sys.exit(1)
    doi = sys.argv[1]
    meta = resolve(doi)
    print(json.dumps(meta, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
