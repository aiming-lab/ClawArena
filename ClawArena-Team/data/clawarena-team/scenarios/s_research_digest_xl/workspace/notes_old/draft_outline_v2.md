# Draft Outline v2 — LLM-Assisted Query Planning Survey (OUTDATED)

> **Warning:** This is a draft document from November 2025 for the discontinued
> database-ML project. It is NOT relevant to the April 2026 research digest on
> efficient and trustworthy language models.

**Document status:** Draft v2, abandoned 2025-11-28
**Original target venue:** VLDB 2026 (submission deadline missed — project discontinued)

---

## Proposed Paper Structure

### Abstract (~250 words)

We survey the emerging intersection of large language models and relational database internals,
with emphasis on query optimisation, cardinality estimation, and physical design advisors.
We taxonomise 52 papers from 2018–2024, identify three recurring failure modes in production
deployment, and propose a unified evaluation framework...

### 1. Introduction

- LLMs increasingly applied to structured data tasks
- Database vendors experimenting with neural components in production
- Gap: no unified evaluation framework for "learned DB" components

### 2. Background

#### 2.1 Traditional Query Optimisation
Cost-based optimisers, histograms, cardinality estimation.

#### 2.2 Rise of Learned Components
Bao, Aurora, NEO, BAONN, Marcus et al. 2019–2024.

#### 2.3 LLMs and Structured Data
DB-BERT, GPT-4 on SQL generation benchmarks.

### 3. Taxonomy (52 papers)

| Category | Papers | Key limitation |
|---|---|---|
| Learned cardinality estimation | 18 | Distribution shift |
| Learned query optimisation | 16 | Regression risk |
| Physical design advisors | 11 | Cold start |
| NL-to-SQL | 7 | Schema generalisation |

### 4. Failure Mode Analysis

**FM-1: Distribution shift fragility.** Learned models trained on historical query logs
fail catastrophically when the workload changes. Bao mitigates this with online learning
but still incurs a regression window.

**FM-2: Explainability deficit.** DBAs cannot inspect or override neural decisions.
Regulatory environments (GDPR, SOX) may prohibit black-box query planning.

**FM-3: Cold start.** New schemas or workloads require substantial warm-up data.
Hybrid approaches that fall back to the native optimiser are most practical.

### 5. Proposed Evaluation Framework

Five axes: throughput, latency p99, regression rate, warm-up cost, explainability score.

### 6. Open Challenges

- Cross-workload generalisation
- Hardware heterogeneity
- Online-vs-offline training tradeoffs

### 7. Conclusion

Learned database components are promising but not yet production-ready without careful
hybrid design and rigorous evaluation...

---

*Status: outline abandoned 2025-11-28 when project discontinued. Do not use.*
