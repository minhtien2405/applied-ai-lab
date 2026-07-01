---
name: observability-for-ml-systems
description: Guides agents through instrumenting ML/LLM/agentic systems — structured logging, RED/USE metrics adapted for ML, OpenTelemetry tracing, symptom-based alerting. Use when shipping anything that runs in production, or when adding telemetry to an existing ML service.
---

# observability-for-ml-systems

## Overview

Instrument ML systems as you build, not after. The minimum bar: structured logs, RED metrics (Rate / Errors / Duration) adapted for ML, USE metrics (Utilization / Saturation / Errors) for resources, OpenTelemetry-compatible tracing that follows a request end-to-end, and symptom-based alerts that fire on user-visible problems.

## When to Use

- Shipping an ML/LLM/agentic service to production
- Adding telemetry to an existing service that has none
- Hitting "we can't tell what went wrong" during an incident
- Designing the serving layer (use alongside `model-serving-design`)

Do **not** use for: local dev scripts, Jupyter demos (use print + manual inspection).

## Process

1. **Define what a "request" is.**
   - One user query? One inference call? One agent turn?
   - Trace context follows one logical request end-to-end (gateway → retrieval → model → tool calls → response).
   - Exit criteria: request definition written; trace span tree expected shape sketched.

2. **Instrument structured logging.**
   - JSON logs with fields: timestamp, level, request_id, trace_id, user_id (hashed), model_variant, prompt_template_version, latency_ms, cost, error_code.
   - No `print()` in production paths. No free-text logs that can't be queried.
   - PII redaction at log time, not after.
   - Exit criteria: log schema documented + every log call uses it.

3. **Instrument RED metrics for ML.**
   - **Rate**: requests per second, per model variant, per tool.
   - **Errors**: error rate, by error code (timeout, rate_limited, content_filter, fallback_failed, ...).
   - **Duration**: p50, p95, p99 latency, per model variant and per request stage (retrieval, model call, tool call).
   - Exit criteria: RED metrics exported to a metrics system (Prometheus, Datadog, CloudWatch).

4. **Instrument USE metrics for resources.**
   - **Utilization**: GPU utilization, CPU, memory, queue depth.
   - **Saturation**: queue wait time, request concurrency vs limit, connection pool usage.
   - **Errors**: provider 5xx, network errors, disk errors.
   - Exit criteria: USE metrics exported for each resource the service depends on.

5. **Instrument ML-specific metrics.**
   - **Quality**: per-request eval score (if online eval possible), judge score (if LLM-judge in the loop), user feedback (thumbs up/down).
   - **Cost**: tokens in / out, embedding calls, retrieval calls, reranker calls, GPU time. Aggregate per request, per user, per day.
   - **Fallback**: fallback rate, fallback level distribution, fallback-triggered-by-error-code breakdown.
   - **Cache**: cache hit rate, cache wrong-answer rate (sampled), cache size.
   - Exit criteria: ML-specific metrics exported, per the `model-serving-design` spec.

6. **Instrument tracing (OpenTelemetry).**
   - One trace per request. Spans for: gateway, retrieval, model call (per variant tried), tool call (per call), rerank, cache lookup.
   - Span attributes: model_variant, prompt_template_version, tool_name, fallback_path, cost, latency, success/error_code.
   - Propagate trace context across service boundaries (W3C trace context headers).
   - Exit criteria: traces visible in a tracing backend (Tempo, Jaeger, Langfuse, LangSmith, Honeycomb).

7. **Define symptom-based alerts.**
   - Alert on user-visible symptoms, not internal causes:
     - Error rate > X% over 5 minutes
     - p95 latency > Y ms over 10 minutes
     - Fallback rate > Z% over 15 minutes (model is failing, fallback is masking it)
     - Cost per hour > $W (silent cost spike)
     - Cache hit rate dropped > V% (cache broken or traffic pattern shifted)
     - Drift signal > threshold (from `drift-and-sliced-eval`)
   - Avoid alerting on CPU/disk alone — those are causes, not symptoms.
   - Exit criteria: alert rules + thresholds + escalation channel + runbook link per alert.

8. **Write the runbook.**
   - For each alert: what it means, how to investigate (which dashboard, which trace query), common causes, mitigation steps, escalation.
   - Exit criteria: runbook committed, linked from each alert.

## Rationalizations

| Excuse | Rebuttal |
|---|---|
| "We'll add observability after launch" | After launch, you'll have an incident before you have observability. Add it with the code. |
| "Logs are enough, no need for metrics + traces" | Logs tell you what happened in one request. Metrics tell you what's happening across all requests. Traces connect them. You need all three. |
| "Tracing is too expensive" | Sample. Head-based sampling for normal traffic, tail-based for errors. Cost is manageable; blind spots are not. |
| "PII redaction can be done in log pipeline" | Redact at log time, not after. Once PII hits the pipeline, it's in 5 systems before you redact it. |
| "Alert on CPU > 80%" | CPU is a cause. Alert on symptom (latency, error rate) — you'll catch the user impact sooner. |
| "We don't need online quality metrics" | Without online quality, you can't tell offline-vs-online gap. Sample production, run judge on the sample, get the gap. |
| "Fallback rate is fine because fallback works" | High fallback rate means primary is failing. Fallback working is not the same as primary working. Alert on fallback rate. |

## Red Flags

- `print()` in production code paths.
- Logs are free text, unstructured — can't query.
- No trace context propagation across service boundaries — can't follow a request.
- Alerts on CPU/disk without corresponding symptom alerts.
- No per-model-variant or per-tool metrics — can't tell which variant is degraded.
- No cost tracking — silent cost spikes.
- No fallback-rate alert — primary fails silently behind fallback.
- PII in logs — compliance + security incident.
- Runbook missing for an alert — on-call doesn't know what to do.

## Verification

Before this skill is complete:

- **Request definition**: documented; trace span tree sketched.
- **Structured logs**: JSON schema with required fields; PII redaction at log time.
- **RED metrics**: rate, errors, duration exported per model variant and per stage.
- **USE metrics**: utilization, saturation, errors exported per resource.
- **ML-specific metrics**: quality, cost, fallback, cache — all exported.
- **Tracing**: OpenTelemetry, one trace per request, spans per stage, context propagated.
- **Alerts**: symptom-based rules with thresholds + escalation + runbook link.
- **Runbooks**: per alert, with investigation steps + common causes + mitigation + escalation.
