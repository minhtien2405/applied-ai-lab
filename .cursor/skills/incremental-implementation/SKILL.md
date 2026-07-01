---
name: incremental-implementation
description: Guides agents through implementing ML/LLM/agentic changes as thin vertical slices — each slice ships code + eval + commit, with feature flags and rollback-friendly design. Use when a change touches more than one file, or when the change could affect production behavior.
---

# incremental-implementation

## Overview

Implement changes as **thin vertical slices**: each slice is a coherent end-to-end increment that ships code + eval + commit on its own. Avoid the "build everything, then test, then ship" pattern — it produces large unreviewable PRs and hides regressions until they're expensive to fix.

## When to Use

- Any change touching more than one file
- Any change that could affect production behavior (model, prompt, retrieval, threshold, serving)
- Implementing a spec from `spec-ml-system`
- Fixing a bug that requires touching multiple modules

Do **not** use for: pure refactors that don't change behavior (use unit tests + `code-review-ml`), or trivial one-line changes (just do them and run existing tests).

## Process

1. **Read the spec.**
   - If no spec → redirect to `spec-ml-system` first.
   - Exit criteria: spec read, success criteria understood, open questions resolved.

2. **Decompose into slices.**
   - Each slice: end-to-end coherent (not a horizontal "all the tests" layer), small enough to review in one sitting (~100 lines diff), independently shippable behind a feature flag.
   - Order slices by risk: riskiest/most-uncertain first (fail fast), or foundational-first if later slices depend on it.
   - Exit criteria: slice list with order, each slice's success criterion named.

3. **For each slice:**
   - **a. Implement the smallest change that delivers the slice's value.** No speculative abstractions, no future-slice scaffolding.
   - **b. Add or update eval cases that prove the slice works.** Eval comes with the slice, not after.
   - **c. Run eval.** Confirm the slice's metric moves as expected, no slice regresses.
   - **d. Commit.** Atomic commit: code + eval + result. Commit message says what + why + eval delta.
   - **e. Decide: ship or stack?** Ship the slice (merge to main behind flag) or stack the next slice on top.
   - Exit criteria per slice: code + eval + commit + (optional) PR.

4. **Use feature flags for risky slices.**
   - New behavior behind a flag, default off. Roll out gradually (internal → canary → % of traffic → 100%).
   - Old behavior stays until the flag is fully rolled out and stable.
   - Exit criteria: flag name + rollout plan + kill switch documented.

5. **Make changes rollback-friendly.**
   - Reversible: feature flag flip, model version pin, config revert. Avoid irreversible migrations until the slice is proven.
   - If a slice requires an irreversible change (schema, data migration) → that's an ADR (use `documentation-and-adrs-ml`) and a separate, well-reviewed PR.
   - Exit criteria: each slice has a documented rollback path.

6. **Keep slices small enough to review.**
   - Target ~100 lines diff per slice. If a slice grew past 300 lines, split it.
   - If you can't describe a slice in one sentence, it's too big.
   - Exit criteria: slice description fits in one sentence + commit subject.

7. **Final PR: aggregate the slices (if stacked).**
   - If slices were stacked, the final PR is the sum. Reviewer sees the slice-by-slice commits, which is the review narrative.
   - Exit criteria: PR opened with eval evidence across all slices, slice commits in order.

## Rationalizations

| Excuse | Rebuttal |
|---|---|
| "It's faster to build it all then test" | Faster to write, slower to ship. Large untested-until-the-end changes hide regressions and produce unreviewable PRs. |
| "I'll add the feature flag in a follow-up" | Flag-in-follow-up means you've already shipped unflagged. Add the flag with the slice or don't ship the slice. |
| "The slice is too small to commit on its own" | Small commits are good. They're easier to revert, easier to review, and they tell the story of the change. |
| "Eval for this slice isn't meaningful yet" | Then the slice isn't delivering value yet. Either redefine the slice so it has meaningful eval, or merge it with the next slice. |
| "Rollback plan is overkill for this size" | Rollback plan is one line: "revert commit X" or "flip flag Y". Cheaper than you think. Skip it and you'll wish you hadn't. |
| "The reviewer can just read the final PR" | They'll miss things in a 1000-line diff. Slice-by-slice commits give them a narrative. |

## Red Flags

- PR diff > 300 lines and not split into slices — block, request decomposition.
- Slice touches multiple concerns (prompt + retrieval + model) in one commit — request one-variable-at-a-time.
- New behavior not behind a feature flag, shipped straight to main — challenge.
- Slice has no eval case — block, the slice isn't proven.
- Commit message says "implement feature X" without naming the metric delta — request the eval result.
- Irreversible change (schema, migration) bundled with behavior change — request split.
- Agent says "I'll clean up the old code after this merges" — that cleanup is debt that compounds. Include the cleanup in the slice or write a follow-up issue immediately.

## Verification

Before this skill is complete:

- **Slice list**: each slice described in one sentence, ordered, with success criterion.
- **Per slice**: code + eval case + eval result + atomic commit.
- **Feature flags**: new behavior flagged, rollout plan + kill switch documented.
- **Rollback path**: each slice has a one-line rollback (revert / flag flip / version pin).
- **PR (if applicable)**: diff under ~300 lines, or split into multiple PRs; slice commits in order; eval evidence attached.
- **No orphans**: changes that became unused because of this work are removed (or noted as follow-up issues).
