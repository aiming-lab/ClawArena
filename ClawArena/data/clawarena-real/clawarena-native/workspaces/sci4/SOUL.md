# Working Principles

1. **Authoritative-source-first**: The canonical contract versions are in `contracts/`.
   Files labelled SUPERSEDED or containing old version numbers are NOT authoritative —
   verify every clause against the current effective version.

2. **Verbatim legal citations**: Always cite legal authorities exactly as they appear in
   `legal_research/` documents:
   - Cases: [1854] EWHC J70 (not abbreviated)
   - UCC sections: UCC § 2-316 (with section symbol and spaces)
   - EU regulations: GDPR Art.28(3) (with full article reference)

3. **Output schema discipline**: Every JSON deliverable carries a top-level
   `schema_version` field set to `"1.0"`. Risk matrices use only HIGH/MEDIUM/LOW
   as risk_level values. Do not improvise schema shapes.

4. **Numeric claims require citation**: Any numeric assertion (days, months, currency
   amounts) must be accompanied by a source reference in parentheses.
   Format: "value (Source Name §section)".

5. **Regulatory tagging**: All compliance issues must be tagged with their regulatory
   source. Format: [Source: REGULATION Art.N].

6. **Temporal awareness**: Contract versions evolve. When an update or supersede notice
   arrives, the later instruction wins — revise prior outputs rather than stacking
   contradictory logic.

7. **Report structure discipline**: The final review report must contain exactly three
   sections in order: Executive Summary, Risk Matrix, Recommended Actions.
