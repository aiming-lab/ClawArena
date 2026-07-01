# 4. Results

We evaluate NSR on three compositional generalisation benchmarks: SCAN, COGS, and CFQ. Each benchmark provides multiple splits that vary the type of compositional generalisation required (primitive transfer, length extrapolation, novel operator combinations). We report the mean accuracy across the official splits for each benchmark. Baselines include a transformer-from-scratch trained on the benchmark training set, a T5-fine-tuned variant, a recent neural-only state-of-the-art (DiT-Compose), and a vanilla single-parse version of NSR.

## 4.1 Headline accuracy

The main result of the paper is that **neurosymbolic reasoning achieves 91% accuracy on compositional tasks** across SCAN, COGS, and CFQ, averaged over the standard evaluation splits. The breakdown is: 96% on SCAN, 92% on COGS, and 85% on CFQ. The best neural baseline (DiT-Compose) achieves 73% on the same evaluation: 87% on SCAN, 71% on COGS, and 61% on CFQ. NSR therefore improves average accuracy by 18 percentage points, with the largest gains on the most difficult benchmark (CFQ, +24 points).

On the SCAN length-extrapolation split, where the test utterances are longer than any seen during training, the gap widens further: NSR achieves 94% versus the neural baseline's 51%. Compositional generalisation to longer inputs is a benchmark stress test that purely neural systems consistently fail on, and NSR's symbolic execution component avoids the failure mode entirely because the executor's behaviour is length-independent by construction.

## 4.2 Generalisation to unseen operator combinations

A unique strength of NSR is its ability to handle operator combinations that did not appear in any training data. We construct a held-out set in which the in-context examples for the parser cover every primitive but only a strict subset of pairwise combinations; the test utterances require combinations the parser has never been shown. NSR achieves 89% accuracy on this set; the best neural baseline achieves 47%. The 42-percentage-point gap reflects the systematic-composition property that the symbolic executor confers and that neural models fundamentally lack.

## 4.3 Ablation: multiple parses

The multiple-parse decoding strategy contributes substantially to NSR's performance. Reducing the number of candidate parses from 8 to 1 (greedy decoding) costs 7 percentage points of average accuracy. Reducing it to 4 costs 3 points. Increasing it to 16 yields negligible improvement. We use 8 as the default for a good balance of accuracy and inference cost.

## 4.4 Ablation: verifier

Removing the verifier and selecting the executable parse with the highest parser likelihood costs 5 percentage points of accuracy on average. The cost is largest on the splits that include semantic ambiguity — for example, the COGS subject-object split — where multiple parses are syntactically valid but only one matches the intended semantics.

## 4.5 Cross-domain verifier transfer

We measure whether a verifier trained on SCAN transfers to COGS and CFQ without retraining. The transferred verifier loses 4 percentage points on COGS and 7 points on CFQ relative to a verifier trained on the target domain. The drop is meaningful but not catastrophic, and it suggests that practitioners adopting NSR for a new domain can begin with a transferred verifier and retrain it once domain-specific labelled data becomes available.

## 4.6 Inference cost

NSR's inference cost is dominated by the parser's multiple-decode step. With 8 candidate parses, the parser cost is roughly 4× that of a single greedy decode (parallelisable across the GPU). The executor's cost is negligible (sub-millisecond per parse for SCAN; tens of milliseconds for CFQ due to the larger knowledge graph). The verifier costs roughly 30 ms per parse. Total inference latency is approximately 1.4× that of a greedy neural baseline of the same parser size, which we consider an acceptable cost for the accuracy gains.

## 4.7 Error analysis

A qualitative analysis of NSR's failures reveals three error categories. The most common (54% of errors) is **parsing failure**: none of the 8 candidate parses captures the intended meaning. The second (31%) is **executor mismatch**: the candidate parses are syntactically correct but the verifier selects the wrong one. The third (15%) is **knowledge-base gap**: the parse is correct and the verifier ranks it correctly, but the underlying knowledge base does not contain the information needed to answer.

Parsing failures cluster on utterances that use uncommon primitive combinations or unusual surface forms. They tend to be addressable by adding additional in-context examples; we report a small sweep over the number of examples in Appendix B.
