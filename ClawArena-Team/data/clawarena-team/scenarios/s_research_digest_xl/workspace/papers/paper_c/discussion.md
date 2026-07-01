# 5. Discussion

FaithRAG demonstrates that a substantial fraction of RAG's reliability problems are decoding-time rather than retrieval-time, and that they can be addressed by an auxiliary scorer combined with a constrained decoding objective. Here we situate the work, discuss its limitations, and consider deployment implications.

## 5.1 Related work

There are several adjacent lines of work. The classical RAG framework introduced retrieval as a method for grounding generation; subsequent work has improved retrieval quality (dense retrievers, hybrid retrievers, learned rerankers) and integrated retrieval into training (REALM, RETRO, Atlas). These efforts make the input to the decoder more informative but do not change the decoder's tendency to drift away from that input. FaithRAG complements them rather than replacing them.

Constrained decoding has been studied in machine translation (constrained beam search) and in safety-oriented decoding (FUDGE, GeDi, NeuroLogic). The closest of these is FUDGE, which uses a future-discriminator to constrain decoding. FaithRAG differs in two respects: the attribution scorer is a context-conditional model rather than a future predictor, and the constraint is calibrated by an attribution interpretation rather than a free-form classifier. The result is a constraint that is interpretable and amenable to standard NLI-style debugging.

There has also been work on "faithfulness" classifiers used at evaluation time rather than at decoding time. These classifiers — FactCC, QAFactEval, and others — serve as benchmark tools rather than runtime mitigations. We use FactCC in our evaluation precisely because it was trained on a different distribution from our attribution scorer, which avoids the circularity of using the same model both to enforce a constraint and to evaluate compliance with it.

## 5.2 Limitations

Three limitations are worth noting. First, FaithRAG's effectiveness depends on the quality of the attribution scorer, which in turn depends on the diversity and realism of its training data. Our scorer is trained on English text and on tasks similar to TruthfulQA and FActScore; it has not been evaluated on multilingual or code-generation RAG, where the notion of "attribution" is different.

Second, the constraint can produce conservative refusals when no candidate token has high attribution probability — for example, when the retrieved passages are off-topic. We have implemented a fallback that gracefully degrades to standard RAG decoding in such cases, but the fallback can mask retrieval failures from the application layer. Production deployments should monitor the rate at which the fallback fires.

Third, the attribution scorer's latency overhead is meaningful (≈ 30% in our default configuration), and the distilled variant trades quality for latency. We expect this overhead to shrink as small-model architectures improve, but for the moment FaithRAG is best suited to applications where factuality is more valuable than the last 30% of decoding throughput.

## 5.3 Deployment considerations

We have deployed FaithRAG in a real-world legal-research product where hallucination is a regulatory concern. Three operational observations may be useful for similar deployments. First, the appropriate `λ` value varies substantially by query category: factual lookups benefit from high `λ`, while open-ended synthesis questions are best served by lower `λ`. We learn the per-category `λ` from production telemetry. Second, the fallback rate is a useful early signal for retrieval-quality regressions, often before they are visible in downstream metrics. Third, users sometimes notice that FaithRAG-generated answers are *shorter* than standard-RAG answers — a side effect of the constraint pruning ungrounded continuations — and may need product-level guidance about why brevity is sometimes a virtue.
