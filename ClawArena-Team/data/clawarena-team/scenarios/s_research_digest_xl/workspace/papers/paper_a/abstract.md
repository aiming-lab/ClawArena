# Sparse Attention Transformers: Memory-Efficient Self-Attention via Adaptive Locality

**Authors:** Alexandra Merritt¹, Jiulong Chen², Priya Nair¹, Olaf Steinberg³

¹ University of Coastal Research, ² Tsinghua Institute of AI, ³ Technical University of Berlin

**Venue:** Proceedings of NeurIPS 2026

## Abstract

The quadratic memory cost of full self-attention has long constrained the practical context length of transformer-based language models. In this paper, we introduce **SparseFormer**, a novel architecture that dynamically selects a sparse subset of attention keys and values for each query token based on learned locality priors. Our central finding is that **sparse attention reduces VRAM by 40%** compared to full-attention baselines while preserving more than 97% of downstream task accuracy across seven standard benchmarks. We provide theoretical bounds on the approximation error introduced by our sparsity mask and validate these bounds empirically on sequences up to 128k tokens. SparseFormer achieves state-of-the-art efficiency on the LongBench suite and enables single-GPU inference for models that would otherwise require multi-GPU setups.

**Keywords:** sparse attention, memory efficiency, long-context transformers, VRAM reduction
