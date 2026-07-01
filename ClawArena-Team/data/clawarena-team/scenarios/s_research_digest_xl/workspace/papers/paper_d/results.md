# 4. Results

We evaluate DistillAlign on toxicity, helpfulness, and training cost. Our experiments use a 13B-parameter student model trained from a publicly available instruction-tuned checkpoint. The reward model is a 1.3B-parameter encoder. Baselines are: (i) the same checkpoint without further alignment ("SFT-only"); (ii) the same checkpoint after standard RLHF using a reward model trained on a 200K-pair human-labelled preference dataset; and (iii) the same checkpoint after vanilla Constitutional AI training, using the same constitution as DistillAlign but with the critique loop applied at every PPO step.

## 4.1 Toxicity

The headline finding of the paper concerns the ToxicBench suite, a collection of 8K adversarial prompts derived from Real-Toxicity-Prompts and a curated set of jailbreak-style attacks. We measure the fraction of generated responses that exceed a moderate-toxicity threshold under the Perspective API. The SFT-only baseline produces toxic outputs on 14.2% of prompts; standard RLHF reduces this to 8.7%; **constitutional AI alignment reduces toxicity by 52%** on ToxicBench compared with the RLHF-only baseline, bringing the toxic-output rate to 4.2%. Vanilla Constitutional AI achieves a similar 4.5% rate, confirming that DistillAlign matches the alignment quality of the full critique loop while avoiding its training cost.

We additionally evaluate on the BBQ social-bias benchmark and a held-out internal red-teaming set. DistillAlign improves on standard RLHF by 38% relative on BBQ and by 47% relative on the red-teaming set. The improvements are uniform across the demographic categories that the benchmarks separately stratify.

## 4.2 Helpfulness

Aggressive alignment risks producing models that refuse legitimate requests or hedge unnecessarily — an effect sometimes referred to as the "alignment tax". We measure helpfulness on three standard benchmarks: MT-Bench, AlpacaEval-2.0, and a curated set of 500 production-derived help-seeking prompts. DistillAlign loses 0.6 points of MT-Bench score relative to standard RLHF (a small but measurable degradation) and 1.1 points of AlpacaEval win rate. On the production help-seeking set, the human-annotated helpfulness rating drops by 2.4% relative.

These costs are within the range typically observed for alignment interventions and are substantially smaller than the cost we observed when running vanilla Constitutional AI, which lost 1.8 MT-Bench points and 2.9 AlpacaEval points. We attribute DistillAlign's smaller helpfulness penalty to the principle-conditioned reward-model training, which produces a reward model that is more selective about what constitutes a violation.

## 4.3 Training cost

DistillAlign training proceeds in three stages: (1) tutor-driven preference data generation, (2) reward model training, (3) PPO. The first two stages are one-time costs that are amortised over all subsequent applications of the reward model. The third is comparable in cost to a standard RLHF run.

For our 13B student, the total training cost is approximately 280 GPU-hours, dominated by PPO. Vanilla Constitutional AI at the same scale costs approximately 900 GPU-hours due to the per-step critique overhead. DistillAlign is therefore 3× cheaper to train. When the reward model is reused across multiple student trainings or model iterations (a common situation in production deployment), the savings widen further: the first 13B student costs 280 GPU-hours, but each subsequent student costs only 230 (the PPO portion alone).

## 4.4 Robustness to distribution shift

We test DistillAlign on three out-of-distribution prompt collections: (i) prompts from a non-English language (German); (ii) prompts from a domain not represented in the constitutional principles (programming-language code completion); and (iii) prompts crafted by a separate red team to bypass the alignment. In all three cases, DistillAlign retains a substantial fraction of its alignment benefit: 64% of the relative toxicity reduction on German, 71% on code, and 58% on the adversarial set. The drop is real but not catastrophic, and it is comparable to the corresponding drop for vanilla Constitutional AI.

## 4.5 Ablations

We run three ablations. First, removing the principle-conditioned training objective from reward-model training reduces ToxicBench performance by 9% relative, demonstrating that the conditioning is a meaningful contributor and not merely a regularisation trick. Second, reducing the synthetic preference dataset from 1.2M to 200K pairs reduces ToxicBench performance by 14%, confirming that the synthetic data scale matters. Third, using a smaller (0.4B-parameter) reward model loses 7% relative on ToxicBench, indicating that the reward model can be downsized but at a measurable quality cost.
