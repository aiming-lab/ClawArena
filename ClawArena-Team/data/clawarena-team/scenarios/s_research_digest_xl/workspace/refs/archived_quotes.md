# Archived Quotation Bank — Previous Projects

> **Warning:** This file contains quotations and excerpts collected during previous
> research projects (2023–2025). The content relates primarily to database systems,
> distributed computing, and early NLP work. It is NOT relevant to the April 2026
> research digest on efficient and trustworthy language models.
> Do not source quotes from this file for the current assignment.

Last updated: 2025-10-14

---

## Quotations — Database Systems & ML

> "The elephant in the room for learned query optimisers is the cold start problem:
> you need queries to learn from, but you need to handle queries before you have learned anything."
>
> — Marcus et al., *Neo: A Learned Query Optimizer*, VLDB 2019, §6 Discussion

---

> "Cardinality estimation errors have a multiplicative effect on query plan quality;
> a single bad estimate can cascade into plan selection that is orders of magnitude slower."
>
> — Leis et al., *How Good Are Query Optimizers, Really?*, VLDB 2015, §1 Introduction

---

> "We argue that the primary bottleneck for production adoption of learned database components
> is not accuracy, but regression risk: a learned component must never be catastrophically
> worse than the baseline, even on out-of-distribution inputs."
>
> — Trummer, *DB-BERT: A Database Tuning Tool That "Reads the Manual"*, SIGMOD 2022, §7

---

> "The join ordering problem is NP-hard in the number of relations, yet most query optimisers
> solve it heuristically in milliseconds. Learned optimisers must match or beat this latency
> budget at inference time — a constraint that shapes architectural choices significantly."
>
> — Collected from: VLDB 2024 Survey on Learned Database Components, §3.2

---

## Quotations — Early NLP & Scaling

> "What we are seeing is not artificial general intelligence, but rather an extraordinary
> compression of internet text into weights that support a surprising diversity of task formats."
>
> — Paraphrased from: Bender et al., *On the Dangers of Stochastic Parrots*, FAccT 2021

---

> "Emergent capabilities in large language models pose a challenge for evaluation:
> the capability did not exist at smaller scale, so benchmark designers did not know to test for it."
>
> — Wei et al., *Emergent Abilities of Large Language Models*, TMLR 2022

---

> "Scaling laws predict loss, not capabilities. The relationship between loss reduction
> and capability gain is highly non-linear and task-specific."
>
> — Hoffmann et al., *Training Compute-Optimal Large Language Models*, NeurIPS 2022

---

## Quotations — Research Methodology

> "A result that cannot be reproduced is not a result. It is a story."
>
> — Attributed to: anonymous reviewer, NeurIPS 2023 (paraphrase from author response)

---

> "The 'impressive demo' trap is when we mistake a model's best-case performance
> for its typical performance. Evaluation must be adversarial, not aspirational."
>
> — Collected from: internal lab discussion notes, Spring 2024

---

> "Statistical significance is necessary but not sufficient for scientific significance.
> We need effect sizes, confidence intervals, and ablations — not just p-values."
>
> — Lab whiteboard, attributed to Prof. Hartmann, Fall 2024

---

*Archive status: closed. Do not add new entries. Maintained for historical reference only.*
