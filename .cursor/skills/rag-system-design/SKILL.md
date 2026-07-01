---
name: rag-system-design
description: Guides agents through designing a RAG system — chunking, hybrid search, rerank, retrieval eval (RAGAS-style), failure modes. Use when building or modifying retrieval-augmented generation: knowledge base, search, rerank, or answer generation.
---

# rag-system-design

## Overview

Design RAG systems that actually retrieve the right context and ground answers in it. The hard parts are not "wire embedding + vector DB" — they're chunking strategy, hybrid search weights, rerank placement, retrieval evaluation, and the failure modes (retrieval miss, context pollution, hallucination despite grounding).

## When to Use

- Building a new RAG system
- Adding hybrid search (BM25 + vector) to an existing vector-only RAG
- Adding a reranker
- Changing chunking strategy
- Tuning top-k or retrieval weights
- Hitting "the answers are hallucinated / wrong / missing context" symptoms

Do **not** use for: pure chatbot with no retrieval (just use a model), or pure search with no generation (use a search skill).

## Process

1. **Characterize the knowledge base.**
   - Document types (markdown, PDF, code, HTML), sizes, languages, update cadence.
   - Permission / tenancy model — whose docs can whose queries see?
   - Freshness requirement — must answers reflect docs updated minutes ago, or daily OK?
   - Exit criteria: KB profile written (types, sizes, languages, freshness, permissions).

2. **Choose chunking strategy.**
   - Chunk size: too small → context fragmented, too large → context pollution.
   - Chunk boundaries: structural (headings, paragraphs, code blocks) beat fixed-size windows.
   - Overlap: small overlap to preserve cross-boundary context, not so much that you double-index.
   - Metadata: each chunk carries source doc, section, timestamp, permission tag.
   - Exit criteria: chunking spec + sample chunks inspected for sanity.

3. **Choose embedding model.**
   - Match the language and domain of your KB. Generic embeddings underperform on domain jargon.
   - Dimension vs cost vs latency tradeoff — bigger isn't always better.
   - Multi-lingual KB → multi-lingual embedding, not translation-then-embed.
   - Exit criteria: embedding model chosen with reason + benchmark on your KB (not just MTEB).

4. **Design hybrid search.**
   - Vector (semantic) + BM25 (lexical) — neither alone is enough. Vector misses exact-match queries; BM25 misses synonym / paraphrase queries.
   - Fusion: RRF (Reciprocal Rank Fusion) is the safe default. Weighted sum requires tuning on eval.
   - Top-k: retrieve more, rerank down. Typical: retrieve 50-100, rerank to 5-10 for the prompt.
   - Exit criteria: hybrid config + retrieval top-k + fusion method.

5. **Add a reranker.**
   - Cross-encoder rerank on the top-N retrieved chunks — much cheaper than reranking the whole KB, much better accuracy than vector-only.
   - Reranker model: small cross-encoder (bge-reranker, etc.) is usually enough; bigger if your domain needs it.
   - Exit criteria: reranker chosen + top-N to top-k pipeline spec.

6. **Design the prompt with grounding.**
   - System prompt: "answer only from the provided context; if the context doesn't contain the answer, say so".
   - Context placement: at the top, clearly delimited from the question.
   - Citation: require the model to cite source chunks (chunk IDs or inline refs).
   - Exit criteria: prompt template with citation requirement.

7. **Design retrieval eval (RAGAS-style).**
   - Metrics: faithfulness (answer grounded in retrieved context), answer relevancy (answer addresses the question), context precision (retrieved chunks relevant), context recall (relevant chunks retrieved).
   - Golden set: questions + reference answers + reference chunks. Freeze before tuning.
   - Judge: LLM judge with deterministic config; N runs to estimate variance.
   - Failure-mode golden cases: deliberately ambiguous questions, questions with no answer in the KB, questions requiring multi-hop retrieval — make sure the eval catches these.
   - Exit criteria: eval harness spec with all 4 metrics + golden set + judge config.

8. **Design failure modes.**
   - **Retrieval miss**: query returns irrelevant chunks → answer says "I don't know" (good) or hallucinates (bad). Eval must catch the bad path.
   - **Context pollution**: too many chunks, signal drowned → answer quality drops. Tune top-k.
   - **Hallucination despite grounding**: model ignores context. Strengthen prompt, eval faithfulness.
   - **Stale context**: KB updated but cache returns old answer. Cache invalidation on KB update.
   - Exit criteria: failure-mode list + per-mode eval case + mitigation.

9. **Write the design doc / ADR.**
   - KB profile, chunking, embedding, hybrid search, rerank, prompt, eval, failure modes — all in one doc.
   - Exit criteria: ADR committed before implementation.

## Rationalizations

| Excuse | Rebuttal |
|---|---|
| "Vector search alone is fine" | Vector-only misses exact-match (product codes, error strings, names). Hybrid with BM25 catches both. The eval will show it. |
| "Reranker is overkill" | Reranker is the single biggest RAG quality lever after hybrid search. Cost is small (cross-encoder on top-N), gain is large. |
| "We'll figure out chunking later" | Chunking shapes everything downstream — embedding, retrieval, rerank, prompt. Fix it early; changing it later means re-indexing the whole KB. |
| "Eval can be a few test questions" | A few questions won't catch failure modes. Build a golden set with deliberate edge cases (no-answer, multi-hop, ambiguous). |
| "Citation is nice-to-have" | Without citation, you can't audit hallucinations. Require it from day one. |
| "Cache everything, RAG is expensive" | Caching RAG answers without KB-version invalidation returns stale answers. Either invalidate on KB update or skip the cache. |

## Red Flags

- Vector-only retrieval (no BM25) — exact-match queries will fail.
- No reranker, just top-k from vector — context pollution, lower answer quality.
- Fixed-size chunking with no structural awareness — cross-boundary context lost.
- Top-k retrieved = top-k in prompt (no rerank) — too much context, signal drowned.
- Prompt has no "say I don't know" instruction — model will hallucinate on retrieval miss.
- No citation in answer — can't audit hallucinations post-hoc.
- Eval is "we tested 5 questions internally" — won't catch failure modes.
- Cache has no KB-version invalidation — stale answers.
- No failure-mode golden cases — system will look fine in eval and fail in production.

## Verification

Before this skill is complete:

- **KB profile**: types, sizes, languages, freshness, permissions documented.
- **Chunking**: strategy + sample chunks inspected; metadata on each chunk.
- **Embedding**: model chosen with benchmark on your KB (not just MTEB).
- **Hybrid search**: vector + BM25 with RRF (or weighted sum tuned on eval); top-N to rerank.
- **Reranker**: chosen + pipeline spec (top-N retrieved → top-k in prompt).
- **Prompt**: grounding instruction + citation requirement.
- **Eval**: faithfulness + answer relevancy + context precision + context recall; golden set frozen; failure-mode cases included; judge variance estimated.
- **Failure modes**: retrieval miss, context pollution, hallucination, stale context — each with eval case + mitigation.
- **ADR**: committed before implementation.
