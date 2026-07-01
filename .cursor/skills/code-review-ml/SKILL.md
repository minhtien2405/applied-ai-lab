---
name: code-review-ml
description: Guides agents through reviewing ML/LLM/agentic code changes on five axes — correctness, eval discipline, production-readiness, honesty, maintainability — with a "would a staff ML engineer approve?" bar. Use before merging any ML-relevant change, or when reviewing a peer's PR.
---

# code-review-ml

## Overview

Review ML/LLM/agentic changes on five axes, with a staff-engineer bar. ML code review is stricter than generic code review because the failure modes are subtler (data leakage, judge variance, fallback storms, slice regressions hidden by aggregates) and the claims are easier to inflate.

## When to Use

- Before merging any change that touches model, prompt, retrieval, threshold, data, or serving
- Reviewing a peer's ML PR
- Self-review before opening a PR
- When a hook (`pre-commit-eval-reminder`) fires

Do **not** use for: pure docs, pure formatting, or trivial changes with no ML behavior impact.

## Process

1. **Read the spec (if exists) and the PR description.**
   - What was the change supposed to do? What metric was it supposed to move?
   - Exit criteria: you can state the change's intent in one sentence before reading the diff.

2. **Read the diff slice-by-slice.**
   - Look at commits individually (assumes `incremental-implementation` was followed).
   - Exit criteria: each commit's intent understood.

3. **Run the five-axis review.**

   **Axis 1 — Correctness**
   - Does the code do what the spec says?
   - Edge cases handled (empty input, null, malformed, timeout)?
   - Data flow: are features point-in-time correct? Train/eval split defensible?
   - Caching: keys correct, TTL sane, invalidation handled?
   - Concurrency: race conditions in model calls, fallback paths?

   **Axis 2 — Eval discipline**
   - Eval case added or updated for the change?
   - Eval result attached to the PR (aggregate + sliced)?
   - Baseline unchanged without ADR (check `baseline.json` diff)?
   - LLM judge variance accounted for (N runs, deterministic seed)?
   - No slice regression beyond tolerance?

   **Axis 3 — Production-readiness**
   - Fallback path exists for new external dependency?
   - Feature flag in place for risky change?
   - Observability added (trace fields, metrics, logs) — not "after launch"?
   - Cost delta estimated (per-1K-requests)?
   - Rollback path documented (revert / flag flip / version pin)?

   **Axis 4 — Honesty**
   - Claims in PR description match eval evidence?
   - No over-claim of ownership ("I built X" when teammate did — check git blame)?
   - No inflated metric without population + comparison baseline named?
   - Offline-vs-online gap stated honestly ("offline +X, online validation pending")?
   - No silent baseline / threshold / golden-set edit?

   **Axis 5 — Maintainability**
   - Code readable, names clear, no clever tricks?
   - No speculative abstraction (per Karpathy "Simplicity First")?
   - No orphaned code from this change (unused imports, dead functions)?
   - Matched existing style, not "improved" adjacent code (per "Surgical Changes")?
   - Tests / eval cases will fail loudly if the change regresses?

   Exit criteria: each axis has a verdict (approve / request changes / block) + 1-line justification.

4. **Assign severity to each comment.**
   - **Block**: must fix before merge (data leakage, eval missing, slice regression unaddressed, no fallback for new external dep).
   - **Request changes**: should fix before merge, but PR is fundamentally OK.
   - **Nit**: optional, won't block merge.
   - **FYI**: comment for the author's awareness, no action expected.
   - Exit criteria: every comment has a severity label.

5. **Write the review summary.**
   - Verdict (approve / request changes / block) + 1-paragraph rationale + top 1-2 things to fix.
   - Use the staff-engineer bar: "would a staff ML engineer approve this?" If no, what's missing?
   - Exit criteria: summary comment posted on the PR.

6. **Don't merge on the author's say-so.**
   - If you're the reviewer and the author says "trust me, eval is fine" — demand the eval output.
   - If you're the author and self-reviewing — be at least as harsh as a peer would be.
   - Exit criteria: every claim has evidence in the PR.

## Rationalizations

| Excuse | Rebuttal |
|---|---|
| "It's a small PR, full review is overkill" | Small ML PRs still regress slices. Five-axis review on a 20-line PR takes 5 minutes. |
| "The eval passed, so it's fine" | Eval passing aggregate doesn't mean no slice regression. Check the sliced breakdown. |
| "Fallback can be added later" | Then the change isn't production-ready. Block until fallback exists and is tested. |
| "The reviewer can take my word for the metric" | ML claims are easy to inflate. Demand the eval output attached. |
| "This is how the previous code did it" | The previous code might be wrong. Don't propagate bugs. |
| "The threshold change is trivial" | Threshold changes affect users. Demand an ADR + before/after sliced eval. |
| "It's just a prompt tweak" | Prompt tweaks move metrics. Demand the eval hypothesis + delta. |
| "I don't want to be that reviewer" | The kind reviewer lets bugs reach production. Be the reviewer who catches things in PR, not in post-mortem. |

## Red Flags

- PR has no eval evidence attached — block.
- `baseline.json` changed with no ADR link — block.
- PR claims "production +X%" from offline eval alone — challenge.
- PR bundles multiple changes (prompt + retrieval + model) in one diff — request split.
- Reviewer comments only on style, not on eval/slices/fallback — they're reviewing the wrong axis.
- Author responds to "where's the eval?" with "trust me" — block.
- New external dependency has no fallback — block.
- Sliced eval missing, only aggregate reported — request sliced breakdown.
- Code "improves" adjacent unrelated code — request revert of the orthogonal changes.

## Verification

Before this skill is complete:

- **Five-axis verdict**: each axis has approve / request changes / block + 1-line justification.
- **Severity labels**: every review comment labeled (Block / Request changes / Nit / FYI).
- **Summary comment**: verdict + rationale + top 1-2 fixes, posted on PR.
- **Staff-engineer bar**: explicit answer to "would a staff ML engineer approve this?" — if no, what's missing is named.
- **Evidence-backed**: every challenge the reviewer raises is either resolved with evidence in the PR or remains a block.
- **No silent merges**: PR is not merged while any Block comment is unresolved.
