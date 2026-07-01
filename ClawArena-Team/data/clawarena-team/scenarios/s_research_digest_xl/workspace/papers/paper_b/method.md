# 3. Method

ClusterMoE consists of two components that work in tandem: a one-time **expert clustering** procedure that determines how experts are partitioned across devices, and a runtime **pipeline-parallel scheduler** that orchestrates communication and compute. The two components are designed independently and can be deployed individually, but they are most effective when combined.

## 3.1 Expert clustering

The goal of clustering is to assign the `E` experts in an MoE model to `D` devices such that the expected fraction of tokens whose routing destination is the local device is maximised. Formally, given an empirical co-activation matrix `C ∈ R^{E×E}` (where `C_{ij}` is the empirical probability that experts `i` and `j` are both activated on the same token), we seek a partition `π : [E] → [D]` that maximises `Σ_{i,j} C_{ij} · 1[π(i) = π(j)]` subject to a load-balancing constraint that each device hold roughly `E/D` experts.

This is a classical balanced graph partitioning problem, and we solve it with a standard multi-level spectral algorithm (METIS-style). The co-activation matrix `C` is constructed from a calibration set of 500K tokens sampled from production traffic; we found that this calibration is robust across input distribution shifts as long as the underlying task family does not change. For models that serve heterogeneous task mixes (for example, both code completion and conversational dialogue), we maintain a separate clustering per task family and switch between them based on the request route.

The clustering is computed once per model release and stored as a small JSON manifest. It costs about 90 seconds on a single CPU core for a 64-expert model and has been negligible relative to the cost of the model release pipeline.

## 3.2 Pipeline-parallel scheduler

Even after clustering, some tokens require communication across device boundaries. ClusterMoE's scheduler is designed to overlap this communication with compute so that the network does not appear on the critical path.

The scheduler partitions each MoE layer into three phases: **local compute**, in which each device runs experts on the tokens that were routed to it locally; **cross-device transfer**, in which non-local tokens are sent to their destination devices; and **remote compute**, in which each device runs experts on tokens it received from elsewhere. In a naïve schedule, these phases run serially and the cross-device transfer phase appears as a bubble in the timeline. ClusterMoE instead pipelines the phases across consecutive layers: while layer `L+1` is doing its local compute, layer `L`'s cross-device transfer is in flight on the network. Because the network bandwidth is provisioned to match the compute throughput, the two phases roughly balance, and the cross-device transfer hides entirely under the local compute of the subsequent layer.

The scheduler is implemented as a thin wrapper around standard NCCL primitives and adds approximately 300 lines of code on top of an existing expert-parallel runtime. The implementation is publicly released as a drop-in replacement for the expert-parallel layer in HuggingFace Transformers and DeepSpeed-MoE.

## 3.3 Capacity factor and overflow handling

A practical consideration for any MoE deployment is what to do when a device receives more tokens than its experts can process within the allotted time slice. The standard mitigation is to set a **capacity factor** that caps the number of tokens any expert will process; overflow tokens are then either dropped (degrading quality) or rerouted (incurring an extra communication round). ClusterMoE's locality-aware partitioning reduces the frequency and severity of overflow by an order of magnitude because the correlated experts that would otherwise create hotspots are now on the same device and can share their capacity dynamically.

Concretely, ClusterMoE replaces the per-expert capacity cap with a per-device cap: as long as the total work assigned to a device is within budget, any individual expert on that device may exceed its nominal share. This requires a small modification to the gating function's overflow-handling logic, which we describe in Appendix A.

## 3.4 Interaction with the gating function

ClusterMoE does not modify the gating function during training, which means it can be applied to any pretrained MoE without retraining. However, models trained with a *device-aware* auxiliary loss (which penalises gating decisions that create cross-device traffic) cluster slightly better in our experiments: the gating function learns to prefer experts whose activation patterns are mutually correlated, which makes the subsequent partitioning step easier. We provide a reference implementation of the device-aware auxiliary loss and report numbers for both pretrained and device-aware variants in the next section.
