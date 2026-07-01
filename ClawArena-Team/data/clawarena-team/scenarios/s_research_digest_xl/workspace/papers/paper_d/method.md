# 3. Method

DistillAlign is structured as a three-stage training procedure: (1) a *tutor* model runs the full Constitutional AI critique loop on a corpus of prompts, generating synthetic preference data; (2) a *reward model* is trained on the preference data; (3) the *student* language model is fine-tuned with PPO against the reward model. Each stage uses standard components, and the system is intentionally designed to slot into existing RLHF infrastructure.

## 3.1 Tutor and constitution

The tutor is a frozen, pretrained language model, typically smaller than the student. In our default configuration, we use a 13B-parameter tutor and a 70B-parameter student; we find that the tutor's quality has a much smaller effect on downstream alignment than one might expect, because the constitutional principles do most of the work.

The constitution is a set of `n` principles in natural language. We use the published Anthropic constitution as a starting point, augmented with five additional principles that reflect our deployment requirements (concerning code-generation safety, medical claims, financial advice, and two domain-specific scenarios). The principles are stable across all of our experiments and are listed verbatim in Appendix A.

For each prompt in the corpus, the tutor produces an initial response, then critiques the response against each principle in turn ("Is this response problematic with respect to principle `k`? Identify any issues."), then produces a revised response that addresses the critique. We run two rounds of critique-and-revise, which we find gives diminishing returns beyond round two. The initial and final responses are then packaged as a synthetic preference pair: the revised response is preferred over the initial response.

We generate 1.2 million such preference pairs from a prompt corpus that mixes (a) public instruction-following datasets, (b) red-teaming prompts from public sources, and (c) de-identified production traffic from our own deployment.

## 3.2 Reward model training

The reward model is a standard transformer encoder with a scalar head. It is trained on the synthetic preference data using the Bradley-Terry maximum-likelihood objective:

```
L = - log σ(r(prompt, preferred) - r(prompt, dispreferred))
```

We use a 1.3B-parameter reward model — small enough to be cheap to query during PPO but large enough to learn the constitutional reasoning encoded in the synthetic preferences. We initialise the reward model from a publicly available instruction-tuned checkpoint and train for two epochs over the preference data with the AdamW optimiser.

A key implementation detail is the use of a *principle-conditioned* training objective for the first epoch. Each preference pair is associated with the constitutional principle that the critique invoked, and we condition the reward model on this principle by prepending it to the input. This conditioning produces a small but consistent improvement in alignment quality, presumably because it forces the reward model to internalise the principle structure rather than memorising surface statistics of the preference data. We drop the conditioning at inference time, so the reward model still operates as a standard scalar scorer in the PPO loop.

## 3.3 Student PPO

The student is fine-tuned against the reward model using PPO, exactly as in standard RLHF. We use the trlx implementation of PPO with one modification: a per-batch KL penalty against a frozen reference model, which we find prevents the early-training collapse that sometimes occurs when the reward model is overconfident on out-of-distribution prompts.

The student is not exposed to the constitution directly during PPO; all of the constitutional information is encoded in the reward model. This is the key design choice that makes DistillAlign cheap relative to vanilla Constitutional AI: the expensive multi-pass critique runs once per prompt during the synthetic-data generation stage and is then amortised across all student updates.

## 3.4 Iterative distillation

In settings where the constitution evolves over time (for example, a new principle is added in response to a discovered failure mode), DistillAlign supports incremental updates without full retraining. We re-run the tutor on a small batch of prompts using the updated constitution, train a delta-reward model on the new preference data, and combine the delta with the base reward model as a weighted sum. The weighting parameter is tuned on a small validation set. We have used this procedure three times during the year-long development of DistillAlign and find it scales well to constitutions of up to 40 principles.

## 3.5 Compatibility with existing pipelines

DistillAlign produces a reward model that is interchangeable with any other RLHF reward model. The PPO loop, the optimisation hyperparameters, and the orchestration layer all remain unchanged from a standard RLHF deployment. Organisations adopting DistillAlign therefore do not need to overhaul their training infrastructure; they need only to obtain or train a constitutional reward model.
