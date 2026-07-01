---
description: Run the eval harness and report delta vs baseline with sliced breakdown. Primary verification for ML/LLM/agentic changes. Activates eval-driven-development.
---

Activate the `eval-driven-development` skill. Run the project's eval harness and report results.

Steps:
1. Confirm the eval harness is runnable. If not, say so and stop — don't claim a result without running.
2. Run eval on the current (changed) state.
3. Run eval on the baseline state if the baseline result isn't already cached / recent.
4. Report:
   - **Aggregate delta** vs baseline (per metric)
   - **Per-slice delta** vs baseline (per slicing dimension)
   - **Cost / latency delta** (if applicable)
   - **Judge variance estimate** (if LLM judge; N runs)
   - **Any slice regressing beyond tolerance** — flagged as block
5. One-paragraph honest read: what improved, what didn't, what's ambiguous. No cherry-picking.
6. Verdict: ship / iterate / revert — with reason.

If eval is flaky (variance > delta), say so — don't claim a real delta. Propose how to reduce variance (N runs, deterministic seed, lower-variance judge).

If a slice regressed beyond tolerance, block — even if aggregate improved.

Run target: $ARGUMENTS
