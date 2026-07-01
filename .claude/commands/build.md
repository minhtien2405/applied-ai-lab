---
description: Implement the next slice from a plan — thin vertical slice with eval + atomic commit. Activates incremental-implementation + eval-driven-development.
---

Activate the `incremental-implementation` and `eval-driven-development` skills. Implement the slice I name below.

Rules:
1. Smallest change that delivers the slice's value. No speculative abstraction, no scaffolding for future slices.
2. Add or update the eval case that proves the slice works. Eval comes with the slice, not after.
3. Run eval. Confirm the slice's metric moves as expected, no slice regresses beyond tolerance. Show me the delta.
4. If the change introduces new behavior or new external dependency → feature flag + fallback path. Don't ship unflagged to main.
5. Atomic commit at the end: code + eval case + (if changed) baseline update with ADR link. Commit message says what + why + eval delta.
6. Don't touch code unrelated to this slice (Karpathy "Surgical Changes"). If you notice dead code, mention it — don't delete it.

If eval fails or regresses: stop, don't ship. Report what failed and propose one-variable-at-a-time iteration.

Slice: $ARGUMENTS
