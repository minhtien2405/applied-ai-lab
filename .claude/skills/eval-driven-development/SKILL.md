---
name: eval-driven-development
description: Guides agents through making any model/prompt/retrieval/data change eval-driven — state the metric delta hypothesis, run eval, prove the change moves the metric, ship only with evidence. Use when changing any ML/LLM/agentic/RAG component, before merging or claiming improvement.
---

# eval-driven-development

## Overview

Every change to an ML/LLM/agentic system — model, prompt, retrieval, threshold, data, serving config — must be **eval-driven**: you state the expected metric delta before coding, you run the eval after, you ship only if the delta is real and no slice regresses beyond tolerance. "I think it's better" is not sufficient evidence.

This is the **primary verification skill** for the pack. Unit tests verify code; eval verifies ML behavior.

## When to Use

- Changing a prompt template, system prompt, or few-shot examples
- Swapping or upgrading a model (foundation, fine-tuned, embedding, reranker)
- Changing retrieval (chunking, top-k, hybrid weights, rerank strategy)
- Tuning a threshold, cutoff, or routing rule
- Updating training data, golden set, or eval set
- Changing serving config (fallback order, cache TTL, batch size)
- Any PR that claims a quality / latency / cost improvement

Do **not** use for: pure refactors that don't change behavior (use `incremental-implementation` + unit tests), pure docs/ADRs (use `documentation-and-adrs-ml`).

## Process

1. **State the eval hypothesis** (before coding).
   - Metric name + current baseline value + target value + reason for expected change.
   - Example: "faithfulness currently 0.82, target ≥ 0.86, expected because new prompt explicit about citing sources".
   - Exit criteria: hypothesis written in the spec, ADR, or chat message — not just in your head.

2. **Confirm the eval harness exists and is runnable.**
   - If no eval harness exists yet → build one first (golden set + metric + runner). This is non-negotiable.
   - If harness exists but golden set is unfrozen → freeze it before proceeding. Optimizing against an unfrozen golden set is leakage.
   - Exit criteria: `make eval` (or equivalent) runs and produces a delta-vs-baseline report.

3. **Run eval on the unchanged baseline (if not already recent).**
   - Establishes the "before" number. Don't skip — your memory of last week's number is not reliable.
   - Exit criteria: baseline eval result recorded with timestamp + model/prompt version.

4. **Implement the smallest change that could move the metric.**
   - One variable at a time. Don't bundle prompt + retrieval + model changes in one eval run — you won't know which caused the delta.
   - Exit criteria: code change is minimal, traceable to the hypothesis.

5. **Run eval on the changed version.**
   - Capture: aggregate delta, per-slice delta, judge variance estimate (if LLM-judge), latency/cost delta.
   - Exit criteria: eval output saved (file, artifact, or pasted into PR).

6. **Read the eval result honestly.**
   - Did the metric move as hypothesized? If not — why? Don't rationalize.
   - Did any slice regress beyond tolerance? If yes — block the merge even if aggregate improved.
   - Did cost / latency regress? Those are regressions too.
   - Exit criteria: a one-paragraph honest read of the result, including the parts that didn't improve.

7. **Ship or iterate.**
   - Ship: eval shows expected delta, no slice regression, no cost/latency regression → PR with eval output attached.
   - Iterate: hypothesis wrong → revise hypothesis, change one variable, rerun. Don't keep changing blindly.
   - Revert: change made things worse → revert and write a one-line note about why (becomes ADR fuel).
   - Exit criteria: PR merged with eval evidence, OR revert with note, OR revised hypothesis for next iteration.

## Rationalizations

| Excuse | Rebuttal |
|---|---|
| "I'll add eval after it works" | Eval-after-working usually means eval-never. The eval harness shapes the implementation — build it first. |
| "The change is too small to need eval" | Small changes can still regress slices. State the expected delta in one line — that's the eval hypothesis. |
| "Eval is flaky so the delta isn't trustworthy" | Then fix the eval (larger N, lower-variance judge, deterministic seed) before claiming anything about the change. Flaky eval means you can't ship — not that you can ship without evidence. |
| "Aggregate improved by 5 points, that's a win" | Aggregate can hide slice regressions. Show sliced breakdown. A 5-point aggregate win with a 10-point slice regression is a bug, not a win. |
| "Offline looks good, ship it" | Offline is necessary, not sufficient. For user-facing changes, name the online validation plan (A/B, shadow, canary). Don't claim production win from offline alone. |
| "The judge is an LLM, it's noisy, just trust my read" | LLM judge variance is exactly why you need N>1 and a delta-vs-baseline, not single-shot judgments. If variance is too high to detect your delta, your delta isn't real. |
| "I tweaked the baseline to reflect the new expected behavior" | That's tuning the baseline to pass. Baseline updates need an ADR + a fresh eval run proving the new baseline is real. |
| "We don't have time for eval this sprint" | Then you don't have time to ship the change either. Ship-without-eval is debt that compounds — every future change is harder to validate. |

## Red Flags

- Agent cannot name the metric the change should move — stop and clarify.
- Agent edits `baseline.json` or golden set without an ADR — block.
- Agent ships a PR with no eval output attached — block.
- Agent explains away a sliced regression by pointing at the aggregate — block.
- Agent claims "production improved" from offline eval alone — challenge.
- Agent runs eval once and cherry-picks the best run — demand N runs and report variance.
- Agent bundles multiple changes in one eval run — demand one-variable-at-a-time.
- Agent says "eval is too slow so I skipped it" — eval-too-slow is a problem to fix, not a reason to skip.

## Verification

Before this skill is considered complete, evidence must exist for:

- **Hypothesis**: written before code (timestamp proves order — e.g. in spec/ADR/issue comment).
- **Baseline eval**: a "before" run with timestamp + version pin (model, prompt, retrieval config).
- **Changed eval**: an "after" run on the same harness, same golden set, same judge config.
- **Delta report**: aggregate + sliced breakdown + cost/latency delta, attached to the PR or commit.
- **Honest read**: one paragraph acknowledging what did and didn't improve (no cherry-picking).
- **Slice check**: explicit statement that no slice regressed beyond tolerance (or list of regressing slices and the decision to block/accept).
- **Online validation plan** (if user-facing): A/B, shadow, or canary — named, not hand-waved.

"Seems better" is never sufficient. "Eval moved metric X from W to T, no slice regressed beyond tolerance, cost per 1K requests unchanged" is the minimum acceptable claim.
