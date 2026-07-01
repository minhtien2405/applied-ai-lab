---
description: Write an ADR for an irreversible ML decision (model choice, threshold, schema, eval framework). Activates documentation-and-adrs-ml.
---

Activate the `documentation-and-adrs-ml` skill. Write an ADR for the decision below.

Output a markdown ADR with these sections:
- **Title + Status** (Proposed) + Date + Deciders
- **Context** — problem, constraints, what's known
- **Decision** — what we decided
- **Alternatives considered** — what else was on the table, why not (with eval numbers where applicable)
- **Consequences** — positive / negative / neutral
- **Rollback plan** — how to undo, or mitigation if irreversible

For ML-specific decisions, include:
- **Model choice**: which model, why, alternatives benchmarked (with eval numbers), cost/latency tradeoff, fallback plan, version pin
- **Threshold**: which metric, which slice, current value, new value, tolerance, eval evidence (sliced), rollback
- **Schema**: old, new, migration plan, backward-compat window, deprecation timeline
- **Eval framework**: which framework, why, golden set plan, judge config, regression tolerance, CI gate rules

Pick a filename `docs/adrs/NNNN-short-title.md` — find the highest existing NNNN in `docs/adrs/` and increment. Don't reuse numbers. If superseding an existing ADR, mark the old as "Superseded by ADR-MMMM" and write the new one separately.

Link the ADR from any implementing PR. Don't edit an accepted ADR to change the decision — supersede instead.

Decision: $ARGUMENTS
