# 4. Results

We evaluate SparseFormer along four axes: memory consumption, throughput, downstream task accuracy, and training stability. All experiments use a 13B-parameter base architecture trained on the standard RedPajama-v2 mixture for one trillion tokens, with sequence lengths uniformly sampled from {4k, 16k, 32k, 64k, 128k}. Dense-attention baselines are trained with identical hyperparameters and an otherwise-identical codebase.

## 4.1 Memory footprint

The headline result of our paper concerns memory: **sparse attention reduces VRAM by 40%** compared to the dense baseline at 32k context length on a single H100 GPU, with the reduction growing to 51% at 64k and 58% at 128k. The savings come from two sources. First, the materialised attention matrix occupies only `O(n k)` rather than `O(n^2)` cells, which dominates the saving at long contexts. Second, the key/value cache used during autoregressive decoding is compressed using the same bucket structure, reducing decoding memory by an additional 18% on top of the encoder savings.

These figures are measured under realistic deployment conditions: float16 precision, FlashAttention-style fused kernels for both the dense and sparse baselines, and batch sizes selected to saturate each GPU. The savings hold across a wide range of model sizes; we report numbers for 1.3B, 7B, 13B, and 30B variants in Appendix B.

## 4.2 Throughput and latency

Memory savings translate into throughput gains when they enable larger batch sizes. At 32k context length, SparseFormer fits a batch of 24 sequences on a single H100, compared with 14 for the dense baseline, yielding a 1.71× throughput improvement on prefill-heavy workloads. For decoding, where the bottleneck is memory bandwidth on the key/value cache, SparseFormer achieves a 1.43× speedup at 32k context and a 1.92× speedup at 128k. End-to-end, on the LongBench inference suite, SparseFormer reduces the median request latency by 28% relative to the dense baseline at equal model quality.

The custom CUDA kernel described in Section 3.4 is responsible for roughly half of these gains; the rest comes from the underlying architectural sparsity. A pure-PyTorch reference implementation of SparseFormer achieves about 60% of the speedup of the fused kernel, demonstrating that the architecture is amenable to efficient implementation but benefits significantly from hardware-aware engineering.

## 4.3 Downstream task accuracy

We evaluate SparseFormer on seven downstream benchmarks: MMLU, HellaSwag, ARC-Challenge, GSM8K, HumanEval, LongBench-QA, and Needle-in-a-Haystack at 64k. SparseFormer achieves 97.3% of dense-attention accuracy on average, with no benchmark showing a degradation larger than 4.2%. The most challenging case is Needle-in-a-Haystack at 64k, where the model must retrieve a single fact from a long distractor context; the adaptive locality prior must select the correct bucket containing the needle, which is harder when the needle is short and the distractor density is high. Even in this adversarial setting, SparseFormer recovers 94.1% of the dense baseline's recall.

On the four benchmarks where we have matched compute-equivalent runs (the dense baseline trained to consume the same FLOPS as the SparseFormer model), SparseFormer actually *outperforms* the dense baseline by an average of 1.8 points. We attribute this to the regularising effect of the sparsity mask, which prevents the model from overfitting to spurious long-range correlations in the training mixture.

## 4.4 Training stability

A common failure mode of sparse-attention models is unstable pretraining: the discrete mask interacts poorly with optimisation, leading to loss spikes or divergence. We did not observe any such instability across the 12 pretraining runs that contributed to this paper. The straight-through gradient estimator and the auxiliary coverage and load-balancing losses keep the optimisation well-conditioned throughout training. The loss curves of SparseFormer and the dense baseline are visually indistinguishable for the first 300 billion tokens, after which the dense baseline diverges from the optimal trajectory due to memory pressure forcing a reduction in effective batch size.

## 4.5 Ablations

We include three ablations in the main paper. First, replacing the learned ALP with a fixed local window of equivalent budget loses 9.4 accuracy points on average — confirming that the learned prior, not merely the sparsity, is responsible for SparseFormer's quality. Second, removing the coverage auxiliary loss causes the mask to collapse to a near-local pattern after 100B tokens, with corresponding accuracy degradation. Third, increasing the per-query budget `k` from 128 to 256 yields only a 0.7-point average improvement, indicating that 128 active keys is already near the quality plateau for our base architecture.
