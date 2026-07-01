# 4. Results

We evaluate ClusterMoE on a 64-expert, 70B total-parameter MoE model trained on a standard 1.5T-token mixture. All inference experiments use 8×H100 SXM5 GPUs connected by NVLink within a node; cross-node experiments use 200Gb InfiniBand. Baselines are the standard expert-parallel implementation in DeepSpeed-MoE and the more recent tutel framework.

## 4.1 Latency

The primary result of this paper is that **mixture-of-experts cuts inference latency by 35%** compared to the expert-parallel baseline. The 35% number is measured as the median end-to-end response latency on the LongChat-1.5 evaluation suite at batch size 32, sequence length 4096, and decoding length 512. At smaller batch sizes (1, 4) the speedup grows to 42% because the relative cost of communication is higher when there is less compute to hide it under. At larger batch sizes (128, 512) the speedup is more modest at 26% because the communication has already been amortised across many tokens by the baseline.

The latency reduction breaks down into three components, which we measure separately by selectively disabling parts of ClusterMoE. The clustering itself (without the pipeline scheduler) accounts for 18 percentage points of the reduction by virtue of reducing cross-device traffic. The pipeline scheduler accounts for 11 points by hiding the residual cross-device traffic under local compute. The remaining 6 points come from the per-device capacity cap, which reduces the frequency of overflow events and the associated synchronisation stalls.

## 4.2 Throughput

Throughput improvements track latency improvements at small batch sizes but converge at large batch sizes where the system is compute-bound regardless of MoE topology. At batch size 32, ClusterMoE achieves 1.54× the throughput (tokens per second per GPU) of the expert-parallel baseline. At batch size 512, the improvement is 1.21×, still material but no longer dominant.

## 4.3 Quality

ClusterMoE is a deployment-time optimisation and does not change any model parameters; we therefore expect downstream quality to be identical to the baseline. We verify this by running the model on six standard benchmarks (MMLU, HellaSwag, MT-Bench, HumanEval, GSM8K, BBH) under both ClusterMoE and expert-parallel deployment, and we find quality differences of less than 0.2% on every benchmark — well within the noise of generation-based evaluation. The capacity-cap modification described in Section 3.3 does cause a small number of tokens to be processed by a non-preferred expert under extreme load, but our measurements indicate that this affects fewer than 0.05% of tokens at the operating points we consider.

## 4.4 Network sensitivity

A key practical question is how the latency benefit changes with network bandwidth. We sweep the inter-device bandwidth from 25 GB/s (typical of PCIe deployments) to 600 GB/s (NVLink) by software throttling. At low bandwidth, where communication dominates the baseline cost, ClusterMoE delivers up to a 48% latency reduction. At high bandwidth, where communication is already cheap, the reduction shrinks to 22%. ClusterMoE thus provides a "free" speedup on premium NVLink deployments and a transformative speedup on budget PCIe deployments — the latter being the more common case in production inference fleets.

## 4.5 Cross-node deployment

For models that exceed single-node memory, we benchmark ClusterMoE on a 16-GPU configuration spanning two nodes connected by 200Gb InfiniBand. In this regime, cross-node communication is roughly 10× slower than intra-node, so the locality-aware clustering becomes especially valuable: 87% of tokens stay within the originating node compared with 50% under uniform expert-parallel placement, and the resulting latency reduction widens to 41%.

## 4.6 Ablations

Two ablations are worth highlighting. First, replacing the spectral clustering algorithm with random partitioning eliminates 17 of the 35 percentage points of latency reduction, confirming that the cluster structure of the co-activation matrix is meaningful and that random placement is far from optimal. Second, replacing the pipeline scheduler with a synchronous (non-pipelined) schedule reclaims 9 points of latency cost, indicating that the pipelining contribution is large even when the clustering has already reduced raw communication volume.
