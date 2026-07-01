# 5. Discussion

ClusterMoE addresses two long-standing operational pathologies of MoE inference — load imbalance and communication overhead — by exploiting the empirical structure of expert co-activation rather than fighting against it. The resulting latency reductions are large in absolute terms and translate directly into cost savings for any deployment that meters inference time. In this section we situate the work, discuss its limitations, and outline practical considerations for adopters.

## 5.1 Related work

The MoE inference literature has produced several deployment frameworks. **DeepSpeed-MoE** introduced the expert-parallel baseline we compare against and remains the most widely deployed framework for MoE inference. **tutel** added expert replication and adaptive capacity factors to mitigate load imbalance at the cost of memory; ClusterMoE's per-device capacity cap is conceptually similar but is enabled by — and synergistic with — the clustering. **FasterMoE** introduced a hybrid expert-parallel-and-data-parallel scheme that we did not benchmark against directly because its assumptions (large batch sizes, small expert counts) do not match our deployment setting. **GShard** and **Switch-Transformer** are training-time frameworks rather than inference-time, and their conventions for capacity and routing have flowed through to most production MoE deployments.

The closest conceptual prior work is **expert co-location** as discussed in the GShard paper as a hypothetical optimisation. To our knowledge, ClusterMoE is the first system to operationalise this idea with a measured-co-activation clustering algorithm and a pipeline scheduler designed to exploit it.

## 5.2 Limitations

Several limitations are worth noting. First, ClusterMoE assumes that the co-activation matrix is stable over the deployment horizon. For models served on stationary task distributions (the typical production case), we have observed stability over months; for models exposed to rapidly evolving query distributions, periodic re-clustering may be required.

Second, the spectral clustering algorithm produces a static partition. Adaptive partitioning that responds to short-term traffic shifts is conceivable but introduces additional engineering complexity and risk; we have left it for future work.

Third, our experiments use models with 16 to 64 experts, which is typical of current production MoE designs. The clustering structure may degrade for much larger expert counts where co-activation correlations become weaker. We have run preliminary experiments at 128 experts (Appendix F) and the latency reduction is still 27%, suggesting that the approach scales gracefully, but more work is needed to characterise its limits.

Finally, ClusterMoE's benefits accrue primarily to inference; we did not evaluate it as a training-time optimisation, where the dynamics are quite different because the gating function is itself evolving.

## 5.3 Operational considerations

We deployed ClusterMoE in a production inference service serving roughly 4 billion tokens per day. Three operational lessons are worth recording. First, the clustering computation is fast enough that it can be regenerated as part of a routine model release pipeline; we do not need a separate workflow for it. Second, the pipeline scheduler interacts with the autoscaling system in non-obvious ways: because cross-device traffic is much lower under ClusterMoE, the network telemetry that the autoscaler had previously used as a load proxy became less informative, and we had to add new signals. Third, the per-device capacity cap occasionally produces "expert overflow" events under extreme load spikes; we recommend monitoring these events and treating sustained overflow as an autoscaling trigger.
