---
name: model-serving-design
description: Guides agents through designing the model serving layer — unified gateway, fallback ladder, semantic cache, cost-aware routing, never-500 target. Use when building or modifying model serving, LLM gateway, inference routing, or fallback strategy.
---

# model-serving-design

## Overview

Design the serving layer that sits between your application and your models: a unified gateway that abstracts model swap, a fallback ladder that keeps never-500 even when providers fail, a semantic cache that absorbs repeat traffic, cost-aware routing that picks the cheapest model that meets the quality bar.

## When to Use

- Building a model gateway / LLM proxy
- Adding a new model or provider to an existing serving stack
- Designing fallback for an external model dependency
- Routing requests across model variants (cheap vs premium, fast vs high-quality)
- Adding semantic caching to a serving path
- Hitting reliability or cost ceilings with current serving

Do **not** use for: model training itself (use `spec-ml-system` + eval), or pure client-side SDK swaps (just do it).

## Process

1. **Map the requirements.**
   - Latency budget (p50, p95, p99), cost budget per request and per day, quality floor (worst-acceptable output), availability target (never-500? 99.9%?).
   - Traffic pattern: peak QPS, burst shape, geographic distribution.
   - Exit criteria: numbers for each — not "fast and cheap".

2. **Design the unified gateway interface.**
   - One interface for all model calls. Application code never imports `openai` or `anthropic` directly — it calls `gateway.complete()`.
   - Request shape: model-agnostic (messages, tools, params). Response shape: model-agnostic (text, tool calls, usage, cost, latency).
   - Provider adapters translate to/from each provider's API.
   - Exit criteria: interface spec with request/response types, adapter list.

3. **Design the fallback ladder.**
   - Order: primary → fallback 1 → fallback 2 → cache → static answer → honest error.
   - Triggers for falling over: timeout, 5xx, rate limit, content filter, low-quality-detected.
   - Each level has a latency budget — falling over consumes budget, so lower levels must be faster.
   - Test by injecting primary failure in eval. **Fallback that's never tested fails when first needed.**
   - Exit criteria: ladder order + trigger conditions + eval injection plan.

4. **Design the semantic cache.**
   - Cache key: embedding of normalized input (case-folded, whitespace-trimmed, PII-redacted).
   - Similarity threshold for hit (tune on eval — too loose → wrong answers, too tight → no hits).
   - TTL: how long is a cached answer valid? Depends on knowledge freshness — RAG answers expire when source docs update.
   - Bypass for: requests with user-specific context, requests that must be fresh, requests above quality threshold requiring fresh model.
   - Cache hit rate target + cache wrong-answer rate target — measure both.
   - Exit criteria: cache key + threshold + TTL + bypass rules + measurement plan.

5. **Design cost-aware routing.**
   - Routes: cheap-model for easy requests, premium-model for hard requests, static-answer for known-frequent.
   - Classification: how do you decide "easy" vs "hard"? (heuristic, classifier, or always try cheap and escalate on low-confidence).
   - Cost tracking per request, per user, per day. Alert on cost spike.
   - Exit criteria: routing rules + classifier approach + cost tracking + alerting.

6. **Design observability.**
   - Per-request trace: model variant, prompt template version, fallback path taken, cache hit/miss, latency breakdown, cost.
   - Aggregate metrics: QPS, p50/p95/p99 latency, fallback rate, cache hit rate, cost per 1K requests, error rate by error type.
   - Symptom alerts: error rate > X%, fallback rate > Y%, p95 latency > Z ms, cost per day > $W.
   - Exit criteria: trace schema + metric list + alert thresholds.

7. **Write the design doc / ADR.**
   - Gateway interface, fallback ladder, cache, routing, observability — all in one doc.
   - This is an irreversible-enough decision to warrant an ADR.
   - Exit criteria: ADR committed before implementation.

## Rationalizations

| Excuse | Rebuttal |
|---|---|
| "We'll add fallback when we hit an outage" | Then you'll have an outage before you have fallback. Add it now, test it in eval. |
| "Caching is premature optimization" | If you have repeat traffic, caching pays for itself in a week. If you don't, the cache hit rate metric will tell you and you can remove it. |
| "Routing adds complexity, just use one model" | One model means one provider's outages take you down, and one provider's pricing changes hit your margin. Routing is resilience + cost control. |
| "Never-500 is unrealistic" | It's a target, not a guarantee. The point is that downstream failures degrade gracefully, not surface as 5xx to users. A cached answer or honest "try again later" beats a 5xx. |
| "We don't need an ADR for this" | Gateway shape, fallback order, cache strategy — all expensive to reverse. ADR is cheap; reversal is not. |
| "Cost tracking can be added later" | Without cost tracking, you won't notice the silent 10x cost spike until the bill arrives. Add it with the gateway. |

## Red Flags

- Application code imports a specific provider's SDK directly — bypass the gateway, lose fallback.
- Fallback ladder exists but is never tested in eval — it will fail when first needed.
- Cache has no bypass rules — user-specific requests get wrong cached answers.
- Routing has no cost tracking — silent cost spikes.
- No latency budget per fallback level — fallback storms cascade into total latency blowup.
- Gateway interface leaks provider-specific concepts (e.g. exposes `openai_message` type) — model swap is no longer free.
- "Never-500" claimed but no injection test in eval — claim is unverified.

## Verification

Before this skill is complete:

- **Requirements**: latency / cost / quality / availability numbers stated, not hand-waved.
- **Gateway interface**: model-agnostic request/response types documented; adapter list named.
- **Fallback ladder**: order + triggers + per-level latency budget + eval injection plan.
- **Semantic cache**: key + threshold + TTL + bypass rules + hit-rate and wrong-answer-rate targets.
- **Cost-aware routing**: rules + classifier + cost tracking + alert thresholds.
- **Observability**: trace schema + metric list + symptom alert thresholds.
- **ADR**: committed before implementation; alternatives considered documented.
- **Eval**: fallback injection test, cache hit-rate and wrong-answer-rate, routing classification accuracy, latency p95, cost per 1K requests — all measured before ship.
