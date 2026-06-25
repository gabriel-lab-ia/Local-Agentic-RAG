---
source_id: llmops_rag_evaluation
title: "Evaluation of Retrieval-Augmented Generation Systems"
domain: llmops
topic: rag_evaluation
url: "https://www.deepset.ai/blog/rag-evaluation"
license: engineering_synthesis
language: en
source_type: engineering_synthesis
---

# RAG evaluation

Retrieval-augmented generation must be evaluated as multiple connected
components rather than as one opaque text-generation system.

## Evaluation layers

Evaluate separately:

1. corpus quality;
2. chunking and metadata;
3. retrieval;
4. context construction;
5. answer generation;
6. citation correctness;
7. end-to-end task success.

## Retrieval metrics

Given a labeled evaluation set, retrieval can be measured with:

- recall at k;
- precision at k;
- mean reciprocal rank;
- normalized discounted cumulative gain;
- hit rate;
- source coverage.

Retrieval evaluation requires relevance judgments or trusted expected
sources.

## Generation metrics

Evaluate whether the answer is:

- correct;
- grounded in retrieved evidence;
- relevant;
- complete;
- concise;
- citation-aligned;
- safe.

Fluency alone is not evidence of correctness.

## Faithfulness

A faithful answer should not make factual claims unsupported by the supplied
context.

Each claim can be classified as:

- supported;
- contradicted;
- not present in context;
- not requiring retrieval evidence.

## Evaluation dataset

A useful test set contains:

- answerable questions;
- unanswerable questions;
- ambiguous questions;
- multi-document questions;
- adversarial wording;
- outdated-information traps;
- metadata-filtering cases;
- near-duplicate sources.

## Component diagnosis

A wrong answer may result from:

```text
correct source not retrieved
retrieved source ranked too low
chunk missing required context
prompt discarded evidence
model ignored evidence
citation mapped incorrectly
```

Evaluation should identify the failing layer.

## Regression testing

Store evaluation cases in version control.

Run them after changes to:

- embedding model;
- chunk size;
- overlap;
- retrieval algorithm;
- reranker;
- prompt;
- generator model;
- corpus.

## Engineering guidance

Maintain a human-reviewed benchmark.
Record retrieval and generation results separately.
Include no-answer behavior.
Compare changes against a baseline.
inspect failures manually.
prevent evaluation data from contaminating the corpus.
