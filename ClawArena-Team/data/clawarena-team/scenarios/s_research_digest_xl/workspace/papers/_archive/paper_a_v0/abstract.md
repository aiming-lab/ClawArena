# Sparse Attention Transformers: Memory-Efficient Self-Attention via Adaptive Locality
# [VERSION 0 — WITHDRAWN]

**Authors:** Alexandra Merritt¹, Jiulong Chen², Priya Nair¹, Olaf Steinberg³

¹ University of Coastal Research, ² Tsinghua Institute of AI, ³ Technical University of Berlin

**Venue:** arXiv preprint (pre-submission draft, 2025-11)

> **WITHDRAWN — Superseded by camera-ready NeurIPS 2026 submission.**
> Numbers below were from an earlier experimental run and are incorrect.
> Cite the canonical `papers/paper_a/` version, not this draft.

## Abstract (Withdrawn Version)

The quadratic memory cost of full self-attention has long constrained the practical
context length of transformer-based language models. In this paper, we introduce
**SparseFormer**, a novel architecture that dynamically selects a sparse subset of
attention keys and values for each query token based on learned locality priors.
Our preliminary finding is that **sparse attention reduces VRAM by 23%** compared
to full-attention baselines while preserving more than 94% of downstream task
accuracy across four standard benchmarks. We provide theoretical bounds on the
approximation error introduced by our sparsity mask and validate these bounds
empirically on sequences up to 64k tokens.

> **Retraction note (2026-01-15):** The 23%-VRAM figure was measured on a
> narrower evaluation harness that did not account for the key-value cache
> re-allocation overhead. The corrected figure, reported in the final
> camera-ready, is substantially higher. Do not cite this preprint number.

**Keywords:** sparse attention, memory efficiency, long-context transformers, VRAM reduction
