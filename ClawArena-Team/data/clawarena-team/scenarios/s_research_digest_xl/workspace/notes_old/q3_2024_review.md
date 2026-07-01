# Q3 2024 Literature Review — Database-Integrated ML Systems (OUTDATED)

> **Warning:** These notes are from Q3 2024 and relate to a discontinued project on
> ML-integrated database query optimisation. They are NOT relevant to the April 2026
> research digest on efficient and trustworthy language models.

## Overview

This document summarises the literature reviewed between July and September 2024 for the
"LLM-assisted Query Planning" internship project under Prof. Hartmann. The project was
discontinued in November 2024 after the lab pivoted to alignment research.

## Aurora (Zhang et al., 2024)

Aurora proposes an end-to-end learned query optimiser that replaces the traditional
cost-based planner in PostgreSQL. A neural encoder maps SQL query trees to a
latent representation, which is decoded into physical operator sequences. The key
claim is a 2.3× speedup on TPC-H benchmarks. Limitations include poor generalisation
to schema drift and high offline training cost.

**Takeaway:** Learned planners can beat hand-crafted heuristics on stable workloads
but are brittle in production environments.

## DB-BERT (Trummer, 2023)

DB-BERT repurposes BERT-style masked language models to extract performance tuning
hints from database documentation. It identifies parameter recommendations in manuals
and applies them automatically. Achieves measurable throughput gains on MySQL without
any labelled training data.

**Takeaway:** Pre-trained LMs encode surprising amounts of operational database
knowledge that can be extracted zero-shot.

## Bao (Marcus et al., 2021)

Bao (Bandit Optimizer) frames cardinality estimation as a contextual bandit problem.
It learns a small neural network to choose among a portfolio of hint sets for the
native query optimiser. Online learning allows the system to adapt to workload shift
without expensive offline retraining.

**Takeaway:** Hybrid learned + rules-based approaches offer better stability than
fully neural planners in adversarial query workloads.

## VLDB 2024 Survey — MLOps for Database Workloads

A broad survey covering 47 papers on applying machine learning to database internals.
Taxonomy includes: learned indexes, learned cardinality estimation, learned query
optimisation, learned physical design. Concludes that deployment in production
is still rare due to explainability and regression risk concerns.

**Takeaway:** The gap between academic benchmark results and production adoption
remains large across all subfields.

---

*Notes compiled by: Graduate Research Assistant, Q3 2024. Project archived November 2024.*
