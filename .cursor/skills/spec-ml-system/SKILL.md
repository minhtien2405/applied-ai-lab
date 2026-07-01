---
name: spec-ml-system
description: Guides agents through specifying an ML/LLM/agentic system from business problem to success criteria, data plan, eval plan, and fallback strategy — before any code. Use when starting a new ML feature, a significant change, or when the ask is underspecified.
---

# spec-ml-system

## Overview

Turn a vague ML/LLM/agentic ask into a concrete spec: what business problem, what success looks like (offline + online metrics), what data, what eval, what fallback, what can go wrong. Code comes after the spec, not before.

## When to Use

- Starting a new ML feature or significant change
- The ask is underspecified ("build a fraud classifier", "add RAG to the assistant")
- A decision is expensive to reverse (model choice, threshold, schema)
- You find yourself guessing what the user wants — stop and spec instead

Do **not** use for: trivial one-line changes (just do them), pure refactors with no behavior change (use `incremental-implementation`), or post-incident fixes (use `ml-incident-response` first, then spec the permanent fix).

## Process

1. **Clarify the business problem.**
   - What user-visible behavior should change? What's the cost of the current behavior?
   - Reframe ML jargon to business terms: "fraud recall +10 points" → "catch X% more fraud, saving $Y/month, with Z% more good users flagged".
   - Exit criteria: a one-sentence problem statement the user agrees with.

2. **Define success criteria — offline and online.**
   - Offline: which metric, current baseline, target, tolerance, slice requirements.
   - Online: how will production validation happen (A/B, shadow, canary)? What's the online metric (conversion, retention, cost)?
   - Exit criteria: 2-5 metrics with current + target values, named explicitly.

3. **Define the data plan.**
   - Sources, freshness, point-in-time correctness, schema, ownership.
   - Train/eval split strategy (time-based, group-based — pick one and justify).
   - Golden set: how big, how labeled, frozen when?
   - Exit criteria: data sources + split strategy + golden set plan written down.

4. **Define the eval plan.**
   - Metric definitions (formula, not just names). RAGAS? custom judge? human?
   - Judge variance mitigation (N runs, deterministic seed, model for judge).
   - Slicing dimensions (segment, language, request type, latency tier).
   - Exit criteria: eval harness spec — runnable by someone reading only this.

5. **Define the fallback strategy.**
   - What happens when the primary fails (LLM API down, model endpoint slow, retrieval empty)?
   - Fallback ladder: primary → cache → cheaper model → static answer → honest error.
   - Exit criteria: fallback order named + which fallback the eval will test.

6. **Identify risks and unknowns.**
   - What could go wrong? What's irreversible? What needs an ADR?
   - What are the top 3 failure modes you'll monitor post-ship?
   - Exit criteria: risk list with severity + which become ADRs.

7. **Write the spec doc.**
   - One file (markdown). Sections: Problem, Success Criteria, Data, Eval, Fallback, Risks, Open Questions.
   - Exit criteria: spec committed to `docs/specs/` (or wherever the project keeps specs), linked from the implementing PR.

8. **Get spec approval before coding.**
   - Show the spec to the user (or reviewer). Resolve open questions.
   - Exit criteria: explicit "go" from the user, or revised spec with answers.

## Rationalizations

| Excuse | Rebuttal |
|---|---|
| "The user wants it now, no time to spec" | Coding without spec takes longer — you'll build the wrong thing and rebuild. A 30-min spec saves a 3-day wrong build. |
| "It's just a small change, no spec needed" | Then the spec is one line: "metric X is at W, target T, change is Y". That's still a spec. If you can't write that line, you don't understand the change. |
| "We'll figure out the eval as we go" | Eval-as-you-go means eval-shaped-to-fit-the-result. Define the eval first so it can't be gamed. |
| "The business problem is obvious" | Then writing it in one sentence is cheap. If you can't, it wasn't obvious. |
| "Fallback can be added later" | Fallback-added-later is fallback-tested-never. Specify the fallback now so the eval can inject primary failure. |
| "Online metrics are PM's job" | The spec needs to name them so you know what offline success translates to. If you don't know the online metric, you can't pick the offline threshold. |

## Red Flags

- Spec has metrics without current baseline values — you'll optimize blind.
- Spec names a model before naming the metric — cart before horse.
- Spec has no fallback section — production will fail in ways the spec didn't consider.
- Spec has no slicing plan — aggregate-only metrics hide slice regressions.
- Spec confuses offline and online metrics — "we'll see recall improve in production" without naming the online signal is hand-waving.
- Spec has no open questions — every real spec has unknowns; claiming none means you haven't thought hard enough.
- Agent starts coding before spec is approved — block, redirect to spec.

## Verification

Before this skill is complete:

- **Spec doc exists** at a discoverable path, committed.
- **Problem statement** is one sentence, agreed by user.
- **Success criteria** lists 2-5 metrics with current + target + tolerance.
- **Data plan** names sources, split strategy, golden set freeze date.
- **Eval plan** is runnable from the spec alone (metric formulas, judge config, slicing).
- **Fallback plan** names the ladder and which level the eval tests.
- **Risks** listed with severity; irreversible ones flagged for ADRs.
- **Open questions** listed (even if empty after user answers).
- **Approval**: explicit user "go" before coding begins.
