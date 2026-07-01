# 5. Discussion

DistillAlign demonstrates that the alignment benefits of Constitutional AI can be obtained without paying its training-time cost, by distilling the critique capability into a reward model that is then used in a standard RLHF loop. The result is a system that is cheaper, more operationally familiar, and easier to iterate than the original Constitutional AI proposal, while delivering comparable alignment quality. In this section we situate the work and discuss several considerations that affect responsible deployment.

## 5.1 Related work

DistillAlign sits at the intersection of three lines of work: RLHF, Constitutional AI, and model distillation. Within the RLHF literature, the closest precursors are reward-model-based approaches such as Anthropic's HH-RLHF and OpenAI's InstructGPT, which we treat as the standard baseline. Within the Constitutional AI literature, the closest precursor is the original Anthropic Constitutional AI paper, whose self-critique procedure we use as the tutor stage; subsequent work has explored variants of the critique loop but has generally retained the per-step overhead that DistillAlign eliminates.

Distillation has a long history in supervised learning, going back to Hinton et al. Within alignment, prior distillation work has focused on distilling response *quality* rather than alignment *behaviour*. DistillAlign is distinctive in that it distills the *evaluative* capability of the tutor — the ability to detect constitutional violations — rather than the tutor's response distribution itself. This distinction matters because evaluative capability is what the reward model needs, and it can be captured by a much smaller model than would be required to match the tutor's generation quality.

A complementary line of work, **process reward models** (PRMs), trains reward models on the intermediate reasoning steps that produce a final answer. DistillAlign is conceptually adjacent: the synthetic preference pairs encode the *reasoning* (the critique) that justifies the preference. We do not currently expose the reasoning explicitly to the reward model, but a hybrid PRM-style variant of DistillAlign is a natural extension and is the subject of ongoing work.

## 5.2 Limitations

DistillAlign's effectiveness depends on the quality of the tutor's constitutional critiques. A weak tutor produces synthetic preference data that does not adequately distinguish aligned from misaligned outputs, and the resulting reward model is correspondingly noisy. We have found that a 13B tutor is sufficient for the constitutions we have studied, but more complex constitutions (with subtler distinctions among principles) may require a stronger tutor.

The constitutional principles themselves are a hand-crafted artefact, and engineering a good constitution remains an art. DistillAlign does not solve this problem; it merely reduces the marginal cost of testing a candidate constitution against a downstream metric (because the tutor stage is the same, only the reward model needs to be retrained). We view this as a productivity multiplier for constitutional engineering rather than an automation of it.

DistillAlign is also susceptible to the well-known failure modes of reward-model-based RLHF: reward hacking, sycophancy, and over-optimisation. The KL penalty against a reference model in our PPO loop mitigates the most severe forms of these failures, but they remain a long-term concern and should be monitored in production.

## 5.3 Safety and dual-use considerations

DistillAlign reduces the cost of alignment, which is broadly a positive outcome. However, the same machinery could in principle be used to optimise a language model against a *misaligned* constitution — for example, a constitution that encodes the values of a particular ideology or commercial interest. Because the constitution is the only explicit articulation of the alignment goals, the integrity of the constitution itself becomes safety-critical. We recommend that production deployments treat the constitution as a versioned, reviewed artefact and audit changes to it with the same rigour as code changes to safety-critical systems.

We have engaged with external safety reviewers during the preparation of this paper and incorporated their feedback into both the constitution we publish and the operational recommendations in Appendix G.
