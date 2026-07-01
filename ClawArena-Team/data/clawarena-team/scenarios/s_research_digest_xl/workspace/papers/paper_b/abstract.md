# Efficient Mixture-of-Experts Inference via Expert Clustering and Pipeline Parallelism

**Authors:** Benjamin Okafor¹, Mei Lin Zhao², Sven Reinhardt³, Ananya Iyer¹

¹ Stanford Inference Lab, ² Peking University NLP Group, ³ ETH Zürich

**Venue:** Proceedings of ICML 2026

## Abstract

Mixture-of-Experts (MoE) architectures offer a compelling path to scaling language models without proportional increases in inference cost. However, existing MoE deployments suffer from load imbalance and inter-device communication bottlenecks that limit their practical throughput. In this paper we introduce **ClusterMoE**, a deployment framework that groups experts by learned activation similarity and co-locates them on the same device, combined with a novel pipeline-parallel inference scheduler. Our key finding is that **mixture-of-experts cuts inference latency by 35%** compared to naïve expert-parallel baselines, measured on a 64-expert, 70B total-parameter model on 8×H100 hardware. We validate ClusterMoE on six generation benchmarks and demonstrate consistent latency improvements across batch sizes 1–512.

**Keywords:** mixture of experts, inference latency, expert clustering, pipeline parallelism
