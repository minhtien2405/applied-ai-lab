---
description: Decompose a spec into small, verifiable slices with acceptance criteria and dependency order. Inline planning (no separate skill).
---

Read the spec at the path below (or the spec I describe) and decompose it into thin vertical slices for `incremental-implementation`.

For each slice, give me:
- **Slice name** (one sentence)
- **Success criterion** (which metric moves, by how much)
- **Files touched** (rough)
- **Feature flag name** (if risky)
- **Rollback path** (one line: revert / flag flip / version pin)
- **Dependencies** (which slices must come first)

Order slices by risk (riskiest/most-uncertain first) or by foundation (if later slices depend on earlier).

Constraints:
- Target ~100 lines diff per slice. Flag any slice that looks > 300 — split it.
- One variable per slice (don't bundle prompt + retrieval + model in one slice).
- Each slice must have a meaningful eval case — if not, redefine or merge.

Output as a numbered list. Don't write code in this turn.

Spec: $ARGUMENTS
