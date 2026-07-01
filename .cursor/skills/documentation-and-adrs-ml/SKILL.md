---
name: documentation-and-adrs-ml
description: Guides agents through writing Architecture Decision Records (ADRs) for ML-specific decisions and runbooks for ML systems. Use when making irreversible ML decisions (model choice, threshold, schema), shipping a feature, or documenting a system for handover/on-call.
---

# documentation-and-adrs-ml

## Overview

Document the **why**, not the what (code shows what). Two artifacts matter most for ML systems: **ADRs** (decisions that are expensive to reverse — model choice, threshold, schema, eval framework) and **runbooks** (what to do when the alert fires). ML systems without these rot fast — the people who built them leave, and the systems become unfixable.

## When to Use

- Making an irreversible ML decision (model choice, threshold, schema, eval framework, golden set definition)
- Shipping a feature (write the ADR + runbook with it)
- On-call runbook for a new alert
- Handover / onboarding a new engineer to a system
- After an incident (`ml-incident-response` post-mortem may spawn ADRs)

Do **not** use for: trivial reversible changes (just do them + commit message), or API reference docs (auto-generate from code).

## Process

1. **Decide: is this an ADR-worthy decision?**
   - ADR-worthy: expensive to reverse, affects multiple people / teams, sets a precedent, irreversibly commits resources (training run, data migration, schema).
   - Not ADR-worthy: trivial, reversible, local to one file.
   - Exit criteria: yes/no with reason.

2. **If yes — write the ADR.**
   - Filename: `docs/adrs/NNNN-short-title.md` (NNNN = sequential number, zero-padded).
   - Sections:
     - **Title + status** (Proposed / Accepted / Superseded / Deprecated) + date + deciders
     - **Context** — what's the problem? what constraints? what's known?
     - **Decision** — what we decided
     - **Alternatives considered** — what else was on the table, why we didn't pick it
     - **Consequences** — positive, negative, neutral
     - **Rollback plan** — how to undo this if it goes wrong (if reversible; if not, mitigation)
   - Exit criteria: ADR committed with all sections.

3. **For ML-specific decisions, add ML-specific content.**
   - **Model choice ADR**: which model, why, alternatives benchmarked (with eval numbers), cost/latency tradeoff, fallback plan, version pin strategy.
   - **Threshold ADR**: which metric, which slice, current value, new value, tolerance, eval evidence (sliced), rollback (revert to old threshold).
   - **Schema ADR**: old schema, new schema, migration plan, backward-compat window, deprecation timeline.
   - **Eval framework ADR**: which framework (DeepEval, RAGAS, custom), why, golden set plan, judge config, regression tolerance, CI gate rules.
   - Exit criteria: ML-specific section present with evidence (eval numbers, not opinions).

4. **Write the runbook (for shipped systems).**
   - Filename: `docs/runbooks/<system>.md` or per-alert `docs/runbooks/<alert-name>.md`.
   - Sections:
     - **What this alert means** — symptom, what users experience
     - **How to investigate** — which dashboard, which trace query, which log query, key signals to check first
     - **Common causes** — top 3-5 root causes from past incidents
     - **Mitigation steps** — immediate actions to restore users (rollback / flag flip / fallback / disable)
     - **Escalation** — who to page, when, with what context
     - **Post-incident** — link to `ml-incident-response` for RCA + post-mortem
   - Exit criteria: runbook committed, linked from the alert.

5. **Keep docs next to code.**
   - ADRs in `docs/adrs/` in the same repo as the code. Not a separate wiki. Wiki links rot; repo ADRs travel with the code.
   - Runbooks in `docs/runbooks/` likewise.
   - Exit criteria: docs in the repo, discoverable from `README.md` index.

6. **Number ADRs sequentially, never reuse numbers.**
   - Superseding an ADR: write a new ADR (NNNN+1) that references the old, mark old as Superseded.
   - Don't edit an accepted ADR to change the decision — that erases history.
   - Exit criteria: ADR numbering monotonic; supersession chain clear.

7. **Link from PRs and commits.**
   - PR that implements an ADR: "Implements ADR-NNNN" in the description.
   - Commit that introduces a decision: "ADR-NNNN: <decision>" in the message.
   - Exit criteria: bidirectional links (ADR references PR, PR references ADR).

## ADR template

```markdown
# ADR-NNNN — [Short title]

- **Status**: Proposed | Accepted | Superseded by ADR-MMMM | Deprecated
- **Date**: YYYY-MM-DD
- **Deciders**: [who]

## Context
[Problem, constraints, what's known.]

## Decision
[What we decided.]

## Alternatives considered
- [Alt 1] — [why not]
- [Alt 2] — [why not]

## Consequences
- Positive: [...]
- Negative: [...]
- Neutral: [...]

## Rollback plan
[How to undo, or mitigation if irreversible.]
```

## Rationalizations

| Excuse | Rebuttal |
|---|---|
| "ADRs slow us down" | An ADR is 30 minutes. Reversing an undocumented irreversible decision is weeks. ADRs are faster. |
| "We'll document it later" | Later, the people who decided will have left, and the decision will be irrecoverable. Document at decision time. |
| "Runbooks are bureaucratic" | On-call without a runbook pages you at 3am with no idea what to do. Runbooks are sleep protection. |
| "The code is self-documenting" | Code shows what, not why. Why did we pick threshold 0.7 not 0.8? Code can't tell you. ADR can. |
| "ADRs go in the wiki" | Wiki links rot, wikis get migrated, search breaks. Repo ADRs travel with the code and stay findable. |
| "Just update the old ADR with the new decision" | Erases history. Write a new ADR that supersedes the old; mark old as Superseded. |
| "This decision is obvious, no ADR needed" | If it's obvious, the ADR is short. If you can't write it, it wasn't obvious. |
| "Runbook can be added when there's an incident" | Then you'll have the incident before the runbook. Write it when you ship the alert. |

## Red Flags

- ADR with no "Alternatives considered" section — decision wasn't actually considered, just picked.
- ADR with no rollback plan — irreversible decision with no undo path.
- ADR that's been edited to change the decision — history erased; write a superseding ADR instead.
- Runbook that says "investigate the issue" with no concrete dashboard / query / signal — useless at 3am.
- ADRs in a separate wiki, not the repo — link rot, search rot, code-doc drift.
- Threshold / model change shipped with no ADR — the next person will reverse it accidentally.
- ADR references eval numbers but the eval output isn't linked — claims without evidence.
- Runbook missing for an active alert — on-call pages you, not the runbook.

## Verification

Before this skill is complete:

- **ADR-worthy check**: yes/no decision recorded with reason.
- **ADR written**: all sections present (status, context, decision, alternatives, consequences, rollback).
- **ML-specific content**: present for ML decisions (model, threshold, schema, eval) with eval evidence linked.
- **Runbook**: for shipped systems, committed and linked from the alert.
- **Location**: ADRs in `docs/adrs/`, runbooks in `docs/runbooks/`, both in the same repo as code.
- **Numbering**: sequential, monotonic; supersession chain clear.
- **Bidirectional links**: ADR ↔ PR / commit.
- **README index**: ADRs and runbooks discoverable from the repo `README.md`.
