---
name: ml-incident-response
description: Guides agents through responding to production ML incidents — mitigate-first, then RCA, then permanent fix (S-A-R-L adapted for ML). Use during active production incidents: regression, drift spike, fallback storm, hallucination surge, cost spike.
---

# ml-incident-response

## Overview

When production ML is broken, the order is **mitigate-first, then RCA, then permanent fix**. Don't debug while users are affected. This skill adapts S-A-R-L (Situation → Action → Result → Lesson) for ML incidents, where the Action phase has a strict mitigate-before-investigate order.

## When to Use

- Active production incident: error rate spike, latency spike, drift alert, fallback storm, hallucination surge, cost spike
- Users reporting ML-quality regression
- On-call responding to a paged ML alert

Do **not** use for: pre-production bugs (use `debugging-ml-failures`), slow-quality-decline-without-incident (use `drift-and-sliced-eval` monitoring), or non-ML incidents (use your org's general incident process).

## Process

1. **Declare and assemble.**
   - State the incident: what's broken, since when, who's affected, severity (SEV1 / SEV2 / SEV3).
   - Assign incident commander (IC), comms lead, ops lead. For small incidents, one person may wear all three hats — but say so out loud.
   - Open an incident channel. Start a timeline doc (timestamped events).
   - Exit criteria: incident declared, channel open, roles named, timeline started.

2. **Capture initial state (before mitigating).**
   - Snapshot: current error rate, latency, fallback rate, drift signals, recent deploys (last 24h), recent config changes.
   - Save a sample of failing inputs (PII-redacted) for RCA later.
   - Exit criteria: state captured in the timeline doc.

3. **Mitigate-first (restore user experience).**
   - Goal: stop the bleeding, not fix the cause. Pick the cheapest mitigation:
     - **Roll back** the last deploy / model version / config change. Often the fastest.
     - **Flip feature flag** to disable new behavior.
     - **Increase fallback aggressiveness** (route more traffic to cheaper/stable model).
     - **Disable the affected feature** if user-facing impact is worse than missing feature.
     - **Throttle traffic** if backend is overloaded.
   - Verify mitigation worked: error rate / latency / fallback rate recovering.
   - Exit criteria: user-visible metrics recovering; mitigation in place; verified.

4. **Communicate.**
   - Internal: incident channel + stakeholder update (every 30 min for SEV1, 2h for SEV2, daily for SEV3).
   - External (if user-facing): status page update within 30 min for SEV1.
   - Format: what's broken, what we're doing, what users should expect, next update time.
   - Exit criteria: comms sent on cadence; next update scheduled.

5. **RCA (root cause analysis) — only after mitigation.**
   - Now that users are stable, find the cause.
   - Use `debugging-ml-failures` for the technical RCA: reproduce, localize, reduce, classify flakiness-vs-regression.
   - Common ML incident causes: model regression from a deploy, drift crossing a threshold, fallback storm (primary failed, fallback overloaded), cache invalidation bug, prompt template regression, golden set drifted, cost spike from routing misconfiguration.
   - Exit criteria: root cause named with evidence (repro + localization).

6. **Permanent fix.**
   - Fix the root cause, not just the symptom.
   - Add a golden case from the incident so it can't recur silently.
   - Add or tighten an alert that would catch this earlier next time.
   - Run eval (per `eval-driven-development`) to verify the fix doesn't regress.
   - Exit criteria: fix merged + eval passes + golden case added + alert added/tightened.

7. **Post-mortem (within 5 business days).**
   - S-A-R-L write-up: Situation (what happened, when, impact), Action (mitigation + RCA + fix), Result (time-to-mitigate, time-to-fix, user impact), Lesson (what to change to prevent or catch earlier).
   - Blameless: focus on systems and processes, not individuals.
   - Action items: each has owner + due date. Track to closure.
   - Exit criteria: post-mortem doc published; action items tracked.

## ML-specific incident patterns

| Pattern | Symptom | Mitigation |
|---|---|---|
| **Model regression** | Quality metric drops after a deploy | Roll back model version |
| **Drift spike** | Drift alert fires, quality degrading | Roll back; investigate drifted slice |
| **Fallback storm** | Fallback rate spikes, fallback also degrading (overloaded) | Reduce traffic; route to a stable fallback; fix primary |
| **Hallucination surge** | Faithfulness drops, user complaints | Roll back prompt; strengthen grounding; add eval cases |
| **Cost spike** | Cost per hour alert fires | Check routing config; roll back if a routing change caused it |
| **Cache pollution** | Cache hit rate high but answers wrong | Invalidate cache; check cache key/threshold |
| **Stale context (RAG)** | Answers reference outdated docs | Re-index KB; check KB freshness pipeline |
| **Judge variance spike** | Eval flakiness alert | Pin judge config; switch to lower-variance judge model |

## Rationalizations

| Excuse | Rebuttal |
|---|---|
| "Let me debug before rolling back" | Users are affected. Mitigate first, debug second. Rollback is minutes; RCA is hours. |
| "The mitigation might make things worse" | Then revert the mitigation. But trying mitigation is faster than prolonged user impact. |
| "Comms can wait until we understand it" | Users and stakeholders need to know it's being worked on. Comms-with-unknowns is better than silence. |
| "Post-mortem is bureaucratic" | Without post-mortem, the same incident recurs. Action items are how systems get better. |
| "Action items can be informal" | Informal action items don't get done. Owner + due date + tracking. |
| "It was a one-off, no fix needed" | One-offs recur in ML. Add the golden case anyway. |
| "We can't reproduce, so RCA is impossible" | Then add more observability and capture more state next time. Don't skip the post-mortem. |

## Red Flags

- Debugging while users are affected (no mitigation) — wrong order.
- Mitigation without verification — assumed fix, not confirmed.
- No incident channel / timeline — facts will be lost by post-mortem time.
- Comms silence during SEV1 — stakeholders panic, rumor fills the gap.
- RCA skipped ("we know what caused it") — write it down anyway; memory is unreliable.
- Post-mortem blames an individual — systems, not people.
- No action items from post-mortem — incident will recur.
- No golden case added — same regression can re-merge silently.
- No alert tightened — next time it's caught at the same late stage.

## Verification

Before this skill is complete:

- **Declaration**: incident declared, severity assigned, roles named, channel open, timeline started.
- **State capture**: error rate, latency, fallback rate, drift, recent changes — all snapshotted before mitigation.
- **Mitigation**: cheapest restore applied (rollback / flag flip / fallback / disable / throttle); user-visible metrics recovering; verified.
- **Comms**: internal + (if user-facing) external, on cadence, with next-update time.
- **RCA**: root cause named with evidence (repro + localization per `debugging-ml-failures`).
- **Permanent fix**: merged; eval passes; golden case added; alert added/tightened.
- **Post-mortem**: S-A-R-L write-up published within 5 business days; blameless; action items with owners + due dates; tracked to closure.
