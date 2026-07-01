# SKILL.md anatomy — format spec

Every skill in this pack follows the same structure. Skills are **process workflows an agent follows**, not reference docs an agent reads once.

## Required structure

```markdown
---
name: lowercase-hyphen-name
description: Guides agents through [task]. Use when [trigger condition].
---

# [Skill name]

## Overview
1-2 sentences: what this skill does. Generic — no project-specific references.

## When to Use
Trigger conditions expressed as **work-types**, not project layers.
Examples: "starting a new ML feature", "tests fail with non-deterministic
output", "before merging a model change". Avoid: "when working on layer L1".

## Process
Step-by-step workflow. Each step has:
- **Action** — what the agent does
- **Exit criteria** — when to move to the next step (verifiable, not "feels right")

Example:
1. State the eval hypothesis — metric, current baseline, target, reason for
   expected change. Exit: hypothesis written in spec/ADR or chat.
2. Implement the smallest change that could move the metric. Exit: code written.
3. Run eval. Exit: `make eval` (or equivalent) prints delta vs baseline.

## Rationalizations
Table of excuses the agent might use to skip steps, with rebuttals.
This is the **anti-rationalization** layer — it makes the skill robust to
LLM self-justification.

| Excuse | Rebuttal |
|---|---|
| "I'll add eval after it works" | Eval-after-working usually means eval-never. Add the eval harness first; it shapes the implementation. |
| "The change is too small to need a spec" | Small changes can still regress slices. State the metric delta you expect in one line — that's the spec. |

## Red Flags
Signs the workflow is going off the rails. Stop and reassess when these appear.

- Agent cannot name the metric the change should move
- Agent edits `baseline.json` or threshold without an ADR
- Agent ships without an eval delta
- Agent explains away a sliced regression with an aggregate metric

## Verification
Evidence required before the skill is considered complete. "Seems right" is
never sufficient.

- Eval run output (delta vs baseline, sliced breakdown)
- Benchmark numbers (latency p50/p95/p99, cost per 1K requests)
- Trace ID or observability dashboard link (for production-facing changes)
- ADR link (for irreversible decisions)
- Test output (for code-level changes)
```

## Design choices (borrowed from addyosmani/agent-skills)

- **Process, not prose.** Each skill is a workflow with steps and exit criteria — not a reference doc.
- **Anti-rationalization.** Every skill includes the excuses-vs-rebuttals table. This is the layer that prevents LLMs from silently skipping steps.
- **Verification is non-negotiable.** Every skill ends with concrete evidence requirements.
- **Progressive disclosure.** `SKILL.md` is the entry point. Supporting references load only when needed — keep `SKILL.md` lean (target ≤ 100 lines).
- **Trigger by work-type, not project layer.** Skills activate based on what the agent is doing, not where in some architecture the work lands.

## Naming

- `lowercase-hyphen-name` — same convention as addyosmani.
- Avoid prefixes like `ml-` unless needed for conflict avoidance in target repos. Default names are generic and descriptive.
- One skill per directory: `skills/<name>/SKILL.md`.

## Portability check (run before committing any skill)

```bash
grep -ri "applied-ai-lab\|L1\b\|L8\b\|8-layer\|scanit\|got.it\|vg corp\|golf" .claude/skills/ .claude/agents/ .claude/commands/ .cursor/rules/
```

Must return **0 matches**. If any match: rewrite the offending line in generic terms ("your eval harness", "your model gateway", "a fraud detection model", "a RAG system").
