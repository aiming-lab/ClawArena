# 4. Results

We evaluate FedAlign on three federated fine-tuning benchmarks: a medical-records domain adaptation task, a customer-support chat domain adaptation task, and a multilingual instruction-following task. Each benchmark provides a centralised training set (used to compute the centralised-fine-tuning baseline) and a federated split that partitions the data across 32 simulated clients along a realistic non-IID axis. The base model is a Llama-3 8B checkpoint, and we report results both for full-parameter fine-tuning and for LoRA fine-tuning.

## 4.1 Privacy-accuracy trade-off

The headline finding of the paper is that **federated learning preserves privacy with only 8% accuracy drop** relative to centralised, non-private fine-tuning, under a strict (ε=2, δ=10⁻⁵) differential privacy guarantee. The 8% figure is the average across the three benchmarks for the full-parameter fine-tuning configuration. The breakdown is: 9% on the medical task, 7% on the customer-support task, and 8% on the multilingual task.

The corresponding number for DP-FedAvg (vanilla DP federated learning without the alignment regulariser) under the same privacy budget is 27%. FedAlign therefore closes the gap by 19 percentage points, which is the largest reported improvement over DP-FedAvg of which we are aware.

For LoRA fine-tuning, the accuracy drop is slightly smaller (6%, averaged across benchmarks), because LoRA's lower-dimensional parameter space requires less noise to achieve the same privacy guarantee. LoRA-FedAlign is therefore our recommended configuration for resource-constrained deployments.

## 4.2 Comparison to non-private federated baselines

To isolate the contribution of the alignment regulariser independently of the privacy mechanism, we also run experiments without DP. Under no privacy mechanism, FedAlign closes 81% of the gap between vanilla FedAvg and centralised training, compared with 53% for FedProx and 64% for SCAFFOLD. The alignment regulariser therefore meaningfully outperforms existing client-drift mitigations, and the advantage is preserved when DP noise is added.

## 4.3 Data heterogeneity sweep

A key practical question is how the benefit of FedAlign varies with the degree of client heterogeneity. We simulate three heterogeneity regimes by varying the Dirichlet concentration parameter `α` that governs the federated split: `α = 10` (mild heterogeneity), `α = 1` (moderate), and `α = 0.1` (severe).

Under mild heterogeneity, FedAvg performs reasonably and FedAlign's improvement is modest (3 percentage points relative to FedAvg). Under moderate heterogeneity, FedAvg's accuracy drops by 12 points and FedAlign recovers 9 of them. Under severe heterogeneity, FedAvg's accuracy drops by 23 points and FedAlign recovers 18. The alignment regulariser therefore delivers the largest benefit in exactly the regime where it is most needed.

## 4.4 Communication overhead

The communication overhead of FedAlign relative to DP-FedAvg is the broadcast of the anchor representations, which we measure at 1.1% of the per-round bytes for our 8B model. The end-to-end wall-clock overhead, measured on a simulated network with 100 Mb/s client uplinks, is 1.8% per round. Both overheads are well within the noise of practical federated deployments.

## 4.5 Ablations

We run three ablations. First, removing the alignment regulariser entirely (keeping DP-SGD and FedAvg) recovers DP-FedAvg performance, confirming that the regulariser is responsible for the accuracy improvement. Second, replacing the selective clipping with naïve clipping of the full gradient costs 4 percentage points, demonstrating that selective clipping is a meaningful contributor. Third, varying the number of anchor inputs from 256 to 16K shows a logarithmic improvement up to roughly 4K anchors, after which further anchors yield negligible benefit; we use 4K as our default.

## 4.6 Privacy guarantees

We use the moments accountant to compute the differential privacy guarantee. Under our default configuration of 100 rounds of training with a noise multiplier of 1.1 and a clipping norm of 1.0, the cumulative privacy spend is (ε=2.04, δ=10⁻⁵). The accountant matches the empirically observed privacy under a membership inference attack: the attack's AUC is 0.51, very close to the random-guessing baseline of 0.5.
