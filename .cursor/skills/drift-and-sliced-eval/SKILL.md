---
name: drift-and-sliced-eval
description: Guides agents through detecting distribution drift and sliced evaluation — avoiding the aggregate-metric trap where overall looks fine but a slice is regressing. Use for production monitoring, post-deploy validation, and any eval where aggregate alone is insufficient.
---

# drift-and-sliced-eval

## Overview

Two intertwined disciplines: **sliced eval** (never trust an aggregate — break down by segment, language, request type, latency tier) and **drift detection** (production input distribution shifting away from training/eval distribution, silently degrading the model). Together they catch the regressions that aggregate offline metrics hide.

## When to Use

- Post-deploy validation (does production behave like eval predicted?)
- Setting up production monitoring for an ML/LLM system
- Investigating "the metric is fine but users complain" symptoms
- Designing the eval harness — slice definitions must be planned, not bolted on
- After a model upgrade — drift check before declaring ship

Do **not** use for: pre-deploy code-only changes with no ML behavior impact (use unit tests + `code-review-ml`).

## Process

1. **Define slicing dimensions.**
   - User segments: geography, language, device, account tier, new vs returning.
   - Request types: intent, query length, topic, complexity tier.
   - Latency tiers: fast vs slow requests (sometimes quality differs).
   - Time: hour-of-day, day-of-week (catches batch-job contamination, traffic shifts).
   - Exit criteria: 3-7 slicing dimensions named, each with a reason (why this slice might behave differently).

2. **Set per-slice tolerance.**
   - Aggregate tolerance is too loose — a 5% aggregate drop can hide a 30% slice drop.
   - Per-slice tolerance: tighter for high-stakes slices (e.g. regulated populations), looser for long-tail.
   - Exit criteria: per-slice tolerance table, justified by stakes.

3. **Add sliced reporting to the eval harness.**
   - Every eval run produces a per-slice breakdown, not just aggregate.
   - Slice size reported alongside metric — a 50% drop on a slice of 5 samples is noise; on 5000 is signal.
   - Exit criteria: eval output includes slice breakdown + sample size per slice.

4. **Define drift signals.**
   - **Input drift**: distribution of inputs in production vs golden set. Track via feature distributions (for tabular) or embedding clusters (for text/queries).
   - **Output drift**: distribution of model outputs (predictions, scores, response lengths, tool-call patterns) over time.
   - **Concept drift**: input distribution same, but input→output relationship changed (ground truth shifted). Hardest to detect — requires labeled production samples.
   - Exit criteria: drift signals named per type, with measurement approach.

5. **Set drift thresholds and alerting.**
   - Thresholds based on historical baseline (PSI, KS test, KL divergence — pick one per signal).
   - Alert on sustained drift, not single-point — avoid alert fatigue from transient spikes.
   - Exit criteria: drift threshold per signal + alert condition (sustained N hours) + alert channel.

6. **Wire sliced eval into CI.**
   - CI eval gate checks per-slice, not just aggregate. Slice regression beyond tolerance blocks the merge.
   - Exit criteria: CI config blocks on slice regression, with a way to override (requires ADR + reviewer sign-off).

7. **Wire drift detection into production monitoring.**
   - Daily drift report: per-signal drift status vs threshold.
   - Weekly sliced production metric report: per-slice quality / latency / cost.
   - Exit criteria: dashboards exist + on-call runbook references them.

8. **Define drift response playbook.**
   - Mild drift: monitor, no action.
   - Moderate drift: investigate, tighten eval on drifted slice, schedule retraining.
   - Severe drift: roll back, escalate (use `ml-incident-response`).
   - Exit criteria: drift response runbook with thresholds + actions.

## Rationalizations

| Excuse | Rebuttal |
|---|---|
| "Aggregate metric improved, ship it" | Aggregate can hide slice regressions. Check slices before declaring win. |
| "Slice breakdown is too much reporting" | A slice table is 10 extra lines in the eval output. The regressions it catches cost 10x the reporting overhead. |
| "Drift detection is overkill for v1" | Drift is silent — by the time users complain, the model has been degraded for weeks. Add drift signals with the launch. |
| "We'll add slicing later" | Slicing defined post-hoc is slicing shaped to fit the result. Define slices when you design the eval. |
| "Slice is too small to matter" | Small high-stakes slices (regulated populations, paying users) matter more than large low-stakes ones. Stakes, not size, drive priority. |
| "Concept drift won't happen to us" | It happens to every model with real-world labels (fraud, spam, intent). Plan for it. |
| "PSI / KS test is too statistical" | Pick one drift metric, learn its threshold on your data. You don't need a stats PhD to use PSI = 0.2 as "notable drift". |

## Red Flags

- Eval output reports only aggregate — no slices.
- Slice tolerances are uniform ("5% for all") — ignores slice stakes.
- Drift signals defined but no thresholds / alerts — drift detection without response is theater.
- CI gate checks aggregate only — slice regressions merge silently.
- No labeled production samples — can't detect concept drift.
- Drift alerts fire constantly with no action — alert fatigue, real drift ignored.
- Sliced production metrics not on a dashboard — on-call can't see them during incidents.
- "Slice regressed but aggregate improved, so it's a win" — wrong. Slice regression blocks merge.

## Verification

Before this skill is complete:

- **Slicing dimensions**: 3-7 named, each with a reason.
- **Per-slice tolerance**: table with justification by stakes.
- **Sliced eval output**: every eval run produces slice breakdown + sample size.
- **Drift signals**: input / output / concept drift — each named with measurement approach.
- **Drift thresholds**: per signal, with sustained-N-hours alert condition.
- **CI gate**: blocks on slice regression beyond tolerance; override requires ADR.
- **Production dashboards**: drift status + sliced production metrics, linked from on-call runbook.
- **Drift response runbook**: mild / moderate / severe thresholds + actions, links to `ml-incident-response` for severe.
