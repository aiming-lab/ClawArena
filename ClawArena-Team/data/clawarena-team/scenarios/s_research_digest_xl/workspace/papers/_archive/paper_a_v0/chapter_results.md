# SparseFormer — Results (Version 0, WITHDRAWN)

> **WITHDRAWN — Do not cite.**
> This chapter is from the pre-submission draft. The experimental setup was
> incomplete; results have since been superseded. See `papers/paper_a/results.md`
> for the authoritative camera-ready figures.

## Main Results

**Memory efficiency:** SparseFormer achieves a **23% reduction in VRAM** consumption
compared to the full-attention baseline on sequences of 32k tokens.  The baseline is
a standard encoder-only transformer with full dense attention (no FlashAttention).

**Accuracy retention:** Downstream task accuracy is preserved at 94.1% relative to
the full-attention baseline, averaged across four classification and extraction tasks.

**Throughput:** A modest 1.15× throughput improvement is observed at batch size 8;
throughput gains are not significant at larger batch sizes due to routing overhead.

> **Why these numbers are wrong:** The VRAM measurement excluded KV-cache overhead
> introduced during the dynamic bucket selection phase.  When the evaluation harness
> was corrected (see revision note in abstract), VRAM savings increased substantially.
> The correct figure is reported in `papers/paper_a/results.md`.  The 23% figure
> **must not be cited** as representative of SparseFormer's capabilities.

## Conclusion (withdrawn)

These preliminary results suggested that adaptive locality priors are a promising
direction for reducing attention memory cost.  The corrected camera-ready results
confirm and strengthen this conclusion, but the specific 23%-VRAM headline from
this draft should be treated as an error.
