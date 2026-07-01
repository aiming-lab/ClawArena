# 3. Method

FaithRAG is built on top of a standard RAG pipeline. At inference time, the system retrieves the top-`k` passages from a dense index over the source corpus, prepends them to the user's query, and runs an autoregressive decoder. FaithRAG modifies only the *decoding* step: the retrieval stage is unchanged, and the underlying language model is not re-trained. This section describes the three components that make up the modification: the attribution scorer, the constrained decoding objective, and the temperature schedule that governs the fluency-faithfulness trade-off.

## 3.1 Attribution scorer

The attribution scorer is a small bidirectional encoder (roughly 110M parameters in our default configuration) that assigns each candidate next token `t` an attribution probability `a(t | context, passages)` — informally, the probability that `t` would be supported by at least one retrieved passage if the entire continuation following `t` were natural language. The scorer is trained on a dataset of (query, passage, faithful-continuation, unfaithful-continuation) tuples, where the faithful continuations are extracted from human-written answers grounded in the passages and the unfaithful continuations are mined from real RAG outputs that an external evaluator marked as hallucinated.

The scorer operates on the concatenation of the retrieved passages and the current decoded prefix, plus the candidate next token. Critically, it does not require access to the language model's internal states, which makes it compatible with closed-weight APIs that expose only token-level logits and outputs. The scorer is small enough (≈ 220 ms per decoding step on a single H100) that it adds only modest latency overhead to the overall RAG pipeline.

For training the scorer, we collect 1.2M tuples from a mixture of publicly available RAG evaluation datasets, augmented with our own production traffic (de-identified, with consent). The scorer is trained with a contrastive log-likelihood objective that pushes faithful tokens above unfaithful ones in the per-token attribution score.

## 3.2 Constrained decoding objective

At each decoding step, the language model produces a logit vector `ℓ ∈ R^V` over the vocabulary, where `V` is the vocabulary size. Standard decoding selects the next token as `argmax(ℓ)` (for greedy decoding) or samples from `softmax(ℓ / T)` for a chosen temperature `T`. FaithRAG instead samples from a *constrained* distribution:

```
p_faith(t) ∝ exp((ℓ(t) + λ · log a(t | context, passages)) / T)
```

The constraint term `λ · log a(t)` shifts the logit distribution toward tokens that are well-supported by the retrieved passages. The hyperparameter `λ ≥ 0` controls the strength of the constraint: `λ = 0` recovers ordinary RAG decoding, and `λ → ∞` forces the decoder to select only tokens with non-negligible attribution probability. In practice, values of `λ` between 1.5 and 3.0 give the best balance, with the optimum depending on the application's tolerance for ungrounded generation.

We compute the constrained distribution only on the top-`m` candidate tokens by logit (with `m = 50` in our default configuration), which keeps the per-step cost of the attribution scorer bounded. Tokens outside the top-`m` are assigned attribution score 0 and effectively excluded from the constrained distribution.

## 3.3 Annealed temperature schedule

A constant `λ` is suboptimal at boundary cases: at the very start of a generation, there is little prefix for the attribution scorer to condition on, and high `λ` can be over-conservative; at the end, after the decoder has committed to a particular framing, the constraint is most needed. We therefore use a simple linear annealing schedule that ramps `λ` from `λ_min` at the first decoded token to `λ_max` by the 32nd. The annealing parameters are tuned once per application using a small held-out validation set.

## 3.4 Compatibility with existing pipelines

A practical design goal of FaithRAG is that it should compose with any pre-existing RAG stack. The attribution scorer takes the same inputs as the generator (the retrieved passages and the current prefix) and produces a per-token score; it does not require changes to the retriever, the generator's weights, or the orchestration layer. We provide a thin wrapper that intercepts the generator's logits, queries the scorer, and produces the constrained distribution. The wrapper is roughly 200 lines of Python and has been integrated with three different popular RAG frameworks during the development of this paper.
