# 3. Method

NSR consists of three components: a *parser* that maps natural language utterances to typed lambda calculus programs, an *executor* that evaluates the programs against a structured knowledge base, and a *verifier* that ranks candidate parses by their executability and semantic plausibility. The pipeline is depicted in Figure 1 of the paper; below we describe each component in turn.

## 3.1 Parser

The parser is a pretrained large language model (we use a 7B-parameter model in the default configuration, though the approach works with models from 1B to 70B). The model is prompted with a brief instruction, the symbolic vocabulary (a list of typed primitives appropriate to the task domain), and a small number of in-context examples. Given a natural language utterance, the parser produces a typed lambda calculus expression that is intended to denote the utterance's meaning.

A typical example, drawn from the SCAN benchmark, is the utterance "jump twice and turn left". The parser is expected to produce the expression:

```
SEQ(REPEAT(JUMP, 2), TURN_LEFT)
```

where `SEQ`, `REPEAT`, `JUMP`, and `TURN_LEFT` are primitives in the SCAN vocabulary. The parser is not given the expression directly — it must learn to produce it from the in-context examples and from its pretraining knowledge of compositional language.

A critical design choice is that the parser produces *multiple* candidate parses per utterance (typically 8 in our default configuration). The parses are decoded via nucleus sampling and are typically diverse: the top sample reflects the parser's most confident guess, while lower-probability samples explore alternative interpretations. The multiple-parse strategy is the first line of defence against parser errors: even when the top parse is incorrect, a correct parse often appears among the lower-probability samples.

## 3.2 Executor

The executor is a standard interpreter for the typed lambda calculus, instantiated with the domain-specific primitives. For SCAN, the primitives are actions and modifiers; for COGS, they are predicates and entities over a small relational world; for CFQ, they are SPARQL-like graph queries. The executor is implemented as roughly 600 lines of Python and includes a type checker that catches malformed expressions before execution.

The executor produces three outputs for each candidate parse: a value (the result of evaluation), a type (the lambda-calculus type of the expression), and a flag indicating whether the expression executed successfully (without type errors or undefined primitives). The flag is the second line of defence against parser errors: malformed parses are filtered out before they can produce confidently wrong answers.

## 3.3 Verifier

The verifier is a small model (110M parameters in our default configuration) that scores each successfully-executed candidate parse. The verifier takes as input the original utterance, the candidate parse, and the executor's output value, and produces a scalar score that estimates the probability that the parse correctly captures the utterance's meaning.

The verifier is trained on a synthetic dataset that we generate by running the parser on a large pool of utterances and labelling each (utterance, parse, value) triple as correct or incorrect via a heuristic agreement check (multiple parses that produce the same value are considered jointly correct, and a small held-out human-labelled set is used to anchor the heuristic). The verifier is trained with a contrastive binary classification objective and reaches above-95% AUC on the held-out set.

At inference time, the verifier scores each candidate parse, and the system returns the value associated with the highest-scoring parse. The verifier is the third line of defence against parser errors: even when the parser produces multiple type-correct parses, the verifier typically distinguishes the semantically correct one.

## 3.4 Training-free deployment for new domains

A practical advantage of NSR is that adapting it to a new domain requires no training of the parser or the executor. To adapt the system, a developer needs to specify the symbolic vocabulary (a list of typed primitives) and a small number of in-context examples for the parser. The verifier can either be retrained (which we recommend if a domain-specific labelled set is available) or used as-is if domain transfer of the verifier is acceptable. We report cross-domain transfer results for the verifier in the next section.

## 3.5 Implementation and reproducibility

The full NSR pipeline is implemented in approximately 2000 lines of Python. The parser uses the HuggingFace Transformers interface; the executor is a standalone module; the verifier is a small transformer with a scalar head. All three components, along with the synthetic training data for the verifier, are released under a permissive licence.
