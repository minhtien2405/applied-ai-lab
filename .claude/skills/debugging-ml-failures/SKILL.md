---
name: debugging-ml-failures
description: Guides agents through debugging non-deterministic ML/LLM failures — flakiness triage, LLM judge variance vs real regression, reproducibility, stop-the-line rule. Use when tests fail with non-deterministic output, eval regresses inconsistently, or behavior is unexpected and hard to reproduce.
---

# debugging-ml-failures

## Overview

ML failures are non-deterministic in ways traditional bugs aren't: LLM judge variance, sampling temperature, batch composition, cache hits, race conditions in async calls. This skill is a five-step triage: **reproduce, localize, reduce, fix, guard** — with a stop-the-line rule for production-impacting failures and a flakiness-vs-regression decision tree.

## When to Use

- Tests fail with non-deterministic output (pass on retry, fail again later)
- Eval regresses inconsistently across runs
- Production behavior unexpected and hard to reproduce
- LLM judge gives different scores on identical inputs
- A model change "broke something" but you can't pin down what

Do **not** use for: deterministic code bugs (use a normal debugging workflow), production incidents (use `ml-incident-response` first, this skill feeds the RCA step).

## Process

1. **Reproduce.**
   - Don't fix what you can't reproduce. Pin: model version, prompt version, seed, temperature, retrieval state, cache state, golden set version, judge config.
   - If you can't reproduce with everything pinned → the failure involves an uncontrolled variable (time-based data, race condition, cache TTL). Hunt that variable, don't skip repro.
   - Exit criteria: a command that reproduces the failure deterministically (or a documented race-condition repro).

2. **Localize.**
   - Bisect: which change introduced the failure? `git bisect` on commits, or one-variable-at-a-time on (prompt, retrieval, model, threshold).
   - Don't bisect multiple variables at once — you won't know which one caused it.
   - Slice the failure: does it happen on all inputs or one slice? Sliced repro is faster to localize.
   - Exit criteria: one commit (or one variable change) named as the cause.

3. **Reduce.**
   - Minimal repro: smallest input + simplest config that still fails.
   - A 10-token prompt that fails beats a 1000-token prompt that fails — easier to reason about, easier to add as a golden case.
   - For LLM judge variance: reduce to a single (input, expected) pair; run judge N times; measure variance.
   - Exit criteria: minimal repro written down (one-line input + expected + actual).

4. **Decide: flakiness or real regression?**
   - **Flakiness**: same input, same config, different output across runs. Caused by: non-zero temperature, sampling, race conditions, judge variance, time-based data, cache state.
   - **Real regression**: same input, same config, same output — but the output is wrong. Caused by: a code/model/prompt change that deterministically broke something.
   - Mix: a real regression that only manifests on some samples (sliced regression).
   - Exit criteria: classified as flakiness / real / mixed, with evidence (N runs, variance numbers).

5. **Fix.**
   - **Flakiness**: pin the uncontrolled variable (seed=0, temperature=0, deterministic judge, freeze time-based data, disable cache for the test). Don't fix flakiness by retrying until it passes.
   - **Real regression**: revert the offending change OR fix the change. Add a golden case from the minimal repro so it can't regress silently again.
   - **Mixed**: fix the regression AND pin the flakiness.
   - Exit criteria: fix committed + golden case added + eval passes deterministically on N runs.

6. **Guard.**
   - Add the minimal repro as a golden case.
   - Add an eval slice for the affected dimension (so future similar regressions surface in sliced eval, not aggregate).
   - If flakiness was the cause — add a "deterministic mode" CI check that pins all uncontrolled variables, runs eval N times, asserts variance < threshold.
   - Exit criteria: golden case + slice + (if flakiness) deterministic-mode CI check.

7. **Stop-the-line (if production-impacting).**
   - If the failure is impacting production users → stop new deploys, roll back if needed, escalate to `ml-incident-response`. Don't keep developing while production is broken.
   - Exit criteria: production stabilized (rollback / flag flip) before continuing debugging.

## Flakiness-vs-regression decision tree

```text
Run repro 5 times with everything pinned:
├── All 5 fail identically          → Real regression
├── Some pass, some fail            → Flakiness (or mixed)
│   ├── Disable cache, retry        → still flaky? cache state
│   ├── Set seed=0, temp=0, retry   → still flaky? judge variance or race
│   └── Freeze golden set, retry    → still flaky? golden set unfrozen
└── All 5 pass (but failed first)   → Flakiness; capture next failure
```

## Rationalizations

| Excuse | Rebuttal |
|---|---|
| "It passed on retry, ship it" | Retry-passing is flakiness, not a fix. The failure will return in production. |
| "Can't reproduce, but the fix is obvious" | If you can't reproduce, you can't verify the fix. You'll ship a fix for a bug you don't understand. |
| "The judge is just noisy, ignore variance" | Noisy judge means you can't detect real regressions either. Fix the judge (N runs, deterministic config, lower-variance model). |
| "I'll bisect all variables at once" | You won't know which one caused it. One variable at a time. |
| "Adding a golden case is overkill for a one-off" | The one-off will recur. Golden case is cheap insurance. |
| "Stop-the-line is too disruptive" | Production-impacting failures get worse the longer you let them run. Stop, stabilize, then debug. |
| "Flakiness is just how LLMs are" | LLM output can be made deterministic (temp=0, seed). Judge variance can be reduced (N runs, better judge). "Inherent flakiness" is usually fixable. |

## Red Flags

- "Can't reproduce" followed by a fix anyway — fix is unverified.
- Retry-until-pass as a "fix" — flakiness hidden, not fixed.
- Bisecting multiple variables simultaneously — can't isolate cause.
- No minimal repro — debugging in the dark.
- Judge variance unmeasured — can't tell flakiness from regression.
- No golden case added after a fix — same bug will recur silently.
- Production-impacting failure debugged without rollback — failure continues while you debug.
- "It's just LLM noise" without pinning temperature/seed — dismissal, not diagnosis.

## Verification

Before this skill is complete:

- **Repro**: a command that reproduces the failure deterministically (or a documented race).
- **Localization**: one commit / one variable change named as the cause.
- **Minimal repro**: one-line input + expected + actual.
- **Classification**: flakiness / real / mixed, with N-run evidence.
- **Fix**: committed; addresses the root cause (not retry-until-pass).
- **Golden case**: minimal repro added as an eval case.
- **Slice**: affected dimension added to sliced eval.
- **Deterministic-mode CI** (if flakiness): pins uncontrolled variables, runs N times, asserts variance.
- **Stop-the-line** (if production-impacting): rollback / flag flip completed before debugging continued.
