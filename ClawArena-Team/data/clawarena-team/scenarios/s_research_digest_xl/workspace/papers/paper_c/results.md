# 4. Results

We evaluate FaithRAG on three primary axes: factual accuracy, hallucination rate, and fluency. Our experiments use a Llama-3-derived 13B-parameter base generator and a 110M-parameter attribution scorer, both fine-tuned on the same instruction-following mixture. We compare against three baselines: (i) the same generator without retrieval; (ii) the generator with standard RAG (top-5 passage retrieval, unconstrained decoding); and (iii) RAG with a state-of-the-art reranker (RankZephyr) but unconstrained decoding.

## 4.1 Factual accuracy

The headline finding of this paper is that **retrieval augmentation boosts factual accuracy by 28%** on the combined TruthfulQA-Generation and FActScore benchmarks, where we compute the accuracy as the fraction of generations that are scored as factually correct by the benchmark's official evaluator. The 28% improvement is measured against the no-retrieval baseline. Against the standard-RAG baseline, FaithRAG adds an additional 11% improvement, which represents the contribution of the constrained decoding objective specifically (as distinct from the contribution of retrieval itself). Adding a reranker on top of standard RAG yields a smaller marginal improvement of 4%, confirming that reranking helps but cannot recover the gains that constrained decoding provides.

The improvements are consistent across the benchmark subsets. On the TruthfulQA-Health subset, where the correct answer often contradicts a popular misconception, FaithRAG outperforms standard RAG by 14% absolute. On the FActScore-Politicians subset, where the answer is typically a list of factual claims that must each be verifiable, FaithRAG improves the per-claim verification rate by 19%.

## 4.2 Hallucination rate

We measure hallucination rate using FactCC, a learned automatic factuality checker trained on a different distribution than our attribution scorer to avoid circular evaluation. The hallucination rate of standard RAG on our enterprise QA benchmark is 18.4%. FaithRAG reduces this to 10.9%, a relative reduction of 41%. The reduction is largest on questions where the retrieved passage contradicts the model's parametric belief — exactly the context-drift cases that motivated FaithRAG.

We additionally conduct a 200-example human evaluation. Annotators marked each generation as "fully grounded", "partially grounded", or "ungrounded". The grounded rate (fully + partially) increases from 71% under standard RAG to 89% under FaithRAG, with the fully-grounded rate rising from 48% to 73%.

## 4.3 Fluency and helpfulness

We are careful to assess whether the constraint harms generation quality. We measure fluency using MAUVE and per-token perplexity under a reference model, and helpfulness using win rates on MT-Bench. Under our default `λ` of 2.0, FaithRAG's MAUVE score drops by 1.2 points relative to standard RAG (a small but measurable decrease) and the perplexity rises by 4%. MT-Bench win rate drops by 1.8 points. These are modest costs given the factuality gains, and they shrink further at lower `λ` values.

To make the fluency-faithfulness trade-off explicit, we report a Pareto sweep over `λ` in the range [0, 5]. The Pareto frontier is concave: small `λ` purchases large faithfulness gains for small fluency costs, and the marginal trade-off worsens at higher `λ`. Practitioners should typically operate near the knee, around `λ` = 1.5-2.5.

## 4.4 Latency overhead

The attribution scorer adds approximately 220 ms per decoded token on a single H100, which is roughly 30% of the generator's own per-token latency. For applications where latency is critical, we provide a distilled 35M-parameter variant of the scorer that runs in 75 ms per token at the cost of 0.8 points of factual accuracy. The full and distilled scorers are released alongside the paper.

## 4.5 Ablations

We ablate three components of FaithRAG. First, removing the attribution scorer and replacing it with a simple lexical-overlap heuristic recovers only 9 of the 11 percentage points of factuality improvement, demonstrating that the learned scorer materially outperforms a rule-based proxy. Second, removing the temperature annealing schedule (using a constant `λ` = 2.0) loses 2 percentage points of factuality and increases the rate of refusals (the generator declining to answer). Third, training the attribution scorer on only the public datasets without the de-identified production traffic loses 3 points of factuality, indicating that real RAG-failure examples are a valuable training signal.
